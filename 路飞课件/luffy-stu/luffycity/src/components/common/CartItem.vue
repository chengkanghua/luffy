<template>
    <div class="cart_item">
      <div class="cart_column column_1">
        <el-checkbox class="my_el_checkbox" v-model="cart.is_selected"></el-checkbox>
      </div>
      <div class="cart_column column_2">

        <img :src="cart.course_img" alt="">
        <span><router-link :to="'/course/detail/'+cart.id +'/'">{{cart.name}}</router-link></span>
      </div>
      <div class="cart_column column_3">
        <el-select v-model="cart.expire_id" size="mini" placeholder="请选择购买有效期" class="my_el_select">
          <el-option :label="expire.expire_text" :value="expire.id" :key="expire.id" v-for="(expire,index) in cart.expire_list"></el-option>

          </el-select>
      </div>
      <div class="cart_column column_4">¥{{cart.real_price}}</div>
      <div class="cart_column column_4" style="cursor: pointer;" @click="delete_course">删除</div>
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
    props:["cart",],
    watch:{
      "cart.is_selected":function () {
        this.change_course_selected();
      },
      "cart.expire_id":function () {
        this.change_expire();
      }
    },
  methods:{

      delete_course(){
        let token = this.check_user_login();

        this.$axios.delete(`${this.$settings.Host}/cart/?course_id=${this.cart.id}`,{
          headers:{
            "Authorization":"jwt " + token,
          }
        })
        .then((res)=>{
          this.$message.success('删除课程成功！');

          this.$emit('del_course');
        })
        .catch((error)=>{
           this.$message.success(error.response.msg);
        })

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

      change_course_selected(){
        let token = this.check_user_login();

        this.$axios.patch(`${this.$settings.Host}/cart/`,{
          is_selected:this.cart.is_selected,
          course_id:this.cart.id,
        },{
          headers:{
            "Authorization":"jwt " + token,
          }
        })
        .then((res)=>{
          this.$message.success(res.data.msg);
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
        this.$message.success(res.data.msg);
        console.log(res.data);
        this.cart.real_price = res.data.real_price;

        this.$emit('change_expire_handler')
      })
      .catch((error)=>{
        this.$message.error(res.data.msg);
      })
    }


  }
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
