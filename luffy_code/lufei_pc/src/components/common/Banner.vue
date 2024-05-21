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
