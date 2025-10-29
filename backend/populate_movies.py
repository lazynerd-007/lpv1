#!/usr/bin/env python3
"""
Script to populate the database with sample movies for testing
"""
import asyncio
import sys
import os
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import get_db_session
from app.models.movie import Movie
from app.models.relationships import MovieGenre, MovieLanguage, MovieCast
from app.models.enums import ContentType, CastRole

# Sample movie data
SAMPLE_MOVIES = [
    {
        "title": "The Wedding Party",
        "local_title": "The Wedding Party",
        "release_date": date(2016, 12, 16),
        "runtime": 110,
        "plot_summary": "A lavish wedding turns chaotic when family secrets and unexpected guests threaten to ruin the celebration.",
        "director": "Kemi Adetiba",
        "producer": "Mo Abudu",
        "production_company": "EbonyLife Films",
        "production_state": "Lagos",
        "box_office_ng": "₦453 million",
        "poster_url": "https://example.com/wedding-party-poster.jpg",
        "trailer_url": "https://example.com/wedding-party-trailer.mp4",
        "genres": ["Comedy", "Romance", "Drama"],
        "languages": ["English", "Yoruba"],
        "cast": [
            {"actor_name": "Adesua Etomi", "character_name": "Dunni Coker", "role_type": "actor"},
            {"actor_name": "Banky W", "character_name": "Dozie", "role_type": "actor"},
            {"actor_name": "RMD", "character_name": "Chief Felix Onwuka", "role_type": "actor"}
        ]
    },
    {
        "title": "King of Boys",
        "local_title": "King of Boys",
        "release_date": date(2018, 10, 26),
        "runtime": 170,
        "plot_summary": "A businesswoman's political ambitions are threatened when her past catches up with her.",
        "director": "Kemi Adetiba",
        "producer": "Kemi Adetiba",
        "production_company": "KAP Motion Pictures",
        "production_state": "Lagos",
        "box_office_ng": "₦245 million",
        "poster_url": "https://example.com/king-of-boys-poster.jpg",
        "trailer_url": "https://example.com/king-of-boys-trailer.mp4",
        "genres": ["Crime", "Drama", "Thriller"],
        "languages": ["English", "Yoruba"],
        "cast": [
            {"actor_name": "Sola Sobowale", "character_name": "Eniola Salami", "role_type": "actor"},
            {"actor_name": "Adesua Etomi", "character_name": "Kemi", "role_type": "actor"},
            {"actor_name": "Reminisce", "character_name": "Makanaki", "role_type": "actor"}
        ]
    },
    {
        "title": "Lionheart",
        "local_title": "Lionheart",
        "release_date": date(2018, 12, 21),
        "runtime": 95,
        "plot_summary": "A young woman fights to save her father's bus company from bankruptcy and corruption.",
        "director": "Genevieve Nnaji",
        "producer": "Genevieve Nnaji",
        "production_company": "The Entertainment Network",
        "production_state": "Enugu",
        "box_office_ng": "₦150 million",
        "poster_url": "https://example.com/lionheart-poster.jpg",
        "trailer_url": "https://example.com/lionheart-trailer.mp4",
        "genres": ["Drama", "Family"],
        "languages": ["English", "Igbo"],
        "cast": [
            {"actor_name": "Genevieve Nnaji", "character_name": "Adaeze Obiagu", "role_type": "actor"},
            {"actor_name": "Nkem Owoh", "character_name": "Godswill", "role_type": "actor"},
            {"actor_name": "Pete Edochie", "character_name": "Chief Ernest Obiagu", "role_type": "actor"}
        ]
    },
    {
        "title": "October 1",
        "local_title": "October 1",
        "release_date": date(2014, 10, 1),
        "runtime": 143,
        "plot_summary": "A police detective investigates a series of murders in a colonial Nigerian town on the eve of independence.",
        "director": "Kunle Afolayan",
        "producer": "Kunle Afolayan",
        "production_company": "Golden Effects Pictures",
        "production_state": "Ogun",
        "box_office_ng": "₦180 million",
        "poster_url": "https://example.com/october-1-poster.jpg",
        "trailer_url": "https://example.com/october-1-trailer.mp4",
        "genres": ["Mystery", "Thriller", "Drama"],
        "languages": ["English", "Yoruba"],
        "cast": [
            {"actor_name": "Sadiq Daba", "character_name": "Inspector Danladi Waziri", "role_type": "actor"},
            {"actor_name": "Kayode Olaiya", "character_name": "Agbekoya", "role_type": "actor"},
            {"actor_name": "David Bailie", "character_name": "Father Dowling", "role_type": "actor"}
        ]
    },
    {
        "title": "Half of a Yellow Sun",
        "local_title": "Half of a Yellow Sun",
        "release_date": date(2013, 9, 8),
        "runtime": 106,
        "plot_summary": "Two sisters navigate love and loss during the Nigerian Civil War.",
        "director": "Biyi Bandele",
        "producer": "Andrea Calderwood",
        "production_company": "Potboiler Productions",
        "production_state": "Calabar",
        "box_office_ng": "₦95 million",
        "poster_url": "https://example.com/half-yellow-sun-poster.jpg",
        "trailer_url": "https://example.com/half-yellow-sun-trailer.mp4",
        "genres": ["Drama", "Romance", "War"],
        "languages": ["English", "Igbo"],
        "cast": [
            {"actor_name": "Chiwetel Ejiofor", "character_name": "Odenigbo", "role_type": "actor"},
            {"actor_name": "Thandiwe Newton", "character_name": "Olanna", "role_type": "actor"},
            {"actor_name": "Anika Noni Rose", "character_name": "Kainene", "role_type": "actor"}
        ]
    },
    {
        "title": "The Figurine",
        "local_title": "Araromire",
        "release_date": date(2009, 10, 9),
        "runtime": 122,
        "plot_summary": "Two friends discover an ancient figurine that brings them luck, but at a terrible cost.",
        "director": "Kunle Afolayan",
        "producer": "Kunle Afolayan",
        "production_company": "Golden Effects Pictures",
        "production_state": "Osun",
        "box_office_ng": "₦65 million",
        "poster_url": "https://example.com/figurine-poster.jpg",
        "trailer_url": "https://example.com/figurine-trailer.mp4",
        "genres": ["Supernatural", "Thriller", "Drama"],
        "languages": ["English", "Yoruba"],
        "cast": [
            {"actor_name": "Kunle Afolayan", "character_name": "Femi", "role_type": "actor"},
            {"actor_name": "Ramsey Nouah", "character_name": "Mide", "role_type": "actor"},
            {"actor_name": "Omoni Oboli", "character_name": "Mona", "role_type": "actor"}
        ]
    },
    {
        "title": "Living in Bondage: Breaking Free",
        "local_title": "Living in Bondage: Breaking Free",
        "release_date": date(2019, 11, 8),
        "runtime": 115,
        "plot_summary": "The son of a man who made a deal with dark forces must break the family curse.",
        "director": "Ramsey Nouah",
        "producer": "Steve Gukas",
        "production_company": "Play Network Studios",
        "production_state": "Lagos",
        "box_office_ng": "₦125 million",
        "poster_url": "https://example.com/living-bondage-poster.jpg",
        "trailer_url": "https://example.com/living-bondage-trailer.mp4",
        "genres": ["Supernatural", "Drama", "Thriller"],
        "languages": ["English", "Igbo"],
        "cast": [
            {"actor_name": "Swanky JKA", "character_name": "Nnamdi Okeke Jr.", "role_type": "actor"},
            {"actor_name": "Munachi Abii", "character_name": "Ego", "role_type": "actor"},
            {"actor_name": "Kenneth Okonkwo", "character_name": "Andy Okeke", "role_type": "actor"}
        ]
    },
    {
        "title": "Citation",
        "local_title": "Citation",
        "release_date": date(2020, 11, 6),
        "runtime": 151,
        "plot_summary": "A graduate student fights against sexual harassment and corruption in academia.",
        "director": "Kunle Afolayan",
        "producer": "Kunle Afolayan",
        "production_company": "KAP Motion Pictures",
        "production_state": "Ogun",
        "box_office_ng": "₦85 million",
        "poster_url": "https://example.com/citation-poster.jpg",
        "trailer_url": "https://example.com/citation-trailer.mp4",
        "genres": ["Drama", "Thriller"],
        "languages": ["English", "French", "Yoruba"],
        "cast": [
            {"actor_name": "Temi Otedola", "character_name": "Moremi Oluwa", "role_type": "actor"},
            {"actor_name": "Jimmy Jean-Louis", "character_name": "Professor N'Dyare", "role_type": "actor"},
            {"actor_name": "Joke Silva", "character_name": "Professor Ibukun Awosika", "role_type": "actor"}
        ]
    }
]

async def populate_movies():
    """Populate the database with sample movies"""
    print("Starting movie population...")
    
    try:
        # Get database session
        async with get_db_session() as db:
            # Check if movies already exist
            existing_movies = await db.execute("SELECT COUNT(*) FROM movies")
            count = existing_movies.scalar()
            
            if count > 0:
                print(f"Database already contains {count} movies. Clearing existing movies...")
                # Clear existing data
                await db.execute("DELETE FROM movie_cast")
                await db.execute("DELETE FROM movie_languages")
                await db.execute("DELETE FROM movie_genres")
                await db.execute("DELETE FROM movies")
                await db.commit()
                print("Existing movies cleared.")
            
            # Add new movies
            for movie_data in SAMPLE_MOVIES:
                print(f"Adding movie: {movie_data['title']}")
                
                # Create movie
                movie = Movie(
                    title=movie_data["title"],
                    local_title=movie_data["local_title"],
                    release_date=movie_data["release_date"],
                    runtime=movie_data["runtime"],
                    plot_summary=movie_data["plot_summary"],
                    director=movie_data["director"],
                    producer=movie_data["producer"],
                    production_company=movie_data["production_company"],
                    production_state=movie_data["production_state"],
                    box_office_ng=movie_data["box_office_ng"],
                    poster_url=movie_data["poster_url"],
                    trailer_url=movie_data["trailer_url"],
                    type=ContentType.MOVIE
                )
                
                db.add(movie)
                await db.flush()  # Get the movie ID
                
                # Add genres
                for genre in movie_data["genres"]:
                    movie_genre = MovieGenre(movie_id=movie.id, genre=genre)
                    db.add(movie_genre)
                
                # Add languages
                for language in movie_data["languages"]:
                    movie_language = MovieLanguage(movie_id=movie.id, language=language)
                    db.add(movie_language)
                
                # Add cast
                for cast_member in movie_data["cast"]:
                    movie_cast = MovieCast(
                        movie_id=movie.id,
                        actor_name=cast_member["actor_name"],
                        character_name=cast_member["character_name"],
                        role_type=CastRole.ACTOR
                    )
                    db.add(movie_cast)
            
            # Commit all changes
            await db.commit()
            print(f"Successfully added {len(SAMPLE_MOVIES)} movies to the database!")
            
    except Exception as e:
        print(f"Error populating movies: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(populate_movies())