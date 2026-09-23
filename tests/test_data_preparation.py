from src.machine_learning.data_preparation import prepare_features
import pandas as pd

def test_prepare_features():
    df = pd.DataFrame({
        "order_id": ["A", "B"],
        "customer_state": ["SP", "RJ"],
        "number_of_items": [1, 3],
        "total_price": [100.0, 350.0],
        "delayed": [0, 1]
    })

    X,Y = prepare_features(df)
    assert len(X) == len(df)
    assert len(Y) == len(df)

    assert "delayed" not in X.columns
    assert "order_id" not in X.columns


def test_target_values():
    df = pd.DataFrame({
        "order_id" : ["A", "B", "C"],
        "delayed" :[0,1,0]
    })

    assert set(df["delayed"].unique()).issubset({0,1})

def test_one_row_per_order():
    df = pd.DataFrame({
        "order_id" : ["A", "B", "C"],
        "delayed" :[0,1,0]
    })

    assert len(df) == df["order_id"].nunique()




