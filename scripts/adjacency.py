#Processes the adjacency list found at https://www.census.gov/programs-surveys/geography/technical-documentation/records-layout/county-adjacency-record-layout.html into a decent csv format

import re
import pandas as pd

#Regexs
re_county = re.compile(r'^[^\t][\w \,\.\"\'\-]+\t(\d+)\s+"(?:[\w \,\.\"\'\-]+)"\s+(\d+)')
re_adj = re.compile(r'(\d+$)')

#Parsing text file
with open('../data/raw/county_adjacency.txt', 'r') as file:
    county_fips = 'HEAD_ENTRY'
    adj = []
    adj_dict = {}
    for line in file:
        match = re_county.search(line)
        if(match):
            adj_dict[county_fips] = adj
            county_fips = match.group(1)
            adj = []
            adj.append(match.group(2))
        else:
            match = re_adj.search(line)
            adj.append(match.group(0))
    adj_dict[county_fips] = adj
    
#Determining max number of columns
max = 0
for k in adj_dict:
    if(len(adj_dict[k]) > max):
        max = len(adj_dict[k])
del adj_dict['HEAD_ENTRY']

#Outputting CSV format
with open("../data/processed/adjacency_list.csv","w") as outFile:
    outFile.write('county')
    for i in range(max):
        outFile.write(',adjacent' + str(i))
    outFile.write('\n')
    for k in adj_dict:
        outString = k
        for v in adj_dict[k]:
            outString = outString + ',' + v
        outString = outString + '\n'
        outFile.write(outString)