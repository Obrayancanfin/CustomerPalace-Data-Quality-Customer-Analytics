"""Optional churn classification baseline. Exploratory only, not a production model."""
from pathlib import Path
import json

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "customers_clean.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def main():
    if not DATA.exists():
        raise FileNotFoundError("Lancez d'abord : python src/pipeline.py")
    df = pd.read_csv(DATA)
    df = df[df["churned"].isin(["Yes", "No"])].copy()
    y = (df["churned"] == "Yes").astype(int)

    # Exclude IDs, direct identifiers and date/tenure fields whose availability at prediction time
    # cannot be established from the supplied dataset.
    excluded = {"customer_id", "churned", "signup_date", "last_login", "tenure_months"}
    X = df.drop(columns=[c for c in excluded if c in df.columns])
    # Remove fields that are entirely empty after cleaning.
    X = X.dropna(axis=1, how="all")
    numeric = X.select_dtypes(include="number").columns.tolist()
    categorical = [c for c in X.columns if c not in numeric]

    prep_num = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    prep_cat = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])
    prep = ColumnTransformer([
        ("numeric", prep_num, numeric),
        ("categorical", prep_cat, categorical),
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    models = {
        "baseline_majoritaire": DummyClassifier(strategy="most_frequent"),
        "regression_logistique": Pipeline([
            ("preprocessing", prep),
            ("model", LogisticRegression(max_iter=2000, class_weight="balanced", random_state=42)),
        ]),
    }
    results = {
        "note": "Expérience exploratoire. Les variables peuvent avoir été mesurées après le churn; vérifier leur disponibilité réelle avant toute interprétation opérationnelle.",
        "target": "churned (Yes=1, No=0)",
        "n_rows": int(len(df)),
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "test_size": 0.25,
        "random_state": 42,
        "features": X.columns.tolist(),
        "models": {},
    }
    for name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        results["models"][name] = {
            "accuracy": round(float(accuracy_score(y_test, pred)), 4),
            "precision": round(float(precision_score(y_test, pred, zero_division=0)), 4),
            "recall": round(float(recall_score(y_test, pred, zero_division=0)), 4),
            "f1": round(float(f1_score(y_test, pred, zero_division=0)), 4),
            "confusion_matrix_labels_order": ["No (0)", "Yes (1)"],
            "confusion_matrix": confusion_matrix(y_test, pred, labels=[0, 1]).tolist(),
        }
    (OUT / "ml_baseline_metrics.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    cm = results["models"]["regression_logistique"]["confusion_matrix"]
    pd.DataFrame(cm, index=["réel_No", "réel_Yes"], columns=["prédit_No", "prédit_Yes"]).to_csv(OUT / "ml_confusion_matrix.csv")
    print("Évaluation terminée sur un jeu de test réservé.")
    for name, metrics in results["models"].items():
        print(f"{name}: accuracy={metrics['accuracy']}, precision={metrics['precision']}, recall={metrics['recall']}, F1={metrics['f1']}")
    print("Résultats : outputs/ml_baseline_metrics.json et outputs/ml_confusion_matrix.csv")
    print("Attention : un score élevé ne garantit pas une performance sur de futurs clients.")

if __name__ == "__main__":
    main()
