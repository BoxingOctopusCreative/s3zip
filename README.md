# s3zip

`s3zip` is a command-line utility that downloads the contents of an S3 bucket and archives it to a ZIP file. It uses the `boto3` library to interact with the S3 service and the `click` library to provide a user-friendly command-line interface.

## Installation

`s3zip` can be installed using pip:

```
pip install s3zip
```

## Usage

```
Usage: s3zip [OPTIONS]

  Downloads the contents of an S3 bucket and archives it to a ZIP file.

Options:
  -b, --bucket TEXT          S3 bucket name  [required]
  -r, --region TEXT          AWS region  [required]
  -c, --config TEXT          AWS configuration file path
  -a, --access-key TEXT      AWS access key ID
  -s, --secret-key TEXT      AWS secret access key
  -o, --output TEXT          Output file name  [default: archive.zip]
  --help                     Show this message and exit.
```

To use `s3zip`, simply provide the required options `bucket` and `region`:

```
s3zip --bucket my-bucket --region us-west-2
```

You can also specify the AWS configuration file path, access key ID, and secret access key using the `config`, `access-key`, and `secret-key` options, respectively:

```
s3zip --bucket my-bucket --region us-west-2 --config ~/.aws/config --access-key AKI1234567890 --secret-key abcdef1234567890
```

By default, `s3zip` will create a file named `archive.zip` in the current directory. You can specify a different output file name using the `output` option:

```
s3zip --bucket my-bucket --region us-west-2 --output my-archive.zip
```

You can also set the values of these options using environment variables. The option names are converted to uppercase and prefixed with `S3ZIP_`. For example, you can set the S3 bucket name using the `S3ZIP_BUCKET` environment variable:

```
export S3ZIP_BUCKET=my-bucket
s3zip --region us-west-2
```

## Docker

`s3zip` can also be used as a Docker container. To build the Docker image:

```
docker build -t s3zip .
```

To run the container:

```
docker run --rm -e S3ZIP_BUCKET=my-bucket -e S3ZIP_REGION=us-west-2 s3zip
```

Replace `my-bucket` and `us-west-2` with the appropriate values.

## License

`s3zip` is licensed under the Mozilla Public License v2.0. See `LICENSE` for more information.
