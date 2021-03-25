import boto3
import botocore

from progress.bar import IncrementalBar

from groundhogs_day import aws_list_helper, aws_creds_helper


def enable_s3_account_block(role, accounts_list):
    """
    Function to enable AWS S3 Account-Level block
    """
    print("\nEnabling AWS S3 Account Block")
    print("==============================")
    enable_s3_account_level_blocks(role, accounts_list)


def enable_s3_account_level_blocks(role, accounts_list):
    """
    Subfunction for enabling AWS S3 Account-Level block
    """
    completed_accounts = []
    failed_accounts = []
    bar = IncrementalBar('Processing Accounts:', max = len(accounts_list))

    for account in accounts_list:

        sts_credentials = aws_creds_helper.generate_cross_account_credentials(account['AccountId'], role)
        account_session = aws_creds_helper.generate_cross_account_session(service='s3control',\
            credentials=sts_credentials, region=None)
        try:
            s3_account_block = account_session.put_public_access_block(
                AccountId=account['AccountId'],
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': True,
                    'IgnorePublicAcls': True,
                    'BlockPublicPolicy': True,
                    'RestrictPublicBuckets': True
                }
            )
        except botocore.exceptions.ClientError as e:
            print(e.response['Error']['Message'])
            failed_accounts.append(account['AccountId'])
        else:
            completed_accounts.append(account['AccountId'])
            bar.next()

    if len(completed_accounts) == len(accounts_list):
        print("\n>> SUCCESS: Successfully set S3 Account-Level Blocks in all accounts")

    else:
        print("========================================================================")
        print("ERROR: Failed to set S3 Account-Level Blocks for the following accounts:")
        print("========================================================================")
        for failed_account in failed_accounts:
            print(f"- {failed_account}")


def disable_s3_account_block(role, accounts_list):
    """
    Function to disable AWS S3 Account-Level block
    """
    print("\nDisabling AWS S3 Account Block")
    print("==============================")

    disable_s3_account_level_blocks(role, accounts_list)


def disable_s3_account_level_blocks(role, accounts_list):
    """
    Subfunction for disabling AWS S3 Account-Level block
    """
    completed_accounts = []
    failed_accounts = []
    bar = IncrementalBar('Processing', max = len(accounts_list))

    for account in accounts_list:

        sts_credentials = aws_creds_helper.generate_cross_account_credentials(account['AccountId'], role)
        account_session = aws_creds_helper.generate_cross_account_session(service='s3control', credentials=sts_credentials,
                                region=None)
        try:
            delete_response = account_session.delete_public_access_block(
                AccountId=account['AccountId']
            )
        except botocore.exceptions.ClientError as e:
            print(e.response['Error']['Message'])
            failed_accounts.append(account['AccountId'])
            raise e
        else:
            completed_accounts.append(account['AccountId'])
            bar.next()

    if len(completed_accounts) == len(accounts_list):
        print("\n SUCCESS: Successfully disabled S3 Account-Level Blocks in all accounts")

    else:
        print("========================================================================")
        print("ERROR: Failed to set S3 Account-Level Blocks for the following accounts:")
        print("========================================================================")
        for failed_account in failed_accounts:
            print(f"- {failed_account}")
