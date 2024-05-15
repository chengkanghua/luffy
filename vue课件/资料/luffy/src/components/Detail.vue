<template>
    <div class="detail">
      <Header></Header>
      <div class="routerView">
        <div class="course-intro">
          <div class="intro-top" style="background: rgb(95, 58, 72);">
            <p class="return active">
              <img src="@/assets/triangle.png" alt="">
              返回免费课主页
            </p>

            <div class="intro-data">
              <h1>Python21天入门</h1>
              <p>
                <span>
                  课程小节：
                  <b>87</b>
                  小节
                </span>
                <span>
                  时长：
                  <b>19</b>
                  小时

                </span>
                <span>
                  <b>78511</b>
                  人在学
                </span>
              </p>
            </div>

            <div class="course-nav" style="background: rgb(95, 58, 72);">
              <ul>
                <li :class="{this:course_item_switch===0}" @click="course_item_switch=0">
                  <p>课程详情</p>
                </li>
                <li :class="{this:course_item_switch===1}" @click="course_item_switch=1">
                  <p>讨论提问</p>
                  <span>(236)</span>

                </li>
                <li :class="{this:course_item_switch===2}" @click="course_item_switch=2">
                  <p>课件下载</p>
                </li>
              </ul>
            </div>
          </div>
          <div class="course-intro-item">
            <div v-if="course_item_switch===0" class="intro-content">
              <div class="course-item-box">
                <div class="content-item">
                  <div class="title">介绍</div>
                  <article>
                    即使之前你从未写过1行代码，也能在学完本课程后，达到Python入门水平，能开发300-500行代码的小程序，掌握基本的编程思维、软件设计方法。无论你日后想做人工智能、数据分析，还是WEB开发、爬虫、大数据等，都应该先把这部分基础掌握。
                  </article>
                  <div class="title">你将会学到的</div>
                  <ul>
                    <li>
                      <img src="@/assets/dui.png" alt="">
                      <p>学会Python基础语法</p>
                    </li>
                    <li>
                      <img src="@/assets/dui.png" alt="">
                      <p>学会Python基础语法</p>
                    </li>
                    <li>
                      <img src="@/assets/dui.png" alt="">
                      <p>掌握Python字符编码&数据类型</p>
                    </li>
                  </ul>
                </div>
                <div class="course-outline">
                  <div class="title">
                    <p class="title-name">
                      课程大纲
                    </p>
                    <p class="title-side">
                      <span>全部收起</span>
                      <span>
                        <b>87</b>
                        小节
                      </span>
                      <span>
                        18:31:54
                      </span>
                    </p>
                  </div>

<!--                  大纲部分-->
                  <ul class="outline-list">
                    <li class="list-data">
                      <div class="list-data-title">
                        <div class="list-name">
                          <img class="open hide" src="@/assets/jiahao.png" alt="">
                          <img class="us" src="@/assets/jianhao.png" alt="">
                          <p>第1章·基本语法</p>
                        </div>
                        <div class="list-num">
                          <span class="section-num hide">
                            <b>28</b>
                            小节
                          </span>
                          <span>
                            4:42:34
                          </span>
                        </div>
                      </div>
                      <ul class="list-data-item">
                        <li class="login">
                          <div class="data-item-name">
                            <img src="@/assets/bofang1.png" alt="" class="img1">
                            <img src="@/assets/bofang2.png" alt="" class="img2">
                            <p>
                              1
                              .
                              1
                              编程语言是如何演变过来的
                            </p>
                          </div>
                          <div class="data-item-num">
                            <span class="type">预览</span>
                            <span class="time">17:50</span>
                          </div>
                        </li>
                        <li class="login">
                          <div class="data-item-name">
                            <img src="@/assets/bofang1.png" alt="" class="img1">
                            <img src="@/assets/bofang2.png" alt="" class="img2">
                            <p>
                              1
                              .
                              1
                              编程语言是如何演变过来的
                            </p>
                          </div>
                          <div class="data-item-num">
                            <span class="type">预览</span>
                            <span class="time">17:50</span>
                          </div>
                        </li>
                        <li class="login">
                          <div class="data-item-name">
                            <img src="@/assets/bofang1.png" alt="" class="img1">
                            <img src="@/assets/bofang2.png" alt="" class="img2">
                            <p>
                              1
                              .
                              1
                              编程语言是如何演变过来的
                            </p>
                          </div>
                          <div class="data-item-num">
                            <span class="type">预览</span>
                            <span class="time">17:50</span>
                          </div>
                        </li>
                        <li class="login">
                          <div class="data-item-name">
                            <img src="@/assets/bofang1.png" alt="" class="img1">
                            <img src="@/assets/bofang2.png" alt="" class="img2">
                            <p>
                              1
                              .
                              1
                              编程语言是如何演变过来的
                            </p>
                          </div>
                          <div class="data-item-num">
                            <span class="type">预览</span>
                            <span class="time">17:50</span>
                          </div>
                        </li>
                        <li class="login">
                          <div class="data-item-name">
                            <img src="@/assets/bofang1.png" alt="" class="img1">
                            <img src="@/assets/bofang2.png" alt="" class="img2">
                            <p>
                              1
                              .
                              1
                              编程语言是如何演变过来的
                            </p>
                          </div>
                          <div class="data-item-num">
                            <span class="type">预览</span>
                            <span class="time">17:50</span>
                          </div>
                        </li>
                        <li class="login">
                          <div class="data-item-name">
                            <img src="@/assets/bofang1.png" alt="" class="img1">
                            <img src="@/assets/bofang2.png" alt="" class="img2">
                            <p>
                              1
                              .
                              1
                              编程语言是如何演变过来的
                            </p>
                          </div>
                          <div class="data-item-num">
                            <span class="type">预览</span>
                            <span class="time">17:50</span>
                          </div>
                        </li>
                      </ul>
                    </li>
                    <li class="list-data">
                      <div class="list-data-title">
                        <div class="list-name">
                          <img class="open hide" src="@/assets/jiahao.png" alt="">
                          <img class="us" src="@/assets/jianhao.png" alt="">
                          <p>第1章·基本语法</p>
                        </div>
                        <div class="list-num">
                          <span class="section-num hide">
                            <b>28</b>
                            小节
                          </span>
                          <span>
                            4:42:34
                          </span>
                        </div>
                      </div>
                      <ul class="list-data-item">
                        <li class="login">
                          <div class="data-item-name">
                            <img src="@/assets/bofang1.png" alt="" class="img1">
                            <img src="@/assets/bofang2.png" alt="" class="img2">
                            <p>
                              1
                              .
                              1
                              编程语言是如何演变过来的
                            </p>
                          </div>
                          <div class="data-item-num">
                            <span class="type">预览</span>
                            <span class="time">17:50</span>
                          </div>
                        </li>
                        <li class="login">
                          <div class="data-item-name">
                            <img src="@/assets/bofang1.png" alt="" class="img1">
                            <img src="@/assets/bofang2.png" alt="" class="img2">
                            <p>
                              1
                              .
                              1
                              编程语言是如何演变过来的
                            </p>
                          </div>
                          <div class="data-item-num">
                            <span class="type">预览</span>
                            <span class="time">17:50</span>
                          </div>
                        </li>
                        <li class="login">
                          <div class="data-item-name">
                            <img src="@/assets/bofang1.png" alt="" class="img1">
                            <img src="@/assets/bofang2.png" alt="" class="img2">
                            <p>
                              1
                              .
                              1
                              编程语言是如何演变过来的
                            </p>
                          </div>
                          <div class="data-item-num">
                            <span class="type">预览</span>
                            <span class="time">17:50</span>
                          </div>
                        </li>
                        <li class="login">
                          <div class="data-item-name">
                            <img src="@/assets/bofang1.png" alt="" class="img1">
                            <img src="@/assets/bofang2.png" alt="" class="img2">
                            <p>
                              1
                              .
                              1
                              编程语言是如何演变过来的
                            </p>
                          </div>
                          <div class="data-item-num">
                            <span class="type">预览</span>
                            <span class="time">17:50</span>
                          </div>
                        </li>
                        <li class="login">
                          <div class="data-item-name">
                            <img src="@/assets/bofang1.png" alt="" class="img1">
                            <img src="@/assets/bofang2.png" alt="" class="img2">
                            <p>
                              1
                              .
                              1
                              编程语言是如何演变过来的
                            </p>
                          </div>
                          <div class="data-item-num">
                            <span class="type">预览</span>
                            <span class="time">17:50</span>
                          </div>
                        </li>
                        <li class="login">
                          <div class="data-item-name">
                            <img src="@/assets/bofang1.png" alt="" class="img1">
                            <img src="@/assets/bofang2.png" alt="" class="img2">
                            <p>
                              1
                              .
                              1
                              编程语言是如何演变过来的
                            </p>
                          </div>
                          <div class="data-item-num">
                            <span class="type">预览</span>
                            <span class="time">17:50</span>
                          </div>
                        </li>
                      </ul>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <div v-if="course_item_switch===1">
              讨论问题部分
            </div>
            <div v-if="course_item_switch===2">
              课件下载部分
            </div>
<!--            右侧边栏-->
            <div class="course-side">
              <div class="side-video">
                <div class="video-box">

                  <video-player class="video-player vjs-custom-skin"
                       ref="videoPlayer"
                       :playsinline="true"
                       :options="playerOptions"
                       @play="onPlayerPlay($event)"
                       @pause="onPlayerPause($event)"
                  >
                  </video-player>
<!--                  <img src="@/assets/PY1.png" alt="">-->
<!--                  <p>-->
<!--                    <img src="@/assets/triangle_1.svg" alt="">-->
<!--                  </p>-->
                </div>
                <div class="student-prower">
                  <div class="title">
                    学霸团专属权益
                  </div>
                  <ul>
                    <li>
                      <img style="width: 18px;height: 20px" src="@/assets/ziliao.png" alt="">
                      <p>课件下载</p>
                    </li>
                    <li>
                      <img style="width: 17px;height: 17px" src="@/assets/gongkaike.png" alt="">
                      <p>定期公开课</p>
                    </li>
                    <li>
                      <img style="width: 21px;height: 18px" src="@/assets/jiaoliu.png" alt="">
                      <p>
                        学员交流
                        <br>
                        QQ群：
                        701031800
                      </p>
                    </li>
                    <li>
                      <img style="width: 18px;height: 18px" src="@/assets/answer.png" alt="">
                      <p>导师答疑</p>
                    </li>
                  </ul>
                  <p class="btns start-study">继续学习</p>
                  <a target="_blank" class="btns add-team" href="https://jq.qq.com/?_wv=1027&k=5XfBMXm">加入学霸团</a>

                </div>
              </div>
<!--              <div class="side-video"></div>-->
            </div>
          </div>
          <div class="preview-video beyond"></div>
        </div>
      </div>
      <Footer></Footer>
    </div>
</template>

<script>
    import Header from "./common/Header";
    import Footer from "./common/Footer";
    import {videoPlayer} from 'vue-video-player';

    export default {
        name: "Detail",
      data(){
          return {
            course_item_switch:0,

            playerOptions: {
              playbackRates: [0.7, 1.0, 1.5, 2.0], // 播放速度
              autoplay: false, //如果true,则自动播放
              muted: false, // 默认情况下将会消除任何音频。
              loop: false, // 循环播放
              preload: 'auto', // 建议浏览器在<video>加载元素后是否应该开始下载视频数据。auto浏览器选择最佳行为,立即开始加载视频（如果浏览器支持）
              language: 'zh-CN',
              aspectRatio: '16:9', // 将播放器置于流畅模式，并在计算播放器的动态大小时使用该值。值应该代表一个比例 - 用冒号分隔的两个数字（例如"16:9"或"4:3"）

              fluid: true, // 当true时，Video.js player将拥有流体大小。换句话说，它将按比例缩放以适应其容器。
              sources: [{
                type: "video/mp4",//还可以配置其他格式
                src: "http://img.ksbbs.com/asset/Mon_1703/05cacb4e02f9d9e.mp4" //你的视频地址（必填）
              },
              ],

              poster: "../../static/PY1.png", //视频封面图
              width: document.documentElement.clientWidth,
              notSupportedMessage: '此视频暂无法播放，请稍后再试', //允许覆盖Video.js无法播放媒体源时显示的默认信息。
            }
          }
      },
      components:{
          Header,
          Footer,
      },
      methods:{
          onPlayerPlay(player) {
            alert("play");
          },
          onPlayerPause(player){
            alert("pause");
          },
          player() { //创建player插件对象实例
            return this.$refs.videoPlayer.player
          }
      }

    }
</script>

<style scoped>

  .course-intro-item .course-side{
    width: 374px;
    height: auto;
    margin-top: -260px;
    float: right;
    z-index: 2;
    position: relative;
  }
  .course-intro-item .course-side .side-video{
    width: 100%;
    height: auto;
    background: #fff;
    border-radius: 6px;
    box-shadow: 0 2px 4px 0 #f3f3f3;
    border: 1px solid #e8e8e8;
  }
  .course-intro-item .course-side .side-video .video-box{
    width: 100%;
    height: auto;
    position: relative;
    padding: 5px 4px 27px;
    box-sizing: border-box;
    cursor: pointer;
  }
  .course-intro-item .course-side .side-video .video-box img{
    width: 100%;
    height: auto;
  }
  .course-intro-item .course-side .side-video .video-box p{
    width: 104px;
    height: 104px;
    border-radius: 100%;
    background: hsla(0,0%,100%,.2);
    position: absolute;
    left: 50%;
    top: 50%;
    margin-left: -52px;
    margin-top: -62px;
    text-align: center;
    line-height: 104px;
  }
  .course-intro-item .course-side .side-video .video-box p img{
    width: 46px;
    height: auto;
    margin-left: 12px;
  }
  .course-intro-item .course-side .side-video .student-prower{
    padding: 0 31px 30px;
    box-sizing: border-box;
  }
  .course-intro-item .course-side .side-video .student-prower .title{
    color: #000;
    font-size: 15px;
    font-weight: 400;
    margin-bottom: 20px;
  }
  .course-intro-item .course-side .side-video .student-prower ul{
      width: 100%;
    height: auto;
    display: flex;
    flex-wrap: wrap;
  }
  .course-intro-item .course-side .side-video .student-prower ul li{
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    margin-right: 10px;
  }
  .course-intro-item .course-side .side-video .student-prower ul li img{
    margin-right: 6px;
  }
  .course-intro-item .course-side .side-video .student-prower ul li p{
    width: 119px;
    font-size: 12px;
    color: #4a4a4a;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .course-intro-item .course-side .side-video .student-prower .start-study{
    color: #fff;
    margin-top: 27px;
    margin-bottom: 12px;
    background: #ffc210;
  }
  .course-intro-item .course-side .side-video .student-prower .btns{
    width: 100%;
    height: 52px;
    line-height: 52px;
    border-radius: 2px;
    font-size: 18px;
    font-weight: 500;
    padding-left: 111px;
    box-sizing: border-box;
    cursor: pointer;
    display: block;
    text-decoration: none;
  }
  .course-intro-item .course-side .side-video .student-prower .add-team{
    color: #f5a623;
    border: 1px solid #f5a623;
    box-sizing: border-box;
  }


  .course-intro-item .intro-content{
    width: 780px;
    float: left;
  }
  .intro-content .course-item-box{
    width: 100%;
    height: auto;
  }
  .course-item-box .content-item{
    width: 100%;
    height: auto;
    border-radius: 4px;
    padding: 30px 20px 15px;
    background: #f3f3f3;
    box-sizing: border-box;
    box-shadow: 0 2px 4px 0 #f3f3f3;
  }
  .content-item .title{
    color: #000;
    font-size: 22px;
  }
  .content-item article{
    font-size: 14px;
    color: #5e5e5e;
    margin-top: 10px;
    line-height: 28px;
    margin-bottom: 50px;
  }
  .content-item ul{
    width: 100%;
    display: flex;
    flex-wrap: wrap;
    margin-top: 17px;
  }
  .content-item ul li{
    display: flex;
    align-items: center;
    margin-right: 36px;
    margin-bottom: 15px;
  }
  .content-item ul li img {
    width: 18px;
    height: 18px;
    margin-right: 12px;
  }
  .content-item ul li p{
    width: 303px;
    font-size: 14px;
    color: #5e5e5e;
  }

  .course-item-box .course-outline{
    width: 100%;
  }
  .course-outline .title{
    margin-top: 50px;
    margin-bottom: 13px;
    padding-left: 17px;
    padding-right: 20px;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    box-sizing: border-box;
  }
  .course-outline .title .title-name{
    color: #000;
    font-size: 22px;
  }
  .course-outline .title .title-side{
    display: flex;
    align-items: center;
    font-size: 14px;
  }
  .course-outline .title .title-side span:first-of-type{
    color: #2a2a2a;
    margin-right: 39px;
    cursor: pointer;
  }

  .course-outline .title .title-side span:nth-of-type(2){
    min-width: 43px;
    text-align: right;
    color: #4a4a4a;
    display: inline-block;
  }

  .course-outline .title .title-side span:nth-of-type(3){
    width: 80px;
    color: #4a4a4a;
    margin-left: 17px;
    text-align: right;
    display: inline-block;
  }
  .course-outline .outline-list{
    width: 100%;
    height: auto;
  }

  .course-outline .outline-list .list-data{
    width: 780px;
    height: auto;
    margin-bottom: 2px;
  }
  .course-outline .outline-list .list-data .list-data-title{
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #f9f9f9;
    padding-left: 26px;
    padding-right: 20px;
    border-radius: 2px;
    box-sizing: border-box;
    margin-bottom: 1px;
    cursor: pointer;
  }
  .outline-list .list-data .list-data-title .list-name{
    display: flex;
    align-items: center;
  }

  .list-data .list-data-title .list-name img{
    width: 10px;
    height: auto;
    margin-right: 15px;
  }
  .list-data .list-data-title .list-name p{
    width: 546px;
    font-size: 15px;
    color: #5e5e5e;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .list-data .list-data-title .list-num{
    display: flex;
    align-items: center;
  }
  .list-data .list-data-title .list-num span:first-of-type{
    min-width: 43px;
    text-align: right;
    color: #4a4a4a;
    display: inline-block;
  }
  .list-data .list-data-title .list-num span:nth-of-type(2){
    width: 80px;
    color: #4a4a4a;
    margin-left: 17px;
    text-align: right;
    display: inline-block;
  }


  .outline-list .list-data .list-data-item {
    width: 100%;
    height: auto;
    margin-bottom: 4px;
    border-top: 1px solid #dadada;
  }

  .outline-list .list-data .list-data-item li{
    cursor: pointer;
    width: 100%;
    height: 48px;
    background: #fff;
    border-radius: 2px;
    border: 1px solid #dadada;
    border-top: none;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-left: 50px;
    padding-right: 20px;
    box-sizing: border-box;
    color: #6ca4c5;
  }
  .outline-list .list-data .list-data-item li .data-item-name{
    display: flex;
    align-items: center;
  }
  .outline-list .list-data .list-data-item li .data-item-name img{
    width: 16px;
    height: 16px;
    margin-right: 9px;
  }
  .outline-list .list-data .list-data-item li .data-item-name .img2{
    display: none;
  }
  .outline-list .list-data .list-data-item li .data-item-name p{
    width: 430px;
    font-size: 14px;
  }

  .outline-list .list-data .list-data-item li .data-item-num{
    display: flex;
    align-items: center;
  }
  .outline-list .list-data .list-data-item li .data-item-num .type{
    min-width: 43px;
    text-align: right;
    display: inline-block;
  }
  .outline-list .list-data .list-data-item li .data-item-num .time{
    width: 80px;
    margin-left: 17px;
    text-align: right;
    display: inline-block;
  }

  .course-intro{
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: auto;
    /*padding-bottom: 40px;*/
  }

  .intro-top{
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 300px;
    position: relative;
  }
  .intro-top .return{
    color: #fff;
    width: 1200px;
    font-size: 16px;
    font-weight: 500;
    margin-top: 30px;
    margin-bottom: 38px;
    display: flex;
    cursor: pointer;
    align-items: center;
  }
  .intro-top .return img{
    width: 6px;
    height: 11px;
    margin-right: 6px;
  }
  .intro-top .intro-data{
    width: 1200px;
    padding-left: 23px;
  }
  .intro-data h1{
    width: 780px;
    font-size: 36px;
    color: #fff;
    font-weight: 400;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .intro-data p{
    width: 780px;
    color: #fff;
    font-size: 16px;
    margin-top: 8px;
  }
  .intro-data p span{
    margin-right: 26px;
  }
  .intro-top .course-nav{
    width: 100%;
    height: 72px;
    display: flex;
    align-items: center;
    flex-direction: column;
    position: absolute;
    left: 0;
    top: 228px;
  }
  .course-nav ul{
    width: 1200px;
    display: flex;
    align-items: center;
    padding-left: 23px;
    box-sizing: border-box;
  }
  .course-nav ul .this{
    color: #fff;
    font-weight: 500;
  }
  .course-nav ul li{
    font-size: 16px;
    margin-top: 14px;
    color: #e9e9e9;
    margin-right: 26px;
    display: flex;
    cursor: pointer;
    box-sizing: border-box;
  }
  .course-nav ul li p{
    padding-bottom: 4px;
  }
  .course-nav ul .this p{
    box-shadow: 0 2px 0 0 #fff;
  }
  .course-nav ul li span{
    padding-bottom: 4px;
    /*padding-top: 16px;*/
  }
  .course-intro-item{
    width: 1200px;
    margin-top: 24px;
  }



</style>

