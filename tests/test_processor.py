import pandas as pd

from app.processor import analyze_csv, clean_csv, validate_csv


def create_sample_dataframe():
    return pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5, 6],
            "name": ["John", "Alice", "Bob", "John", "David", "Emma"],
            "age": [25, 27, None, 25, 31, "abc"],
            "salary": [50000, 60000, 55000, 50000, 70000, 65000],
            "department": ["IT", "HR", "IT", "IT", "Finance", "HR"],
        }
    )


def test_validate_valid_csv():
    df = create_sample_dataframe()

    is_valid, message = validate_csv(df)

    assert is_valid is True
    assert message == "CSV validation successful"


def test_validate_arbitrary_columns():
    df = pd.DataFrame({"product": ["Book"], "quantity": [2]})

    is_valid, message = validate_csv(df)

    assert is_valid is True
    assert message == "CSV validation successful"


def test_validate_duplicate_normalized_columns():
    df = pd.DataFrame([["Book", "Novel"]], columns=[" Product ", "product"])

    is_valid, message = validate_csv(df)

    assert is_valid is False
    assert message == "CSV contains duplicate columns: product"


def test_clean_csv_removes_invalid_and_duplicate_records():
    df = create_sample_dataframe()

    cleaned_df = clean_csv(df)

    assert len(cleaned_df) == 3


def test_clean_csv_normalizes_departments():
    df = create_sample_dataframe()

    cleaned_df = clean_csv(df)

    assert set(cleaned_df["department"]) == {"IT", "HR", "FINANCE"}


def test_clean_csv_removes_invalid_age_values():
    df = create_sample_dataframe()

    cleaned_df = clean_csv(df)

    assert cleaned_df["age"].notna().all()
    assert pd.api.types.is_numeric_dtype(cleaned_df["age"])


def test_clean_csv_handles_arbitrary_columns():
    df = pd.DataFrame(
        {
            " Product ": ["  BOOK-1 ", "BOOK-2", "BOOK-2", None],
            "Quantity": ["2", "4", "4", None],
            "Description": [" hardcover ", " paperback ", " paperback ", None],
        }
    )

    cleaned_df = clean_csv(df)

    assert list(cleaned_df.columns) == ["product", "quantity", "description"]
    assert cleaned_df.to_dict("records") == [
        {
            "product": "BOOK-1",
            "quantity": 2,
            "description": "hardcover",
        },
        {
            "product": "BOOK-2",
            "quantity": 4,
            "description": "paperback",
        },
    ]


def test_clean_csv_handles_numeric_department_values():
    df = pd.DataFrame({"department": [101, 102]})

    cleaned_df = clean_csv(df)

    assert cleaned_df["department"].tolist() == [101, 102]


def test_analyze_csv_record_count():
    df = create_sample_dataframe()
    cleaned_df = clean_csv(df)

    analysis = analyze_csv(cleaned_df)

    assert analysis["total_records"] == 3


def test_analyze_csv_numeric_statistics():
    df = create_sample_dataframe()
    cleaned_df = clean_csv(df)

    analysis = analyze_csv(cleaned_df)

    assert analysis["numeric_statistics"]["age"]["mean"] == 27.67

    assert analysis["numeric_statistics"]["salary"]["mean"] == 60000.0


def test_analyze_csv_department_distribution():
    df = create_sample_dataframe()
    cleaned_df = clean_csv(df)

    analysis = analyze_csv(cleaned_df)

    assert analysis["department_distribution"] == {"IT": 1, "HR": 1, "FINANCE": 1}
