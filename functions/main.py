import json
import os
import tempfile
from zipfile import ZipFile
from google.cloud import storage

def unzip(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    file = event
    name = file.get('name')
    bucket = file.get('bucket')
    content_type = file.get('contentType')
    print(f"Notified of file: {name} in bucket {bucket} of type {content_type}.")
    if bucket and name and content_type and content_type == 'application/zip':
        process(bucket, name)
    else:
        print(f"That doesn't seem like something that should be processed. Skipping this file.")
        print(json.dumps(file))

def process(bucket, zip_file):
    """ Extracts a zip file
    Extracted files are placed into the same folder as the zip file itself.
    Any path information is discarded (zips often contain a folder, e.g. 'snap' or 'title')
    """
    print("It's a zip. Unpacking...")
    zip_file_url = f"gs://{bucket}/{zip_file}"
    zip_folder = os.path.dirname(zip_file)
    print(f"Extracting {zip_file_url} to: {zip_folder}")
    downloaded = get_blob(bucket, zip_file)
    try:
        with ZipFile(downloaded) as archive:
            for archive_item in archive.namelist():
                ext = os.path.splitext(archive_item)[1]
                if ext == ".png":
                    archive_file_name = os.path.basename(archive_item)
                    image_file_url = f"{zip_folder}/{archive_file_name}"
                    with tempfile.TemporaryDirectory() as temp_dir:
                        extracted_path = archive.extract(archive_item, path=temp_dir)
                        print(f"Extracted {archive_item} to {extracted_path} -> {image_file_url}")
                        put_blob(bucket, image_file_url, extracted_path)
                        print(f'Uploaded {image_file_url} to bucket {bucket}')
                else:
                        print(f"Skipping {archive_item}")
    finally:
        delete_blob(bucket, zip_file)

def get_blob(bucket_name, blob_name):
    """Downloads a file from a bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    file = tempfile.TemporaryFile()
    blob.download_to_file(file)
    print(f"File {blob_name} downloaded from{bucket_name} to {file.name}.")
    return file

def put_blob(bucket_name, blob_name, file_name):
    """Uploads a file to a bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(file_name)
    print(f"File {file_name} uploaded to {bucket_name} as {blob_name}.")
    os.remove(file_name)

def delete_blob(bucket_name, blob_name):
    """Uploads a file to a bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()
    print(f"File {blob_name} deleted flom {bucket_name}.")

if __name__ == '__main__':
    unzip({'name': 'pS_flyers_upd_205.zip', 'bucket': 'mamecloud', 'contentType': 'application/zip'}, "")
