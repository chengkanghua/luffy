<template>
	<div class="box">
		<img src="../../static/image/Loginbg.3377d0c.jpg" alt="">
		<div class="register">
			<div class="register_box">
        <div class="register-title">注册路飞学城</div>
				<div class="inp">
					<input v-model = "mobile" type="text" @blur="checkMobile" placeholder="手机号码" class="user">
          <input v-model = "password" type="password" placeholder="登录密码" class="user">
          <div class="sms-box">
            <input v-model = "sms_code" type="text" maxlength='4' placeholder="输入验证码" class="user">
            <div class="sms-btn" @click="smsHandle">{{sms_text}}</div>
            <!-- <div class="sms-btn" @click="smsHandle">点击发送短信</div> -->
          </div>
          <!-- <div id="geetest"></div>滑动验证这里我就不加了 -->
					<button class="register_btn" @click="registerHander">注册</button>
					<p class="go_login" >已有账号 <router-link to="/user/login">直接登录</router-link></p>
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
        validateResult:false,
        is_send:false,    // 是否已经发送短信的状态
        send_intervel:60, // 发送短信的间隔
        sms_text:"点击发送短信", // 发送短信的提示
    }
  },
  created(){
  },
  methods:{
    checkMobile(){
              if(!this.mobile){return} //空值的时候不要检查
              // 检查手机号的合法性[格式和是否已经注册]
              this.$axios.get(`${this.$settings.Host}/user/mobile/${this.mobile}/`)
              .then(
                 response=>{
                    // console.log(response)
                    this.$message.success(response.data.message);
                 }
              ).catch(err=>{
                  // console.log(err)
                  this.$message.error(err.response.data.message);
              });


          },
    registerHander(){
              // 用户注册
              this.$axios.post(`${this.$settings.Host}/user/register/`,{
                mobile: this.mobile,
                sms_code:this.sms_code,
                password:this.password,
              }).then(response=>{
                //默认是不需要记住密码的功能的，所以我们存到sessionStorage中
                console.log(response.data);
                localStorage.removeItem("user_token");
                localStorage.removeItem("user_id");
                localStorage.removeItem("user_name");
                sessionStorage.user_token = response.data.token;
                sessionStorage.user_id = response.data.id;
                sessionStorage.user_name = response.data.username;

                // 页面跳转
                let self = this;
                this.$alert("注册成功!","路飞学城",{
                   callback(){
                        self.$router.push("/");
                   }
                });

              }).catch(error=>{
                let data = error.response.data;
                let message = "";
                for(let key in data){
                    message = data[key][0];
                }
                this.$message.error(message);
              });
    },
    smsHandle(){
            // 判断是否填写了手机
            if( !/^\d{11}$/.test(this.mobile) ){
              this.$alert('手机号码格式有误!', '警告');
              return false;
            }

            // 判断是否在60s内有发送过短信,如果有则,不能点击发送
            if(this.is_send){
              this.$alert('60s内不能频繁发送短信!', '警告');
              return false;
            }

            this.$axios.get(this.$settings.Host+`/user/sms/${this.mobile}/`).then(response=>{
              let data = response.data
              if( data.status == '0' ){
                this.$alert(data.result);  // 短信发送失败
              }else{
                this.is_send = true;
                let _this = this
                let num = _this.send_intervel
                _this.$alert(data.result,"成功",{
                  callback(){
                      let intervalID = setInterval(()=>{
                        if(num<=1){
                          _this.sms_text = "点击发送短信";
                          _this.is_send = false;
                          clearInterval(intervalID);
                        }else{
                          num--;
                          _this.sms_text = num + "秒后发送短信";
                        }

                    },1000)
                  }
                });

              }
            }).catch(error=>{
                console.log(error.response)
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
