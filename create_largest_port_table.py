import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv, dotenv_values

# Load environment variables from the .env file
load_dotenv()

# PostgreSQL database connection parameters
def get_database_conn():
    # Get database credentials from environment variable
    config = dict(dotenv_values('.env'))
    db_user_name = config.get('DB_USER_NAME')
    db_password = config.get('DB_PASSWORD')
    db_name = config.get('DB_NAME')
    port = config.get('PORT')
    host = config.get('HOST')
    
    # Create and return a PostgreSQL database connection object
    conn_str = f'postgresql+psycopg2://{db_user_name}:{db_password}@{host}:{port}/{db_name}'
    engine = create_engine(conn_str)
    return engine

# Get the PostgreSQL engine
engine = get_database_conn()
print('PostgreSQL database connected successfully')

# query to create a table in PostgreSQL
query = text('''
    CREATE TABLE IF NOT EXISTS largest_port_by_country (
        country TEXT,
        port_count INTEGER
    )
''')

insert_query = text('''
INSERT INTO largest_port_by_country (country, port_count)
SELECT
    cc.country_name AS country,
    COUNT(*) AS port_count
FROM
    country_codes cc
JOIN
    wpi_data wd ON cc.country_code = wd.wpi_country_code
WHERE
    wd.load_offload_wharves = 'Y'
GROUP BY
    cc.country_name
ORDER BY
    port_count DESC
LIMIT 20;
''')

# Execute the query to create the table
with engine.connect() as connection:
    connection.execute(query)
    connection.commit()

# Execute the query to insert data into the table
with engine.connect() as connection:
    connection.execute(insert_query)
    connection.commit()

print('Table created and data inserted successfully')
