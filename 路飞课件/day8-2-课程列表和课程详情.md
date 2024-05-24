# 课程列表页

## 课程列表接口实现分页显示数据

在当前子应用courses下创建一个分页器的文件paginations.py，代码：

```python
from rest_framework.pagination import PageNumberPagination
class CustomPageNumberPagination(PageNumberPagination):
    # page_query_param = "" # 地址上面代表页码的变量名，默认为page
    page_size = 5         # 每一页显示的数据量，没有设置页码，则不进行分页
	# 允许客户端通过指定的参数名来设置每一页数据量的大小，默认是size
    page_size_query_param = "size"
    max_page_size = 20    # 限制每一页最大展示的数据量
```



视图中加载声明的分页器，代码：

```python
# 按条件筛选[分类]展示课程信息
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .paginations import CustomPageNumberPagination
class CourseListAPIView(ListAPIView):
    """课程列表"""
    queryset = Course.objects.filter(is_show=True,is_delete=False).order_by("orders")
    serializer_class = CourseModelSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # 设置支持设置的筛选过滤字段
    filter_fields = ('course_category', )
    # 设置支持设置的排序字段
    ordering_fields = ('id', 'students', 'price')
    # 指定分页器
    pagination_class = CustomPageNumberPagination
```



客户端请求后端发送数据[https://element.eleme.cn/#/zh-CN/component/pagination]

```vue
<template>
  <div class="course">
    <Header></Header>
    <div class="main">
      <!-- 筛选条件 -->
      <div class="condition">
        <ul class="cate-list">
          <li class="title">课程分类:</li>
          <li @click="category=0" :class="category==0?'this':''">全部</li>
          <li @click="category=cat.id" :class="category==cat.id?'this':''" v-for="cat in category_list">{{cat.name}}</li>
        </ul>

        <div class="ordering">
          <ul>
            <li class="title">筛&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;选: </li>
            <li @click="change_order_type('id')" class="default" :class="change_order_class('id')">默认</li>
            <li @click="change_order_type('students')" class="hot" :class="change_order_class('students')">人气</li>
            <li @click="change_order_type('price')" class="price" :class="change_order_class('price')">价格</li>

<!--            <li @click="filters.type=0" class="default" :class="filters.type==0?'this':''">默认</li>-->
<!--            <li @click="filters.type=1" class="hot" :class="filters.type==1?'this':''">人气</li>-->
<!--            <li @click="filters.type=2" class="price" :class="filters.type==2?'this':''">价格</li>-->
          </ul>
          <p class="condition-result">共21个课程</p>
        </div>

      </div>
      <el-pagination
      background
      layout="prev, pager, next,sizes"
      :page-size="filters.size"
      :page-sizes="[2, 3, 5, 10]"
      @current-change="handleCurrentChange"
      @size-change="handleSizeChange"
      :total="total">
    </el-pagination>
      <!-- 课程列表 -->
      <div class="course-list">
        <div class="course-item" v-for="course in course_list">
          <div class="course-image">
            <img :src="course.course_img" alt="">
          </div>
          <div class="course-info">
            <h3><router-link to="/course/detail/1">{{course.name}}</router-link> <span><img src="/static/image/avatar1.svg" alt="">{{course.students}}人已加入学习</span></h3>
            <p class="teather-info">{{course.teacher.name}} {{course.teacher.signature}} {{course.teacher.title}} <span>共{{course.lessons}}课时/{{course.pub_lessons==course.lessons?'更新完成':`已更新${course.pub_lessons}课时`}}</span></p>
            <ul class="lesson-list">
              <li :key="key" v-for="(lesson,key) in course.lessons_list"><span class="lesson-title">0{{key}} | 第{{lesson.lesson}}节：{{lesson.name}}</span> <span class="free" v-if="lesson.free_trail">免费</span></li>
<!--              <li><span class="lesson-title">01 | 第1节：初识编码初识编码</span> <span class="free">免费</span></li>-->
<!--              <li><span class="lesson-title">01 | 第1节：初识编码</span> <span class="free">免费</span></li>-->
<!--              <li><span class="lesson-title">01 | 第1节：初识编码初识编码初识编码初识编码</span> <span class="free">免费</span></li>-->
            </ul>
            <div class="pay-box">
              <span class="discount-type">限时免费</span>
              <span class="discount-price">￥0.00元</span>
              <span class="original-price">原价：{{course.price}}元</span>
              <span class="buy-now">立即购买</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <el-pagination
      background
      layout="prev, pager, next,sizes"
      :page-size="filters.size"
      :page-sizes="[2, 3, 5, 10]"
      @current-change="handleCurrentChange"
      @size-change="handleSizeChange"
      :total="total">
    </el-pagination>
    <Footer></Footer>
  </div>
</template>

<script>
  import Header from "./common/Header"
  import Footer from "./common/Footer"
  export default {
      name: "Course",
      data(){
        return{
          category: 0,
          category_list:[],
          total: 0,
          course_list: [],
          filters:{
              type: "id", // 筛选类型，id表示默认，students表示人气,price表示价格
              orders: "desc",  // 排序类型[控制样式]，desc表示降序，asc表示升序
              size: 5, // 单页数据量
              page: 1, // 当前页码
          }
        }
      },
      watch:{
          category(){
              this.get_course();
          }
      },
      created(){
        this.get_course_category();
        this.get_course();
      },
      methods:{
        get_course_category(){
            // 获取课程分类信息
            this.$axios.get(`${this.$settings.HOST}/course/category/`).then(response=>{
                this.category_list = response.data;
            })
        },
        get_course(){
            let filters = {
                page: this.filters.page,
                size: this.filters.size,
            };

            if(this.filters.orders==="desc"){
                filters.ordering = "-"+this.filters.type;
            }else{
                filters.ordering = this.filters.type;
            }
            // 判断是否要根据分类显示课程信息
            if( this.category > 0 ){
                filters.course_category = this.category;
            }

            this.$axios.get(`${this.$settings.HOST}/course/`,{
                params:filters
            }).then(response=>{
                this.course_list = response.data.results;  //数据结构变了
                this.total = response.data.count;
            });
        },
        change_order_type(type){
            // 更改升序或者降序
            if( this.filters.type === type && this.filters.orders === "desc" ){
                this.filters.orders="asc";
            }else if( this.filters.type === type && this.filters.orders === "asc"){
                this.filters.orders="desc";
            }

            // 更改排序方式
            this.filters.type=type;
            // 重新获取课程
            this.get_course();
        },
        change_order_class(type){
            // 更改当前选中筛选条件的高亮方式
            if( this.filters.type === type && this.filters.orders === "asc" ){
              return "this asc";
            }else if(this.filters.type===type && this.filters.orders === "desc"){
              return "this desc";
            }else{
              return "";
            }
        },
        handleCurrentChange(page){
            // 切换页码时，重新获取课程
            console.log("本次点击的页码是:", page);
            this.filters.page = page;
            this.get_course();
        },
        handleSizeChange(size){
            // 切换单页显示的数据量
            this.filters.size = size;
            // 重置页码
            this.filters.page = 1;
            this.get_course();
        },
      },
      components:{
        Header,
        Footer,
      }
  }
</script>



<style scoped>
  .course{
    background: #f6f6f6;
  }
  .course .main{
    width: 1100px;
    margin: 35px auto 0;
  }
  .course .condition{
    margin-bottom: 35px;
    padding: 25px 30px 25px 20px;
    background: #fff;
    border-radius: 4px;
    box-shadow: 0 2px 4px 0 #f0f0f0;
  }
  .course .cate-list{
    border-bottom: 1px solid #333;
    border-bottom-color: rgba(51,51,51,.05);
    padding-bottom: 18px;
    margin-bottom: 17px;
  }
  .course .cate-list::after{
    content:"";
    display: block;
    clear: both;
  }
  .course .cate-list li{
    float: left;
    font-size: 16px;
    padding: 6px 15px;
    line-height: 16px;
    margin-left: 14px;
    position: relative;
    transition: all .3s ease;
    cursor: pointer;
    color: #4a4a4a;
    border: 1px solid transparent; /* transparent 透明 */
  }
  .course .cate-list .title{
    color: #888;
    margin-left: 0;
    letter-spacing: .36px;
    padding: 0;
    line-height: 28px;
  }
  .course .cate-list .this{
    color: #ffc210;
    border: 1px solid #ffc210!important;
    border-radius: 30px;
  }
  .course .ordering::after{
    content:"";
    display: block;
    clear: both;
  }
  .course .ordering ul{
    float: left;
  }
  .course .ordering ul::after{
    content:"";
    display: block;
    clear: both;
  }
  .course .ordering .condition-result{
    float: right;
    font-size: 14px;
    color: #9b9b9b;
    line-height: 28px;
  }
  .course .ordering ul li{
    float: left;
    padding: 6px 15px;
    line-height: 16px;
    margin-left: 14px;
    position: relative;
    transition: all .3s ease;
    cursor: pointer;
    color: #4a4a4a;
  }
  .course .ordering .title{
    font-size: 16px;
    color: #888;
    letter-spacing: .36px;
    margin-left: 0;
    padding:0;
    line-height: 28px;
  }
  .course .ordering .this{
    color: #ffc210;
    position: relative;
  }
  .course .ordering .this::before,
  .course .ordering .this::after{
    cursor: pointer;
    content:"";
    display: block;
    width: 0px;
    height: 0px;
    border: 5px solid transparent;
    position: absolute;
    right: 0;
  }
  .course .ordering .this::before{
    border-bottom: 5px solid #aaa;
    margin-bottom: 2px;
    top: 2px;
  }
  .course .ordering .this::after{
    border-top: 5px solid #aaa;
    bottom: 2px;
  }
  .course .ordering .asc::before{
    border-bottom-color: #ffc210;
  }
  .course .ordering .desc::after{
    border-top-color: #ffc210;
  }
  .course .course-item:hover{
    box-shadow: 4px 6px 16px rgba(0,0,0,.5);
  }
  .course .course-item{
    width: 1050px;
    background: #fff;
    padding: 20px 30px 20px 20px;
    margin-bottom: 35px;
    border-radius: 2px;
    cursor: pointer;
    box-shadow: 2px 3px 16px rgba(0,0,0,.1);
    /* css3.0 过渡动画 hover 事件操作 */
    transition: all .2s ease;
  }
  .course .course-item::after{
    content:"";
    display: block;
    clear: both;
  }
  /* 顶级元素 父级元素  当前元素{} */
  .course .course-item .course-image{
    float: left;
    width: 423px;
    height: 210px;
    margin-right: 30px;
  }
  .course .course-item .course-image img{
    width: 100%;
  }
  .course .course-item .course-info{
    float: left;
    width: 596px;
  }
  .course-item .course-info h3 {
    font-size: 26px;
    color: #333;
    font-weight: normal;
    margin-bottom: 8px;
  }
  .course-item .course-info h3 span{
    font-size: 14px;
    color: #9b9b9b;
    float: right;
    margin-top: 14px;
  }
  .course-item .course-info h3 span img{
      width: 11px;
      height: auto;
      margin-right: 7px;
  }
  .course-item .course-info .teather-info{
      font-size: 14px;
      color: #9b9b9b;
      margin-bottom: 14px;
      padding-bottom: 14px;
      border-bottom: 1px solid #333;
      border-bottom-color: rgba(51,51,51,.05);
  }
  .course-item .course-info .teather-info span{
      float: right;
  }
  .course-item .lesson-list::after{
      content:"";
      display: block;
      clear: both;
  }
  .course-item .lesson-list li {
    float: left;
    width: 44%;
    font-size: 14px;
    color: #666;
    padding-left: 22px;
    /* background: url("路径") 是否平铺 x轴位置 y轴位置 */
    background: url("/static/image/play-icon-gray.svg") no-repeat left 4px;
    margin-bottom: 15px;
  }
  .course-item .lesson-list li .lesson-title{
      /* 以下3句，文本内容过多，会自动隐藏，并显示省略符号 */
      text-overflow: ellipsis;
      overflow: hidden;
      white-space: nowrap;
      display:inline-block;
      max-width: 200px;
  }
  .course-item .lesson-list li:hover{
      background-image: url("/static/image/play-icon-yellow.svg");
      color: #ffc210;
  }
  .course-item .lesson-list li .free{
      width: 34px;
      height: 20px;
      color: #fd7b4d;
      vertical-align: super;
      margin-left: 10px;
      border: 1px solid #fd7b4d;
      border-radius: 2px;
      text-align: center;
      font-size: 13px;
      white-space: nowrap;
  }
  .course-item .lesson-list li:hover .free{
      color: #ffc210;
      border-color: #ffc210;
  }
  .course-item .pay-box::after{
    content:"";
    display: block;
    clear: both;
  }
  .course-item .pay-box .discount-type{
    padding: 6px 10px;
    font-size: 16px;
    color: #fff;
    text-align: center;
    margin-right: 8px;
    background: #fa6240;
    border: 1px solid #fa6240;
    border-radius: 10px 0 10px 0;
    float: left;
  }
  .course-item .pay-box .discount-price{
    font-size: 24px;
    color: #fa6240;
    float: left;
  }
  .course-item .pay-box .original-price{
    text-decoration: line-through;
    font-size: 14px;
    color: #9b9b9b;
    margin-left: 10px;
    float: left;
    margin-top: 10px;
  }
  .course-item .pay-box .buy-now{
    width: 120px;
    height: 38px;
    background: transparent;
    color: #fa6240;
    font-size: 16px;
    border: 1px solid #fd7b4d;
    border-radius: 3px;
    transition: all .2s ease-in-out;
    float: right;
    text-align: center;
    line-height: 38px;
  }
  .course-item .pay-box .buy-now:hover{
    color: #fff;
    background: #ffc210;
    border: 1px solid #ffc210;
  }
  .el-pagination{
  text-align: center;
    padding-top: 20px;
    padding-bottom: 50px;
  }
</style>
```



修改分页样式中的字体大小，static/reset.css，代码：

```css
.el-pagination button, .el-pagination span:not([class*=suffix]),
.el-input--mini,
.el-pagination__sizes .el-input .el-input__inner,
.el-pager li{
  font-size: 16px;
}

.el-pagination{
  text-align: center;
    padding-top: 20px;
    padding-bottom: 50px;
  }
```







# 课程详情页

## CKEditor富文本编辑器

富文本即具备丰富样式格式的文本。在运营后台，运营人员需要录入课程的相关描述，可以是包含了HTML语法格式的字符串。为了快速简单的让用户能够在页面中编辑带html格式的文本，我们引入富文本编辑器。

富文本编辑器：ueditor(百度)、ckeditor、kindeditor

### 1. 安装

```shell
pip install django-ckeditor==6.3
```

### 2. 添加应用

在INSTALLED_APPS中添加

```python
INSTALLED_APPS = [
    ...
    'ckeditor',  # 富文本编辑器
    'ckeditor_uploader',  # 富文本编辑器上传图片模块
    ...
]
```

### 3. 添加CKEditor设置

在settings/dev.py中添加

```python
# 富文本编辑器ckeditor配置
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',  # 工具条功能,full表示全部，Basic表示基本功能，功能少很多，还有个Custom自定义功能选项
        'height': 300,      # 编辑器高度
        # 'width': 300,     # 编辑器宽
    },
}
CKEDITOR_UPLOAD_PATH = ''  # 上传图片保存路径，留空则调用django的文件上传功能



#自定义
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline','Image'],  #通过浏览器f12来查看每个功能的标签，就看到了类值cke_button_工具名称[注意使用驼峰式来写]
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source']
        ]
    }
}
```

### 4. 添加ckeditor路由

在总路由中添加

```python
re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
```

### 5. 为模型类添加字段

ckeditor提供了两种类型的Django模型类字段

- `ckeditor.fields.RichTextField` 不支持上传文件的富文本字段
- `ckeditor_uploader.fields.RichTextUploadingField` 支持上传文件的富文本字段\

修改course/models.py里面的字段信息,记得要重新数据迁移

```python
from ckeditor_uploader.fields import RichTextUploadingField
class Course(models.Model):
    """
    专题课程
    """
	...
    
    brief = RichTextUploadingField(max_length=2048, verbose_name="课程概述", null=True, blank=True)
    
```

效果：

![1557886665513](assets/1557886665513.png)





## 课程详情页显示

详情页组件代码：

```vue
<template>
    <div class="detail">
      <Header/>
      <div class="main">
        <div class="course-info">
          <div class="wrap-left">

          </div>
          <div class="wrap-right">
            <h3 class="course-name">Linux系统基础5周入门精讲</h3>
            <p class="data">23475人在学&nbsp;&nbsp;&nbsp;&nbsp;课程总时长：148课时/180小时&nbsp;&nbsp;&nbsp;&nbsp;难度：初级</p>
            <div class="sale-time">
              <p class="sale-type">限时免费</p>
              <p class="expire">距离结束：仅剩 01天 04小时 33分 <span class="second">08</span> 秒</p>
            </div>
            <p class="course-price">
              <span>活动价</span>
              <span class="discount">¥0.00</span>
              <span class="original">¥29.00</span>
            </p>
            <div class="buy">
              <div class="buy-btn">
                <button class="buy-now">立即购买</button>
                <button class="free">免费试学</button>
              </div>
              <div class="add-cart"><img src="/static/image/cart-yellow.svg" alt="">加入购物车</div>
            </div>
          </div>
        </div>
        <div class="course-tab">
          <ul class="tab-list">
            <li :class="tabIndex==1?'active':''" @click="tabIndex=1">详情介绍</li>
            <li :class="tabIndex==2?'active':''" @click="tabIndex=2">课程章节 <span :class="tabIndex!=2?'free':''">(试学)</span></li>
            <li :class="tabIndex==3?'active':''" @click="tabIndex=3">用户评论 (42)</li>
            <li :class="tabIndex==4?'active':''" @click="tabIndex=4">常见问题</li>
          </ul>
        </div>
        <div class="course-content">
          <div class="course-tab-list">
            <div class="tab-item" v-if="tabIndex==1">
              <p><img alt="" src="https://hcdn1.luffycity.com/static/frontend/course/5/21天01_1547098127.6672518.jpeg" width="840"></p>
              <p><img alt="" src="https://hcdn1.luffycity.com/static/frontend/course/5/21天01_1547098127.6672518.jpeg" width="840"></p>
              <p><img alt="" src="https://hcdn1.luffycity.com/static/frontend/course/5/21天01_1547098127.6672518.jpeg" width="840"></p>
            </div>
            <div class="tab-item" v-if="tabIndex==2">
              <div class="tab-item-title">
                <p class="chapter">课程章节</p>
                <p class="chapter-length">共11章 147个课时</p>
              </div>
              <div class="chapter-item">
                <p class="chapter-title"><img src="/static/image/1.svg" alt="">第1章·Linux硬件基础</p>
                <ul class="lesson-list">
                  <li class="lesson-item">
                    <p class="name"><span class="index">1-1</span> 课程介绍-学习流程<span class="free">免费</span></p>
                    <p class="time">07:30 <img src="/static/image/chapter-player.svg"></p>
                    <button class="try">立即试学</button>
                  </li>
                  <li class="lesson-item">
                    <p class="name"><span class="index">1-2</span> 服务器硬件-详解<span class="free">免费</span></p>
                    <p class="time">07:30 <img src="/static/image/chapter-player.svg"></p>
                    <button class="try">立即试学</button>
                  </li>
                </ul>
              </div>
              <div class="chapter-item">
                <p class="chapter-title"><img src="/static/image/1.svg" alt="">第2章·Linux发展过程</p>
                <ul class="lesson-list">
                  <li class="lesson-item">
                    <p class="name"><span class="index">2-1</span> 操作系统组成-Linux发展过程</p>
                    <p class="time">07:30 <img src="/static/image/chapter-player.svg"></p>
                    <button class="try">立即购买</button>
                  </li>
                  <li class="lesson-item">
                    <p class="name"><span class="index">2-2</span> 自由软件-GNU-GPL核心讲解</p>
                    <p class="time">07:30 <img src="/static/image/chapter-player.svg"></p>
                    <button class="try">立即购买</button>
                  </li>
                </ul>
              </div>
            </div>
            <div class="tab-item" v-if="tabIndex==3">
              用户评论
            </div>
            <div class="tab-item" v-if="tabIndex==4">
              常见问题
            </div>
          </div>
          <div class="course-side">
             <div class="teacher-info">
               <h4 class="side-title"><span>授课老师</span></h4>
               <div class="teacher-content">
                 <div class="cont1">
                   <img src="/static/image/马金聚pc2x_1560859575.8268683.png">
                   <div class="name">
                     <p class="teacher-name">李泳谊</p>
                     <p class="teacher-title">老男孩LInux学科带头人</p>
                   </div>
                 </div>
                 <p class="narrative" >Linux运维技术专家，老男孩Linux金牌讲师，讲课风趣幽默、深入浅出、声音洪亮到爆炸</p>
               </div>
             </div>
          </div>
        </div>
      </div>
      <Footer/>
    </div>
</template>

<script>
import Header from "./common/Header"
import Footer from "./common/Footer"

export default {
    name: "Detail",
    data(){
      return {
        course_id: 0,
        tabIndex:2, // 当前选项卡显示的下标
      }
    },
    created(){
      // 课程ID
      this.get_course_id();
    },
    methods: {
      get_course_id(){
        	let course_id = 0;
          //try{
          //  course_id = parseInt(this.$route.params.id);
          //}catch (e) {
            //console.log(e)
          //  console.log(e.message);
          //  course_id = 1
            
          //}
        
          let course_id = this.$route.params.id;
          if(course_id > 0){
              this.course_id = parseInt( course_id );
          }else{
              let self = this;
              this.$alert("对不起，访问页面参数有误！","错误",{
                  callback(){
                    self.$router.go(-1);
                  }
              });
              return false;
          }
          return course_id;
      },
    },
    components:{
      Header,
      Footer,
    }
}
</script>

<style scoped>
.main{
  background: #fff;
  padding-top: 30px;
}
.course-info{
  width: 1200px;
  margin: 0 auto;
  overflow: hidden;
}
.wrap-left{
  float: left;
  width: 690px;
  height: 388px;
  background-color: #000;
}
.wrap-right{
  float: left;
  position: relative;
  height: 388px;
}
.course-name{
  font-size: 20px;
  color: #333;
  padding: 10px 23px;
  letter-spacing: .45px;
}
.data{
  padding-left: 23px;
  padding-right: 23px;
  padding-bottom: 16px;
  font-size: 14px;
  color: #9b9b9b;
}
.sale-time{
  width: 464px;
  background: #fa6240;
  font-size: 14px;
  color: #4a4a4a;
  padding: 10px 23px;
  overflow: hidden;
}
.sale-type {
  font-size: 16px;
  color: #fff;
  letter-spacing: .36px;
  float: left;
}
.sale-time .expire{
  font-size: 14px;
  color: #fff;
  float: right;
}
.sale-time .expire .second{
  width: 24px;
  display: inline-block;
  background: #fafafa;
  color: #5e5e5e;
  padding: 6px 0;
  text-align: center;
}
.course-price{
  background: #fff;
  font-size: 14px;
  color: #4a4a4a;
  padding: 5px 23px;
}
.discount{
  font-size: 26px;
  color: #fa6240;
  margin-left: 10px;
  display: inline-block;
  margin-bottom: -5px;
}
.original{
  font-size: 14px;
  color: #9b9b9b;
  margin-left: 10px;
  text-decoration: line-through;
}
.buy{
  width: 464px;
  padding: 0px 23px;
  position: absolute;
  left: 0;
  bottom: 20px;
  overflow: hidden;
}
.buy .buy-btn{
  float: left;
}
.buy .buy-now{
  width: 125px;
  height: 40px;
  border: 0;
  background: #ffc210;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
  margin-right: 15px;
  outline: none;
}
.buy .free{
  width: 125px;
  height: 40px;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 15px;
  background: #fff;
  color: #ffc210;
  border: 1px solid #ffc210;
}
.add-cart{
  float: right;
  font-size: 14px;
  color: #ffc210;
  text-align: center;
  cursor: pointer;
  margin-top: 10px;
}
.add-cart img{
  width: 20px;
  height: 18px;
  margin-right: 7px;
  vertical-align: middle;
}

.course-tab{
    width: 100%;
    background: #fff;
    margin-bottom: 30px;
    box-shadow: 0 2px 4px 0 #f0f0f0;

}
.course-tab .tab-list{
    width: 1200px;
    margin: auto;
    color: #4a4a4a;
    overflow: hidden;
}
.tab-list li{
    float: left;
    margin-right: 15px;
    padding: 26px 20px 16px;
    font-size: 17px;
    cursor: pointer;
}
.tab-list .active{
    color: #ffc210;
    border-bottom: 2px solid #ffc210;
}
.tab-list .free{
    color: #fb7c55;
}
.course-content{
    width: 1200px;
    margin: 0 auto;
    background: #FAFAFA;
    overflow: hidden;
    padding-bottom: 40px;
}
.course-tab-list{
    width: 880px;
    height: auto;
    padding: 20px;
    background: #fff;
    float: left;
    box-sizing: border-box;
    overflow: hidden;
    position: relative;
    box-shadow: 0 2px 4px 0 #f0f0f0;
}
.tab-item{
    width: 880px;
    background: #fff;
    padding-bottom: 20px;
    box-shadow: 0 2px 4px 0 #f0f0f0;
}
.tab-item-title{
    justify-content: space-between;
    padding: 25px 20px 11px;
    border-radius: 4px;
    margin-bottom: 20px;
    border-bottom: 1px solid #333;
    border-bottom-color: rgba(51,51,51,.05);
    overflow: hidden;
}
.chapter{
    font-size: 17px;
    color: #4a4a4a;
    float: left;
}
.chapter-length{
    float: right;
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .19px;
}
.chapter-title{
    font-size: 16px;
    color: #4a4a4a;
    letter-spacing: .26px;
    padding: 12px;
    background: #eee;
    border-radius: 2px;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-align: center;
    align-items: center;
}
.chapter-title img{
    width: 18px;
    height: 18px;
    margin-right: 7px;
    vertical-align: middle;
}
.lesson-list{
    padding:0 20px;
}
.lesson-list .lesson-item{
    padding: 15px 20px 15px 36px;
    cursor: pointer;
    justify-content: space-between;
    position: relative;
    overflow: hidden;
}
.lesson-item .name{
    font-size: 14px;
    color: #666;
    float: left;
}
.lesson-item .index{
    margin-right: 5px;
}
.lesson-item .free{
    font-size: 12px;
    color: #fff;
    letter-spacing: .19px;
    background: #ffc210;
    border-radius: 100px;
    padding: 1px 9px;
    margin-left: 10px;
}
.lesson-item .time{
    font-size: 14px;
    color: #666;
    letter-spacing: .23px;
    opacity: 1;
    transition: all .15s ease-in-out;
    float: right;
}
.lesson-item .time img{
    width: 18px;
    height: 18px;
    margin-left: 15px;
    vertical-align: text-bottom;
}
.lesson-item .try{
    width: 86px;
    height: 28px;
    background: #ffc210;
    border-radius: 4px;
    font-size: 14px;
    color: #fff;
    position: absolute;
    right: 20px;
    top: 10px;
    opacity: 0;
    transition: all .2s ease-in-out;
    cursor: pointer;
    outline: none;
    border: none;
}
.lesson-item:hover{
    background: #fcf7ef;
    box-shadow: 0 0 0 0 #f3f3f3;
}
.lesson-item:hover .name{
    color: #333;
}
.lesson-item:hover .try{
    opacity: 1;
}

.course-side{
    width: 300px;
    height: auto;
    margin-left: 20px;
    float: right;
}
.teacher-info{
    background: #fff;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px 0 #f0f0f0;
}
.side-title{
    font-weight: normal;
    font-size: 17px;
    color: #4a4a4a;
    padding: 18px 14px;
    border-bottom: 1px solid #333;
    border-bottom-color: rgba(51,51,51,.05);
}
.side-title span{
    display: inline-block;
    border-left: 2px solid #ffc210;
    padding-left: 12px;
}

.teacher-content{
    padding: 30px 20px;
    box-sizing: border-box;
}

.teacher-content .cont1{
    margin-bottom: 12px;
    overflow: hidden;
}

.teacher-content .cont1 img{
    width: 54px;
    height: 54px;
    margin-right: 12px;
    float: left;
}
.teacher-content .cont1 .name{
    float: right;
}
.teacher-content .cont1 .teacher-name{
    width: 188px;
    font-size: 16px;
    color: #4a4a4a;
    padding-bottom: 4px;
}
.teacher-content .cont1 .teacher-title{
    width: 188px;
    font-size: 13px;
    color: #9b9b9b;
    white-space: nowrap;
}
.teacher-content .narrative{
    font-size: 14px;
    color: #666;
    line-height: 24px;
}
</style>

```

路由显示，代码：

```python
import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)
// @ 表示src目录
import Home from "@/components/Home"
import Login from "@/components/Login"
import Register from "@/components/Register"
import Course from "@/components/Course"
import Detail from "@/components/Detail"
export default new Router({
  mode:"history",
  routes: [
    // ....，
    {
      path: '/courses/:id',
      name: 'Detail',
      component: Detail,
    },
  ]
})

```

课程列表的组件中， 打通点击前往详情页的链接地址：

```python
<h3><router-link :to="'/courses/detail/'+course.id">{{course.name}}</router-link> <span><img src="/static/image/avatar1.svg" alt="">{{course.students}}人已加入学习</span></h3>
```



因为接下来的组件中使用了vue-video视频播放组件，所以我们需要先预安装。

安装依赖

```bash
npm install vue-video-player@5.0.2 --save
```

在main.js中注册加载组件

```java
require('video.js/dist/video-js.css');
require('vue-video-player/src/custom-theme.css');
import VideoPlayer from 'vue-video-player'
Vue.use(VideoPlayer);
```



Detail.vue组件中内置vue-video播放器，代码：

分四个步骤：

1. 通过import 导入videoPlayer组件
2. 在vue组件中的component，注册播放器组件
3. 在html中调用videoPlayer组件标签
4. 在data中配置播放器的相关参数

```vue
<template>
    <div class="detail">
      <Header/>
      <div class="main">
        <div class="course-info">
          <div class="wrap-left">
            <videoPlayer class="video-player vjs-custom-skin"
               ref="videoPlayer"
               :playsinline="true"
               :options="playerOptions"
               @play="onPlayerPlay($event)"
               @pause="onPlayerPause($event)">

            </videoPlayer>
          </div>
          <div class="wrap-right">
            <h3 class="course-name">Linux系统基础5周入门精讲</h3>
            <p class="data">23475人在学&nbsp;&nbsp;&nbsp;&nbsp;课程总时长：148课时/180小时&nbsp;&nbsp;&nbsp;&nbsp;难度：初级</p>
            <div class="sale-time">
              <p class="sale-type">限时免费</p>
              <p class="expire">距离结束：仅剩 01天 04小时 33分 <span class="second">08</span> 秒</p>
            </div>
            <p class="course-price">
              <span>活动价</span>
              <span class="discount">¥0.00</span>
              <span class="original">¥29.00</span>
            </p>
            <div class="buy">
              <div class="buy-btn">
                <button class="buy-now">立即购买</button>
                <button class="free">免费试学</button>
              </div>
              <div class="add-cart"><img src="/static/image/cart-yellow.svg" alt="">加入购物车</div>
            </div>
          </div>
        </div>
        <div class="course-tab">
          <ul class="tab-list">
            <li :class="tabIndex==1?'active':''" @click="tabIndex=1">详情介绍</li>
            <li :class="tabIndex==2?'active':''" @click="tabIndex=2">课程章节 <span :class="tabIndex!=2?'free':''">(试学)</span></li>
            <li :class="tabIndex==3?'active':''" @click="tabIndex=3">用户评论 (42)</li>
            <li :class="tabIndex==4?'active':''" @click="tabIndex=4">常见问题</li>
          </ul>
        </div>
        <div class="course-content">
          <div class="course-tab-list">
            <div class="tab-item" v-if="tabIndex==1">
              <p><img alt="" src="https://hcdn1.luffycity.com/static/frontend/course/5/21天01_1547098127.6672518.jpeg" width="840"></p>
              <p><img alt="" src="https://hcdn1.luffycity.com/static/frontend/course/5/21天01_1547098127.6672518.jpeg" width="840"></p>
              <p><img alt="" src="https://hcdn1.luffycity.com/static/frontend/course/5/21天01_1547098127.6672518.jpeg" width="840"></p>
            </div>
            <div class="tab-item" v-if="tabIndex==2">
              <div class="tab-item-title">
                <p class="chapter">课程章节</p>
                <p class="chapter-length">共11章 147个课时</p>
              </div>
              <div class="chapter-item">
                <p class="chapter-title"><img src="/static/image/1.svg" alt="">第1章·Linux硬件基础</p>
                <ul class="lesson-list">
                  <li class="lesson-item">
                    <p class="name"><span class="index">1-1</span> 课程介绍-学习流程<span class="free">免费</span></p>
                    <p class="time">07:30 <img src="/static/image/chapter-player.svg"></p>
                    <button class="try">立即试学</button>
                  </li>
                  <li class="lesson-item">
                    <p class="name"><span class="index">1-2</span> 服务器硬件-详解<span class="free">免费</span></p>
                    <p class="time">07:30 <img src="/static/image/chapter-player.svg"></p>
                    <button class="try">立即试学</button>
                  </li>
                </ul>
              </div>
              <div class="chapter-item">
                <p class="chapter-title"><img src="/static/image/1.svg" alt="">第2章·Linux发展过程</p>
                <ul class="lesson-list">
                  <li class="lesson-item">
                    <p class="name"><span class="index">2-1</span> 操作系统组成-Linux发展过程</p>
                    <p class="time">07:30 <img src="/static/image/chapter-player.svg"></p>
                    <button class="try">立即购买</button>
                  </li>
                  <li class="lesson-item">
                    <p class="name"><span class="index">2-2</span> 自由软件-GNU-GPL核心讲解</p>
                    <p class="time">07:30 <img src="/static/image/chapter-player.svg"></p>
                    <button class="try">立即购买</button>
                  </li>
                </ul>
              </div>
            </div>
            <div class="tab-item" v-if="tabIndex==3">
              用户评论
            </div>
            <div class="tab-item" v-if="tabIndex==4">
              常见问题
            </div>
          </div>
          <div class="course-side">
             <div class="teacher-info">
               <h4 class="side-title"><span>授课老师</span></h4>
               <div class="teacher-content">
                 <div class="cont1">
                   <img src="/static/image/马金聚pc2x_1560859575.8268683.png">
                   <div class="name">
                     <p class="teacher-name">李泳谊</p>
                     <p class="teacher-title">老男孩LInux学科带头人</p>
                   </div>
                 </div>
                 <p class="narrative" >Linux运维技术专家，老男孩Linux金牌讲师，讲课风趣幽默、深入浅出、声音洪亮到爆炸</p>
               </div>
             </div>
          </div>
        </div>
      </div>
      <Footer/>
    </div>
</template>

<script>
import Header from "./common/Header"
import Footer from "./common/Footer"

// 加载组件
import {videoPlayer} from 'vue-video-player';

export default {
    name: "Detail",
    data(){
      return {
        tabIndex:2, // 当前选项卡显示的下标
        playerOptions: {
          playbackRates: [0.7, 1.0, 1.5, 2.0], // 播放速度
          autoplay: false, //如果true,则自动播放
          muted: false, // 默认情况下将会消除任何音频。
          loop: false, // 循环播放
          preload: 'auto',  // 建议浏览器在<video>加载元素后是否应该开始下载视频数据。auto浏览器选择最佳行为,立即开始加载视频（如果浏览器支持）
          language: 'zh-CN',
          aspectRatio: '16:9', // 将播放器置于流畅模式，并在计算播放器的动态大小时使用该值。值应该代表一个比例 - 用冒号分隔的两个数字（例如"16:9"或"4:3"）
          fluid: true, // 当true时，Video.js player将拥有流体大小。换句话说，它将按比例缩放以适应其容器。
          sources: [{ // 播放资源和资源格式
            type: "video/mp4",
            src: "http://img.ksbbs.com/asset/Mon_1703/05cacb4e02f9d9e.mp4" //你的视频地址（必填）
          }],
          poster: "../static/image/course-cover.jpeg", //视频封面图
          width: document.documentElement.clientWidth, // 默认视频全屏时的最大宽度
          notSupportedMessage: '此视频暂无法播放，请稍后再试', //允许覆盖Video.js无法播放媒体源时显示的默认信息。
        }
      }
    },
    methods: {
      onPlayerPlay(event){
        // 当视频播放时，执行的方法
        alert("关闭广告")
      },
      onPlayerPause(event){
        // 当视频暂停播放时，执行的方法
        alert("显示广告");
      },
    },
    components:{
      Header,
      Footer,
      videoPlayer, // 注册组件
    }
}
</script>
```



 

### 后端提供课程详情页数据接口

模型中针对 难度等级返回文本内容而不是等级数值

模型代码：

```python

class Course(BaseModel):
    """
    专题课程
    """
		# ....
    
    level_choices = (
        (0, '初级'),
        (1, '中级'),
        (2, '高级'),
    )
    
    # 省略。。。
    
    @property
    def level_name(self):
        return self.level_choices[self.level][1]
```



课程详情页中的视频是一个封面视频，所以我们给course表添加一个封面视频字段

```python
course_video = models.FileField(upload_to='video',null=True,blank=True,verbose_name='封面视频')
```





序列化器代码:

```python
# 把原来的讲师序列化器增加几个字段
class TeacherSerializer(serializers.ModelSerializer):
    """课程列表的老师信息"""
    class Meta:
        model = Teacher
        fields = ["id","name","role","title","signature","brief","image"]

        
class CourseRetrieveSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    class Meta:
        model = Course
        fields = ["id","name","course_img","students","lessons","pub_lessons","price","teacher","brief","level_name",'course_video']

```



视图代码:

```python
from rest_framework.generics import RetrieveAPIView
from .serializers import CourseRetrieveSerializer
class CourseRetrieveAPIView(RetrieveAPIView):
    queryset = Course.objects.filter(is_delete=False, is_show=True)
    serializer_class = CourseRetrieveSerializer
```



路由代码:

```python
    re_path("(?P<pk>\d+)/", views.CourseRetrieveAPIView.as_view()),
```





### 前端请求api接口并显示数据

```vue
<template>
    <div class="detail">
      <Header/>
      <div class="main">
        <div class="course-info">
          <div class="wrap-left">
            <videoPlayer class="video-player vjs-custom-skin"
               ref="videoPlayer"
               :playsinline="true"
               :options="playerOptions"
               @play="onPlayerPlay($event)"
               @pause="onPlayerPause($event)">

            </videoPlayer>
          </div>
          <div class="wrap-right">
            <h3 class="course-name">{{course_info.name}}</h3>
            <p class="data">{{course_info.students}}人在学&nbsp;&nbsp;&nbsp;&nbsp;课程总时长：{{course_info.lessons}}课时/{{course_info.pub_lessons}}小时&nbsp;&nbsp;&nbsp;&nbsp;难度：{{course_info.level_name}}</p>
            <div class="sale-time">
              <p class="sale-type">限时免费</p>
              <p class="expire">距离结束：仅剩 01天 04小时 33分 <span class="second">08</span> 秒</p>
            </div>
            <p class="course-price">
              <span>活动价</span>
              <span class="discount">¥0.00</span>
              <span class="original">¥{{course_info.price}}</span>
            </p>
            <div class="buy">
              <div class="buy-btn">
                <button class="buy-now">立即购买</button>
                <button class="free">免费试学</button>
              </div>
              <div class="add-cart"><img src="/static/image/cart-yellow.svg" alt="">加入购物车</div>
            </div>
          </div>
        </div>
        <div class="course-tab">
          <ul class="tab-list">
            <li :class="tabIndex==1?'active':''" @click="tabIndex=1">详情介绍</li>
            <li :class="tabIndex==2?'active':''" @click="tabIndex=2">课程章节 <span :class="tabIndex!=2?'free':''">(试学)</span></li>
            <li :class="tabIndex==3?'active':''" @click="tabIndex=3">用户评论 (42)</li>
            <li :class="tabIndex==4?'active':''" @click="tabIndex=4">常见问题</li>
          </ul>
        </div>
        <div class="course-content">
          <div class="course-tab-list">
            <div class="tab-item" v-if="tabIndex==1">
              <div class="course-brief" v-html="course_info.brief_text"></div>
            </div>
            <div class="tab-item" v-if="tabIndex==2">
              <div class="tab-item-title">
                <p class="chapter">课程章节</p>
                <p class="chapter-length">共11章 147个课时</p>
              </div>
              <div class="chapter-item">
                <p class="chapter-title"><img src="/static/image/1.svg" alt="">第1章·Linux硬件基础</p>
                <ul class="lesson-list">
                  <li class="lesson-item">
                    <p class="name"><span class="index">1-1</span> 课程介绍-学习流程<span class="free">免费</span></p>
                    <p class="time">07:30 <img src="/static/image/chapter-player.svg"></p>
                    <button class="try">立即试学</button>
                  </li>
                  <li class="lesson-item">
                    <p class="name"><span class="index">1-2</span> 服务器硬件-详解<span class="free">免费</span></p>
                    <p class="time">07:30 <img src="/static/image/chapter-player.svg"></p>
                    <button class="try">立即试学</button>
                  </li>
                </ul>
              </div>
              <div class="chapter-item">
                <p class="chapter-title"><img src="/static/image/1.svg" alt="">第2章·Linux发展过程</p>
                <ul class="lesson-list">
                  <li class="lesson-item">
                    <p class="name"><span class="index">2-1</span> 操作系统组成-Linux发展过程</p>
                    <p class="time">07:30 <img src="/static/image/chapter-player.svg"></p>
                    <button class="try">立即购买</button>
                  </li>
                  <li class="lesson-item">
                    <p class="name"><span class="index">2-2</span> 自由软件-GNU-GPL核心讲解</p>
                    <p class="time">07:30 <img src="/static/image/chapter-player.svg"></p>
                    <button class="try">立即购买</button>
                  </li>
                </ul>
              </div>
            </div>
            <div class="tab-item" v-if="tabIndex==3">
              用户评论
            </div>
            <div class="tab-item" v-if="tabIndex==4">
              常见问题
            </div>
          </div>
          <div class="course-side">
             <div class="teacher-info">
               <h4 class="side-title"><span>授课老师</span></h4>
               <div class="teacher-content">
                 <div class="cont1">
                   <img :src="course_info.teacher.image">
                   <div class="name">
                     <p class="teacher-name">{{course_info.teacher.name}} {{course_info.teacher.title}}</p>
                     <p class="teacher-title">{{course_info.teacher.signature}}</p>
                   </div>
                 </div>
                 <p class="narrative" >{{course_info.teacher.brief}}</p>
               </div>
             </div>
          </div>
        </div>
      </div>
      <Footer/>
    </div>
</template>

<script>
import Header from "./common/Header"
import Footer from "./common/Footer"

// 加载组件
import {videoPlayer} from 'vue-video-player';

export default {
    name: "Detail",
    data(){
      return {
        tabIndex:2, // 当前选项卡显示的下标
        course_info: {}, // 课程信息
        playerOptions: {
          playbackRates: [0.7, 1.0, 1.5, 2.0], // 播放速度
          autoplay: false, //如果true,则自动播放
          muted: false, // 默认情况下将会消除任何音频。
          loop: false, // 循环播放
          preload: 'auto',  // 建议浏览器在<video>加载元素后是否应该开始下载视频数据。auto浏览器选择最佳行为,立即开始加载视频（如果浏览器支持）
          language: 'zh-CN',
          aspectRatio: '16:9', // 将播放器置于流畅模式，并在计算播放器的动态大小时使用该值。值应该代表一个比例 - 用冒号分隔的两个数字（例如"16:9"或"4:3"）
          fluid: true, // 当true时，Video.js player将拥有流体大小。换句话说，它将按比例缩放以适应其容器。
          sources: [{ // 播放资源和资源格式
            type: "video/mp4",
            src: "http://img.ksbbs.com/asset/Mon_1703/05cacb4e02f9d9e.mp4" //你的视频地址（必填）
          }],
          poster: "../static/image/course-cover.jpeg", //视频封面图
          width: document.documentElement.clientWidth, // 默认视频全屏时的最大宽度
          notSupportedMessage: '此视频暂无法播放，请稍后再试', //允许覆盖Video.js无法播放媒体源时显示的默认信息。
        }
      }
    },
    created(){
      this.get_course_data();
    },
    methods: {
      onPlayerPlay(event){
        // 当视频播放时，执行的方法
        alert("关闭广告")
      },
      onPlayerPause(event){
        // 当视频暂停播放时，执行的方法
        alert("显示广告");
      },
      get_course_data(){
        // 获取地址栏上面的课程ID
        let course_id = this.$route.params.course;
        if( course_id < 1 ){
          let _this = this;
          _this.$alert("对不起，当前视频不存在！","警告",{
            callback(){
              _this.$router.go(-1);
            }
          });
        }

        // ajax请求课程信息
        this.$axios.get(`${this.$settings.Host}/courses/${course_id}/`).then(response=>{
          // console.log(response.data);
          this.course_info = response.data;
        }).catch(response=>{
          this.$message({
            message:"对不起，访问页面出错！请联系客服工作人员！"
          })
        })
      },
    },
    components:{
      Header,
      Footer,
      videoPlayer, // 注册组件
    }
}
</script>

<style scoped>
.main{
  background: #fff;
  padding-top: 30px;
}
.course-info{
  width: 1200px;
  margin: 0 auto;
  overflow: hidden;
}
.wrap-left{
  float: left;
  width: 690px;
  height: 388px;
  background-color: #000;
}
.wrap-right{
  float: left;
  position: relative;
  height: 388px;
}
.course-name{
  font-size: 20px;
  color: #333;
  padding: 10px 23px;
  letter-spacing: .45px;
}
.data{
  padding-left: 23px;
  padding-right: 23px;
  padding-bottom: 16px;
  font-size: 14px;
  color: #9b9b9b;
}
.sale-time{
  width: 464px;
  background: #fa6240;
  font-size: 14px;
  color: #4a4a4a;
  padding: 10px 23px;
  overflow: hidden;
}
.sale-type {
  font-size: 16px;
  color: #fff;
  letter-spacing: .36px;
  float: left;
}
.sale-time .expire{
  font-size: 14px;
  color: #fff;
  float: right;
}
.sale-time .expire .second{
  width: 24px;
  display: inline-block;
  background: #fafafa;
  color: #5e5e5e;
  padding: 6px 0;
  text-align: center;
}
.course-price{
  background: #fff;
  font-size: 14px;
  color: #4a4a4a;
  padding: 5px 23px;
}
.discount{
  font-size: 26px;
  color: #fa6240;
  margin-left: 10px;
  display: inline-block;
  margin-bottom: -5px;
}
.original{
  font-size: 14px;
  color: #9b9b9b;
  margin-left: 10px;
  text-decoration: line-through;
}
.buy{
  width: 464px;
  padding: 0px 23px;
  position: absolute;
  left: 0;
  bottom: 20px;
  overflow: hidden;
}
.buy .buy-btn{
  float: left;
}
.buy .buy-now{
  width: 125px;
  height: 40px;
  border: 0;
  background: #ffc210;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
  margin-right: 15px;
  outline: none;
}
.buy .free{
  width: 125px;
  height: 40px;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 15px;
  background: #fff;
  color: #ffc210;
  border: 1px solid #ffc210;
}
.add-cart{
  float: right;
  font-size: 14px;
  color: #ffc210;
  text-align: center;
  cursor: pointer;
  margin-top: 10px;
}
.add-cart img{
  width: 20px;
  height: 18px;
  margin-right: 7px;
  vertical-align: middle;
}

.course-tab{
    width: 100%;
    background: #fff;
    margin-bottom: 30px;
    box-shadow: 0 2px 4px 0 #f0f0f0;

}
.course-tab .tab-list{
    width: 1200px;
    margin: auto;
    color: #4a4a4a;
    overflow: hidden;
}
.tab-list li{
    float: left;
    margin-right: 15px;
    padding: 26px 20px 16px;
    font-size: 17px;
    cursor: pointer;
}
.tab-list .active{
    color: #ffc210;
    border-bottom: 2px solid #ffc210;
}
.tab-list .free{
    color: #fb7c55;
}
.course-content{
    width: 1200px;
    margin: 0 auto;
    background: #FAFAFA;
    overflow: hidden;
    padding-bottom: 40px;
}
.course-tab-list{
    width: 880px;
    height: auto;
    padding: 20px;
    background: #fff;
    float: left;
    box-sizing: border-box;
    overflow: hidden;
    position: relative;
    box-shadow: 0 2px 4px 0 #f0f0f0;
}
.tab-item{
    width: 880px;
    background: #fff;
    padding-bottom: 20px;
    box-shadow: 0 2px 4px 0 #f0f0f0;
}
.tab-item-title{
    justify-content: space-between;
    padding: 25px 20px 11px;
    border-radius: 4px;
    margin-bottom: 20px;
    border-bottom: 1px solid #333;
    border-bottom-color: rgba(51,51,51,.05);
    overflow: hidden;
}

.chapter{
    font-size: 17px;
    color: #4a4a4a;
    float: left;
}
.chapter-length{
    float: right;
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .19px;
}
.chapter-title{
    font-size: 16px;
    color: #4a4a4a;
    letter-spacing: .26px;
    padding: 12px;
    background: #eee;
    border-radius: 2px;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-align: center;
    align-items: center;
}
.chapter-title img{
    width: 18px;
    height: 18px;
    margin-right: 7px;
    vertical-align: middle;
}
.lesson-list{
    padding:0 20px;
}
.lesson-list .lesson-item{
    padding: 15px 20px 15px 36px;
    cursor: pointer;
    justify-content: space-between;
    position: relative;
    overflow: hidden;
}
.lesson-item .name{
    font-size: 14px;
    color: #666;
    float: left;
}
.lesson-item .index{
    margin-right: 5px;
}
.lesson-item .free{
    font-size: 12px;
    color: #fff;
    letter-spacing: .19px;
    background: #ffc210;
    border-radius: 100px;
    padding: 1px 9px;
    margin-left: 10px;
}
.lesson-item .time{
    font-size: 14px;
    color: #666;
    letter-spacing: .23px;
    opacity: 1;
    transition: all .15s ease-in-out;
    float: right;
}
.lesson-item .time img{
    width: 18px;
    height: 18px;
    margin-left: 15px;
    vertical-align: text-bottom;
}
.lesson-item .try{
    width: 86px;
    height: 28px;
    background: #ffc210;
    border-radius: 4px;
    font-size: 14px;
    color: #fff;
    position: absolute;
    right: 20px;
    top: 10px;
    opacity: 0;
    transition: all .2s ease-in-out;
    cursor: pointer;
    outline: none;
    border: none;
}
.lesson-item:hover{
    background: #fcf7ef;
    box-shadow: 0 0 0 0 #f3f3f3;
}
.lesson-item:hover .name{
    color: #333;
}
.lesson-item:hover .try{
    opacity: 1;
}

.course-side{
    width: 300px;
    height: auto;
    margin-left: 20px;
    float: right;
}
.teacher-info{
    background: #fff;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px 0 #f0f0f0;
}
.side-title{
    font-weight: normal;
    font-size: 17px;
    color: #4a4a4a;
    padding: 18px 14px;
    border-bottom: 1px solid #333;
    border-bottom-color: rgba(51,51,51,.05);
}
.side-title span{
    display: inline-block;
    border-left: 2px solid #ffc210;
    padding-left: 12px;
}

.teacher-content{
    padding: 30px 20px;
    box-sizing: border-box;
}

.teacher-content .cont1{
    margin-bottom: 12px;
    overflow: hidden;
}

.teacher-content .cont1 img{
    width: 54px;
    height: 54px;
    margin-right: 12px;
    float: left;
}
.teacher-content .cont1 .name{
    float: right;
}
.teacher-content .cont1 .teacher-name{
    width: 188px;
    font-size: 16px;
    color: #4a4a4a;
    padding-bottom: 4px;
}
.teacher-content .cont1 .teacher-title{
    width: 188px;
    font-size: 13px;
    color: #9b9b9b;
    white-space: nowrap;
}
.teacher-content .narrative{
    font-size: 14px;
    color: #666;
    line-height: 24px;
}
</style>

```



样式重置，static/css/reset.css，代码：

```css
.course-brief img{
  width: 100%;
}
```





### 后端提供当前课程对应的章节和课时列表信息

courses/serializers.py,序列化器，代码：

```python
from .models import CourseCategory,Course,Teacher,CourseChapter,CourseLesson
class CourseLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLesson
        fields = ["id","name","duration","free_trail"]

class CourseChapterSerializer(serializers.ModelSerializer):
    coursesections = CourseLessonSerializer(many=True)
    class Meta:
        model = CourseChapter
        fields = ["chapter","name","summary","coursesections"]
```

courses/views.py视图，代码：

```python
from .models import CourseChapter
from .serializers import CourseChapterSerializer
class CourseChapterListAPIView(ListAPIView):
    queryset = CourseChapter.objects.filter(is_deleted=False, is_show=True).order_by("chapter")
    serializer_class = CourseChapterSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['course', ]
```



courses/urls.py路由，代码：

```python
    re_path("chapters/", views.CourseChapterListAPIView.as_view()),
```



### 前端请求章节信息展示到页面中

```vue
<template>
    <div class="detail">
      <Header/>
      <div class="main">
        <div class="course-info">
          <div class="wrap-left">
            <videoPlayer class="video-player vjs-custom-skin"
               ref="videoPlayer"
               :playsinline="true"
               :options="playerOptions"
               @play="onPlayerPlay($event)"
               @pause="onPlayerPause($event)">

            </videoPlayer>
          </div>
          <div class="wrap-right">
            <h3 class="course-name">{{course_info.name}}</h3>
            <p class="data">{{course_info.students}}人在学&nbsp;&nbsp;&nbsp;&nbsp;课程总时长：{{course_info.lessons}}课时/{{course_info.pub_lessons}}小时&nbsp;&nbsp;&nbsp;&nbsp;难度：{{course_info.level_name}}</p>
            <div class="sale-time">
              <p class="sale-type">限时免费</p>
              <p class="expire">距离结束：仅剩 01天 04小时 33分 <span class="second">08</span> 秒</p>
            </div>
            <p class="course-price">
              <span>活动价</span>
              <span class="discount">¥0.00</span>
              <span class="original">¥{{course_info.price}}</span>
            </p>
            <div class="buy">
              <div class="buy-btn">
                <button class="buy-now">立即购买</button>
                <button class="free">免费试学</button>
              </div>
              <div class="add-cart"><img src="/static/image/cart-yellow.svg" alt="">加入购物车</div>
            </div>
          </div>
        </div>
        <div class="course-tab">
          <ul class="tab-list">
            <li :class="tabIndex==1?'active':''" @click="tabIndex=1">详情介绍</li>
            <li :class="tabIndex==2?'active':''" @click="tabIndex=2">课程章节 <span :class="tabIndex!=2?'free':''">(试学)</span></li>
            <li :class="tabIndex==3?'active':''" @click="tabIndex=3">用户评论 (42)</li>
            <li :class="tabIndex==4?'active':''" @click="tabIndex=4">常见问题</li>
          </ul>
        </div>
        <div class="course-content">
          <div class="course-tab-list">
            <div class="tab-item" v-if="tabIndex==1">
              <div class="course-brief" v-html="course_info.brief_text"></div>
            </div>
            <div class="tab-item" v-if="tabIndex==2">
              <div class="tab-item-title">
                <p class="chapter">课程章节</p>
                <p class="chapter-length">共{{course_chapters.length}}章 {{course_info.lessons}}个课时</p>
              </div>
              <div class="chapter-item" v-for="chapter in course_chapters">
                <p class="chapter-title"><img src="/static/image/1.svg" alt="">第{{chapter.chapter}}章·{{chapter.name}}</p>
                <ul class="lesson-list">
                  <li class="lesson-item" v-for="lesson in chapter.coursesections">
                    <p class="name"><span class="index">{{chapter.chapter}}-{{lesson.id}}</span> {{lesson.name}}<span class="free" v-if="lesson.free_trail">免费</span></p>
                    <p class="time">{{lesson.duration}} <img src="/static/image/chapter-player.svg"></p>
                    <button class="try" v-if="lesson.free_trail">立即试学</button>
                    <button class="try" v-else>立即购买</button>
                  </li>
                </ul>
              </div>
            </div>
            <div class="tab-item" v-if="tabIndex==3">
              用户评论
            </div>
            <div class="tab-item" v-if="tabIndex==4">
              常见问题
            </div>
          </div>
          <div class="course-side">
             <div class="teacher-info">
               <h4 class="side-title"><span>授课老师</span></h4>
               <div class="teacher-content">
                 <div class="cont1">
                   <img :src="course_info.teacher.image">
                   <div class="name">
                     <p class="teacher-name">{{course_info.teacher.name}} {{course_info.teacher.title}}</p>
                     <p class="teacher-title">{{course_info.teacher.signature}}</p>
                   </div>
                 </div>
                 <p class="narrative" >{{course_info.teacher.brief}}</p>
               </div>
             </div>
          </div>
        </div>
      </div>
      <Footer/>
    </div>
</template>

<script>
import Header from "./common/Header"
import Footer from "./common/Footer"

// 加载组件
import {videoPlayer} from 'vue-video-player';

export default {
    name: "Detail",
    data(){
      return {
        tabIndex:2,   // 当前选项卡显示的下标
        course_id: 0, // 当前课程信息的ID
        course_info: {
          teacher:{},
        }, // 课程信息
        course_chapters:[], // 课程的章节课时列表
        playerOptions: {
          playbackRates: [0.7, 1.0, 1.5, 2.0], // 播放速度
          autoplay: false, //如果true,则自动播放
          muted: false, // 默认情况下将会消除任何音频。
          loop: false, // 循环播放
          preload: 'auto',  // 建议浏览器在<video>加载元素后是否应该开始下载视频数据。auto浏览器选择最佳行为,立即开始加载视频（如果浏览器支持）
          language: 'zh-CN',
          aspectRatio: '16:9', // 将播放器置于流畅模式，并在计算播放器的动态大小时使用该值。值应该代表一个比例 - 用冒号分隔的两个数字（例如"16:9"或"4:3"）
          fluid: true, // 当true时，Video.js player将拥有流体大小。换句话说，它将按比例缩放以适应其容器。
          sources: [{ // 播放资源和资源格式
            type: "video/mp4",
            src: "http://img.ksbbs.com/asset/Mon_1703/05cacb4e02f9d9e.mp4" //你的视频地址（必填）
          }],
          poster: "../static/image/course-cover.jpeg", //视频封面图
          width: document.documentElement.clientWidth, // 默认视频全屏时的最大宽度
          notSupportedMessage: '此视频暂无法播放，请稍后再试', //允许覆盖Video.js无法播放媒体源时显示的默认信息。
        }
      }
    },
    created(){
      this.get_course_id();
      this.get_course_data();
      this.get_chapter();
    },
    methods: {
      onPlayerPlay(event){
        // 当视频播放时，执行的方法
        alert("关闭广告")
      },
      onPlayerPause(event){
        // 当视频暂停播放时，执行的方法
        alert("显示广告");
      },
      get_course_id(){
        // 获取地址栏上面的课程ID
        this.course_id = this.$route.params.course;
        if( this.course_id < 1 ){
          let _this = this;
          _this.$alert("对不起，当前视频不存在！","警告",{
            callback(){
              _this.$router.go(-1);
            }
          });
        }
      },
      get_course_data(){
        // ajax请求课程信息
        this.$axios.get(`${this.$settings.Host}/courses/${this.course_id}/`).then(response=>{
          // console.log(response.data);
          this.course_info = response.data;
        }).catch(response=>{
          this.$message({
            message:"对不起，访问页面出错！请联系客服工作人员！"
          })
        })
      },

      get_chapter(){
        // 获取当前课程对应的章节课时信息
        this.$axios.get(`${this.$settings.Host}/courses/chapters/`,{
          params:{
            "course": this.course_id,
          }
        }).then(response=>{
          this.course_chapters = response.data;
        }).catch(error=>{
          console.log(error.response);
        })
      },
    },
    components:{
      Header,
      Footer,
      videoPlayer, // 注册组件
    }
}
</script>

<style scoped>
.main{
  background: #fff;
  padding-top: 30px;
}
.course-info{
  width: 1200px;
  margin: 0 auto;
  overflow: hidden;
}
.wrap-left{
  float: left;
  width: 690px;
  height: 388px;
  background-color: #000;
}
.wrap-right{
  float: left;
  position: relative;
  height: 388px;
}
.course-name{
  font-size: 20px;
  color: #333;
  padding: 10px 23px;
  letter-spacing: .45px;
}
.data{
  padding-left: 23px;
  padding-right: 23px;
  padding-bottom: 16px;
  font-size: 14px;
  color: #9b9b9b;
}
.sale-time{
  width: 464px;
  background: #fa6240;
  font-size: 14px;
  color: #4a4a4a;
  padding: 10px 23px;
  overflow: hidden;
}
.sale-type {
  font-size: 16px;
  color: #fff;
  letter-spacing: .36px;
  float: left;
}
.sale-time .expire{
  font-size: 14px;
  color: #fff;
  float: right;
}
.sale-time .expire .second{
  width: 24px;
  display: inline-block;
  background: #fafafa;
  color: #5e5e5e;
  padding: 6px 0;
  text-align: center;
}
.course-price{
  background: #fff;
  font-size: 14px;
  color: #4a4a4a;
  padding: 5px 23px;
}
.discount{
  font-size: 26px;
  color: #fa6240;
  margin-left: 10px;
  display: inline-block;
  margin-bottom: -5px;
}
.original{
  font-size: 14px;
  color: #9b9b9b;
  margin-left: 10px;
  text-decoration: line-through;
}
.buy{
  width: 464px;
  padding: 0px 23px;
  position: absolute;
  left: 0;
  bottom: 20px;
  overflow: hidden;
}
.buy .buy-btn{
  float: left;
}
.buy .buy-now{
  width: 125px;
  height: 40px;
  border: 0;
  background: #ffc210;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
  margin-right: 15px;
  outline: none;
}
.buy .free{
  width: 125px;
  height: 40px;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 15px;
  background: #fff;
  color: #ffc210;
  border: 1px solid #ffc210;
}
.add-cart{
  float: right;
  font-size: 14px;
  color: #ffc210;
  text-align: center;
  cursor: pointer;
  margin-top: 10px;
}
.add-cart img{
  width: 20px;
  height: 18px;
  margin-right: 7px;
  vertical-align: middle;
}

.course-tab{
    width: 100%;
    background: #fff;
    margin-bottom: 30px;
    box-shadow: 0 2px 4px 0 #f0f0f0;

}
.course-tab .tab-list{
    width: 1200px;
    margin: auto;
    color: #4a4a4a;
    overflow: hidden;
}
.tab-list li{
    float: left;
    margin-right: 15px;
    padding: 26px 20px 16px;
    font-size: 17px;
    cursor: pointer;
}
.tab-list .active{
    color: #ffc210;
    border-bottom: 2px solid #ffc210;
}
.tab-list .free{
    color: #fb7c55;
}
.course-content{
    width: 1200px;
    margin: 0 auto;
    background: #FAFAFA;
    overflow: hidden;
    padding-bottom: 40px;
}
.course-tab-list{
    width: 880px;
    height: auto;
    padding: 20px;
    background: #fff;
    float: left;
    box-sizing: border-box;
    overflow: hidden;
    position: relative;
    box-shadow: 0 2px 4px 0 #f0f0f0;
}
.tab-item{
    width: 880px;
    background: #fff;
    padding-bottom: 20px;
    box-shadow: 0 2px 4px 0 #f0f0f0;
}
.tab-item-title{
    justify-content: space-between;
    padding: 25px 20px 11px;
    border-radius: 4px;
    margin-bottom: 20px;
    border-bottom: 1px solid #333;
    border-bottom-color: rgba(51,51,51,.05);
    overflow: hidden;
}

.chapter{
    font-size: 17px;
    color: #4a4a4a;
    float: left;
}
.chapter-length{
    float: right;
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .19px;
}
.chapter-title{
    font-size: 16px;
    color: #4a4a4a;
    letter-spacing: .26px;
    padding: 12px;
    background: #eee;
    border-radius: 2px;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-align: center;
    align-items: center;
}
.chapter-title img{
    width: 18px;
    height: 18px;
    margin-right: 7px;
    vertical-align: middle;
}
.lesson-list{
    padding:0 20px;
}
.lesson-list .lesson-item{
    padding: 15px 20px 15px 36px;
    cursor: pointer;
    justify-content: space-between;
    position: relative;
    overflow: hidden;
}
.lesson-item .name{
    font-size: 14px;
    color: #666;
    float: left;
}
.lesson-item .index{
    margin-right: 5px;
}
.lesson-item .free{
    font-size: 12px;
    color: #fff;
    letter-spacing: .19px;
    background: #ffc210;
    border-radius: 100px;
    padding: 1px 9px;
    margin-left: 10px;
}
.lesson-item .time{
    font-size: 14px;
    color: #666;
    letter-spacing: .23px;
    opacity: 1;
    transition: all .15s ease-in-out;
    float: right;
}
.lesson-item .time img{
    width: 18px;
    height: 18px;
    margin-left: 15px;
    vertical-align: text-bottom;
}
.lesson-item .try{
    width: 86px;
    height: 28px;
    background: #ffc210;
    border-radius: 4px;
    font-size: 14px;
    color: #fff;
    position: absolute;
    right: 20px;
    top: 10px;
    opacity: 0;
    transition: all .2s ease-in-out;
    cursor: pointer;
    outline: none;
    border: none;
}
.lesson-item:hover{
    background: #fcf7ef;
    box-shadow: 0 0 0 0 #f3f3f3;
}
.lesson-item:hover .name{
    color: #333;
}
.lesson-item:hover .try{
    opacity: 1;
}

.course-side{
    width: 300px;
    height: auto;
    margin-left: 20px;
    float: right;
}
.teacher-info{
    background: #fff;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px 0 #f0f0f0;
}
.side-title{
    font-weight: normal;
    font-size: 17px;
    color: #4a4a4a;
    padding: 18px 14px;
    border-bottom: 1px solid #333;
    border-bottom-color: rgba(51,51,51,.05);
}
.side-title span{
    display: inline-block;
    border-left: 2px solid #ffc210;
    padding-left: 12px;
}

.teacher-content{
    padding: 30px 20px;
    box-sizing: border-box;
}

.teacher-content .cont1{
    margin-bottom: 12px;
    overflow: hidden;
}

.teacher-content .cont1 img{
    width: 54px;
    height: 54px;
    margin-right: 12px;
    float: left;
}
.teacher-content .cont1 .name{
    float: right;
}
.teacher-content .cont1 .teacher-name{
    width: 188px;
    font-size: 16px;
    color: #4a4a4a;
    padding-bottom: 4px;
}
.teacher-content .cont1 .teacher-title{
    width: 188px;
    font-size: 13px;
    color: #9b9b9b;
    white-space: nowrap;
}
.teacher-content .narrative{
    font-size: 14px;
    color: #666;
    line-height: 24px;
}
</style>
```

效果：

![1557895744328](assets/1557895744328.png)



