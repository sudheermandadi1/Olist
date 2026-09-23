from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import StratifiedKFold, cross_validate

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (RandomForestClassifier, GradientBoostingClassifier)

from sklearn.metrics import(f1_score, accuracy_score, recall_score, roc_auc_score, 
    precision_score,confusion_matrix, classification_report)

from src.utils.ml_logger import ml_logger

from src.machine_learning.preprocessing import create_preprocessor



def create_models():
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
        "Decision Tree" : DecisionTreeClassifier(random_state=42,class_weight="balanced"),
        "Random Forest Classifier" : RandomForestClassifier(n_estimators=150, random_state=42, n_jobs= -1, class_weight="balanced"),
        "Gradient Boosting" : GradientBoostingClassifier(random_state= 42)


    }

    return models

def create_pipeline(model):
    pipeline = Pipeline(
        steps =[
            ("preprocessor", create_preprocessor()),
            ("model", model)
        ]

            )

    return pipeline

def cross_validation_models(x_train, y_train):
    models = create_models()

    cv = StratifiedKFold(
        n_splits= 5,
        shuffle=True,
        random_state= 42
    )

    scoring = {
        "accuracy" : "accuracy",
        "precision" : "precision",
        "recall" : "recall",
        "f1" : "f1",
        "roc_auc" : "roc_auc"
    }

    results =[]

    for model_name, model in models.items():

        ml_logger.info(f"cross validation has started for model : {model_name}")

        pipeline = create_pipeline(model)

        scores = cross_validate(
            pipeline,
            x_train,y_train,
            cv = cv,
            scoring= scoring,
            n_jobs= -1
        )


        result = {
             "model" : model_name,
             "accuracy" : scores["test_accuracy"].mean(),
             "f1-score" : scores["test_f1"].mean(),
             "precision" : scores["test_precision"].mean(),
             "recall" : scores["test_recall"].mean(),
             "roc-auc" : scores["test_roc_auc"].mean()

        }

        results.append(result)

        ml_logger.info(f"cross-validation completed for model : {model_name}")

    results_df = pd.DataFrame(results)

    return results_df


def best_model(df):

    best_row = df.loc[df["f1-score"].idxmax()]

    best_model_name = best_row["model"]

    ml_logger.info("="*80)
    ml_logger.info(f"selected best model is : {best_model_name}")
    ml_logger.info("="*80)

    return best_model_name

def train_final_model(model_name, x_train, y_train):
    ml_logger.info("="*80)
    ml_logger.info("final model training has started.....") 
    models = create_models()
    model = models[model_name]
    pipeline = create_pipeline(model)

    pipeline.fit(x_train,y_train)

    ml_logger.info("final model training completed....")

    return pipeline

def evaluate_model(pipeline, x_test, y_test):
    ml_logger.info("Evaluating final model on test data..")

    y_pred = pipeline.predict(x_test)

    y_probs = pipeline.predict_proba(x_test)[:, 1]


    accuracy = accuracy_score(y_test, y_pred)

    precision = precision_score(y_test, y_pred)

    recall =  recall_score(y_test, y_pred)

    f1 = f1_score(y_test, y_pred)

    roc_auc = roc_auc_score(y_test, y_probs)


    ml_logger.info("=="*40)
    ml_logger.info("Final test results:")
    ml_logger.info("=="*40)

    ml_logger.info(f"Accuracy : {accuracy:.4f}")
    ml_logger.info(f"Precision : {precision:.4f}")
    ml_logger.info(f"Recall {recall:.4f}")
    ml_logger.info(f"F1-score : {f1:.4f}")
    ml_logger.info(f"Roc-auc : {roc_auc:.4f}")

    ml_logger.info("Confusion Matrix:  ")
    ml_logger.info(confusion_matrix(y_test, y_pred))

    return {
        "accuracy" : accuracy,
        "precision": precision,
        "recall" : recall,
        "f1" : f1,
        "roc_auc" : roc_auc

    }


def save_model(pipeline, filename = "saved_models/olist_model.pkl"):
    Path("saved_models").mkdir(exist_ok = True)

    joblib.dump(pipeline, filename)

    ml_logger.info(f"model has saved to :  {filename}")

















    











    


