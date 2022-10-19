FROM google/cloud-sdk:latest

WORKDIR /usr/src/app

#COPY requirements.txt requirements.txt
#RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN gcloud auth activate-service-account scheduler@roomr-222721.iam.gserviceaccount.com --key-file=/usr/src/app/ServiceAccount.json
RUN gcloud container clusters get-credentials roomr-cluster-1 --project=roomr-222721 --region=us-central1

ENV PORT=8084

#CMD python main.py
CMD uvicorn main:app --host 0.0.0.0 --workers 1 --port $PORT

