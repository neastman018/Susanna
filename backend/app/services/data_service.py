""" Service to interact with SQLite data storage. """
import os
import sqlite3
from dotenv import load_dotenv
import json
from datetime import datetime
from colorama import Fore, Style, init
from typing import Optional, Dict, Any, List

# --- START: Robust Import Fix ---
try:
    from ..models.data_models import QuoteModel, ConfigModel, AlarmModel
except (ImportError, ValueError):
    # Fallback for direct execution or different module structure
    from app.models.data_models import QuoteModel, ConfigModel, AlarmModel
# --- END: Robust Import Fix ---


load_dotenv('.env.development')


class DataService:
    # Updated __init__ to accept optional test_mode flag
    def __init__(self, test_mode: bool = False):
        self.test_mode = test_mode
        
        if self.test_mode:
            # When in test mode, set all database paths to the SQLite in-memory identifier
            in_memory_path = ":memory:"
            quotes_path = in_memory_path
            daily_logs_path = in_memory_path
            alarm_path = in_memory_path
            
            print(f"{Fore.YELLOW}--- Test Mode Active: Using In-Memory Databases ---{Style.RESET_ALL}")
            
        else:
            # Robust path resolution for production/development file system usage
            current_file_path = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.abspath(os.path.join(current_file_path, '..', '..'))
            
            quotes_rel_path = os.getenv('DB_QUOTES_PATH', 'app/db/quotes.db')
            daily_logs_rel_path = os.getenv('DB_DAILY_LOGS_PATH', 'app/db/app_logs.db') 
            alarm_rel_path = os.getenv('DB_ALARM_PATH', 'app/db/alarms.db')
            
            quotes_path = os.path.join(project_root, quotes_rel_path)
            daily_logs_path = os.path.join(project_root, daily_logs_rel_path)
            alarm_path = os.path.join(project_root, alarm_rel_path)
            
            # Ensure the database directory structure exists (only for file-based DBs)
            os.makedirs(os.path.dirname(alarm_path), exist_ok=True)
            
            print(f"{Fore.GREEN}DB Paths Resolved:{Style.RESET_ALL}")
            print(f"Quotes Path: {quotes_path}")
            print(f"Logs Path:   {daily_logs_path}")
            print(f"Alarm Path:  {alarm_path}\n")

        # Create persistent connections and store them on the instance
        self.conn_quotes = sqlite3.connect(quotes_path)
        self.conn_logs = sqlite3.connect(daily_logs_path)
        self.conn_alarm = sqlite3.connect(alarm_path)

        # Ensure the tables exist regardless of whether the DB is in-memory or file-based
        self._initialize_daily_logs_db()
        self._initialize_alarm_db()

    def close(self):
        """Closes all persistent database connections."""
        self.conn_quotes.close()
        self.conn_logs.close()
        self.conn_alarm.close()
        print(f"{Fore.BLUE}DataService connections closed.{Style.RESET_ALL}")

    def _initialize_daily_logs_db(self):
        """Ensures the single, structured daily_logs table exists and is fully defined."""
        try:
            cursor = self.conn_logs.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS daily_logs (
                    log_date TEXT PRIMARY KEY,
                    high_temp REAL,
                    low_temp REAL,
                    wake_up_alarm_time TEXT,
                    raw_config_json TEXT
                )
            """)
            self.conn_logs.commit()
            print("Daily logs database initialized successfully.")
            
        except sqlite3.Error as e:
            print(f"Error initializing daily logs database: {e}")
                
    def _initialize_alarm_db(self):
        """Ensures the alarms table exists and migrates the schema to add day_of_week if missing."""
        try:
            cursor = self.conn_alarm.cursor()
            
            # 1. Ensure the table exists with the current full schema
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alarms (
                    label TEXT PRIMARY KEY,
                    alarm_time TEXT,
                    start_date TEXT,
                    repeat TEXT,
                    day_of_week TEXT,
                    sound TEXT,
                    armed INTEGER
                )
            """)
            
            # 2. Schema Migration: Only attempt ALTER TABLE if not in test mode
            if not self.test_mode: 
                try:
                    cursor.execute("PRAGMA table_info(alarms)")
                    columns = [info[1] for info in cursor.fetchall()]
                    if 'day_of_week' not in columns:
                        cursor.execute("ALTER TABLE alarms ADD COLUMN day_of_week TEXT")
                        print("Schema Migration: Successfully added 'day_of_week' column to alarms table.")
                except sqlite3.OperationalError as e:
                    # Catch and log any unexpected issues during migration
                    print(f"Warning during alarm table schema migration: {e}")
            
            self.conn_alarm.commit()
            print("Alarm configuration database initialized successfully.")
            
        except sqlite3.Error as e:
            print(f"Error initializing alarm database: {e}")
        
    def insert_daily_log(self, config_data: Dict[str, Any]) -> bool:
        """Inserts a structured daily log entry into the centralized 'daily_logs' table."""
        date_str = datetime.now().strftime('%Y-%m-%d')
        
        # 1. Extract and process fields from the config dictionary
        weather = config_data.get("WEATHER", {})
        high_temp = weather.get("TODAY_HIGH")
        low_temp = weather.get("TODAY_LOW")
        
        alarm_config = config_data.get("ALARM", {})
        today_weekday = datetime.now().strftime('%A').upper()
        # Safely access the wake up time based on the current weekday
        wake_up_alarm_time = alarm_config.get("WAKE_UP_TIMES", {}).get(today_weekday)
        
        raw_config_json = json.dumps(config_data)

        try:
            cursor = self.conn_logs.cursor()

            # Insert or replace the log using the centralized table
            cursor.execute("""
                INSERT OR REPLACE INTO daily_logs 
                    (log_date, high_temp, low_temp, wake_up_alarm_time, raw_config_json)
                VALUES (?, ?, ?, ?, ?)
            """, (date_str, high_temp, low_temp, wake_up_alarm_time, raw_config_json))

            self.conn_logs.commit()
            print(f"\nDaily log for {date_str} saved successfully to daily_logs table.")
            return True

        except sqlite3.Error as e:
            print(f"Error inserting daily log for {date_str}: {e}")
            return False
        
    def get_random_quote(self) -> Optional[QuoteModel]:
        try:
            cursor = self.conn_quotes.cursor()
            
            cursor.execute("""
                SELECT saint_name, quote_text FROM quotes
                ORDER BY RANDOM()
                LIMIT 1
            """)
            
            row = cursor.fetchone()
            
            if row:
                return QuoteModel(**{"quote": row[1], "author": row[0]})
            
            return None
            
        except sqlite3.Error as e:
            print(f"Error loading quotes: {e}")
            return None
        
    def insert_alarm(self, alarm: AlarmModel) -> bool:
        """Inserts or updates the alarm configuration in the database. Serializes day_of_week."""
        try:
            # Serialize the day_of_week list into a JSON string
            day_of_week_json = json.dumps(alarm.day_of_week) 
            
            cursor = self.conn_alarm.cursor()
            
            # Note: The column order must match the VALUES order below
            cursor.execute("""
                INSERT OR REPLACE INTO alarms 
                    (label, alarm_time, start_date, repeat, day_of_week, sound, armed) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                alarm.label, 
                alarm.alarm_time, 
                alarm.start_date, 
                alarm.repeat, 
                day_of_week_json, # Insert the JSON string
                alarm.sound, 
                int(alarm.armed)
            ))
            
            self.conn_alarm.commit()
            print(f"Alarm configuration saved: {alarm.label}")
            return True
            
        except sqlite3.Error as e:
            print(f"Error saving alarm config: {e}")
            return False
                
    def grab_all_alarms(self) -> List[AlarmModel]:
        """Retrieves all alarm configurations from the database. Deserializes day_of_week."""
        alarms: List[AlarmModel] = []
        try:
            cursor = self.conn_alarm.cursor()
            
            # FIXED: Ensuring day_of_week is selected and is the 4th column (index 3)
            cursor.execute("""
                SELECT 
                    alarm_time, 
                    start_date, 
                    repeat, 
                    day_of_week, 
                    sound, 
                    label, 
                    armed 
                FROM alarms
            """)
            rows = cursor.fetchall()
            
            for row in rows:
                # Deserialize the day_of_week JSON string back to a Python list
                # Index 3 corresponds to the 'day_of_week' column
                day_of_week_list = json.loads(row[3]) 
                
                alarm = AlarmModel(
                    alarm_time=row[0],
                    start_date=row[1],
                    repeat=row[2],
                    day_of_week=day_of_week_list, # Use the deserialized list
                    sound=row[4],
                    label=row[5],
                    armed=bool(row[6])
                )
                alarms.append(alarm)
                
            return alarms
            
        except sqlite3.Error as e:
            print(f"Error retrieving alarms: {e}")
            return []
    
    def clear_alarms(self) -> bool:
        """Utility function to clear all entries in the alarms table."""
        try:
            cursor = self.conn_alarm.cursor()
            
            cursor.execute("DELETE FROM alarms")
            self.conn_alarm.commit()
            print("Cleared all entries from the 'alarms' table.")
            return True
            
        except sqlite3.Error as e:
            print(f"Error clearing alarms: {e}")
            return False
    
if __name__ == "__main__":
    init(autoreset=True) # Initialize colorama
    
    # --- Running in test mode for demonstration ---
    print(f"\n{Fore.MAGENTA}--- Running in Test Mode (In-Memory Demonstration) ---{Style.RESET_ALL}")
    
    # Use a 'try...finally' block to ensure the connection is closed
    data_service_test = None
    try:
        # 1. Initialize the service (creates tables in memory)
        data_service_test = DataService(test_mode=True) 
        
        # --- Test Data ---
        alarm1 = AlarmModel(
            alarm_time="05:30",
            start_date="2025-12-16",
            repeat="Weekly",
            day_of_week=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            sound="Thats_Life.mp3",
            label="Weekday Wake Up",
            armed=True
        )
        
        # --- Test Insertion (using the persistent connection) ---
        print(f"\n{Fore.CYAN}--- Inserting Test Alarm (In-Memory) ---{Style.RESET_ALL}")
        data_service_test.insert_alarm(alarm1)
        
        # --- Test Retrieval (using the persistent connection) ---
        print(f"\n{Fore.CYAN}--- Retrieving All Alarms (In-Memory) ---{Style.RESET_ALL}")
        retrieved_alarms = data_service_test.grab_all_alarms()
        
        if retrieved_alarms:
            print(f"{Fore.GREEN}SUCCESS: Retrieved {len(retrieved_alarms)} alarms from in-memory DB.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}FAILURE: No alarms retrieved from in-memory DB.{Style.RESET_ALL}")

    finally:
        # 2. Close the connection, wiping the in-memory database
        if data_service_test:
            data_service_test.close()

    # Now, if we try to open a new instance, it will be empty again:
    print(f"\n{Fore.MAGENTA}--- Verifying Database Wiped (New Instance) ---{Style.RESET_ALL}")
    new_data_service = DataService(test_mode=True)
    if not new_data_service.grab_all_alarms():
        print(f"{Fore.GREEN}SUCCESS: New in-memory DB is empty.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}FAILURE: New in-memory DB still has data.{Style.RESET_ALL}")
    new_data_service.close()