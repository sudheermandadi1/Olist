import pandas as pd

from psycopg2.extras import execute_values

from src.connection import get_connection
from src.utils.logger import logger


def load_sellers(csv_path):

    logger.info("Starting seller loading")

    df = pd.read_csv(csv_path)

    logger.info(
        f"Seller CSV loaded: {len(df)} rows"
    )

    columns = [
        "seller_id",
        "seller_zip_code_prefix",
        "seller_city",
        "seller_state"
    ]

    data = list(
        df[columns].itertuples(
            index=False,
            name=None
        )
    )

    connection = get_connection()
    cursor = connection.cursor()

    try:

        query = """
        INSERT INTO sellers (
            seller_id,
            seller_zip_code_prefix,
            seller_city,
            seller_state
        )
        VALUES %s
        ON CONFLICT (seller_id) DO NOTHING;
        """

        execute_values(
            cursor,
            query,
            data
        )

        connection.commit()

        logger.info(
            f"Successfully loaded {len(data)} sellers"
        )

    except Exception:

        connection.rollback()

        logger.exception(
            "Failed to load sellers"
        )

        raise

    finally:

        cursor.close()
        connection.close()

        logger.info("Seller database connection closed")