<template>
  <div class="cart">
    <Header></Header>
    <div class="main">
      <div class="shopping-cart-wrap">
        <h3 class="shopping-cart-tit">
          我的购物车
          <small>
            共
            <span>2</span>
            门课程
          </small>
        </h3>
        <div class="content">
          <el-table
            ref="multipleTable"
            :data="tableData"
            tooltip-effect="dark"
            style="width: 100%"
            @selection-change="handleSelectionChange">
            <el-table-column
              type="selection"
              width="80">
            </el-table-column>
            <el-table-column
              prop="title"
              label="课程"
              width="540">
              <template slot-scope="scope">
                <img :src="scope.row.img_src" alt="">
                <router-link :to="scope.row.addr">{{scope.row.desc}}</router-link>
              </template>
            </el-table-column>
            <el-table-column
              label="有效期"
              width="216">
              <!-- 关于有效期的下拉菜单，我们使用element-ui中的表单里面的一个下拉菜单 -->
              <template slot-scope="scope">
                <div class="c1">
                  <el-form ref="form" :model="scope.row.expire_list">
                    <el-form-item>
                      <el-select v-model="expire" placeholder="请选择活动区域">
                        <el-option v-for="item in expire_list" :label="item.title" :value="item.id" :key="item.id"></el-option>

                      </el-select>
                    </el-form-item>
                  </el-form>
                </div>
              </template>

            </el-table-column>
            <el-table-column
              label="价格"
              width="162">
              <template slot-scope="scope">
                ￥{{scope.row.price}}
              </template>
            </el-table-column>
            <el-table-column
              label="操作"
              width="162"
              show-overflow-tooltip>
              <template slot-scope="scope">
                <router-link to="/cart" class="do-btn">删除</router-link>
              </template>
            </el-table-column>

          </el-table>
        </div>
        <ul class="pas-left">
          <li class="charge-list">
            <input type="checkbox" class="select_all" id="color-input-red" width="20px" height="20px">
            <span class="shopping-cart-bot-font" style="margin-left: 15px; cursor: pointer">全选</span>
          </li>
          <li class="charge-list" style="margin-left: 58px;">
            <img alt="" width="18" height="auto" src="@/assets/delete.png">
            <span class="shopping-cart-bot-font" style="margin-left: 15px; cursor: pointer; border: 0;" >删除</span>
          </li>
          <li class="charge-list" style="margin-left: auto">
            <span class="shopping-cart-bot-font" style="margin-right: 62px">总计: <b>0.0</b>￥</span>
            <button class="go-charge-btn">去结算</button>
          </li>

        </ul>
      </div>
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
  import Header from "./common/Header";
  import Footer from "./common/Footer";

  export default {
    name: "Cart",
    data() {
      return {
        expire:'1个月有效',
        token: true,
        expire_list: [
          {id: 1, title: '1个月有效'},
          {id: 2, title: '3个月有效'},
          {id: 3, title: '6个月有效'},
        ],
        tableData: [
          {
            title: '2016-05-02',
            expire: '三个月过期',
            img_src: '../../static/shopcarshow.jpeg',
            addr: '/cart',
            desc: '傻逼alex',
            price: '1',
          },
          {
            title: '2016-05-02',
            expire: '三个月过期',
            img_src: '../../static/shopcarshow.jpeg',
            addr: '/cart',
            desc: '傻逼alex',
            price: '2',
          },
        ]
      }
    },
    components: {
      Header,
      Footer,
    },
    methods: {
      handleSelectionChange(val) {
        this.multipleSelection = val;
      }
    }
  }
</script>

<style scoped>

  .main {
    width: 100%;
    /*flex: 1;*/
    /*flex-grow: 1;*/
    /*flex-direction: column;*/
  }

  .shopping-cart-wrap {
    width: 1200px;
    margin: 0 auto;
  }

  .shopping-cart-tit {
    font-size: 18px;
    color: #666;
    margin: 25px 0;
    font-family: PingFangSC-Regular;
  }

  .shopping-cart-tit small {
    font-size: 12px;
    color: #d0d0d0;
    display: inline-block;
    font-family: PingFangSC-Regular;
  }

  .content {
    width: 100%;
  }


  .content img {
    width: 175px;
    height: auto;
    margin-right: 35px;
  }

  .do-btn {
    border: none;
    outline: none;
    background: none;
    font-size: 14px;
    color: #ffc210;
    margin-right: 15px;
    font-family: PingFangSC-Regular;
  }
  .c1 /deep/ .el-form-item__content{
    /*注意：element-ui中的标签都是自动生成的，这些标签其实并不是我们自己在文档中写的，所以我们直接使用它翻译出来的标签的class类值来找对应的标签进行修改是找不到，所以如果希望scoped 样式中的选择器“深入”，也就是修改当前组件的element-ui插件的样式，即影响子组件，则可以使用 >>> 组合器，但是需要我们确保使用的element-ui标签外层有一个我们自己写的父级标签，举个例子：比如我写的父级标签的class类值为a，里面的element-ui的标签类值为el-form-item，我想修改el-form-item的样式，那么就要这么写选择器：.a >>> .el-form-item{color:'red';},这就可以了，但是官方文档中的方法说某些预处理器（如Sass）可能无法对>>>符号正确解析。在这些情况下，你可以使用 /deep/ 组合器 和 >>>符号完全相同。例如.a /deep/ .el-form-item{color:'red';}，当然，我们还可以直接在APP这个全局组件中直接进行样式修改，但是如果进行全局样式修改会污染其他组件中使用了这个插件的样式，所以不建议在全局修改样式*/
    margin-top: 20px;
    width: 120px;
  }

  .shopping-cart-wrap .pas-left{
    width: 100%;
    height: 80px;
    background: #F7F7F7;
    margin-bottom: 100px;
    margin-top: 50px;
    display: flex;
    align-items: center;
    padding-left: 25px!important;
  }
  .charge-list{
    display: flex;
    align-items: center;
    list-style: none;
  }
  .charge-list .shopping-cart-bot-font{
    font-size: 18px;
    color: #666;
    font-family: PingFangSC-Regular;
  }
  .charge-list .go-charge-btn{
    width: 159px;
    height: 80px;
    outline: none;
    border: none;
    background: #ffc210;
    font-size: 18px;
    color: #fff;
    font-family: PingFangSC-Regular;
  }

</style>
