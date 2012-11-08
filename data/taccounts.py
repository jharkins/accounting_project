import csv
import re
from pprint import pprint
import json
import io

''' T-Account Dictionary

For each account_name, create the 

<account_name>:
    debits:
        <debit_1>
        ...
    credits:
        <credit_1>
        ...


'''

# Used for labeling a column
dorc = ['','', 'Debit','Credit']

# Accounts dictionary
accounts = {}

# Build a dictionary of t-accounts
with open('journal.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        # Determine if this is a blank row
        all_blank = True

        # Keep track of the cell number - for debits and credits
        cn = 0

        # Keep track of the account
        account = ''

        for cell in row:
            if cell != '':
                all_blank = False

                # These define a transaction - might be important later
                if re.match('^[0-9]', cell):
                    print "Transaction Detected: {}".format(cell)

                if re.match('^[A-Za-z-_\(\)]', cell):
                    a = cell.strip()
                    print "Account Detected: {}".format(a)
                    account = a

                    # Add the account to the dict
                    if account not in accounts:
                        # Frame out the account
                        accounts[account] = {'Debit': [], 'Credit': []}

                if re.match('^[\$]', cell):
                    s = re.sub(r'\s', '', cell)

                    if account == '':
                        raise Exception('A transaction without an account!')
                    
                    print "{} Detected: {}".format(dorc[cn], s)
                    accounts[account][dorc[cn]].append(s)

            cn+=1

        # If it's not a blank row, 
        if all_blank == False:
            pass


pprint(accounts)

with io.open('taccounts.json', 'wb') as outfile:
    json.dump(accounts, outfile)


