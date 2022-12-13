from kubernetes import client, config, utils
from kubernetes.client.exceptions import ApiException, ApiValueError
from models.job import Job, Container
from models.redis import RedisHelper
from models.monad import RedisMaybeMonad
from kubernetes.config.config_exception import ConfigException
import json, uuid, os, time

class Scheduler:

    def __init__(self):
        try:
            config.load_kube_config()
        except ConfigException:
            stream = os.popen(r'/usr/lib/google-cloud-sdk/bin/gcloud auth activate-service-account scheduler@roomr-222721.iam.gserviceaccount.com --key-file=/usr/src/app/ServiceAccount.json')
            output = stream.read()
            print(output)
            config.load_kube_config(config_file="/usr/src/app/config")
        self._api_instance = client.BatchV1Api()
        self.redis = RedisHelper()

    def job_exists(self, uuidValue):
        return str(uuidValue) in self.list_jobs().keys()
           
    def schedule(self, data):
        k8s_client = client.ApiClient()
        utils.create_from_dict(k8s_client, data)

    def schedule_job(self, image, data): 
        uuidValue = uuid.uuid4()
        uuidValue = str(uuidValue)
        if self.job_exists(uuidValue):
            scheduler.delete_job(uuidValue)
            print(f"Job with name {uuidValue} already exists")
            return uuidValue

        monad = RedisMaybeMonad(uuidValue, json.dumps(data)) \
            .bind(self.redis.set_key)
        if monad.has_errors():
            print(self.redis._redis_host)
            print(monad.error_status)
            return uuidValue

        job = Job(uuidValue)
        container = Container(image, uuidValue)
        container.add_environment_variables("REDIS_HOST", os.environ.get("REDIS_HOST", "localhost"))
        container.add_command("python")
        container.add_command("main.py")
        container.add_command(f"--key={uuidValue}")
        job.add_container(container)
        self.schedule(job.to_json())
        return uuidValue

    def schedule_maintenance_ticket_job(self, data):
        self.schedule_job("upload-service", data)

    def schedule_tenant_profile_job(self, data):
        self.schedule_job("tenant-profile-service", data)

    def schedule_landlord_profile_job(self, data):
        self.schedule_job("landlord-profile-service", data)

    def schedule_lease_ticket_job(self, data):
        self.schedule_job("generate-lease", data)

    def schedule_add_tenant_email_job(self, data):
        self.schedule_job("add-tenant-email", data)

    def schedule_sign_lease_tenant(self, data):
        self.schedule_job("sign-lease-tenant", data)
    
    def delete_job(self, jobName):
        self._api_instance.delete_namespaced_job(
            name=jobName,
            namespace="default",
            body=client.V1DeleteOptions(
                propagation_policy='Foreground',
                grace_period_seconds=5))
        
    def list_jobs(self):
        v1 = client.CoreV1Api()
        response = v1.list_pod_for_all_namespaces()
        data = {}
        for pod in response.items:
            data[pod.metadata.name[:-6]] = pod.metadata.name
        return data
       