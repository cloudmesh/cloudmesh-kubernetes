
import os
import sys

n=sys.argv[1] or 1

for i in range(5000,5000+n):
    os.system(f"python -m flask run --port={i}")
