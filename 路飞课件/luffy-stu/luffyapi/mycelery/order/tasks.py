
from order.models import Order
from datetime import datetime,timedelta
from luffyapi.settings import contants

from mycelery.main import app


@app.task(name='check_oo')
def check_order():
    """订单超时取消任务"""
    # 超时条件，当前时间 > 订单生成时间 + 超时时间段 --- 超时
    # 当前时间 - 超时时间段 > 订单生成时间  --- 超时
    # 订单生成时间 < 当前时间 - 超时时间段 --- 超时

    print('定时任务开始执行了')

    now_time = datetime.now()
    out_time = contants.ORDER_OUTTIME  #12小时

    # 超时时间点
    order_out_time = now_time - timedelta(seconds=out_time)

    order_list = Order.objects.filter(order_status=0,created_time__lt=order_out_time)

    for order in order_list:
        order.order_status = 3
        order.save()










