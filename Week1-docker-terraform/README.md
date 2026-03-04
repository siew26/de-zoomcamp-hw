# DE Zoomcamp Homework

## Question 1. Understanding Docker images
1. Run a Python container with bash as entrypoint to interact with it:

    ```docker run -it --entrypoint=bash python:3.13.11-slim```

2. Check pip version

    ```pip -V```

## Prepare the Data (Q3-Q6)
### Virtual Environment Setup
1. Install tools that can manage virtual env

    ```pip install uv```

2. Init virtual env with Python 3.13

    ```uv init --python 3.13```

3. Check Python version in virtual env

    ```uv run python -V```

    ```uv run which python```
    
### Jupyter Notebook Setup
1. Download the files
2. Install dependencies to work with data and .parquet files

    ```uv pip install pandas pyarrow```
        
3. Add Jupyter to vm:

   ```uv add --dev jupyter```

4. Launch jupyter notebook

   ```uv run jupyter notebook```

5. Open the link from terminal and create a new notebook (Green_taxi_notebook.ipynb)

6. After completing the notebook, convert notebook to script

    ```uv run jupyter nbconvert --to=script Green_taxi_notebook.ipynb```
    
7. Use the script Green_taxi_ingest.py to ingest data into Postgres:

     ```
     uv run python Green_taxi_ingest.py \
            --pg-user=root \                  
            --pg-pass=root \                         
            --pg-host=localhost \                    
            --pg-port=5432 \                          
            --pg-db=green_taxi \                     
            --year=2025 \                      
            --month=11 
    ```

### Docker Setup for Postgres & pgadmin
1. Create Docker network to allow containers to communicate:

    ```docker network create pg_network```

    ```docker network ls```

2. Run Postgres container in network:

    ```
    docker run -it --rm \
        -e POSTGRES_USER="root" \
        -e POSTGRES_PASSWORD="root" \
        -e POSTGRES_DB="green_taxi" \
        -v green_taxi_postgres_data:/var/lib/postgresql \
        -p 5432:5432 \
        --network=pg_network \
        --name=pgdatabase \
        postgres:18
    ```
    
3. Run pgadmin in same network
    ```
    docker run -it \
        -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
        -e PGADMIN_DEFAULT_PASSWORD="root" \
        -v pgadmin_data:/var/lib/pgadmin \
        -p 8085:80 \
        --network=pg_network \
        --name pgadmin \
        dpage/pgadmin4
    ```

    
## Question 3. Counting short trips
```
select count(*) from public.green_taxi_data
where cast(lpep_pickup_datetime as date) >='2025-11-01'
and cast(lpep_pickup_datetime as date) <'2025-12-01'
and trip_distance<=1
```


## Question 4. Longest trip for each day
```
select cast(lpep_pickup_datetime as date) as pu_date, max(trip_distance) from public.green_taxi_data
where trip_distance<100
group by 1
order by 2 desc
```

## Question 5. Biggest pickup zone
```
select
"Zone",
rank() over (order by sum(total_amount) desc) as rn 
from public.green_taxi_data a 
left join public.zones b on a."PULocationID"=b."LocationID"
group by 1
```

## Question 6. Largest tip
```
select
"Zone",
rank() over (order by sum(tip_amount) desc) as rn 
from public.green_taxi_data a 
left join public.zones b on a."DOLocationID"=b."LocationID"
where cast(lpep_pickup_datetime as date) >='2025-11-01'
and cast(lpep_pickup_datetime as date) <'2025-12-01'
group by 1
```
