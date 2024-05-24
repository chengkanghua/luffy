<template>
  <div class="cart">
    <Header/>
    <div class="cart-info">
        <h3 class="cart-top">购物车结算 <span>共1门课程</span></h3>
        <div class="cart-title">
           <el-row>
             <el-col :span="2">&nbsp;</el-col>
             <el-col :span="10">课程</el-col>
             <el-col :span="8">有效期</el-col>
             <el-col :span="4">价格</el-col>
           </el-row>
        </div>
        <div class="cart-item" v-for="(course,index) in course_list">
          <el-row>
             <el-col :span="2" class="checkbox">&nbsp;&nbsp;</el-col>
             <el-col :span="10" class="course-info">
               <img :src="course.course_img" alt="">
                <span>{{course.name}}</span>
             </el-col>
             <el-col :span="8"><span>{{course.expire_text}}</span></el-col>
             <el-col :span="4" class="course-price">¥{{course.real_price}}</el-col>
           </el-row>
        </div>

        <div class="discount">
          <div id="accordion">
            <div class="coupon-box">
              <div class="icon-box">
                <span class="select-coupon">使用优惠劵：</span>
                <a class="select-icon unselect" :class="use_coupon?'is_selected':''" @click="use_coupon=!use_coupon"><img class="sign is_show_select" src="../../static/image/12.png" alt=""></a>
                <span class="coupon-num">有{{coupon_list.length}}张可用</span>
              </div>
              <p class="sum-price-wrap">商品总金额：<span class="sum-price">{{real_price}}元</span></p>
            </div>
            <div id="collapseOne" v-if="use_coupon">
              <ul class="coupon-list"  v-if="coupon_list.length>0">
                <li class="coupon-item" v-for="(item,index) in coupon_list" :class="select_coupon(index,item.id)" @click="click_coupon(index,item.id)" >
                  <p class="coupon-name">{{item.coupon.name}}</p>
                  <p class="coupon-condition">满{{item.coupon.condition}}元可以使用</p>
                  <p class="coupon-time start_time">开始时间：{{item.start_time.replace("T"," ")}}</p>
                  <p class="coupon-time end_time">过期时间：{{item.end_time.replace("T"," ")}}</p>
                </li>

              </ul>
              <div class="no-coupon" v-if="coupon_list.length<1">
                <span class="no-coupon-tips">暂无可用优惠券</span>
              </div>
            </div>
          </div>
          <div class="credit-box">
            <label class="my_el_check_box"><el-checkbox class="my_el_checkbox" v-model="use_credit"></el-checkbox></label>
            <p class="discount-num1" v-if="!use_credit">使用我的贝里</p>
            <p class="discount-num2" v-else><span>总积分：{{user_credit}}，已抵扣  <el-input-number @change="handleChange"  v-model="credit" :min="0" :max="max_credit()" label="请填写积分"></el-input-number>，本次花费以后，剩余{{parseInt(user_credit-credit)}}积分</span></p>
          </div>
         <!-- <p class="sun-coupon-num">优惠券抵扣：<span>0.00元</span></p> -->
        </div>

        <div class="calc">
            <el-row class="pay-row">
              <el-col :span="4" class="pay-col"><span class="pay-text">支付方式：</span></el-col>
              <el-col :span="8">
                <span class="alipay" v-if="pay_type===0"><img src="../../static/image/alipay2.png" alt=""></span>
                <span class="alipay" v-else><img src="../../static/image/alipay.png" alt="" @click="pay_type=0"></span>

                <span class="alipay wechat" v-if="pay_type===1"><img src="../../static/image/wechat2.png" alt=""></span>
                <span class="alipay wechat" v-else><img src="../../static/image/wechat.png" alt="" @click="pay_type=1"></span>
              </el-col>
              <el-col :span="8" class="count">实付款： <span>¥{{(real_price_show - this.credit/credit_to_money).toFixed(2)}}</span></el-col>
              <el-col :span="4" class="cart-pay"><span @click="payhander">支付宝支付</span></el-col>
            </el-row>
        </div>

    </div>
    <Footer/>
  </div>
</template>

<script>
  import Header from "./common/Header"
  import Footer from "./common/Footer"
  export default {
    name:"Order",
    data(){
      return {
        course_list: [],
        coupon_list:[],
        total_price: 0,
        real_price: 0,
        real_price_show: 0,
        pay_type:0,  //切换支付方式效果标识
        credit:0,    //使用了多少积分
        coupon:0,    //优惠券
        use_credit: false,  // 是否使用了积分
        use_coupon: false,  // 优惠券ID，0表示没有使用优惠券
        user_credit: localStorage.credit || sessionStorage.credit,
        credit_to_money: localStorage.credit_to_money || sessionStorage.credit_to_money,
      }
    },
    components:{
      Header,
      Footer,
    },
    created(){
      this.get_course_list();
      this.token = this.check_user_login();
      this.get_coupon();
    },
    methods: {
      handleChange(value){
        if (!value){
          this.credit = 0;
        }
      },

      max_credit(){
        let max_credit_to_money = this.user_credit / this.credit_to_money
        let user_max_credit = 0;
        if (max_credit_to_money > this.real_price_show){
          user_max_credit = parseInt(this.real_price_show*this.credit_to_money)
        }else {
          user_max_credit = parseInt(this.user_credit)
        }
        return user_max_credit
      },

      select_coupon(index,coupon_id){
        let current_coupon = this.coupon_list[index];
        if (this.real_price < current_coupon.coupon.condition){
          return "disable"
        }
        let start_timestamp = parseInt(new Date(current_coupon.start_time) / 1000)
        let end_timestamp = parseInt(new Date(current_coupon.end_time) / 1000)
        let now_timestamp = parseInt(new Date()/1000)
        if(now_timestamp < start_timestamp || now_timestamp > end_timestamp){
          return "disable"
        }
        if (coupon_id === this.coupon){
          return "active"
        }
      },

      click_coupon(index,coupon_id){
        let current_coupon = this.coupon_list[index];
        if (this.real_price < current_coupon.coupon.condition){
          return false
        }
        let start_timestamp = parseInt(new Date(current_coupon.start_time) / 1000)
        let end_timestamp = parseInt(new Date(current_coupon.end_time) / 1000)
        let now_timestamp = parseInt(new Date()/1000)
        if(now_timestamp < start_timestamp || now_timestamp > end_timestamp){
          return false
        }
        this.coupon = coupon_id
        this.cal_real_price();
      },

      check_user_login(){
        let token = sessionStorage.user_token || localStorage.user_token
        if(! token){
          this.$confirm('您还没有登录','路飞',{
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
          this.$router.push('/login/');
        })
          return false;
        }
        return token
      },

      get_course_list(){
        let token = this.check_user_login();
        this.$axios.get(`${this.$settings.Host}/cart/order/`,{
          headers:{
            "Authorization":"jwt " + token,
          }
        })
        .then((res)=>{
          this.course_list = res.data.select_course_list;
          this.total_price = res.data.total_price;
          this.real_price = res.data.real_total_price;
          this.real_price_show = res.data.real_total_price;

        })
        .catch((error)=>{
          this.$message.error(error.response);
        })
      },

      payhander(){
        let token = this.check_user_login();
        this.$axios.post(`${this.$settings.Host}/order/`,{
          pay_type:this.pay_type,
          credit:this.credit,
          coupon:this.coupon,
        },{
          headers:{
            "Authorization":"jwt " + token,
          }
        })
        .then((res)=>{
          this.$message.success('生成订单成功，准备跳转支付页面');
          // location.href="https://openapi.alipay.com/gateway.do? + order_string"
          // console.log(res.data.order_number);
          this.$axios.get(`${this.$settings.Host}/payments/alipay/`,{
            params:{
              order_number:res.data.order_number,
            }
          })
          .then((response) => {
            // console.log(response);
            location.href = response.data;

          })
          .catch((error)=>{
            console.log(error.response.data);
          })

        })
        .catch((error)=>{
          console.log(error.response.data)
          // this.$message.error(error.response.msg);
        })
      },

      get_coupon(){
        this.$axios.get(`${this.$settings.Host}/coupon/`,{
          headers:{
            "Authorization":"jwt " + this.token,
          }
        })
        .then((res)=>{
          this.coupon_list = res.data;
        })
        .catch((error)=>{
          this.$message.error(error.response);
        })
      },

      cal_real_price(){
        this.coupon_list.forEach((value,key)=>{
          if (value.id === this.coupon){
            let start_timestamp = parseInt(new Date(value.start_time) / 1000)
            let end_timestamp = parseInt(new Date(value.end_time) / 1000)
            let now_timestamp = parseInt(new Date()/1000)
            if (now_timestamp > start_timestamp && now_timestamp <= end_timestamp){
              //没有使用优惠券的真实价格
              // 优惠券的计算方式
              let cal_func = value.coupon.sale
              let d = parseFloat(cal_func.substr(1)); //取计算规则 乘 或者减的 对象
              if (cal_func[0] === "*"){
                this.real_price_show = this.real_price * d
              }
              else {
                this.real_price_show = this.real_price - d
              }
              // this.credit = (this.credit - this.real_price - this.real_price_show) * this.credit_to_money;
            }
          }
        })
      },




    }
  }
</script>

<style scoped>
.cart{
  /* margin-top: 80px; */
}
.cart-info{
  overflow: hidden;
  width: 1200px;
  margin: auto;
  margin-bottom: 150px;
}
.cart-top{
  font-size: 18px;
  color: #666;
  margin: 25px 0;
  font-weight: normal;
}
.cart-top span{
    font-size: 12px;
    color: #d0d0d0;
    display: inline-block;
}
.cart-title{
    background: #F7F7F7;
    height: 80px;
    line-height: 80px;
}
.calc{
  margin-top: 25px;
  margin-bottom: 40px;
}

.calc .count{
  text-align: right;
  margin-right: 10px;
  vertical-align: middle;
}
.calc .count span{
    font-size: 36px;
    color: #333;
}
.calc .cart-pay{
    margin-top: 5px;
    width: 110px;
    height: 38px;
    outline: none;
    border: none;
    color: #fff;
    line-height: 38px;
    background: #ffc210;
    border-radius: 4px;
    font-size: 16px;
    text-align: center;
    cursor: pointer;
}
.cart-item{
  height: 120px;
  line-height: 120px;
  margin-bottom: 30px;
}
.course-info img{
    width: 175px;
    height: 115px;
    margin-right: 35px;
    vertical-align: middle;
}
.alipay{
  display: inline-block;
  height: 48px;
}
.alipay img{
  height: 100%;
  width:auto;
}

.pay-text{
  display: block;
  text-align: right;
  height: 100%;
  line-height: 100%;
  vertical-align: middle;
  margin-top: 20px;
}

.coupon-box{
  text-align: left;
  padding-bottom: 22px;
  padding-left:30px;
  border-bottom: 1px solid #e8e8e8;
}
.coupon-box::after{
  content: "";
  display: block;
  clear: both;
}
.icon-box{
  float: left;
}
.icon-box .select-coupon{
  float: left;
  color: #666;
  font-size: 16px;
}
.icon-box::after{
  content:"";
  clear:both;
  display: block;
}
.select-icon{
  width: 20px;
  height: 20px;
  float: left;
}
.select-icon img{
  max-height:100%;
  max-width: 100%;
  margin-top: 2px;
  transform: rotate(-90deg);
  transition: transform .5s;
}
.is_show_select{
  transform: rotate(0deg)!important;
}
.coupon-num{
    height: 22px;
    line-height: 22px;
    padding: 0 5px;
    text-align: center;
    font-size: 12px;
    float: left;
    color: #fff;
    letter-spacing: .27px;
    background: #fa6240;
    border-radius: 2px;
    margin-left: 20px;
}
.sum-price-wrap{
    float: right;
    font-size: 16px;
    color: #4a4a4a;
    margin-right: 45px;
}
.sum-price-wrap .sum-price{
  font-size: 18px;
  color: #fa6240;
}

.no-coupon{
  text-align: center;
  width: 100%;
  padding: 50px 0px;
  align-items: center;
  justify-content: center; /* 文本两端对其 */
  border-bottom: 1px solid rgb(232, 232, 232);
}
.no-coupon-tips{
  font-size: 16px;
  color: #9b9b9b;
}
.credit-box{
  height: 40px;
  margin-top: 20px;
  display: flex;
  align-items: center;
  justify-content: flex-end
}
.my_el_check_box{
  position: relative;
}
.my_el_checkbox{
  margin-right: 10px;
  width: 16px;
  height: 16px;
}
.discount{
    overflow: hidden;
}
.discount-num1{
  color: #9b9b9b;
  font-size: 16px;
  margin-right: 45px;
}
.discount-num2{
  margin-right: 45px;
  font-size: 16px;
  color: #4a4a4a;
}
.sun-coupon-num{
  margin-right: 45px;
  margin-bottom:43px;
  margin-top: 40px;
  font-size: 16px;
  color: #4a4a4a;
  display: inline-block;
  float: right;
}
.sun-coupon-num span{
  font-size: 18px;
  color: #fa6240;
}
.coupon-list{
  margin: 20px 0;
}
.coupon-list::after{
  display: block;
  content:"";
  clear: both;
}
.coupon-item{
  float: left;
  margin: 15px 8px;
  width: 200px;
  height: 100px;
  padding: 5px;
  background-color: #fa3030;
  cursor: pointer;
}
.coupon-list .active{
  background-color: #fa9000;
}
.coupon-list .disable{
  cursor: not-allowed;
  background-color: #fa6060;
}
.coupon-condition{
  font-size: 12px;
  text-align: center;
  color: #fff;
}
.coupon-name{
  color: #fff;
  font-size: 24px;
  text-align: center;
}
.coupon-time{
  text-align: left;
  color: #fff;
  font-size: 12px;
}
.unselect{
  margin-left: 0px;
  transform: rotate(-90deg);
}
.is_selected{
  transform: rotate(-1turn)!important;
}
.coupon-item p{
    margin: 0;
    padding: 0;
  }

.el-icon-minus,.el-icon-plus{
 	font-size: 12px;
}

</style>
