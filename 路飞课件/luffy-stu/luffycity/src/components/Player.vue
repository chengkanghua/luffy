<template>
    <div class="player">
      <div id="player"></div>
    </div>
</template>

<script>
export default {
  name:"Player",
  data () {
    return {

    }
  },
  methods: {
    check_login(){
        // 检查当前访问者是否登录了！
        let token = localStorage.user_token || sessionStorage.user_token;
        if( !token ){
          this.$alert("对不起，您尚未登录，请登录以后再进行学习。").then(()=>{
            this.$router.push("/user/login");
          });
          return false; // 阻止代码往下执行
        }
        return token;
      },
  },

  mounted(){
      let jwt_token = this.check_login();

      let user_name = localStorage.user_name || sessionStorage.user_name;

      // 1. 到数据库中查询用户购买的课程，是否有当前章节
      // 2. 到数据库中查询当前用户购买的课程是否在有效期内
      // 3. 播放页面显示课程章节和课时的播放列表
    	// 4. 通过vid播放不同的课时视频
    	// 以上4个功能自行完成
      let vid = "e3a65556c5de813fdaeee5b94da6868c_e"; // this.$route.query.vid;
      let self = this;
      var player = polyvPlayer({
        wrap: '#player',
        width: document.documentElement.clientWidth-260, // 页面宽度
        height: document.documentElement.clientHeight, // 页面高度
        forceH5: true,  //支持h5标准
        vid: vid,
        code: user_name, // 一般是用户昵称
        // 视频加密播放的配置
        playsafe: function (vid, next) { // 向后端发送请求获取加密的token
            self.$axios.get(`${self.$settings.Host}/course/polyv/`,{
              params:{
                vid: vid,
              },
              headers:{
                "Authorization":"jwt " + jwt_token,
              }
            }).then(function (response) {
                // 获取播放视频的token令牌
              console.log(response);

                next(response.data);  //token字符串
            })
        }
      });
  },

  computed: {
  },

}
</script>

<style scoped>
</style>
