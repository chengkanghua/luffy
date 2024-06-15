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
							<input type="checkbox" class="no" name="a" v-model="remember"/>
							<span>记住密码</span>
						</p>
						<p>忘记密码</p>
					</div>
					<button class="login_btn" @click="get_captcha">登录</button>
					<p class="go_login" >没有账号 <router-link to="/register/">立即注册</router-link></p>
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
        login_type: 0, //登录页面标签切换的标识
        username:"",
        password:"",
        remember:false,
    }
  },

  methods:{
    loginHandler(){

      this.$axios.post(`${this.$settings.Host}/users/login/`,{
        username:this.username,
        password:this.password,
      })
      .then((res) =>{
        console.log(res.data);
        let data = res.data
        //是否勾选了记住我
        if (this.remember){
          sessionStorage.clear();
          localStorage.user_token = data.token;
          localStorage.id = data.id;
          localStorage.username = data.username;
          // 'credit':user.credit,
        // 'credit_to_money':contants.CREDIT_MONEY,
          localStorage.credit = data.credit;
          localStorage.credit_to_money = data.credit_to_money;
        }
        else{
          localStorage.clear();
          sessionStorage.user_token = data.token;
          sessionStorage.id = data.id;
          sessionStorage.username = data.username;
          sessionStorage.credit = data.credit;
          sessionStorage.credit_to_money = data.credit_to_money;
        }

        let self=this;
        this.$alert('xxx','ssss',{
          callback(){
            self.$router.push('/'); //编程式导航
          }
        })

      })
        .catch((res)=>{
          // console.log(res.response);
          this.$message.error('用户名或者密码有误，请重新输入！')
        })
    },

    handlerPopup(captchaObj){
       // 成功的回调,滑动成功之后触发的回调函数
        captchaObj.onSuccess(()=> {
            var validate = captchaObj.getValidate();
            console.log('>>>',validate)
            this.$axios.post(`${this.$settings.Host}/users/captcha/`,{
              geetest_challenge: validate.geetest_challenge,
              geetest_validate: validate.geetest_validate,
              geetest_seccode: validate.geetest_seccode
            })
          .then((data)=>{
              console.log(data);
              if (data.data.status === 'success'){
                this.loginHandler();
              }

          })

        });

        // 将验证码加到id为geetest1的元素里
        document.getElementById('geetest1').innerHTML = '';
        captchaObj.appendTo("#geetest1");


    },

    get_captcha(){
      if (!this.username){
        this.$message.error('请先填写用户名！')
        return false;
      }
      this.$axios.get(`${this.$settings.Host}/users/captcha/`,{
        params:{
          username:this.username,
        }
      })
      .then((data)=>{
            console.log(data);

            initGeetest({
                gt: data.data.gt,
                challenge: data.data.challenge,
                product: "popup",
                offline: !data.data.success
            }, this.handlerPopup);
      })
      .catch((error)=>{
        console.log(error.response);
        this.$message.error(error.response.data.msg);
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
