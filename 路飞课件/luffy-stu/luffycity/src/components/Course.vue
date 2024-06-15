<template>
  <div class="course">
    <Header></Header>
    <div class="main">
      <!-- 筛选条件 -->
      <div class="condition">
        <ul class="cate-list">
          <li class="title">课程分类:</li>
          <li @click="category=0" :class="{this:category===0}">全部</li>
          <li @click="category=value.id" :class="{this:category===value.id}" v-for="(value,index) in category_list" :key="value.id">{{value.name}}</li>


        </ul>

        <div class="ordering">
          <ul>
            <li class="title">筛&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;选: </li>
            <li class="default" @click="change_order_type('id')" :class="chang_order_class('id')">默认</li>
            <li @click="change_order_type('students')" class="hot " :class="chang_order_class('students')">人气</li>
            <li @click="change_order_type('price')" class="price" :class="chang_order_class('price')">价格</li>
          </ul>
          <p class="condition-result">共21个课程</p>
        </div>

      </div>
      <!-- 课程列表 -->
      <div class="course-list">
        <div v-for="(value,index) in course_list" class="course-item">
          <div class="course-image">
            <img :src="value.course_img" alt="">
          </div>
          <div class="course-info">
            <h3><router-link :to="'/course/detail/'+value.id+'/'">{{value.name}}</router-link> <span><img src="/static/image/avatar1.svg" alt="">{{value.students}}人已加入学习</span></h3>
            <p class="teather-info">{{value.teacher.name}} {{value.teacher.signature}} {{value.teacher.title}} <span >共{{value.lessons}}课时/{{value.lessons===value.pub_lessons?'更新完成':`已更新${value.pub_lessons}课时`}}</span></p>
            <ul class="lesson-list">
              <li v-for="(item,i) in value.lesson_list"><span class="lesson-title">0{{i+1}} | 第{{item.lesson}}节：{{item.name}}</span> <span class="free" v-if="item.free_trail">免费</span></li>

            </ul>
            <div class="pay-box">
              <span class="discount-type" v-if="value.discount_name">{{value.discount_name}}</span>
              <span class="discount-price">￥{{value.real_price}}元</span>
              <span class="original-price" v-if="value.discount_name">原价：{{value.price}}元</span>
              <span class="buy-now">立即购买</span>
            </div>
          </div>
        </div>

      </div>
    </div>

    <el-pagination
      background
      layout="prev, pager, next,sizes,jumper"
      @current-change="handleCurrentChange"
      @size-change="handleSizeChange"
      :page-size="filters.size"
      :page-sizes="[2,3,5,10]"
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
          category:0, //标记哪个课程分类被选中了，默认是全部
          category_list:[],  //存放课程分类
          total:0, // 总数据量
          filters:{
            type:'id', //标记当前选中的是哪个排序功能
            orders:'desc',  //标记当前的排序状态
            size:5,  // 每页显示条数
            page:1,  //当前用户点击的页码
          },
          course_list:[],
        }
      },
      components:{
        Header,
        Footer,
      },
      watch:{ //监听category数据属性的变化，一旦变化就会触发它对应的函数
        category(){
          this.get_course();
        }
      }
      ,
    created() {
        this.get_category();
        this.get_course();
    },

    methods:{

        handleSizeChange(size){
          this.filters.size = size;
          this.get_course();
        },

        handleCurrentChange(page){
          this.filters.page = page;
          this.get_course();
        },

        get_category(){
          this.$axios.get(`${this.$settings.Host}/course/category/`)
          .then((res)=>{
            this.category_list = res.data;
          })
          .catch((error)=>{
            console.log(error.response);
          })
        },

        //获取课程数据
        get_course(){
          let filters = {
            page:this.filters.page,
            size:this.filters.size,
          };
          if (this.category > 0){
            filters.course_category = this.category;
          }

          if (this.filters.orders === 'desc'){
            filters.ordering = '-' + this.filters.type;
          }else {
            filters.ordering = this.filters.type;
          }

          // filters.ordering = '-id'

          //http://api.luffycity.cn:8001/course/list/?course_category=6&ordering=id
          this.$axios.get(`${this.$settings.Host}/course/list/`,{
            params:filters,
          })
          .then((res)=>{
            let data = res.data;
            this.course_list = res.data.results;
            this.total = data.count;
          })
          .catch((res)=>{
            console.log(res.response);
          })
        },

        change_order_type(type){  //'id'
          if (this.filters.type === type && this.filters.orders==='desc'){
            this.filters.orders = 'asc';

          }else if(this.filters.type === type && this.filters.orders==='asc'){
            this.filters.orders = 'desc';
          }
          this.filters.type = type;

          //点击切换排序规则时，触发请求数据的动作
          this.get_course();

        }  ,


        // 修改排序标签的样式
        chang_order_class(type){
          // console.log(type);
          // console.log(this.filters.type);
          if(type === this.filters.type && this.filters.orders==='desc'){

            return 'this asc';
          }else if(type === this.filters.type && this.filters.orders==='asc'){
             return 'this desc';
          }else {
            return '';
          }

        }

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
  }
  .course .ordering .price{
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

  .course .ordering .desc::after{
    border-top: 5px solid #f5a623;
  }
  .course .ordering .asc::before{
    border-bottom: 5px solid #f5a623;
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
</style>

