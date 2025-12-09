import sqlite3
import json
import os
from datetime import datetime

date_str = datetime.now().strftime('%Y_%m_%d')
table_name = f"config_{date_str}"


# --- 1. Define the absolute path to your configuration database ---
# IMPORTANT: Use an absolute path on Raspbian (e.g., '/etc/myapp/config.db').
# For Windows testing, we'll use a path relative to the script for simplicity.
DB_PATH = 'config.db'

# --- 2. The Complex Configuration Object ---
# This is the data structure you want to share and modify.
FULL_CONFIG_OBJECT = {
    "ALARM": {
        "ALARM_SOUND": "Thats_Life.mp3",
        "WAKE_UP_TIMES": {
            "SUNDAY": "7:00",
            "MONDAY": "5:30",
            "TUESDAY": "5:30",
            "WEDNESDAY": "5:30",
            "THURSDAY": "5:30",
            "FRIDAY": "5:30",
            "SATURDAY": "7:00"
        }
    },
    "WEATHER": {
        "LATITUDE": 38.93368707829988,
        "LONGITUDE": -77.1774930079404
    },
    "CALENDARS": {
        "PRIMARY": {
            "NAME": "Personal",
            "ICAL_URL": "https://calendar.google.com/calendar/ical/nick.eastman%40youthapostles.org/public/basic.ics"
        }
    },
    "QUOTES": {
        "Pope John Paul II": {
            "1": "The future starts today, not tomorrow.",
            "2": "Do not be afraid to be saints.",
            "3": "Freedom consists not in doing what we like, but in having the right to do what we ought.",
            }
    }
}

def initialize_db(): # Can I make a table for each day?
    """Initializes the database and creates the necessary settings table."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # SQL to create the table if it doesn't exist
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                name TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                description TEXT
            )
        """)
        conn.commit()
        print(f"Database initialized at: {os.path.abspath(DB_PATH)}")
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
    finally:
        if conn:
            conn.close()

def save_config(name, config_object, description):
    """Saves a configuration object by converting it to a JSON string."""
    try:
        # Convert Python dictionary to JSON string
        json_string = json.dumps(config_object)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # INSERT OR REPLACE will insert a new row, or update the value if 'name' already exists
        cursor.execute(f"""
            INSERT OR REPLACE INTO {table_name} (name, value, description)
            VALUES (?, ?, ?)
        """, (name, json_string, description))

        conn.commit()
        print(f"\nConfiguration '{name}' saved successfully.")

    except sqlite3.Error as e:
        print(f"Error saving config: {e}")
    finally:
        if conn:
            conn.close()

def load_config(name):
    """Loads a configuration object and converts the JSON string back to a Python dictionary."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT value FROM {table_name} WHERE name=?", (name,))
        row = cursor.fetchone()
        
        if row:
            json_string = row[0]
            # Convert JSON string back to Python dictionary
            return json.loads(json_string)
        else:
            print(f"Configuration '{name}' not found.")
            return None
            
    except sqlite3.Error as e:
        print(f"Error loading config: {e}")
        return None
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    # 1. Initialize the database and table
    initialize_db()

    # 2. Save the full configuration object under a single key
    save_config('full_app_config', FULL_CONFIG_OBJECT, 'Master configuration for all modules.')

    # 3. Load the configuration back into a dictionary
    loaded_config = load_config('full_app_config')

    # 4. Demonstrate access and usage
    if loaded_config:
        print("\n--- Loaded and Parsed Configuration ---")
        
        # Access nested data easily
        saturday_time = loaded_config['ALARM']['WAKE_UP_TIMES']['SATURDAY']
        weather_lat = loaded_config['WEATHER']['LATITUDE']
        
        print(f"Saturday Wake-up Time: {saturday_time}")
        print(f"Weather Latitude: {weather_lat}")
        
        # Example of how a second app could read and use a different part:
        calendar_name = loaded_config['CALENDARS']['PRIMARY']['NAME']
        print(f"Calendar Name: {calendar_name}")
        
        print(f"Using table: {table_name}")
        
    print("-" * 40)
    print("Script finished. The config.db file is ready to be shared.")