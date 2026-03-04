#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
import click

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='green_taxi', help='PostgreSQL database name')
@click.option('--year', default='2025', type=int, help='Year of the data')
@click.option('--month', default='11', type=int, help='Month of the data')

def run(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month):

    tripfile=f"green_tripdata_{year}-{month:02d}.parquet"
    df=pd.read_parquet(tripfile)
    df_zone=pd.read_csv("taxi_zone_lookup.csv")
    
    #create database connection    
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    df.to_sql(name='green_taxi_data', con=engine, if_exists='replace')
    df_zone.to_sql(name='zones',con=engine, if_exists='replace')

if __name__=='__main__':
    run()