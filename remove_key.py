import json, os

with open("./ServiceAccount.json") as serviceAccount:
    key = json.load(serviceAccount)

os.system(f"gcloud iam service-accounts keys delete {key['private_key_id']} --iam-account=scheduler@roomr-222721.iam.gserviceaccount.com --quiet")  

