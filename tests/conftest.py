import moto
import pytest
import json
import pandas as pd
import os
import boto3

@pytest.fixture(scope="module")
def test_dataframe():
    return pd.read_csv('./test_data/MOCK_DATA.csv')

@pytest.fixture(scope="module")
def test_obfurscated_dataframe():
    return pd.read_csv('./test_data/MOCK_DATA_OBF.csv')

@pytest.fixture(scope="module")
def input_json():
    return json.dumps({"file_to_obfuscate" : "s3://gdpr_test_bucket/test_file.csv", "pii_fields": ["name", "email"]})

@pytest.fixture(scope="module")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"

@pytest.fixture(scope="module")
def aws(aws_credentials):
    with moto.mock_aws(aws_credentials):
        yield boto3.client("s3", region_name="eu-west-2")

@pytest.fixture(scope="module")
def create_bucket(aws):
    boto3.client("s3").create_bucket(Bucket="gdpr-test-bucket", CreateBucketConfiguration={'LocationConstraint':'eu-west-2'})

@pytest.fixture(scope="module")
def add_files_to_bucket(aws):
    boto3.client("s3").put_object(Body="./test_data/MOCK_DATA.csv", Bucket="gdpr-test-bucket", Key="mock_data.csv")