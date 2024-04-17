class ListItem:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __repr__(self):
        return f"ListItem(name={self.name}, score={self.score})"

    def __lt__(self, other):
        return self.score < other.score  # Sort primarily by score
    
    def __str__(self):
        # Provides a nicely formatted string, used by the print() function.
        return f"{self.name}: {self.score}"