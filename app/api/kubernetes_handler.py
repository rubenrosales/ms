# kubernetes_base_handler.py
from kubernetes import client, config

class KubernetesBaseHandler:
    def __init__(self, namespace):
        config.load_incluster_config()
        self.api_client = client.ApiClient()
        self.namespace = namespace

    def create_resource(self, resource_type, body):
        api_instance = self.api_client.get_api_from_resource(resource_type)
        return api_instance.create_namespaced_object(
            namespace=self.namespace,
            body=body
        )

    def delete_resource(self, resource_type, name):
        api_instance = self.api_client.get_api_from_resource(resource_type)
        return api_instance.delete_namespaced_object(
            name=name,
            namespace=self.namespace,
            body=client.V1DeleteOptions()
        )

# kubernetes_handler.py
from kubernetes import client
from kubernetes_base_handler import KubernetesBaseHandler

class KubernetesHandler(KubernetesBaseHandler):
    def __init__(self, namespace):
        super().__init__(namespace)
        self.apps_api = client.AppsV1Api(api_client=self.api_client)

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

        return self.create_resource('Deployment', deployment)

    def delete_deployment(self, name):
        return self.delete_resource('Deployment', name)


# kubernetes_job_handler.py
from kubernetes import client
from kubernetes_base_handler import KubernetesBaseHandler
class KubernetesJobHandler(KubernetesBaseHandler):
    def __init__(self, namespace):
        super().__init__(namespace)
        self.batch_api = client.BatchV1Api(api_client=self.api_client)

    def create_job(self, name, image, command, environment):
        container = client.V1Container(
            name=name,
            image=image,
            command=command,
            env=[client.V1EnvVar(name=k, value=v) for k, v in environment.items()]
        )

        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={'job': name}),
            spec=client.V1PodSpec(containers=[container], restart_policy='Never')
        )

        job_spec = client.V1JobSpec(
            template=template,
            backoff_limit=0,
            active_deadline_seconds=300
        )

        job = client.V1Job(
            api_version='batch/v1',
            kind='Job',
            metadata=client.V1ObjectMeta(name=name),
            spec=job_spec
        )
        
        return self.create_resource('Job', job)
