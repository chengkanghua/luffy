

from mycelery.main import app
from luffyapi.libs.yuntongxun.sms import CCP
from luffyapi.settings import contants
import logging
logger = logging.getLogger('django')

@app.task(name='send_sms')
def send_sms(mobile,sms_code):
    """发送短信的任务"""
    ccp = CCP()
    ret = ccp.send_template_sms('13833013278', [sms_code, contants.SMS_EXPIRE_TIME // 60], 1)
    if not ret:
        logger.error("%s 发送短信失败" % mobile)






@app.task
def send_sms2():
    """发送短信的任务"""

    return '发送短信2'















