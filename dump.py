import argparse
from counting.irv import get_irv_winner
from format.blt import load_blt
import pickle

parser = argparse.ArgumentParser()
parser.add_argument("input_type", choices=[
    "blt",
    "pickle",
])
parser.add_argument("path")
args = parser.parse_args()

if args.input_type == "blt":
    with open(args.path, "r") as file:
        blt = load_blt(file)
elif args.input_type == "pickle":
    with open(args.path, "rb") as file:
        blt = pickle.load(file)

for ballot, weight in blt.ballots.items():
    print(f"{weight} ballots of: {ballot}")

for candidate_number, vote_count in get_irv_winner(blt.ballots).items():
    print(f"{blt.candidate_names[candidate_number - 1]}: {vote_count} votes")
