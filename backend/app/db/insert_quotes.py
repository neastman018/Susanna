import sqlite3
import csv
import io
import os

# Define the path to your shared database file
DB_PATH = 'backend/app/db/quotes.db'


Quotes = """
"Saint/Pope","Quote"
"Pope John Paul II","Freedom consists not in doing what we like, but in having the right to do what we ought."
"Pope John Paul II","The world offers you comfort. But you were not made for comfort. You were made for greatness"
"Pope John Paul II","The worst prison would be a closed heart."
"Pope John Paul II","Do not be afraid. Do not be satisfied with mediocrity. Put out into the deep and let down your nets for a catch."
"Pope John Paul II","The future starts today, not tomorrow."
"Pope John Paul II","It is the duty of every man to uphold the dignity of every woman."
"Pope John Paul II","My past, O Lord, to Your mercy; my present, to Your love; my future to Your providence."
"Padre Pio","Pray, hope, and don't worry."
"Padre Pio","The most beautiful act of faith is the one made in darkness, in sacrifice, and with extreme effort."
"Padre Pio","Sufferings gladly borne for others convert more people than sermons."
"Padre Pio","Do not become upset when difficulty comes your way. Laugh in its face and know that you are in the hands of God."
"Padre Pio","A soul in a state of grace has nothing to fear of demons who are cowards."
"St. Francis De Sales","Be who you are and be that well."
"St. Francis De Sales","Never be in a hurry; do everything quietly and in a calm spirit. Do not lose your inner peace for anything whatsoever, even if your whole world seems upset."
"St. Francis De Sales","Everything and everyone is won by the sweetness of our words and works."
"St. Francis De Sales","A word or a smile is often enough to put fresh life in a despondent soul."
"Pier Giorgio Frassati","In a world gone astray from God there is no peace, but it also lacks charity, which is true and perfect love."
"Pier Giorgio Frassati","To live without faith, without a heritage to defend, without battling constantly for truth, is not to live but to ‘get along’; we must never just ‘get along’."
"Pier Giorgio Frassati","Every day that passes, I fall more desperately in love with the mountains… I am ever more determined to climb the mountains, to scale the mighty peaks, to feel that pure joy which can only be felt in the mountains."
"Pier Giorgio Frassati","The world's thy ship and not thy home."
"Pope Benedict XVI","Purity of heart is what enables us to see."
"Pope Benedict XVI","If our church is not marked by caring for the poor, the oppressed, the hungry, we are guilty of heresy."
"St. Ignatius Loyola","Go forth and set the world on fire."
"St. Ignatius Loyola","Act as if everything depended on you; trust as if everything depended on God."
"St. Ignatius Loyola","Ad Majorem Dei Gloriam."
"St. Ignatius Loyola","Guard your eyes since they are the windows through which sin enters the soul."
"St. John Bosco","Act today in such a way that you need not blush tomorrow."
"St. John Bosco","Joy, with peace, is the sister of charity. Serve the Lord with laughter."
"St. John Bosco","Foolish is he who follows the pleasures of this world, because these are always fleeting and bring much pain. The only true pleasure is that which comes to us through faith."
"St. John Bosco","Let us strive to fare well in this life and in the next."
"St. John Bosco","Your reward in heaven will make up completely for all your pain and suffering."
"St. John Bosco","All for God and for His Glory. In whatever you do, think of the Glory of God as your main goal."
"St. Therese of Lisieux","True charity consists in bearing all our neighbour's defects - not being surprised at their weakness, but edified at their smallest virtues."
"St. Therese of Lisieux","The guest of our soul knows our misery; He comes to find an empty tent within us - that is all He asks."
"St. Therese of Lisieux","If every flower wanted to be a rose, nature would lose her springtime beauty."
"St. Therese of Lisieux","True happiness on earth consists in being forgotten and in remaining completely ignorant of created things. I understood that all we accomplish, however brilliant, is worth nothing without love."
"St. Therese of Lisieux","Do not think that love in order to be genuine has to be extraordinary. What we need is to love without getting tired."
"St. Therese of Lisieux","Without love, deeds, even the most brilliant, count as nothing."
"St. Therese of Lisieux","Remember that nothing is small in the eyes of God. Do all that you do with love."
"Mother Teresa","\"If you judge people, you have no time to love them.\""
"Mother Teresa","Peace begins with a smile."
"Mother Teresa","Not all of us can do great things. But we can do small things with great love."
"Mother Teresa","Every time you smile at someone, it is an action of love, a gift to that person, a beautiful thing."
"Mother Teresa","It's not how much we give but how much love we put into giving."
"Mother Teresa","A life not lived for others is not a life."
"Mother Teresa","If you find happiness, people may be jealous. Be happy anyway."
"Mother Teresa","Life is an opportunity, benefit from it. Life is beauty, admire it. Life is a dream, realize it."
"Mother Teresa","Yesterday is gone. Tomorrow has not yet come. We have only today. Let us begin."
"""

def populate_quotes_table():
    """Reads the CSV data and populates the quotes table in SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        print(f"Connected to database at: {os.path.abspath(DB_PATH)}")

        # 1. Create the new table for quotes (if it doesn't exist)
        # We use a simple structure: an auto-incrementing ID, the name, and the quote text.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                saint_name TEXT NOT NULL,
                quote_text TEXT NOT NULL
            )
        """)

        # 2. Prepare the data for insertion
        # We use io.StringIO to read the string Quotes as if it were a file.
        csv_file = io.StringIO(Quotes.strip())
        reader = csv.reader(csv_file)
        
        # Skip the header row
        next(reader) 
        
        insert_data = []
        for row in reader:
            # Row structure is: [Saint/Pope, Quote]
            if len(row) == 2:
                insert_data.append((row[0], row[1]))

        # 3. Insert all data using executemany for efficiency
        cursor.executemany("""
            INSERT INTO quotes (saint_name, quote_text)
            VALUES (?, ?)
        """, insert_data)

        conn.commit()
        print(f"\nSuccessfully inserted {len(insert_data)} quotes into the 'quotes' table.")

    except sqlite3.Error as e:
        print(f"SQLite Error during population: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()
            

def show_table():
    """Utility function to display all entries in the quotes table."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT saint_name, quote_text FROM quotes")
        rows = cursor.fetchall()
        
        for row in rows:
            print(f"[{row[0]}] - {row[1]}")
            
    except sqlite3.Error as e:
        print(f"SQLite Error during display: {e}")
    finally:
        if conn:
            conn.close()
            
def clear_db():
    """Utility function to clear the quotes table."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM quotes")
        conn.commit()
        print("Cleared all entries from the 'quotes' table.")
        
    except sqlite3.Error as e:
        print(f"SQLite Error during clearing: {e}")
    finally:
        if conn:
            conn.close()
            
if __name__ == "__main__":
    clear_db()
    populate_quotes_table()
    
    
    # --- Verification Step (Optional) ---
    # You can uncomment this section to verify the data was inserted correctly
    # print("\n--- Verification: Reading back 3 quotes ---")
    # try:
    #     conn = sqlite3.connect(DB_PATH)
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT saint_name, quote_text FROM quotes LIMIT 3")
    #     for row in cursor.fetchall():
    #         print(f"[{row[0]}] - {row[1][:60]}...")
    # except sqlite3.Error as e:
    #     print(f"Verification Error: {e}")
    # finally:
    #     if conn:
    #         conn.close()