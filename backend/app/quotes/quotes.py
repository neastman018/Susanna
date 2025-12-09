import sqlite3
import os
from dotenv import load_dotenv

load_dotenv('.env.development')
DB_QUOTES_PATH = os.getenv('DB_QUOTES_PATH')

print (f"Using quotes database at: {DB_QUOTES_PATH}")
DB_PATH = 'quotes.db'


def get_random_quote():
    conn = None

    try:
        conn = sqlite3.connect(DB_QUOTES_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT saint_name, quote_text FROM quotes
            ORDER BY RANDOM()
            LIMIT 1
        """)
        
        row = cursor.fetchone()  
        
        if row:
            return {"quote": row[1], "author": row[0]}     
         
    except sqlite3.Error as e:
        print(f"Error loading quotes: {e}")
        return None
    finally:
        if conn:
            conn.close()
            
def show_all_quotes():
    conn = None
    
    try:
        conn = sqlite3.connect(DB_QUOTES_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table';
        """)
        
        tables = cursor.fetchall()
        
        if tables:
            print("Tables in database:")
            for table in tables:
                print(f"  - {table[0]}")
            return tables
        else:
            print("No tables found.")
            return None
            
    except sqlite3.Error as e:
        print(f"Error loading tables: {e}")
        return None
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    quote = get_random_quote()
    if quote:
        print(f'"{quote["quote"]}" - {quote["author"]}')
    else:
        print("No quote found.")