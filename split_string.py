import re

cellDatePosition = "<Cell R1C7 '2019-03-08'>"
# take first number after R and C, (it is in an array beacuse of re)
row = int(re.findall(r'R(\d+)',cellDatePosition)[0])
col = int(re.findall(r'C(\d+)',cellDatePosition)[0])

