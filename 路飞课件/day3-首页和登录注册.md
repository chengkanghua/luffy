

## 轮播图功能实现

### 安装依赖模块和配置

#### 图片处理模块

前面已经安装了，如果没有安装则需要安装

```shell
pip install pillow
```



#### 上传文件相关配置

settings.py，由于我们需要在后台上传我们的轮播图图片，所以我们需要在django中配置一下上传文件的相关配置，有了它之后，就不需要我们自己写上传文件，保存文件的操作了，看配置：

```python
# 访问静态文件的url地址前缀
STATIC_URL = '/static/'
# 设置django的静态文件目录
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,"static")
]

# 项目中存储上传文件的根目录[暂时配置]，注意，uploads目录需要手动创建否则上传文件时报错
MEDIA_ROOT=os.path.join(BASE_DIR,"uploads")
# 访问上传文件的url地址前缀
MEDIA_URL ="/media/"

```



在django项目中转换上传文件的Url地址，总路由urls.py新增代码：

```python
from django.urls import re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
  	...
    re_path(r'media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
]
```



### 注册home子应用

因为当前功能是drf的第一个功能，所以我们先创建一个子应用home，创建在luffy/apps目录下

![1557456645658](assets/1557456645658.png)

```

\luffyapi\luffyapi>cd luffyapi/apps
\luffyapi\luffyapi\apps>python ../../manage.py startapp home

```



注册home子应用，因为子应用的位置发生了改变，所以为了原来子应用的注册写法，所以新增一个导包路径：

```python
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 新增一个系统导包路径
import sys
#sys.path使我们可以直接import导入时使用到的路径，所以我们直接将我们的apps路径加到默认搜索路径里面去，那么django就能直接找到apps下面的应用了
sys.path.insert(0,os.path.join(BASE_DIR,"apps"))



INSTALLED_APPS = [
	# 注意，加上drf框架的注册	
    'rest_framework',
    
    # 子应用
    'home',

]
```

注意，pycharm会路径错误的提示。可以鼠标右键设置apps为 mark dir.... as source root，不推荐，因为这是pycharm提供的。



#### 新建开发分支进行独立开发

接下来,我们完成的功能[轮播图]这些,建议采用开发分支来完成,所以我们可以通过以下命令,复刻一份代码[也就是新建一个分支]出来进行独立开发.这样的话,就不会影响到线上的主干代码!!!

```
# 新建一个分支 
git branch 分支名称

# 查看所有分支
git branch

# 切换分支[-b表示新建分支的同时并切换到新分支]
git checkout -b 分支名称

# 删除分支
git branch -d 分支名称
```

接下来,我们可以创建一个dev开发分支并在开发分支下干活!

```
git branch dev
git checkout dev
```





### 创建轮播图的模型

home/models.py

```python
from django.db import models

# Create your models here.
class Banner(models.Model):
    """轮播广告图模型"""
    # 模型字段
    title = models.CharField(max_length=500, verbose_name="广告标题")
    link = models.CharField(max_length=500, verbose_name="广告链接")
    # upload_to 设置上传文件的保存子目录,将来上传来的文件会存到我们的media下面的banner文件夹下，这里存的是图片地址。
    image_url =  models.ImageField(upload_to="banner", null=True, blank=True, max_length=255, verbose_name="广告图片")
    remark = models.TextField(verbose_name="备注信息")
    is_show = models.BooleanField(default=False, verbose_name="是否显示") #将来轮播图肯定会更新，到底显示哪些
    orders = models.IntegerField(default=1, verbose_name="排序")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")

    # 表信息声明
    class Meta:
        db_table = "ly_banner"
        verbose_name = "轮播广告"
        verbose_name_plural = verbose_name

    # 自定义方法[自定义字段或者自定义工具方法]
    def __str__(self):
        return self.title
```



数据迁移

```python
python manage.py makemigrations
python manage.py migrate
```

效果：

![1557457331569](assets/1557457331569.png)



### 序列化器

home/serializers.py

```python
from rest_framework import serializers
from .models import Banner
class BannerModelSerializer(serializers.ModelSerializer):
    """轮播广告的序列化器"""
    # 模型序列化器字段声明
    class Meta:
        model = Banner
        fields = ["image_url","link"]
```



### 视图代码

views.py

```python
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from .models import Banner
from .serializers import BannerModelSerializer
from luffyapi.settings import constants
class BannerListAPIView(ListAPIView): # 自动导包
    queryset = Banner.objects.filter(is_show=True, is_deleted=False).order_by("-orders","-id")[:constants.BANNER_LENGTH] #没有必要获取所有图片数据，因为有些可能是删除了的、或者不显示的
    # 切片获取数据的时候，我们可以将切片长度设置成配置项
    serializer_class = BannerModelSerializer
```

在settings配置文件夹中创建一个constants.py配置文件，将来里面存放我们所有的一些常量信息配置，比如上面的轮播图数据切片长度

```python
BANNER_LENGTH = 10
```





### 路由代码

home/urls.py

```python
from django.urls import path,re_path
from . import views
urlpatterns = [
    path("banner/",views.BannerListAPIView.as_view()),
]
```

把home的路由urls.py注册到总路由

```python
from django.contrib import admin
from django.urls import path,re_path,include
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
    path('home/', include("home.urls") ),
]

```

同时,我们可以通过一个配置文件,统一配置一些业务需要使用的常量,例如,显示轮播图的数据量:

settings目录新建一个constants.py常量文件:

```python
#　轮播的显示数量
BANNER_LENGTH = 10
```





访问http://api.luffycity.cn:8000/home/banner/，效果：

![1557457803586](assets/1557457803586.png)



所以我们需要有一个后台提供数据.安装xadmin

```python
pip install https://codeload.github.com/sshwsfc/xadmin/zip/django2 -i https://pypi.douban.com/simple/
```

上面安装的版本是支持的django2版本的



大神修改版本： xadmin下载地址：https://github.com/vip68/xadmin_bugfix 

这个版本支持django3.0版本

去[github](https://so.csdn.net/so/search?q=github&spm=1001.2101.3001.7020)下载完之后解压，把xadmin这个文件夹复制到项目根目录下或者apps目录下都可以，



requirements.txt
```TEXT
asgiref==3.4.1
backports.zoneinfo==0.2.1
defusedxml==0.7.1
diff-match-patch==20200713
Django==3.2.25
django-ckeditor==6.3.2
django-cors-headers==3.10.1
django-crispy-forms==1.13.0
django-formtools==2.4
django-import-export==2.7.1
django-js-asset==2.0.0
django-reversion==4.0.2
djangorestframework==3.15.1
et-xmlfile==1.1.0
future==1.0.0
httplib2==0.22.0
importlib-resources==5.4.0
MarkupPy==1.14
odfpy==1.4.1
openpyxl==3.1.2
Pillow==8.4.0
PyMySQL==1.0.2
pyparsing==3.1.2
pytz==2024.1
PyYAML==6.0.1
six==1.16.0
sqlparse==0.4.4
tablib==3.1.0
typing-extensions==4.1.1
xlrd==2.0.1
XlsxWriter==3.2.0
xlwt==1.3.0
zipp==3.6.0

```

```
pip install -r requirements.txt
```





在配置文件中注册如下应用

```python
INSTALLED_APPS = [
    ...
    'xadmin',
    'crispy_forms',
    'reversion',
    ...
]

# 修改使用中文界面
LANGUAGE_CODE = 'zh-Hans'

# 修改时区
TIME_ZONE = 'Asia/Shanghai'
```



xadmin有建立自己的数据库模型类，需要进行数据库迁移

```shell
python manage.py makemigrations
python manage.py migrate
```

控制台报错

```
  File "<frozen importlib._bootstrap>", line 677, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 728, in exec_module
  File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
  File "E:\pyCharmProject\hengda\xadmin\plugins\importexport.py", line 48, in <module>
    from import_export.admin import DEFAULT_FORMATS, SKIP_ADMIN_LOG, TMP_STORAGE_CLASS
ImportError: cannot import name 'SKIP_ADMIN_LOG' from 'import_export.admin' (D:\Anaconda\envs\hengda\lib\site-packages\import_export\admin.py)
```

点击报错的链接： File "E:\pyCharmProject\hengda\xadmin\plugins\importexport.py", line 48, in <module>

之后我们就来到了importexport.py代码中，可以看到有爆红的地方，这是因为在新的xadmin中已经弃用了这个库包的引入，所以我们要替换掉它，

找到报错的代码用到的地方，在def get_skip_admin_log(self)的上面加上test（self）函数代码保存，之后再运行 python manage.py migrate，你会发现这时候已经可以了。
```PY
      def test(self):
        if self.aaa is None:
            return ImportMixin(ImportExportMixin).get_skip_admin_log()
        else:
            return self.aaa
 
    # def get_skip_admin_log(self):
    #     if self.skip_admin_log is None:
    #         return SKIP_ADMIN_LOG
    #     else:
    #         return self.skip_admin_log
    #
    # def get_tmp_storage_class(self):
    #     if self.tmp_storage_class is None:
    #         return TMP_STORAGE_CLASS
    #     else:
    #         return self.tmp_storage_class
```

报错 cannot import name ‘DEFAULT_FORMATS‘

点击对应的文件

```python
# 注释掉引用不了的
from import_export.formats.base_formats import DEFAULT_FORMATS
```







在总路由中添加xadmin的路由信息

```python
import xadmin
xadmin.autodiscover()

# version模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
xversion.register_models()

urlpatterns = [
    path(r'xadmin/', xadmin.site.urls),
]

---------------------------------------------------新版
import xadmin

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('admin/', xadmin.site.urls),
]
```



如果之前没有创建超级用户，需要创建，如果有了，则可以直接使用之前的。

```python
python manage.py createsuperuser
```

![1557459230311](assets/1557459230311.png)

#### 给xadmin设置基本站点配置信息 

apps/xadmin/xadmin.py

```python
import xadmin
from xadmin import views

class BaseSetting(object):
    """xadmin的基本配置"""
    enable_themes = True  # 开启主题切换功能
    use_bootswatch = True

xadmin.site.register(views.BaseAdminView, BaseSetting)

class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "路飞学城"  # 设置站点标题
    site_footer = "路飞学城有限公司"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠

xadmin.site.register(views.CommAdminView, GlobalSettings)
```



![1557459373544](assets/1557459373544.png)



### 注册轮播图模型到xadmin中



在当前子应用中创建xadmin/adminx.py，添加如下代码

```python
# 轮播图
#from .models import Banner
from home.models import Banner
class BannerModelAdmin(object):
    list_display=["title","orders","is_show"]
    
xadmin.site.register(Banner, BannerModelAdmin)
```



#### 修改后端xadmin中子应用名称

子应用xadmin/apps.py

```python
#class HomeConfig(AppConfig):
#    name = 'home'
#    verbose_name = '我的首页'
```

在home这个app下面的``__init__.py``中设置下面的内容

```python
#default_app_config = "home.apps.HomeConfig" 
default_app_config = 'xadmin.apps.XAdminConfig'
```

![1557459568731](assets/1557459568731.png)

给轮播图添加测试数据

![1557459669649](assets/1557459669649.png)



添加几条测试数据效果：

 



经过上面的操作,我们就完成了轮播图的API接口,接下来,可以考虑提交一个代码版本.

但是,我们前面创建了一个本地开发分支,所以我们如果直接提交代码,默认是在dev分支提交的.

所以就不能直接使用`git push`,而是采用以下命令提交

```bash
git add .
git commit -m "服务端实现轮播图的API接口"
# 注意  dev:dev  表示从本地的dev中把代码推送到线上分支dev,如果线上没有dev分支,则自动创建dev分支
git push origin dev:dev
```

经过上面的操作,我们就可以看到,线上也存在了一个dev分支,而master分支的代码并没有变化.

开发中,如果dev的代码经过开发人员的自测以后,就可以申请合并dev分支代码到主分支,master里面去了.

1. 申请合并分支

![1561519134676](assets\1561519134676.png)

2. 填写申请合并分支的表单

![1561520384469](assets\1561520384469.png)

3. 经过测试和审查人员的检查通过以后,我们就可以直接合并分支了.

![1561520409942](assets\1561520409942.png)

4. 开发人员合并分支

   ![1561520437539](assets\1561520437539.png)

5. 审查和测试人员同意合并分支

   ![1561520496375](assets\1561520496375.png)



### 客户端代码获取数据

compoents/common/Banner.vue代码：

```vue
<template>
<!--    <h1>轮播图组件</h1>-->
  <el-carousel indicator-position="outside" height="400px">
    <el-carousel-item v-for="(value,index) in banner_list" :key="value.id">

      <a :href="value.link" style="display: inline-block;height: 400px;width: 100%">
        <img :src="value.image_url" alt="" width="100%" height="400px">
      </a>
     <!-- <img src="@/assets/banner/banner1.png" alt=""> -->

    </el-carousel-item>
  </el-carousel>
</template>

<script>
    //router-link主要用于站内页面跳转，使用的是相对路径
    //a标签用于外部链接页面跳转

    export default {
        name: "Banner",
      data(){
          return {
            banner_list:[]
          }
      },
      methods:{
          get_banner_data(){
            this.$axios.get(`${this.$settings.Host}/home/banner/`,)
              .then((res)=>{
                // console.log(res);
                this.banner_list = res.data
              })
              .catch((error)=>{
                console.log(error);
              })


          }
      },
      created() {
          this.get_banner_data();
      }
    }
</script>

<style scoped>

</style>

```

common/Footer.vue

```VUE
<template>
    <div class="footer">
      <div class="footer-item">
        <div class="foot-left">
        <div class="foot-content">
          <p>
            <span>关于我们</span>
            &nbsp;&nbsp;|&nbsp;&nbsp;
            <span>贝里小卖铺</span>
          </p>
          <p>
            地址：北京市昌平区顺沙路八号院汇德商厦402  邮箱：customer@luffycity.com
          </p>
          <p>
             © 2017-2020 北京路飞学城教育科技有限公司版权所有
            <a class="copyright" href="http://beian.miit.gov.cn" target="_blank" >京ICP备17072161号-1</a>
          </p>
          <p>
            <a class="report-link" target="_blank" href="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=11010102002019&amp;token=1ee3034d-ba3a-4cc3-89d4-89875e2dd0b1">
              <img class="report-img" src="//img.alicdn.com/tfs/TB1..50QpXXXXX7XpXXXXXXXXXX-40-40.png" style="float:left" >
              京公网安备 11010102002019号
            </a>
          </p>
        </div>

      </div>
        <img src="@/assets/code.png" alt="" class="code">
      </div>
    </div>
</template>

<script>
    export default {
        name: "Foot"
    }
</script>

<style scoped>

  .footer{
    display: flex;
    align-items: center;
    width: 100%;
    height: 140px;
    flex-direction: column;
    overflow: hidden;
    background: #191c25;
    position:fixed;
    bottom:0;
  }
  .footer .foot-left{
    display: flex;
    align-items: center;
  }
  .footer .foot-left .foot-content p{
    margin-bottom: 10px;
    font-size: 13px;
    font-family: PingFangSC-Regular;
    font-weight: 400;
    color: #d0d0d0;
  }
  .footer-item{
    width: 960px;
    height: 100%;
    justify-content: space-between;
  }
  .foot-left{
    display: flex;
    align-items: center;
    float: left;
  }
  .foot-content a{
    color: #d0d0d0;
  }
  .footer .foot-left .foot-content p:first-child span{
    font-size: 16px;
    font-weight: 400;
    display: inline-block;
    font-family: PingFangSC-Regular;
    cursor: pointer;
  }
  .foot-content .report-img{
    display: inline-block;
    height: 20px;
    width: 20px;
    margin-right: 12px;
  }
  .footer-item .code{
    width: 74px;
    height: auto;
    margin-right: 100px;
    float: right;
    padding-top: 30px;
  }

</style>

```

common/Header.vue

```vue
<template>
  <div class="header">
    <el-container>
      <el-header>
        <el-row>
          <el-col class="logo" :span="3">
            <a href="/">
              <img src="@/assets/head-logo.svg" alt="">
            </a>
          </el-col>
          <el-col class="nav" :span="16">
              <el-row>
                <el-col :span="3"><router-link class="current" to="/">免费课</router-link></el-col>
                <el-col :span="3"><router-link to="/">轻课</router-link></el-col>
                <el-col :span="3"><router-link to="/">学位课</router-link></el-col>
                <el-col :span="3"><router-link to="/">题库</router-link></el-col>
                <el-col :span="3"><router-link to="/">教育</router-link></el-col>
              </el-row>
          </el-col>
          <el-col class="login-bar" :span="5">
            <el-row v-if="token">
              <el-col class="cart-ico" :span="9">
                <router-link to="">
                  <b class="goods-number">0</b>
                  <img class="cart-icon" src="@/assets/cart.png" alt="">
                  <!-- <span>购物车</span> -->
                  <span><router-link to="/cart">购物车</router-link></span>
                </router-link>
              </el-col>
              <el-col class="study" :span="8" :offset="2"><router-link to="">学习中心</router-link></el-col>
              <el-col class="member" :span="5">
                <el-menu class="el-menu-demo" mode="horizontal">
                  <el-submenu index="2">
                    <template slot="title"><router-link to=""><img src="@/assets/logo@2x.png" alt=""></router-link></template>
                    <el-menu-item index="2-1">我的账户</el-menu-item>
                    <el-menu-item index="2-2">我的订单</el-menu-item>
                    <el-menu-item index="2-3">我的优惠卷</el-menu-item>
                    <el-menu-item index="2-3">退出登录</el-menu-item>
                  </el-submenu>
                </el-menu>
              </el-col>
            </el-row>
            <el-row v-else>
              <el-col class="cart-ico" :span="9">
                <router-link to="">
                  <img class="cart-icon" src="@/assets/cart.png" alt="">
                  <span>购物车</span>
                </router-link>
              </el-col>
              <el-col :span="10" :offset="5">
                <span class="register">
                  <router-link to="/login">登录</router-link>
                  &nbsp;&nbsp;|&nbsp;&nbsp;
                  <router-link to="/register">注册</router-link>
                </span>
              </el-col>
            </el-row>
          </el-col>
        </el-row>
      </el-header>
    </el-container>
  </div>
</template>

<script>
  export default {
    name: "Header",
    data(){
      return {
        // 设置一个登录标识，表示是否登录
        token: false,
      };
    }
  }
</script>

<style scoped>
  .header{
    top:0;
    left:0;
    right:0;
    margin: auto;
    background-color: #fff;
    height: 80px;
    z-index: 1000;
    position: fixed;
    box-shadow: 0 0.5px 0.5px 0 #c9c9c9;
  }
  .header .el-container{
    width: 1200px;
    margin: 0 auto;
  }
  .el-header{
    height: 80px!important;
    padding:0;
  }
  .logo{

  }
  .logo img{
    padding-top: 22px;
  }

  .nav{
    margin-top: 22px;
  }

  .nav .el-col a{
    display: inline-block;
    text-align: center;
    padding-bottom: 16px;
    padding-left: 5px;
    padding-right: 5px;
    position: relative;
    font-size: 16px;
    margin-left: 20px;
  }

  .nav .el-col .current{
    color: #4a4a4a;
    border-bottom: 4px solid #ffc210;
  }

  .login-bar{
    margin-top: 22px;
  }
  .cart-ico{
    position: relative;
    border-radius: 17px;
  }
  .cart-ico:hover{
    background: #f0f0f0;
  }
  .goods-number{
    width: 16px;
    height: 16px;
    line-height: 17px;
    font-size: 12px;
    color: #fff;
    text-align: center;
    background: #fa6240;
    border-radius: 50%;
    transform: scale(.8);
    position: absolute;
    left: 16px;
    top: -1px;
  }
  .cart-icon{
    width: 15px;
    height: auto;
    margin-left: 6px;
  }
  .cart-ico span{
    margin-left: 12px;
  }
  .member img{
    width: 26px;
    height: 26px;
    border-radius: 50%;
    display: inline-block;
  }
  .member img:hover{
    border: 1px solid yellow;
  }

</style>

```

app.vue

```vue
<template>
  <div id="app">

    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>


</style>

```

router/index.js

```
import Vue from 'vue'
import Router from 'vue-router'
Vue.use(Router)

import Home from "../components/Home";
export default new Router({
  mode:"history",
  routes: [
    {
      path: '/',
      // name: 'HelloWorld',
      component: Home
    },
    {
      path: '/home/',
      // name: 'HelloWorld',  路由别名  url('',name='')
      component: Home,
    },
  ],

})

```





效果：

![1557460383648](assets/1557460383648.png)

这里代码用了之前vue的Header Footer 代码 做了很多修改



这里就可以通过git提交一个版本了

```git
git add .
git commit -m '前后端配合轮播图功能完成'
git push -u origin dev:dev

```





## 导航功能实现

### 创建模型

引入一个公共模型【抽象模型，不会在数据迁移的时候为它创建表】

apps/home/models.py

```python
from django.db import models
from luffyapi.utils.models import BaseModel
# Create your models here.
class Banner(BaseModel):
    """轮播广告图模型"""
    # 模型字段
    title = models.CharField(max_length=500, verbose_name="广告标题")
    link = models.CharField(max_length=500, verbose_name="广告链接")
    # upload_to 设置上传文件的保存子目录
    image_url =  models.ImageField(upload_to="banner", null=True, blank=True, max_length=255, verbose_name="广告图片")
    remark = models.TextField(verbose_name="备注信息")

    # 表信息声明
    class Meta:
        db_table = "ly_banner"
        verbose_name = "轮播广告"
        verbose_name_plural = verbose_name

    # 自定义方法[自定义字段或者自定义工具方法]
    def __str__(self):
        return self.title


class Nav(BaseModel):
    """导航菜单模型"""
    POSITION_OPTION = (
        (1, "顶部导航"),
        (2, "脚部导航"),
    )
    title = models.CharField(max_length=500, verbose_name="导航标题")
    link = models.CharField(max_length=500, verbose_name="导航链接")
    position = models.IntegerField(choices=POSITION_OPTION, default=1, verbose_name="导航位置")
    is_site = models.BooleanField(default=False, verbose_name="是否是站外地址")

    class Meta:
        db_table = 'ly_nav'
        verbose_name = '导航菜单'
        verbose_name_plural = verbose_name

    # 自定义方法[自定义字段或者自定义工具方法]
    def __str__(self):
        return self.title
```

公共模型，保存项目的公共代码库目录下luffy/utils/models.py文件中。

```python
from django.db import models

class BaseModel(models.Model):
    """公共模型"""
    is_show = models.BooleanField(default=False, verbose_name="是否显示")
    orders = models.IntegerField(default=1, verbose_name="排序")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
		#更新：update方法不能自动更新auto_now的时间，save()方法保存能够自动修改更新时间
    class Meta:
        # 设置当前模型为抽象模型，在数据迁移的时候django就不会为它单独创建一张表
        abstract = True
```



数据迁移

```python
python manage.py makemigrations
python manage.py migrate
```



### 序列化器代码

```python
from .models import Nav
class NavModelSerializer(serializers.ModelSerializer):
    """导航菜单序列化器"""
    class Meta:
        model = Nav
        fields = ["title","link","is_site"]
```



### 视图代码

views.py

```python
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Banner
from .serializers import BannerModelSerializer
from luffyapi.settings import constants

class BannerListAPIView(ListAPIView): # 自动导包
    """轮播广告视图"""
    queryset = Banner.objects.filter(is_show=True, is_deleted=False).order_by("-orders","-id")[:constants.BANNER_LENGTH]
    serializer_class = BannerModelSerializer

from .models import Nav
from .serializers import NavModelSerializer
class HeaderNavListAPIView(ListAPIView):
    """顶部导航菜单视图"""
    queryset = Nav.objects.filter(is_show=True, is_deleted=False,position=1).order_by("-orders","-id")[:constants.HEADER_NAV_LENGTH]
    serializer_class = NavModelSerializer



```

#### 常量配置

settings/constants.py，代码：

```python
# 首页展示的轮播广告数量
BANNER_LENGTH = 10
# 顶部导航的数量
HEADER_NAV_LENGTH = 7
# 脚部导航的数量
FOOTER_NAV_LENGTH = 7
```



### 路由代码

urls.py

```python
from django.urls import path,re_path
from . import views
urlpatterns = [
    path("banner/",views.BannerListAPIView.as_view()),
    path("nav/header/", views.HeaderNavListAPIView.as_view()),
    #path("nav/footer/", views.FooterNavListAPIView.as_view()),
]
```



### 注册导航模型到xadmin中

在当前子应用adminx.py，添加如下代码

```python
import xadmin
from xadmin import views

class BaseSetting(object):
    """xadmin的基本配置"""
    enable_themes = True  # 开启主题切换功能
    use_bootswatch = True

xadmin.site.register(views.BaseAdminView, BaseSetting)

class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "路飞学城"  # 设置站点标题
    site_footer = "路飞学城有限公司"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠

xadmin.site.register(views.CommAdminView, GlobalSettings)


# 轮播图
from .models import Banner
class BannerModelAdmin(object):
    list_display=["title","orders","is_show"]
xadmin.site.register(Banner, BannerModelAdmin)

# 导航菜单
from home.models import Nav
class NavModelAdmin(object):
    list_display=["title","link","is_show","is_site","position"]
xadmin.site.register(Nav, NavModelAdmin)
```

添加测试数据

![1557462133673](assets/1557462133673.png)

### 客户端代码获取数据

Header.vue代码：

```vue
<template>
  <div class="total-header">
    <div class="header">
    <el-container>
      <el-header height="80px" class="header-cont">
        <el-row>
          <el-col class="logo" :span="3">
            <a href="/">
              <img src="@/assets/head-logo.svg" alt="">

            </a>
          </el-col>
          <el-col class="nav" :span="10">
            <el-row>
                <el-col :span="3" v-for="(value,index) in nav_data_list" :key="value.id">

                  <router-link v-if="!value.is_site" :to="value.link" :class="{active:count===index}" @click="count=index">{{value.title}}</router-link>
                  <a v-else :href="value.link" :class="{active:count===index}">{{value.title}}</a>

                </el-col>

              </el-row>

          </el-col>
          <el-col :span="11" class="header-right-box">
            <div class="search">
              <input type="text" id="Input" placeholder="请输入想搜索的课程" style="" @blur="inputShowHandler" ref="Input" v-show="!s_status">
              <ul @click="ulShowHandler" v-show="s_status" class="search-ul">
                <span>Python</span>
                <span>Linux</span>
              </ul>
              <p>
                <img class="icon" src="@/assets/sousuo1.png" alt="" v-show="s_status">
                <img class="icon" src="@/assets/sousuo2.png" alt="" v-show="!s_status">
                <img class="new" src="@/assets/new.png" alt="">
              </p>
            </div>
            <div class="register" v-show="!token">
              <router-link to="/"><button class="signin">登录</button></router-link>
              &nbsp;&nbsp;|&nbsp;&nbsp;
<!--              <a target="_blank" href="">-->
                <router-link to="/"><button class="signup">注册</button></router-link>

<!--              </a>-->
            </div>
            <div class="shop-car" v-show="token">
              <router-link to="/">
                <b>6</b>
                <img src="@/assets/shopcart.png" alt="">
                <span>购物车 </span>
              </router-link>
            </div>
            <div class="nav-right-box" v-show="token">
                <div class="nav-right">
                  <router-link to="/">
                    <div class="nav-study">我的教室</div>
                  </router-link>
                  <div class="nav-img" @mouseover="personInfoList" @mouseout="personInfoOut">
                    <img src="@/assets/touxiang.png" alt="" style="border: 1px solid rgb(243, 243, 243);">
<!--                    hover &#45;&#45; mouseenter+mouseout-->
                    <ul class="home-my-account" v-show="list_status">
                      <li>
                        我的账户
                        <img src="@/assets/back.svg" alt="">
                      </li>
                      <li>
                        我的订单
                        <img src="@/assets/back.svg" alt="">
                      </li>
                      <li>
                        贝里小卖铺
                        <img src="@/assets/back.svg" alt="">
                      </li>
                      <li>
                        我的优惠券
                        <img src="@/assets/back.svg" alt="">
                      </li>
                      <li>
                        <span>
                          我的消息
                          <b>(26)</b>
                        </span>
                        <img src="@/assets/back.svg" alt="">
                      </li>
                      <li>
                        退出
                        <img src="@/assets/back.svg" alt="">
                      </li>

                    </ul>
                  </div>

                </div>

              </div>


          </el-col>
        </el-row>

      </el-header>


    </el-container>

  </div>
  </div>

</template>

<script>
    export default {
      name: "Header",
      data(){
        return {
          // 设置一个登录状态的标记，因为登录注册部分在登录之后会发生变化,false未登录转台
          token:true,
          count:0, //标记导航栏中哪一个有class类值为active的值
          s_status:true, //用来标记搜索框是否显示成input框
          list_status:false, //用来控制个人中心下拉菜单的动态显示，false不显示
          nav_data_list:[],
        }
      },
      methods:{
        ulShowHandler(){
          this.s_status = false;
          console.log(this.$refs.Input);

          // this.$refs.Input.focus();
          this.$nextTick(()=>{
            this.$refs.Input.focus();
          })

        },
        inputShowHandler(){
          console.log('xxxxx')
          this.s_status = true;
        },
        personInfoList(){
          this.list_status = true;
        },
        personInfoOut(){
          this.list_status = false;
        },
        get_nav_data(){
          this.$axios.get(`${this.$settings.Host}/home/nav/header/`,).then((res)=>{
            console.log(res.data);
            this.nav_data_list = res.data;
          })
          .catch((error)=>{
            console.log(error);
          })
        }
      },

      created() {
        this.get_nav_data();
      }

    }



</script>

<style scoped>
  .header-cont .nav .active{
    color: #f5a623;
    font-weight: 500;
    border-bottom: 2px solid #f5a623;
  }
  .total-header{
    min-width: 1200px;
    z-index: 100;
    box-shadow: 0 4px 8px 0 hsla(0,0%,59%,.1);
  }
  .header{
    width: 1200px;
    margin: 0 auto;
  }
  .header .el-header{
    padding: 0;
  }
  .logo{
    height: 80px;
    /*line-height: 80px;*/
    /*text-align: center;*/
    display: flex; /* css3里面的弹性布局，高度设定好之后，设置这个属性就能让里面的内容居中 */
    align-items: center;
  }
  .nav .el-row .el-col{
    height: 80px;
    line-height: 80px;
    text-align: center;

  }
  .nav a{
    font-size: 15px;
    font-weight: 400;
    cursor: pointer;
    color: #4a4a4a;
    text-decoration: none;
  }
  .nav .el-row .el-col a:hover{
    border-bottom: 2px solid #f5a623
  }

  .header-cont{
    position: relative;
  }
  .search input{
    width: 185px;
    height: 26px;
    font-size: 14px;
    color: #4a4a4a;
    border: none;
    border-bottom: 1px solid #ffc210;

    outline: none;
  }
  .search ul{
    width: 185px;
    height: 26px;
    display: flex;
    align-items: center;
    padding: 0;

    padding-bottom: 3px;
    border-bottom: 1px solid hsla(0,0%,59%,.25);
    cursor: text;
    margin: 0;
    font-family: Helvetica Neue,Helvetica,Microsoft YaHei,Arial,sans-serif;
  }
  .search .search-ul,.search #Input{
    padding-top:10px;
  }
  .search ul span {
    color: #545c63;
    font-size: 12px;
    padding: 3px 12px;
    background: #eeeeef;
    cursor: pointer;
    margin-right: 3px;
    border-radius: 11px;
  }
  .hide{
    display: none;
  }
  .search{
    height: auto;
    display: flex;
  }
  .search p{
    position: relative;
    margin-right: 20px;
    margin-left: 4px;
  }

  .search p .icon{
    width: 16px;
    height: 16px;
    cursor: pointer;
  }
  .search p .new{
    width: 18px;
    height: 10px;
    position: absolute;
    left: 15px;
    top: 0;
  }
  .register{
    height: 36px;
    display: flex;
    align-items: center;
    line-height: 36px;
  }
  .register .signin,.register .signup{
    font-size: 14px;
    color: #5e5e5e;
    white-space: nowrap;
  }
  .register button{
    outline: none;
    cursor: pointer;
    border: none;
    background: transparent;
  }
  .register a{
    color: #000;
    outline: none;
  }
  .header-right-box{
    height: 100%;
    display: flex;
    align-items: center;
    font-size: 15px;
    color: #4a4a4a;
    position: absolute;
    right: 0;
    top: 0;
  }
  .shop-car{
    width: 99px;
    height: 28px;
    border-radius: 15px;
    margin-right: 20px;
    background: #f7f7f7;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    cursor: pointer;
  }
  .shop-car b{
    position: absolute;
    left: 28px;
    top: -1px;
    width: 18px;
    height: 16px;
    color: #fff;
    font-size: 12px;
    font-weight: 350;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 50%;
    background: #ff0826;
    overflow: hidden;
    transform: scale(.8);
  }
  .shop-car img{
    width: 20px;
    height: 20px;
    margin-right: 7px;
  }

  .nav-right-box{
    position: relative;
  }
  .nav-right-box .nav-right{
    float: right;
    display: flex;
    height: 100%;
    line-height: 60px;
    position: relative;
  }
  .nav-right .nav-study{
    font-size: 15px;
    font-weight: 300;
    color: #5e5e5e;
    margin-right: 20px;
    cursor: pointer;

  }
  .nav-right .nav-study:hover{
    color:#000;
  }
  .nav-img img{
    width: 26px;
    height: 26px;
    border-radius: 50%;
    display: inline-block;
    cursor: pointer;
  }
  .home-my-account{
    position: absolute;
    right: 0;
    top: 60px;
    z-index: 101;
    width: 190px;
    height: auto;
    background: #fff;
    border-radius: 4px;
    box-shadow: 0 4px 8px 0 #d0d0d0;
  }
  li{
    list-style: none;
  }
  .home-my-account li{
    height: 40px;
    font-size: 14px;
    font-weight: 300;
    color: #5e5e5e;
    padding-left: 20px;
    padding-right: 20px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-sizing: border-box;
  }
  .home-my-account li img{
    cursor: pointer;
    width: 5px;
    height: 10px;
  }
  .home-my-account li span{
    height: 40px;
    display: flex;
    align-items: center;
  }
  .home-my-account li span b{
    font-weight: 300;
    margin-top: -2px;
  }

</style>

```

底部导航就不做了。





# 用户的登陆认证

## 前端显示登陆页面

### 登录页组件

Login.vue  

```vue
<template>
	<div class="login box">
		<img src="../../static/image/Loginbg.3377d0c.jpg" alt="">
		<div class="login">
			<div class="login-title">
				<img src="../../static/image/Logotitle.1ba5466.png" alt="">
				<p>帮助有志向的年轻人通过努力学习获得体面的工作和生活!</p>
			</div>
			<div class="login_box">
				<div class="title">
					<span @click="login_type=0">密码登录</span>
					<span @click="login_type=1">短信登录</span>
				</div>
				<div class="inp" v-if="login_type==0">
					<input v-model = "username" type="text" placeholder="用户名 / 手机号码" class="user">
					<input v-model = "password" type="password" name="" class="pwd" placeholder="密码">
					<div id="geetest1"></div>
					<div class="rember">
						<p>
							<input type="checkbox" class="no" name="a"/>
							<span>记住密码</span>
						</p>
						<p>忘记密码</p>
					</div>
					<button class="login_btn">登录</button>
					<p class="go_login" >没有账号 <span>立即注册</span></p>
				</div>
				<div class="inp" v-show="login_type==1">
					<input v-model = "username" type="text" placeholder="手机号码" class="user">
					<input v-model = "password"  type="text" class="pwd" placeholder="短信验证码">
          <button id="get_code">获取验证码</button>
					<button class="login_btn">登录</button>
					<p class="go_login" >没有账号 <span>立即注册</span></p>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
  name: 'Login',
  data(){
    return {
        login_type: 0,
        username:"",
        password:"",
    }
  },

  methods:{

  },

};
</script>

<style scoped>
.box{
	width: 100%;
  height: 100%;
	position: relative;
  overflow: hidden;
}
.box img{
	width: 100%;
  min-height: 100%;
}
.box .login {
	position: absolute;
	width: 500px;
	height: 400px;
	top: 0;
	left: 0;
  margin: auto;
  right: 0;
  bottom: 0;
  top: -338px;
}
.login .login-title{
     width: 100%;
    text-align: center;
}
.login-title img{
    width: 190px;
    height: auto;
}
.login-title p{
    font-family: PingFangSC-Regular;
    font-size: 18px;
    color: #fff;
    letter-spacing: .29px;
    padding-top: 10px;
    padding-bottom: 50px;
}
.login_box{
    width: 400px;
    height: auto;
    background: #fff;
    box-shadow: 0 2px 4px 0 rgba(0,0,0,.5);
    border-radius: 4px;
    margin: 0 auto;
    padding-bottom: 40px;
}
.login_box .title{
	font-size: 20px;
	color: #9b9b9b;
	letter-spacing: .32px;
	border-bottom: 1px solid #e6e6e6;
	 display: flex;
    	justify-content: space-around;
    	padding: 50px 60px 0 60px;
    	margin-bottom: 20px;
    	cursor: pointer;
}
.login_box .title span:nth-of-type(1){
	color: #4a4a4a;
    	border-bottom: 2px solid #84cc39;
}

.inp{
	width: 350px;
	margin: 0 auto;
}
.inp input{
    border: 0;
    outline: 0;
    width: 100%;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
}
.inp input.user{
    margin-bottom: 16px;
}
.inp .rember{
     display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    margin-top: 10px;
}
.inp .rember p:first-of-type{
    font-size: 12px;
    color: #4a4a4a;
    letter-spacing: .19px;
    margin-left: 22px;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-align: center;
    align-items: center;
    /*position: relative;*/
}
.inp .rember p:nth-of-type(2){
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .19px;
    cursor: pointer;
}

.inp .rember input{
    outline: 0;
    width: 30px;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
}

.inp .rember p span{
    display: inline-block;
  font-size: 12px;
  width: 100px;
  /*position: absolute;*/
/*left: 20px;*/

}
#geetest{
	margin-top: 20px;
}
.login_btn{
     width: 100%;
    height: 45px;
    background: #84cc39;
    border-radius: 5px;
    font-size: 16px;
    color: #fff;
    letter-spacing: .26px;
    margin-top: 30px;
}
.inp .go_login{
    text-align: center;
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .26px;
    padding-top: 20px;
}
.inp .go_login span{
    color: #84cc39;
    cursor: pointer;
}
</style>
```

### 绑定登陆页面路由地址

main.js  

```javascript
import Vue from "vue"
import Router from "vue-router"

// 导入需要注册路由的组件
import Home from "../components/Home"
import Login from "../components/Login"
Vue.use(Router);

// 配置路由列表
export default new Router({
  mode:"history",
  routes:[
    // 路由列表
		...
    {
      name:"Login",
      path: "/user/login",
      component:Login,
    }
  ]
})
```

#### 调整首页头部子组件中登陆按钮的链接信息

Header.vue

```vue
<router-link to="/user/login">登录</router-link>
```





## 后端实现登陆认证

Django默认已经提供了认证系统Auth模块，我们认证的时候，会使用auth模块里面给我们提供的表。认证系统包含：

- 用户管理
- 权限
- 用户组
- 密码哈希系统
- 用户登录或内容显示的表单和视图
- 一个可插拔的后台系统 admin

Django默认用户的认证机制依赖Session机制，我们在项目中将引入JWT认证机制，将用户的身份凭据存放在Token中，然后对接Django的认证系统，帮助我们来实现：

- 用户的数据模型
- 用户密码的加密与验证
- 用户的权限系统



### Django用户模型类

Django认证系统中提供了用户模型类User保存用户的数据，默认的User包含以下常见的基本字段：

| 字段名             | 字段描述                                                     |
| ------------------ | ------------------------------------------------------------ |
| `username`         | 必选。150个字符以内。 用户名可能包含字母数字，`_`，`@`，`+` `.` 和`-`个字符。 |
| `first_name`       | 可选（`blank=True`）。 少于等于30个字符。                    |
| `last_name`        | 可选（`blank=True`）。 少于等于30个字符。                    |
| `email`            | 可选（`blank=True`）。 邮箱地址。                            |
| `password`         | 必选。 密码的哈希加密串。 （Django 不保存原始密码）。 原始密码可以无限长而且可以包含任意字符。 |
| `groups`           | 与`Group` 之间的多对多关系。                                 |
| `user_permissions` | 与`Permission` 之间的多对多关系。                            |
| `is_staff`         | 布尔值。 设置用户是否可以访问Admin 站点。                    |
| `is_active`        | 布尔值。 指示用户的账号是否激活。 它不是用来控制用户是否能够登录，而是描述一种帐号的使用状态。 |
| `is_superuser`     | 是否是超级用户。超级用户具有所有权限。                       |
| `last_login`       | 用户最后一次登录的时间。                                     |
| `date_joined`      | 账户创建的时间。 当账号创建时，默认设置为当前的date/time。   |

上面缺少一些字段，所以后面我们会对它进行改造，比如说它里面没有手机号字段，后面我们需要加上。

##### 常用方法：

- `set_password`(*raw_password*)

  设置用户的密码为给定的原始字符串，并负责密码的。 不会保存`User` 对象。当`None`为`raw_password` 时，密码将设置为一个不可用的密码。

- `check_password`(*raw_password*)

  如果给定的raw_password是用户的真实密码，则返回True，可以在校验用户密码时使用。

##### 管理器方法：

管理器方法即可以通过`User.objects.` 进行调用的方法。

- `create_user`(*username*, *email=None*, *password=None*, **\*extra_fields*)

  创建、保存并返回一个`User`对象。

- `create_superuser`(*username*, *email*, *password*, **\*extra_fields*)

  与`create_user()` 相同，但是设置`is_staff` 和`is_superuser` 为`True`。



### 创建用户模块的子应用

```shell
python ../../manage.py startapp users
```

在settings.py文件中注册子应用。

```python
INSTALLED_APPS = [
		...
  	'users',
]
```



### 创建自定义的用户模型类

Django认证系统中提供的用户模型类及方法很方便，我们可以使用这个模型类，但是字段有些无法满足项目需求，如本项目中需要保存用户的手机号，需要给模型类添加额外的字段。

Django提供了`django.contrib.auth.models.AbstractUser`用户抽象模型类允许我们继承，扩展字段来使用Django认证系统的用户模型类。

**我们可以在apps中创建Django应用users，并在配置文件中注册users应用。**

在创建好的应用models.py中定义用户的用户模型类。目前我们是将所有用户都放到一个表里面的，比如管理员，老师(上传课程)，客户等等，以后我们通过用户组进行用户划分

```python
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    """用户模型类"""
    mobile = models.CharField(max_length=15, unique=True, verbose_name='手机号码')
    avatar = models.ImageField(upload_to='avatar',verbose_name='用户头像',null=True,blank=True)

    class Meta:
        db_table = 'ly_user'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
```

我们自定义的用户模型类还不能直接被Django的认证系统所识别，需要在配置文件中告知Django认证系统使用我们自定义的模型类。

在配置文件中进行设置

```python
#注册自定义用户模型，格式：“应用名.模型类名”
AUTH_USER_MODEL = 'users.User'
```

`AUTH_USER_MODEL` 参数的设置以`点.`来分隔，表示`应用名.模型类名`。

**注意：Django建议我们对于AUTH_USER_MODEL参数的设置一定要在第一次数据库迁移之前就设置好，否则后续使用可能出现未知错误。**

执行数据库迁移

```shell
python manage.py makemigrations
python manage.py migrate
```

如果在第一次数据迁移以后，才设置AUTH_USER_MODEL自定义用户模型，则会报错。解决方案如下：

```python
0. 先把现有的数据库导出备份，然后清掉数据库中所有的数据表。 mysqldump -hlocalhost -uroot -p123 -p luffy > luffy.sql
1. 把开发者创建的所有子应用下面的migrations目录下除了__init__.py以外的所有迁移文件，只要涉及到用户的，一律删除,并将django-migrations表中的数据全部删除。
2. 把django.contrib.admin.migrations目录下除了__init__.py以外的所有迁移文件，全部删除。
3. 把django.contrib.auth.migrations目录下除了__init__.py以外的所有迁移文件，全部删除。
4. 把reversion.migrations目录下除了__init__.py以外的所有迁移文件，全部删除。这个不在django目录里面，在site-packages里面，是xadmin安装的时候带的，它会记录用户信息，也需要删除
5. 把xadmin.migrations目录下除了__init__.py以外的所有迁移文件，全部删除。
6. 删除我们当前数据库中的所有表   
SELECT concat('DROP TABLE IF EXISTS ', table_name, ';') FROM information_schema.tables WHERE table_schema = 'luffy';
7. 接下来，执行数据迁移(makemigrations和migrate)，回顾第0步中的数据，将数据导入就可以了，以后如果要修改用户相关数据，不需要重复本次操作，直接数据迁移即可。
mysql -uroot -p luffy < luffy.sql
```





### Django REST framework JWT

在用户注册或登录后，我们想记录用户的登录状态，或者为用户创建身份认证的凭证。我们不再使用Session认证机制，而使用Json Web Token认证机制。

很多公司开发的一些移动端可能不支持cookie，并且我们通过cookie和session做接口登录认证的话，效率其实并不是很高，我们的接口可能提供给多个客户端，session数据保存在服务端，那么就需要每次都调用session数据进行验证，比较耗时，所以引入了token认证的概念，我们也可以通过token来完成，我们来看看jwt是怎么玩的。

```
Json web token (JWT), 是为了在网络应用环境间传递声明而执行的一种基于JSON的开放标准（(RFC 7519).该token被设计为紧凑且安全的，特别适用于分布式站点的单点登录（SSO）场景。JWT的声明一般被用来在身份提供者和服务提供者间传递被认证的用户身份信息，以便于从资源服务器获取资源，也可以增加一些额外的其它业务逻辑所必须的声明信息，该token也可直接被用于认证，也可被加密。
```



看图

![image-20200526175605253](2-%E9%A6%96%E9%A1%B5%E5%92%8C%E7%99%BB%E5%BD%95%E6%B3%A8%E5%86%8C.assets/image-20200526175605253.png)

### JWT的构成

JWT就一段字符串，由三段信息构成的，将这三段信息文本用`.`链接一起就构成了Jwt字符串。就像这样:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ
```

第一部分我们称它为头部（header),第二部分我们称其为载荷（payload, 类似于飞机上承载的物品)，第三部分是签证（signature).



### header

jwt的头部承载两部分信息：

- 声明类型，这里是jwt
- 声明加密的算法 通常直接使用 HMAC SHA256

完整的头部就像下面这样的JSON：

```
{
  'typ': 'JWT',
  'alg': 'HS256'
}
```

然后将头部进行base64.b64encode()加密（该加密是可以对称解密的),构成了第一部分.

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
```

python中base64加密解密

```python
import base64
str1 = 'admin'
str2 = str1.encode()
b1 = base64.b64encode(str2) #数据越多，加密后的字符串越长
b2 = base64.b64decode(b1) #admin
各个语言中都有base64加密解密的功能，所以我们jwt为了安全，需要配合第三段加密
```



### payload

载荷就是存放有效信息的地方。这个名字像是特指飞机上承载的货品，这些有效信息可以存放下面三个部分信息。

- 标准中注册的声明
- 公共的声明
- 私有的声明

**标准中注册的声明** (建议但不强制使用) ：

- **iss**: jwt签发者
- **sub**: jwt所面向的用户
- **aud**: 接收jwt的一方
- **exp**: jwt的过期时间，这个过期时间必须要大于签发时间
- **nbf**: 定义在什么时间之前，该jwt都是不可用的.
- **iat**: jwt的签发时间
- **jti**: jwt的唯一身份标识，主要用来作为一次性token,从而回避重放攻击。

  以上是JWT 规定的7个官方字段，供选用

**公共的声明** ： 公共的声明可以添加任何的信息，一般添加用户的相关信息或其他业务需要的必要信息.但不建议添加敏感信息，因为该部分在客户端可解密.

**私有的声明** ： 私有声明是提供者和消费者所共同定义的声明，一般不建议存放敏感信息，因为base64是对称解密的，意味着该部分信息可以归类为明文信息。

定义一个payload，json格式的数据:

```
{
  "sub": "1234567890",
  "exp": "3422335555", #时间戳形式
  "name": "John Doe",
  "admin": true
}
```

然后将其进行base64.b64encode() 加密，得到JWT的第二部分。

```
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9
```

### signature

JWT的第三部分是一个签证信息，这个签证信息由三部分组成：

- header (base64后的)
- payload (base64后的)
- secret密钥

这个部分需要base64加密后的header和base64加密后的payload使用`.`连接组成的字符串，然后通过header中声明的加密方式进行加盐`secret`组合加密，然后就构成了jwt的第三部分。

```
// javascript
var encodedString = base64UrlEncode(header) + '.' + base64UrlEncode(payload);

var signature = HMACSHA256(encodedString, 'secret'); // TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ
```

将这三部分用`.`连接成一个完整的字符串,构成了最终的jwt:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ
```

**注意：secret是保存在服务器端的，jwt的签发生成也是在服务器端的，secret就是用来进行jwt的签发和jwt的验证，所以，它就是你服务端的私钥，在任何场景都不应该流露出去。一旦客户端得知这个secret, 那就意味着客户端是可以自我签发jwt了。**

```
jwt的优点：
1. 实现分布式的单点登陆非常方便
2. 数据实际保存在客户端，所以我们可以分担服务器的存储压力
3. JWT不仅可用于认证，还可用于信息交换。善用JWT有助于减少服务器请求数据库的次数，jwt的构成非常简单，字节占用很小，所以它是非常便于传输的。

jwt的缺点：
1. 数据保存在了客户端，我们服务端只认jwt，不识别客户端。
2. jwt可以设置过期时间，但是因为数据保存在了客户端，所以对于过期时间不好调整。#secret_key轻易不要改，一改所有客户端都要重新登录
```

认证流程图

![image-20200526181217337](2-%E9%A6%96%E9%A1%B5%E5%92%8C%E7%99%BB%E5%BD%95%E6%B3%A8%E5%86%8C.assets/image-20200526181217337.png)



**关于签发和核验JWT，我们可以使用Django REST framework JWT扩展来完成。**

[文档网站http://getblimp.github.io/django-rest-framework-jwt/](http://getblimp.github.io/django-rest-framework-jwt/)



### 安装配置JWT

安装

```shell
pip install djangorestframework-jwt -i https://mirrors.aliyun.com/pypi/simple/
```

配置(github网址：https://github.com/jpadilla/django-rest-framework-jwt)

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}
import datetime
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1), 
}
```

- JWT_EXPIRATION_DELTA 指明token的有效期



我们django创建项目的时候，在settings配置文件中直接就给生成了一个serect_key，我们直接可以使用它作为我们jwt的serect_key,其实djangorestframework-jwt默认配置中就使用的它。



### 手动生成jwt（我们暂时用不到）

Django REST framework JWT 扩展的说明文档中提供了手动签发JWT的方法

```python
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

payload = jwt_payload_handler(user)
token = jwt_encode_handler(payload)
```



在用户注册或登录成功后，在序列化器中返回用户信息以后同时返回token即可。

### 后端实现登陆认证接口

Django REST framework JWT提供了登录获取token的视图，可以直接使用

在子应用路由users/urls.py中

```python
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path(r'login/', obtain_jwt_token),
]
```

在主路由中，引入当前子应用的路由文件

```python
urlpatterns = [
		...
    path('user/', include("users.urls")),
    # include 的值必须是 模块名.urls 格式,字符串中间只能出现一个圆点
]
```



手动创建一个超级用户

```BASH
python manage.py createsuperuser
```



接下来，我们可以通过postman来测试下功能，但是jwt是通过username和password来进行登录认证处理的，所以我们要给真实数据，jwt会去我们配置的user表中去查询用户数据的。

![image-20200526184032452](2-%E9%A6%96%E9%A1%B5%E5%92%8C%E7%99%BB%E5%BD%95%E6%B3%A8%E5%86%8C.assets/image-20200526184032452.png)





## 前端实现登陆功能

在登陆组件中找到登陆按钮，绑定点击事件

```html
<button class="login_btn" @click="loginhander">登录</button>
```

在methods中请求后端

```javascript
export default {
  name: 'Login',
  data(){
    return {
        login_type: 0,
        remember:false, // 记住密码
        username:"",
        password:"",
    }
  },

  methods:{
    // 登录
    loginhander(){
      this.$axios.post("http://127.0.0.1:8000/users/authorizations/",{"username":this.username,"password":this.password}).then(response=>{
        console.log(response.data)
      }).catch(error=>{
        console.log(error)
      })
    }
  },

};
```



### 2.3.7 前端保存jwt

我们可以将JWT保存在cookie中，也可以保存在浏览器的本地存储里，我们保存在浏览器本地存储中

浏览器的本地存储提供了sessionStorage 和 localStorage 两种，从属于window对象：

- **sessionStorage** 浏览器关闭即失效
- **localStorage** 长期有效

使用方法

```js
sessionStorage.变量名 = 变量值   // 保存数据
sessionStorage.setItem("变量名","变量值") // 保存数据
sessionStorage.变量名  // 读取数据
sessionStorage.getItem("变量名") // 读取数据
sessionStorage.removeItem("变量名") // 清除单个数据
sessionStorage.clear()  // 清除所有sessionStorage保存的数据

localStorage.变量名 = 变量值   // 保存数据
localStorage.setItem("变量名","变量值") // 保存数据
localStorage.变量名  // 读取数据
localStorage.getItem("变量名") // 读取数据
localStorage.removeItem("变量名") // 清除单个数据
localStorage.clear()  // 清除所有sessionStorage保存的数据
```

登陆组件代码Login.vue

```javascript
	// 使用浏览器本地存储保存token
  if (this.remember) {
    // 记住登录
    sessionStorage.clear();
    localStorage.token = response.data.token;
  } else {
    // 未记住登录
    localStorage.clear();
    sessionStorage.token = response.data.token;
  }
	// 页面跳转回到上一个页面 也可以使用 this.$router.push("/") 回到首页
	this.$router.go(-1)
```



默认的返回值仅有token，我们还需在返回值中增加username和id，方便在客户端页面中显示当前登陆用户

通过修改该视图的返回值可以完成我们的需求。

在user/utils.py 中，创建

```python
def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'id': user.id,
        'username': user.username
    }
```

修改settings/dev.py配置文件

```python
# JWT
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.utils.jwt_response_payload_handler',
}
```

登陆组件代码Login.vue

```javascript
	// 使用浏览器本地存储保存token
  if (this.remember) {
    // 记住登录
    sessionStorage.clear();
    localStorage.token = response.data.token;
    localStorage.id = response.data.id;
    localStorage.username = response.data.username;
  } else {
    // 未记住登录
    localStorage.clear();
    sessionStorage.token = response.data.token;
    sessionStorage.id = response.data.id;
    sessionStorage.username = response.data.username;
  }
	//登录成功之后，提示用户，然后用户点击确定，就跳转到首页
	let ths = this;
  this.$alert('登录成功！','路飞学城',{  #element-ui的alert需要三个参数，提示信息，标题，{callback回调函数}
    callback(){
      ths.$router.push('/');  
    }
  })
```



### 2.3.9 多条件登录

JWT扩展的登录视图，在收到用户名与密码时，也是调用Django的认证系统中提供的**authenticate()**来检查用户名与密码是否正确。

我们可以通过修改Django认证系统的认证后端（主要是authenticate方法）来支持登录账号既可以是用户名也可以是手机号。

**官方说：修改Django认证系统的认证后端需要继承django.contrib.auth.backends.ModelBackend，并重写authenticate方法。**

`authenticate(self, request, username=None, password=None, **kwargs)`方法的参数说明：

- request 本次认证的请求对象
- username 本次认证提供的用户账号
- password 本次认证提供的密码

**我们想要让用户既可以以用户名登录，也可以以手机号登录，那么对于authenticate方法而言，username参数即表示用户名或者手机号。**

重写authenticate方法的思路：

1. 根据username参数查找用户User对象，username参数可能是用户名，也可能是手机号
2. 若查找到User对象，调用User对象的check_password方法检查密码是否正确

在users应用下创建一个utils.py中编写：

```python
def get_user_by_account(account):
    """
    根据帐号获取user对象
    :param account: 账号，可以是用户名，也可以是手机号
    :return: User对象 或者 None
    """
    try:
        user = models.User.objects.filter(Q(username=account)|Q(mobile=account)).first()
    except models.User.DoesNotExist:
        return None
    else:
        return user

from . import models
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend

class UsernameMobileAuthBackend(ModelBackend):
    """
    自定义用户名或手机号认证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)
        #if user is not None and user.check_password(password) :
        if user is not None and user.check_password(password) and user.is_authenticated:
            #user.is_authenticated是看他有没有权限的，这里可以不加上它
            return user
```

在配置文件settings/dev.py中告知Django使用我们自定义的认证后端

```python
AUTHENTICATION_BACKENDS = [
    'users.utils.UsernameMobileAuthBackend',
]
```



以上就实现了我们通过用户名或者手机号的一个多条件登录。



跳转到首页之后，我们需要显示的不再是登录注册按钮，而是显示购物车，个人中心等内容，所以我们需要调增一下我们的Header.vue组件。





## 前端首页实现登陆状态的判断

common/Header.vue组件代码：

```vue
<template>
  <div class="total-header">
    <div class="header">
    <el-container>
      <el-header height="80px" class="header-cont">
        <el-row>
          <el-col class="logo" :span="3">
            <a href="/">
              <img src="@/assets/head-logo.svg" alt="">

            </a>
          </el-col>
          <el-col class="nav" :span="10">
            <el-row>
                <el-col :span="3" v-for="(value,index) in nav_data_list" :key="value.id">

                  <router-link v-if="!value.is_site" :to="value.link" :class="{active:count===index}" @click="count=index">{{value.title}}</router-link>
                  <a v-else :href="value.link" :class="{active:count===index}">{{value.title}}</a>

                </el-col>

              </el-row>

          </el-col>
          <el-col :span="11" class="header-right-box">
            <div class="search">
              <input type="text" id="Input" placeholder="请输入想搜索的课程" style="" @blur="inputShowHandler" ref="Input" v-show="!s_status">
              <ul @click="ulShowHandler" v-show="s_status" class="search-ul">
                <span>Python</span>
                <span>Linux</span>
              </ul>
              <p>
                <img class="icon" src="@/assets/sousuo1.png" alt="" v-show="s_status">
                <img class="icon" src="@/assets/sousuo2.png" alt="" v-show="!s_status">
                <img class="new" src="@/assets/new.png" alt="">
              </p>
            </div>
            <div class="register" v-show="!token">
              <router-link to="/user/login"><button class="signin">登录</button></router-link>
              &nbsp;&nbsp;|&nbsp;&nbsp;
<!--              <a target="_blank" href="">-->
                <router-link to="/"><button class="signup">注册</button></router-link>

<!--              </a>-->
            </div>
            <div class="shop-car" v-show="token">
              <router-link to="/">
                <b>6</b>
                <img src="@/assets/shopcart.png" alt="">
                <span>购物车 </span>
              </router-link>
            </div>
            <div class="nav-right-box" v-show="token">
                <div class="nav-right">
                  <router-link to="/">
                    <div class="nav-study">我的教室</div>
                  </router-link>
                  <div class="nav-img" @mouseover="personInfoList" @mouseout="personInfoOut">
                    <img src="@/assets/touxiang.png" alt="" style="border: 1px solid rgb(243, 243, 243);">
<!--                    hover &#45;&#45; mouseenter+mouseout-->
                    <ul class="home-my-account" v-show="list_status">
                      <li>
                        我的账户
                        <img src="https://hcdn1.luffycity.com/static/frontend/activity/back_1568185800.821227.svg" alt="">
                      </li>
                      <li>
                        我的订单
                        <img src="https://hcdn1.luffycity.com/static/frontend/activity/back_1568185800.821227.svg" alt="">
                      </li>
                      <li>
                        贝里小卖铺
                        <img src="https://hcdn1.luffycity.com/static/frontend/activity/back_1568185800.821227.svg" alt="">
                      </li>
                      <li>
                        我的优惠券
                        <img src="https://hcdn1.luffycity.com/static/frontend/activity/back_1568185800.821227.svg" alt="">
                      </li>
                      <li>
                        <span>
                          我的消息
                          <b>(26)</b>
                        </span>
                        <img src="https://hcdn1.luffycity.com/static/frontend/activity/back_1568185800.821227.svg" alt="">
                      </li>
                      <li>
                        退出
                        <img src="https://hcdn1.luffycity.com/static/frontend/activity/back_1568185800.821227.svg" alt="">
                      </li>

                    </ul>
                  </div>

                </div>

              </div>


          </el-col>
        </el-row>

      </el-header>


    </el-container>

  </div>
  </div>

</template>

<script>
    export default {
      name: "Header",
      data(){
        return {
          // 设置一个登录状态的标记，因为登录注册部分在登录之后会发生变化,false未登录转台
          token:false,
          count:0, //标记导航栏中哪一个有class类值为active的值
          s_status:true, //用来标记搜索框是否显示成input框
          list_status:false, //用来控制个人中心下拉菜单的动态显示，false不显示
          nav_data_list:[],
        }
      },
      methods:{
        ulShowHandler(){
          this.s_status = false;
          console.log(this.$refs.Input);

          // this.$refs.Input.focus();
          this.$nextTick(()=>{
            this.$refs.Input.focus();
          })

        },
        inputShowHandler(){
          console.log('xxxxx')
          this.s_status = true;
        },
        personInfoList(){
          this.list_status = true;
        },
        personInfoOut(){
          this.list_status = false;
        },
        get_nav_data(){
          this.$axios.get(`${this.$settings.HOST}/nav/header/`,).then((res)=>{
            console.log(res.data);
            this.nav_data_list = res.data;
          })
          .catch((error)=>{
            console.log(error);
          })
        },

        check_user_login(){
          // let t = sessionStorage.token || localStorage.token;
          // console.log('>>>',t);
          // if (t){
          //   this.token = true;
          // }
          // else {
          //   this.token = false;
          // }
          // return t
          // 从sessionStorage或者localStorage里面去token来判断是否已经登录了
          this.token = sessionStorage.user_token || localStorage.user_token
        }
      },

      created() {
        this.get_nav_data();
        //检查用户登录状态
        this.check_user_login();
      }

    }



</script>

<style scoped>
  .header-cont .nav .active{
    color: #f5a623;
    font-weight: 500;
    border-bottom: 2px solid #f5a623;
  }
  .total-header{
    min-width: 1200px;
    z-index: 100;
    box-shadow: 0 4px 8px 0 hsla(0,0%,59%,.1);
  }
  .header{
    width: 1200px;
    margin: 0 auto;
  }
  .header .el-header{
    padding: 0;
  }
  .logo{
    height: 80px;
    /*line-height: 80px;*/
    /*text-align: center;*/
    display: flex; /* css3里面的弹性布局，高度设定好之后，设置这个属性就能让里面的内容居中 */
    align-items: center;
  }
  .nav .el-row .el-col{
    height: 80px;
    line-height: 80px;
    text-align: center;

  }
  .nav a{
    font-size: 15px;
    font-weight: 400;
    cursor: pointer;
    color: #4a4a4a;
    text-decoration: none;
  }
  .nav .el-row .el-col a:hover{
    border-bottom: 2px solid #f5a623
  }

  .header-cont{
    position: relative;
  }
  .search input{
    width: 185px;
    height: 26px;
    font-size: 14px;
    color: #4a4a4a;
    border: none;
    border-bottom: 1px solid #ffc210;

    outline: none;
  }
  .search ul{
    width: 185px;
    height: 26px;
    display: flex;
    align-items: center;
    padding: 0;

    padding-bottom: 3px;
    border-bottom: 1px solid hsla(0,0%,59%,.25);
    cursor: text;
    margin: 0;
    font-family: Helvetica Neue,Helvetica,Microsoft YaHei,Arial,sans-serif;
  }
  .search .search-ul,.search #Input{
    padding-top:10px;
  }
  .search ul span {
    color: #545c63;
    font-size: 12px;
    padding: 3px 12px;
    background: #eeeeef;
    cursor: pointer;
    margin-right: 3px;
    border-radius: 11px;
  }
  .hide{
    display: none;
  }
  .search{
    height: auto;
    display: flex;
  }
  .search p{
    position: relative;
    margin-right: 20px;
    margin-left: 4px;
  }

  .search p .icon{
    width: 16px;
    height: 16px;
    cursor: pointer;
  }
  .search p .new{
    width: 18px;
    height: 10px;
    position: absolute;
    left: 15px;
    top: 0;
  }
  .register{
    height: 36px;
    display: flex;
    align-items: center;
    line-height: 36px;
  }
  .register .signin,.register .signup{
    font-size: 14px;
    color: #5e5e5e;
    white-space: nowrap;
  }
  .register button{
    outline: none;
    cursor: pointer;
    border: none;
    background: transparent;
  }
  .register a{
    color: #000;
    outline: none;
  }
  .header-right-box{
    height: 100%;
    display: flex;
    align-items: center;
    font-size: 15px;
    color: #4a4a4a;
    position: absolute;
    right: 0;
    top: 0;
  }
  .shop-car{
    width: 99px;
    height: 28px;
    border-radius: 15px;
    margin-right: 20px;
    background: #f7f7f7;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    cursor: pointer;
  }
  .shop-car b{
    position: absolute;
    left: 28px;
    top: -1px;
    width: 18px;
    height: 16px;
    color: #fff;
    font-size: 12px;
    font-weight: 350;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 50%;
    background: #ff0826;
    overflow: hidden;
    transform: scale(.8);
  }
  .shop-car img{
    width: 20px;
    height: 20px;
    margin-right: 7px;
  }

  .nav-right-box{
    position: relative;
  }
  .nav-right-box .nav-right{
    float: right;
    display: flex;
    height: 100%;
    line-height: 60px;
    position: relative;
  }
  .nav-right .nav-study{
    font-size: 15px;
    font-weight: 300;
    color: #5e5e5e;
    margin-right: 20px;
    cursor: pointer;

  }
  .nav-right .nav-study:hover{
    color:#000;
  }
  .nav-img img{
    width: 26px;
    height: 26px;
    border-radius: 50%;
    display: inline-block;
    cursor: pointer;
  }
  .home-my-account{
    position: absolute;
    right: 0;
    top: 60px;
    z-index: 101;
    width: 190px;
    height: auto;
    background: #fff;
    border-radius: 4px;
    box-shadow: 0 4px 8px 0 #d0d0d0;
  }
  li{
    list-style: none;
  }
  .home-my-account li{
    height: 40px;
    font-size: 14px;
    font-weight: 300;
    color: #5e5e5e;
    padding-left: 20px;
    padding-right: 20px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-sizing: border-box;
  }
  .home-my-account li img{
    cursor: pointer;
    width: 5px;
    height: 10px;
  }
  .home-my-account li span{
    height: 40px;
    display: flex;
    align-items: center;
  }
  .home-my-account li span b{
    font-weight: 300;
    margin-top: -2px;
  }


</style>

```



再做一个退出登陆，Header.vue

```vue
<li @click="logoutHandler">退出<img src="https://hcdn1.luffycity.com/static/frontend/activity/back_1568185800.821227.svg" alt=""></li>

                  
<script>
    export default {
      name: "Header",
      data(){
        return {
          // 设置一个登录状态的标记，因为登录注册部分在登录之后会发生变化,false未登录转台
          token:false,
          count:0, //标记导航栏中哪一个有class类值为active的值
          s_status:true, //用来标记搜索框是否显示成input框
          list_status:false, //用来控制个人中心下拉菜单的动态显示，false不显示
          nav_data_list:[],
        }
      },
      methods:{
        ...

        check_user_login(){
          
          this.token = sessionStorage.user_token || localStorage.user_token;
        },

        //退出登录
        logoutHandler(){
          //clear是清除所有的保存内容，可能有其他同事也通过localStorage等保存了数据，给人家清除了就不好了，对吧，所以我们加了哪些就清除哪些
          // localStorage.clear();
          localStorage.removeItem("user_token");
          localStorage.removeItem("user_id");
          localStorage.removeItem("user_name");
          sessionStorage.removeItem("user_token");
          sessionStorage.removeItem("user_id");
          sessionStorage.removeItem("user_name");
          //别忘了再次执行一下判断登录状态的操作
          this.check_user_login();
        }
      },

      created() {
        this.get_nav_data();
        //检查用户登录状态
        this.check_user_login();
      }

    }

```





为了防止人机程序自动登录，那么我们接入滑动验证码。

## 在登录认证中接入极验验证

官网： https://www.geetest.com/first_page/

注册登录以后，即进入登录后台，选择行为验证。

![1553576294430](assets/1553576294430.png)

![1553576382897](assets/1553576382897.png)



![1553576348110](assets/1553576348110.png)



![1553576402354](assets/1553576402354.png)





接下来，就可以根据官方文档，把验证码集成到项目中了

文档地址：https://docs.geetest.com/install/overview/start/

下载和安装验证码模块包。

```shell
git clone https://github.com/GeeTeam/gt3-python-sdk.git
```

安装依赖模块

```python
pip install requests
```



把验证码模块放在utils中

![1553578068434](assets/1553578068434.png)

并在user子应用下创建验证码视图类，并提供验证码和校验验证码的视图方法。

```python
from django.shortcuts import render,HttpResponse
pc_geetest_id = "5e876edb2bda195c265416b70e7389a7"
pc_geetest_key = "c1f0f6f5958507924d187db31cd136e5"

#上面的不行就用下面的
#pc_geetest_id = "8845ffc862dc0597b30f78831369a27b"
#pc_geetest_key = "2dc2dde1477594e1aebc5534ba3c080f"
# Create your views here.
from luffyapi.libs.geetest import GeetestLib
from rest_framework.response import Response
from .utils import get_user_by_account
from rest_framework import status as http_status
from rest_framework.views import APIView
class CaptchaAPIView(APIView):
    """验证码视图类"""
    status = False
    user_id = 0
    def get(self,request):
        """获取验证码"""
        username = request.query_params.get("username")
        user = get_user_by_account(username)
        if user is None:
            return Response({"message":"对不起，用户不存在！"},status=http_status.HTTP_400_BAD_REQUEST)

        self.user_id = user.id
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        self.status = gt.pre_process(self.user_id)
        # todo 后面增加status和user_id保存到redis数据库
        response_str = gt.get_response_str()
        #return Response(response_str)
      	return HttpResponse(response_str)

    def post(self,request):
        """验证码的验证方法"""
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        if self.status:
            result = gt.success_validate(challenge, validate, seccode, self.user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        result = {"status":"success"} if result else {"status":"fail"}
        return Response(result)
```

路由注册：

```python
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from . import views
urlpatterns = [
    # path(r"banner/", views.BannerListAPIView.as_view()),
    path(r"login/", obtain_jwt_token),
    path(r"captcha/", views.CaptchaAPIView.as_view()),
]
```



#### 前端获取显示并校验验证码

把下载会哦图的验证码模块包中的gt.js放置到前端项目中，并在main.js中引入

```javascript
// 导入gt极验
import '../static/js/gt.js'
```



注意：将我们reset.css文件中的这个一段，里面的input去掉，不然看不到效果。

```
input,select,textarea{
  border: none;
  outline: none;
}
```



Login.vue代码

```vue
<template>
	<div class="login box">
		<img src="../../static/image/Loginbg.3377d0c.jpg" alt="">
		<div class="login">
			<div class="login-title">
				<img src="../../static/image/Logotitle.1ba5466.png" alt="">
				<p>帮助有志向的年轻人通过努力学习获得体面的工作和生活!</p>
			</div>
			<div class="login_box">
				<div class="title">
					<span @click="login_type=0">密码登录</span>
					<span @click="login_type=1">短信登录</span>
				</div>
				<div class="inp" v-if="login_type==0">
					<input v-model = "username" type="text" placeholder="用户名 / 手机号码" class="user">
					<input v-model = "password" type="password" name="" class="pwd" placeholder="密码">
					<div id="geetest1"></div>
					<div class="rember">
						<p>
							<input type="checkbox" class="no" v-model="remember"/>
							<span>记住密码</span>
						</p>
						<p>忘记密码</p>
					</div>
					<button class="login_btn" @click="get_geetest_captcha">登录</button>
					<p class="go_login" >没有账号 <span>立即注册</span></p>
				</div>
				<div class="inp" v-show="login_type==1">
					<input v-model = "username" type="text" placeholder="手机号码" class="user">
					<input v-model = "password"  type="text" class="pwd" placeholder="短信验证码">
          <button id="get_code">获取验证码</button>
					<button class="login_btn">登录</button>
					<p class="go_login" >没有账号 <span>立即注册</span></p>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
  name: 'Login',
  data(){
    return {
        login_type: 0,
        username:"",
        password:"",
        remember:false,
    }
  },
  methods:{
    loginHander(){
        // 用户密码账号登录
        this.$axios.post(`${this.$settings.HOST}/user/login/`,{
            username:this.username,
            password:this.password,
        }).then(response=>{
            if(this.remember){
                // 记住登录状态
                sessionStorage.removeItem("user_token");
                sessionStorage.removeItem("user_id");
                sessionStorage.removeItem("user_name");
                localStorage.user_token = response.data.token;
                localStorage.user_id = response.data.id;
                localStorage.user_name = response.data.username;
            }else{
                // 不记住登录状态
                localStorage.removeItem("user_token");
                localStorage.removeItem("user_id");
                localStorage.removeItem("user_name");
                sessionStorage.user_token = response.data.token;
                sessionStorage.user_id = response.data.id;
                sessionStorage.user_name = response.data.username;
            }

            // 页面跳转
            let self = this;
            this.$alert("登录成功!","路飞学城",{
               callback(){
                    self.$router.push("/");
               }
            });

        }).catch(error=>{
            this.$message.error("对不起，登录失败！请确认密码或账号是否正确！");
        });
    },
    get_geetest_captcha(){
        // 获取验证码
        this.$axios.get(`${this.$settings.HOST}/users/captcha/`,{
          params:{
              username: this.username,
          }
        }).then(response=>{
            // 使用initGeetest接口
            // 参数1：配置参数
            // 参数2：回调，回调的第一个参数验证码对象，之后可以使用它做appendTo之类的事件
            // let data = JSON.parse(response.data);
            initGeetest({
                gt: data.gt,
                challenge: data.challenge,
                product: "popup", // 产品形式，包括：float，embed，popup。注意只对PC版验证码有效
                offline: !data.success // 表示用户后台检测极验服务器是否宕机，一般不需要关注
            }, this.handlerPopup);
        }).catch(error=>{
            console.log(error.response);
        });
    },
    handlerPopup(captchaObj) {
        let self = this;
        // 极验验证密码的验证方法
        captchaObj.onSuccess(function () {
            var validate = captchaObj.getValidate();
            // 当用户拖动验证码正确以后，发送请求给后端
            self.$axios.post(`${self.$settings.HOST}/users/captcha/`,{
                geetest_challenge: validate.geetest_challenge,
                geetest_validate: validate.geetest_validate,
                geetest_seccode: validate.geetest_seccode
            }).then(response=>{
                if(response.data.status){
                    // 验证码通过以后，才发送账号和密码进行登录！
                    self.loginHander();
                }
            }).catch(error=>{
               console.log(error.response);
            });
        });

        // 将验证码加到id为geetest1的元素里
        captchaObj.appendTo("#geetest1");
    }
  },

};
</script>

<style scoped>
.box{
	width: 100%;
  height: 100%;
	position: relative;
  overflow: hidden;
}
.box img{
	width: 100%;
  min-height: 100%;
}
.box .login {
	position: absolute;
	width: 500px;
	height: 400px;
	top: 0;
	left: 0;
  margin: auto;
  right: 0;
  bottom: 0;
  top: -338px;
}
.login .login-title{
     width: 100%;
    text-align: center;
}
.login-title img{
    width: 190px;
    height: auto;
}
.login-title p{
    font-family: PingFangSC-Regular;
    font-size: 18px;
    color: #fff;
    letter-spacing: .29px;
    padding-top: 10px;
    padding-bottom: 50px;
}
.login_box{
    width: 400px;
    height: auto;
    background: #fff;
    box-shadow: 0 2px 4px 0 rgba(0,0,0,.5);
    border-radius: 4px;
    margin: 0 auto;
    padding-bottom: 40px;
}
.login_box .title{
	font-size: 20px;
	color: #9b9b9b;
	letter-spacing: .32px;
	border-bottom: 1px solid #e6e6e6;
	 display: flex;
    	justify-content: space-around;
    	padding: 50px 60px 0 60px;
    	margin-bottom: 20px;
    	cursor: pointer;
}
.login_box .title span:nth-of-type(1){
	color: #4a4a4a;
    	border-bottom: 2px solid #84cc39;
}

.inp{
	width: 350px;
	margin: 0 auto;
}
.inp input{
    border: 0;
    outline: 0;
    width: 100%;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
}
.inp input.user{
    margin-bottom: 16px;
}
.inp .rember{
     display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    margin-top: 10px;
}
.inp .rember p:first-of-type{
    font-size: 12px;
    color: #4a4a4a;
    letter-spacing: .19px;
    margin-left: 22px;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-align: center;
    align-items: center;
    /*position: relative;*/
}
.inp .rember p:nth-of-type(2){
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .19px;
    cursor: pointer;
}

.inp .rember input{
    outline: 0;
    width: 30px;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
}

.inp .rember p span{
    display: inline-block;
  font-size: 12px;
  width: 100px;
  /*position: absolute;*/
/*left: 20px;*/

}
#geetest{
	margin-top: 20px;
}
.login_btn{
     width: 100%;
    height: 45px;
    background: #84cc39;
    border-radius: 5px;
    font-size: 16px;
    color: #fff;
    letter-spacing: .26px;
    margin-top: 30px;
}
.inp .go_login{
    text-align: center;
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .26px;
    padding-top: 20px;
}
.inp .go_login span{
    color: #84cc39;
    cursor: pointer;
}
</style>
```



