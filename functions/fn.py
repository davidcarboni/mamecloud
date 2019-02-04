import json
from zipfile import ZipFile

def unzip(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    file = event
    print(f"Processing file: {file['name']} from {file['bucket']}.")
    if file.get('contentType') == 'application/zip':
        print("It's a zip")
    else:
        print(f"not a zip: {file['contentType']}")
    print(json.dumps(file))

unzip({'name': 'myzip.zip', 'bucket': 'myBucket', 'contentType': 'application/zip'}, "")
