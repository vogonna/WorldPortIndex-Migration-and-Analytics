import pandas as pd
from geopy.distance import geodesic
from sqlalchemy import create_engine, text
from dotenv import load_dotenv, dotenv_values

# Load environment variables from the .env file
load_dotenv()

# Load environment variables from .env file
config = dict(dotenv_values('.env'))
db_user_name = config.get('DB_USER_NAME')
db_password = config.get('DB_PASSWORD')
db_name = config.get('DB_NAME')
port = config.get('PORT')
host = config.get('HOST')

# Create and return a PostgreSQL database connection object
conn_str = f'postgresql+psycopg2://{db_user_name}:{db_password}@{host}:{port}/{db_name}'
engine = create_engine(conn_str)

# SQL query to select data from the wpi_data table
query = text('SELECT main_port_name as port_name, wpi_country_code, latitude_degrees, latitude_minutes, latitude_hemisphere, longitude_degrees, longitude_minutes, longitude_hemisphere  FROM wpi_data;')

# Execute the query and load the result into a pandas DataFrame
with engine.connect() as connection:
    ports_df = pd.read_sql_query(query, con=connection)
    
# Filter the DataFrame for Singapore's JURONG ISLAND port
jurong_island = ports_df[(ports_df['wpi_country_code'] == 'SG') & (ports_df['port_name'] == 'JURONG ISLAND')]

# # Extract latitude and longitude for JURONG ISLAND
jurong_island_latitude = jurong_island['latitude_degrees'].values[0] + (jurong_island['latitude_minutes'].values[0] / 60)
jurong_island_longitude = jurong_island['longitude_degrees'].values[0] + (jurong_island['longitude_minutes'].values[0] / 60)

# Function to calculate distance between two coordinates using Haversine formula
def calculate_distance(row):
    port_latitude = row['latitude_degrees'] + (row['latitude_minutes'] / 60)
    port_longitude = row['longitude_degrees'] + (row['longitude_minutes'] / 60)
    
    jurong_island_coords = (jurong_island_latitude, jurong_island_longitude)
    port_coords = (port_latitude, port_longitude)
    
    distance = geodesic(jurong_island_coords, port_coords).meters
    return distance

# Apply the function to calculate distances for all ports
ports_df['distance_in_meters'] = ports_df.apply(calculate_distance, axis=1)

# Filter the 5 nearest ports
five_nearest_ports = ports_df[ports_df['port_name'] != 'JURONG ISLAND'].nlargest(5, 'distance_in_meters')[['port_name', 'distance_in_meters']]

# Create a new table in the database to store the result
five_nearest_ports.to_sql('five_nearest_ports', con=engine, if_exists='replace', index=False)

# Print the result
print("5 Nearest Ports to JURONG ISLAND:")
print(five_nearest_ports)