from abc import ABC, abstractmethod
from flask import jsonify
from cloudevents.sdk import (
    converters,
    CloudEvent,
)

class BaseResponse(ABC):
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def get_response(self):
        pass
        
class JSONResponse(BaseResponse):
    def get_response(self):
        return jsonify(self.data)

class CloudEventResponse(BaseResponse):
    def get_response(self):
        event = CloudEvent(
            source="my-source",
            type="my-event-type",
            data=self.data,
            datacontenttype="application/json",
        )
        headers, body = converters.to_binary(event)
        return body, headers
