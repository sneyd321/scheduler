




class Job:
    
    def __init__(self, name):
        self.apiVersion = "batch/v1"
        self.kind = "Job"
        self.metadata = Metadata(name)
        self.jobSpec = JobSpec()

    def to_json(self):
        return {
            "apiVersion": self.apiVersion,
            "kind": self.kind,
            "metadata": self.metadata.to_json(),
            "spec": self.jobSpec.to_json()
        }

    def add_container(self, container):
        self.jobSpec.template.templateSpec.add_container(container)
  


class Metadata:

    def __init__(self, name):
        self.name = name

    def to_json(self):
        return {
            "name": self.name
        }

class JobSpec:

    def __init__(self):
        self.template = Template()
        self.ttlSecondsAfterFinished = 100

    def to_json(self):
        return {
            "template": self.template.to_json(),
            "ttlSecondsAfterFinished": self.ttlSecondsAfterFinished
        }

class Template:

    def __init__(self):
        self.templateSpec = TemplateSpec()

    def to_json(self):
        return {
            "spec": self.templateSpec.to_json()
        }


class TemplateSpec:

    def __init__(self):
        self.containers = []
        self.restartPolicy = "Never"

    def add_container(self, container):
        self.containers.append(container)

    def to_json(self):
        return {
            "containers": [container.to_json() for container in self.containers],
            "restartPolicy": self.restartPolicy
        }

    
    
class Container:

    def __init__(self, image, name):
        self.commands = []
        self.image = f"us-central1-docker.pkg.dev/roomr-222721/roomr-docker-repo/{image}:latest"
        self.name = name
        self.environmentVariables = []
        self.resources = Resources()
        
        

    def add_command(self, command):
        self.commands.append(command)

    def add_environment_variables(self, key, value):
        self.environmentVariables.append({"name": key, "value": value})

    def to_json(self):
        return {
            "command": self.commands,
            "image": self.image,
            "name": self.name,
            "env": self.environmentVariables,
            "resources": self.resources.to_json()
        }

class Resources:
    
    def __init__(self):
        self.request = Request("250m", "64Mi")
        self.limit = Limit("500m", "128Mi")

    def to_json(self):
        return {
            "requests": self.request.to_json(),
            "limit": self.limit.to_json()
        }

class Limit:

    def __init__(self, cpu, memory):
        self.cpu = cpu
        self.memory = memory

    def to_json(self):
        return {
            "cpu": self.cpu,
            "memory": self.memory
        }

class Request:
    def __init__(self, cpu, memory):
        self.cpu = cpu
        self.memory = memory

    def to_json(self):
        return {
            "cpu": self.cpu,
            "memory": self.memory
        }