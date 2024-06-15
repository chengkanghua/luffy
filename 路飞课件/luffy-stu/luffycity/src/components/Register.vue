<template>
	<div class="box">
		<img src="../../static/image/Loginbg.3377d0c.jpg" alt="">
		<div class="register">
			<div class="register_box">
        <div class="register-title">注册路飞学城</div>
				<div class="inp">
					<input v-model = "mobile" type="text" placeholder="手机号码" class="user" @blur="checkMobile">
          <input v-model = "password" type="password" placeholder="登录密码" class="user">

          <div class="sms-box">
            <input v-model = "sms_code" type="text" maxlength='6' placeholder="输入验证码" class="user">
            <div id="sms_btn" class="sms-btn"  @click="smsHandler" >{{sms_msg}}</div>
          </div>

          <!-- <div id="geetest"></div>滑动验证这里我就不加了 -->
					<button class="register_btn" @click="registerHandler">注册</button>
					<p class="go_login" >已有账号 <router-link to="/login/">直接登录</router-link></p>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
  name: 'Register',
  data(){
    return {
        sms_code:"",
        mobile:"",
      	password:"",
        sms_msg:'点击发送短信',
        is_send_sms:false,  //是否已经发送过短信的标记
        validateResult:false,
        flag:false,  //判断定时器是否已经开启了
    }
  },
  created(){
  },
  methods:{

    //校验手机号唯一性
    checkMobile(){
      if (! /^1[3-9]\d{9}$/.test(this.mobile)){
        this.$message.error('手机号格式不对！');
        return false;
      }

      this.$axios.get(`${this.$settings.Host}/users/mobile/${this.mobile}/`)
      .then((res)=>{

      })
      .catch((error)=>{
        console.log(error.response.data);
        this.$message.error(error.response.data.msg);
      })
    },

    registerHandler(){
      this.$axios.post(`${this.$settings.Host}/users/register/`,{
        mobile:this.mobile,
        sms_code:this.sms_code,
        password:this.password,
      })
      .then((res)=>{
        console.log(res.data);
        localStorage.removeItem('user_token')
        localStorage.removeItem('id')
        localStorage.removeItem('username')
        sessionStorage.user_token = res.data.token;
        sessionStorage.id = res.data.id;
        sessionStorage.username = res.data.username;
        let ths = this;
        this.$alert('注册成功','路飞',{
          callback(){
            ths.$router.push('/');
          }
        })

      })
      .catch((error)=>{
        // console.log(error.response.data);
        let data = error.response.data
        let message = '';
        for (let key in data){
          message = data[key][0];
        }
        this.$message.error(message);

      })
    },

    smsHandler(){
      // let btn = document.getElementById('sms_btn');
      // btn.setAttribute('disabled','disabled');
      // 前端手机格式验证



      let interval_time = 60;

      if (this.flag === false){
        let t = setInterval(()=>{
          if (interval_time <=1 ){
            clearInterval(t);
            // btn.removeAttribute('disabled');
            this.sms_msg = '点击发送短信';
            this.flag = false;
          }else {
            // this.is_send_sms = true;
            this.sms_msg = `${interval_time}秒后重新发送`;
            interval_time--;
          }
        },1000)
        this.flag = true;
      }else {
        return false;
      }



      this.$axios.get(`${this.$settings.Host}/users/sms/${this.mobile}/`)
      .then((res)=>{
        console.log(res.data);
      })
      .catch((error)=>{
        this.$message.error(error.response.data.msg);
        // console.log();
      })
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
.box .register {
	position: absolute;
	width: 500px;
	height: 400px;
	top: 0;
	left: 0;
  margin: auto;
  right: 0;
  bottom: 0;
  top: -120px;
}
.register .register-title{
    width: 100%;
    font-size: 24px;
    text-align: center;
    padding-top: 30px;
    padding-bottom: 30px;
    color: #4a4a4a;
    letter-spacing: .39px;
}
.register-title img{
    width: 190px;
    height: auto;
}
.register-title p{
    font-family: PingFangSC-Regular;
    font-size: 18px;
    color: #fff;
    letter-spacing: .29px;
    padding-top: 10px;
    padding-bottom: 50px;
}
.register_box{
    width: 400px;
    height: auto;
    background: #fff;
    box-shadow: 0 2px 4px 0 rgba(0,0,0,.5);
    border-radius: 4px;
    margin: 0 auto;
    padding-bottom: 40px;
}
.register_box .title{
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
.register_box .title span:nth-of-type(1){
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
.register_btn{
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

.sms-box{
  position: relative;
}
.sms-btn{
    font-size: 14px;
    color: #ffc210;
    letter-spacing: .26px;
    position: absolute;
    right: 16px;
    top: 10px;
    cursor: pointer;
    overflow: hidden;
    background: #fff;
    border-left: 1px solid #484848;
    padding-left: 16px;
    padding-bottom: 4px;
}
</style>

