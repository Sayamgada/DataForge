# DataForge

## Automated CI/CD Pipeline for a Containerized CSV Data Processing Service

DataForge is a FastAPI-based CSV data processing service that validates, cleans, and analyzes uploaded CSV files. The application is containerized using Docker and integrated with a GitHub Actions CI/CD pipeline that automatically tests the application, builds and tests the Docker image, publishes it to Docker Hub, and deploys the latest version to Render.

## Project Objective

The objective of this project is to demonstrate an automated CI/CD pipeline for a containerized application.

The pipeline automatically performs:

- Code linting using Flake8
- Automated testing using Pytest
- Docker image building
- Docker container testing
- Docker Hub image publishing
- Automatic deployment to Render

The CSV processing functionality provides the actual application that is continuously tested, built, and deployed through the pipeline.

## Application Features

DataForge provides a REST API for CSV processing.

The service can:

- Validate required CSV columns
- Normalize column names
- Convert numeric fields
- Clean invalid records
- Remove duplicate records
- Calculate numerical statistics
- Generate department-wise record distribution
- Return processing results as JSON

## Technology Stack

| Technology     | Purpose                      |
| -------------- | ---------------------------- |
| Python 3.12    | Application runtime          |
| FastAPI        | REST API framework           |
| Pandas         | CSV processing and analysis  |
| Pytest         | Automated testing            |
| Flake8         | Code quality and linting     |
| Docker         | Application containerization |
| Docker Hub     | Container image registry     |
| GitHub Actions | CI/CD automation             |
| Render         | Cloud deployment             |

## Project Structure

```text
DataForge/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── processor.py
├── sample_data/
│   └── input.csv
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_processor.py
├── .dockerignore
├── .flake8
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## API Endpoints

### GET `/`

Returns basic information about the DataForge service.

Example response:

```json
{
  "service": "DataForge CSV Processing Service",
  "status": "running",
  "version": "1.0.0"
}
```

### GET `/health`

Used as a health check to verify that the application is running correctly.

Example response:

```json
{
  "status": "healthy"
}
```

### POST `/process`

Accepts a CSV file, validates and processes it, and returns the analysis results.

The CSV file must contain the following columns:

```text
id
name
age
salary
department
```

## CSV Processing Flow

The application processes the uploaded CSV through the following stages:

```text
CSV Upload
    ↓
CSV Validation
    ↓
Data Cleaning
    ↓
Remove Invalid Records
    ↓
Remove Duplicate Records
    ↓
Data Analysis
    ↓
JSON Response
```

### Data Cleaning

The application performs the following operations:

1. Normalizes column names.
2. Converts `age` and `salary` to numeric values.
3. Removes records with invalid required fields.
4. Removes records with invalid age values.
5. Trims whitespace from names.
6. Converts department names to uppercase.
7. Removes duplicate records.

### Data Analysis

The service calculates:

- Total number of records
- Missing values
- Mean, minimum, and maximum values for numeric columns
- Department distribution

## Sample Input

The project includes `sample_data/input.csv`:

```csv
id,name,age,salary,department
1,John,25,50000,IT
2,Alice,27,60000,HR
3,Bob,,55000,IT
4,John,25,50000,IT
5,David,31,70000,Finance
6,Emma,abc,65000,HR
```

After processing:

```text
Original records: 6
Cleaned records: 3
Records removed: 3
```

The remaining valid records are:

```text
John
Alice
David
```

## Running Locally

### 1. Clone the Repository

```bash
git clone https://github.com/Sayamgada/DataForge.git
cd DataForge
```

### 2. Create a Virtual Environment

On Windows:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the Application

```bash
uvicorn app.main:app --reload
```

The application will be available at:

```text
http://localhost:8000
```

Swagger API documentation:

```text
http://localhost:8000/docs
```

Health check:

```text
http://localhost:8000/health
```

## Running with Docker

Build the Docker image:

```bash
docker build -t dataforge .
```

Run the container:

```bash
docker run -d --name dataforge-service -p 8000:8000 dataforge
```

Check the application:

```text
http://localhost:8000/health
```

## Running with Docker Compose

Start the service:

```bash
docker compose up --build
```

The application will be available at:

```text
http://localhost:8000
```

Stop the service:

```bash
docker compose down
```

## Testing

### Run Flake8

```bash
flake8 app tests
```

### Run Pytest

```bash
pytest
```

The project currently contains 15 automated tests covering the CSV processing functionality and API endpoints.

## CI/CD Pipeline

The project uses GitHub Actions to automate the software delivery process.

The pipeline is triggered when code is pushed to the `main` branch or when a pull request targets `main`.

### Pipeline Flow

```text
Developer
    ↓
git push
    ↓
GitHub
    ↓
GitHub Actions
    ↓
Flake8
    ↓
Pytest
    ↓
Docker Build
    ↓
Docker Container Test
    ↓
Docker Hub
    ↓
Render Deploy Hook
    ↓
Render
    ↓
Updated DataForge Application
```

## Continuous Integration

The CI stage performs:

### 1. Checkout

The latest source code is retrieved from the GitHub repository.

### 2. Python Setup

GitHub Actions configures Python 3.12.

### 3. Dependency Installation

The dependencies from `requirements.txt` are installed.

### 4. Code Quality Check

Flake8 checks the application and test code fo
