<template>
<!--    <h1>轮播图组件</h1>-->
  <el-carousel indicator-position="outside" height="400px">
    <el-carousel-item v-for="(value,index) in banner_list" :key="value.id">

      <a :href="value.link" style="display: inline-block;height: 400px;width: 100%">
        <img :src="value.img_src" alt="" width="100%" height="400px">
      </a>
<!--      <img src="@/assets/banner/banner1.png" alt="">-->
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
            banner_list:[

              // {id:1,img_src:require('@/assets/banner/banner1.png'),link:'http://www.baidu.com'},
              // {id:2,img_src:'@/assets/banner/banner2.png',link:'http://www.baidu.com'},
              // {id:3,img_src:'@/assets/banner/banner3.png',link:'http://www.baidu.com'},
            //数据属性中写图片路径的方式
              // 方式1：通过require映射成static路径下的图片路径
            //   {id:1,img_src:require('@/assets/banner/banner1.png'),link:'http://www.baidu.com'},
            //   {id:2,img_src:require('@/assets/banner/banner2.png'),link:'http://www.baidu.com'},
            //   {id:3,img_src:require('@/assets/banner/banner3.png'),link:'http://www.baidu.com'},

              //方式2：直接使用static目录
            {id:1,img_src:'../../../static/banner/banner1.png',link:'http://www.baidu.com'},
              {id:2,img_src:'../../../static/banner/banner2.png',link:'http://www.baidu.com'},
              {id:3,img_src:'../../../static/banner/banner3.png',link:'http://www.baidu.com'},

            ]
          }
      }
    }
</script>

<style scoped>

</style>
