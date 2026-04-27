import random

class RandomOutcomeStrategy:

    def determine(self, probability):
        return "WIN" if random.random() < probability else "LOSS"