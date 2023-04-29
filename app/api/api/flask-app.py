import os
import json
import docker
from flask import Flask, request
from base_response import BaseResponse, JSONResponse, CloudEventResponse
from kubernetes_handler import KubernetesHandler
from docker_handler import DockerHandler

# Load config from file
with open('config.json', 'r') as f:
    config = json.load(f)

app = Flask(__name__)
client = docker.from_env()
kubernetes_handler = KubernetesHandler()
docker_handler = DockerHandler()


def validate_data(data):
    # Validate input arguments
    if 'image' not in data:
        return 'Image is required', 400

    # Add more validation logic as needed

    return None, None


def create_container(data):
    # Extract container creation parameters
    image = data['image']
    container_name = data.get('container_name', f'{image}-container')
    command = data.get('command', config.get('default_command', 'bash'))
    environment = data.get('environment', {})

    # Try to create container using Docker
    try:
        container = docker_handler.create_container(image, container_name, command, environment)
        response_data = f'Container {container_name} created successfully'
        status_code = 200
        return container, response_data, status_code
    except:
        pass

    # Try to create resource using Kubernetes
    try:
        resource = kubernetes_handler.create_resource(image, container_name, command, environment)
        response_data = f'Resource {container_name} created successfully'
        status_code = 200
        return resource, response_data, status_code
    except:
        pass

    # Return error response if creation failed
    response_data = 'Error creating container or resource'
    status_code = 500
    return None, response_data, status_code


def from_http(headers, data):
    content_type = headers.get('content-type', '').lower()
    if 'application/json' in content_type:
        return json.loads(data.decode('utf-8'))
    elif 'application/cloudevents+json' in content_type:
        ce_data = json.loads(data.decode('utf-8'))
        if 'data' in ce_data:
            return ce_data['data']
    return {}

@app.route('/', methods=['POST'])
def handle_event():
    # Parse CloudEvent or JSON request
    event = from_http(request.headers, request.get_data())

    # Extract data from event
    if event['datacontenttype'] == 'application/json':
        data = event['data']
    else:
        data = {}

    # Validate input arguments
    error_response, status_code = validate_data(data)
    if error_response is not None:
        return error_response, status_code

    # Create container or resource
    resource, response_data, status_code = create_container(data)

    # Return a response
    response_type = request.headers.get("Response-Type", config.get('default_response_type', 'json'))
    response_data = {"status": "ok", "data": data}
    if response_type == "cloudevent":
        response = CloudEventResponse(response_data).get_response()
    else:
        response = JSONResponse(response_data).get_response()
    return response


if __name__ == '__main__':
    app.run(debug=config.get('debug', False), host=config.get('host', '0.0.0.0'), port=config.get('port', 8080))
