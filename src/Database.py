
import psycopg2
import time
import logging

class Database:
    def __init__(self, logging, host, port, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.conn = None
        self.cur = None
        self.logging = logging

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                user=self.user, 
                password=self.password, 
                host=self.host, 
                port= self.port,
                database=self.database, 
            )
            #self.conn.autocommit = True
            self.cur = self.conn.cursor()
            return True
        except Exception as exp:
            self.logging.error(f"Error connecting to database: {exp}")
            return False

        #self.create_table()

    def close(self):
        if self.conn:
            self.cur.close()
            self.conn.close()

    def create_table(self):
        try:
            # Check if the database exists
            self.cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'presalebot'")
            database_exists = self.cur.fetchone()
            
            # If the database doesn't exist, create it
            if not database_exists:
                self.cur.execute("CREATE DATABASE presalebot")
                self.logging.info("Database 'presalebot' created successfully.")
            else:
                self.logging.info("Database 'presalebot' already exists.")
            

            # # Create projects table
            # self.cur.execute("""
            #     CREATE TABLE IF NOT EXISTS projects (
            #         id SERIAL PRIMARY KEY,
            #         url VARCHAR(255) UNIQUE
            #     )
            # """)
            # logging.info("Table 'projects' created successfully.")

            # Create project_info table
            self.cur.execute("""
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
                )
            """)
            self.logging.info("Table 'project_info' created successfully.")

        except psycopg2.Error as e:
            self.logging.error("Error: %s", e)


    

    def check_project_url(self, url):
        self.cur.execute("SELECT * FROM projects WHERE url = %s", (url,))
        existing_link = self.cur.fetchone()
        if existing_link is None:
            existing_link = False
        return existing_link


    def insert_project_data(self, url, data):
        # self.cur.execute("INSERT INTO projects (url) VALUES (%s)", (url,))
        # self.conn.commit()

        try:
            # Begin a transaction
            #self.conn.autocommit = False
            #self.conn.begin()

            # Insert URL into the projects table
            # self.cur.execute("INSERT INTO projects (url) VALUES (%s) RETURNING id", (url,))
            # project_id = self.cur.fetchone()[0]  # Get the generated project ID

            # Insert URL-related data into the project_info table
            self.cur.execute("""
                INSERT INTO projects (
                    url,name, symbol, web, twitter, telegram, token_address, supply,
                    pool_address, soft_cap, start_time, end_time, lockup_time, rate, raised
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                url, data.name, data.symbol, data.web, data.twitter, data.telegram, data.token_address, data.supply,
                    data.pool_address, data.soft_cap, data.start_time, data.end_time, data.lockup_time, data.rate, data.raised
            ))

            # Commit the transaction
            self.conn.commit()
            self.logging.info("Data inserted successfully.")
            return True

        except Exception as e:
            # Rollback the transaction in case of an error
            self.conn.rollback()
            self.logging.error("Error while adding record to DB: %s", e)
            return False
        

if __name__ == "__main__":
    db = Database("localhost", "presalebot", "postgres", "presalebot")
    db.connect()
    db.create_table()
    db.close()