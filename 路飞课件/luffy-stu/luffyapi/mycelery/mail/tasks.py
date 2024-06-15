

from mycelery.main import app

@app.task(name='send_email')
def send_email():
    """发送短信的任务"""


    return '发送邮件'
















