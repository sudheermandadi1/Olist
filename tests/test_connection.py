from src.connection import get_connection
import logging
from src.utils.logger import logger


logger.info("database connection test has started")
connection = get_connection()
logger.info("Database connected test successful")

connection.close()
logger.info("database connection closed")
