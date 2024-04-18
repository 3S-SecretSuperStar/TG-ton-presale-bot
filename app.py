
import os
import time
import logging
import schedule
import datetime
from src.Database import Database
from src.Scheduler import Scheduler
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

 # Get the value of the environment variables
DELETE_FILES_OLDER_THAN_DAYS = int(os.environ.get('DELETE_FILES_OLDER_THAN_DAYS', '30'))        # default 30
DELETE_SERVICE_INTERVAL=int(os.environ.get('DELETE_SERVICE_INTERVAL', '12'))        # default 12
SCRAPPING_INTERVAL=int(os.environ.get('SCRAPPING_INTERVAL', '1'))        # default 12
HOST = os.environ.get('DB_HOST', 'localhost')
DB_DATABASE = os.environ.get('DB_DATABASE', 'presalebot')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'presalebot')
PORT = os.environ.get('PORT', '5432')




def config_log():
    # Configure logging
    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Create the full path to the log file
    formatted_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filepath = os.path.join(log_directory, f"log_{formatted_datetime}.txt")

    logging.basicConfig(filename=log_filepath, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Log File Created Successfully")
    return logging

def config_db(logging):
    db_directory = "db"
    if not os.path.exists(db_directory):
        os.makedirs(db_directory)
    
    # Set up database connection
    db = Database(logging=logging, host=HOST, port=PORT, database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD)
    status = db.connect()
    if status == False:
        logging.error("Error connecting to database")
        return None
    return db

def delete_old_logs():
    logging.info('........................................................')
    logging.info('............Delete Log Scheduler........................')
    # Get current date
    current_date = datetime.datetime.now()

    # Define the directory containing the log files
    log_directory = "logs/"

    filelist = os.listdir(log_directory)
    # Iterate over files in the logs directory
    for filename in filelist:
        filepath = os.path.join(log_directory, filename)
        # Check if the file is a regular file
        if os.path.isfile(filepath):
            try:
                # Get the creation time of the file
                creation_time = datetime.datetime.fromtimestamp(os.path.getctime(filepath))
                # Calculate the difference in days
                delta_days = (current_date - creation_time).days
                # Check if the file is older than 30 days
                if delta_days > DELETE_FILES_OLDER_THAN_DAYS:
                    # Delete the file
                    os.remove(filepath)
                    
                    logging.info(f"Deleted old log file: {filename}")
                    
            except Exception as e:
                logging.error('Error deleting old log file:', e)

    logging.info('........................................................')



# Config Logging
logging = config_log()

# Config Database as well as the mapping directory
db = config_db(logging)

if db == None:
    logging.error("Error connecting to database")
    exit(1)

logging.info("Database Connected Successfully")

# Set up pinksale scheduler
scheduler = Scheduler(logging=logging, db=db)

# Schedule the delete log files job to run every 12 hours
schedule.every(DELETE_SERVICE_INTERVAL).hours.do(delete_old_logs)

# Schedule the pinksale scrapping job to Run the every 4 hours
schedule.every(SCRAPPING_INTERVAL).hours.do(scheduler.run)

error_message = f"System Deployed Successfully, Interval: {SCRAPPING_INTERVAL}"
logging.info(error_message)
# Run indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)

