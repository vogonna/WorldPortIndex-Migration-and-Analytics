import psycopg2
from dotenv import dotenv_values
from sqlalchemy import create_engine, text

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

# Coordinates of the distress call
distress_lat = 32.610982
distress_long = -38.706256

# Query to create a table in PostgreSQL
create_table_query = text('''
    CREATE TABLE IF NOT EXISTS nearest_port (
        country_name TEXT,
        main_port_name TEXT,
        latitude_degrees FLOAT,
        longitude_degrees FLOAT
    )
''')

# Define the SQL query for insertion
insert_query = text('''
    INSERT INTO nearest_port (country_name, main_port_name, latitude_degrees, longitude_degrees)
    SELECT
        cc.country_name,
        wd.main_port_name,
        wd.latitude_degrees,
        wd.longitude_degrees
    FROM
        wpi_data wd
    JOIN
        country_codes cc ON wd.wpi_country_code = cc.country_code
    WHERE
        wd.supplies_provisions = 'Y'
        AND wd.supplies_water = 'Y'
        AND wd.supplies_fuel_oil = 'Y'
        AND wd.supplies_diesel_oil = 'Y'
    ORDER BY
        (
            6371 * 
            acos(
                cos(radians(:lat)) * cos(radians(wd.latitude_degrees)) * cos(radians(wd.longitude_degrees) - radians(:long)) +
                sin(radians(:lat)) * sin(radians(wd.latitude_degrees))
            )
        ) ASC;
''')

# Execute the query to create the table
with engine.connect() as connection:
    connection.execute(create_table_query)
    connection.commit()

# Execute the query to insert data into the table
with engine.connect() as connection:
    # Create a transaction
    trans = connection.begin()

    try:
        # Execute the insert query
        connection.execute(insert_query, {'lat': distress_lat, 'long': distress_long})
        trans.commit()  # Commit the transaction
    except Exception as e:
        trans.rollback()  # Rollback the transaction in case of an error
        print(f"Error: {e}")

# Print the relevant information
with engine.connect() as connection:
    # Use text to create an SQL statement object
    select_query = text("SELECT * FROM nearest_port")
    result = connection.execute(select_query).fetchone()
    if result:
        print("Data successfully inserted into PostgreSQL database:")
        print(result)
    else:
        print("No data found in the nearest_port table.")
