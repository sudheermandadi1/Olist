from src.connection import get_connection
from src.utils.ml_logger import ml_logger

import pandas as pd
from sklearn.model_selection import train_test_split

def load_ml_dataset():
    ml_logger.info("loading ml dataset from postgresql")

    connection = get_connection()
    query =" SELECT * FROM ml_order_dataset;"

    try:
        df = pd.read_sql(query,connection)
        ml_logger.info(f"loaded {len(df)} records from database")
        ml_logger.info(f" shape of data: {df.shape}")

        return df
    except Exception:
        ml_logger.exception("failed to load the data from database")

        raise
    finally:
        connection.close()


def prepare_features(df):

    ml_logger.info("preparing target data and features data for model training.....")

    x = df.drop(columns =["order_id", "delayed"])

    y = df["delayed"]

    ml_logger.info(f"features shape: {x.shape}")
    ml_logger.info(f"target data shape: {y.shape}")

    return (x,y)

def spliting_data(x,y):
    ml_logger.info("spliting data into train and test data to prevent data leakage....")

    x_train, x_test, y_train, y_test = train_test_split(x,y,
                                                        test_size=0.2,
                                                        random_state=40,
                                                        stratify=y)

    ml_logger.info(f"x_train shape: {x_train.shape}")
    ml_logger.info(f"y_train shape: {y_train.shape}")
    ml_logger.info(f"x_test shape: {x_test.shape}")
    ml_logger.info(f"x_test shape: {y_test.shape}")

    return (x_train, x_test, y_train, y_test)


def prepare_data():
    df = load_ml_dataset()

    ml_logger.info("checking missing values in loaded data:")
    ml_logger.info(f"{df.isnull().sum()}")

    x,y = prepare_features(df)

    return spliting_data(x,y)

    

