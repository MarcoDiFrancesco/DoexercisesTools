import re

cellDatePosition = "<Cell R1C7 '2019-03-08'>"
print(cellDatePosition)
cellDatePosition.split()
print(re.findall(r'R(\d+)',cellDatePosition))
print(re.findall(r'C(\d+)',cellDatePosition))

