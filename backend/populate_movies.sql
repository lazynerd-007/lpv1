-- Populate database with sample movies
-- Clear existing data first
DELETE FROM movie_cast;
DELETE FROM movie_languages;
DELETE FROM movie_genres;
DELETE FROM movies;

-- Insert sample movies
INSERT INTO movies (id, title, local_title, release_date, runtime, plot_summary, director, producer, production_company, production_state, box_office_ng, poster_url, trailer_url, type) VALUES
(gen_random_uuid(), 'The Wedding Party', 'The Wedding Party', '2016-12-16', 110, 'A lavish wedding turns chaotic when family secrets and unexpected guests threaten to ruin the celebration.', 'Kemi Adetiba', 'Mo Abudu', 'EbonyLife Films', 'Lagos', '₦453 million', 'https://example.com/wedding-party-poster.jpg', 'https://example.com/wedding-party-trailer.mp4', 'movie'),

(gen_random_uuid(), 'King of Boys', 'King of Boys', '2018-10-26', 170, 'A businesswoman''s political ambitions are threatened when her past catches up with her.', 'Kemi Adetiba', 'Kemi Adetiba', 'KAP Motion Pictures', 'Lagos', '₦245 million', 'https://example.com/king-of-boys-poster.jpg', 'https://example.com/king-of-boys-trailer.mp4', 'movie'),

(gen_random_uuid(), 'Lionheart', 'Lionheart', '2018-12-21', 95, 'A young woman fights to save her father''s bus company from bankruptcy and corruption.', 'Genevieve Nnaji', 'Genevieve Nnaji', 'The Entertainment Network', 'Enugu', '₦150 million', 'https://example.com/lionheart-poster.jpg', 'https://example.com/lionheart-trailer.mp4', 'movie'),

(gen_random_uuid(), 'October 1', 'October 1', '2014-10-01', 143, 'A police detective investigates a series of murders in a colonial Nigerian town on the eve of independence.', 'Kunle Afolayan', 'Kunle Afolayan', 'Golden Effects Pictures', 'Ogun', '₦180 million', 'https://example.com/october-1-poster.jpg', 'https://example.com/october-1-trailer.mp4', 'movie'),

(gen_random_uuid(), 'Half of a Yellow Sun', 'Half of a Yellow Sun', '2013-09-08', 106, 'Two sisters navigate love and loss during the Nigerian Civil War.', 'Biyi Bandele', 'Andrea Calderwood', 'Potboiler Productions', 'Calabar', '₦95 million', 'https://example.com/half-yellow-sun-poster.jpg', 'https://example.com/half-yellow-sun-trailer.mp4', 'movie'),

(gen_random_uuid(), 'The Figurine', 'Araromire', '2009-10-09', 122, 'Two friends discover an ancient figurine that brings them luck, but at a terrible cost.', 'Kunle Afolayan', 'Kunle Afolayan', 'Golden Effects Pictures', 'Osun', '₦65 million', 'https://example.com/figurine-poster.jpg', 'https://example.com/figurine-trailer.mp4', 'movie'),

(gen_random_uuid(), 'Living in Bondage: Breaking Free', 'Living in Bondage: Breaking Free', '2019-11-08', 115, 'The son of a man who made a deal with dark forces must break the family curse.', 'Ramsey Nouah', 'Steve Gukas', 'Play Network Studios', 'Lagos', '₦125 million', 'https://example.com/living-bondage-poster.jpg', 'https://example.com/living-bondage-trailer.mp4', 'movie'),

(gen_random_uuid(), 'Citation', 'Citation', '2020-11-06', 151, 'A graduate student fights against sexual harassment and corruption in academia.', 'Kunle Afolayan', 'Kunle Afolayan', 'KAP Motion Pictures', 'Ogun', '₦85 million', 'https://example.com/citation-poster.jpg', 'https://example.com/citation-trailer.mp4', 'movie');

-- Add genres for the movies
-- Note: We'll use a simplified approach since we can't easily reference the movie IDs
-- In a real scenario, you'd need to get the actual UUIDs from the inserted movies

-- For demonstration, let's add some sample genres
WITH movie_ids AS (
    SELECT id, title FROM movies WHERE title IN (
        'The Wedding Party', 'King of Boys', 'Lionheart', 'October 1', 
        'Half of a Yellow Sun', 'The Figurine', 'Living in Bondage: Breaking Free', 'Citation'
    )
)
INSERT INTO movie_genres (movie_id, genre)
SELECT m.id, g.genre
FROM movie_ids m
CROSS JOIN (
    SELECT 'Comedy' as genre UNION ALL
    SELECT 'Romance' UNION ALL
    SELECT 'Drama' UNION ALL
    SELECT 'Crime' UNION ALL
    SELECT 'Thriller' UNION ALL
    SELECT 'Family' UNION ALL
    SELECT 'Mystery' UNION ALL
    SELECT 'War' UNION ALL
    SELECT 'Supernatural'
) g
WHERE 
    (m.title = 'The Wedding Party' AND g.genre IN ('Comedy', 'Romance', 'Drama')) OR
    (m.title = 'King of Boys' AND g.genre IN ('Crime', 'Drama', 'Thriller')) OR
    (m.title = 'Lionheart' AND g.genre IN ('Drama', 'Family')) OR
    (m.title = 'October 1' AND g.genre IN ('Mystery', 'Thriller', 'Drama')) OR
    (m.title = 'Half of a Yellow Sun' AND g.genre IN ('Drama', 'Romance', 'War')) OR
    (m.title = 'The Figurine' AND g.genre IN ('Supernatural', 'Thriller', 'Drama')) OR
    (m.title = 'Living in Bondage: Breaking Free' AND g.genre IN ('Supernatural', 'Drama', 'Thriller')) OR
    (m.title = 'Citation' AND g.genre IN ('Drama', 'Thriller'));

-- Add languages for the movies
WITH movie_ids AS (
    SELECT id, title FROM movies WHERE title IN (
        'The Wedding Party', 'King of Boys', 'Lionheart', 'October 1', 
        'Half of a Yellow Sun', 'The Figurine', 'Living in Bondage: Breaking Free', 'Citation'
    )
)
INSERT INTO movie_languages (movie_id, language)
SELECT m.id, l.language
FROM movie_ids m
CROSS JOIN (
    SELECT 'English' as language UNION ALL
    SELECT 'Yoruba' UNION ALL
    SELECT 'Igbo' UNION ALL
    SELECT 'French'
) l
WHERE 
    (m.title = 'The Wedding Party' AND l.language IN ('English', 'Yoruba')) OR
    (m.title = 'King of Boys' AND l.language IN ('English', 'Yoruba')) OR
    (m.title = 'Lionheart' AND l.language IN ('English', 'Igbo')) OR
    (m.title = 'October 1' AND l.language IN ('English', 'Yoruba')) OR
    (m.title = 'Half of a Yellow Sun' AND l.language IN ('English', 'Igbo')) OR
    (m.title = 'The Figurine' AND l.language IN ('English', 'Yoruba')) OR
    (m.title = 'Living in Bondage: Breaking Free' AND l.language IN ('English', 'Igbo')) OR
    (m.title = 'Citation' AND l.language IN ('English', 'French', 'Yoruba'));

-- Add some sample cast members
WITH movie_ids AS (
    SELECT id, title FROM movies WHERE title IN (
        'The Wedding Party', 'King of Boys', 'Lionheart', 'October 1', 
        'Half of a Yellow Sun', 'The Figurine', 'Living in Bondage: Breaking Free', 'Citation'
    )
)
INSERT INTO movie_cast (movie_id, actor_name, character_name, role_type)
SELECT m.id, c.actor_name, c.character_name, 'actor'
FROM movie_ids m
CROSS JOIN (
    SELECT 'Adesua Etomi' as actor_name, 'Dunni Coker' as character_name, 'The Wedding Party' as movie_title UNION ALL
    SELECT 'Banky W', 'Dozie', 'The Wedding Party' UNION ALL
    SELECT 'RMD', 'Chief Felix Onwuka', 'The Wedding Party' UNION ALL
    SELECT 'Sola Sobowale', 'Eniola Salami', 'King of Boys' UNION ALL
    SELECT 'Adesua Etomi', 'Kemi', 'King of Boys' UNION ALL
    SELECT 'Reminisce', 'Makanaki', 'King of Boys' UNION ALL
    SELECT 'Genevieve Nnaji', 'Adaeze Obiagu', 'Lionheart' UNION ALL
    SELECT 'Nkem Owoh', 'Godswill', 'Lionheart' UNION ALL
    SELECT 'Pete Edochie', 'Chief Ernest Obiagu', 'Lionheart' UNION ALL
    SELECT 'Sadiq Daba', 'Inspector Danladi Waziri', 'October 1' UNION ALL
    SELECT 'Kayode Olaiya', 'Agbekoya', 'October 1' UNION ALL
    SELECT 'David Bailie', 'Father Dowling', 'October 1'
) c
WHERE m.title = c.movie_title;

-- Display the results
SELECT 
    m.title,
    m.director,
    m.release_date,
    m.runtime,
    STRING_AGG(DISTINCT mg.genre, ', ') as genres,
    STRING_AGG(DISTINCT ml.language, ', ') as languages
FROM movies m
LEFT JOIN movie_genres mg ON m.id = mg.movie_id
LEFT JOIN movie_languages ml ON m.id = ml.movie_id
GROUP BY m.id, m.title, m.director, m.release_date, m.runtime
ORDER BY m.release_date DESC;