FROM python:3.9

# Install dependencies
RUN pip install --upgrade pip && \
    pip install boto3 click

# Copy the code to the container
COPY s3_archiver.py /app/s3_archiver.py

# Set the working directory
WORKDIR /app

# Run the script
CMD ["python", "s3_archiver.py"]