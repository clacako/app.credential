from django.conf import settings
from urllib.parse import urlencode
import requests

class Credential():
    def __init__(self, endpoint, payload=None, *args, **kwargs):
        self.__endpoint = endpoint
        self.__payload  = payload
        
        # if kwargs:
        #     settings.HEADERS_API["token"]   = kwargs["token"] if "token" in kwargs else None
    
    def __request(self, method, payload=None):
        response = requests.request(
            method,
            "{}{}".format(settings.HOST_API_CREDENTIAL, self.__endpoint),
            headers = settings.HEADERS_API_CREDENTIAL,
            data    = payload
        ).json()
        
        return response
    
    def get(self):
        self.response   = self.__request(method="GET")
        self.status     = self.response.get("status")
        self.message    = self.response.get("message")
        return self
    
    def post(self):
        self.response   = self.__request(method="POST", payload=urlencode(self.__payload))
        self.status     = self.response.get("status")
        self.message    = self.response.get("message")
        return self
    
    def put(self):
        self.response   = self.__request(method="PUT", payload=urlencode(self.__payload))
        self.status     = self.response.get("status")
        self.message    = self.response.get("message")
        return self
    
    def delete(self):
        self.response   = self.__request(method="DELETE", payload=urlencode(self.__payload))
        self.status     = self.response.get("status")
        self.message    = self.response.get("message")
        return self
    
    def is_success(self):
        if self.response.get("status") >= 200 and self.response.get("status") <= 251:
            self.data   = self.response.get("data")
            return True
        return False
    
    def is_unauthorized(self):
        if self.response.get("status") == 401:
            return True
        return False
        