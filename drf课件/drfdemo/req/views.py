from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse
from django.views import View
from rest_framework import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class StudentAPIView(APIView):
    def get(self,request):
        print(request)

        #获取url中的请求参数
        #当我们访问http://127.0.0.1:8000/req/students/?age=100
        print(request.query_params) # <QueryDict: {'age': ['100']}>
        return Response({'msg': 'ok'})

    def post(self,request):
        # 获取post请求体中的数据
        print(request.data)   #drf能够解析json格式的数据  格式普通字典类型 {'xxx': '1'}，getlist方法用不了
        print(request.data.get('hobby'))
        print(request.data.getlist('hobby'))  #获取多选数据，当发送数据类型json，就不能用getlist了
        '''
        结果：
            <QueryDict: {'name': ['小黑'], 'hobby': ['篮球', '美女']}>
            美女
            ['篮球', '美女']
        '''
        return Response({'msg':'ok'})
