import boto3, botocore
from progress.bar import IncrementalBar

from groundhogs_day import aws_creds_helper, aws_list_helper

def delete_default_vpc(session, vpc_id):
    """
    Deletes all the resources in default VPC in all AWS regions and then deletes default VPC in all the regions.
    :return: Prints output of VPC deletion to console
    """
    try:
        session.delete_vpc(
            VpcId=vpc_id
        )
    except Exception as e:
        print('Exception: ' + str(e))
    else:
        print("Successfully deleted VPC")


def delete_default_vpc(role, accounts_list):
    """
    Function to delete the default vpcs in all account
    """
    print("\nDeleting all default VPCs")
    print("==============================")

    completed_accounts = []
    bar = IncrementalBar('Processing Accounts:', max = len(accounts_list))
    regions = aws_list_helper.organizations_list_service_regions('ec2')
    for account in accounts_list:
        print(f'\nRemoving Default VPCs from: {account["Name"]}')

        sts_credentials = aws_creds_helper.generate_cross_account_credentials(account['AccountId'], role)

        for region in regions:
            try:
                regional_session = aws_creds_helper.generate_cross_account_session(service='ec2',\
                    credentials=sts_credentials, region=region)

                awsVPCs = regional_session.describe_vpcs(Filters = [{'Name': 'isDefault','Values': ['true',]},])
                igw = regional_session.describe_internet_gateways()
                subnets = regional_session.describe_subnets()

                # iterate over VPC to find Default VPC
                if awsVPCs['Vpcs']:
                    # iterate over VPC to find Default VPC
                    for vpcAttributes in awsVPCs['Vpcs']:
                        # check if VPC is Default VPC
                        if vpcAttributes['IsDefault']:
                            ec2 = boto3.resource('ec2',
                                                 region_name=region,
                                                 aws_access_key_id=sts_credentials[0],
                                                 aws_secret_access_key=sts_credentials[1],
                                                 aws_session_token=sts_credentials[2])

                            # Checks if there are any subnets
                            if subnets['Subnets']:
                                # Delete subnets in Default VPC
                                for subnet in subnets['Subnets']:
                                    # check if Subnets belong to Default VPC
                                    if subnet['VpcId'] == vpcAttributes['VpcId']:
                                        subnetId = ec2.Subnet(subnet['SubnetId'])
                                        print("\tAbout to delete Subnet Id: " + str(subnetId))
                                        subnetId.delete()

                            # detach and delete IGW (Internet Gateway) in Default VPC
                            # check if IGW exists
                            for _ in igw['InternetGateways']:
                                try:
                                    IGWid = igw['InternetGateways'][0]['InternetGatewayId']
                                    IGWisAttached = igw['InternetGateways'][0]['Attachments'][0]['State']
                                    IGWattachedToVPC = igw['InternetGateways'][0]['Attachments'][0]['VpcId']
                                except Exception as e:
                                    IGWisAttached = ''
                                    IGWattachedToVPC = ''
                                # check if IGW atatched to VPC and VPC is Default VPC
                                if IGWisAttached == 'available' and IGWattachedToVPC == vpcAttributes['VpcId']:
                                    internet_gateway = ec2.InternetGateway(
                                        igw['InternetGateways'][0]['InternetGatewayId'])
                                    print("\tAbout to detach and delete internet_gateway =" + str(internet_gateway))
                                    internet_gateway.detach_from_vpc(VpcId=vpcAttributes['VpcId'])
                                    internet_gateway.delete()

                            # delete Default VPC
                            regional_session.delete_vpc(VpcId=vpcAttributes['VpcId'], DryRun=False)
                            print("\t The detault VPC ID = " + str(vpcAttributes['VpcId']) + " is being deleted in " + str(
                                region))
            except botocore.exceptions.ClientError as err:
                if err.response['Error']['Code'] == 'AuthFailure':
                    print(f'\tThe region: {region} is not enabled')
            except Exception as e:
                print(f'\nException: {str(e)}\n')
