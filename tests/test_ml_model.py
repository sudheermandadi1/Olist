import pytest
from src.machine_learning.model import (
    create_models,
    create_pipeline,
    train_final_model,
    cross_validation_models,
    best_model,
    evaluate_model,save_model,

)

from sklearn.datasets import make_classification
from sklearn.pipeline import Pipeline
import pandas as pd

from tests.conftest import logger
@pytest.fixture
def sample_data():

    x = pd.DataFrame({
        "customer_city": [
            "Trier", "Berlin", "Hamburg", "Munich", "Trier",
            "Berlin", "Hamburg", "Munich", "Trier", "Berlin"
        ],
        "purchase_month": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "purchase_day_of_week": [0, 1, 2, 3, 4, 5, 6, 0, 1, 2],
        "num_of_products": [1, 2, 1, 3, 2, 4, 1, 2, 3, 1],
        "num_of_sellers": [1, 1, 2, 2, 1, 3, 1, 2, 2, 1],
        "num_of_categories": [1, 2, 1, 2, 2, 3, 1, 2, 3, 1],
        "total_price": [20, 50, 30, 100, 75, 150, 25, 60, 90, 40],
        "total_product_weight": [500, 1000, 750, 2000, 1200, 3000, 600, 900, 1500, 700]
    })

    y = pd.Series(
        [0, 1, 0, 1, 1, 0, 0, 1, 1, 0],
        name="target"
    )

    return x, y
def test_create_model():
    logger.info("StART:  test_create_model")
    models = create_models()
    logger.info("models created : %s", list(models.keys()))

    assert len(models) == 4
    assert "Logistic Regression" in models
    assert "Random Forest Classifier" in models
    assert "Decision Tree" in models
    assert "Gradient Boosting" in models
    logger.info("PASS : test_create_model")

def test_create_pipeline(sample_data):
    logger.info("START : test_create_pipeline")
    models = create_models()
    model = models["Decision Tree"]
    logger.info("Creating pipeline for Decision Tree")
    sam_Pipeline = create_pipeline(model)

    logger.info("Pipeline steps : %s", list(sam_Pipeline.named_steps.keys()))

    assert isinstance(sam_Pipeline,Pipeline)
    assert "preprocessor" in sam_Pipeline.named_steps
    assert "model" in sam_Pipeline.named_steps

    logger.info("PASS : test_create_pipeline")


def test_cross_validation_models(sample_data):
    logger.info("START: test_cross_validation_models")

    x, y = sample_data
    logger.info(
        "Running cross-validation with X shape=%s, y shape=%s",
        x.shape,
        y.shape,
    )
    results = cross_validation_models(x,y)
    assert len(results) == 4
    excepted_columns = ["model", "accuracy", "f1-score", "precision", "recall", "roc-auc"]

    assert list(results.columns) == excepted_columns
    logger.info("PASS: test_cross_validation_models")

def test_cross_validation_scores(sample_data):
    logger.info("START: test_cross_validation_scores")
    x,y = sample_data
    results = cross_validation_models(x,y)
    logger.info("Checking accuracy scores")
    assert results["accuracy"].between(0,1).all()

    logger.info("Checking precision scores")
    assert results["precision"].between(0,1).all()

    logger.info("Checking recall scores")
    assert results["recall"].between(0,1).all()

    logger.info("Checking F1 scores")
    assert results["f1-score"].between(0,1).all()

    logger.info("Checking ROC-AUC scores")
    assert results["roc-auc"].between(0,1).all()
    logger.info("PASS: test_cross_validation_scores")
    

def test_best_model():
    logger.info("START: test_best_model")
    data = { "model": [ "Logistic Regression", 
                        "Decision Tree", 
                        "Random Forest Classifier",
                        "Gradient Boosting", ],
                        "accuracy": [0.80, 0.82, 0.85, 0.84],
                        "f1-score": [0.75, 0.78, 0.88, 0.80],
                        "precision": [0.76, 0.79, 0.87, 0.81],
                        "recall": [0.74, 0.77, 0.89, 0.79],
                        "roc-auc": [0.80, 0.83, 0.91, 0.85], }

    data = pd.DataFrame(data)
    logger.info("Testing best model selection")
    best = best_model(data)

    logger.info("Selected best model: %s", best)
    assert best == "Random Forest Classifier"
    logger.info("PASS: test_best_model")


def test_train_final_model(sample_data):
    logger.info("START: test_train_final_model")
    x,y = sample_data

    logger.info("Training Logistic Regression model")
    sam_pipeline = train_final_model("Logistic Regression", x,y)
    logger.info("Model training completed")
    assert isinstance(sam_pipeline, Pipeline)

    pre = sam_pipeline.predict(x)
    logger.info(
        "Prediction completed. Number of predictions: %d",
        len(pre),
    )
    assert len(pre) == len(y)
    logger.info("PASS: test_train_final_model")


def test_evaluate_model(sample_data):
    logger.info("START: test_evaluate_model")
    x,y = sample_data
    logger.info("Training model for evaluation")
    pipeline = train_final_model("Logistic Regression", x, y)

    logger.info("Evaluating model")
    results = evaluate_model(pipeline, x, y)

    logger.info("Evaluation results: %s", results)
    assert isinstance(results, dict)

    expected_keys= ["accuracy", "precision", "recall", "f1", "roc_auc"]
    logger.info("Checking evaluation result keys")
    for keys in expected_keys:
        assert keys in results
    logger.info("Checking evaluation scores")
    for values in results.values():
        assert 0<= values <=1
    logger.info("PASS: test_evaluate_model")
    
    




