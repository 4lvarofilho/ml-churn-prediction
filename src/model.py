from typing import Dict
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, roc_auc_score


def train_model(X, y, random_state: int = 42) -> RandomForestClassifier:
    classifier = RandomForestClassifier(n_estimators = 200, random_state = random_state, n_jobs = -1)
    classifier.fit(X, y)
    return classifier

def evaluate_model(classifier: RandomForestClassifier, X_test, y_test) -> Dict[str, float]:
    probabilities = classifier.predict_proba(X_test)[:, 1]
    predictions = classifier.predict(X_test)
    
    return {
        "roc_auc": float(roc_auc_score(y_test, probabilities)),
        "precision": float(precision_score(y_test, predictions)),
        "recall": float(recall_score(y_test, predictions))
    }
    
def save_model(obj, path: str):
    joblib.dump(obj, path)
    
def load_model(path: str):
    return joblib.load(path)