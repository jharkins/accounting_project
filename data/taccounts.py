import csv
import re
from pprint import pprint
import json
import io
import math

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
balances = {
    '': {'starting': 0, 'balance': 0},
    'Allowance for Doubtful Accounts': {'starting': -25000, 'balance':0},
    'Contributed Capital': {'starting': -3000000, 'balance':0},
    'Patent': {'starting': 0, 'balance':0},
    'Bond Interest Expense': {'starting': 0, 'balance':0},
    'Gain on Sale of Land': {'starting': 0, 'balance':0},
    'Securities Fair Value Adjustment': {'starting': 0, 'balance':0},
    'Equipment': {'starting': 5000000, 'balance':0},
    'Sales Revenue': {'starting': 0, 'balance':0},
    'Advertising Expense': {'starting': 0, 'balance':0},
    'Interest Expense': {'starting': 0, 'balance':0},
    'Utility Expense': {'starting': 0, 'balance':0},
    'Wage Expense': {'starting': 0, 'balance':0},
    'Office Supplies': {'starting': 0, 'balance':0},
    'Retained Earnings': {'starting': -1995000, 'balance':0},
    'Supplies Expense': {'starting': 0, 'balance':0},
    'Loss on Sale of Equipment': {'starting': 0, 'balance':0},
    'Office Furniture': {'starting': 0, 'balance':0},
    'COGS': {'starting': 0, 'balance':0},
    'No economic transaction': {'starting': 0, 'balance':0},
    'Bond Interest Payable': {'starting': 0, 'balance':0},
    'Wages Payable': {'starting': -150000, 'balance':0},
    'Interest Income': {'starting': 0, 'balance':0},
    'Accumulated Depreciation': {'starting': -2000000, 'balance':0},
    'Marketable Securities': {'starting': 75000, 'balance':0},
    'Premium on Bonds Payable': {'starting': 0, 'balance':0},
    'Land': {'starting': 1450000, 'balance':0},
    'Cash': {'starting': 785000, 'balance':0},
    'Prepaid Insurance': {'starting': 0, 'balance':0},
    'Accounts Payable': {'starting': -450000, 'balance':0},
    'Bad debt expense': {'starting': 0, 'balance':0},
    'Accounts Receivable': {'starting': 455000, 'balance':0},
    'Amortization': {'starting': 0, 'balance':0},
    'Short Term Note payable': {'starting': 0, 'balance':0},
    'Rent Expense': {'starting': 0, 'balance':0},
    'Accumulated Depreciation- Equipment': {'starting': 0, 'balance':0},
    'Unrealized Gain': {'starting': 0, 'balance':0},
    'Fuel Expense': {'starting': 0, 'balance':0},
    'Dividends Payable': {'starting': -155000, 'balance':0},
    'Bonds Payable': {'starting': 0, 'balance':0},
    'Prepaid Rent': {'starting': 0, 'balance':0},
    'Depreciation Expense': {'starting': 0, 'balance':0},
    'Interest Payable': {'starting': 0, 'balance':0},
    'Insurance Expense': {'starting': 0, 'balance':0},
    'Deferred Revenue': {'starting': 0, 'balance':0},
    'No Transaction': {'starting': 0, 'balance':0},
    'Long Term Note Payable': {'starting': -1250000, 'balance':0},
    'Long Term Notes Receivable': {'starting': 285000, 'balance':0},
    'Inventory': {'starting': 975000, 'balance':0}
}

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
                    transaction_row_index = 0
                    journal_entries[transaction_id] = {
                            'id': cell,
                            'date': {0: '31-Dec'},
                            'transaction_note': {},
                            'entries': {},
                            'num_rows': 0
                    }

                if re.match('^[0-9]+-[A-Za-z]+$', cell):
                    print "Date Detected: {}".format(cell)
                    journal_entries[transaction_id]['date'][transaction_row_index] = cell

                if re.match('^[\sA-Za-z-_\(\)]', cell):
                    a = cell.strip()
                    if cn == 2:
                        print "Note Detected: {} in column {}".format(a,cn)
                        journal_entries[transaction_id]['transaction_note'][transaction_row_index] = a

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
                    journal_entries[transaction_id]['entries'][transaction_row_index] = [account, dorc[cn], s]

            cn+=1


        # If it's not a blank row, 
        if all_blank == False:
            transaction_row_index += 1
            print "The transaction row index: {}".format(transaction_row_index)
            journal_entries[transaction_id]['num_rows']=transaction_row_index

for account_name in accounts:

    #print accounts[account_name]
    starting_balance = balances[account_name]['starting']

    total_credits = 0
    total_debits = 0

    if starting_balance < 0:
        total_credits += math.fabs(starting_balance)
    else:
        total_debits += starting_balance

    for credit in accounts[account_name]['Credit']:
        total_credits += float(credit[1].strip('$').replace(',',''))

    for debit in accounts[account_name]['Debit']:
        total_debits += float(debit[1].strip('$').replace(',',''))

    balance = total_credits - total_debits

    accounts[account_name]['starting_balance'] = starting_balance
    accounts[account_name]['ending_balance'] = balance

with io.open('taccounts.v5.json', 'wb') as outfile:
    json.dump(accounts, outfile)

with io.open('journal_entries.v5.json', 'wb') as outfile:
    json.dump(journal_entries, outfile)


