#!/usr/bin/env bash

gcloud config set project `cat project.txt`
base=$PWD

# Update functions
cd functions && zip -r functions.zip .
#gsutil -m cp -r functions.zip gs://mamecloud-functions/
rm functions.zip
cd $base

# The buckets we want to trigger on:
declare -a buckets=(
  "mamecloud"
)

for bucket in "${buckets[@]}"
do
  # TODO: deploy from a source repo?
  function=unzip
  echo gcloud functions deploy ${function} --region=europe-west1 --runtime=python37 --source=gs://mamecloud-functions/functions.zip --memory=128MB --trigger-bucket --trigger-resource=${bucket} --trigger-event=google.storage.object.finalize --entry-point=unzip
done
