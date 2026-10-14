import pandas as pd


def validate_csv(df):
    normalized_columns = [str(column).strip().lower() for column in df.columns]

    if not normalized_columns:
        return False, "CSV must contain at least one column"

    if any(not column for column in normalized_columns):
        return False, "CSV contains an empty column name"

    seen_columns = set()
    duplicate_columns = set()
    for column in normalized_columns:
        if column in seen_columns:
            duplicate_columns.add(column)
        seen_columns.add(column)

    if duplicate_columns:
        duplicates = ", ".join(sorted(duplicate_columns))
        return False, f"CSV contains duplicate columns: {duplicates}"

    return True, "CSV validation successful"


def clean_csv(df):
    cleaned_df = df.copy()

    cleaned_df.columns = [str(column).strip().lower() for column in cleaned_df.columns]

    for column in cleaned_df.columns:
        cleaned_df[column] = cleaned_df[column].map(
            lambda value: value.strip() if isinstance(value, str) else value
        )
        cleaned_df[column] = cleaned_df[column].replace("", pd.NA)

        if column not in {"age", "salary"}:
            non_missing_values = cleaned_df[column].dropna()
            if not non_missing_values.empty:
                numeric_values = pd.to_numeric(non_missing_values, errors="coerce")
                if numeric_values.notna().all():
                    cleaned_df[column] = pd.to_numeric(
                        cleaned_df[column], errors="coerce"
                    )

    cleaned_df = cleaned_df.dropna(how="all")

    if "age" in cleaned_df.columns:
        cleaned_df["age"] = pd.to_numeric(cleaned_df["age"], errors="coerce")
        cleaned_df = cleaned_df[cleaned_df["age"].notna()]

    if "salary" in cleaned_df.columns:
        cleaned_df["salary"] = pd.to_numeric(cleaned_df["salary"], errors="coerce")

    if "department" in cleaned_df.columns:
        cleaned_df["department"] = cleaned_df["department"].map(
            lambda value: value.upper() if isinstance(value, str) else value
        )

    required_if_present = [
        column
        for column in ["id", "name", "salary", "department"]
        if column in cleaned_df.columns
    ]
    if required_if_present:
        cleaned_df = cleaned_df.dropna(subset=required_if_present)

    duplicate_subset = ["name", "age", "salary", "department"]
    if not set(duplicate_subset).issubset(cleaned_df.columns):
        duplicate_subset = list(cleaned_df.columns)
    cleaned_df = cleaned_df.drop_duplicates(subset=duplicate_subset)

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
