##  我的订单

#### 订单状态显示分析

```
根据订单状态显示:
1. 如果未支付[order.order_stauts==0],则显示"去支付"按钮
2. 如果已支付[order.order_stauts==1],则显示"去学习"按钮
3. 如果未支付,并超过指定时间[12个小时],则显示"超时取消" [Celery / Django-crontab 定时任务https://github.com/kraiz/django-crontab ]
   用户下单在12小时以后自动判断订单状态如果是0,则直接改成3
   
定时任务[crontab]，主要是依靠：操作系统的定时计划或者第三方软件的定时执行
定时任务的常见场景：
   1. 订单超时
   2. 生日邮件[例如，每天凌晨检查当天有没有用户生日，有则发送一份祝福邮件]
   3. 财务统计[例如，每个月的1号，把当月的订单进行统计，生成一个财务记录，保存到数据库中]
   4. 页面缓存[例如，把首页设置为每隔5分钟生成一次缓存]
```



#### 使用Celery的定时任务来完成订单超时功能

Celery官方文档中关于定时任务使用的说明：

```python
http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html
```



在实现定时任务之前，我们需要先简单使用一下。

我们需要新增一个任务目录，例如order

```
celey_tasks/
    ├── sms/
    │   ├── __init__.py
    │   └── tasks.py
    ├── config.py
    ├── __init__.py
    ├── main.py
    ├── order/
    │   ├── __init__.py
    │   └── tasks.py
    └── sms

```

在main.py中，注册任务目录【注意，接下来后面我们使用django的模型处理，所以必须对django的配置进行引入】

```bash
import os

from celery import Celery

# 1. 创建示例对象
app = Celery("luffy")

# 2. 加载配置
app.config_from_object("celery_tasks.config")
# 3. 注册任务[自动搜索并加载任务]
# 参数必须必须是一个列表，里面的每一个任务都是任务的路径名称
# app.autodiscover_tasks(["任务1","任务2"])
app.autodiscover_tasks(["celery_tasks.sms","celery_tasks.order"])

# 4. 在终端下面运行celery命令启动celery
# celery -A 主程序 worker --loglevel=info
# celery -A celery_tasks.main worker --loglevel=info
```

接下来，在order任务目录下， 创建固定名字的任务文件tasks.py，代码：

```python
from mycelery.main import app

@app.task(name="check_order")
def check_order():
    print("检查订单是否过期!!!")
```

接下来，我们需要把这个任务设置定时任务，所以需要借助Celery本身提供的Crontab模块。

在配置文件config.py中，对定时任务进行注册：

```python
# 任务队列的链接地址
broker_url = 'redis://127.0.0.1:6379/15'
# 结果队列的链接地址
result_backend = 'redis://127.0.0.1:6379/14'

from celery.schedules import crontab
from .main import app
# 定时任务的调度列表，用于注册定时任务
app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'check_order_outtime': {
        # 本次调度的任务
        'task': 'check_order', # 这里的任务名称必须先到main.py中注册,如果写了别名，直接写别名就可以了
        # 定时任务的调度周期
        # 'schedule': crontab(minute=0, hour=0),   # 每周凌晨00:00
        'schedule': crontab(),   # 每分钟,没写秒数，那么就是每分钟的0秒开始
      	# 'args': (16, 16),  # 注意：任务就是一个函数，所以如果有参数则需要传递
    },
}
```

接下来，我们就可以重启Celery并启用Celery的定时任务调度器

先在终端下，运行celery的定时任务程序，以下命令：

```bash
celery -A mycelery.main beat  # mycelery.main 是celery的主应用文件
```

然后再新建一个终端，运行以下命令，上面的命令必须先指定：

```python
celery -A mycelery.main worker --loglevel=info
```

注意，使用的时候，如果有时区必须先配置好系统时区。



经过上面的测试以后，我们接下来只需改造上面的任务函数，用于判断修改订单是否超时。

要完成订单的任务功能，如果需要调用django框架的模型操作，那么必须针对django框架进行配置加载和初始化。

main.py，代码：

```python
import os

from celery import Celery

# 1. 创建示例对象
app = Celery("luffy")

# 把celery和django进行组合，识别和加载django的配置文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luffyapi.settings.dev')

# 在当前clery中启动django框架，对django框架进行进行初始化
import django
django.setup()

# 2. 加载配置
app.config_from_object("celery_tasks.config")
# 3. 注册任务[自动搜索并加载任务]
# 参数必须必须是一个列表，里面的每一个任务都是任务的路径名称
# app.autodiscover_tasks(["任务1","任务2"])
app.autodiscover_tasks(["celery_tasks.sms","celery_tasks.order"])

# 4. 在终端下面运行celery命令启动celery
# celery -A 主程序 worker --loglevel=info
# celery -A celery_tasks.main worker --loglevel=info
```

注意，因为在django中是有时区配置的，所以，我们在django框架配置中也要修改时区配置。

任务代码tasks.py的实现：

```python
from mycelery.main import app
from luffyapi.settings import constants
from datetime import datetime
from order.models import Order

@app.task(name="check_order")
def check_order():
    """超时取消过期订单"""
    # 超时条件： 当前时间 > (订单生成时间 + 超时时间)   =====>>>>  (当前时间 - 超时时间) > 订单生成时间
    now_timestamp = datetime.now().timestamp()
    # 订单过期时间,只要小于下面的时间的都是过期了的
    timeout_number = now_timestamp - constants.ORDER_OUTTIME
    timeout_date_string = datetime.fromtimestamp(timeout_number)
    order_outtime_list = Order.objects.filter(order_status=0, created_time__lte=timeout_date_string)
    for order in order_outtime_list:
        order.order_status = 3
        order.save()
```

配置文件，settings/constants.py，代码：

```python
# 设置订单超时超时的时间[单位: 秒]
ORDER_OUTTIME = 12 * 60 * 60
```



重新启动celery的定时任务模块和celery的主应用程序。
