import json
import os.path
import os.remove
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
    zip_file_url = f"gs://{bucket}/{zipfile}"
    zip_folder_url = os.path.dirname(gcs_zip_file)
    print(f"Extracting {zip_file_url} to: {zip_folder_url}")
    with ZipFile(zip_file) as archive:
        for archive_item in archive.namelist():
            ext = os.path.splitext(archive_item)[1]
            if ext == ".png":
                archive_file_name = os.path.basename(archive_item)
                image_file_url = f"{zip_folder_url}/{archive_file_name}"
                with tempfile.TemporaryDirectory() as temp_dir:
                    extracted = archive.extract(archive_item, path=temp_dir)
                    print(f"Extracted {archive_item} to {extracted} -> {gcs_image_file}")
                    put_blob(bucket, image_file_url, open(temp)
            else:
                print(f"Skipping {archive_item}")

def get_blob(bucket_name, blob_name):
    """Downloads a file from a bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    file = tempfile.TemporaryFile()
    blob.download_to_file(file)
    print(f"File {blob_name} downloaded from{bucket_name} to {file.name}.")
    return file

def put_blob(bucket_name, blob_name, file):
    """Uploads a file to a bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_file(file)
    print(f"File {file.name} uploaded to {bucket_name} as {blob_name}.")
    os.remove(file)

unzip({'name': 'pS_flyers_upd_205.zip', 'bucket': 'mamecloud', 'contentType': 'application/zip'}, "")
