import os
import tempfile
import zipfile
from unittest import mock

import boto3
import pytest

from s3zip import archive_bucket


@pytest.fixture(scope='module')
def s3_client():
    return boto3.client('s3', region_name='us-west-2')


@pytest.fixture(scope='module')
def s3_bucket(s3_client):
    bucket_name = 'test-bucket'
    s3_client.create_bucket(Bucket=bucket_name)

    yield bucket_name

    s3_client.delete_bucket(Bucket=bucket_name)


@pytest.fixture(scope='module')
def s3_object(s3_client, s3_bucket):
    object_key = 'test-object'
    s3_client.put_object(Bucket=s3_bucket, Key=object_key, Body=b'This is a test')

    yield object_key

    s3_client.delete_object(Bucket=s3_bucket, Key=object_key)


def test_archive_bucket(s3_client, s3_bucket, s3_object):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        archive_bucket(bucket_name=s3_bucket, region='us-west-2', output_file=f.name)

        assert os.path.exists(f.name)

        with zipfile.ZipFile(f.name) as zip_file:
            assert s3_object in zip_file.namelist()

    os.unlink(f.name)


@mock.patch('boto3.client')
def test_archive_bucket_with_credentials(mock_s3_client, s3_bucket, s3_object):
    mock_client = mock.MagicMock()
    mock_client.get_paginator.return_value.paginate.return_value = [{
        'Contents': [{'Key': s3_object}]
    }]
    mock_s3_client.return_value = mock_client

    with tempfile.NamedTemporaryFile(delete=False) as f:
        archive_bucket(bucket_name=s3_bucket, region='us-west-2',
                       access_key='fake-access-key', secret_key='fake-secret-key', output_file=f.name)

        assert os.path.exists(f.name)

        with zipfile.ZipFile(f.name) as zip_file:
            assert s3_object in zip_file.namelist()

    os.unlink(f.name)
