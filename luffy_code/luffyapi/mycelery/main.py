# 主程序
import os
from celery import Celery
# 创建celery实例对象
app = Celery("luffy")

# 把celery和django进行组合，需要识别和加载django的配置文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luffyapi.settings.dev')
#如果只是使用了logging日志功能的话可以不写以下两句，因为logging是python提供的模块，但是将来可能使用celery来执行其他的django任务，所以我们先写上
import django
django.setup()


# 通过app对象加载配置，文件路径
app.config_from_object("mycelery.config")

# 自动搜索并加载任务
# 参数必须必须是一个列表，里面的每一个任务都是任务的路径名称
# app.autodiscover_tasks(["任务1","任务2"])
app.autodiscover_tasks(["mycelery.sms",]) #会自动识别sms目录下面的tasks.py文件中的任务，所以不需写成mycelery.sms.tasks

# 启动Celery的命令
# 强烈建议切换目录到项目的根目录下启动celery!!
# celery -A mycelery.main worker --loglevel=info -P eventlet