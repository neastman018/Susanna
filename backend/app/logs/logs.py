import os
import glob
from datetime import datetime

def log(text):
    print(text)
    # Get list of all txt files in the directory
    txt_files = glob.glob(os.path.join("./logs", "*.txt"))
    
    if not txt_files:
        print("No txt files found in the directory. Creating file")
        return

    # Get the most recently modified file
    latest_file = max(txt_files, key=os.path.getmtime)
    
    # Write to the most recent file
    with open(latest_file, 'a') as f:
        f.write(text + '\n')
    


def time_stamp() -> str:
    return datetime.now().strftime("%m/%d--%H:%M")


# Example usage:
if __name__ == "__main__":
    text_to_write = "This is a new line."
    print(time_stamp())