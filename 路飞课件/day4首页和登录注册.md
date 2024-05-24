# 首页

## 前端显示首页

### 首页组件代码

Home.vue

```vue
<template>
  <div id="home">
    <Header/>
    <Banner/>
    <Footer/>
  </div>
</template>

<script>
import Header from "./common/Header"
import Banner from "./common/Banner"
import Footer from "./common/Footer"

export default {
  name:"Home",
  data(){
    return {

    }
  },
  components:{
    Header,
    Banner,
    Footer,
  }
}
</script>

<style scoped>

</style>

```



### 首页头部子组件

Header.vue

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
                <el-col :span="3"><router-link class="current" to="/course">免费课</router-link></el-col>
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
                  <img class="cart-icon" src="@/assets/cart.svg" alt="">
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
                  <img class="cart-icon" src="@/assets/cart.svg" alt="">
                  <span><router-link to="/cart">购物车</router-link></span>
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

### 脚部子组件

Footer.vue

```vue
<template>
  <div class="footer">
    <el-container>
      <el-row>
        <el-col :span="4"><router-link to="">关于我们</router-link></el-col>
        <el-col :span="4"><router-link to="">联系我们</router-link></el-col>
        <el-col :span="4"><router-link to="">商务合作</router-link></el-col>
        <el-col :span="4"><router-link to="">帮助中心</router-link></el-col>
        <el-col :span="4"><router-link to="">意见反馈</router-link></el-col>
        <el-col :span="4"><router-link to="">新手指南</router-link></el-col>
        <el-col :span="24"><p class="copyright">Copyright © luffycity.com版权所有 | 京ICP备17072161号-1</p></el-col>
      </el-row>
    </el-container>
  </div>
</template>

<script>
  export default {
    name:"Footer",
    data(){
      return {}
    }
  }
</script>


<style scoped>
.footer{
  width: 100%;
  height: 128px;
  background: #25292e;
}
.footer .el-container{
  width: 1200px;
  margin: auto;
}
.footer .el-row {
  align-items: center;
  padding: 0 200px;
  padding-bottom: 15px;
  width: 100%;
  margin-top: 38px;
}
.footer .el-row a{
  color: #fff;
  font-size: 14px;
}
.footer .el-row .copyright{
  text-align: center;
  color: #fff;
  font-size: 14px;
}
</style>

```

### 轮播图子组件

Banner.vue

```vue
<template>
  <div class="banner">
      <el-carousel trigger="click" height="473px">
        <el-carousel-item v-for="banner in banner_list">
          <a :href="banner.link"><img width="100%" :src="banner.img" alt=""></a>
        </el-carousel-item>
      </el-carousel>
  </div>
</template>

<script>
  export default {
    name:"Banner",
    data(){
      return {
        banner_list:[
          {link:"http://www.baidu.com",img:"/static/banner/1.png"},
          {link:"http://www.baidu.com",img:"/static/banner/2.png"},
          {link:"http://www.baidu.com",img:"/static/banner/3.png"},
        ]
      };
    }
  }
</script>

<style>
.el-carousel__arrow{
  width: 100px!important;
  height: 100px!important;
}
.el-icon-arrow-left{
  font-size: 35px;
  margin-left: 50px;
}
.el-carousel__arrow--left{
  left: -50px;
}
</style>
```



### 注册首页路由

```python
import Vue from "vue"
import Router from "vue-router"

// 导入需要注册路由的组件
import Home from "../components/Home"
Vue.use(Router);

// 配置路由列表
export default new Router({
  mode:"history",
  routes:[
    // 路由列表
    {
      name:"Home",
      path: "/home",
      component:Home,
    },
    {
      name:"Home",
      path: "/",
      component:Home,
    }
  ]
})

```



## 轮播图功能实现

### 安装依赖模块和配置

#### 图片处理模块

前面已经安装了，如果没有安装则需要安装

```shell
pip install pillow
```



#### 上传文件相关配置

settings.py

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

注册home子应用，因为子应用的位置发生了改变，所以为了原来子应用的注册写法，所以新增一个导包路径：

```python
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 新增一个系统导包路径
import sys
sys.path.insert(0,os.path.join(BASE_DIR,"apps"))



INSTALLED_APPS = [
	# 注意，加上drf框架的注册	
    'rest_framework',
    
    # 子应用
    'home',

]
```

注意，pycharm会路径错误的提示。可以鼠标右键设置apps为 mark dir.... as source root



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
    # upload_to 设置上传文件的保存子目录
    image_url =  models.ImageField(upload_to="banner", null=True, blank=True, max_length=255, verbose_name="广告图片")
    remark = models.TextField(verbose_name="备注信息")
    is_show = models.BooleanField(default=False, verbose_name="是否显示")
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
    queryset = Banner.objects.filter(is_show=True, is_deleted=False).order_by("-orders","-id")[:constants.BANNER_LENGTH]
    serializer_class = BannerModelSerializer
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





访问http://api.luffycity.cn:8000/banner/，效果：

![1557457803586](assets/1557457803586.png)



所以我们需要有一个后台提供数据.安装xadmin

```python
pip install https://codeload.github.com/sshwsfc/xadmin/zip/django2 -i https://pypi.douban.com/simple/
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
```



如果之前没有创建超级用户，需要创建，如果有了，则可以直接使用之前的。

```python
python manage.py createsuperuser
```

![1557459230311](assets/1557459230311.png)

#### 给xadmin设置基本站点配置信息

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



在当前子应用中创建adminx.py，添加如下代码

```python
# 轮播图
from .models import BannerInfo
class BannerInfoModelAdmin(object):
    list_display=["title","orders","is_show"]
xadmin.site.register(BannerInfo, BannerInfoModelAdmin)
```



#### 修改后端xadmin中子应用名称

子应用/apps.py

```python
class HomeConfig(AppConfig):
    name = 'home'
    verbose_name = '我的首页'
```

``__init__.py``

```python
default_app_config = "home.apps.HomeConfig"
```

![1557459568731](assets/1557459568731.png)

给轮播图添加测试数据

![1557459669649](assets/1557459669649.png)



添加几条测试数据效果：

![1557459949073](assets/1557459949073.png)



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

Banner.vue代码：

```vue
<template>
  <el-carousel height="720px" :interval="3000" arrow="always">
    <el-carousel-item :key="key" v-for="banner,key in banner_list">
      <a :href="banner.link"><img :src="banner.image_url"></a>
    </el-carousel-item>
  </el-carousel>
</template>

<script>
    export default {
        name: "Banner",
        data(){
            return {
                banner_list:[]
            }
        },
        created() {
            this.get_banner_list();
        },
        methods:{
            get_banner_list(){
                // 获取轮播广告列表
                this.$axios.get(`${this.$settings.HOST}/banner/`,{}).then(response=>{
                  this.banner_list = response.data;
                }).catch(error=>{
                  console.log(error.response)
                });
            }
        }
    }
</script>

<style scoped>
  .el-carousel__item h3 {
    color: #475669;
    font-size: 18px;
    opacity: 0.75;
    line-height: 300px;
    margin: 0;
  }

  .el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
  }

  .el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
  }
</style>

```

效果：

![1557460383648](assets/1557460383648.png)



## 导航功能实现

### 创建模型

引入一个公共模型【抽象模型，不会在数据迁移的时候为它创建表】

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

公共模型，保存项目的公共代码库目录下luffy/utils.py文件中。

```python
from django.db import models

class BaseModel(models.Model):
    """公共模型"""
    is_show = models.BooleanField(default=False, verbose_name="是否显示")
    orders = models.IntegerField(default=1, verbose_name="排序")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

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
    """导航菜单视图"""
    queryset = Nav.objects.filter(is_show=True, is_deleted=False,position=1).order_by("-orders","-id")[:constants.HEADER_NAV_LENGTH]
    serializer_class = NavModelSerializer


class FooterNavListAPIView(ListAPIView):
    """导航菜单视图"""
    queryset = Nav.objects.filter(is_show=True, is_deleted=False,position=2).order_by("-orders","-id")[:constants.FOOTER_NAV_LENGTH]
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
    path("nav/header/",views.NavHeaderListAPIView.as_view()),
    path("nav/footer/",views.NavFooterListAPIView.as_view()),
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
    <div class="header-box">
      <div class="header">
        <div class="content">
          <div class="logo full-left">
            <router-link to="/"><img src="/static/image/logo.svg" alt=""></router-link>
          </div>
          <ul class="nav full-left">
              <li v-for="nav in nav_list">
                <span v-if="nav.is_site"><a :href="nav.link">{{nav.title}}</a></span>
                <span v-else><router-link :to="nav.link">{{nav.title}}</router-link></span>
              </li>
          </ul>
          <div class="login-bar full-right">
            <div class="shop-cart full-left">
              <img src="/static/image/cart.svg" alt="">
              <span><router-link to="/cart">购物车</router-link></span>
            </div>
            <div class="login-box full-left">
              <span>登录</span>
              &nbsp;|&nbsp;
              <span>注册</span>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
    export default {
      name: "Header",
      data(){
        return{
            nav_list: [],
        }
      },
      created() {
          this.get_nav();
      },
      methods:{
          get_nav(){
              this.$axios.get(`${this.$settings.HOST}/nav/header/`,{}).then(response=>{
                  this.nav_list = response.data;
              }).catch(error=>{
                  console.log(error.response);
              })
          }
      }
    }
</script>

<style scoped>
.header-box{
  height: 80px;
}
.header{
  width: 100%;
  height: 80px;
  box-shadow: 0 0.5px 0.5px 0 #c9c9c9;
  position: fixed;
  top:0;
  left: 0;
  right:0;
  margin: auto;
  z-index: 99;
  background: #fff;
}
.header .content{
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}
.header .content .logo{
  height: 80px;
  line-height: 80px;
  margin-right: 50px;
  cursor: pointer; /* 设置光标的形状为爪子 */
}
.header .content .logo img{
  vertical-align: middle;
}
.header .nav li{
  float: left;
  height: 80px;
  line-height: 80px;
  margin-right: 30px;
  font-size: 16px;
  color: #4a4a4a;
  cursor: pointer;
}
.header .nav li span{
  padding-bottom: 16px;
  padding-left: 5px;
  padding-right: 5px;
}
.header .nav li span a{
  display: inline-block;
}
.header .nav li .this{
  color: #4a4a4a;
  border-bottom: 4px solid #ffc210;
}
.header .nav li:hover span{
  color: #000;
}
.header .login-bar{
  height: 80px;
}
.header .login-bar .shop-cart{
  margin-right: 20px;
  border-radius: 17px;
  background: #f7f7f7;
  cursor: pointer;
  font-size: 14px;
  height: 28px;
  width: 88px;
  margin-top: 30px;
  line-height: 32px;
  text-align: center;
}
.header .login-bar .shop-cart:hover{
  background: #f0f0f0;
}
.header .login-bar .shop-cart img{
  width: 15px;
  margin-right: 4px;
  margin-left: 6px;
}
.header .login-bar .shop-cart span{
  margin-right: 6px;
}
.header .login-bar .login-box{
  margin-top: 33px;
}
.header .login-bar .login-box span{
  color: #4a4a4a;
  cursor: pointer;
}
.header .login-bar .login-box span:hover{
  color: #000000;
}
</style>

```

Footer.vue

```vue
<template>
    <div class="footer">
      <ul>
          <li v-for="nav in nav_list">
              <span v-if="nav.is_site"><a :href="nav.link">{{nav.title}}</a></span>
              <span v-else><router-link :to="nav.link">{{nav.title}}</router-link></span>
          </li>
      </ul>
      <p>Copyright © luffycity.com版权所有 | 京ICP备17072161号-1</p>
    </div>
</template>

<script>
    export default {
      name: "Footer",
      data(){
        return{
            nav_list: [],
        }
      },
      created() {
          this.get_nav();
      },
      methods:{
          get_nav(){
              this.$axios.get(`${this.$settings.HOST}/nav/footer/`,{}).then(response=>{
                  this.nav_list = response.data;
              }).catch(error=>{
                  console.log(error.response);
              })
          }
      }
    }
</script>

<style scoped>
.footer {
  width: 100%;
  height: 128px;
  background: #25292e;
  color: #fff;
}
.footer ul{
  margin: 0 auto 16px;
  padding-top: 38px;
  width: 810px;
}
.footer ul li{
  float: left;
  width: 112px;
  margin: 0 10px;
  text-align: center;
  font-size: 14px;
}
.footer ul::after{
  content:"";
  display:block;
  clear:both;
}
.footer p{
  text-align: center;
  font-size: 12px;
}
</style>

```



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

Django默认已经提供了认证系统Auth模块。认证系统包含：

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
python ../../manage.py startapp user
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

在创建好的应用models.py中定义用户的用户模型类。

```python
class User(AbstractUser):
    """用户模型类"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

    class Meta:
        db_table = 'ly_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
```

我们自定义的用户模型类还不能直接被Django的认证系统所识别，需要在配置文件中告知Django认证系统使用我们自定义的模型类。

在配置文件中进行设置

```python
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
0. 先把现有的数据库导出备份，然后清掉数据库中所有的数据表。
1. 把开发者创建的所有子应用下面的migrations目录下除了__init__.py以外的所有迁移文件，只要涉及到用户的，一律删除
2. 把django.contrib.admin.migrations目录下除了__init__.py以外的所有迁移文件，全部删除。
3. 把django.contrib.auth.migrations目录下除了__init__.py以外的所有迁移文件，全部删除。
4. 把reversion.migrations目录下除了__init__.py以外的所有迁移文件，全部删除。
5. 把xadmin.migrations目录下除了__init__.py以外的所有迁移文件，全部删除。
6. 接下来，执行数据迁移，回顾第0步中的数据，以后如果要修改用户相关数据，不需要重复本次操作，直接数据迁移即可。
```



### Django REST framework JWT

在用户注册或登录后，我们想记录用户的登录状态，或者为用户创建身份认证的凭证。我们不再使用Session认证机制，而使用Json Web Token认证机制。

```
Json web token (JWT), 是为了在网络应用环境间传递声明而执行的一种基于JSON的开放标准（(RFC 7519).该token被设计为紧凑且安全的，特别适用于分布式站点的单点登录（SSO）场景。JWT的声明一般被用来在身份提供者和服务提供者间传递被认证的用户身份信息，以便于从资源服务器获取资源，也可以增加一些额外的其它业务逻辑所必须的声明信息，该token也可直接被用于认证，也可被加密。
```



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

### payload

载荷就是存放有效信息的地方。这个名字像是特指飞机上承载的货品，这些有效信息包含三个部分

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

**公共的声明** ： 公共的声明可以添加任何的信息，一般添加用户的相关信息或其他业务需要的必要信息.但不建议添加敏感信息，因为该部分在客户端可解密.

**私有的声明** ： 私有声明是提供者和消费者所共同定义的声明，一般不建议存放敏感信息，因为base64是对称解密的，意味着该部分信息可以归类为明文信息。

定义一个payload:

```
{
  "sub": "1234567890",
  "exp": "3422335555",
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
2. 数据实际保存在客户端，所以我们可以分担都武器的存储压力

jwt的缺点：
1. 数据保存在了客户端，我们服务端只认jwt，不识别客户端。
2. jwt可以设置过期时间，但是因为数据保存在了客户端，所以对于过期时间不好调整。
```



**关于签发和核验JWT，我们可以使用Django REST framework JWT扩展来完成。**

[文档网站http://getblimp.github.io/django-rest-framework-jwt/](http://getblimp.github.io/django-rest-framework-jwt/)



### 安装配置JWT

安装

```shell
pip install djangorestframework-jwt
```

settings/dev.py,配置

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



### 手动生成jwt

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

在子应用路由urls.py中

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



接下来，我们可以通过postman来测试下功能

![1553572597916](assets/1553572597916.png)



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

浏览器的本地存储提供了sessionStorage 和 localStorage 两种：

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
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'user.utils.jwt_response_payload_handler',
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
```



### 2.3.9 多条件登录

JWT扩展的登录视图，在收到用户名与密码时，也是调用Django的认证系统中提供的**authenticate()**来检查用户名与密码是否正确。

我们可以通过修改Django认证系统的认证后端（主要是authenticate方法）来支持登录账号既可以是用户名也可以是手机号。

**修改Django认证系统的认证后端需要继承django.contrib.auth.backends.ModelBackend，并重写authenticate方法。**

`authenticate(self, request, username=None, password=None, **kwargs)`方法的参数说明：

- request 本次认证的请求对象
- username 本次认证提供的用户账号
- password 本次认证提供的密码

**我们想要让用户既可以以用户名登录，也可以以手机号登录，那么对于authenticate方法而言，username参数即表示用户名或者手机号。**

重写authenticate方法的思路：

1. 根据username参数查找用户User对象，username参数可能是用户名，也可能是手机号
2. 若查找到User对象，调用User对象的check_password方法检查密码是否正确

在users/utils.py中编写：

```python
def get_user_by_account(account):
    """
    根据帐号获取user对象
    :param account: 账号，可以是用户名，也可以是手机号
    :return: User对象 或者 None
    """
    try:
        if re.match('^1[3-9]\d{9}$', account):
            # 帐号为手机号
            user = User.objects.get(mobile=account)
        else:
            # 帐号为用户名
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user

import re
from .models import User
from django.contrib.auth.backends import ModelBackend
class UsernameMobileAuthBackend(ModelBackend):
    """
    自定义用户名或手机号认证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)
        if user is not None and user.check_password(password):
            return user
```

在配置文件settings/dev.py中告知Django使用我们自定义的认证后端

```python
AUTHENTICATION_BACKENDS = [
    'user.utils.UsernameMobileAuthBackend',
]
```



## 前端首页实现登陆状态的判断

common/Header.vue组件代码：

```vue
<template>
    <div class="header-box">
      <div class="header">
        <div class="content">
          <div class="logo full-left">
            <router-link to="/"><img src="/static/image/logo.svg" alt=""></router-link>
          </div>
          <ul class="nav full-left">
              <li v-for="nav in nav_list">
                <span v-if="nav.is_site"><a :href="nav.link">{{nav.title}}</a></span>
                <span v-else><router-link :to="nav.link">{{nav.title}}</router-link></span>
              </li>
          </ul>

          <div class="login-bar full-right">
            <div class="shop-cart full-left">
              <span class="shop-cart-total">0</span>
              <img src="/static/image/cart.svg" alt="">
              <span><router-link to="/cart">购物车</router-link></span>
            </div>
            <div class="login-box login-box1 full-left">
              <router-link to="">学习中心</router-link>
              <el-menu width="200" class="member el-menu-demo" mode="horizontal">
                  <el-submenu index="2">
                    <template slot="title"><img src="/static/image/logo@2x.png" alt=""></template>
                    <el-menu-item index="2-1">我的账户</el-menu-item>
                    <el-menu-item index="2-2">我的订单</el-menu-item>
                    <el-menu-item index="2-3">我的优惠卷</el-menu-item>
                    <el-menu-item index="2-3"><span>退出登录</span></el-menu-item>
                  </el-submenu>
                </el-menu>
            </div>
          </div>

          <div v-if="token" class="login-bar full-right">
            <div class="shop-cart full-left">
              <img src="/static/image/cart.svg" alt="">
              <span><router-link to="/cart">购物车</router-link></span>
            </div>
            <div class="login-box full-left">
              <router-link to="/user/login">登录</router-link>
              &nbsp;|&nbsp;
              <span>注册</span>
            </div>
          </div>

        </div>
      </div>
    </div>
</template>



<style scoped>
...

.header .login-bar .shop-cart{
  margin-right: 20px;
  border-radius: 17px;
  background: #f7f7f7;
  cursor: pointer;
  font-size: 14px;
  height: 28px;
  width: 90px;
  margin-top: 30px;
  line-height: 32px;
  text-align: center;
}
    
.member{
    display: inline-block;
    height: 34px;
    margin-left: 20px;
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
.header .login-bar .login-box1{
  margin-top: 16px;
}
</style>
```



退出登陆，Header.vue

```vue
<template>
    <div class="header-box">
      <div class="header">
        <div class="content">
          <div class="logo full-left">
            <router-link to="/"><img src="/static/image/logo.svg" alt=""></router-link>
          </div>
          <ul class="nav full-left">
              <li v-for="nav in nav_list">
                <span v-if="nav.is_site"><a :href="nav.link">{{nav.title}}</a></span>
                <span v-else><router-link :to="nav.link">{{nav.title}}</router-link></span>
              </li>
          </ul>

          <div v-if="token" class="login-bar full-right">
            <div class="shop-cart full-left">
              <span class="shop-cart-total">0</span>
              <img src="/static/image/cart.svg" alt="">
              <span><router-link to="/cart">购物车</router-link></span>
            </div>
            <div class="login-box login-box1 full-left">
              <router-link to="">学习中心</router-link>
              <el-menu width="200" class="member el-menu-demo" mode="horizontal">
                  <el-submenu index="2">
                    <template slot="title"><img src="/static/image/logo@2x.png" alt=""></template>
                    <el-menu-item index="2-1">我的账户</el-menu-item>
                    <el-menu-item index="2-2">我的订单</el-menu-item>
                    <el-menu-item index="2-3">我的优惠卷</el-menu-item>
                    <el-menu-item index="2-3"><span @click="logoutHander">退出登录</span></el-menu-item>
                  </el-submenu>
                </el-menu>
            </div>
          </div>

          <div v-else class="login-bar full-right">
            <div class="shop-cart full-left">
              <img src="/static/image/cart.svg" alt="">
              <span><router-link to="/cart">购物车</router-link></span>
            </div>
            <div class="login-box full-left">
              <router-link to="/user/login">登录</router-link>
              &nbsp;|&nbsp;
              <span>注册</span>
            </div>
          </div>

        </div>
      </div>
    </div>
</template>

<script>
    export default {
      name: "Header",
      data(){
        return{
            token:"",
            nav_list: [],
        }
      },
      created() {
          this.check_user_login();
          this.get_nav();
      },
      methods:{
          check_user_login(){
            // 获取用户的登录状态
            this.token = sessionStorage.user_token || localStorage.user_token;
            return this.token;
          },
          get_nav(){
              this.$axios.get(`${this.$settings.HOST}/nav/header/`,{}).then(response=>{
                  this.nav_list = response.data;
              }).catch(error=>{
                  console.log(error.response);
              })
          },
          logoutHander(){
              // 退出登录
              localStorage.removeItem("user_token");
              localStorage.removeItem("user_id");
              localStorage.removeItem("user_name");
              sessionStorage.removeItem("user_token");
              sessionStorage.removeItem("user_id");
              sessionStorage.removeItem("user_name");
              this.check_user_login();
          }
      }
    }
</script>

<style scoped>
.header-box{
  height: 80px;
}
.header{
  width: 100%;
  height: 80px;
  box-shadow: 0 0.5px 0.5px 0 #c9c9c9;
  position: fixed;
  top:0;
  left: 0;
  right:0;
  margin: auto;
  z-index: 99;
  background: #fff;
}
.header .content{
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}
.header .content .logo{
  height: 80px;
  line-height: 80px;
  margin-right: 50px;
  cursor: pointer; /* 设置光标的形状为爪子 */
}
.header .content .logo img{
  vertical-align: middle;
}
.header .nav li{
  float: left;
  height: 80px;
  line-height: 80px;
  margin-right: 30px;
  font-size: 16px;
  color: #4a4a4a;
  cursor: pointer;
}
.header .nav li span{
  padding-bottom: 16px;
  padding-left: 5px;
  padding-right: 5px;
}
.header .nav li span a{
  display: inline-block;
}
.header .nav li .this{
  color: #4a4a4a;
  border-bottom: 4px solid #ffc210;
}
.header .nav li:hover span{
  color: #000;
}
.header .login-bar{
  height: 80px;
}
.header .login-bar .shop-cart{
  margin-right: 20px;
  border-radius: 17px;
  background: #f7f7f7;
  cursor: pointer;
  font-size: 14px;
  height: 28px;
  width: 90px;
  margin-top: 30px;
  line-height: 32px;
  text-align: center;
}
.header .login-bar .shop-cart:hover{
  background: #f0f0f0;
}
.header .login-bar .shop-cart img{
  width: 15px;
  margin-right: 4px;
  margin-left: 6px;
}
.header .login-bar .shop-cart span{
  margin-right: 6px;
}
.header .login-bar .login-box{
  margin-top: 32px;
}
.header .login-bar .login-box span{
  color: #4a4a4a;
  cursor: pointer;
}
.header .login-bar .login-box span:hover{
  color: #000000;
}
.member{
    display: inline-block;
    height: 34px;
    margin-left: 20px;
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
.header .login-bar .login-box1{
  margin-top: 16px;
}
</style>
```



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



把验证码模块防止在utils中

![1553578068434](assets/1553578068434.png)

并在user子应用下创建验证码视图类，并提供验证码和校验验证码的视图方法。

```python
from django.shortcuts import render
pc_geetest_id = "5e876edb2bda195c265416b70e7389a7"
pc_geetest_key = "c1f0f6f5958507924d187db31cd136e5"
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
        return Response(response_str)

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
        this.$axios.get(`${this.$settings.HOST}/user/captcha/`,{
          params:{
              username: this.username,
          }
        }).then(response=>{
            // 使用initGeetest接口
            // 参数1：配置参数
            // 参数2：回调，回调的第一个参数验证码对象，之后可以使用它做appendTo之类的事件
            let data = JSON.parse(response.data);
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
            self.$axios.post(`${self.$settings.HOST}/user/captcha/`,{
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

        // 将验证码加到id为captcha的元素里，append追加的形式不太好，就是点击多次会加载多次的验证码，所以我们改为下面的写法
        //captchaObj.appendTo("#geetest1");
        let g1 = document.getElementById('geetest1');
        g1.innerHTML = '';
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


