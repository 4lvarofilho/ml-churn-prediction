from typing import Tuple, List
import pandas as pd
import numpy as np

def basic_preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    if "customerID" in df.columns:
        df = df.drop(columns=["customerID"])
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"].replace(" ", np.nan), errors='coerce')
        df["TotalCharges"] = df["TotalCharges"].fillna(0.0)
    if "Churn" in df.columns:
        df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
    return df

def featurize(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series, List[str]]:
    df = basic_preprocess(df)
    
    service_cols = [
        "PhoneService",
        "MultipleLines",
        "InternetService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies"
    ]
    services_present = [col for col in service_cols if col in df.columns]
    if services_present:
        df["n_services"] = df[services_present].apply(lambda row: sum(x not in ["No", "No internet service", "No phone service", np.nan] for x in row), axis=1)
    
    cat_cols = df.select_dtypes(include=["object"]).columns.tolist()
    cat_cols = [col for col in cat_cols if col != "Churn"]
    df = pd.get_dummies(df, columns=cat_cols, drop_first=True)
    
    if "Churn" in df.columns:
        y = df["Churn"]
        X = df.drop(columns=["Churn"])
    else:
        y = pd.Series(dtype=int)
        X = df
    feature_names = X.columns.tolist()
    return X, y, feature_names