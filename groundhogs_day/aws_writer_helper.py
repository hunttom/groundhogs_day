import csv
import json


def create_account_id_csv(account_list):
    print("Creating a csv file of Account Ids")
    with open('account_ids.csv', 'w') as csvfile:
        fieldnames = ['AccountId']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator=',')

        for account in account_list:
            row = {}
            row['AccountId'] = account['AccountId']
            writer.writerow(row)

def create_json_file(data, type):
    """
    Function creates JSON dump of output
    """
    print("Creating a json file")
    with open(f'{type}.json', 'w') as jsonfile:
        json.dump(data, jsonfile)