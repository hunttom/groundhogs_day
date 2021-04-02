import click

from groundhogs_day import aws_configure, aws_list_helper, aws_organizations, aws_s3, aws_vpc

"""
ghd iam [--on --off] scope [--org --account]
"""

"""
ghd guardduty [--on --off] scope [--org --account]
"""

"""
ghd securityhub [--on --off] scope [--org --account]
"""

"""
ghd config [--on --off] scope [--org --account]
"""
@click.group()
@click.option('--profile', '-p',
    default='default',
    help='Enter profile to use',
    type=str
)
@click.pass_context
def cli(ctx, profile):
    """
    Main function for CLI
    """
    aws_profile = config_profile(profile=profile)
    ctx.obj['profile'] = aws_profile

@cli.command()
@click.pass_context
def configure(ctx):
    """ghd [--profile ] configure """
    aws_profile = ctx.obj['profile']
    aws_configure.configure_cli(profile=aws_profile)

@cli.command()
@click.argument(
    'list',
    type=click.Choice(['organization', 'accounts', 'org_admins'])
    )
@click.option('--output', 
    type=click.Choice(['json', 'csv', 'table'], case_sensitive=False), default='table')
@click.option('--export',
    is_flag=True)
@click.pass_context
def list(ctx, list, output, export):
    """ghd list [organization, accounts, org_admins] [--output <json,csv,table>] [--export <csv,json>]"""

    account_list = aws_list_helper.organizations_list_accounts()

    if list == 'organization':
        # ghd list organization [--output <json,table>] --export (json)
        aws_organizations.organization_information(account_list=account_list, output_format=output, export=export)
    elif list == 'accounts':
        # ghd list accounts [--output <csv,json,table>] --export (csv,json)
        aws_organizations.account_information(data=account_list, output_format=output, export=export)
    elif list == 'org_admins':
        # ghd list org_admins [--output <csv,json,table>] --export (json)
        aws_organizations.organization_admins(output_format=output, export=export)

@cli.command()
@click.option('--on/--off', default=True)
@click.option('--target', help='Account Id for S3 Account Settings')
@click.pass_context
def s3account(ctx, on, target):
    """ghd s3account [--on --off] --target <accountid>"""
    aws_profile = ctx.obj['profile']
    config_data = aws_configure.read_profile(profile=aws_profile)
    role = config_data['aws_iam_role']
    if target:
        accounts_list = [{'Name': 'Target Account', 'AccountId': f'{target}', 'Email': 'example@mail.com'}]
    else:
        accounts_list = aws_list_helper.organizations_list_accounts()
    if on:
        aws_s3.enable_s3_account_block(role=role, accounts_list=accounts_list)
    else:
        aws_s3.disable_s3_account_block(role=role, accounts_list=accounts_list)


@cli.command()
@click.pass_context
@click.option('--target', help='Account Id for deleting default VPCs')
def vpcdelete(ctx):
    """ghd vpcdelete"""
    aws_profile = ctx.obj['profile']
    config_data = aws_configure.read_profile(profile=aws_profile)
    role = config_data['aws_iam_role']
    if target:
        accounts_list = [{'Name': 'Target Account', 'AccountId': f'{target}', 'Email': 'example@mail.com'}]
    else:
        accounts_list = aws_list_helper.organizations_list_accounts()
    aws_vpc.delete_default_vpc(role=role, accounts_list=accounts_list)


def config_profile(profile):
    if profile:
        aws_profile = profile
    else:
        aws_profile = 'default'
    return aws_profile



def main():

    cli(obj={})


if __name__ == '__main__':
    main()
