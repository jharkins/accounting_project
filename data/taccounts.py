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
dorc = ['','', '', '', 'Debit','Credit']

# Accounts dictionary
accounts = {}

# Journal Entries
journal_entries = {} 

transaction_id = False

# Build a dictionary of t-accounts
with open('journal_entries.v3.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        # Determine if this is a blank row
        all_blank = True

        # Keep track of the cell number - for debits and credits
        cn = 0

        # Keep track of the account
        account = ''

        # Keep track of transaction for the journal

        for cell in row:
            if cell != '':
                all_blank = False

                # These define a transaction - might be important later
                if re.match('^[0-9]+$', cell):
                    print "\nTransaction Detected: {}".format(cell)
                    transaction_id = cell
                    journal_entries[transaction_id] = {
                            'id': cell,
                            'date': '31-Dec',
                            'transaction_note': '',
                            'entries': []
                    }

                if re.match('^[0-9]+-[A-Za-z]+$', cell):
                    print "Date Detected: {}".format(cell)
                    journal_entries[transaction_id]['date'] = cell

                if re.match('^[\sA-Za-z-_\(\)]', cell):
                    a = cell.strip()
                    if cn == 2:
                        print "Note Detected: {} in column {}".format(a,cn)
                        journal_entries[transaction_id]['transaction_note'] = a

                    if cn == 3:
                        print "Account Detected: {} in column {}".format(a,cn)
                        account = a

                    # Add the account to the dict
                    if account not in accounts:
                        # Frame out the account
                        accounts[account] = {'Debit': [], 'Credit': []}

                if re.search('\$[\d,\.]+', cell) and (cn == 4 or cn == 5):
                    s = re.sub(r'\s', '', cell)

                    if account == '':
                        print row
                        raise Exception('A transaction without an account!')
                    
                    print "In {} a {} of {} was found".format(account, dorc[cn], s)

                    accounts[account][dorc[cn]].append([transaction_id, s])
                    journal_entries[transaction_id]['entries'].append( [account, dorc[cn], s])

            cn+=1


        # If it's not a blank row, 
        if all_blank == False:
            pass

pprint(journal_entries)
pprint(accounts)

with io.open('taccounts.v4.json', 'wb') as outfile:
    json.dump(accounts, outfile)

with io.open('journal_entries.v4.json', 'wb') as outfile:
    json.dump(journal_entries, outfile)


