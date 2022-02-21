import logging
import os

import boto3
from botocore.exceptions import ClientError


def s3_client(s3_key, s3_secret):
    session = boto3.session.Session(
        aws_access_key_id=s3_key,
        aws_secret_access_key=s3_secret,
        region_name="eu-west-1",
    )
    client = session.client("s3")
    return client


def upload_file(s3_key, s3_secret, file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    try:
        s3_client(s3_key, s3_secret).upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_file(s3_key, s3_secret, file_name, bucket):
    try:
        s3_client(s3_key, s3_secret).download_file(bucket, file_name, f"temp/{file_name}")
    except ClientError as e:
        logging.error(e)
        return False
    return True
