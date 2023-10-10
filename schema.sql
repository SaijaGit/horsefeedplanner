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
    amount FLOAT,
    FOREIGN KEY (feed_id) REFERENCES feeds (id) ON DELETE CASCADE
);

CREATE TABLE recommendations (	
    id SERIAL PRIMARY KEY,	
    weight_class INT,	
    exercise_level horse_exercise,	
    energy FLOAT,	
    energy_tolerance FLOAT,	
    protein FLOAT,	
    protein_tolerance FLOAT,	
    calcium FLOAT,	
    calcium_tolerance FLOAT,	
    phosphorus FLOAT,	
    phosphorus_tolerance FLOAT,	
    magnesium FLOAT,	
    magnesium_tolerance FLOAT,	
    iron FLOAT,	
    iron_tolerance FLOAT,	
    copper FLOAT,	
    copper_tolerance FLOAT,	
    zinc FLOAT,	
    zinc_tolerance FLOAT,	
    vitamin_a FLOAT,	
    vitamin_a_tolerance FLOAT,	
    vitamin_d3 FLOAT,	
    vitamin_d3_tolerance FLOAT,	
    vitamin_e FLOAT,	
    vitamin_e_tolerance FLOAT,	
    vitamin_b1 FLOAT,	
    vitamin_b1_tolerance FLOAT,	
    vitamin_b2 FLOAT,	
    vitamin_b2_tolerance FLOAT,	
    vitamin_b6 FLOAT,	
    vitamin_b6_tolerance FLOAT,	
    vitamin_b12 FLOAT,	
    vitamin_b12_tolerance FLOAT,	
    biotin FLOAT,	
    biotin_tolerance FLOAT,	
    niacin FLOAT,	
    niacin_tolerance FLOAT	
);	

