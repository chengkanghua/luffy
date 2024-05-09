# 7. 序列化器-Serializer

作用：

    1. 序列化,序列化器会把模型对象转换成字典,经过response以后变成json字符串
    2. 反序列化,把客户端发送过来的数据,经过request以后变成字典,序列化器可以把字典转成模型
    3. 反序列化,完成数据校验功能


## 7.1 定义序列化器

Django REST framework中的Serializer使用类来定义，须继承自rest_framework.serializers.Serializer。

接下来，为了方便演示序列化器的使用，我们先创建一个新的子应用sers

```
python manage.py startapp sers
```



我们已有了一个数据库模型类students/Student

```python
from django.db import models

# Create your models here.
class Student(models.Model):
    # 模型字段
    name = models.CharField(max_length=100,verbose_name="姓名",help_text="提示文本:账号不能为空！")
    sex = models.BooleanField(default=True,verbose_name="性别")
    age = models.IntegerField(verbose_name="年龄")
    class_null = models.CharField(max_length=5,verbose_name="班级编号")
    description = models.TextField(verbose_name="个性签名")

    class Meta:
        db_table="tb_student"
        verbose_name = "学生"
        verbose_name_plural = verbose_name
```

我们想为这个模型类提供一个序列化器，可以定义如下：

```python
from rest_framework import serializers

# 声明序列化器，所有的序列化器都要直接或者间接继承于 Serializer
# 其中，ModelSerializer是Serializer的子类，ModelSerializer在Serializer的基础上进行了代码简化
class StudentSerializer(serializers.Serializer):
    """学生信息序列化器"""
    # 1. 需要进行数据转换的字段
    id = serializers.IntegerField()
    name = serializers.CharField()
    age = serializers.IntegerField()
    sex = serializers.BooleanField()
    description = serializers.CharField()

    # 2. 如果序列化器集成的是ModelSerializer，则需要声明调用的模型信息

    # 3. 验证代码

    # 4. 编写添加和更新模型的代码
```

**注意：serializer不是只能为数据库模型类定义，也可以为非数据库模型类的数据定义。**serializer是独立于数据库之外的存在。



**常用字段类型**：

| 字段                    | 字段构造方式                                                 |
| ----------------------- | ------------------------------------------------------------ |
| **BooleanField**        | BooleanField()                                               |
| **NullBooleanField**    | NullBooleanField()                                           |
| **CharField**           | CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True) |
| **EmailField**          | EmailField(max_length=None, min_length=None, allow_blank=False) |
| **RegexField**          | RegexField(regex, max_length=None, min_length=None, allow_blank=False) |
| **SlugField**           | SlugField(max*length=50, min_length=None, allow_blank=False) 正则字段，验证正则模式 [a-zA-Z0-9*-]+ |
| **URLField**            | URLField(max_length=200, min_length=None, allow_blank=False) |
| **UUIDField**           | UUIDField(format='hex_verbose')  format:  1) `'hex_verbose'` 如`"5ce0e9a5-5ffa-654b-cee0-1238041fb31a"`  2） `'hex'` 如 `"5ce0e9a55ffa654bcee01238041fb31a"`  3）`'int'` - 如: `"123456789012312313134124512351145145114"`  4）`'urn'` 如: `"urn:uuid:5ce0e9a5-5ffa-654b-cee0-1238041fb31a"` |
| **IPAddressField**      | IPAddressField(protocol='both', unpack_ipv4=False, **options) |
| **IntegerField**        | IntegerField(max_value=None, min_value=None)                 |
| **FloatField**          | FloatField(max_value=None, min_value=None)                   |
| **DecimalField**        | DecimalField(max_digits, decimal_places, coerce_to_string=None, max_value=None, min_value=None) max_digits: 最多位数 decimal_palces: 小数点位置 |
| **DateTimeField**       | DateTimeField(format=api_settings.DATETIME_FORMAT, input_formats=None) |
| **DateField**           | DateField(format=api_settings.DATE_FORMAT, input_formats=None) |
| **TimeField**           | TimeField(format=api_settings.TIME_FORMAT, input_formats=None) |
| **DurationField**       | DurationField()                                              |
| **ChoiceField**         | ChoiceField(choices) choices与Django的用法相同               |
| **MultipleChoiceField** | MultipleChoiceField(choices)                                 |
| **FileField**           | FileField(max_length=None, allow_empty_file=False, use_url=UPLOADED_FILES_USE_URL) |
| **ImageField**          | ImageField(max_length=None, allow_empty_file=False, use_url=UPLOADED_FILES_USE_URL) |
| **ListField**           | ListField(child=, min_length=None, max_length=None)          |
| **DictField**           | DictField(child=)                                            |

**选项参数：**

| 参数名称            | 作用             |
| ------------------- | ---------------- |
| **max_length**      | 最大长度         |
| **min_length**      | 最小长度         |
| **allow_blank**     | 是否允许为空     |
| **trim_whitespace** | 是否截断空白字符 |
| **max_value**       | 最大值           |
| **min_value**       | 最小值           |

通用参数：

| 参数名称           | 说明                                          |
| ------------------ | --------------------------------------------- |
| **read_only**      | 表明该字段仅用于序列化输出，默认False         |
| **write_only**     | 表明该字段仅用于反序列化输入，默认False       |
| **required**       | 表明该字段在反序列化时必须输入，默认True      |
| **default**        | 反序列化时使用的默认值                        |
| **allow_null**     | 表明该字段是否允许传入None，默认False         |
| **validators**     | 该字段使用的验证器                            |
| **error_messages** | 包含错误编号与错误信息的字典                  |
| **label**          | 用于HTML展示API页面时，显示的字段名称         |
| **help_text**      | 用于HTML展示API页面时，显示的字段帮助提示信息 |



## 7.2 创建Serializer对象

定义好Serializer类后，就可以创建Serializer对象了。

Serializer的构造方法为：

```python
Serializer(instance=None, data=empty, **kwarg)
```

说明：

1）用于序列化时，将模型类对象传入**instance**参数

2）用于反序列化时，将要被反序列化的数据传入**data**参数

3）除了instance和data参数外，在构造Serializer对象时，还可通过**context**参数额外添加数据，如

```python
serializer = AccountSerializer(account, context={'request': request})
```

**通过context参数附加的数据，可以通过Serializer对象的context属性获取。**



1. 使用序列化器的时候一定要注意，序列化器声明了以后，不会自动执行，需要我们在视图中进行调用才可以。
2. 序列化器无法直接接收数据，需要我们在视图中创建序列化器对象时把使用的数据传递过来。
3. 序列化器的字段声明类似于我们前面使用过的表单系统。
4. 开发restful api时，序列化器会帮我们把模型数据转换成字典.
5. drf提供的视图会帮我们把字典转换成json,或者把客户端发送过来的数据转换字典.



## 7.3 序列化器的使用

序列化器的使用分两个阶段：

1. 在客户端请求时，使用序列化器可以完成对数据的反序列化。
2. 在服务器响应时，使用序列化器可以完成对数据的序列化。



### 7.3.2  反序列化

#### 7.3.2.1 数据验证

使用序列化器进行反序列化时，需要对数据进行验证后，才能获取验证成功的数据或保存成模型类对象。

在获取反序列化的数据前，必须调用**is_valid()**方法进行验证，验证成功返回True，否则返回False。

验证失败，可以通过序列化器对象的**errors**属性获取错误信息，返回字典，包含了字段和字段的错误。如果是非字段错误，可以通过修改REST framework配置中的**NON_FIELD_ERRORS_KEY**来控制错误字典中的键名。

验证成功，可以通过序列化器对象的**validated_data**属性获取数据。

在定义序列化器时，指明每个字段的序列化类型和选项参数，本身就是一种验证行为。

为了方便演示效果，我们单独再次创建一个子应用unsers，。

```bash
python manage.py startapp unsers
```



定义序列化器，代码：unsers/serializers.py

```python
from rest_framework import serializers
class StudentSerializer(serializers.Serializer):
    # 需要转换的字段声明
    # 小括号里面声明主要提供给反序列化使用的
    name = serializers.CharField(required=True, max_length=20)
    age = serializers.IntegerField(max_value=150, min_value=0,required=True)
    sex = serializers.BooleanField(default=True)
    description = serializers.CharField(required=False,allow_null=True, allow_blank=True) #required=False,字段都可以不传递给后端，allow_null=True,允许提交过来的数据为空值(null--None)，allow_blank=True 允许提交过来的数据为空字符串
    
    # 如果序列化器调用的模型中的字段声明，则需要声明Meta类

    # 验证

    # 添加和更新代码

```

通过构造序列化器对象，并将要反序列化的数据传递给data构造参数，进而进行验证 unsers/views.py

```python
from django.http import JsonResponse
from django.views import View
from .serializers import StudentSerializer
from students.models import Student


class StudentView(View):
    def post(self, request):
        """添加一个学生"""
        # 接受参数
        # content-type:'application/json' #django默认解析不了这种数据格式
        # urlencoded #在postman修改成这种格式再发送
        post_data = request.POST
        data = {
            "name": post_data.get('name'),
            "age": post_data.get('age'),
            "sex": post_data.get('sex'),
            "description": post_data.get('description'),
        }
        # 调用序列化器进行反序列化验证和转换
        serializer = StudentSerializer(data=data)
        # serializer.errors  # 查看错误信息

        # 当验证失败时,可以直接通过声明 raise_exception=True 让django直接跑出异常,那么验证出错之后，直接就再这里报错，程序中断了就
        # result = serializer.is_valid(raise_exception=True)
        # print("验证结果:%s" % result)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return JsonResponse(serializer.errors)  # 返回校验的错误信息


        # 获取通过验证后的数据
        print(serializer.validated_data)  # form -- clean_data
        # 保存数据
        student = Student.objects.create(
            name=serializer.validated_data.get("name"),
            age=serializer.validated_data.get("age"),
            sex=serializer.validated_data.get("sex"),
            description=serializer.validated_data.get("description")
        )

        print(student)
        # 返回响应结果给客户端
        # alt + enter，可以实现快速导包
        return JsonResponse({"message": "ok"})
```

is_valid()方法还可以在验证失败时抛出异常serializers.ValidationError，可以通过传递**raise_exception=True**参数开启，REST framework接收到此异常，会向前端返回HTTP 400 Bad Request响应。

```python
# Return a 400 response if the data was invalid.
serializer.is_valid(raise_exception=True)
```



unsers/urls.py

```py
from django.urls import path
from unsers import views


urlpatterns = [
    path('students/',views.StudentView.as_view()),
]
```

drfdemo/urls.py   全局路由添加路径

```py

urlpatterns = [
    ...
    path('unser/',include('unsers.urls')),
]
```



这里使用postman 测试

post    http://127.0.0.1:8000/unser/students/

选body    raw  json 格式

```json
{
    "name": "小红",
    "age": "18",
    "sex": 1,
    "description": "111"
}
```



send 之后提示Forbidden   csrf 错误

setting.py设置

```
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware', #暂时注释这个
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```



发送json格式数据  默认解析不到

```py
class StudentView(View):
    def post(self, request):
        # content-type:'application/json' #django默认解析不了这种数据格式
        # urlencoded #在postman修改成这种格式再发送
        post_data = request.POST
        data = {
            "name": post_data.get('name'),
            "age": post_data.get('age'),
            "sex": post_data.get('sex'),
            "description": post_data.get('description'),
        }
```







如果觉得这些还不够，需要再补充定义验证行为，可以使用以下三种方法：

局部钩子

##### 1) validate_字段名

对`<field_name>`字段进行验证，如

```python
class StudentSerializer(serializers.Serializer):
    """学生数据序列化器"""
    ...

    # 序列化器中可以自定义单个字段的验证方法  def validate_<字段名>(用户提交的字段数据):
    def validate_name(self,data):
        if(data=="老男孩666"):
            raise serializers.ValidationError("用户名不能是老男孩666")

        # 验证完成以后务必要返回字段值
        return data
```



全局钩子

##### 2) validate

在序列化器中需要同时对多个字段进行比较验证时，可以定义validate方法来验证，如

```python
class StudentSerializer(serializers.Serializer):
    """学生数据序列化器"""
    ...
		
    # 方法名时固定的,用于验证多个字段,参数就是实例化序列化器类时的data参数
    def validate(self,data):
        name = data.get("name")
        if(name == "python"):
            raise serializers.ValidationError("用户名不能是python")

        age = data.get("age")
        if(age==0):
            raise serializers.ValidationError("年龄不能是0")

        # 验证完成以后务必要返回data
        return data
```



##### 3) validators

在字段中添加validators选项参数，也可以补充验证行为，如

```python
def check_age(age):
    if age ==50:
        raise serializers.ValidationError("年龄不能刚好是50")
    return age

def check_name(val):
    if '666' not in val:
        raise serializers.ValidationError("没有包含666")
    else:
        return val

class StudentSerializer(serializers.Serializer):
    # 需要转换的字段声明
    # 小括号里面声明主要提供给反序列化使用的
    name = serializers.CharField(required=True, max_length=20,validators=[check_name,])
    age = serializers.IntegerField(max_value=150, min_value=0,required=True,validators=[check_age])
    sex = serializers.BooleanField(default=True)
    description = serializers.CharField(required=False,allow_null=True, allow_blank=True)
```





#### 7.3.2.2  反序列化-保存数据

前面的验证数据成功后,我们可以使用序列化器来完成数据反序列化的过程.这个过程可以把数据转成模型类对象.

首先我们可以在views中直接写上保存数据的代码

```python
# Create your views here.
from django.http import JsonResponse
from django.views import View
from .serializers import StudentSerializer
from students.models import Student
class StudentView(View):
    def post(self,request):
        """添加一个学生"""
        # 接受参数
        post_data = request.POST
        data = {
            "name":post_data.get('name'),
            "age":post_data.get('age'),
            "sex":post_data.get('sex'),
            "description":post_data.get('description'),
        }
        serializer = StudentSerializer(data=data)
				serializer.errors  
        result = serializer.is_valid(raise_exception=True)
        print( "验证结果:%s" % result )
        print( serializer.validated_data ) 
        
        student = Student.objects.create(
            name=serializer.validated_data.get("name"),
            age=serializer.validated_data.get("age"),
            sex=serializer.validated_data.get("sex")
        )

        print(student)
        return JsonResponse({"message": "ok"})
```





还可以通过序列化器提供的create()和update()两个方法来实现。

```python
from rest_framework import serializers
from students.models import Student

def check_age(age):
    if age ==50:
        raise serializers.ValidationError("年龄不能刚好是50")
    return age

class StudentSerializer(serializers.Serializer):
    # 需要转换的字段声明
    # 小括号里面声明主要提供给反序列化使用的
    name = serializers.CharField(required=True, max_length=20)
    age = serializers.IntegerField(max_value=150, min_value=0,required=True,validators=[check_age])
    sex = serializers.BooleanField(default=True)
    description = serializers.CharField(required=False,allow_null=True, allow_blank=True) #required=False,
    # 如果序列化器调用的模型中的字段声明，则需要声明Meta类

    # 验证
    # 序列化器中可以自定义单个字段的验证方法  def validate_<字段名>(用户提交的字段数据):
    def validate_name(self,data):
        if(data=="老男孩"):
            raise serializers.ValidationError("用户名不能是老男孩")

        # 验证完成以后务必要返回字段值
        return data

    # 方法名时固定的,用于验证多个字段,参数就是实例化序列化器类时的data参数
    def validate(self,data):
        name = data.get("name")
        if(name == "python"):
            raise serializers.ValidationError("用户名不能是python")

        age = data.get("age")
        if(age==0):
            raise serializers.ValidationError("年龄不能是0")

        # 验证完成以后务必要返回data
        return data

    # 添加和更新代码
    # 序列化器中会提供了两个方法: create 和 update,方法名是固定的
    def create(self, validated_data):  # validated_data 参数,在序列化器调用时,会自动传递验证完成以后的数据
        student = Student.objects.create(
            name=self.validated_data.get("name"),
            age=self.validated_data.get("age"),
            sex=self.validated_data.get("sex"),
            description=serializer.validated_data.get("description")
        )

        return student

    def update(self,instance,validated_data): #instance表示当前更新的记录对象
        """更新学生信息"""
        instance.name=validated_data.get("name")
        instance.sex=validated_data.get("sex")
        instance.age=validated_data.get("age")
        instance.description=validated_data.get("description")
        # 调用模型的save更新保存数据
        instance.save()

        return instance
```

实现了上述两个方法后，在视图中调用序列化器进行反序列化数据的时候，就可以通过save()方法返回一个数据对象实例了

```python
student = serializer.save()  #如果是添加，自动会调用create，更新就自动调用update
```

视图代码：

```python
# Create your views here.
from django.http import JsonResponse
from django.views import View
from .serializers import StudentSerializer
from students.models import Student
class StudentView(View):
    def post(self,request):
        """添加一个学生"""
        
        ....


    def put(self,request):
        """更新学生信息"""
        # 接受参数
        data = {
            "id":9,
            "name":"abc",
            "age":18,
            "sex":1,
            "description":"测试",
        }
        # 获取要修改的数据
        instance = Student.objects.get(pk=data.get("id"))
        # 调用序列化器
        serializer = StudentSerializer(instance=instance,data=data)
        # 验证
        serializer.is_valid(raise_exception=True)
        # 转换成模型数据
        student = serializer.save()

        return JsonResponse({"message": "ok"})
```



如果创建序列化器对象的时候，没有传递instance实例，则调用save()方法的时候，create()被调用，相反，如果传递了instance实例，则调用save()方法的时候，update()被调用。



#### 7.3.2.3 附加说明

1） 在对序列化器进行save()保存时，可以额外传递数据，这些数据可以在create()和update()中的validated_data参数获取到

```python
# request.user 是django中记录当前登录用户的模型对象

serializer.save(owner=user)

```

2）默认序列化器必须传递所有required的字段，否则会抛出验证异常。但是我们可以使用partial参数来允许部分字段更新

```python
# 更新学生的部分字段信息，当数据库允许为空，但是序列化器要求必须字段填写的时候，可以使用以下方式避开
serializer = StudentSerializer(instance=instance, data=data, partial=True)
```



把上面序列化器子应用sers和反序列化器子应用unsers里面的序列化器进行对比。

```python
from rest_framework import serializers

# 声明序列化器，所有的序列化器都要直接或者间接继承于 Serializer
# 其中，ModelSerializer是Serializer的子类，ModelSerializer在Serializer的基础上进行了代码简化
class StudentSerializer(serializers.Serializer):
    """学生信息序列化器"""
    # 1. 需要进行数据转换的字段
    id = serializers.IntegerField()
    name = serializers.CharField()
    age = serializers.IntegerField()
    sex = serializers.BooleanField()
    description = serializers.CharField()
```

 ```python
from rest_framework import serializers
from students.models import Student

def check_age(age):
    if age ==50:
        raise serializers.ValidationError("年龄不能刚好是50")
    return age

class StudentSerializer(serializers.Serializer):
    # 需要转换的字段声明
    # 小括号里面声明主要提供给反序列化使用的
    name = serializers.CharField(required=True, max_length=20)
    age = serializers.IntegerField(max_value=150, min_value=0,required=True,validators=[check_age])
    sex = serializers.BooleanField(default=True)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    # 如果序列化器调用的模型中的字段声明，则需要声明Meta类

    # 验证
    # 序列化器中可以自定义单个字段的验证方法  def validate_<字段名>(用户提交的字段数据):
    def validate_name(self,data):
        if(data=="老男孩"):
            raise serializers.ValidationError("用户名不能是老男孩")

        # 验证完成以后务必要返回字段值
        return data

    # 方法名时固定的,用于验证多个字段,参数就是实例化序列化器类时的data参数
    def validate(self,data):
        name = data.get("name")
        if(name == "python"):
            raise serializers.ValidationError("用户名不能是python")

        age = data.get("age")
        if(age==0):
            raise serializers.ValidationError("年龄不能是0")

        # 验证完成以后务必要返回data
        return data

    # 添加和更新代码
    # 序列化器中会提供了两个方法: create 和 update,方法名是固定的
    def create(self, validated_data): # validated_data 参数,在序列化器调用时,会自动传递验证完成以后的数据
        student = Student.objects.create(
            name=self.validated_data.get("name"),
            age=self.validated_data.get("age"),
            sex=self.validated_data.get("sex")
        )

        return student

    def update(self,instance,validated_data):
        """更新学生信息"""
        instance.name=validated_data.get("name")
        instance.sex=validated_data.get("sex")
        instance.age=validated_data.get("age")
        instance.description=validated_data.get("description")
        # 调用模型的save更新保存数据
        instance.save()

        return instance
 ```

可以发现，反序列化器中的代码会包含了序列化器中的大部分代码，除了ID字段的声明。

所以在开发的时候，我们一般都是直接写在一起，那么有些字段只会出现在序列化器阶段，例如ID。还有些字段只会出现在反序列化阶段，例如：用户密码。

那么， 我们需要在序列化器类中，声明那些字段是在序列化时使用，哪些字段在反序列化中使用了。

最终序列化器中的代码：

```python
from rest_framework import serializers
from students.models import Student

def check_age(age):
    if age ==50:
        raise serializers.ValidationError("年龄不能刚好是50")
    return age

class StudentSerializer(serializers.Serializer):
    # 需要转换的字段声明
    # 小括号里面声明主要提供给反序列化使用的
    id=serializers.IntegerField(read_only=True)  #read_only=True读取数据时能读出来，反序列化校验数据的时候不需要校验。
    name = serializers.CharField(required=True, max_length=20)
    age = serializers.IntegerField(max_value=150, min_value=0,required=True,validators=[check_age])
    sex = serializers.BooleanField(default=True,write_only=True)#write_only=True读取数据时不能读出来。但是反序列化校验数据保存时，需要传给我们的序列化器
    description = serializers.CharField(required=True, allow_null=True, allow_blank=True)
    # 如果序列化器调用的模型中的字段声明，则需要声明Meta类

    # 验证
    # 序列化器中可以自定义单个字段的验证方法  def validate_<字段名>(用户提交的字段数据):
    def validate_name(self,data):
        if(data=="老男孩"):
            raise serializers.ValidationError("用户名不能是老男孩")

        # 验证完成以后务必要返回字段值
        return data

    # 方法名时固定的,用于验证多个字段,参数就是实例化序列化器类时的data参数
    def validate(self,data):
        name = data.get("name")
        if(name == "python"):
            raise serializers.ValidationError("用户名不能是python")

        age = data.get("age")
        if(age==0):
            raise serializers.ValidationError("年龄不能是0")

        # 验证完成以后务必要返回data
        return data

    # 添加和更新代码
    # 序列化器中会提供了两个方法: create 和 update,方法名是固定的
    def create(self, validated_data): # validated_data 参数,在序列化器调用时,会自动传递验证完成以后的数据
        student = Student.objects.create(
            name=self.validated_data.get("name"),
            age=self.validated_data.get("age"),
            sex=self.validated_data.get("sex")
        )

        return student

    def update(self,instance,validated_data):
        """更新学生信息"""
        instance.name=validated_data.get("name")
        instance.sex=validated_data.get("sex")
        instance.age=validated_data.get("age")
        instance.description=validated_data.get("description")
        # 调用模型的save更新保存数据
        instance.save()

        return instance
```



### 7.3.3 模型类序列化器

如果我们想要使用序列化器对应的是Django的模型类，DRF为我们提供了ModelSerializer模型类序列化器来帮助我们快速创建一个Serializer类。

ModelSerializer与常规的Serializer相同，但提供了：

- 基于模型类自动生成一系列字段
- 基于模型类自动为Serializer生成validators，比如unique_together
- 包含默认的create()和update()的实现

#### 7.3.3.1 定义

为了方便学习和查看效果， 新建一个子应用msers。

```python
python manage.py startapp msers
```



比如我们创建一个msers/serializers.py

```python
from rest_framework import serializers
from students.models import Student

class StudentModelSerializer(serializers.ModelSerializer):
    # 字段声明

    # 如果模型类序列化器,必须声明本次调用是哪个模型,模型里面的哪些字段
    class Meta:
        model = Student
        fields = ["id", "name", "age", "description", "sex"]
        # fields = "__all__" # 表示操作模型中的所有字段
        # 添加额外的验证选项
        # exclude = ['id', ]  # 排除字段
        extra_kwargs = {
            "sex": {"write_only": True, },
            "id": {"read_only": True, }
        }

```

- model 指明参照哪个模型类
- fields 指明为模型类的哪些字段生成



#### 7.3.3.2 指定字段

1) 使用**fields**来明确字段，`__all__`表名包含所有字段，也可以写明具体哪些字段，如

```python
class StudentModelSerializer(serializers.ModelSerializer):
    """学生数据序列化器"""
    class Meta:
        model = Student
        fields = ['id', 'age', 'name',"description"]
```

2) 使用**exclude**可以明确排除掉哪些字段

```python
class StudentModelSerializer(serializers.ModelSerializer):
    """学生数据序列化器"""
    class Meta:
        model = Student
        exclude = ['sex']
```



3) 指明只读字段[少用,通过extra_kwargs更方便一些],

可以通过**read_only_fields**指明只读字段，即仅用于序列化输出的字段

```python
class StudentModelSerializer(serializers.ModelSerializer):
    """学生数据序列化器"""
    class Meta:
        model = Student
        fields = ['id', 'age', 'name',"description"]
        read_only_fields = ('id',)
        #write_only_fields = ('sex',)
```



#### 7.3.3.3 添加额外参数

我们可以使用**extra_kwargs**参数为ModelSerializer添加或修改原有的选项参数

```python
from rest_framework import serializers
from students.models import Student
class StudentModelSerializer(serializers.ModelSerializer):
    # 额外字段声明,必须在fields里面也要声明上去,否则序列化器不会调用
    # password2 = serializers.CharField(write_only=True,required=True)
    # r_password = serializers.CharField() #额外字段 确认密码，需要在下面的 fileds上加上这个字段名
    
    # 如果模型类序列化器,必须声明本次调用是哪个模型,模型里面的哪些字段
    class Meta:
        model = Student
        # fields = ["id","name","age","description","sex","password2"]
        fields = ["id","name","age","description","sex"]
        # fields = "__all__" # 表示操作模型中的所有字段
        # 添加额外的验证选项，比如额外的字段验证
        extra_kwargs = {
            "sex":{"write_only":True,},
            "id":{"read_only":True,}
        }

    # 验证代码  局部钩子 全局钩子 都可以在这里写

    # 也可以重新声明一个create和update
```



简单做个示例 msers/views.py

```python
from django.http import JsonResponse
from django.views import View
from msers.serializers import StudentModelSerializer
from students import models

# Create your views here.

class StudentModelViewSet(View):
    def get(self,request):
        data_list = models.Student.objects.all()
        serializer = StudentModelSerializer(instance=data_list,many=True)

        return JsonResponse(serializer.data,safe=False)

    def post(self,request):

        data = request.POST
        serializers = StudentModelSerializer(data=data)  # 这个使用save 方法是调用create

        # serializers = StudentModelSerializer(instance=instance,data=data)  # 这个使用save 方法是调用update更新

        status = serializers.is_valid(raise_exception=True)
        # print(status)
        # print(serializers.validated_data)
        student = serializers.save()  #上面使用的ModelSerializer，所以不需要我们自己写create方法了
        print(student)
        return JsonResponse({'msg':'henhao'})
```

msers/urls.py

```py
from django.urls import path
from . import views

urlpatterns = [
    path(r'students/',views.StudentModelViewSet.as_view()),

]

```

drfdemo/urls.py

```py
urlpatterns = [
   ...
    path('msers/',include('msers.urls')), //添加路由
]

```



上面只演示了添加操作，更新操作自行测试吧



什么时候继承序列化器类Serializer，什么时候继承模型序列化器类ModelSerializer？主要还是看哪个更适合你的应用场景

```
继承序列化器类Serializer
	字段声明
	验证
	添加/保存数据功能
继承模型序列化器类ModelSerializer
	字段声明[可选,看需要]
	Meta声明
	验证
	添加/保存数据功能[可选]
```



看表字段大小，看使用哪个更加节省代码了。



