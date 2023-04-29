class ExampleMicroservice(MicroserviceInterface):
    def handle_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Implement microservice functionality here
        output_data = {'status': 'ok', 'data': data}
        return output_data

    def validate_input(self, data: Dict[str, Any]) -> Optional[str]:
        # Implement input validation here
        if 'input_data' not in data:
            return 'Input data is required'
        return None

    def serialize_output(self, data: Dict[str, Any]) -> str:
        # Implement output serialization here
        return json.dumps(data)
