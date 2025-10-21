"""
Security utilities and middleware for request validation and sanitization
"""
import re
import html
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class SecurityUtils:
    """Utility class for security-related operations"""
    
    # Common XSS patterns
    XSS_PATTERNS = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'on\w+\s*=',
        r'<iframe[^>]*>.*?</iframe>',
        r'<object[^>]*>.*?</object>',
        r'<embed[^>]*>.*?</embed>',
        r'<link[^>]*>',
        r'<meta[^>]*>',
        r'<style[^>]*>.*?</style>',
    ]
    
    # SQL injection patterns
    SQL_PATTERNS = [
        r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION)\b)',
        r'(\b(OR|AND)\s+\d+\s*=\s*\d+)',
        r'(\b(OR|AND)\s+[\'"][^\'"]*[\'"])',
        r'(--|#|/\*|\*/)',
        r'(\bUNION\s+SELECT\b)',
        r'(\bINTO\s+OUTFILE\b)',
    ]
    
    @classmethod
    def sanitize_html(cls, text: str) -> str:
        """Sanitize HTML content to prevent XSS"""
        if not text:
            return text
        
        # HTML encode the text
        sanitized = html.escape(text)
        
        # Remove potentially dangerous patterns
        for pattern in cls.XSS_PATTERNS:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE | re.DOTALL)
        
        return sanitized
    
    @classmethod
    def validate_no_sql_injection(cls, text: str) -> bool:
        """Check if text contains potential SQL injection patterns"""
        if not text:
            return True
        
        text_upper = text.upper()
        
        for pattern in cls.SQL_PATTERNS:
            if re.search(pattern, text_upper, re.IGNORECASE):
                return False
        
        return True
    
    @classmethod
    def validate_email_format(cls, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @classmethod
    def validate_url(cls, url: str, allowed_schemes: List[str] = None) -> bool:
        """Validate URL format and scheme"""
        if not url:
            return False
        
        if allowed_schemes is None:
            allowed_schemes = ['http', 'https']
        
        try:
            parsed = urlparse(url)
            return parsed.scheme in allowed_schemes and parsed.netloc
        except Exception:
            return False
    
    @classmethod
    def sanitize_filename(cls, filename: str) -> str:
        """Sanitize filename to prevent directory traversal"""
        if not filename:
            return filename
        
        # Remove path separators and dangerous characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
        sanitized = re.sub(r'\.\.', '', sanitized)  # Remove parent directory references
        sanitized = sanitized.strip('. ')  # Remove leading/trailing dots and spaces
        
        return sanitized
    
    @classmethod
    def validate_password_strength(cls, password: str) -> Dict[str, Any]:
        """Validate password strength and return detailed feedback"""
        if not password:
            return {"valid": False, "errors": ["Password is required"]}
        
        errors = []
        
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        
        if len(password) > 128:
            errors.append("Password must be less than 128 characters long")
        
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        
        if not re.search(r'\d', password):
            errors.append("Password must contain at least one digit")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character")
        
        # Check for common weak passwords
        weak_patterns = [
            r'password',
            r'123456',
            r'qwerty',
            r'admin',
            r'letmein',
        ]
        
        for pattern in weak_patterns:
            if re.search(pattern, password.lower()):
                errors.append("Password contains common weak patterns")
                break
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "strength": cls._calculate_password_strength(password)
        }
    
    @classmethod
    def _calculate_password_strength(cls, password: str) -> str:
        """Calculate password strength score"""
        score = 0
        
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if re.search(r'[a-z]', password):
            score += 1
        if re.search(r'[A-Z]', password):
            score += 1
        if re.search(r'\d', password):
            score += 1
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1
        if len(set(password)) > len(password) * 0.7:  # Character diversity
            score += 1
        
        if score <= 2:
            return "weak"
        elif score <= 4:
            return "medium"
        elif score <= 6:
            return "strong"
        else:
            return "very_strong"


class SecurityMiddleware(BaseHTTPMiddleware):
    """Middleware for request security validation and sanitization"""
    
    def __init__(self, app, max_request_size: int = 10 * 1024 * 1024):  # 10MB default
        super().__init__(app)
        self.max_request_size = max_request_size
        self.security_utils = SecurityUtils()
    
    async def dispatch(self, request: Request, call_next):
        """Process request for security validation"""
        
        # Check request size
        content_length = request.headers.get('content-length')
        if content_length and int(content_length) > self.max_request_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Request too large"
            )
        
        # Add security headers to response
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' https:; "
            "connect-src 'self' https:; "
            "frame-ancestors 'none';"
        )
        
        # Remove server information
        if "server" in response.headers:
            del response.headers["server"]
        
        return response


class InputValidationMiddleware(BaseHTTPMiddleware):
    """Middleware for input validation and sanitization"""
    
    def __init__(self, app, sanitize_inputs: bool = True):
        super().__init__(app)
        self.sanitize_inputs = sanitize_inputs
        self.security_utils = SecurityUtils()
    
    async def dispatch(self, request: Request, call_next):
        """Validate and sanitize request inputs"""
        
        # Skip validation for certain content types
        content_type = request.headers.get('content-type', '')
        if content_type.startswith('multipart/form-data'):
            # Handle file uploads separately
            return await call_next(request)
        
        # Validate query parameters
        for key, value in request.query_params.items():
            if not self.security_utils.validate_no_sql_injection(value):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid characters in query parameter: {key}"
                )
        
        # Validate path parameters
        for key, value in request.path_params.items():
            if not self.security_utils.validate_no_sql_injection(str(value)):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid characters in path parameter: {key}"
                )
        
        response = await call_next(request)
        return response


def validate_request_data(data: Dict[str, Any], sanitize: bool = True) -> Dict[str, Any]:
    """Validate and optionally sanitize request data"""
    if not isinstance(data, dict):
        return data
    
    validated_data = {}
    security_utils = SecurityUtils()
    
    for key, value in data.items():
        if isinstance(value, str):
            # Check for SQL injection
            if not security_utils.validate_no_sql_injection(value):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid characters in field: {key}"
                )
            
            # Sanitize HTML if requested
            if sanitize:
                value = security_utils.sanitize_html(value)
        
        elif isinstance(value, dict):
            value = validate_request_data(value, sanitize)
        
        elif isinstance(value, list):
            value = [
                validate_request_data(item, sanitize) if isinstance(item, dict)
                else security_utils.sanitize_html(item) if isinstance(item, str) and sanitize
                else item
                for item in value
            ]
        
        validated_data[key] = value
    
    return validated_data