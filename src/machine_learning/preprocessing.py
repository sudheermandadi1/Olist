from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

from sklearn.pipeline import Pipeline
from src.utils.ml_logger import ml_logger

def create_preprocessor():
    try:
        
        ml_logger.info("data preprocessing process has started...")
        categorical_features = ["customer_city"]
        numerical_features = [

            "purchase_month",

            "purchase_day_of_week",

            "num_of_products",

            "num_of_sellers",

            "num_of_categories",

            "total_price",

            "total_product_weight"
        ]   

        categorical_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("encoder", OneHotEncoder(handle_unknown="ignore"))
            ]
        
        )

        numerical_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="mean")),
                ("scaler", StandardScaler())
            ]
        )

        preprocessor = ColumnTransformer(
            transformers=[
                ("categorical", categorical_pipeline, categorical_features),
                ("numerical", numerical_pipeline, numerical_features)
            ]

        )

        ml_logger.info("data preprocesing is completed....")



        return preprocessor

    except Exception:
        ml_logger.exception("data preprocessing is failed...")

        raise
    




    

     