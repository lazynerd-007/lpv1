"""
Comprehensive API examples for OpenAPI documentation
"""
from typing import Dict, Any


class APIExamples:
    """Collection of API request/response examples"""
    
    # Authentication Examples
    AUTH_EXAMPLES = {
        "register_request": {
            "summary": "User Registration Request",
            "description": "Example request for registering a new user",
            "value": {
                "email": "adaeze.okafor@example.com",
                "password": "NollywoodFan2024!",
                "name": "Adaeze Okafor",
                "bio": "Passionate about Nollywood cinema and storytelling. Love reviewing movies that showcase Nigerian culture.",
                "location": "Abuja, Nigeria"
            }
        },
        "register_response": {
            "summary": "Successful Registration Response",
            "description": "Response after successful user registration",
            "value": {
                "user": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "email": "adaeze.okafor@example.com",
                    "name": "Adaeze Okafor",
                    "bio": "Passionate about Nollywood cinema and storytelling. Love reviewing movies that showcase Nigerian culture.",
                    "location": "Abuja, Nigeria",
                    "avatar_url": None,
                    "role": "user",
                    "is_verified": False,
                    "created_at": "2024-01-15T10:30:00Z"
                },
                "tokens": {
                    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDAiLCJlbWFpbCI6ImFkYWV6ZS5va2Fmb3JAZW1haWwuY29tIiwicm9sZSI6InVzZXIiLCJleHAiOjE3MDUzMjE4MDAsImlhdCI6MTcwNTMxOTAwMH0.example_signature",
                    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDAiLCJ0eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwNTkyMzgwMCwiaWF0IjoxNzA1MzE5MDAwfQ.example_refresh_signature",
                    "token_type": "bearer",
                    "expires_in": 1800
                }
            }
        },
        "login_request": {
            "summary": "User Login Request",
            "description": "Example request for user authentication",
            "value": {
                "email": "adaeze.okafor@example.com",
                "password": "NollywoodFan2024!"
            }
        },
        "login_response": {
            "summary": "Successful Login Response",
            "description": "Response after successful authentication",
            "value": {
                "user": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "email": "adaeze.okafor@example.com",
                    "name": "Adaeze Okafor",
                    "bio": "Passionate about Nollywood cinema and storytelling.",
                    "location": "Abuja, Nigeria",
                    "avatar_url": "https://res.cloudinary.com/lemonnpie/image/upload/v1705319000/users/550e8400-e29b-41d4-a716-446655440000/avatar.jpg",
                    "role": "user",
                    "is_verified": True,
                    "created_at": "2024-01-15T10:30:00Z"
                },
                "tokens": {
                    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    "token_type": "bearer",
                    "expires_in": 1800
                }
            }
        }
    }
    
    # Movie Examples
    MOVIE_EXAMPLES = {
        "movie_response": {
            "summary": "Movie Details Response",
            "description": "Complete movie information with cast and ratings",
            "value": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "The Wedding Party 2: Destination Dubai",
                "local_title": "The Wedding Party 2",
                "release_date": "2017-12-15",
                "runtime": 98,
                "plot_summary": "Nonso continues his romance with Deirdre, the bridesmaid from London. While on a dinner date, Nonso proposes to Deirdre by accident and sets off a chain of events too powerful to stop. Deirdre's upper-crust British family are against the match, as are some members of the Nigerian clan, but Deirdre's determination to marry Nonso and Nonso's desire to marry Deirdre leads them to Dubai for a wedding celebration that will be remembered for a very long time.",
                "poster_url": "https://res.cloudinary.com/lemonnpie/image/upload/v1705319000/movies/wedding-party-2-poster.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=example",
                "director": "Niyi Akinmolayan",
                "producer": "Mo Abudu",
                "production_company": "EbonyLife Films",
                "production_state": "Lagos, Nigeria",
                "box_office_ng": "₦500,000,000",
                "type": "movie",
                "genres": ["Comedy", "Romance", "Drama"],
                "languages": ["English", "Igbo"],
                "cast": [
                    {
                        "actor_name": "Adesua Etomi",
                        "character_name": "Dunni Coker",
                        "role_type": "actor"
                    },
                    {
                        "actor_name": "Banky Wellington",
                        "character_name": "Nonso Onwuka",
                        "role_type": "actor"
                    }
                ],
                "lemon_pie_rating": 8.2,
                "review_count": 1247,
                "rating_distribution": {
                    "1": 12,
                    "2": 8,
                    "3": 15,
                    "4": 23,
                    "5": 45,
                    "6": 78,
                    "7": 156,
                    "8": 298,
                    "9": 387,
                    "10": 225
                },
                "cultural_authenticity_avg": 9.1,
                "production_quality_avg": 7.8,
                "created_at": "2024-01-10T08:00:00Z",
                "updated_at": "2024-01-15T14:30:00Z"
            }
        },
        "movie_search_request": {
            "summary": "Movie Search Request",
            "description": "Search movies with filters and sorting",
            "value": {
                "query": "wedding party",
                "genre": "comedy",
                "year": 2017,
                "rating_min": 7,
                "language": "english",
                "sort": "rating_desc",
                "page": 1,
                "size": 20
            }
        },
        "movies_list_response": {
            "summary": "Movies List Response",
            "description": "Paginated list of movies with metadata",
            "value": {
                "items": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "title": "The Wedding Party 2: Destination Dubai",
                        "local_title": "The Wedding Party 2",
                        "release_date": "2017-12-15",
                        "poster_url": "https://res.cloudinary.com/lemonnpie/image/upload/v1705319000/movies/wedding-party-2-poster.jpg",
                        "director": "Niyi Akinmolayan",
                        "genres": ["Comedy", "Romance", "Drama"],
                        "lemon_pie_rating": 8.2,
                        "review_count": 1247
                    }
                ],
                "total": 1,
                "page": 1,
                "size": 20,
                "pages": 1
            }
        }
    }
    
    # Review Examples
    REVIEW_EXAMPLES = {
        "review_create_request": {
            "summary": "Create Review Request",
            "description": "Submit a comprehensive movie review",
            "value": {
                "movie_id": "123e4567-e89b-12d3-a456-426614174000",
                "lemon_pie_rating": 9,
                "review_text": "The Wedding Party 2 is a delightful continuation of the beloved Nigerian romantic comedy franchise. The film successfully balances humor with heartfelt moments, showcasing the cultural dynamics between Nigerian and British families. Adesua Etomi and Banky Wellington deliver compelling performances that feel authentic and engaging. The Dubai setting adds a fresh visual appeal, though the story remains grounded in relatable relationship dynamics. The production quality is notably high for Nollywood standards, with excellent cinematography and sound design. While some plot points feel predictable, the cultural authenticity and strong performances make this a worthy sequel that celebrates Nigerian cinema.",
                "cultural_authenticity_rating": 9,
                "production_quality_rating": 8,
                "story_rating": 7,
                "acting_rating": 9,
                "cinematography_rating": 8,
                "spoiler_warning": False
            }
        },
        "review_response": {
            "summary": "Review Response",
            "description": "Complete review information with user details",
            "value": {
                "id": "456e7890-f12c-34e5-b678-901234567890",
                "user": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "Adaeze Okafor",
                    "avatar_url": "https://res.cloudinary.com/lemonnpie/image/upload/v1705319000/users/550e8400-e29b-41d4-a716-446655440000/avatar.jpg",
                    "role": "user",
                    "is_verified": True
                },
                "movie_id": "123e4567-e89b-12d3-a456-426614174000",
                "lemon_pie_rating": 9,
                "review_text": "The Wedding Party 2 is a delightful continuation of the beloved Nigerian romantic comedy franchise...",
                "cultural_authenticity_rating": 9,
                "production_quality_rating": 8,
                "story_rating": 7,
                "acting_rating": 9,
                "cinematography_rating": 8,
                "spoiler_warning": False,
                "helpful_votes": 23,
                "unhelpful_votes": 2,
                "helpfulness_score": 21,
                "user_vote": None,
                "created_at": "2024-01-15T16:45:00Z",
                "updated_at": "2024-01-15T16:45:00Z"
            }
        }
    }
    
    # User Examples
    USER_EXAMPLES = {
        "user_profile_response": {
            "summary": "User Profile Response",
            "description": "Complete user profile with statistics",
            "value": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "adaeze.okafor@example.com",
                "name": "Adaeze Okafor",
                "bio": "Passionate about Nollywood cinema and storytelling. Love reviewing movies that showcase Nigerian culture and heritage.",
                "location": "Abuja, Nigeria",
                "avatar_url": "https://res.cloudinary.com/lemonnpie/image/upload/v1705319000/users/550e8400-e29b-41d4-a716-446655440000/avatar.jpg",
                "role": "user",
                "is_verified": True,
                "created_at": "2024-01-15T10:30:00Z",
                "stats": {
                    "total_reviews": 47,
                    "average_rating": 7.8,
                    "followers_count": 156,
                    "following_count": 89,
                    "movies_watched": 203
                }
            }
        },
        "user_update_request": {
            "summary": "Update User Profile Request",
            "description": "Update user profile information",
            "value": {
                "name": "Adaeze Okafor-Johnson",
                "bio": "Film critic and Nollywood enthusiast. Passionate about promoting African cinema and storytelling. Currently working on a documentary about the evolution of Nigerian cinema.",
                "location": "Lagos, Nigeria"
            }
        }
    }
    
    # Error Examples
    ERROR_EXAMPLES = {
        "validation_error": {
            "summary": "Validation Error",
            "description": "Request validation failed",
            "value": {
                "error": "validation_error",
                "message": "Request validation failed",
                "details": {
                    "email": "Invalid email format",
                    "password": "Password must contain at least one uppercase letter"
                },
                "timestamp": "2024-01-15T12:00:00Z",
                "path": "/api/v1/auth/register"
            }
        },
        "authentication_error": {
            "summary": "Authentication Error",
            "description": "Authentication required or failed",
            "value": {
                "error": "authentication_error",
                "message": "Invalid or expired token",
                "timestamp": "2024-01-15T12:00:00Z",
                "path": "/api/v1/users/profile"
            }
        },
        "authorization_error": {
            "summary": "Authorization Error",
            "description": "Insufficient permissions",
            "value": {
                "error": "authorization_error",
                "message": "Insufficient permissions to access this resource",
                "details": {"required_role": "admin", "user_role": "user"},
                "timestamp": "2024-01-15T12:00:00Z",
                "path": "/api/v1/admin/users"
            }
        },
        "rate_limit_error": {
            "summary": "Rate Limit Error",
            "description": "Too many requests",
            "value": {
                "error": "rate_limit_exceeded",
                "message": "Rate limit exceeded. Try again later.",
                "details": {
                    "limit": 60,
                    "window": "1 minute",
                    "retry_after": 45
                },
                "timestamp": "2024-01-15T12:00:00Z",
                "path": "/api/v1/auth/login"
            }
        },
        "not_found_error": {
            "summary": "Resource Not Found",
            "description": "Requested resource does not exist",
            "value": {
                "error": "not_found",
                "message": "Movie not found",
                "details": {"movie_id": "123e4567-e89b-12d3-a456-426614174000"},
                "timestamp": "2024-01-15T12:00:00Z",
                "path": "/api/v1/movies/123e4567-e89b-12d3-a456-426614174000"
            }
        }
    }
    
    # Pagination Examples
    PAGINATION_EXAMPLES = {
        "pagination_response": {
            "summary": "Paginated Response",
            "description": "Standard pagination format used across all list endpoints",
            "value": {
                "items": [],
                "total": 1247,
                "page": 2,
                "size": 20,
                "pages": 63,
                "has_next": True,
                "has_prev": True,
                "next_page": 3,
                "prev_page": 1
            }
        }
    }
    
    @classmethod
    def get_all_examples(cls) -> Dict[str, Any]:
        """Get all examples organized by category"""
        return {
            "authentication": cls.AUTH_EXAMPLES,
            "movies": cls.MOVIE_EXAMPLES,
            "reviews": cls.REVIEW_EXAMPLES,
            "users": cls.USER_EXAMPLES,
            "errors": cls.ERROR_EXAMPLES,
            "pagination": cls.PAGINATION_EXAMPLES
        }
    
    @classmethod
    def get_example_by_name(cls, category: str, name: str) -> Dict[str, Any]:
        """Get specific example by category and name"""
        examples = cls.get_all_examples()
        return examples.get(category, {}).get(name, {})