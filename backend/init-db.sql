-- Initialize PostgreSQL database with required extensions and types

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For trigram similarity search
CREATE EXTENSION IF NOT EXISTS "unaccent"; -- For accent-insensitive search

-- Create custom types
DO $$ BEGIN
    CREATE TYPE user_role AS ENUM ('user', 'critic', 'moderator', 'admin');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE content_type AS ENUM ('movie', 'series');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE moderation_status AS ENUM ('pending', 'approved', 'rejected');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE vote_type AS ENUM ('helpful', 'unhelpful');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE cast_role AS ENUM ('actor', 'director', 'producer', 'writer');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Core tables

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    bio TEXT,
    location VARCHAR(255),
    avatar_url VARCHAR(500),
    role user_role DEFAULT 'user',
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Movies table
CREATE TABLE IF NOT EXISTS movies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    local_title VARCHAR(500),
    release_date DATE NOT NULL,
    runtime INTEGER,
    plot_summary TEXT,
    poster_url VARCHAR(500),
    trailer_url VARCHAR(500),
    director VARCHAR(255),
    producer VARCHAR(255),
    production_company VARCHAR(255),
    production_state VARCHAR(100),
    box_office_ng VARCHAR(100),
    type content_type DEFAULT 'movie',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Reviews table
CREATE TABLE IF NOT EXISTS reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    movie_id UUID REFERENCES movies(id) ON DELETE CASCADE,
    lemon_pie_rating INTEGER CHECK (lemon_pie_rating >= 1 AND lemon_pie_rating <= 10),
    review_text TEXT NOT NULL,
    review_language VARCHAR(10) DEFAULT 'en',
    spoiler_warning BOOLEAN DEFAULT false,
    cultural_authenticity_rating INTEGER CHECK (cultural_authenticity_rating >= 1 AND cultural_authenticity_rating <= 10),
    production_quality_rating INTEGER CHECK (production_quality_rating >= 1 AND production_quality_rating <= 10),
    story_rating INTEGER CHECK (story_rating >= 1 AND story_rating <= 10),
    acting_rating INTEGER CHECK (acting_rating >= 1 AND acting_rating <= 10),
    cinematography_rating INTEGER CHECK (cinematography_rating >= 1 AND cinematography_rating <= 10),
    helpful_votes INTEGER DEFAULT 0,
    unhelpful_votes INTEGER DEFAULT 0,
    is_flagged BOOLEAN DEFAULT false,
    moderation_status moderation_status DEFAULT 'approved',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, movie_id)
);

-- Movie genres relationship table
CREATE TABLE IF NOT EXISTS movie_genres (
    movie_id UUID REFERENCES movies(id) ON DELETE CASCADE,
    genre VARCHAR(100) NOT NULL,
    PRIMARY KEY (movie_id, genre)
);

-- Movie languages relationship table
CREATE TABLE IF NOT EXISTS movie_languages (
    movie_id UUID REFERENCES movies(id) ON DELETE CASCADE,
    language VARCHAR(50) NOT NULL,
    PRIMARY KEY (movie_id, language)
);

-- Movie cast relationship table
CREATE TABLE IF NOT EXISTS movie_cast (
    movie_id UUID REFERENCES movies(id) ON DELETE CASCADE,
    actor_name VARCHAR(255) NOT NULL,
    character_name VARCHAR(255),
    role_type cast_role DEFAULT 'actor',
    PRIMARY KEY (movie_id, actor_name, character_name)
);

-- User follows relationship table
CREATE TABLE IF NOT EXISTS user_follows (
    follower_id UUID REFERENCES users(id) ON DELETE CASCADE,
    following_id UUID REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (follower_id, following_id),
    CHECK (follower_id != following_id)
);

-- User watchlist table
CREATE TABLE IF NOT EXISTS user_watchlist (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    movie_id UUID REFERENCES movies(id) ON DELETE CASCADE,
    added_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, movie_id)
);

-- User favorites table
CREATE TABLE IF NOT EXISTS user_favorites (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    movie_id UUID REFERENCES movies(id) ON DELETE CASCADE,
    added_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, movie_id)
);

-- Review votes table
CREATE TABLE IF NOT EXISTS review_votes (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    review_id UUID REFERENCES reviews(id) ON DELETE CASCADE,
    vote_type vote_type NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, review_id)
);

-- User reports table for content moderation
CREATE TABLE IF NOT EXISTS user_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reporter_id UUID REFERENCES users(id) ON DELETE CASCADE,
    reported_user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    reported_review_id UUID REFERENCES reviews(id) ON DELETE CASCADE,
    reason VARCHAR(255) NOT NULL,
    description TEXT,
    status moderation_status DEFAULT 'pending',
    resolved_by UUID REFERENCES users(id) ON DELETE SET NULL,
    resolved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    data JSONB,
    is_read BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_movies_title ON movies(title);
CREATE INDEX IF NOT EXISTS idx_movies_release_date ON movies(release_date);
CREATE INDEX IF NOT EXISTS idx_movies_director ON movies(director);
CREATE INDEX IF NOT EXISTS idx_movies_type ON movies(type);
CREATE INDEX IF NOT EXISTS idx_reviews_user_id ON reviews(user_id);
CREATE INDEX IF NOT EXISTS idx_reviews_movie_id ON reviews(movie_id);
CREATE INDEX IF NOT EXISTS idx_reviews_created_at ON reviews(created_at);
CREATE INDEX IF NOT EXISTS idx_reviews_lemon_pie_rating ON reviews(lemon_pie_rating);
CREATE INDEX IF NOT EXISTS idx_user_follows_follower_id ON user_follows(follower_id);
CREATE INDEX IF NOT EXISTS idx_user_follows_following_id ON user_follows(following_id);
CREATE INDEX IF NOT EXISTS idx_user_watchlist_user_id ON user_watchlist(user_id);
CREATE INDEX IF NOT EXISTS idx_user_favorites_user_id ON user_favorites(user_id);
CREATE INDEX IF NOT EXISTS idx_review_votes_review_id ON review_votes(review_id);
CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers to automatically update updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_movies_updated_at BEFORE UPDATE ON movies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_reviews_updated_at BEFORE UPDATE ON reviews
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
-- 
Full-text search infrastructure

-- Create search index table for movies
CREATE TABLE IF NOT EXISTS movie_search_index (
    movie_id UUID PRIMARY KEY REFERENCES movies(id) ON DELETE CASCADE,
    search_vector tsvector,
    title_vector tsvector,
    content_vector tsvector,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create GIN indexes for fast text search
CREATE INDEX IF NOT EXISTS idx_movie_search_vector ON movie_search_index USING GIN(search_vector);
CREATE INDEX IF NOT EXISTS idx_movie_title_vector ON movie_search_index USING GIN(title_vector);
CREATE INDEX IF NOT EXISTS idx_movie_content_vector ON movie_search_index USING GIN(content_vector);

-- Function to update search vectors
CREATE OR REPLACE FUNCTION update_movie_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO movie_search_index (movie_id, search_vector, title_vector, content_vector)
    VALUES (
        NEW.id,
        to_tsvector('english', 
            COALESCE(NEW.title, '') || ' ' ||
            COALESCE(NEW.local_title, '') || ' ' ||
            COALESCE(NEW.director, '') || ' ' ||
            COALESCE(NEW.producer, '') || ' ' ||
            COALESCE(NEW.production_company, '') || ' ' ||
            COALESCE(NEW.production_state, '')
        ),
        to_tsvector('english', COALESCE(NEW.title, '') || ' ' || COALESCE(NEW.local_title, '')),
        to_tsvector('english', COALESCE(NEW.plot_summary, ''))
    )
    ON CONFLICT (movie_id) DO UPDATE SET
        search_vector = EXCLUDED.search_vector,
        title_vector = EXCLUDED.title_vector,
        content_vector = EXCLUDED.content_vector,
        updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to automatically update search vectors
CREATE TRIGGER trigger_update_movie_search
    AFTER INSERT OR UPDATE ON movies
    FOR EACH ROW EXECUTE FUNCTION update_movie_search_vector();

-- Function to update search index updated_at timestamp
CREATE TRIGGER update_movie_search_index_updated_at BEFORE UPDATE ON movie_search_index
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create additional search functions for better search experience

-- Function for fuzzy movie search with ranking
CREATE OR REPLACE FUNCTION search_movies(
    search_query TEXT,
    search_limit INTEGER DEFAULT 20,
    search_offset INTEGER DEFAULT 0
)
RETURNS TABLE (
    movie_id UUID,
    title VARCHAR(500),
    local_title VARCHAR(500),
    director VARCHAR(255),
    release_date DATE,
    poster_url VARCHAR(500),
    rank REAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        m.id,
        m.title,
        m.local_title,
        m.director,
        m.release_date,
        m.poster_url,
        ts_rank(msi.search_vector, plainto_tsquery('english', search_query)) as rank
    FROM movies m
    JOIN movie_search_index msi ON m.id = msi.movie_id
    WHERE msi.search_vector @@ plainto_tsquery('english', search_query)
    ORDER BY rank DESC, m.release_date DESC
    LIMIT search_limit OFFSET search_offset;
END;
$$ LANGUAGE plpgsql;

-- Function for movie title suggestions using trigram similarity
CREATE OR REPLACE FUNCTION suggest_movie_titles(
    partial_query TEXT,
    suggestion_limit INTEGER DEFAULT 5
)
RETURNS TABLE (
    title VARCHAR(500),
    similarity_score REAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        m.title,
        similarity(m.title, partial_query) as similarity_score
    FROM movies m
    WHERE similarity(m.title, partial_query) > 0.3
    ORDER BY similarity_score DESC
    LIMIT suggestion_limit;
END;
$$ LANGUAGE plpgsql;