from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
class APIAuth(BaseAuthentication):

    def authenticate(self, request):
        print(request) #<rest_framework.request.Request object at 0x1142bd190>   request.user


        if 1:
            return 'xx','oo'  #request.user = 'xx'  request.auth = 'oo'

        else:
            raise AuthenticationFailed('认证失败')