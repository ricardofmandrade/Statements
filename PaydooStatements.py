import pandas as pd
import numpy as np
import re 
import glob
import os 

pathtofile = '/Users/ricardoandrade/Downloads/Paydoo/Tx_Statements/*'
pathtomerged = '/Users/ricardoandrade/Downloads/Paydoo/Merged_Statements/'
file = '/Users/ricardoandrade/Downloads/Paydoo/Tx_Statements/20200506_uphold_gbp_TransactionDetail.csv'

### Not being used 
pattern_usd = re.compile(pattern = 'usd*')
pattern_eur = re.compile(pattern = 'eur*')
pattern_gbp = re.compile(pattern = 'gbp*')
### Not being used

all_files = []
usd_files = []
eur_files = []
gbp_files = []

### Iterate over all the files in PathToFile and builds a list with those files 
for name in glob.glob(pathtofile):
    if "usd" in name:
        usd_files.append(os.path.abspath(name))
    elif "eur" in name:
        eur_files.append(os.path.abspath(name))
    elif "gbp" in name:
        gbp_files.append(os.path.abspath(name))
    else: 
        print("Unrecognized File")

print(usd_files)

### Combine all files in each list - Can I put this inside the for loop?
usd_csv = pd.concat([pd.read_csv(usd) for usd in usd_files ])
eur_csv = pd.concat([pd.read_csv(eur) for eur in eur_files ])
gbp_csv = pd.concat([pd.read_csv(gbp) for gbp in gbp_files ])
all_files = [usd_csv,eur_csv,gbp_csv]
### Put upper block inside for loop? 

### Iterate over the 3 currencies and treat Data
for currency in all_files:
    pd.DataFrame(data=currency)
    currency['DateTime Converted'] = pd.to_datetime(currency['Processing Date'], errors='raise', format='%d/%m/%Y %H:%M')
    currency.insert(2, 'Day', currency['DateTime Converted'].dt.day)
    currency.insert(3, 'Month', currency['DateTime Converted'].dt.month)
    currency.insert(4, 'Year', currency['DateTime Converted'].dt.year)
    currency.drop(columns=['DateTime Converted','Billing Method','Scheme','BIN','Last 4','Issuing Country',\
        'MDR Region','MDR Product Type','MDR Card Type','Username','Merchant Identifier','Terminal Identifier','Unique ID',\
            'Merchant Category Code','Description','RRN','ARN','Merchant Reference', 'UniqueID', 'Auth Code',\
                'Electronic Commerce Indicator', 'MID Currency','Interchange Fee Descriptor','Scheme Fee Descriptor',\
                    'Reserve Release Date','Settlement Currency','Reason Code','Reason Code Description',\
                         'CPD','Chargeback Date'], errors='ignore', axis = 1, inplace = True)
    print(currency)

### Exporting all files to CSV
usd_csv.to_csv(pathtomerged+"usd_transactions.csv", index=False, encoding='utf-8-sig')
eur_csv.to_csv(pathtomerged+"eur_transactions.csv", index=False, encoding='utf-8-sig')
gbp_csv.to_csv(pathtomerged+"gbp_transactions.csv", index=False, encoding='utf-8-sig')

print(currency.columns)