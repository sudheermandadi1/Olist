
import pandas as pd

from src.utils.logger import logger
from src.connection import get_connection
from psycopg2.extras import execute_values


def load_orders(csv_path):

    logger.info("Started loading order data")

    df = pd.read_csv(csv_path)

    logger.info(f"Order CSV loaded: {len(df)} rows")

    columns = [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    # Convert date columns
    for col in date_columns:
        df[col] = pd.to_datetime(
            df[col],
            errors="coerce"
        )

    # Prepare data
    data = []

    for row in df[columns].itertuples(
        index=False,
        name=None
    ):

        cleaned_row = tuple(
            None if pd.isna(value)
            else value.to_pydatetime()
            if isinstance(value, pd.Timestamp)
            else value
            for value in row
        )

        data.append(cleaned_row)

    # Connect to database
    connection = get_connection()
    cursor = connection.cursor()

    try:

        query = """
            INSERT INTO orders (
                order_id,
                customer_id,
                order_status,
                order_purchase_timestamp,
                order_approved_at,
                order_delivered_carrier_date,
                order_delivered_customer_date,
                order_estimated_delivery_date
            )
            VALUES %s
            ON CONFLICT (order_id) DO NOTHING;
        """

        execute_values(
            cursor,
            query,
            data
        )

        connection.commit()

        logger.info(
            f"Successfully loaded {len(data)} orders"
        )

    except Exception:

        connection.rollback()

        logger.exception(
            "Failed to load orders dataset"
        )

        raise

    finally:

        cursor.close()
        connection.close()

        logger.info(
            "Order database connection has closed"
        )
