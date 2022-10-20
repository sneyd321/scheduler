FROM google/cloud-sdk:slim

WORKDIR /usr/src/app

RUN apt-get install google-cloud-sdk-gke-gcloud-auth-plugin
RUN apt-get install kubectl

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN sh gcloud-init.sh
ENV PORT=$PORT
ENV REDIS_HOST=localhost
ENV GOOGLE_APPLICATION_CREDENTIALS /usr/src/app/service_key.json


#CMD python main.py
CMD uvicorn main:app --host 0.0.0.0 --workers 1 --port $PORT

