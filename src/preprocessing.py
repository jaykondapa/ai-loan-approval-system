import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

from src.config import DATA_PATH, COLUMN_RENAME_MAP, TARGET_COLUMN


def load_data():
    df = pd.read_csv(DATA_PATH)
    df.rename(columns=COLUMN_RENAME_MAP, inplace=True)
    return df


def split_features_target(df):
    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]
    return X, y


def build_preprocessor(X):
    categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()
    numeric_cols = X.select_dtypes(exclude=["object"]).columns.tolist()

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
            ("num", "passthrough", numeric_cols),
        ]
    )

    return preprocessor