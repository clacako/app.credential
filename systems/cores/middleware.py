from systems.engines.apis import Credential
from django.conf import settings

class Permission():
    def __init__(self, token, role_can_access=None, *args, **kwargs):
        self.__role_can_access  = role_can_access
        self.__token            = token
        
    def granted_permission(self):
        try:
            endpoint                    = "authentication/token"
            payload                     = {"token" : self.__token} 
            api_authentication_token    = Credential(endpoint=endpoint, payload=payload).post()
        except Exception as error:
            self.message  = error
            return False
        else:
            if api_authentication_token.is_success():
                credential  = api_authentication_token.data[0]
                # Check authorization
                if credential.get("role") in self.__role_can_access:
                    self.data   = credential
                    return True
                else:
                    self.message  = "401, Unauthorized"
                    return False        
            else:
                self.message  = api_authentication_token.message
                return False