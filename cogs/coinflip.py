import random

def coin_flip():
    """Returns a random value of Heads or Tails."""
    coin_faces = ['Heads','Tails']
    return random.choice(coin_faces)