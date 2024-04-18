-- init.sql


-- CREATE DATABASE presalebot;

-- USE presalebot


CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    url VARCHAR(255) UNIQUE,
    name VARCHAR(255), 
    symbol VARCHAR(255),
    web VARCHAR(255),
    twitter VARCHAR(255),
    telegram VARCHAR(255),
    token_address VARCHAR(255),
    supply VARCHAR(255),
    pool_address VARCHAR(255),
    soft_cap VARCHAR(255),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    lockup_time VARCHAR(255),
    rate VARCHAR(255),
    raised VARCHAR(255),
    scrap_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

