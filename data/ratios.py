import csv
import re
from pprint import pprint
import json
import io

'''
Parse ratios
'''
ratios = {}

# Build a dictionary of t-accounts
with open('ratios.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        ratio = {
            'id': row[0].strip(),
            'name': row[1].strip(),
            'formula': row[2].strip(),
            'values': [
                row[3].strip(), # 2012
                row[4].strip(), # 2011
                row[5].strip() # 2010
            ],
            'description': row[7].strip(),
            'graph': 'cartman.png'
        }

        ratios[ratio['id']]=ratio


with io.open('ratios.v1.json', 'wb') as outfile:
    json.dump(ratios, outfile)


