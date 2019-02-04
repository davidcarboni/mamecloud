#!/usr/bin/env bash

gcloud config set project `cat project.txt`
base=$PWD

# Update functions
cd functions && zip -r functions.zip .
#gsutil -m cp -r functions.zip gs://mame-functions-upload/
rm functions.zip
cd $base

# The buckets we want to trigger on:
declare -a buckets=(
  "zips-cabinet"
  "zips-flyer"
  "zips-controlpanel"
  "zips-snap"
)

for bucket in "${buckets[@]}"
do
  # TODO: deploy from a source repo?
  function=process-${bucket}
  echo gcloud functions deploy ${function} --region=europe-west1 --runtime=python37 --source=gs://mame-functions-upload/functions.zip --memory=128MB --trigger-bucket --trigger-resource=${bucket} --trigger-event=google.storage.object.finalize --entry-point=unzip
done
