CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE horses (
    id SERIAL PRIMARY KEY,               
    horse_name VARCHAR(255),
    birth_year INT,
    weight_class INT,
    exercise_level INT,
    owner_id INT
);

