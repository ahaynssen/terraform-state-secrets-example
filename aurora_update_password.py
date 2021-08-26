#!/usr/env/bin python3

import argparse
import boto3
import secrets
import string
import time

parser = argparse.ArgumentParser(description='Override Terraform password')
parser.add_argument('--db_identifier', type=str, required=True, help="RDS DB instance identifier")
parser.add_argument('--secret_name', type=str, default='db_password', required=False, help="Name for SSM Parameter")
parser.add_argument('--region', type=str, default='us-east-1', required=False, help="AWS region name")
args = parser.parse_args()


def generate_password(string_length=10):
    """Generate a secure random string of letters, digits and special characters """
    password_characters = string.ascii_letters + string.digits + "!#$%^&*()"
    return ''.join(secrets.choice(password_characters) for i in range(string_length))


db_id = args.db_identifier
db_password = generate_password(16)
secret_name = args.secret_name
region = args.region

rds = boto3.client('rds', region_name=region)
db = rds.describe_db_clusters(DBClusterIdentifier=db_id)
while rds.describe_db_clusters(DBClusterIdentifier=db_id)["DBClusters"][0]["Status"] != "available":
    time.sleep(3)
response = rds.modify_db_cluster(DBClusterIdentifier=db_id, MasterUserPassword=db_password, ApplyImmediately=True)
if response:
    print(f"Updated RDS password for {db_id}")

ssm = boto3.client('ssm', region_name=region)
ssm.put_parameter(
    Name=secret_name,
    Description=f'DB Password for {db_id}',
    Type='SecureString',
    Value=db_password,
    Overwrite=True
)