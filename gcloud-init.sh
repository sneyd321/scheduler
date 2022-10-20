#!/bin/bash

gcloud auth activate-service-account scheduler@roomr-222721.iam.gserviceaccount.com --key-file=/usr/src/app/ServiceAccount.json
export ENV GOOGLE_APPLICATION_CREDENTIALS=/usr/src/app/ServiceAccount.json
gcloud container clusters get-credentials roomr-cluster-1 --project=roomr-222721 --region=us-central1 

cp ~/.kube/config /usr/src/app/config 