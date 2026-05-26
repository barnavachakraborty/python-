import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--ip",type = str, required = True)
parser.add_argument("--op",type = str, required = True)
args = parser.parse_args()
ip = args.ip
op = args.op

