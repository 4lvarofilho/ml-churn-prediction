import argparse
import json
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

from data import load_from_bigquery, load_local_csv
from features import featurize
from model import train_model, evaluate_model, save_model

MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-bq", action="store_true", help="Ler dados do BigQuery")
    parser.add_argument("--bq-project", type=str, default=None)
    parser.add_argument("--dataset", type=str, default=None)
    parser.add_argument("--table", type=str, default=None)
    parser.add_argument("--csv", type=str, default="data/raw/telecom_churn.csv")
    parser.add_argument("--out", type=str, default=str(MODEL_DIR / "model.pkl"))
    parser.add_argument("--meta", type=str, default=str(MODEL_DIR / "model_metadata.json"))
    args = parser.parse_args()
    
    if args.from_bq:
        if not (args.bq_project and args.dataset and args.table):
            raise SystemExit("Quando --from-bq, --project, --dataset e --table são obrigatorios.")
        df = load_from_bigquery(args.bq_project, args.dataset, args.table)
    else:
        df = load_local_csv(args.csv)
    
    X, y, features = featurize(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    model = train_model(X_train, y_train)
    metrics = evaluate_model(model, X_test, y_test)
    
    save_model(model, args.out)
    meta = {"metrics": metrics, "features": features}
    with open(args.meta, "w", encoding="utf-8") as file:
        json.dump(meta, file, indent=4)
        
    print("Treinamento finalizado. Modelo salvo em: ", args.out)
    print("Métricas de avaliação: ", metrics)

if __name__ == "__main__":
    main()