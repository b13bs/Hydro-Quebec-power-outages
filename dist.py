#!/usr/bin/python3

import haversine

tab = []
with open("coords.txt") as f:
    for line in f:
        elem1 = float(line.split(" ")[1].strip())
        elem2 = float(line.split(" ")[0])
        tab.append((elem1, elem2))

diff = 9999999
target = (45.4795543, -73.61975660000002)
for elem in tab:
    substraction = haversine.haversine(target, elem)
    if substraction < diff:
        diff = substraction
        result = elem

print(result)

