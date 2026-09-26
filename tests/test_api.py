from io import BytesIO

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["service"] == ("DataForge CSV Processing Service")
    assert data["status"] == "running"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_process_valid_csv():
    csv_content = (
        "id,name,age,salary,department\n"
        "1,John,25,50000,IT\n"
        "2,Alice,27,60000,HR\n"
        "3,David,31,70000,Finance\n"
    )

    response = client.post(
        "/process",
        files={"file": ("input.csv", BytesIO(csv_content.encode()), "text/csv")},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["processing"]["original_rows"] == 3
    assert data["processing"]["cleaned_rows"] == 3
    assert data["processing"]["rows_removed"] == 0


def test_process_csv_with_duplicates():
    csv_content = (
        "id,name,age,salary,department\n"
        "1,John,25,50000,IT\n"
        "2,John,25,50000,IT\n"
        "3,Alice,27,60000,HR\n"
    )

    response = client.post(
        "/process",
        files={"file": ("input.csv", BytesIO(csv_content.encode()), "text/csv")},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["processing"]["original_rows"] == 3
    assert data["processing"]["cleaned_rows"] == 2
    assert data["processing"]["rows_removed"] == 1


def test_process_csv_with_invalid_age():
    csv_content = (
        "id,name,age,salary,department\n"
        "1,John,25,50000,IT\n"
        "2,Alice,invalid,60000,HR\n"
    )

    response = client.post(
        "/process",
        files={"file": ("input.csv", BytesIO(csv_content.encode()), "text/csv")},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["processing"]["original_rows"] == 2
    assert data["processing"]["cleaned_rows"] == 1
    assert data["processing"]["rows_removed"] == 1


def test_process_non_csv_file():
    response = client.post(
        "/process", files={"file": ("input.txt", BytesIO(b"test data"), "text/plain")}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == ("Only CSV files are supported")


def test_process_csv_with_missing_columns():
    csv_content = "id,name,age\n" "1,John,25\n"

    response = client.post(
        "/process",
        files={"file": ("input.csv", BytesIO(csv_content.encode()), "text/csv")},
    )

    assert response.status_code == 400
    assert "Missing required columns" in (response.json()["detail"])
