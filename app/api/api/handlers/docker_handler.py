import docker

class DockerHandler:
    """
    A class for interacting with the Docker API.

    Attributes:
        client (docker.client.DockerClient): A client object for communicating with the Docker daemon.

    Methods:
        __init__(): Initializes a new DockerHandler object.
        create_container(name: str, image: str, command: str, environment: dict) -> docker.models.containers.Container:
            Create and run a new container from the given image with the specified name, command, and environment variables.
        delete_container(name: str) -> None:
            Stops and removes a container with the given name.
    """

    def __init__(self):
        """
        Initializes a new DockerHandler object.

        The DockerHandler object contains a DockerClient instance for communicating with the Docker daemon.
        """
        self.client = docker.from_env()

    def create_container(self, name: str, image: str, command: str, environment: dict) -> docker.models.containers.Container:
        """
        Create and run a new container from the given image with the specified name,
        command, and environment variables.

        Args:
            name (str): The name to assign to the new container.
            image (str): The name of the Docker image to use.
            command (str): The command to run inside the new container.
            environment (dict): A dictionary of environment variable names and values.

        Returns:
            docker.models.containers.Container: A reference to the newly created container.
        """
        return self.client.containers.run(
            image=image,
            name=name,
            command=command,
            detach=True,
            environment=environment
        )

    def delete_container(self, name: str) -> None:
        """
        Stops and removes a container with the given name.

        Args:
            name (str): The name of the container to delete.

        Raises:
            docker.errors.NotFound: If no container exists with the given name.
        """
        try:
            container = self.client.containers.get(name)
            container.stop()
            container.remove()
        except docker.errors.NotFound as e:
            raise e
