import pymongo
import pandas as pd
import os
import json
import glob
import numpy as np
from colorama import Fore, Back, Style
import pandas as pd
import matplotlib.pyplot as plt
import pymongo.errors
import seaborn as sb
import base64
from io import BytesIO
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


"""
Class for to deal with the Mongo Database
This class is responsible for:
    -committing and upload logs to the database
    -grabbing data from the database
    -graphing data from the database
"""


class Mongo:
    """
    Inializes the Mongo class
        - Connects to database
    """
    def __init__(self):

        creds_path = 'creds.json'
        with open(creds_path, 'r') as f:
            creds = json.load(f)
        username = creds['username']
        password = creds['password']
        
        print(f"{Fore.CYAN}Attempting to connect to the database...{Style.RESET_ALL}")

        try:
            uri = f'mongodb://{username}:{password}@localhost:27017'
            self.client = pymongo.MongoClient(uri)
            self.db = self.client.get_database('SmartDisplay')
            self.smartDisplay = self.db['configuration']
            print(f"{Fore.GREEN}Connected to the database{Style.RESET_ALL}")


        except Exception as e:
            print(f"{Fore.RED}Error connecting to the database: {e}{Style.RESET_ALL}")
            raise Exception(f"Error connecting to the database: {e}")


    def insert_config(self, config_path):
        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            result = self.smartDisplay.insert_one({'config': config_data})
            print(f"{Fore.GREEN}Config file inserted with id: {result.inserted_id}{Style.RESET_ALL}")
            return result
        except Exception as e:
            print(f"{Fore.RED}Failed to insert config file: {e}{Style.RESET_ALL}")
            return None

if __name__ == "__main__":
    mongo = Mongo()
    
    
    try:
        test_doc = {"status": "test_insert", "working": True}
        result = mongo.smartDisplay.insert_one(test_doc)
        print(f"{Fore.GREEN}Successfully inserted test doc with ID: {result.inserted_id}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Test insert failed: {e}{Style.RESET_ALL}")