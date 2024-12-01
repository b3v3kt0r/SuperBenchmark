import json
import os
from datetime import datetime
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException

from app.models import AverageResults
from app.utils import calculate_average, filter_results


load_dotenv()

app = FastAPI()

DEBUG_MODE = os.getenv("SUPERBENCHMARK_DEBUG")

if DEBUG_MODE:
    with open("app/test_database.json", "r") as file:
        DATABASE = json.load(file)
else:
    raise HTTPException(status_code=503, detail="The feature is not ready for live yet")


@app.get("/results/average", response_model=AverageResults)
def get_average():
    res = DATABASE["benchmarking_results"]
    return calculate_average(res)


@app.get("/results/average/{start_time}/{end_time}", response_model=AverageResults)
def get_average_in_time_window(start_time: str, end_time: str):
    start_datetime = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
    end_datetime = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S")

    results = filter_results(DATABASE["benchmarking_results"], start_datetime, end_datetime)

    return calculate_average(results)
