# PreSaleBot
A Web Scrapper to scrap information about Pre-Sales of different Crypto projects on Solana, BSC and other blockchains. 


## Requirements

- Python 3.12.2
- VPN (as Twitter API was not accessible w/o it.)
- Maximum 5 Calls in 15 minutes (as per twitter basic plan). If plan is upgraded to enterprise, update RATE_LIMIT and RATE_LIMIT_DURATION variables in .env file

## Local Deployment

### Setup

1. Create a virtual environment:

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Run the Application
```bash
    python app.py  
```



# Docker

### Install Docker

 https://www.docker.com/get-started

### Pull PostgreSQL Docker Image

 ```
 docker pull postgres
 ```

### Run PostgreSQL Container:

 ```
 docker run --name presalebot -e POSTGRES_PASSWORD=presalebot -d -p 5432:5432 -v ~/RNS-Projects/CoinChance/PreSale-Scrapping/db/:/var/lib/postgresql/data postgres
 ```

- Error:

If the following error is reported on starting docker, 

 ```
 Error starting userland proxy: listen tcp4 0.0.0.0:5434: bind: address already in use.
 ```

Do the following: 

* Identify what is running in port 5432: sudo lsof -i :5432
* Kill all the processes that are running under this port: sudo kill -9 <pid>
* Run the command again to verify no process is running now: sudo lsof -i :5432

### Connect to the Database
Once the docker is launched, connect to the PostgreSQL database using any PostgreSQL client or command-line tools.

 ```
 docker exec -it presalebot psql -U postgres
 ```

### Create Database and Table 
Once connected to PostgreSQL, you can create a database and a table to store your links. Here's an example SQL script:

 ```
CREATE DATABASE presalebot;
\c presalebot;

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    url VARCHAR(255) UNIQUE
);

CREATE TABLE project_info (
    id SERIAL PRIMARY KEY,
    project_id INT REFERENCES projects(id),
    name VARCHAR(255), 
    symbol VARCHAR(255),
    web VARCHAR(255),
    twitter VARCHAR(255),
    telegram VARCHAR(255),
    token_address VARCHAR(255),
    supply VARCHAR(255),           -- 1,000,000,000
    pool_address VARCHAR(255),
    soft_cap VARCHAR(255),
    start_time TIMESTAMP,   -- 2024-04-03 18:00:00 (UTC)
    end_time TIMESTAMP,     -- 2024-04-03 18:00:00 (UTC)
    lockup_time VARCHAR(255),   -- 120 days after pool ends
    rate VARCHAR(255),  -- 1 SOL = 155,411.3105 $BOOB
    raised VARCHAR(255),    -- 2,687.3787 SOL (2687.38%)
    scrap_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

 ```

### Command Line Interaction with POSTGRES Docker

```
docker exec -it presalebot psql -U postgres -d presalebot -U postgres -d presalebot
```


### Deploy Dockers
```
docker-compose up --build
```