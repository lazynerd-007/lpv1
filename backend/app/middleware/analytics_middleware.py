"""
Middleware for automatic analytics tracking
"""
import time
import json
from typing import Callable, Optional
from uuid import UUID
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse

from app.services.analytics_service import AnalyticsService
from app.db.database import get_db
from app.auth.dependencies import get_current_user_optional


class AnalyticsMiddleware(BaseHTTPMiddleware):
    """Middleware to automatically track user activities and system metrics"""
    
    def __init__(self, app, track_system_metrics: bool = True, track_user_activities: bool = True):
        super().__init__(app)
        self.track_system_metrics = track_system_metrics
        self.track_user_activities = track_user_activities
        
        # Define which endpoints to track
        self.tracked_endpoints = {
            "GET /api/v1/movies": "browse_movies",
            "GET /api/v1/movies/{movie_id}": "view_movie",
            "POST /api/v1/reviews": "write_review",
            "POST /api/v1/reviews/{review_id}/vote": "vote_review",
            "POST /api/v1/users/{user_id}/follow": "follow_user",
            "DELETE /api/v1/users/{user_id}/follow": "unfollow_user",
            "POST /api/v1/auth/login": "login",
            "POST /api/v1/auth/logout": "logout",
            "GET /api/v1/users/watchlist": "view_watchlist",
            "POST /api/v1/users/watchlist/{movie_id}": "add_to_watchlist",
            "GET /api/v1/movies/search": "search_movies",
        }
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Get request info
        method = request.method
        path = str(request.url.path)
        endpoint_key = f"{method} {path}"
        
        # Try to match with tracked endpoints (handle path parameters)
        activity_type = None
        for pattern, activity in self.tracked_endpoints.items():
            if self._match_endpoint_pattern(endpoint_key, pattern):
                activity_type = activity
                break
        
        # Get user info if available
        user_id = None
        session_id = None
        try:
            # Extract user from request if authenticated
            if hasattr(request.state, 'user'):
                user_id = request.state.user.id
            # Get session ID from headers or cookies
            session_id = request.headers.get('X-Session-ID') or request.cookies.get('session_id')
        except Exception:
            pass
        
        # Process the request
        response = await call_next(request)
        
        # Calculate response time
        response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Track metrics asynchronously (don't block the response)
        if self.track_system_metrics or (self.track_user_activities and activity_type):
            try:
                # Get database session
                async for db in get_db():
                    analytics_service = AnalyticsService(db)
                    
                    # Track system metrics
                    if self.track_system_metrics:
                        await analytics_service.track_system_metric(
                            metric_name="response_time",
                            metric_value=response_time,
                            metric_unit="ms",
                            component="api",
                            extra_data={
                                "endpoint": endpoint_key,
                                "status_code": response.status_code,
                                "method": method,
                                "path": path
                            }
                        )
                    
                    # Track user activity
                    if self.track_user_activities and activity_type:
                        # Extract resource info from path
                        resource_type, resource_id = self._extract_resource_info(path, activity_type)
                        
                        await analytics_service.track_user_activity(
                            user_id=user_id,
                            activity_type=activity_type,
                            resource_type=resource_type,
                            resource_id=resource_id,
                            session_id=session_id,
                            ip_address=self._get_client_ip(request),
                            user_agent=request.headers.get('User-Agent'),
                            extra_data={
                                "endpoint": endpoint_key,
                                "status_code": response.status_code,
                                "response_time_ms": response_time
                            }
                        )
                    
                    break  # Exit the async generator
            except Exception as e:
                # Log error but don't fail the request
                print(f"Analytics tracking error: {e}")
        
        return response
    
    def _match_endpoint_pattern(self, endpoint: str, pattern: str) -> bool:
        """Check if endpoint matches pattern (handling path parameters)"""
        endpoint_parts = endpoint.split('/')
        pattern_parts = pattern.split('/')
        
        if len(endpoint_parts) != len(pattern_parts):
            return False
        
        for ep, pp in zip(endpoint_parts, pattern_parts):
            if pp.startswith('{') and pp.endswith('}'):
                # This is a path parameter, skip comparison
                continue
            elif ep != pp:
                return False
        
        return True
    
    def _extract_resource_info(self, path: str, activity_type: str) -> tuple[Optional[str], Optional[UUID]]:
        """Extract resource type and ID from path"""
        try:
            path_parts = path.strip('/').split('/')
            
            if 'movies' in path_parts:
                movie_idx = path_parts.index('movies')
                if len(path_parts) > movie_idx + 1:
                    try:
                        movie_id = UUID(path_parts[movie_idx + 1])
                        return "movie", movie_id
                    except ValueError:
                        pass
                return "movie", None
            
            elif 'reviews' in path_parts:
                review_idx = path_parts.index('reviews')
                if len(path_parts) > review_idx + 1:
                    try:
                        review_id = UUID(path_parts[review_idx + 1])
                        return "review", review_id
                    except ValueError:
                        pass
                return "review", None
            
            elif 'users' in path_parts:
                user_idx = path_parts.index('users')
                if len(path_parts) > user_idx + 1:
                    try:
                        user_id = UUID(path_parts[user_idx + 1])
                        return "user", user_id
                    except ValueError:
                        pass
                return "user", None
        
        except Exception:
            pass
        
        return None, None
    
    def _get_client_ip(self, request: Request) -> Optional[str]:
        """Get client IP address from request"""
        # Check for forwarded headers first (for load balancers/proxies)
        forwarded_for = request.headers.get('X-Forwarded-For')
        if forwarded_for:
            return forwarded_for.split(',')[0].strip()
        
        real_ip = request.headers.get('X-Real-IP')
        if real_ip:
            return real_ip
        
        # Fallback to direct client IP
        if hasattr(request, 'client') and request.client:
            return request.client.host
        
        return None


# Helper function to track custom events
async def track_custom_event(
    request: Request,
    activity_type: str,
    resource_type: Optional[str] = None,
    resource_id: Optional[UUID] = None,
    extra_data: Optional[dict] = None
):
    """Helper function to track custom analytics events"""
    try:
        # Get user info
        user_id = None
        if hasattr(request.state, 'user'):
            user_id = request.state.user.id
        
        session_id = request.headers.get('X-Session-ID') or request.cookies.get('session_id')
        
        # Get database session
        async for db in get_db():
            analytics_service = AnalyticsService(db)
            
            await analytics_service.track_user_activity(
                user_id=user_id,
                activity_type=activity_type,
                resource_type=resource_type,
                resource_id=resource_id,
                session_id=session_id,
                ip_address=request.headers.get('X-Forwarded-For', '').split(',')[0].strip() or 
                          request.headers.get('X-Real-IP') or 
                          (request.client.host if request.client else None),
                user_agent=request.headers.get('User-Agent'),
                extra_data=extra_data
            )
            break
    except Exception as e:
        print(f"Custom event tracking error: {e}")


# Content metrics helper
async def track_content_view(content_type: str, content_id: UUID, request: Request):
    """Helper function to track content views"""
    try:
        async for db in get_db():
            analytics_service = AnalyticsService(db)
            
            # Increment view count
            await analytics_service.increment_content_metric(
                content_type=content_type,
                content_id=content_id,
                metric_type="views"
            )
            
            # Track detailed view metric
            await analytics_service.track_content_metric(
                content_type=content_type,
                content_id=content_id,
                metric_type="view",
                extra_data={
                    "user_agent": request.headers.get('User-Agent'),
                    "referer": request.headers.get('Referer'),
                    "ip_address": request.headers.get('X-Forwarded-For', '').split(',')[0].strip() or 
                                request.headers.get('X-Real-IP') or 
                                (request.client.host if request.client else None)
                }
            )
            break
    except Exception as e:
        print(f"Content view tracking error: {e}")