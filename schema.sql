CREATE TYPE user_role AS ENUM('basic', 'admin');

CREATE TYPE horse_exercise AS ENUM('Rest', 'Light work', 'Moderate work', 'Heavy work');

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role user_role
);

CREATE TABLE horses (
    id SERIAL PRIMARY KEY,               
    horse_name TEXT,
    birth_year INT,
    weight_class INT,
    exercise_level horse_exercise,
    owner_id INT
);

CREATE TABLE feeds (
    id SERIAL PRIMARY KEY,
    owner_id INT,
    name TEXT,
    moisture FLOAT, 
    energy FLOAT, 
    protein FLOAT, 
    fat FLOAT, 
    fiber FLOAT, 
    starch FLOAT, 
    sugar FLOAT, 
    calcium FLOAT, 
    phosphorus FLOAT, 
    magnesium FLOAT, 
    sodium FLOAT, 
    iron FLOAT, 
    copper FLOAT, 
    manganese FLOAT, 
    zinc FLOAT, 
    iodine FLOAT, 
    selenium FLOAT, 
    cobalt FLOAT, 
    vitamin_a FLOAT, 
    vitamin_d3 FLOAT, 
    vitamin_e FLOAT, 
    vitamin_b1 FLOAT, 
    vitamin_b2 FLOAT, 
    vitamin_b6 FLOAT, 
    vitamin_b12 FLOAT, 
    biotin FLOAT, 
    niacin FLOAT
);

CREATE TABLE nutritions (
    id SERIAL PRIMARY KEY,
    reference TEXT,
    name TEXT,
    symbol TEXT,
    unit TEXT,
    description TEXT
);

CREATE TABLE diets (
    id SERIAL PRIMARY KEY,               
    horse_id INT,
    feed_id INT,
    amount FLOAT
);


