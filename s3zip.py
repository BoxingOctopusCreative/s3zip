import os
import zipfile

import boto3
import click

@click.command()
@click.option("-b", "--bucket",     envvar="BUCKET_NAME",           help="S3 bucket name")
@click.option("-r", "--region",     envvar="AWS_REGION",            help="AWS region")
@click.option("-c", "--config",     envvar="AWS_CONFIG_FILE",       help="AWS configuration file path")
@click.option("-a", "--access-key", envvar="AWS_ACCESS_KEY_ID",     help="AWS access key ID")
@click.option("-s", "--secret-key", envvar="AWS_SECRET_ACCESS_KEY", help="AWS secret access key")
@click.option("-o", "--output",     envvar="OUTPUT_FILE",           help="Output file name", default="archive.zip")
def main(bucket, region, config, access_key, secret_key, output):
    # Get values from environment variables if not provided as command-line arguments.
    if not bucket:
        bucket = os.environ.get("BUCKET_NAME")
    if not region:
        region = os.environ.get("AWS_REGION")
    if not config:
        config = os.environ.get("AWS_CONFIG_FILE")
    if not access_key:
        access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    if not secret_key:
        secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    # Initialize the AWS session and S3 client.
    if config:
        # Use the AWS configuration file.
        session = boto3.Session(profile_name="default", region_name=region, 
                                config=boto3.session.Config(
                                    region_name=region, 
                                    signature_version="s3v4"
                                ), 
                                shared_config_file=config)
    else:
        # Use the AWS access key and secret access key.
        session = boto3.Session(region_name=region, 
                                aws_access_key_id=access_key, 
                                aws_secret_access_key=secret_key, 
                                config=boto3.session.Config(signature_version="s3v4"))
    s3 = session.resource("s3")

    # Create a new zip file to archive the S3 objects.
    with zipfile.ZipFile(output, "w") as zip_file:
        # List all objects in the S3 bucket.
        bucket = s3.Bucket(bucket)
        for object in bucket.objects.all():
            # Download the S3 object.
            object_data = object.get()

            # Add the S3 object to the zip file.
            zip_file.writestr(os.path.basename(object.key), object_data["Body"].read())

    print(f"Successfully created {output}")

if __name__ == "__main__":
    main()
