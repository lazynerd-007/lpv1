# LemonNPie Backend API

A comprehensive Python FastAPI backend for the LemonNPie Nollywood movie review platform.

## Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **Async/Await Support**: Full asynchronous support for high performance
- **PostgreSQL Database**: Robust relational database with SQLAlchemy ORM
- **Redis Caching**: High-performance caching layer
- **JWT Authentication**: Secure token-based authentication
- **Role-based Access Control**: User, Critic, Moderator, and Admin roles
- **Comprehensive Logging**: Structured logging with correlation IDs
- **Docker Support**: Containerized development and deployment
- **Database Migrations**: Alembic for database schema management

## Quick Start

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL 15+ (if running locally)
- Redis 7+ (if running locally)

### Development Setup

1. **Clone the repository and navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Start services with Docker Compose**
   ```bash
   docker-compose up -d postgres redis
   ```

6. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

7. **Start the development server**
   ```bash
   python run.py
   # Or use uvicorn directly:
   # uvicorn app.main:app --reload
   ```

### Using Docker for Development

1. **Start all services**
   ```bash
   docker-compose up
   ```

2. **Run migrations in container**
   ```bash
   docker-compose exec api alembic upgrade head
   ```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── core/
│   │   ├── config.py        # Configuration settings
│   │   ├── logging.py       # Logging configuration
│   │   └── exceptions.py    # Custom exceptions
│   ├── db/
│   │   └── database.py      # Database configuration
│   ├── models/
│   │   ├── user.py          # User model
│   │   ├── movie.py         # Movie model
│   │   └── review.py        # Review model
│   └── cache/
│       └── redis.py         # Redis cache service
├── alembic/                 # Database migrations
├── docker-compose.yml       # Docker services
├── Dockerfile.dev          # Development Docker image
├── requirements.txt        # Python dependencies
└── README.md
```

## Environment Variables

Key environment variables (see `.env.example` for complete list):

- `DEBUG`: Enable debug mode (default: false)
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SECRET_KEY`: JWT secret key (change in production!)
- `ALLOWED_ORIGINS`: CORS allowed origins

## Database

The application uses PostgreSQL with the following extensions:
- `uuid-ossp`: UUID generation
- `pg_trgm`: Trigram similarity for search
- `unaccent`: Accent-insensitive search

### Running Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Caching

Redis is used for:
- Session storage
- API response caching
- Search result caching
- Rate limiting counters

## API Documentation

When running in debug mode, interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Health Checks

- **Application Health**: `GET /health`
- **Database Health**: Included in application health check
- **Redis Health**: Included in application health check

## Development

### Code Style

The project follows Python best practices:
- Type hints for better code documentation
- Async/await for I/O operations
- Structured logging with correlation IDs
- Comprehensive error handling

### Testing

#### Core Infrastructure Tests
```bash
# Run core infrastructure tests (no services required)
python3 test_core_only.py
```

#### Full Test Suite
```bash
# Start required services first
docker-compose up -d postgres redis

# Run all tests
pytest

# Run tests with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_core/test_config.py
```

#### Quick Validation
```bash
# Test configuration and core components
python3 test_simple.py
```

## Deployment

### Production Docker Build

```bash
# Build production image
docker build -f Dockerfile -t lemonnpie-api:latest .

# Run production container
docker run -p 8000:8000 --env-file .env lemonnpie-api:latest
```

### Environment Setup

For production deployment:
1. Set `DEBUG=false`
2. Use strong `SECRET_KEY`
3. Configure proper database and Redis URLs
4. Set up SSL/TLS termination
5. Configure monitoring and logging

## Contributing

1. Follow the existing code style
2. Add tests for new features
3. Update documentation as needed
4. Ensure all tests pass before submitting PR

## License

This project is licensed under the MIT License.