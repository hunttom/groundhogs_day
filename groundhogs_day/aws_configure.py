import os

try:
    import configparser
except:
    import ConfigParser as configparser

def config_checker(config, profile, variable):
    if config[profile][variable]:
        return config[profile][variable]
    else:
        return "None"

def configure_cli(profile):
    config = configparser.ConfigParser()

    config_file = os.path.join(os.path.expanduser('~'),
                            '.aws',
                            'ghd_config')
    if os.path.exists(config_file):
        config.read(config_file)

    else:
        try:
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except FileExistsError:
            print(f'Failed to create config file at: {config_file}')
        else:
            config.read("config_file")
    try:
        config[profile]
    except KeyError:
        config.add_section(profile)

    try:
        region = config_checker(config=config, profile=profile, variable='aws_region')
    except Exception:
        region = ''

    try:
        account = config_checker(config=config, profile=profile, variable='aws_security_account')
    except Exception:
        account = ''

    try:
        role = config_checker(config=config, profile=profile, variable='aws_iam_role')
    except Exception:
        role = ''
    aws_security_account = input(f"Organization security account: [{account}]")
    aws_region = input(f"Default region name: [{region}]")
    aws_iam_role = input(f"Organizational role: [{role}]")

    if aws_region:
        config.set(profile, 'aws_region', aws_region)
    if aws_security_account:
        config.set(profile, 'aws_security_account', aws_security_account)
    if aws_iam_role:
        config.set(profile, 'aws_iam_role', aws_iam_role)

    with open(config_file, 'w') as configfile:
        config.write(configfile)

def read_profile(profile):
    config = configparser.ConfigParser()

    config_file = os.path.join(os.path.expanduser('~'),
                            '.aws',
                            'ghd_config')
    if os.path.exists(config_file):
        config_data = {}
        config.read(config_file)
        configuration = config[profile]
        config_data['aws_region'] = configuration['aws_region']
        config_data['aws_security_account'] = configuration['aws_security_account']
        config_data['aws_iam_role'] = configuration['aws_iam_role']

        return(config_data)

    else:
        print(f'Failed to read config file at: {config_file}')
