from datetime import datetime
from typing import List

from app.models import AverageResults


def calculate_average(results: List[dict]) -> AverageResults:
    total_token = sum(result["token_count"] for result in results)
    total_time_to_first_token = sum(result["time_to_first_token"] for result in results)
    total_time_per_output_token = sum(result["time_per_output_token"] for result in results)
    total_generation_time = sum(result["total_generation_time"] for result in results)

    count = len(results)
    return AverageResults(
        average_token_count=round(total_token / count, 2),
        average_time_to_first_token=round(total_time_to_first_token / count, 2),
        average_time_per_output_token=round(total_time_per_output_token / count, 2),
        average_total_generation_time=round(total_generation_time / count, 2),
    )


def filter_results(results: List[dict], start_time: datetime, end_time: datetime) -> List[dict]:
    return [
        result
        for result in results
        if start_time <= datetime.strptime(result["timestamp"], "%Y-%m-%dT%H:%M:%S") <= end_time
    ]
