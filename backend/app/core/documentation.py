"""
OpenAPI documentation configuration for LemonNPie Backend API
"""
from typing import Dict, Any, List
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI
from app.core.examples import APIExamples


def get_custom_openapi(app: FastAPI) -> Dict[str, Any]:
    """
    Generate custom OpenAPI schema with enhanced documentation
    """
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="LemonNPie Backend API",
        version="1.0.0",
        description=get_api_description(),
        routes=app.routes,
        servers=[
            {
                "url": "http://localhost:8000",
                "description": "Development server"
            },
            {
                "url": "https://api.lemonnpie.com",
                "description": "Production server"
            }
        ]
    )
    
    # Add custom components
    openapi_schema["components"] = {
        **openapi_schema.get("components", {}),
        **get_custom_components()
    }
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = get_security_schemes()
    
    # Add tags with descriptions
    openapi_schema["tags"] = get_api_tags()
    
    # Add custom info
    openapi_schema["info"].update(get_custom_info())
    
    # Add external documentation
    openapi_schema["externalDocs"] = {
        "description": "LemonNPie API Documentation",
        "url": "https://docs.lemonnpie.com"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def get_api_description() -> str:
    """
    Get comprehensive API description
    """
    return """
## LemonNPie Backend API

A comprehensive RESTful API for the LemonNPie Nollywood movie review platform.

### Features

- **User Management**: Registration, authentication, profiles, and social features
- **Movie Database**: Comprehensive Nollywood movie and series information
- **Review System**: User reviews with LemonPie ratings and category-specific ratings
- **Search & Discovery**: Advanced search with filtering and recommendations
- **Admin Panel**: Content moderation and user management tools
- **Real-time Notifications**: WebSocket-based live updates
- **Analytics**: User behavior tracking and content performance metrics
- **File Management**: Image upload and optimization with Cloudinary

### Authentication

This API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

### Rate Limiting

API requests are rate-limited to prevent abuse:
- **General endpoints**: 60 requests per minute per IP
- **Authentication endpoints**: 10 requests per minute per IP
- **Upload endpoints**: 20 requests per minute per user

### Error Handling

All errors follow a consistent format:

```json
{
    "error": "error_type",
    "message": "Human-readable error message",
    "details": {},
    "timestamp": "2024-01-01T00:00:00Z",
    "path": "/api/v1/endpoint"
}
```

### Pagination

List endpoints support pagination with the following parameters:
- `page`: Page number (default: 1)
- `size`: Items per page (default: 20, max: 100)

Response includes pagination metadata:

```json
{
    "items": [...],
    "total": 1000,
    "page": 1,
    "size": 20,
    "pages": 50
}
```

### Filtering and Sorting

Many endpoints support filtering and sorting:
- Use query parameters for filtering: `?genre=drama&year=2023`
- Use `sort` parameter for sorting: `?sort=rating_desc`
- Combine multiple filters: `?genre=drama&rating_min=7&sort=release_date_desc`

### WebSocket Connections

Real-time notifications are available via WebSocket:
- **Endpoint**: `ws://localhost:8000/ws/notifications`
- **Authentication**: Send JWT token as first message
- **Message Format**: JSON with `type` and `data` fields

### API Versioning

This API uses URL path versioning:
- Current version: `v1`
- Base URL: `/api/v1/`
- Backward compatibility maintained for one major version

### SDKs and Libraries

Official SDKs available for:
- JavaScript/TypeScript
- Python
- React Native
- Flutter

### Support

- **Documentation**: https://docs.lemonnpie.com
- **GitHub**: https://github.com/lemonnpie/backend-api
- **Support Email**: api-support@lemonnpie.com
"""


def get_custom_info() -> Dict[str, Any]:
    """
    Get custom API info section
    """
    return {
        "contact": {
            "name": "LemonNPie API Support",
            "url": "https://lemonnpie.com/support",
            "email": "api-support@lemonnpie.com"
        },
        "license": {
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT"
        },
        "termsOfService": "https://lemonnpie.com/terms",
        "x-logo": {
            "url": "https://lemonnpie.com/logo.png",
            "altText": "LemonNPie Logo"
        }
    }


def get_security_schemes() -> Dict[str, Any]:
    """
    Get security schemes for OpenAPI
    """
    return {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT token obtained from /auth/login endpoint"
        },
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
            "description": "API key for third-party integrations"
        }
    }


def get_api_tags() -> List[Dict[str, Any]]:
    """
    Get API tags with descriptions
    """
    return [
        {
            "name": "Authentication",
            "description": "User registration, login, and token management",
            "externalDocs": {
                "description": "Authentication Guide",
                "url": "https://docs.lemonnpie.com/auth"
            }
        },
        {
            "name": "Users",
            "description": "User profile management and social features",
            "externalDocs": {
                "description": "User Management Guide",
                "url": "https://docs.lemonnpie.com/users"
            }
        },
        {
            "name": "Movies",
            "description": "Movie and series information, search, and discovery",
            "externalDocs": {
                "description": "Movies API Guide",
                "url": "https://docs.lemonnpie.com/movies"
            }
        },
        {
            "name": "Reviews",
            "description": "User reviews, ratings, and voting system",
            "externalDocs": {
                "description": "Reviews API Guide",
                "url": "https://docs.lemonnpie.com/reviews"
            }
        },
        {
            "name": "Admin",
            "description": "Administrative functions for content and user management",
            "externalDocs": {
                "description": "Admin API Guide",
                "url": "https://docs.lemonnpie.com/admin"
            }
        },
        {
            "name": "Uploads",
            "description": "File upload and media management",
            "externalDocs": {
                "description": "Upload Guide",
                "url": "https://docs.lemonnpie.com/uploads"
            }
        },
        {
            "name": "Notifications",
            "description": "Real-time notifications and user preferences",
            "externalDocs": {
                "description": "Notifications Guide",
                "url": "https://docs.lemonnpie.com/notifications"
            }
        },
        {
            "name": "Analytics",
            "description": "User behavior tracking and content performance metrics",
            "externalDocs": {
                "description": "Analytics Guide",
                "url": "https://docs.lemonnpie.com/analytics"
            }
        }
    ]


def get_custom_components() -> Dict[str, Any]:
    """
    Get custom OpenAPI components
    """
    # Get all examples from APIExamples class
    all_examples = APIExamples.get_all_examples()
    
    # Flatten examples for OpenAPI components
    openapi_examples = {}
    for category, examples in all_examples.items():
        for name, example in examples.items():
            openapi_examples[f"{category}_{name}"] = example
    
    return {
        "examples": openapi_examples,
        "parameters": {
            "PageParam": {
                "name": "page",
                "in": "query",
                "description": "Page number for pagination",
                "required": False,
                "schema": {
                    "type": "integer",
                    "minimum": 1,
                    "default": 1
                }
            },
            "SizeParam": {
                "name": "size",
                "in": "query",
                "description": "Number of items per page",
                "required": False,
                "schema": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 100,
                    "default": 20
                }
            },
            "SortParam": {
                "name": "sort",
                "in": "query",
                "description": "Sort order for results",
                "required": False,
                "schema": {
                    "type": "string",
                    "enum": [
                        "created_desc", "created_asc",
                        "rating_desc", "rating_asc",
                        "title_asc", "title_desc",
                        "release_date_desc", "release_date_asc"
                    ],
                    "default": "created_desc"
                }
            }
        }
    }


def get_swagger_ui_parameters() -> Dict[str, Any]:
    """
    Get custom Swagger UI configuration
    """
    return {
        "deepLinking": True,
        "displayOperationId": False,
        "defaultModelsExpandDepth": 1,
        "defaultModelExpandDepth": 1,
        "defaultModelRendering": "example",
        "displayRequestDuration": True,
        "docExpansion": "list",
        "filter": True,
        "showExtensions": True,
        "showCommonExtensions": True,
        "tryItOutEnabled": True,
        "requestSnippetsEnabled": True,
        "requestSnippets": {
            "generators": {
                "curl_bash": {
                    "title": "cURL (bash)",
                    "syntax": "bash"
                },
                "curl_powershell": {
                    "title": "cURL (PowerShell)",
                    "syntax": "powershell"
                },
                "curl_cmd": {
                    "title": "cURL (CMD)",
                    "syntax": "bash"
                }
            },
            "defaultExpanded": True,
            "languages": None
        }
    }


def get_redoc_parameters() -> Dict[str, Any]:
    """
    Get custom ReDoc configuration
    """
    return {
        "expandResponses": "200,201",
        "hideDownloadButton": False,
        "hideHostname": False,
        "hideLoading": False,
        "nativeScrollbars": False,
        "noAutoAuth": False,
        "pathInMiddlePanel": False,
        "requiredPropsFirst": True,
        "scrollYOffset": 0,
        "showExtensions": True,
        "sortPropsAlphabetically": True,
        "theme": {
            "colors": {
                "primary": {
                    "main": "#32CD32"  # LemonNPie green
                }
            },
            "typography": {
                "fontSize": "14px",
                "lineHeight": "1.5em",
                "code": {
                    "fontSize": "13px"
                },
                "headings": {
                    "fontFamily": "Montserrat, sans-serif",
                    "fontWeight": "600"
                }
            },
            "sidebar": {
                "backgroundColor": "#fafafa",
                "width": "260px"
            },
            "rightPanel": {
                "backgroundColor": "#263238",
                "width": "40%"
            }
        }
    }