import boto3


def organizations_list_accounts():
    """
    Creates a dictonary of Account Name, Account Id, Email Address, and ARN
    """

    client = boto3.client('organizations')
    response = client.list_accounts()

    account_list = []
    for account_info in response['Accounts']:
        account = {'Name': account_info['Name'], \
                   'AccountId': account_info['Id'], \
                   'Email': account_info['Email']} #, Arn': account_info['Arn']}
        account_list.append(account)

    return account_list


def organizations_list_service_regions(service):
    """
    Locates all regions that the AWS Services
    """
    print(f"Getting list of regions in for {service}...")

    session = boto3.session.Session()
    region_list = session.get_available_regions(service)
    print(f"Number of regions: {len(region_list)} that support {service}")

    return region_list


def organizations_management_account():
    """
    Prints out organizational information for the management account
    """
    client = boto3.client('organizations')
    response = client.describe_organization()
    org_info = {'Id': response['Organization']['Id'], \
        'FeatureSet': response['Organization']['FeatureSet'], 
        'ManagementAccountId': response['Organization']['MasterAccountId'], \
        'Email': response['Organization']['MasterAccountEmail'], \
        'AvailablePolicyTypes': response['Organization']['AvailablePolicyTypes']}

    return org_info


def organizations_describe_account(account_id):
    """
    Creates a dictonary of Account Name, Account Id, Email Address, and ARN for a single account
    """

    client = boto3.client('organizations')
    response = client.describe_account(
        AccountId=account_id
    )

    account_list = []
    account = {'Name': response['Account']['Name'], \
               'AccountId': response['Account']['Id'], \
               'Email': response['Account']['Email']} #, Arn': account_info['Arn']}
    account_list.append(account)

    return account_list

def organizations_describe_delegated_admins():
    """
    Discovers delegated admins
    """
    delegated_admins =[]
    org_client = boto3.client('organizations')
    org_admins = org_client.list_delegated_administrators()
    for admin_account in org_admins['DelegatedAdministrators']:
        account_info = {}
        delegated_services_response = org_client.list_delegated_services_for_account(
            AccountId=admin_account['Id']
        )
        services = []
        for service in delegated_services_response['DelegatedServices']:
            services.append(service['ServicePrincipal'])

        account_info = {'Name': admin_account['Name'], \
               'AccountId': admin_account['Id'], \
               'Email': admin_account['Email'], \
               'Services': services
               }
        delegated_admins.append(account_info)

    return delegated_admins

def csv_printer(org_info):
    """
    Prints data in comma separated values
    """
    csv = []
    for info in org_info: 
        for key, value in info.items():
            csv.append(key)
            csv.append(value)

    print(f"{str(csv).strip('[]')}")
