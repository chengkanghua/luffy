<template>
    <div class="cart_item">
      <div class="cart_column column_1">
        <el-checkbox class="my_el_checkbox" v-model="cart.selected"></el-checkbox>
      </div>
      <div class="cart_column column_2">
        <img :src="cart.course_img" alt="">
        <span><router-link :to="`/course/detail/${cart.id}/`">{{cart.name}}</router-link></span>
      </div>
      <div class="cart_column column_3">
        <el-select v-model="cart.expire_id" size="mini" placeholder="请选择购买有效期" class="my_el_select">
          <el-option :label="expire.expire_text" :value="expire.id" :key="expire.id" v-for="(expire,index) in cart.expire_list"></el-option>
          <!-- <el-option label="1个月有效" value="30" key="30"></el-option>
          <el-option label="2个月有效" value="60" key="60"></el-option>
          <el-option label="3个月有效" value="90" key="90"></el-option>
          <el-option label="永久有效" value="0" key="0"></el-option> -->
        </el-select>
      </div>
      <div class="cart_column column_4">¥{{cart.real_price}}</div>
      <div class="cart_column column_4" @click="delete_course">删除</div>
    </div>
</template>

<script>
export default {
    name: "CartItem",
    data(){
      return {
        checked:false,
        expire: "1个月有效",
      }
    },
    props:["cart",],  //接受父组件传过来的数据
    watch:{
      "cart.selected":function () {
        this.change_course_selected();
      },
      "cart.expire_id":function () {
        this.change_expire();
      }
    },
    methods: {
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

      change_course_selected() {
        let token = this.check_user_login();
        this.$axios.patch(`${this.$settings.Host}/cart/`,{
          selected:this.cart.selected,
          course_id:this.cart.id,  //调用父组件传过来的cart 前面加个this
        },{
          headers:{
            "Authorization":"jwt " + token,
          }
        })
        .then((res)=>{
          console.log(res.data.message)
          // this.$message.success(res.data.message);
          this.$emit('change_expire_handler');
        })
        .catch((error)=>{
          this.$message.error(error.response);
        })
      },
      change_expire(){
          let token = this.check_user_login();
          this.$axios.put(`${this.$settings.Host}/cart/`,{
            expire_id:this.cart.expire_id,
            course_id:this.cart.id,
          },{
            headers:{
              "Authorization":"jwt " + token,
            }
          })
        .then((res)=>{
          this.$message.success(res.data.message);
          // console.log(res.data);
          this.cart.real_price = res.data.real_price;

          //调用父组件的 cal_price 方法
          this.$emit('change_expire_handler')
        })
        .catch((error)=>{
          this.$message.error(res.data.message);
        })
      },

      delete_course(){
          let token = localStorage.user_token || sessionStorage.user_token;
          this.$axios.delete(`${this.$settings.Host}/cart/`,{
              params:{
                  course_id: this.cart.id
              },
              headers:{
                  "Authorization": "jwt " + token,
              }
          }).then(response=>{
              this.$message.success(response.data.message);
              // 当子组件中，切换了商品课程的勾选状态，则通知父组件重新计算购物商品总价
              this.$emit("delete_course");

          }).catch(error=>{
              this.$message.error(error.response);
          });
      },


    },


}
</script>

<style scoped>
  /*.cart_item{*/
  /*  height: 100px;*/
  /*}*/
.cart_item::after{
  content: "";
  display: block;
  clear: both;
}
.cart_column{
  float: left;
  height: 150px;
  display: flex;
  align-items: center;
}
.cart_item .column_1{
  width: 88px;
  position: relative;
}
.my_el_checkbox{
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  top: 0;
  margin: auto;
  width: 16px;
  height: 16px;
}
.cart_item .column_2 {
  /*padding: 67px 10px;*/
  width: 520px;
  /*height: 116px;*/
}
.cart_item .column_2 img{
  width: 175px;
  /*height: 115px;*/
  margin-right: 35px;
  /*vertical-align: middle;*/
}
.cart_item .column_3{
  width: 197px;
  position: relative;
  padding-left: 10px;
}
.my_el_select{
  width: 117px;
  height: 28px;
  position: absolute;
  top: 0;
  bottom: 0;
  margin: auto;
}
.cart_item .column_4{
  /*padding: 67px 10px;*/
  /*height: 116px;*/
  width: 142px;
  /*line-height: 116px;*/
}

</style>
