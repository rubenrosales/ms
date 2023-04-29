from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class Microservice(ABC):
    @abstractmethod
    def handle_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming request data and return response data.

        Args:
            data: A dictionary of input data for the microservice.

        Returns:
            A dictionary of output data from the microservice.
        """
        pass


    def validate_input(self, data: Dict[str, Any]) -> Optional[str]:
        """
        Validate input data for the microservice.

        Args:
            data: A dictionary of input data for the microservice.

        Returns:
            None if input is valid, or an error message string if input is invalid.
        """
        return None

    def serialize_output(self, data: Dict[str, Any]) -> str:
        """
        Serialize output data to a string format.

        Args:
            data: A dictionary of output data from the microservice.

        Returns:
            A string representation of the output data.
        """
        return str(data)
