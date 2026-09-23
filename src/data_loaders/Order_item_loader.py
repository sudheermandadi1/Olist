import pandas as pd

from psycopg2.extras import execute_values

from src.connection import get_connection
from src.utils.logger import logger


def load_order_items(csv_path):

    logger.info("Starting order item loading")

    df = pd.read_csv(csv_path)

    logger.info(
        f"Order item CSV loaded: {len(df)} rows"
    )

    columns = [
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "shipping_limit_date",
        "price",
        "freight_value"
    ]

    df["shipping_limit_date"] = pd.to_datetime(
        df["shipping_limit_date"],
        errors="coerce"
    )

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
        INSERT INTO order_items (
            order_id,
            order_item_id,
            product_id,
            seller_id,
            shipping_limit_date,
            price,
            freight_value
        )
        VALUES %s
        ON CONFLICT (order_id, order_item_id) DO NOTHING;
        """

        execute_values(
            cursor,
            query,
            data
        )

        connection.commit()

        logger.info(
            f"Successfully loaded {len(data)} order items"
        )

    except Exception:

        connection.rollback()

        logger.exception(
            "Failed to load order items"
        )

        raise

    finally:

        cursor.close()
        connection.close()

        logger.info("Order item database connection closed")