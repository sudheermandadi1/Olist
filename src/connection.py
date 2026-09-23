import psycopg2
import os
from  src.utils.logger import logger


from dotenv import load_dotenv

load_dotenv()

def get_connection():
    logger.info("trying to connect to postgreSQL Database")
    try:

        connection = psycopg2.connect(
            host = os.getenv("DB_HOST"),
            port = os.getenv("DB_PORT"),
            user = os.getenv("DB_USER"),
            database = os.getenv("DB_NAME"),
            password = os.getenv("DB_PASSWORD")

        )

        logger.info("successfully connected to postgreSQL")
        return connection
    except Exception:
        logger.exception("failed to connect to database..")
        raise