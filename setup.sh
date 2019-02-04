#!/usr/bin/env bash

PROJECT=`cat project.txt`
STORAGE_CLASS=multi_regional
LOCATION=eu

# The buckets we want
declare -a buckets=(
  "mame-functions-upload"
  "mame-store"
  "zips-cabinet"
  "zips-flyer"
  "zips-controlpanel"
  "zips-snap"
)

for bucket in "${buckets[@]}"
do
   gsutil mb -p $PROJECT -c $STORAGE_CLASS -l $LOCATION gs://${bucket}/
done

gsutil ls
