<template>
    <div class="cart">
      <Header></Header>
      <div class="cart_info">
        <div class="cart_title">
          <span class="text">我的购物车</span>
          <span class="total">共{{$store.state.cart.cart_length}}门课程</span>
        </div>
        <div class="cart_table">
          <div class="cart_head_row">
            <span class="doing_row"></span>
            <span class="course_row">课程</span>
            <span class="expire_row">有效期</span>
            <span class="price_row">单价</span>
            <span class="do_more">操作</span>
          </div>
          <div class="cart_course_list">
            <!-- :cart="value" 父组件往子组件传数据   -->
            <CartItem v-for="(value,index) in cart_list" :key="value.id" :cart="value" @change_expire_handler="calc_total" @delete_course="del_cart(index)" ></CartItem>

          </div>
          <div class="cart_footer_row">
            <span class="cart_select"><label> <el-checkbox v-model="checked"></el-checkbox><span>全选</span></label></span>
            <span class="cart_delete"><i class="el-icon-delete"></i> <span>删除</span></span>
            <span class="goto_pay">去结算</span>
            <span class="cart_total">总计：¥{{total_price.toFixed(2)}}</span>
          </div>
        </div>
      </div>
      <Footer></Footer>
    </div>
</template>

<script>
import Header from "./common/Header"
import Footer from "./common/Footer"
import CartItem from "./common/CartItem"
export default {
    name: "Cart",
    data(){
      return {
        checked: false,
        cart_list:[],
        total_price:0,
      }
    },
    watch: {
      "checked": function(status){
        this.all_selected(status)
      },
    },
    methods:{
        calc_total(){
          // 计算购物车勾选商品的总价格
            /**
               // 在javascript中，数组有一个默认的方法，forEach可以用于对数组进行便利
               arr1 = ["a","b","c","d"]
               arr1.forEach(function(value,key){
                    console.log(`下标：${key}，值=${value}`);
               });
             */
          let total = 0;
          this.cart_list.forEach((course,key)=>{
            if(course.selected){
              total += parseFloat(course.real_price);
            }
          });
          this.total_price = total;
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

      get_cart_data(){
        let token = this.check_user_login();
        this.$axios.get(`${this.$settings.Host}/cart/`,{
          headers:{
              "Authorization":"jwt " + token,
          },
        })
        .then((res)=>{
          this.cart_list = res.data;
          console.log(res.data);
          // 统计勾选商品课程的真实价格
          this.calc_total();
          this.$store.commit("add_cart", this.course_list.length);

        })
        .catch((error)=>{
          // console.log(error.response);
        })
      },

      all_selected(status){
        console.log(status); // true false
        let token = this.check_user_login();
        this.$axios.put(`${this.$settings.Host}/cart/update/`,{
            status:status
        },{
          headers:{
              "Authorization":"jwt " + token,
          },
        })
        .then((res)=>{
          // this.cart_list = res.data;
          console.log(res.data);
          this.get_cart_data(); //更新选中框
        })
        .catch((error)=>{
          // console.log(error.response);
        })

      },

      del_cart(key){
        // 从购物车中删除指定商品
        this.cart_list.splice(key,1);
        // 删除商品课程以后，还要重新计算新的总价
        this.calc_total();
      },

    },
    created(){
      this.get_cart_data();
    },
    components:{
      Header,
      Footer,
      CartItem,
    }
}
</script>

<style scoped>
.cart_info{
  width: 1200px;
  margin: 0 auto 50px;
  margin-bottom: 150px;
}
.cart_title{
  margin: 25px 0;
}
.cart_title .text{
  font-size: 18px;
  color: #666;
}
.cart_title .total{
  font-size: 12px;
  color: #d0d0d0;
}
.cart_table{
  width: 1170px;
}
.cart_table .cart_head_row{
  background: #F7F7F7;
  width: 100%;
  height: 80px;
  line-height: 80px;
  padding-right: 30px;
}
.cart_table .cart_head_row::after{
  content: "";
  display: block;
  clear: both;
}
.cart_table .cart_head_row .doing_row,
.cart_table .cart_head_row .course_row,
.cart_table .cart_head_row .expire_row,
.cart_table .cart_head_row .price_row,
.cart_table .cart_head_row .do_more{
  padding-left: 10px;
  height: 80px;
  float: left;
}
.cart_table .cart_head_row .doing_row{
  width: 78px;
}
.cart_table .cart_head_row .course_row{
  width: 530px;
}
.cart_table .cart_head_row .expire_row{
  width: 188px;
}
.cart_table .cart_head_row .price_row{
  width: 162px;
}
.cart_table .cart_head_row .do_more{
  width: 162px;
}

.cart_footer_row{
  padding-left: 36px;
  background: #F7F7F7;
  width: 100%;
  height: 80px;
  line-height: 80px;
}
.cart_footer_row .cart_select span{
  margin-left: 14px;
  font-size: 18px;
  color: #666;
}
.cart_footer_row .cart_delete{
  margin-left: 58px;
}
.cart_delete .el-icon-delete{
  font-size: 18px;
}

.cart_delete span{
  margin-left: 15px;
  cursor: pointer;
  font-size: 18px;
  color: #666;
}
.cart_total{
  float: right;
  margin-right: 62px;
  font-size: 18px;
  color: #666;
}
.goto_pay{
  float: right;
  width: 159px;
  height: 80px;
  outline: none;
  border: none;
  background: #ffc210;
  font-size: 18px;
  color: #fff;
  text-align: center;
  cursor: pointer;
}
</style>

