"""
Database optimization utilities and index management
"""
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy import text, Index
from sqlalchemy.schema import CreateIndex, DropIndex
import structlog

from app.core.config import settings

logger = structlog.get_logger(__name__)


class DatabaseOptimizer:
    """Database optimization and index management"""
    
    def __init__(self, engine: AsyncEngine):
        self.engine = engine
    
    async def create_performance_indexes(self) -> None:
        """Create indexes for improved query performance"""
        
        indexes = [
            # User table indexes
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email ON users(email)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_role ON users(role)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_is_active ON users(is_active)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_created_at ON users(created_at)",
            
            # Movie table indexes
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_movies_title ON movies(title)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_movies_release_date ON movies(release_date)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_movies_director ON movies(director)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_movies_type ON movies(type)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_movies_created_at ON movies(created_at)",
            
            # Review table indexes
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_reviews_user_id ON reviews(user_id)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_reviews_movie_id ON reviews(movie_id)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_reviews_rating ON reviews(lemon_pie_rating)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_reviews_created_at ON reviews(created_at)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_reviews_moderation_status ON reviews(moderation_status)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_reviews_helpful_votes ON reviews(helpful_votes)",
            
            # Composite indexes for common queries
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_reviews_movie_status ON reviews(movie_id, moderation_status)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_reviews_user_created ON reviews(user_id, created_at)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_movies_type_date ON movies(type, release_date)",
            
            # Relationship table indexes
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_movie_genres_movie_id ON movie_genres(movie_id)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_movie_genres_genre ON movie_genres(genre)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_movie_languages_movie_id ON movie_languages(movie_id)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_movie_languages_language ON movie_languages(language)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_movie_cast_movie_id ON movie_cast(movie_id)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_movie_cast_actor_name ON movie_cast(actor_name)",
            
            # User relationship indexes
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_user_follows_follower ON user_follows(follower_id)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_user_follows_following ON user_follows(following_id)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_user_watchlist_user ON user_watchlist(user_id)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_user_watchlist_movie ON user_watchlist(movie_id)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_user_favorites_user ON user_favorites(user_id)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_user_favorites_movie ON user_favorites(movie_id)",
            
            # Review votes indexes
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_review_votes_review ON review_votes(review_id)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_review_votes_user ON review_votes(user_id)",
            
            # Full-text search indexes (if using PostgreSQL)
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_movies_title_gin ON movies USING gin(to_tsvector('english', title))",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_movies_plot_gin ON movies USING gin(to_tsvector('english', plot_summary))",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_reviews_text_gin ON reviews USING gin(to_tsvector('english', review_text))",
        ]
        
        async with self.engine.begin() as conn:
            for index_sql in indexes:
                try:
                    await conn.execute(text(index_sql))
                    logger.info(f"Created index: {index_sql.split()[-1]}")
                except Exception as e:
                    logger.warning(f"Failed to create index: {e}")
    
    async def analyze_tables(self) -> None:
        """Update table statistics for query optimization"""
        
        tables = [
            "users", "movies", "reviews", "movie_genres", "movie_languages", 
            "movie_cast", "user_follows", "user_watchlist", "user_favorites", 
            "review_votes"
        ]
        
        async with self.engine.begin() as conn:
            for table in tables:
                try:
                    await conn.execute(text(f"ANALYZE {table}"))
                    logger.info(f"Analyzed table: {table}")
                except Exception as e:
                    logger.warning(f"Failed to analyze table {table}: {e}")
    
    async def get_slow_queries(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get slow queries from pg_stat_statements (PostgreSQL only)"""
        
        if "postgresql" not in settings.DATABASE_URL:
            return []
        
        query = """
        SELECT 
            query,
            calls,
            total_exec_time,
            mean_exec_time,
            rows
        FROM pg_stat_statements 
        WHERE query NOT LIKE '%pg_stat_statements%'
        ORDER BY mean_exec_time DESC 
        LIMIT :limit
        """
        
        try:
            async with self.engine.begin() as conn:
                result = await conn.execute(text(query), {"limit": limit})
                return [dict(row._mapping) for row in result.fetchall()]
        except Exception as e:
            logger.warning(f"Failed to get slow queries: {e}")
            return []
    
    async def get_table_sizes(self) -> List[Dict[str, Any]]:
        """Get table sizes for monitoring"""
        
        if "postgresql" not in settings.DATABASE_URL:
            return []
        
        query = """
        SELECT 
            schemaname,
            tablename,
            attname,
            n_distinct,
            correlation
        FROM pg_stats 
        WHERE schemaname = 'public'
        ORDER BY tablename, attname
        """
        
        try:
            async with self.engine.begin() as conn:
                result = await conn.execute(text(query))
                return [dict(row._mapping) for row in result.fetchall()]
        except Exception as e:
            logger.warning(f"Failed to get table sizes: {e}")
            return []
    
    async def optimize_database(self) -> Dict[str, Any]:
        """Run comprehensive database optimization"""
        
        results = {
            "indexes_created": False,
            "tables_analyzed": False,
            "slow_queries": [],
            "table_stats": []
        }
        
        try:
            # Create performance indexes
            await self.create_performance_indexes()
            results["indexes_created"] = True
            
            # Update table statistics
            await self.analyze_tables()
            results["tables_analyzed"] = True
            
            # Get slow queries
            results["slow_queries"] = await self.get_slow_queries()
            
            # Get table statistics
            results["table_stats"] = await self.get_table_sizes()
            
            logger.info("Database optimization completed successfully")
            
        except Exception as e:
            logger.error(f"Database optimization failed: {e}")
            results["error"] = str(e)
        
        return results


class QueryOptimizer:
    """Query optimization utilities"""
    
    @staticmethod
    def add_query_hints(query: str, hints: List[str]) -> str:
        """Add query hints for PostgreSQL"""
        if not hints or "postgresql" not in settings.DATABASE_URL:
            return query
        
        hint_comment = f"/*+ {' '.join(hints)} */"
        return f"{hint_comment}\n{query}"
    
    @staticmethod
    def explain_query(query: str, analyze: bool = False) -> str:
        """Generate EXPLAIN query for analysis"""
        explain_type = "EXPLAIN (ANALYZE, BUFFERS)" if analyze else "EXPLAIN"
        return f"{explain_type} {query}"
    
    @staticmethod
    def get_optimized_pagination_query(
        base_query: str, 
        order_column: str, 
        limit: int, 
        offset: int
    ) -> str:
        """Generate optimized pagination query using cursor-based pagination"""
        
        # For large offsets, cursor-based pagination is more efficient
        if offset > 1000:
            return f"""
            {base_query}
            ORDER BY {order_column}
            LIMIT {limit}
            """
        else:
            return f"""
            {base_query}
            ORDER BY {order_column}
            LIMIT {limit} OFFSET {offset}
            """


# Query optimization decorators
def with_query_timeout(timeout_seconds: int = 30):
    """Decorator to add query timeout"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # This would need to be implemented with asyncio.wait_for
            # in the actual query execution
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def with_query_cache(cache_key_func, ttl: int = 300):
    """Decorator to cache query results"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # This would integrate with the Redis cache service
            # to cache query results
            return await func(*args, **kwargs)
        return wrapper
    return decorator


# Common optimized queries
class OptimizedQueries:
    """Collection of optimized queries for common operations"""
    
    @staticmethod
    def get_movie_with_stats_query() -> str:
        """Optimized query to get movie with statistics"""
        return """
        SELECT 
            m.*,
            COALESCE(r.review_count, 0) as review_count,
            COALESCE(r.avg_rating, 0) as avg_rating,
            COALESCE(r.rating_distribution, '{}') as rating_distribution
        FROM movies m
        LEFT JOIN (
            SELECT 
                movie_id,
                COUNT(*) as review_count,
                AVG(lemon_pie_rating) as avg_rating,
                jsonb_object_agg(
                    lemon_pie_rating::text, 
                    rating_count
                ) as rating_distribution
            FROM (
                SELECT 
                    movie_id,
                    lemon_pie_rating,
                    COUNT(*) as rating_count
                FROM reviews 
                WHERE moderation_status = 'approved'
                GROUP BY movie_id, lemon_pie_rating
            ) rating_counts
            GROUP BY movie_id
        ) r ON m.id = r.movie_id
        WHERE m.id = :movie_id
        """
    
    @staticmethod
    def get_trending_movies_query() -> str:
        """Optimized query for trending movies"""
        return """
        SELECT 
            m.*,
            COUNT(r.id) as recent_review_count,
            AVG(r.lemon_pie_rating) as avg_rating
        FROM movies m
        INNER JOIN reviews r ON m.id = r.movie_id
        WHERE r.created_at >= NOW() - INTERVAL '30 days'
            AND r.moderation_status = 'approved'
        GROUP BY m.id
        HAVING COUNT(r.id) >= 3
        ORDER BY COUNT(r.id) DESC, AVG(r.lemon_pie_rating) DESC
        LIMIT :limit
        """
    
    @staticmethod
    def get_user_activity_feed_query() -> str:
        """Optimized query for user activity feed"""
        return """
        SELECT 
            'review' as activity_type,
            r.id as activity_id,
            r.user_id,
            r.movie_id,
            r.created_at,
            u.name as user_name,
            m.title as movie_title,
            r.lemon_pie_rating as rating
        FROM reviews r
        INNER JOIN users u ON r.user_id = u.id
        INNER JOIN movies m ON r.movie_id = m.id
        WHERE r.user_id IN (
            SELECT following_id 
            FROM user_follows 
            WHERE follower_id = :user_id
        )
        AND r.moderation_status = 'approved'
        AND r.created_at >= NOW() - INTERVAL '7 days'
        ORDER BY r.created_at DESC
        LIMIT :limit OFFSET :offset
        """