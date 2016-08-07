#!/usr/bin/python3
from hash_utils import HashList
from sys import argv

h = HashList(argv[1])
print(h.search(15791986208310520790, 10))
