from rest_framework.views import exception_handler
import logging
logger = logging.getLogger('django')
from django.db import DatabaseError
from rest_framework.response import Response
from rest_framework import status
from redis import RedisError



def custom_exception_handler(exc, context):
    """
    自定义异常处理
    :param exc: 异常类
    :param context: 抛出异常的上下文
    :return: Response响应对象
    """
    # 调用drf框架原生的异常处理方法
    response = exception_handler(exc, context)

    if response is None:
        view = context['view']
        if isinstance(exc, DatabaseError) or isinstance(exc, RedisError):
            # 数据库异常
            logger.error('[%s] %s' % (view, exc))
            response = Response({'message': '服务器内部错误，请联系客服工作人员！'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response