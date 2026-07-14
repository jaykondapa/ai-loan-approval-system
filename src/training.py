from sklearn.model_selection import cross_val_score, RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from src.evaluation import evaluate_model


def train_baseline_models(preprocessor, X, y, X_train, X_test, y_train, y_test):
    baseline_models = {
        "Random Forest": RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            class_weight="balanced",
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            random_state=42,
        ),
    }

    best_model = None
    best_score = 0
    best_name = ""

    for name, model in baseline_models.items():
        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", model),
            ]
        )

        cv_scores = cross_val_score(
            pipeline,
            X,
            y,
            cv=5,
            scoring="f1_weighted",
        ).round(4)

        print("\n==============================")
        print(name, "Cross Validation")
        print("==============================")
        print("Cross-validation F1 scores:", cv_scores.tolist())
        print("Mean CV F1:", round(cv_scores.mean(), 4))
        print("Std Dev:", round(cv_scores.std(), 4))

        pipeline.fit(X_train, y_train)

        metrics = evaluate_model(name, pipeline, X_test, y_test)
        f1 = metrics["f1_score"]

        if f1 > best_score:
            best_model = pipeline
            best_score = f1
            best_name = name

    return best_model, best_score, best_name


def tune_gradient_boosting(preprocessor, X_train, y_train, X_test, y_test):
    print("\nRunning hyperparameter tuning for Gradient Boosting...")

    gb_pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", GradientBoostingClassifier(random_state=42)),
        ]
    )

    param_grid = {
        "model__n_estimators": [50, 100, 150, 200],
        "model__learning_rate": [0.01, 0.05, 0.1, 0.2],
        "model__max_depth": [2, 3, 4, 5],
        "model__min_samples_split": [2, 5, 10],
        "model__min_samples_leaf": [1, 2, 4],
    }

    search = RandomizedSearchCV(
        gb_pipeline,
        param_distributions=param_grid,
        n_iter=20,
        scoring="f1_weighted",
        cv=5,
        random_state=42,
        n_jobs=-1,
    )

    search.fit(X_train, y_train)

    tuned_model = search.best_estimator_

    print("\nBest tuned parameters:")
    print(search.best_params_)

    metrics = evaluate_model(
    "Tuned Gradient Boosting",
    tuned_model,
    X_test,
    y_test,
    )

    tuned_f1 = metrics["f1_score"]
    tuned_roc_auc = metrics["roc_auc"]

    return tuned_model, tuned_f1, tuned_roc_auc