# from models.list.ListItem import ListItem

# def update_score(self, winner: ListItem, loser: ListItem):
#   # Ensure that winner and loser are valid ListItem instances
#   if not isinstance(winner, ListItem) or not isinstance(loser, ListItem):
#     raise TypeError("winner and loser must be instances of ListItem")

#   # Calculate the new Elo scores using the existing logic
#   K = 64
#   expected_winner = 1 / (1 + 10 ** ((loser.score - winner.score) / 400))
#   expected_loser = 1 / (1 + 10 ** ((winner.score - loser.score) / 400))

#   winner.score += int(K * (1 - expected_winner))  # Winner won
#   loser.score += int(K * (0 - expected_loser))  # Loser lost

#   # Update only the changed scores in the JSON file
#   self.update_json_partial({winner.name: winner.score, loser.name: loser.score})