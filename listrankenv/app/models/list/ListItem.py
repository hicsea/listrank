class ListItem:
    def __init__(self, name, score, frequency):
        self.name = name
        self.score = score
        self.frequency = frequency

    def __repr__(self):
        return f"ListItem(name={self.name}, score={self.score})"

    def __lt__(self, other):
        return self.score < other.score  # Sort primarily by score
    
    def __str__(self):
        # Provides a nicely formatted string, used by the print() function.
        return f"{self.name}: {self.score}: {self.frequency} times appeared"
    
    def increment_frequency(self):
        self.frequency += 1