import pyodbc
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv, dotenv_values

# Load environment variables from the .env file
load_dotenv()

# Access database connection parameters
access_conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\dell\Downloads\PUB150\WPI.mdb;'
access_conn = pyodbc.connect(access_conn_str)
access_cursor = access_conn.cursor()

try:
    # Try to establish a connection
    access_conn = pyodbc.connect(access_conn_str)
    print("Access database connection successful!")

except pyodbc.Error as e:
    # Handle any errors that occur during the connection attempt
    print(f"Error connecting to the Access database: {e}")

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
print('PostgreSQL database connected successfully')

# Function to migrate data from Access to PostgreSQL
def migrate_table(access_conn, pg_engine, table_name):
    # Extract data from Access database
    query = f"SELECT * FROM [{table_name}]"
    access_data = pd.read_sql(query, access_conn)

    access_data.columns = access_data.columns.str.replace(" ", "_").str.lower()
    print('Columns extracted successfully')
    
    # Define the PostgreSQL table name
    pg_table_name = table_name.replace(" ", "_").replace("/", "_").lower()
    
    # Copy data from Access to PostgreSQL
    access_data.to_sql(pg_table_name, con=pg_engine, index=False, if_exists='replace')
    print(f'Data copied from Access table {table_name} to PostgreSQL table {pg_table_name} successfully')

# List of table names to migrate
table_names = ["Country Codes", "Country Codes Old", "Depth Code LUT", "Drydock/Marine Railway Code LUT", "Harbor Size LUT", "Harbor Type LUT", "Maximum Size Vessel LUT", "Repairs Code LUT", "Shelter Afforded LUT", 
               "Wpi Data", "WPI Import", "WPI Region"]

# Get PostgreSQL engine
pg_engine = get_database_conn()

# Migrate each table
for table_name in table_names:
    migrate_table(access_conn, pg_engine, table_name)

# Close Access connection
access_conn.close()
