import dlt
from dlt.sources.rest_api import rest_api_source


def run() -> None:
    """Run the NYC taxi REST API pipeline."""
    pipeline = dlt.pipeline(
        pipeline_name="taxi_pipeline",
        destination="duckdb",
        dataset_name="nyc_taxi_data",
    )

    nyc_taxi_source = rest_api_source(
        {
            "client": {
                "base_url": "https://us-central1-dlthub-analytics.cloudfunctions.net/",
                "paginator": {
                    "type": "page_number",
                    "base_page": 1,
                    "page_param": "page",
                    # rely on default stop_after_empty_page=True to stop on empty page
                    "total_path": None,
                },
            },
            "resources": [
                {
                    "name": "nyc_taxi_trips",
                    "endpoint": {
                        "path": "data_engineering_zoomcamp_api",
                    },
                }
            ],
        }
    )

    load_info = pipeline.run(nyc_taxi_source)
    print(load_info)


if __name__ == "__main__":
    run()

