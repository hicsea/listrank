import json
import spacy
import os
import re  # Import regular expressions
import random
import numpy as np
from models.list.ListItem import ListItem
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

class List:
    def __init__(self, listname):
        self.nlp = spacy.load("en_core_web_lg")  # Load the Spacy model
        self.filepath = 'data/'
        self.filename_txt = 'txt/' + listname + '.txt'
        self.filename_json = 'json/' + listname + '.json'
        self.filepath_txt = self.filepath + self.filename_txt
        self.filepath_json = self.filepath + self.filename_json

        self.items = self.load_items()
        self.embeddings = {item.name: self.nlp(item.name).vector for item in self.items}
        self.similarity_matrix = self.compute_similarity_matrix()


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
        return [ListItem(name, details['score'], details['frequency']) for name, details in data.items()]


    def initialize_from_txt(self):
        data = {}
        with open(self.filepath_txt, 'r') as file:
            for line in file:
                # Split line by space, comma, or newline
                items = re.split(r',|\n', line.strip())
                for name in items:
                    if name:  # Ensure the name is not an empty string
                        # Initialize each name with a default score of 1000 and frequency of 0
                        data[name] = {'score': 1000, 'frequency': 0}

        self.save_to_json(data)
        return [ListItem(name, details['score'], details['frequency']) for name, details in data.items()]


    def save_to_json(self, data):
        with open(self.filepath_json, 'w') as file:
            json.dump(data, file)

    def add_item(self, name, score=1000):
        self.items.append(ListItem(name, score, 0))
        self.save_to_json({item.name: item.score for item in self.items})

    def get_two_distinct_items(self):
        if len(self.items) < 2:
            raise ValueError("Not enough items in the list to pick two distinct items.")
        
        weights = [1 / (item.frequency + 1) for item in self.items]
        selected_item1 = random.choices(self.items, weights=weights, k=1)[0]
        item1_idx = self.items.index(selected_item1)

        # Use similarity weights for the second selection
        similarity_weights = self.similarity_matrix[item1_idx]
        combined_weights = [similarity_weights[i] * weights[i] for i in range(len(self.items))]
        combined_weights[item1_idx] = 0  # Make sure not to select the same item

        selected_item2 = random.choices(self.items, weights=combined_weights, k=1)[0]

        return [selected_item1, selected_item2]

    def update_score(self, winner: ListItem, loser: ListItem):
        # Ensure that winner and loser are valid ListItem instances
        if not isinstance(winner, ListItem) or not isinstance(loser, ListItem):
            raise TypeError("winner and loser must be instances of ListItem")

        # Calculate the new Elo scores using the existing logic
        K = 64
        expected_winner = 1 / (1 + 10 ** ((loser.score - winner.score) / 400))
        expected_loser = 1 / (1 + 10 ** ((winner.score - loser.score) / 400))

        winner.score += int(K * (1 - expected_winner))  # Winner won
        loser.score += int(K * (0 - expected_loser))  # Loser lost

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
    
    def compute_similarity_matrix(self):
        # Ensure all vectors are normalized (unit vectors)
        normalized_embeddings = {name: vec / np.linalg.norm(vec) if np.linalg.norm(vec) > 0 else np.zeros_like(vec)
                                 for name, vec in self.embeddings.items()}
        
        # Preparing a matrix to store the similarity scores
        names = list(normalized_embeddings.keys())
        similarity_matrix = np.zeros((len(names), len(names)))

        # Compute cosine similarity between each pair of items
        for i, name1 in enumerate(names):
            for j, name2 in enumerate(names):
                if i <= j:  # No need to calculate twice, matrix is symmetrical
                    similarity_score = np.dot(normalized_embeddings[name1], normalized_embeddings[name2])
                    similarity_matrix[i][j] = similarity_score
                    similarity_matrix[j][i] = similarity_score
                    print(f"{name1}, {name2}: {similarity_score}")

        return similarity_matrix
    
    def cluster_items(self, n_clusters=5):
        """
        Clusters the items into 'n_clusters' using KMeans clustering based on their embeddings.
        Args:
        n_clusters (int): The number of clusters to form.

        Returns:
        dict: A dictionary mapping cluster ids to the list of item names in each cluster.
        """
        # Ensure all vectors are normalized (unit vectors)
        normalized_embeddings = {name: vec / np.linalg.norm(vec) if np.linalg.norm(vec) > 0 else np.zeros_like(vec)
                                for name, vec in self.embeddings.items()}
        
        # Extract embeddings in order and store the corresponding names
        names = list(normalized_embeddings.keys())
        vectors = np.array([normalized_embeddings[name] for name in names])
        
        # Perform KMeans clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        kmeans.fit(vectors)
        labels = kmeans.labels_
        
        # Organize items by cluster
        clusters = {i: [] for i in range(n_clusters)}
        for name, label in zip(names, labels):
            clusters[label].append(name)
        
        return clusters
    
    def print_clusters(self, n_clusters):
        clusters = self.cluster_items(n_clusters)  # Adjust the number of clusters as needed

        for cluster_id, items in clusters.items():
            print(f"Cluster {cluster_id}: {items}")

    
    def __repr__(self):
        return f"{self.items}"