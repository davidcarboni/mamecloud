#!/usr/bin/env bash

gcloud config set project `cat project.txt`
base=$PWD

# Update functions
cd functions && zip -r functions.zip .
gsutil -m cp -r functions.zip gs://mamecloud-functions/
rm functions.zip
cd $base

# TODO: deploy from a source repo?
gcloud functions deploy unzip-file --region=europe-west1 --runtime=python37 --source=gs://mamecloud-functions/functions.zip --memory=128MB --trigger-event=google.storage.object.finalize --trigger-resource=mamecloud-upload --entry-point=unzip

gsutil rm gs://mamecloud-upload/cabinets/test.zip
gsutil cp ~/Downloads/test.zip gs://mamecloud-upload/cabinets/test.zip
