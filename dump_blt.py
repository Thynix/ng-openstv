from blt import load_blt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("path")
args = parser.parse_args()

with open(args.path, "r") as file:
    print(repr(load_blt(file)))
