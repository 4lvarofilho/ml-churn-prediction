import json
from typing import Any, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.model import load_model


MODEL_PATH = "models/model.pkl"
METADATA_PATH = "models/model_metadata.json"

app = FastAPI(title="Previsão de Churn em Telecomunicações")

class Customer(BaseModel):
    data: Dict[str, Any]
    
@app.on_event("startup")
def load_artifacts():
    global MODEL, METADATA, FEATURES
    try:
        MODEL = load_model(MODEL_PATH)
        with open(METADATA_PATH, "r", encoding="utf-8") as file:
            METADATA = json.load(file)
        FEATURES = METADATA.get("features", [])
    except Exception as err:
        MODEL = None
        METADATA = {}
        FEATURES = []
        print("Erro ao carregar o modelo ou metadados:", err)
        
@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": MODEL is not None}

@app.get("/model-info")
def model_info():
    return {"meta": METADATA}

@app.post("/predict")
def predict(customer: Customer):
    if MODEL is None:
        raise HTTPException(status_code = 500, detail="Modelo não carregado.")
        
    import pandas as pd
    
    row = pd.DataFrame([customer.data])
    X = pd.get_dummies(row)
    
    for col in FEATURES:
        if col not in X.columns:
            X[col] = 0
    X = X[FEATURES]
    probability = MODEL.predict_proba(X)[:, 1][0]
    prediction = int(probability >= 0.5)
    return {"probability": float(probability), "prediction": prediction}
