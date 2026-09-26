from io import BytesIO

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile

from app.processor import analyze_csv, clean_csv, validate_csv

app = FastAPI(
    title="DataForge CSV Processing Service",
    description="Automated CSV validation, cleaning and analysis service",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "service": "DataForge CSV Processing Service",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/process")
async def process_csv(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    try:
        contents = await file.read()
        df = pd.read_csv(BytesIO(contents))
    except Exception as exc:
        raise HTTPException(
            status_code=400, detail=f"Unable to read CSV file: {str(exc)}"
        ) from exc

    is_valid, validation_message = validate_csv(df)

    if not is_valid:
        raise HTTPException(status_code=400, detail=validation_message)

    original_rows = len(df)
    cleaned_df = clean_csv(df)
    cleaned_rows = len(cleaned_df)
    analysis = analyze_csv(cleaned_df)

    return {
        "status": "success",
        "filename": file.filename,
        "validation": validation_message,
        "processing": {
            "original_rows": original_rows,
            "cleaned_rows": cleaned_rows,
            "rows_removed": original_rows - cleaned_rows,
        },
        "analysis": analysis,
    }
