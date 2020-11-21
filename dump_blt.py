from format.blt import load_blt
from counting.irv import get_irv_winner
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("path")
args = parser.parse_args()

with open(args.path, "r") as file:
    blt = load_blt(file)
    for ballot in blt.ballots:
        print(ballot)

    print(get_irv_winner(blt.ballots))
