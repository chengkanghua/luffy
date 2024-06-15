import os
from celery import Celery

#1 首先，创建celery对象实例
app = Celery('luffy')
# app2 = Celery()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luffyapi.settings.dev')
import django
django.setup()


#2 加载配置 -- 给celery对象指定 任务队列用什么，结果存哪里等等
app.config_from_object('mycelery.config')


#3 自动发现任务
app.autodiscover_tasks(['mycelery.sms','mycelery.mail','mycelery.order'])
















