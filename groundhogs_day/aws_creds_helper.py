import boto3
import botocore
import sys

def creds_checker(account_id, role):
    try:
        generate_cross_account_credentials(account_id, role)
    except botocore.exceptions.NoCredentialsError as CredsError:
        print('No Active credentials exist')
        sys.exit(1)

def generate_cross_account_credentials(account_id, role):
    """
    Get STS credentials for target account
    """
    client = boto3.client('sts')
    response = client.assume_role(
        RoleArn=f'arn:aws:iam::{account_id}:role/{role}',
        RoleSessionName=f'CrossAccountAccessFor-{role}'
    )

    ACCESS_KEY = response['Credentials']['AccessKeyId']
    SECRET_KEY = response['Credentials']['SecretAccessKey']
    SESSION_TOKEN = response['Credentials']['SessionToken']

    return ACCESS_KEY, SECRET_KEY, SESSION_TOKEN


def generate_cross_account_session(service, credentials, region):
    """
    Assume role in the service and account
    """
    ACCESS_KEY = credentials[0]
    SECRET_KEY = credentials[1]
    SESSION_TOKEN = credentials[2]

    service_response = boto3.client(
        f'{service}',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
        region_name=region
    )

    return(service_response)