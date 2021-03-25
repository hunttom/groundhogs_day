# FOR DISPLAYING INFORMATION FROM AWS
import json

from tabulate import tabulate
from groundhogs_day import aws_list_helper, aws_writer_helper

def display_information(data, output_format):
    """
    Prints a list of Account Information: Name, Account Id, Email Address
    """
    #FORMAT [{}]
    if output_format == 'table':
        print(tabulate(data, headers='keys', tablefmt='pretty'))
    # elif output_format == 'csv':
    #     display_csv_printer(data=data)
    elif output_format == 'json':
        print(json.dumps(data, sort_keys=False, indent=4))



# def organization_table(account_list):
#     """
#     Prints both Organizational Information Overview and Account List
#     """
#     org_info = aws_list_helper.organizations_management_account()

#     print('Organization Information Overview')
#     organization_information(account_list, org_info)

#     print('\nAccount Information')
#     account_information(account_list)


def organizations_accounts_csv_printer(data):
    """
    Prints Account Ids in comma separated values
    """
    #[{}]
    accounts = []
    for account in data:
        accounts.append(int(account['AccountId']))

    string_accounts = [str(accounts).strip('[]')]
    table_date = [string_accounts]

    print(tabulate(table_date, headers=['Account Ids'], tablefmt='pretty'))

def display_csv_printer(data):
    """
    Prints data in comma separated values
    """
    data_list = []
    for data_dict in data:
        for key, value in data_dict.items():
            data_list.append(key)
            data_list.append(value)

    string_info = [str(data_list).strip('[]')]
    table_data = [string_info]
    print(tabulate(table_data, headers=['AWS Info'], tablefmt='pretty'))
