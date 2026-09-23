from src.machine_learning.data_preparation import prepare_data
from src.machine_learning.preprocessing import create_preprocessor

from src.machine_learning.model import (

    create_models,
    create_pipeline,
    cross_validation_models,
    best_model,
    train_final_model,
    evaluate_model,
    save_model
)

from src.utils.ml_logger import ml_logger


def main():
    ml_logger.info("="*80)
    ml_logger.info("OLIST PIPELINE HAS STARTED.......")
    ml_logger.info("="*80)

    try:
        

        (x_train, x_test, y_train, y_test) = prepare_data()

        results = cross_validation_models(x_train, y_train)
        ml_logger.info("-"*80)
        ml_logger.info("Displaying model comparisions....")
        ml_logger.info("-"*80)
        ml_logger.info(results.to_string(index = False))

        best_model_name = best_model(results)

        final_pipeline = train_final_model(best_model_name, x_train, y_train)

        final_metrics = evaluate_model(final_pipeline, x_test, y_test)

        save_model(final_pipeline)

        ml_logger.info("="*80)
        ml_logger.info("OLIST ML PIPELINE COMPLETED.....")
        ml_logger.info("="*80)

    except Exception:
        ml_logger.exception("OLIST ML PIPELINE FAILED")

        raise


if __name__ == "__main__":
    main()





