<template>

    <div class="course">
      <Header></Header>
      <div class="main">
<!--        筛选功能-->
        <div class="top" style="overflow: hidden;">
          <ul>
            <li :class="{this:num===0}" @click="num=0">全部</li>
            <li :class="{this:num===index+1}" v-for="(value,index) in screen_list" :key="index" @click="num=index+1">{{value}}</li>

          </ul>

        </div>
<!--        课程列表-->
        <div class="course-main">
          <div class="session">
            <div>
              <div class="name">
                Python开发
              </div>
              <ul>
                <li>
                  <router-link to="/detail">
                    <div class="img-box">
                      <div></div>
                      <img src="@/assets/list01.png" alt="">
                    </div>
                    <div class="course-item">
                      <p class="title">跟随Alex金角大王3周上手Python开发</p>
                      <div class="item-number">
                        <p class="num">
                          <img src="@/assets/bofang.png" alt="">
                          <span>78168</span>
                          人在学
                        </p>
                        <p class="time">
                          <span>入门</span>
                          <span>19小时</span>
                        </p>
                      </div>
                    </div>
                  </router-link>
                </li>
                <li>
                  <router-link to="">
                    <div class="img-box">
                      <div></div>
                      <img src="@/assets/list01.png" alt="">
                    </div>
                    <div class="course-item">
                      <p class="title">跟随Alex金角大王3周上手Python开发</p>
                      <div class="item-number">
                        <p class="num">
                          <img src="@/assets/bofang.png" alt="">
                          <span>78168</span>
                          人在学
                        </p>
                        <p class="time">
                          <span>入门</span>
                          <span>19小时</span>
                        </p>
                      </div>
                    </div>
                  </router-link>
                </li>
                <li>
                  <router-link to="">
                    <div class="img-box">
                      <div></div>
                      <img src="@/assets/list01.png" alt="">
                    </div>
                    <div class="course-item">
                      <p class="title">跟随Alex金角大王3周上手Python开发</p>
                      <div class="item-number">
                        <p class="num">
                          <img src="@/assets/bofang.png" alt="">
                          <span>78168</span>
                          人在学
                        </p>
                        <p class="time">
                          <span>入门</span>
                          <span>19小时</span>
                        </p>
                      </div>
                    </div>
                  </router-link>
                </li>
                <li>
                  <router-link to="">
                    <div class="img-box">
                      <div></div>
                      <img src="@/assets/list01.png" alt="">
                    </div>
                    <div class="course-item">
                      <p class="title">跟随Alex金角大王3周上手Python开发</p>
                      <div class="item-number">
                        <p class="num">
                          <img src="@/assets/bofang.png" alt="">
                          <span>78168</span>
                          人在学
                        </p>
                        <p class="time">
                          <span>入门</span>
                          <span>19小时</span>
                        </p>
                      </div>
                    </div>
                  </router-link>
                </li>
              </ul>
            </div>
          </div>

        </div>
      </div>
      <Footer></Footer>
    </div>

</template>

<script>
  import Header from './common/Header'
  import Footer from './common/Footer'
    export default {
        name: "Course",
        data(){
          return {
            screen_list:['Python开发', 'Linux云计算','Web前端','Java','Go语言&C语言'],
            num:0,  //作为选中哪个课程分类的标记
          }
        },
        components:{
          Header,
          Footer,
        }
    }
</script>

<style scoped>
  .main{
    width: 100%;
    height: auto;
    display: flex;
    flex: 1;
    background: #f9f9f9;
    flex-direction: column;
  }
  .main .top{
    width: 100%;
    height: 60px;
    background: #fff;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 20px;
  }
  .main .top ul{
    width: 1200px;
    height: auto;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
  }
  .main .top ul .this{
    color: #f5a623;
  }
  .main .top ul li{
    color: #4a4a4a;
    font-size: 14px;
    margin-bottom: 20px;
    margin-right: 50px;
    cursor: pointer;
  }

  .course-main{
    width: 100%;
    display: flex;
    align-items: center;
    flex: 1;
    flex-direction: column;
  }
  .course-main .session{
    height: auto;
    flex-direction: column;
    width: 100%;
    display: flex;
    align-items: center;
  }
  .session .name{
    width: 1200px;
    font-size: 24px;
    color: #4a4a4a;
    margin-top: 60px;
    padding-left: 15px;
    padding-bottom: 15px;
    text-align: left;
  }
  .session ul{
    width: 1200px;
    height: auto;
    display: flex;
    flex-wrap: wrap;
    padding-bottom: 38px;
  }
  .session ul li{
    width: 384px;
    height: auto;
    margin-right: 12px;
    margin-bottom: 42px;
    cursor: pointer;
  }
  .session ul li a{
    display: flex;
    flex-wrap: wrap;
  }
  .session ul li .img-box{
    width: 100%;
    height: 217px;
    position: relative;
  }
  .session ul li .img-box div{
    width: 100%;
    height: 100%;
    position: absolute;
    left: 0;
    top: 0;
    background: hsla(0,0%,100%,.2);
    display: none;
    z-index: 1;
  }
  .session ul li .img-box img{
    width: 100%;
    height: 217px;
    border-radius: 4px 4px 0 0;
  }
  .course-item{
    width: 384px;
    height: 138px;
    background: #fff;
    padding-left: 22px;
    padding-right: 22px;
    box-sizing: border-box;
    border-radius: 0 0 4px 4px;
    box-shadow: 0 5px 20px 0 #e8e8e8;
  }
  .course-item .title{
    width: 340px;
    color: #5e5e5e;
    font-size: 16px;
    padding-top: 39px;
    margin-bottom: 10px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .item-number{
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .item-number .num{
    color: #9d9d9d;
    font-size: 14px;
    display: flex;
    align-items: center;
  }
  .item-number .num img{
    width: 17px;
    height: 17px;
    margin-right: 7px;
  }
  .item-number .time{
    font-size: 14px;
    color: #9d9d9d;
  }
  .item-number .time:first-child{
    margin-right: 22px;
  }


</style>
