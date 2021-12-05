import pandas as pd 

def createPharmacyList():
    #Creates a dictionary of pharmacies to be used in the select group
    df = pd.read_csv("final_data.csv")
    pharmacies = df[['ContractorName', 'ContractorCode','Address','town','city','county','Postcode']].copy()
    pharmacies = pharmacies.fillna('')
    pharmacies = pharmacies.sort_values('ContractorName',ascending=True)
    p = pharmacies.to_dict('records')
    return p
