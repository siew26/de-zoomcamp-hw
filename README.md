## NYC Taxi REST API pipeline

This project defines a dlt pipeline that loads NYC taxi trip data from the Zoomcamp REST API into a local DuckDB database using the `rest_api` verified source.

### Usage

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the pipeline:

```bash
python taxi_pipeline.py
```

