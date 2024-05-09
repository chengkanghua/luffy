[TOC]



# 1. 视图

Django REST framwork 提供的视图的主要作用：

- 控制序列化器的执行（检验、保存、转换数据）
- 控制数据库查询的执行



## 1.2 视图

REST framework 提供了众多的通用视图基类与扩展类，以简化视图的编写。



### 1.2.1 2个视图基类

#### 1.2.1.1 APIView

```
rest_framework.views.APIView
```

`APIView`是REST framework提供的所有视图的基类，继承自Django的`View`父类。

`APIView`与`View`的不同之处在于：

- 传入到视图方法中的是REST framework的`Request`对象，而不是Django的`HttpRequeset`对象；
- 视图方法可以返回REST framework的`Response`对象，视图会为响应数据设置（render）符合前端要求的格式；
- 任何`APIException`异常都会被捕获到，并且处理成合适的响应信息；
- 在进行dispatch()分发前，会对请求进行身份认证、权限检查、流量控制。

支持定义的类属性

- **authentication_classes** 列表或元祖，身份认证类
- **permissoin_classes** 列表或元祖，权限检查类
- **throttle_classes** 列表或元祖，流量控制类

在`APIView`中仍以常规的类视图定义方法来实现get() 、post() 或者其他请求方式的方法。

举例：比如我们创建一个demo的应用，然后我们写下面5个接口

```BASH
python manage.py startapp demo

settings.py 里配置app
```

demo/serializer.py

```py
from rest_framework import serializers
from students.models import Student

class StudentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__" # 表示操作模型中的所有字段

```



demo/view.py

```python
from rest_framework.views import APIView
# Create your views here.
from students import models
from .serializers import StudentModelSerializer
from rest_framework.response import Response
from rest_framework import status

class StudentsAPIView(APIView):

    def get(self,request):
        """
        获取所有学生数据
        :param request:
        :return:
        """
        """
            简单总结：
                1 获取一个数据，传instance参数
                    获取多条数据，传instance,many=True参数
                2 更新数据，传instance和data参数
                    部分字段更新，可以增加partial=True参数
                3 添加数据，传data参数
                4 删除数据，不需要使用序列化器
        """
        data_list = models.Student.objects.all()
        serializer = StudentModelSerializer(instance=data_list,many=True)

        return Response(serializer.data)

    def post(self,request):
        """
        添加学生信息
        :param requeset:
        :return:
        """
        data = request.data
        serializer = StudentModelSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()
        # 将添加的新的数据返回给客户端，可以使用我们的序列化组件先序列化一下
        serializer = StudentModelSerializer(instance=instance)

        return Response(serializer.data,status=status.HTTP_201_CREATED)

class StudentAPIView(APIView):

    def get(self,request,pk):
        """获取单条数据"""
        instance = models.Student.objects.get(pk=pk)
        serializer = StudentModelSerializer(instance=instance)
        return Response(serializer.data)
    def put(self,request,pk):
        """更新学生信息"""
        #由于更新操作，我们需要找到被更新的是哪条记录，所以需要客户端给我们传一个id过来，并且以后我们会用到获取一条数据，删除一条数据，都需要用到一个id值，所以我们把上面的get和post方法写成一个类，更新、获取单条数据和删除数据我们再单独写一个类
        data = request.data
        student = models.Student.objects.get(id=pk)

        #可能提交过来的是部分数据，所以加上一个partial=True参数
        serializer = StudentModelSerializer(instance=student,data=data,partial=True)

        serializer.is_valid(raise_exception=True)

        instance = serializer.save()
        # 将修改后的数据返回给客户端
        serializer = StudentModelSerializer(instance=instance)

        return Response(serializer.data)


    def delete(self,request,pk):
        """删除一条数据,用不到我们的序列化器"""

        ret = models.Student.objects.get(id=pk).delete()

        return Response(None,status=status.HTTP_204_NO_CONTENT)

```

对应的demo/urls.py

```python
from django.urls import path,re_path

from . import views
urlpatterns = [
    path(r'students/',views.StudentsAPIView.as_view()),
    re_path(r'students/(?P<pk>\d+)/',views.StudentAPIView.as_view()),
]
```

drfdemo/urls.py

```py
urlpatterns = [
...
    path('demo/',include('demo.urls')),
]
```



访问接口

http://127.0.0.1:8000/demo/students/

http://127.0.0.1:8000/demo/students/1/





下面我们来看一下rest_framework提供的其他功能，如何来简化我们的代码

#### 1.2.1.2 GenericAPIView[通用视图类]

```
rest_framework.generics.GenericAPIView
```

继承自`APIVIew`，**主要增加了操作序列化器和数据库查询的方法，作用是为下面Mixin扩展类的执行提供方法支持。通常在使用时，可搭配一个或多个Mixin扩展类。**

提供的关于序列化器使用的属性与方法

- 属性：

  - **serializer_class** 指明视图使用的序列化器

- 方法：

  - **get_serializer_class(self)**

    当出现一个视图类中调用多个序列化器时,那么可以通过条件判断在get_serializer_class方法中通过返回不同的序列化器类名就可以让视图方法执行不同的序列化器对象了。

    返回序列化器类，默认返回`serializer_class`，可以重写，例如：

    ```python
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return FullAccountSerializer
        return BasicAccountSerializer
    ```

  - ##### get_serializer(self, *args, \**kwargs)

    返回序列化器对象，主要用来提供给Mixin扩展类使用，如果我们在视图中想要获取序列化器对象，也可以直接调用此方法。

    **注意，该方法在提供序列化器对象的时候，会向序列化器对象的context属性补充三个数据：request、format、view，这三个数据对象可以在定义序列化器时使用。**

    比如`serializer = self.get_serializer(instance=self.get_object(),context={'pk':pk})`,下面的request和view我们后面会用到，现在先了解一下，后面使用就知道了
    
    - **request** 当前视图的请求对象
    - **view** 当前请求的类视图对象
    - format 当前请求期望返回的数据格式

提供的关于数据库查询的属性与方法

- 属性：

  - **queryset** 指明使用的数据查询集

- 方法：

  - **get_queryset(self)**

    返回视图使用的查询集，主要用来提供给Mixin扩展类使用，是列表视图与详情视图获取数据的基础，默认返回`queryset`属性，可以重写，例如：

    ```python
    def get_queryset(self):
        user = self.request.user
        return user.accounts.all()
    ```

  - **get_object(self)**

    返回详情视图所需的模型类数据对象，主要用来提供给Mixin扩展类使用。

    在试图中可以调用该方法获取详情信息的模型类对象。

    **若详情访问的模型类对象不存在，会返回404。**

    该方法会默认使用APIView提供的check_object_permissions方法检查当前对象是否有权限被访问。

    举例：

    ```python
    # url(r'^books/(?P<pk>\d+)/$', views.BookDetailView.as_view()),
    class BookDetailView(GenericAPIView):
        queryset = BookInfo.objects.all()
        serializer_class = BookInfoSerializer
    
        def get(self, request, pk):
            book = self.get_object() # get_object()方法根据pk参数查找queryset中的数据对象
            serializer = self.get_serializer(book)
            return Response(serializer.data)
    ```

其他可以设置的属性

- **pagination_class** 指明分页控制类
- **filter_backends** 指明过滤控制后端（查询一些数据的过滤条件等等）

为了方便学习上面的GenericAPIView通用视图类，我们新建一个子应用。

```python
python manage.py startapp gen

setting.py  注册gen app
```

代码：gen/views.py

```python
from rest_framework.generics import GenericAPIView
from students.models import Student
from .serializers import StudentModelSerializer, StudentModel2Serializer
from rest_framework.response import Response

class StudentsGenericAPIView(GenericAPIView):
    # 本次视图类中要操作的数据[必填]
    queryset = Student.objects.all() #基本上是固定的，查询就这么写
    # 本次视图类中要调用的默认序列化器[选填]
    serializer_class = StudentModelSerializer

    def get(self, request):
        """获取所有学生信息"""
        serializer = self.get_serializer(instance=self.get_queryset(), many=True)

        return Response(serializer.data)

    def post(self,request):

        data = request.data

        serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)

        instance = serializer.save()

        serializer = self.get_serializer(instance=instance)

        return Response(serializer.data)


class StudentGenericAPIView(GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    #一个视图中使用多个序列化类的方法，目前的例子是：get请求获取数据时，我们只给他两个字段数据，其他方法时我们给他所有字段数据，定义了这个get_serializer_class方法之后(其实是对父类的方法进行了重写)，其实上面的serializer_class就可以不同写了
    def get_serializer_class(self):
        """重写获取序列化器类的方法"""
        if self.request.method == "GET":
            return StudentModel2Serializer
        else:
            return StudentModelSerializer

    #在使用GenericAPIView实现获取操作单个数据时，我们试图方法中的参数变量pk最好是pk名，别叫id什么的，不然还需要进行一些其他的配置，比较麻烦一些了，简单看一下源码就知道了
    def get(self,request,pk):
        """获取一条数据"""
        serializer = self.get_serializer(instance=self.get_object())

        return Response(serializer.data)

    def put(self,request,pk):

        data = request.data

        serializer = self.get_serializer(instance=self.get_object(),data=data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        serializer = self.get_serializer(instance=self.get_object())

        return Response(serializer.data)
```

序列化器类：gen/serializers.py

```python
from rest_framework import serializers

from students.models import Student

class StudentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model= Student
        fields = "__all__"

# 只有两个字段的序列化器
class StudentModel2Serializer(serializers.ModelSerializer):
    class Meta:
        model= Student
        fields = ("name","class_null")
```

gen/urls.py

```py
from django.urls import path,re_path

from . import views
urlpatterns = [
    path(r'students/',views.StudentsGenericAPIView.as_view()),
    re_path(r'students/(?P<pk>\d+)/',views.StudentGenericAPIView.as_view()),
]
```

drfdemo/urls.py

```py

urlpatterns = [
...
    path('gen/',include('gen.urls')),
]

```

访问测试

http://127.0.0.1:8000/gen/students/

http://127.0.0.1:8000/gen/students/1/



其实GenericAPIView只是帮我们把数据库查询啊调用序列化器类啊进行了一步封装，目的是为了将一些公共性质的代码挑出去封装一下，其他感觉没啥大用，但其实这个公共性质的代码都不要我们写了，看下面几个扩展类来增强GenericAPIView的作用。

### 1.2.2 5个视图扩展类

作用：

提供了几种后端视图（对数据资源进行曾删改查）处理流程的实现，如果需要编写的视图属于这五种，则视图可以通过继承相应的扩展类来复用代码，减少自己编写的代码量。

这五个扩展类需要搭配GenericAPIView父类，因为五个扩展类的实现需要调用GenericAPIView提供的序列化器与数据库查询的方法。



#### 1）ListModelMixin

获取多条数据的 列表视图扩展类，提供`list(request, *args, **kwargs)`方法快速实现列表视图，返回200状态码。

该Mixin的list方法会对数据进行过滤和分页。

源代码：

```python
class ListModelMixin(object):
    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        # 过滤
        queryset = self.filter_queryset(self.get_queryset())
        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        # 序列化
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
```

举例：

```python
from rest_framework.mixins import ListModelMixin

class BookListView(ListModelMixin, GenericAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer

    def get(self, request):
        return self.list(request)
```



修改gen/views.py

```PY
from rest_framework.mixins import ListModelMixin
class StudentsGenericAPIView(ListModelMixin,GenericAPIView):
    queryset = Student.objects.all() #基本上是固定的，查询就这么写
    serializer_class = StudentModelSerializer
    def get(self, request):
        """获取所有学生信息"""
        # serializer = self.get_serializer(instance=self.get_queryset(), many=True)
        #
        # return Response(serializer.data)
        return self.list(request)
```





#### 2）CreateModelMixin

添加数据的创建视图扩展类，提供`create(request, *args, **kwargs)`方法快速实现创建资源的视图，成功返回201状态码。

如果序列化器对前端发送的数据验证失败，返回400错误。

源代码：

```python
class CreateModelMixin(object):
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        # 获取序列化器
        serializer = self.get_serializer(data=request.data)
        # 验证
        serializer.is_valid(raise_exception=True)
        # 保存
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
```

示例：

```python
from rest_framework.mixins import ListModelMixin, CreateModelMixin
def post(self,request):
  
  return self.create(requset)
```



#### 3）RetrieveModelMixin

获取单条数据，详情视图扩展类，提供`retrieve(request, *args, **kwargs)`方法，可以快速实现返回一个存在的数据对象。

如果存在，返回200， 否则返回404。

源代码：

```python
class RetrieveModelMixin(object):
    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        # 获取对象，会检查对象的权限
        instance = self.get_object()
        # 序列化
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
```

举例：

```python
class BookDetailView(RetrieveModelMixin, GenericAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer

    def get(self, request, pk):
        return self.retrieve(request,pk)
        return self.retrieve(request) #pk也可以不传
```



#### 4）UpdateModelMixin

更新视图扩展类，提供`update(request, *args, **kwargs)`方法，可以快速实现更新一个存在的数据对象。

同时也提供`partial_update(request, *args, **kwargs)`方法，可以实现局部更新。

成功返回200，序列化器校验数据失败时，返回400错误。

源代码：

```python
class UpdateModelMixin(object):
    """
    Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
```

示例：

```python
def put(self,request,pk):
  """更新一条数据"""
  return self.update(request,pk)
```



#### 5）DestroyModelMixin

删除视图扩展类，提供`destroy(request, *args, **kwargs)`方法，可以快速实现删除一个存在的数据对象。

成功返回204，不存在返回404。

源代码：

```python
class DestroyModelMixin(object):
    """
    Destroy a model instance.
    """
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
```

示例：

```python
def delete(self,request,pk):
        """删除一条数据"""
        return self.destroy(request,pk)
```



使用GenericAPIView和视图扩展类，实现api接口，代码：

```python
"""GenericAPIView结合视图扩展类实现api接口"""
from rest_framework.mixins import ListModelMixin,CreateModelMixin
class Students2GenericAPIView(GenericAPIView,ListModelMixin,CreateModelMixin):
    # 本次视图类中要操作的数据[必填]
    queryset = Student.objects.all()
    # 本次视图类中要调用的默认序列化器[玄天]
    serializer_class = StudentModelSerializer

    def get(self, request):
        """获取多个学生信息"""
        return self.list(request)

    def post(self,request):
        """添加学生信息"""
        return self.create(request)


from rest_framework.mixins import RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
class Student2GenericAPIView(GenericAPIView,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
    queryset = Student.objects.all()

    serializer_class = StudentModelSerializer

    # 在使用GenericAPIView视图获取或操作单个数据时,视图方法中的代表主键的参数最好是pk
    def get(self,request,pk):
        """获取一条数据"""
        return self.retrieve(request,pk)

    def put(self,request,pk):
        """更新一条数据"""
        return self.update(request,pk)

    def delete(self,request,pk):
        """删除一条数据"""
        return self.destroy(request,pk)
```

修改后gen/views.py

```py
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin

from students.models import Student
from .serializers import StudentModelSerializer, StudentModel2Serializer
from rest_framework.response import Response

class StudentsGenericAPIView(CreateModelMixin,ListModelMixin,GenericAPIView):
    queryset = Student.objects.all() #基本上是固定的，查询就这么写
    serializer_class = StudentModelSerializer

    def get(self, request):
        """获取所有学生信息"""
        return self.list(request)

    def post(self,request):
        """添加学生信息"""
        return self.create(request)

class StudentGenericAPIView(DestroyModelMixin,UpdateModelMixin,RetrieveModelMixin,GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get_serializer_class(self):
        """重写获取序列化器类的方法"""
        if self.request.method == "GET":
            return StudentModel2Serializer
        else:
            return StudentModelSerializer

    def get(self,request,pk):
        """获取一条数据"""
        return self.retrieve(request,pk)

    def put(self,request,pk):
        '''修改一条数据'''
        return self.update(request,pk)

    def delete(self,request,pk):
        '''删除一条数据'''
        return self.destroy(request,pk)
```







下面还能对我们上面的代码进行简化。视图子类，也叫通用视图子类。

### 1.2.3 GenericAPIView的视图子类

`from rest_framework.generics import ListAPIView...`

#### 1）CreateAPIView

提供 post 方法

继承自： GenericAPIView、CreateModelMixin

#### 2）ListAPIView

提供 get 方法

继承自：GenericAPIView、ListModelMixin

#### 3）RetrieveAPIView

提供 get 方法

继承自: GenericAPIView、RetrieveModelMixin

#### 4）DestoryAPIView

提供 delete 方法

继承自：GenericAPIView、DestoryModelMixin

#### 5）UpdateAPIView

提供 put 和 patch 方法

继承自：GenericAPIView、UpdateModelMixin

#### 6）RetrieveUpdateAPIView

提供 get、put、patch方法

继承自： GenericAPIView、RetrieveModelMixin、UpdateModelMixin

#### 7）RetrieveUpdateDestoryAPIView

提供 get、put、patch、delete方法

继承自：GenericAPIView、RetrieveModelMixin、UpdateModelMixin、DestoryModelMixin



示例：

```python
"""使用GenericAPIView的视图子类进一步简化开发api接口的代码"""
from rest_framework.generics import ListAPIView,CreateAPIView
class Students3GenericAPIView(ListAPIView,CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer


from rest_framework.generics import RetrieveAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView # 结合了上面三个子类的功能
class Student3GenericAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    
```



gen/views.py   修改后测试

```py
from rest_framework.generics import ListAPIView, CreateAPIView,RetrieveAPIView,DestroyAPIView,UpdateAPIView
from students.models import Student
from .serializers import StudentModelSerializer, StudentModel2Serializer

class StudentsGenericAPIView(ListAPIView,CreateAPIView):
    queryset = Student.objects.all() #基本上是固定的，查询就这么写
    serializer_class = StudentModelSerializer

class StudentGenericAPIView(RetrieveAPIView,DestroyAPIView,UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    def get_serializer_class(self):
        """重写获取序列化器类的方法"""
        if self.request.method == "GET":
            return StudentModel2Serializer
        else:
            return StudentModelSerializer
```

测试之前的接口一样好用





## 1.3 视图集基类ViewSet

使用视图集ViewSet，可以将一系列逻辑相关的动作放到一个类中：

- list() 提供一组数据
- retrieve() 提供单个数据
- create() 创建数据
- update() 更新数据
- destory() 删除数据

ViewSet视图集类不再实现get()、post()等方法，而是实现动作 **action** 如 list() 、create() 等。

视图集只在使用as_view()方法的时候，才会将**action**动作与具体请求方式对应上。如：

```python
"""使用视图集把上面的两个视图类组成一个视图类"""
from rest_framework.viewsets import ViewSet
class StudentViewSet(ViewSet):
    def get_all(self,request):
        """获取所有学生信息"""
        data_list = Student.objects.all()
        serializer = StudentModelSerializer(instance=data_list, many=True)
        return Response(serializer.data)

    def add_student(self,request):

        return Response({"message":"添加成功!"})

    def get_one(self,request,pk):
        """获取一个学生信息"""
        instance = Student.objects.get(pk=pk)
        serializer = StudentModelSerializer(instance=instance)
        return Response(serializer.data)
```

在设置路由时，我们可以如下操作

```python
urlpatterns = [
    # 发挥下ViewSet的作用  get请求对应到 get_all方法上
    path("students5/", views.Student2ViewSet.as_view({"get": "get_all", "post": "add_student"})),
    re_path("students5/(?P<pk>\d+)/", views.Student2ViewSet.as_view({"get":"get_one"})),
]
```

再改善一下我们viewset

```python
"""发挥下ViewSet的作用"""
from rest_framework.viewsets import ViewSet
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView
class Student2ViewSet(ViewSet,ListAPIView,CreateAPIView,RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    def get_all(self,request):
        """获取所有学生信息"""
        return self.list(request)

    def add_student(self,request):

        return self.create(request)

    def get_one(self,request,pk):
        """获取一个学生信息"""
        return self.retrieve(request)
```



### 1.3.1 常用视图集父类

#### 1） ViewSet

继承自`APIView`与`ViewSetMixin`，作用也与APIView基本类似，提供了身份认证、权限校验、流量管理等。

**ViewSet主要通过继承ViewSetMixin来实现在调用as_view()时传入字典（如{'get':'list'}）的映射处理工作。**

在ViewSet中，没有提供任何动作action方法，需要我们自己实现action方法。

#### 2）GenericViewSet

使用ViewSet通常并不方便，因为list、retrieve、create、update、destory等方法都需要自己编写，而这些方法与前面讲过的Mixin扩展类提供的方法同名，所以我们可以通过继承Mixin扩展类来复用这些方法而无需自己编写。但是Mixin扩展类依赖于`GenericAPIView`，所以还需要继承`GenericAPIView`。

**GenericViewSet**就帮助我们完成了这样的继承工作，继承自`GenericAPIView`与`ViewSetMixin`，在实现了调用as_view()时传入字典（如`{'get':'list'}`）的映射处理工作的同时，还提供了`GenericAPIView`提供的基础方法，可以直接搭配Mixin扩展类使用。

举例：

```python
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin
class Student3ViewSet(GenericViewSet,ListModelMixin,CreateModelMixin,RetrieveModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    def get_all(self,request):
        """获取所有学生信息"""
        return self.list(request)

    def add_student(self,request):

        return self.create(request)

    def get_one(self,request,pk):
        """获取一个学生信息"""
        return self.retrieve(request)
```

url的定义

```python
urlpatterns = [
    path("students7/", views.Student4ViewSet.as_view({"get": "list", "post": "create"})),
    re_path("students7/(?P<pk>\d+)/", views.Student4ViewSet.as_view({"get": "retrieve","put":"update","delete":"destroy"})),

]
```

简化上面的代码  gen/views.py

```python
"""简化上面的代码"""
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
class StudentGenericViewSet(GenericViewSet,ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
```

gen/urls.py

```py
from django.urls import path,re_path

from . import views
urlpatterns = [
    path(r'students/', views.StudentGenericViewSet.as_view({"get": "list", "post": "create"})),
    re_path(r'students/(?P<pk>\d+)/', views.StudentGenericViewSet.as_view({"get": "retrieve","put":"update","delete":"destroy"})),
]
```

测试接口

http://127.0.0.1:8000/gen/students/

http://127.0.0.1:8000/gen/students/1



#### 3）ModelViewSet

继承自`GenericViewSet`，同时包括了ListModelMixin、RetrieveModelMixin、CreateModelMixin、UpdateModelMixin、DestoryModelMixin。

示例：

```python
"""使用ModelViewSet简写上面的继承代码，最终版"""
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from rest_framework.decorators import action
class StudentModelViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
```



#### 4）ReadOnlyModelViewSet(自行测试吧，就是继承的功能少了)

继承自`GenericViewSet`，同时包括了ListModelMixin、RetrieveModelMixin。



### 1.3.2 视图集中定义附加action动作

在视图集中，除了上述默认的方法动作外，还可以添加自定义动作，进行扩展。

举例，比如做一个登录方法login：

```python
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
class StudentModelViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def login(self,request):  #这个就可以称为自定义的action动作
        """学生登录功能"""
        return Response({"message":"登录成功"})
```

url的定义

```python
urlpatterns = [
    path("students8/", views.StudentModelViewSet.as_view({"get": "list", "post": "create"})),
    re_path("students8/(?P<pk>\d+)/",
            views.StudentModelViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),

    path("stu/login/",views.StudentModelViewSet.as_view({"get":"login"}))

]
```



### 1.3.3 action属性

在视图集中，我们可以通过action对象属性来获取当前请求视图集时的action动作是哪个。

例如：

```python
from rest_framework.viewsets import ModelViewSet
from students.models import Student
from .serializers import StudentModelSerializer
from rest_framework.response import Response
class StudentModelViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get_new_5(self,request):
        """获取最近添加的5个学生信息"""
        # 操作数据库
        print(self.action) # 获取本次请求的视图方法名 get_new_5
        
        
通过路由访问到当前方法中.可以看到本次的action就是请求的方法名

```



# 2. 路由Routers

对于视图集ViewSet，我们除了可以自己手动指明请求方式与动作action之间的对应关系外，还可以使用Routers来帮助我们快速实现路由信息。

REST framework提供了两个router

- **SimpleRouter**
- **DefaultRouter**

## 2.1 使用方法

1） 创建router对象，并注册视图集，例如

```python
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'router_stu', views.StudentGenericViewSet, base_name='student')
urlpatterns = []
urlpatterns += router.urls

print(router.urls)
'''
[
<URLPattern '^router_stu/$' [name='student-list']>, 
<URLPattern '^router_stu\.(?P<format>[a-z0-9]+)/?$' [name='student-list']>, 
<URLPattern '^router_stu/(?P<pk>[^/.]+)/$' [name='student-detail']>, 
<URLPattern '^router_stu/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='student-detail']>, 
<URLPattern '' [name='api-root']>, 
<URLPattern '<drf_format_suffix:format>' [name='api-root']>]
'''

get  login
#但是注意：路由对象只会按照modelviewset中的五个接口(get post put patch delete)生成对应的访问地址而已，上面的login这种自定义动作就不能访问到了 
```

register(prefix, viewset, base_name)

- prefix 该视图集的路由前缀
- viewset 视图集
- base_name 路由别名的前缀 #student-get   student-login

如上述代码会形成的路由如下：

```python
^router_stu/$    name: student-list
^router_stu/{pk}/$   name: student-detail
```

2）添加路由数据

可以有两种方式：

方式1 简单一些

```python
urlpatterns = [
    ...
]
urlpatterns += router.urls
```

或

方式2

```python
urlpatterns = [
    ...
    url(r'^', include(router.urls))
]
```

使用路由类给视图集生成了路由地址

```python
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
class StudentModelViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def login(self,request):
        """学生登录功能"""
        print(self.action)
        return Response({"message":"登录成功"})

```

路由代码：

```python
from django.urls import path, re_path
from . import views
urlpatterns = [
    ...
]

"""使用drf提供路由类router给视图集生成路由列表"""
# 实例化路由类
# drf提供一共提供了两个路由类给我们使用,他们用法一致,功能几乎一样
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

# 注册视图集
# router.register("路由前缀",视图集类)
router.register("router_stu",views.StudentModelViewSet)

# 把生成的路由列表追加到urlpatterns
print( router.urls )
urlpatterns += router.urls


```

上面的代码就成功生成了路由地址[增/删/改/查一条/查多条的功能]，但是不会自动帮我们在视图集自定义方法的路由。

所以我们如果也要给自定义方法生成路由，则需要进行action动作的声明。



## 2.2 视图集中附加action的声明

在视图集中，如果想要让Router自动帮助我们为自定义的动作生成路由信息，需要使用`rest_framework.decorators.action`装饰器。

以action装饰器装饰的方法名会作为action动作名，与list、retrieve等同。

action装饰器可以接收两个参数：

- **methods**: 声明该action对应的请求方式，列表传递

- detail

  : 声明该action的路径是否与单一资源对应，及是否是

  ```
  xxx/<pk>/action方法名/
  ```

  - True 表示路径格式是`xxx/<pk>/action方法名/`
  - False 表示路径格式是`xxx/action方法名/`

举例：

```python
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

class StudentModelViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    # methods 设置当前方法允许哪些http请求访问当前视图方法
    # detail 设置当前视图方法是否是操作一个数据
    # detail为True，表示路径名格式应该为 router_stu/{pk}/login/
    @action(methods=['get'], detail=True)
    def login(self, request,pk):
        """登录"""
        ...

    # detail为False 表示路径名格式应该为 router_stu/get_new_5/
    @action(methods=['put'], detail=False)
    def get_new_5(self, request):
        """获取最新添加的5个学生信息"""
        ...
```

由路由器自动为此视图集自定义action方法形成的路由会是如下内容：

```python
^router_stu/get_new_5/$    name: router_stu-get_new_5
^router_stu/{pk}/login/$   name: router_stu-login
```



gen/views.py  测试

```py
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from students.models import Student
from .serializers import StudentModelSerializer

class StudentGenericViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    # methods 设置当前方法允许哪些http请求访问当前视图方法
    # detail 设置当前视图方法是否是操作一个数据
    # detail为True，表示路径名格式应该为 router_stu/{pk}/login/
    # http://127.0.0.1:8000/gen/router_stu/1/login/
    @action(methods=['get'],detail=True)
    def login(self,request,pk):
        """学生登录功能"""
        print(self.action)
        return Response({"message":"登录成功"})
    # detail为False 表示路径名格式应该为 router_stu/login2/
    # http://127.0.0.1:8000/gen/router_stu/login2/
    @action(methods=['get'],detail=False)
    def login2(self,request):
        """学生登录功能"""
        print(self.action)
        return Response({"message":"登录成功"})
```







## 2.3 路由router形成URL的方式

1） SimpleRouter

![SimpleRouter](assets/SimpleRouter.png)

2）DefaultRouter

![DefaultRouter](assets/DefaultRouter.png)

DefaultRouter与SimpleRouter的区别是，DefaultRouter会多附带一个默认的API根视图，返回一个包含所有列表视图的超链接响应数据。比如使用DefaultRouter时你访问一下`http://127.0.0.1:8001/router_stu/` 会看到一个页面，而SimpleRouter会报错，一般都需要有个查看所有接口的页面，所以我们基本都是用的是DefaultRouter。