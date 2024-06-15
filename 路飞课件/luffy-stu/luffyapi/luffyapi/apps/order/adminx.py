import xadmin
from .models import Order
class OrderModelAdmin(object):
    """订单模型管理类"""
    pass

xadmin.site.register(Order, OrderModelAdmin)


from .models import OrderDetail
class OrderDetailModelAdmin(object):
    """订单详情模型管理类"""
    pass

xadmin.site.register(OrderDetail, OrderDetailModelAdmin)
