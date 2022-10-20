FROM google/cloud-sdk:slim

WORKDIR /usr/src/app

RUN apt-get install google-cloud-sdk-gke-gcloud-auth-plugin
RUN apt-get install kubectl

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN gcloud auth activate-service-account scheduler@roomr-222721.iam.gserviceaccount.com --key-file=/usr/src/app/ServiceAccount.json
RUN gcloud container clusters get-credentials roomr-cluster-1 --project=roomr-222721 --region=us-central1 
ENV PORT=$PORT
ENV REDIS_HOST=localhost
ENV GOOGLE_APPLICATION_CREDENTIALS /usr/src/app/service_key.json


#CMD python main.py
CMD uvicorn main:app --host 0.0.0.0 --workers 1 --port $PORT

