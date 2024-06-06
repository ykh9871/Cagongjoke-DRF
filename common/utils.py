import os

import boto3
import pandas as pd
from io import BytesIO

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")


def get_data_from_s3(bucket_name, file_key):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_S3_REGION_NAME,
    )
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    data = obj["Body"].read()
    return data


def get_dataframe_from_s3(bucket_name, file_key):
    data = get_data_from_s3(bucket_name, file_key)
    return pd.read_parquet(BytesIO(data))
