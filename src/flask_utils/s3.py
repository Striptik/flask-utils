import logging
import os

import boto3
from botocore.exceptions import ClientError

from config import AWS_S3_KEY, AWS_S3_SECRET


def s3_client():
    session = boto3.session.Session(
        aws_access_key_id=AWS_S3_KEY,
        aws_secret_access_key=AWS_S3_SECRET,
        region_name="eu-west-1",
    )
    client = session.client("s3")
    return client


def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    try:
        s3_client().upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_file(file_name, bucket):
    try:
        s3_client().download_file(bucket, file_name, f"temp/{file_name}")
    except ClientError as e:
        logging.error(e)
        return False
    return True
