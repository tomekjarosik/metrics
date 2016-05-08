import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--root-dir', type=str,
                   help='root dir where all build.times files exists')
parser.add_argument('--current', type=str,
                   help='path to file with current metrics')
parser.add_argument('--previous', type=str,
                   help='path to file with previous metrics')
args = parser.parse_args()

print("Hello from python")
print args

"""
import os
path = os.path.dirname(os.path.abspath(__file__))
f = open(os.path.join(path, "build.times"))
for line in f:
    print(line)
"""