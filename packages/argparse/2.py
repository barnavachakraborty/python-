import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--name",help="Enter your name: ")
parser.add_argument("--age", type=int,help = "Enter your age: ")
parser.add_argument("--debug", action="store_true")
args = parser.parse_args()

print(args.name, args.age)