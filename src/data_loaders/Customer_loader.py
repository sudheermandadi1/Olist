import pandas as pd
from psycopg2.extras import execute_values
from src.connection import get_connection
from src.utils.logger import logger

def load_customer(csv_path):
    logger.info("started customer data loading...")

    df = pd.read_csv(csv_path)
    logger.info(f"customer csv loaded:{len(df)} rows")

    columns = [
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state"
    ]

    data = list(
        df[columns].itertuples(index = False, name = None)

    )

    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """ 
          INSERT INTO customers(
                    customer_id,
                    customer_unique_id,
                    customer_zip_code_prefix,
                    customer_city,
                    customer_state
          )
          VALUES %s ON CONFLICT(customer_id) DO NOTHING;         

        """

        execute_values(cursor,  query, data)

        connection.commit()

        logger.info(f"succenfully loaded {len(data)} customers")

    except Exception:
        connection.rollback()

        logger.exception("failed to load customers")
        raise
    finally:
        cursor.close()
        connection.close()
        logger.info("customer database connection closed")
       
