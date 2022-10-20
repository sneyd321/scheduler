FROM google/cloud-sdk:alpine

WORKDIR /usr/src/app

RUN gcloud components install gke-gcloud-auth-plugin
RUN gcloud components install kubectl

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN sh gcloud-init.sh
ENV PORT=$PORT
ENV REDIS_HOST=localhost

#CMD python main.py
CMD uvicorn main:app --host 0.0.0.0 --workers 1 --port $PORT

