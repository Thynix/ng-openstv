import argparse
from counting.irv import get_irv_winner
import pickle

parser = argparse.ArgumentParser()
parser.add_argument("path")
args = parser.parse_args()

with open(args.path, "rb") as file:
    blt = pickle.load(file)
    for ballot in blt.ballots:
        print(ballot)

    print(get_irv_winner(blt.ballots))
