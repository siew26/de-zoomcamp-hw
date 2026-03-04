# DE Zoomcamp Homework - Week 3

## Create a dataset
### 1. Create external table
```sql
CREATE OR REPLACE EXTERNAL TABLE `de-kestra-gcp-workflow.taxi_data.yellow_tripdata_ext`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://yellow-taxi-data-sy/*.parquet'])
```

### 2. Create table from external table
```sql
CREATE TABLE `de-kestra-gcp-workflow.taxi_data.yellow_taxi_data` AS
SELECT *
FROM `de-kestra-gcp-workflow.taxi_data.yellow_tripdata_ext`
```

### Questions:
### Q1: count records
```sql
SELECT count(*)  FROM `de-kestra-gcp-workflow.taxi_data.yellow_taxi_data`
```

### Q2: count the distinct number of PULocationIDs for the entire dataset on both the tables
```sql
select count(distinct PULocationID) from `de-kestra-gcp-workflow.taxi_data.yellow_taxi_data`
;
select count(distinct PULocationID) from `de-kestra-gcp-workflow.taxi_data.yellow_tripdata_ext`
```

### Q4: records have a fare_amount of 0
```sql
select count(*) from `de-kestra-gcp-workflow.taxi_data.yellow_taxi_data`
where fare_amount=0
```

### Q5: Create a partitioned clustered table from external table
```sql
CREATE OR REPLACE TABLE `de-kestra-gcp-workflow.taxi_data.yellow_taxi_data_partitioned_clustered`
PARTITION BY
  DATE(tpep_dropoff_datetime) 
CLUSTER BY VendorID  
  AS
SELECT * FROM `de-kestra-gcp-workflow.taxi_data.yellow_taxi_data`
```

### Q6: distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15
```sql
select distinct VendorID from `de-kestra-gcp-workflow.taxi_data.yellow_taxi_data`
where date(tpep_dropoff_datetime) between date('2024-03-01') and date('2024-03-15')

;
select distinct VendorID from `de-kestra-gcp-workflow.taxi_data.yellow_taxi_data_partitioned_clustered`
where date(tpep_dropoff_datetime) between date('2024-03-01') and date('2024-03-15')
```

