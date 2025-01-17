-- Create a database
CREATE DATABASE movie_database;

-- Use the database
USE movie_database;

-- Create a table
CREATE TABLE movies (
    Poster_Link VARCHAR(2083),
    Series_Title VARCHAR(255),
    Released_Year INT,
    Certificate VARCHAR(50),
    Runtime VARCHAR(50),
    Genre VARCHAR(255),
    IMDB_Rating DECIMAL(3, 1),
    Overview TEXT,
    Meta_score INT,
    Director VARCHAR(255),
    Star1 VARCHAR(255),
    Star2 VARCHAR(255),
    Star3 VARCHAR(255),
    Star4 VARCHAR(255),
    No_of_Votes INT,
    Gross BIGINT
);

-- Insert data
INSERT INTO movies (Poster_Link, Series_Title, Released_Year, Certificate, Runtime, Genre, IMDB_Rating, Overview, Meta_score, Director, Star1, Star2, Star3, Star4, No_of_Votes, Gross)
VALUES
('https://example.com/poster1.jpg', 'Movie Title 1', 2022, 'PG-13', '120 min', 'Drama', 8.5, 'An example overview.', 85, 'Director Name', 'Star1', 'Star2', 'Star3', 'Star4', 100000, 15000000),
('https://example.com/poster2.jpg', 'Movie Title 2', 2021, 'R', '95 min', 'Comedy', 7.2, 'Another example overview.', 72, 'Director Name 2', 'StarA', 'StarB', 'StarC', 'StarD', 50000, 7500000);

-- Select data
SELECT * FROM movies;
