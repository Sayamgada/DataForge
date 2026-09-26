import pandas as pd

REQUIRED_COLUMNS = ["id", "name", "age", "salary", "department"]


def validate_csv(df):
    normalized_columns = [column.strip().lower() for column in df.columns]

    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in normalized_columns
    ]

    if missing_columns:
        return (False, "Missing required columns: " f"{', '.join(missing_columns)}")

    return True, "CSV validation successful"


def clean_csv(df):
    cleaned_df = df.copy()

    cleaned_df.columns = [column.strip().lower() for column in cleaned_df.columns]

    cleaned_df["age"] = pd.to_numeric(cleaned_df["age"], errors="coerce")

    cleaned_df["salary"] = pd.to_numeric(cleaned_df["salary"], errors="coerce")

    cleaned_df["name"] = cleaned_df["name"].astype(str).str.strip()

    cleaned_df["department"] = (
        cleaned_df["department"].astype(str).str.strip().str.upper()
    )

    cleaned_df = cleaned_df.dropna(subset=["id", "name", "salary", "department"])

    cleaned_df = cleaned_df[cleaned_df["age"].notna()]

    cleaned_df = cleaned_df.drop_duplicates(
        subset=["name", "age", "salary", "department"]
    )

    return cleaned_df


def analyze_csv(df):
    analysis = {
        "total_records": int(len(df)),
        "columns": list(df.columns),
        "missing_values": {
            column: int(value) for column, value in df.isnull().sum().items()
        },
    }

    numeric_columns = df.select_dtypes(include="number").columns

    statistics = {}

    for column in numeric_columns:
        statistics[column] = {
            "mean": round(float(df[column].mean()), 2),
            "minimum": round(float(df[column].min()), 2),
            "maximum": round(float(df[column].max()), 2),
        }

    analysis["numeric_statistics"] = statistics

    if "department" in df.columns:
        analysis["department_distribution"] = {
            str(key): int(value)
            for key, value in df["department"].value_counts().items()
        }

    return analysis
