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

- Validate that CSV headers are present and unique
- Normalize column names
- Detect numeric fields
- Clean invalid records
- Remove duplicate records
- Calculate numerical statistics
- Generate distribution for a `department` column when present
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

The service accepts CSV files with any non-empty, unique set of column names. Column names are trimmed and converted to lowercase before processing.

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

1. Normalizes column names and trims whitespace from text values.
2. Detects columns containing numeric values so they can be included in numeric analysis.
3. Removes entirely empty records and duplicate records.
4. When present, converts `age` and `salary` to numeric values and removes records where those values are invalid.
5. When present, trims `name` values and converts `department` values to uppercase.

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

The pipeline runs on pushes to `main` (including revert commits and force-pushes that move `main` to an earlier commit), pull requests targeting `main`, and manual workflow dispatches. A push that moves `main` to an earlier commit is built and deployed like any other update. To run it manually, open **Actions**, select **DataForge CI**, and choose **Run workflow**. Manual runs on `main` also publish the image and deploy; runs on other refs only test and build the image.

### Pipeline Flow

```text
Developer
    ↓
push / rollback / manual run
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
