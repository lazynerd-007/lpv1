"""
Comprehensive API documentation index for LemonNPie Backend API
"""
from typing import Dict, Any, List


class APIDocumentation:
    """Central documentation hub for the API"""
    
    DOCUMENTATION_STRUCTURE = {
        "getting_started": {
            "title": "Getting Started",
            "description": "Quick start guide for LemonNPie API",
            "sections": [
                {
                    "title": "Authentication",
                    "description": "How to authenticate with the API",
                    "endpoint": "/docs#/Authentication",
                    "examples": ["register", "login", "token_refresh"]
                },
                {
                    "title": "Making Your First Request",
                    "description": "Step-by-step guide to your first API call",
                    "endpoint": "/docs#/Movies",
                    "examples": ["get_movies", "search_movies"]
                },
                {
                    "title": "Error Handling",
                    "description": "Understanding API error responses",
                    "endpoint": "/docs#/System",
                    "examples": ["validation_error", "authentication_error"]
                }
            ]
        },
        "core_concepts": {
            "title": "Core Concepts",
            "description": "Essential concepts for using the API effectively",
            "sections": [
                {
                    "title": "API Versioning",
                    "description": "How API versioning works",
                    "endpoint": "/api/versions",
                    "key_points": [
                        "URL path versioning (/api/v1/)",
                        "Backward compatibility policy",
                        "Migration guides available"
                    ]
                },
                {
                    "title": "Pagination",
                    "description": "How to handle paginated responses",
                    "format": {
                        "request": "?page=1&size=20",
                        "response": {
                            "items": [],
                            "total": 1000,
                            "page": 1,
                            "size": 20,
                            "pages": 50
                        }
                    }
                },
                {
                    "title": "Rate Limiting",
                    "description": "API rate limits and best practices",
                    "limits": {
                        "general": "60 requests per minute",
                        "authentication": "10 requests per minute",
                        "uploads": "20 requests per minute"
                    }
                },
                {
                    "title": "Search and Filtering",
                    "description": "Advanced search capabilities",
                    "features": [
                        "Full-text search with ranking",
                        "Multiple filter combinations",
                        "Sorting options",
                        "Fuzzy matching"
                    ]
                }
            ]
        },
        "api_reference": {
            "title": "API Reference",
            "description": "Complete API endpoint documentation",
            "categories": [
                {
                    "name": "Authentication",
                    "description": "User registration, login, and token management",
                    "endpoints": [
                        "POST /api/v1/auth/register",
                        "POST /api/v1/auth/login",
                        "POST /api/v1/auth/refresh",
                        "POST /api/v1/auth/logout"
                    ]
                },
                {
                    "name": "Users",
                    "description": "User profile management and social features",
                    "endpoints": [
                        "GET /api/v1/users/profile",
                        "PUT /api/v1/users/profile",
                        "GET /api/v1/users/{user_id}",
                        "POST /api/v1/users/{user_id}/follow"
                    ]
                },
                {
                    "name": "Movies",
                    "description": "Movie and series information, search, and discovery",
                    "endpoints": [
                        "GET /api/v1/movies",
                        "GET /api/v1/movies/{movie_id}",
                        "GET /api/v1/movies/search",
                        "GET /api/v1/movies/trending"
                    ]
                },
                {
                    "name": "Reviews",
                    "description": "User reviews, ratings, and voting system",
                    "endpoints": [
                        "GET /api/v1/reviews",
                        "POST /api/v1/reviews",
                        "PUT /api/v1/reviews/{review_id}",
                        "POST /api/v1/reviews/{review_id}/vote"
                    ]
                }
            ]
        },
        "guides": {
            "title": "Integration Guides",
            "description": "Detailed guides for common integration scenarios",
            "guides": [
                {
                    "title": "Building a Movie Review App",
                    "description": "Complete guide to building a movie review application",
                    "steps": [
                        "Set up authentication",
                        "Implement movie browsing",
                        "Add review functionality",
                        "Implement user profiles"
                    ]
                },
                {
                    "title": "Real-time Notifications",
                    "description": "Implementing WebSocket notifications",
                    "topics": [
                        "WebSocket connection setup",
                        "Authentication over WebSocket",
                        "Handling notification events",
                        "Error handling and reconnection"
                    ]
                },
                {
                    "title": "File Upload Integration",
                    "description": "Implementing image uploads with Cloudinary",
                    "features": [
                        "Image optimization",
                        "Multiple format support",
                        "Progress tracking",
                        "Error handling"
                    ]
                }
            ]
        },
        "sdks_and_tools": {
            "title": "SDKs and Tools",
            "description": "Official SDKs and development tools",
            "sdks": [
                {
                    "name": "JavaScript/TypeScript SDK",
                    "description": "Official SDK for web applications",
                    "features": ["Type definitions", "Automatic retries", "Request/response interceptors"],
                    "installation": "npm install @lemonnpie/api-client"
                },
                {
                    "name": "Python SDK",
                    "description": "Official SDK for Python applications",
                    "features": ["Async support", "Automatic pagination", "Built-in caching"],
                    "installation": "pip install lemonnpie-api"
                },
                {
                    "name": "React Native SDK",
                    "description": "SDK optimized for React Native apps",
                    "features": ["Offline support", "Image caching", "Push notifications"],
                    "installation": "npm install @lemonnpie/react-native-sdk"
                }
            ],
            "tools": [
                {
                    "name": "API Explorer",
                    "description": "Interactive API testing tool",
                    "url": "https://explorer.lemonnpie.com"
                },
                {
                    "name": "Postman Collection",
                    "description": "Pre-configured Postman collection",
                    "url": "https://postman.lemonnpie.com"
                }
            ]
        },
        "best_practices": {
            "title": "Best Practices",
            "description": "Recommended practices for API integration",
            "categories": [
                {
                    "title": "Performance",
                    "practices": [
                        "Use pagination for large datasets",
                        "Implement proper caching strategies",
                        "Use compression for large payloads",
                        "Batch requests when possible"
                    ]
                },
                {
                    "title": "Security",
                    "practices": [
                        "Store tokens securely",
                        "Implement proper CORS policies",
                        "Validate all user inputs",
                        "Use HTTPS in production"
                    ]
                },
                {
                    "title": "Error Handling",
                    "practices": [
                        "Implement exponential backoff for retries",
                        "Handle rate limiting gracefully",
                        "Log errors for debugging",
                        "Provide meaningful error messages to users"
                    ]
                },
                {
                    "title": "Monitoring",
                    "practices": [
                        "Monitor API response times",
                        "Track error rates",
                        "Set up alerts for critical issues",
                        "Monitor rate limit usage"
                    ]
                }
            ]
        },
        "changelog": {
            "title": "Changelog",
            "description": "API version history and changes",
            "versions": [
                {
                    "version": "v1.0.0",
                    "release_date": "2024-01-01",
                    "status": "current",
                    "changes": [
                        "Initial release",
                        "Core authentication system",
                        "Movie and review management",
                        "User profiles and social features",
                        "Real-time notifications",
                        "File upload with Cloudinary",
                        "Admin panel functionality"
                    ]
                }
            ]
        },
        "support": {
            "title": "Support",
            "description": "Getting help and support",
            "channels": [
                {
                    "name": "Documentation",
                    "description": "Comprehensive API documentation",
                    "url": "https://docs.lemonnpie.com"
                },
                {
                    "name": "Community Forum",
                    "description": "Community support and discussions",
                    "url": "https://community.lemonnpie.com"
                },
                {
                    "name": "GitHub Issues",
                    "description": "Bug reports and feature requests",
                    "url": "https://github.com/lemonnpie/api/issues"
                },
                {
                    "name": "Email Support",
                    "description": "Direct support for integration issues",
                    "email": "api-support@lemonnpie.com"
                }
            ],
            "sla": {
                "response_time": "24 hours for general inquiries",
                "critical_issues": "4 hours for production issues",
                "availability": "99.9% uptime guarantee"
            }
        }
    }
    
    @classmethod
    def get_documentation_index(cls) -> Dict[str, Any]:
        """Get complete documentation structure"""
        return {
            "api_name": "LemonNPie Backend API",
            "version": "v1.0.0",
            "description": "Comprehensive RESTful API for Nollywood movie reviews and discovery",
            "base_url": "https://api.lemonnpie.com",
            "documentation": cls.DOCUMENTATION_STRUCTURE,
            "quick_links": {
                "interactive_docs": "/docs",
                "static_docs": "/redoc",
                "api_info": "/api/info",
                "version_info": "/api/versions",
                "migration_guides": "/api/migration-guides"
            }
        }
    
    @classmethod
    def get_section(cls, section_name: str) -> Dict[str, Any]:
        """Get specific documentation section"""
        return cls.DOCUMENTATION_STRUCTURE.get(section_name, {})
    
    @classmethod
    def search_documentation(cls, query: str) -> List[Dict[str, Any]]:
        """Search through documentation content"""
        results = []
        query_lower = query.lower()
        
        for section_name, section in cls.DOCUMENTATION_STRUCTURE.items():
            # Search in section title and description
            if (query_lower in section.get("title", "").lower() or 
                query_lower in section.get("description", "").lower()):
                results.append({
                    "type": "section",
                    "section": section_name,
                    "title": section.get("title", ""),
                    "description": section.get("description", ""),
                    "relevance": "high"
                })
            
            # Search in subsections
            if "sections" in section:
                for subsection in section["sections"]:
                    if (query_lower in subsection.get("title", "").lower() or
                        query_lower in subsection.get("description", "").lower()):
                        results.append({
                            "type": "subsection",
                            "section": section_name,
                            "title": subsection.get("title", ""),
                            "description": subsection.get("description", ""),
                            "endpoint": subsection.get("endpoint", ""),
                            "relevance": "medium"
                        })
        
        return results