import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
    RocCurveDisplay,
)

from src.config import (
    FEATURE_IMPORTANCE_PATH,
    FEATURE_IMPORTANCE_PLOT_PATH,
    ROC_CURVE_PATH,
    DISPLAY_NAME_MAP,
)


def clean_feature_name(feature_name):
    name = feature_name.replace("num__", "").replace("cat__", "")

    if "_" in name:
        parts = name.split("_")
        base = "_".join(parts[:-1])
        suffix = parts[-1]

        if base in DISPLAY_NAME_MAP:
            return f"{DISPLAY_NAME_MAP[base]} = {suffix}"

    return DISPLAY_NAME_MAP.get(name, name.replace("_", " ").title())


def evaluate_model(name, pipeline, X_test, y_test):
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="weighted", zero_division=0)
    recall = recall_score(y_test, y_pred, average="weighted", zero_division=0)
    f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)
    roc_auc = roc_auc_score(y_test, y_proba)

    print("\n==============================")
    print(name)
    print("==============================")
    print("Accuracy:", round(acc, 4))
    print("Precision:", round(precision, 4))
    print("Recall:", round(recall, 4))
    print("F1 Score:", round(f1, 4))
    print("ROC-AUC:", round(roc_auc, 4))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    return {
    "accuracy": round(acc, 4),
    "precision": round(precision, 4),
    "recall": round(recall, 4),
    "f1_score": round(f1, 4),
    "roc_auc": round(roc_auc, 4),
    }


def save_roc_curve(pipeline, X_test, y_test):
    RocCurveDisplay.from_estimator(pipeline, X_test, y_test)
    plt.title("ROC Curve - Loan Approval Model")
    plt.savefig(ROC_CURVE_PATH, bbox_inches="tight")
    plt.close()
    print("Saved ROC curve to:", ROC_CURVE_PATH)


def save_feature_importance(pipeline):
    fitted_preprocessor = pipeline.named_steps["preprocessor"]
    fitted_model = pipeline.named_steps["model"]

    if not hasattr(fitted_model, "feature_importances_"):
        return

    raw_feature_names = fitted_preprocessor.get_feature_names_out()
    clean_names = [clean_feature_name(name) for name in raw_feature_names]

    importance_df = pd.DataFrame(
        {
            "feature": clean_names,
            "importance": fitted_model.feature_importances_,
        }
    ).sort_values(by="importance", ascending=False)

    importance_df.to_csv(FEATURE_IMPORTANCE_PATH, index=False)

    print("\nTop 10 important features:")
    print(importance_df.head(10))
    print("\nSaved feature importance to:", FEATURE_IMPORTANCE_PATH)

    top_features = importance_df.head(10).sort_values(by="importance")

    plt.figure(figsize=(10, 6))
    plt.barh(top_features["feature"], top_features["importance"])
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.title("Top 10 Feature Importances")
    plt.savefig(FEATURE_IMPORTANCE_PLOT_PATH, bbox_inches="tight")
    plt.close()

    print("Saved feature importance plot to:", FEATURE_IMPORTANCE_PLOT_PATH)