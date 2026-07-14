import os
import joblib
import json
from datetime import datetime

from sklearn.model_selection import train_test_split

from src.config import MODEL_PATH
from src.preprocessing import load_data, split_features_target, build_preprocessor
from src.training import train_baseline_models, tune_gradient_boosting
from src.evaluation import evaluate_model, save_roc_curve, save_feature_importance


def main():
    df = load_data()

    X, y = split_features_target(df)
    preprocessor = build_preprocessor(X)

    X_train, X_temp, y_train, y_temp = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    X_val, X_test, y_val, y_test = train_test_split(
        X_temp,
        y_temp,
        test_size=0.5,
        random_state=42,
        stratify=y_temp,
    )

    print("Train size:", X_train.shape[0])
    print("Validation size:", X_val.shape[0])
    print("Test size:", X_test.shape[0])

    print("\nTraining baseline models...")

    best_model, best_score, best_name = train_baseline_models(
        preprocessor,
        X,
        y,
        X_train,
        X_val,
        y_train,
        y_val,
    )

    tuned_model, tuned_f1, _ = tune_gradient_boosting(
        preprocessor,
        X_train,
        y_train,
        X_val,
        y_val,
    )

    best_model = tuned_model
    best_name = "Tuned Gradient Boosting" 
    #because in all the tests and varations tuned proved to be providing better results

    print("\nBest final model:", best_name)

    print("\nFinal evaluation on held-out test set:")
    final_metrics = evaluate_model(best_name, best_model, X_test, y_test)

    os.makedirs("models", exist_ok=True)
    joblib.dump(best_model, MODEL_PATH)

    metadata = {
    "model_name": best_name,
    "training_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "train_split": "80%",
    "validation_split": "10%",
    "test_split": "10%",
    "metrics": final_metrics,
    }

    with open("models/model_metadata.json", "w") as file:
        json.dump(metadata, file, indent=4)

    print("Saved final model to:", MODEL_PATH)

    save_roc_curve(best_model, X_test, y_test)
    save_feature_importance(best_model)


if __name__ == "__main__":
    main()