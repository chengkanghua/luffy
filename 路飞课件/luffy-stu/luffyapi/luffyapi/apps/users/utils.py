
from luffyapi.settings import contants

def jwt_response_payload_handler(token, user=None, request=None):
    """
    拓展jwt返回的数据
    :param token:  jwt token字符串
    :param user:   当前登录对象，model类模型对象
    :param request:   当前请求对象 drf
    :return:
    """

    # print(token)
    # print(user)
    # print(request)

    return {
        'token': token,
        'username': user.username,
        'id': user.id,
        'credit':user.credit,
        'credit_to_money':contants.CREDIT_MONEY,
    }




def get_user_by_account(account):
    try:
        if re.match(r'^1[3-9]\d{9}$', account):
            user = models.User.objects.get(mobile=account)
        else:
            user = models.User.objects.get(username=account)

    except models.User.DoesNotExist:
        print('ssssssss')
        return None
    else:
        return user

import re
from django.contrib.auth.backends import ModelBackend
from . import models

class UsernameMobileAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        # print('>>>>',request)
        # print(username)
        # print(password)
        # 符合手机号规则，说明用户输入的是手机号，否则默认用户输入的是用户名，所以按照用户名去数据库校验

        user = get_user_by_account(username)
        if user is not None and user.check_password(password):

            return user








