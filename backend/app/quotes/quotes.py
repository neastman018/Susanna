import random

quotes = [
    "Freedom consists not in doing what we like, but in having the right to do what we ought.",
    "It is the duty of every man to uphold the dignity of every woman."
    "Do not be afraid. Do not be satisfied with mediocrity. Put out into the deep and let down your nets for a catch.",           
    "Pray, hope, and do not worry."
    "You learn to speak by speaking, to study by studying, to run by running, to work by working; and just so, you learn to love by loving.",
    
]

authors = [
    "Pope John Paul II",
    "Pope John Paul II",
    "Pope John Paul II",
    "Padre Pio",
    "Saint Francis de Sales"
]

def get_random_quote():
    idx = random.randint(0, len(quotes) - 1)
    return {"quote": quotes[idx], "author": authors[idx]}