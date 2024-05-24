from luffyapi.settings import constants
def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'id': user.id,
        'username': user.username,
        'credit': user.credit,
        'credit_to_money': constants.CREDIT_MONEY,
    }


def get_user_by_account(account):
    """
    根据帐号获取user对象
    :param account: 账号，可以是用户名，也可以是手机号
    :return: User对象 或者 None
    """
    try:
        user = models.User.objects.filter(Q(username=account) | Q(mobile=account)).first()
    except models.User.DoesNotExist:
        return None
    else:
        return user


from . import models
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
class UsernameMobileAuthBackend(ModelBackend):
    """
    自定义用户名或手机号认证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)
        # if user is not None and user.check_password(password) :
        if user is not None and user.check_password(password) and user.is_authenticated:
            # user.is_authenticated是看他有没有权限的，这里可以不加上它
            return user



from ronglian_sms_sdk import SmsSDK
from django.conf import settings
import json
accId = settings.SMS['accId']
accToken = settings.SMS['accToken']
appId = settings.SMS['appId']
def send_message(tid,mobile,datas):
    sdk = SmsSDK(accId, accToken, appId)
    # tid = '1'
    # mobile = '18679816495,'
    # datas = ('2', '22')
    resp = sdk.sendMessage(tid, mobile, datas)
    # print(resp)
    resp = json.loads(resp)
    if resp.get("statusCode") == "000000":
        # 返回1 表示发送短信成功
        return 1
    else:
        # 返回0 表示发送失败
        return 0






