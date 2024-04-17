import json
import os
import re  # Import regular expressions
import random
from ListItem import ListItem

class List:
    def __init__(self, listname):
        self.filepath = 'lists/'
        self.filename_txt = listname + '.txt'
        self.filename_json = listname + '.json'
        self.filepath_txt = self.filepath + self.filename_txt
        self.filepath_json = self.filepath + self.filename_json


        self.items = self.load_items()


    def load_items(self):
        if os.path.exists(self.filepath_json):
            return self.load_from_json()
        elif os.path.exists(self.filepath_txt):
            return self.initialize_from_txt()
        else:
            # Raise an exception if the text file does not exist
            raise FileNotFoundError(f"No such file: {self.filename_txt}")


    def load_from_json(self):
        with open(self.filepath_json, 'r') as file:
            data = json.load(file)
        return [ListItem(name, score) for name, score in data.items()]


    def initialize_from_txt(self):
        data = {}
        with open(self.filepath_txt, 'r') as file:
            for line in file:
                # Split line by space, comma, or newline
                items = re.split(r'[,\s]\s*', line.strip())
                for name in items:
                    if name:  # Ensure the name is not an empty string
                        data[name] = 1000  # Default score

        self.save_to_json(data)
        return [ListItem(name, score) for name, score in data.items()]


    def save_to_json(self, data):
        with open(self.filepath_json, 'w') as file:
            json.dump(data, file)

    def add_item(self, name, score=1000):
        self.items.append(ListItem(name, score))
        self.save_to_json({item.name: item.score for item in self.items})

    def get_two_distinct_items(self):
        if len(self.items) < 2:
            raise ValueError("Not enough items in the list to pick two distinct items.")
        
        # Randomly pick two distinct items
        return random.sample(self.items, 2)
    
    def update_score(self, winner: ListItem, loser: ListItem):
        # Ensure that winner and loser are valid ListItem instances
        if not isinstance(winner, ListItem) or not isinstance(loser, ListItem):
            raise TypeError("winner and loser must be instances of ListItem")

        # Calculate the new Elo scores using the existing logic
        K = 64
        expected_winner = 1 / (1 + 10 ** ((loser.score - winner.score) / 400))
        expected_loser = 1 / (1 + 10 ** ((winner.score - loser.score) / 400))

        winner.score += int(K * (1 - expected_winner))  # Winner won
        loser.score += int(K * (0 - expected_loser))    # Loser lost

        # Update only the changed scores in the JSON file
        self.update_json_partial({winner.name: winner.score, loser.name: loser.score})

    def update_json_partial(self, changes):
        """ Update only specific scores in the JSON file. """
        if os.path.exists(self.filepath_json):
            with open(self.filepath_json, 'r+') as file:
                data = json.load(file)
                data.update(changes)  # Update the scores in the dictionary
                file.seek(0)          # Rewind the file to the start
                file.truncate()       # Truncate the file to overwrite
                json.dump(data, file)  # Write the updated dictionary back to the file
    
    def __repr__(self):
        return f"{self.items}"