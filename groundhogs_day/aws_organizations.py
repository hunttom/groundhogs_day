import boto3
import json


from tabulate import tabulate
from groundhogs_day import aws_list_helper, aws_writer_helper, display_helper

#################
# Organizations #
#################

def organization_information(account_list, output_format, export):
    """
    Organizational Information Overview
    Functions:
        1. Org overview with:
            Org-Id, FeatureSet, Management Account ID, 
            Email, Availabe PolicyTypes, Number of Accounts: 
        Displays in <json,table>
        2. Export Organization Information into JSON file
    """

    #FORMAT OF DATA [{}]: List of Dictionaries

    org_info = aws_list_helper.organizations_management_account()
    org_info['NumberOfAccounts'] = len(account_list)
    organization_information = []
    organization_information.append(org_info)
    display_helper.display_information(data=organization_information, output_format=output_format)
    if export:
        aws_writer_helper.create_json_file(data=organization_information, type='org_info')

############
# Accounts #
############

def account_information(data, output_format, export):
    """
    Account Information Overview
    Functions:
        1. List accounts in org with Name, AccountId, Email: Displays in CSV, JSON, TABLE
        2. Export AccountIds in CSV.
        3. Export Account information into JSON file
    """
    if output_format == 'csv':
        display_helper.organizations_accounts_csv_printer(data)
        if export:
            aws_writer_helper.create_account_id_csv(data)
    else:
        display_helper.display_information(data=data, output_format=output_format)
        if export:
            aws_writer_helper.create_json_file(data=data, type='account_info')

##########
# Admins #
##########

def organization_admins(output_format, export):
    """
    Delegated Admins Information Overview
    Functions:
        1. List organizational admins with Name, AccountId, Email, Services Delegated: Displays in JSON, TABLE
        2. Export Org Admins in JSON
    """
    organization_admins = aws_list_helper.organizations_describe_delegated_admins()
    display_helper.display_information(data=organization_admins, output_format=output_format)
    if export:
        aws_writer_helper.create_json_file(data=organization_admins, type='deletgated_admins')