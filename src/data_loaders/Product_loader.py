
import pandas as pd

from src.utils.logger import logger
from src.connection import get_connection
from psycopg2.extras import execute_values


def load_products(csv_path):

    logger.info("Starting product data loading...")

    df = pd.read_csv(csv_path)

    logger.info(
        f"Product CSV loaded: {len(df)} rows"
    )

    columns = [
        "product_id",
        "product_category_name",
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]

    # Convert numeric columns to numeric values.
    numeric_columns = [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    # Convert pandas NaN/NaT to Python None.
    data = []

    for row in df[columns].itertuples(
        index=False,
        name=None
    ):

        cleaned_row = tuple(
            None if pd.isna(value) else value
            for value in row
        )

        data.append(cleaned_row)

    connection = get_connection()
    cursor = connection.cursor()

    try:

        query = """
            INSERT INTO products (
                product_id,
                product_category_name,
                product_name_lenght,
                product_description_lenght,
                product_photos_qty,
                product_weight_g,
                product_length_cm,
                product_height_cm,
                product_width_cm
            )
            VALUES %s
            ON CONFLICT (product_id) DO NOTHING;
        """

        execute_values(
            cursor,
            query,
            data
        )

        connection.commit()

        logger.info(
            f"Successfully loaded {len(data)} products"
        )

    except Exception:

        connection.rollback()

        logger.exception(
            "Failed to load products"
        )

        raise

    finally:

        cursor.close()
        connection.close()

        logger.info(
            "Product database connection closed"
        )
        
