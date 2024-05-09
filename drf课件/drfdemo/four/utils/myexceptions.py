from rest_framework.views import exception_handler
from rest_framework.response import Response
from four.views import APIErrorxx

def MyExceptionHandler(exc, context): #自定义的错误处理函数
    '''
        	exc错误对象
          context 异常发生时的一些上下文信息
    '''
    # 先调用REST framework默认的异常处理方法获得标准错误响应对象
    # 这个函数是drf提供的，它处理了一些错误，但是如果它处理不了的，它会返回None，所以，如果是None的话，我们需要自己来处理错误
    response = exception_handler(exc, context)
    print(exc,type(exc))  #查询有误 class 'four.views.APIErrorxx'>
    print(context)

    # 在此处补充自定义的异常处理
    if response is None:
        if isinstance(exc,APIErrorxx):
            # 这里就可以记录错误信息了，一般记录到文件中，可以使用日志系统来进行记录
            return Response({'APIErrorxx':'请检查错误信息'})
            # response.data['status_code'] = response.status_code

        # else:
        #     return None

    return response
