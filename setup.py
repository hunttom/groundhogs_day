from setuptools import setup
setup(
    name = 'ghd',
    packages = ['groundhogs_day'],
    version = '0.1.0',
    description='A best practices cli for AWS actions',
    author='tomhunte',
    url='https://github.com/hunttom', # To be updated
    author_email='hunter@grissom.xyz',
    download_url='https://github.com/hunttom', # To be updated
    keywords=['aws', 'python'],
    classifiers=[],
    install_requires=[
        "argparse",
        "boto3",
        "botocore",
        "configparser",
        "click",
        "tabulate",
        "progress"
    ],
    setup_requires=[],
    tests_require=[],
    entry_points = {
        'console_scripts': [
            'ghd = groundhogs_day.__main__:main',
        ],
    },
)
