FROM google/cloud-sdk:latest

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN sh gcloud-init.sh
ENV PORT=$PORT
ENV REDIS_HOST=localhost

#CMD python main.py
CMD uvicorn main:app --host 0.0.0.0 --workers 1 --port $PORT

