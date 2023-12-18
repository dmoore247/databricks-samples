# Databricks notebook source
import boto3

# Create a client using the default profile in the .aws/credentials file
client = boto3.client('sts')

# Get the account ID associated with the instance profile
response = client.get_caller_identity()

# Print the account ID
print(response['Account'])

# UC Shared compute: NoCredentialsError: Unable to locate credentials
# Assigned cluster: 980002020202
# Serverless: NoCredentialsError: Unable to locate credentials
# job cluster w/o instance profile: NoCredentialsError: Unable to locate credentials
# job cluster w/ instance profile:

# COMMAND ----------
