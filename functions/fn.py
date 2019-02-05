import json
import os.path
import tempfile
from zipfile import ZipFile

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

def process(bucket, zipfile):
    """ Extracts a zip file
    Extracted files are placed into the same folder as the zip file itself.
    Any path information is discarded (zips often contain a folder, e.g. 'snap' or 'title')
    """
    print("It's a zip. Unpacking...")
    gcs_zip_file = f"gs://{bucket}/{zipfile}"
    gcs_zip_folder = f"gs://{bucket}/{zipfile}/" + os.path.dirname(gcs_zip_file)
    print(f"Extracting to: {gcs_zip_folder}")
    with ZipFile(zipfile) as zip_file:
        for zip_item in zip_file.namelist():
            stem, ext = os.path.splitext(zip_item)
            if ext == ".png":
                file_name = os.path.basename(zip_item)
                gcs_image_file = f"{gcs_zip_folder}/{file_name}"
                with tempfile.TemporaryDirectory() as temp_dir:
                    extracted = zip_file.extract(zip_item, path=temp_dir)
                    print(f"Extracted {zip_item} to {extracted} -> {gcs_image_file}")
            else:
                print(f"Skipping {zip_item}")

unzip({'name': 'pS_flyers_upd_205.zip', 'bucket': 'myBucket', 'contentType': 'application/zip'}, "")
