# WorldPortIndex-Migration-and-Analytics
Efficient migration of World Port Index data to PostgreSQL, followed by insightful data mart creation for strategic logistics analytics


## Setup
1. Install the required Python packages using the provided command.
2. Create a .env file in the script's directory with the following variables:
  - DB_USER_NAME: Your PostgreSQL username
  - DB_PASSWORD: Your PostgreSQL password
  - DB_NAME: Your PostgreSQL database name
  - PORT: Your PostgreSQL port
  - HOST: Your PostgreSQL host

## Usage
1. Ensure the "WPI.mdb" (Microsoft Access) file is in the same directory as the script.
2. Run the script in your Python environment:
  ```
  python extract_load.py
  ```
3. The script will connect to the Access database, extract specified tables, and load them into corresponding PostgreSQL tables.

## Tables to Migrate
- Country Codes
- Country Codes Old
- Depth Code LUT
- Drydock/Marine Railway Code LUT
- Harbor Size LUT
- Harbor Type LUT
- Maximum Size Vessel LUT
- Repairs Code LUT
- Shelter Afforded LUT
- Wpi Data
- WPI Import
- WPI Region

## Important Notes
- Ensure the correct Microsoft Access Driver is installed.
- Review and update the .env file with your PostgreSQL database credentials.

## Additional Note
- This script assumes the presence of "WPI.mdb" in the script's directory.
- If using a different Access database file, update the script accordingly.

## Output
Screen-shots of the SQL output of the tables created can be found in directory 'Output_Screenshots'