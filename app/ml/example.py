# add relevant imports here
import json
from typing import Any, Dict, Optional
from example import MicroService
#Add class that creates http endpoint that listens for incoming events
class ExampleMicroservice(MicroService):
    def handle_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Implements microservice functionality.
        """
        response_data = {'status': 'ok', 'data': request_data}
        return response_data

    def validate_input(self, data: Dict[str, Any]) -> Optional[str]:
        """Validate input data.

        Args:
            data (Dict[str, Any]): A dictionary of input data.

        Returns:
            Optional[str]: Returns None if input data is valid, else a string
            explaining the validation error.
        """
        if 'input_data' not in data:
            return 'Input data is required'
        return None


    def serialize_output(self, data: Dict[str, Any]) -> str:
        """Serialize the given dictionary data into a JSON string.

        Args:
            data: A dictionary of data to be serialized.

        Returns:
            A JSON string representing the serialized data.

        Raises:
            TypeError: If data is not a dictionary.
            ValueError: If data cannot be serialized as JSON.
        """
        return json.dumps(data)
