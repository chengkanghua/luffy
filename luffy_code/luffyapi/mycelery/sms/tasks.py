# celery的任务必须写在tasks.py的文件中，别的文件名称不识别!!!
from mycelery.main import app
import logging

log = logging.getLogger("django")
from luffyapi.settings import constants
from users.utils import send_message

tid = constants.SMS_TEMPLATE_ID
@app.task(name="send_sms")  # name表示设置任务的名称，如果不填写，则默认使用函数名(路径)做为任务名
def send_sms(mobile, datas,tid=tid,):
    ret = send_message(tid, mobile, datas)
    print("发送短信!!!")
    if not ret:
        log.error("用户注册短信发送失败！手机号：%s" % mobile)

# @app.task  # name表示设置任务的名称，如果不填写，则默认使用函数名做为任务名
# def send_sms2():
#     print("发送短信任务2!!!")
