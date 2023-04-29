# kubernetes_handler.py
from kubernetes import client, config

class KubernetesHandler:
    def __init__(self, namespace):
        config.load_incluster_config()
        self.api_client = client.ApiClient()
        self.core_api = client.CoreV1Api(api_client=self.api_client)
        self.apps_api = client.AppsV1Api(api_client=self.api_client)
        self.namespace = namespace

    def create_deployment(self, name, image, command, environment):
        container = client.V1Container(
            name=name,
            image=image,
            command=command,
            env=[client.V1EnvVar(name=k, value=v) for k, v in environment.items()]
        )

        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={'app': name}),
            spec=client.V1PodSpec(containers=[container])
        )

        spec = client.V1DeploymentSpec(
            replicas=1,
            selector=client.V1LabelSelector(match_labels={'app': name}),
            template=template
        )

        deployment = client.V1Deployment(
            api_version='apps/v1',
            kind='Deployment',
            metadata=client.V1ObjectMeta(name=name),
            spec=spec
        )

        return self.apps_api.create_namespaced_deployment(
            namespace=self.namespace,
            body=deployment
        )

    def delete_deployment(self, name):
        return self.apps_api.delete_namespaced_deployment(
            name=name,
            namespace=self.namespace,
            body=client.V1DeleteOptions()
        )

# docker_handler.py
import docker

class DockerHandler:
    def __init__(self):
        self.client = docker.from_env()

    def create_container(self, name, image, command, environment):
        return self.client.containers.run(
            image=image,
            name=name,
            command=command,
            detach=True,
            environment=environment
        )

    def delete_container(self, name):
        container = self.client.containers.get(name)
        container.stop()
        container.remove()
