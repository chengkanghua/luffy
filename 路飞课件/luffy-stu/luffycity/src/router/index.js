import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

import Home from "../components/Home";
import Course from "../components/Course";
import Detail from "../components/Detail";
import Cart from "../components/Cart";
import Login from "../components/Login";
import Register from "../components/Register";
import Order from "../components/Order";
import Success from "../components/Success";
import UserOrder from "../components/UserOrder";
import Player from "../components/Player";

export default new Router({
  mode:'history',
  routes: [
    {
      path: '/home/',
      // name: 'HelloWorld',  路由别名  url('',name='')
      component: Home,
    },
    {
      path: '/login/',
      // name: 'HelloWorld',  路由别名  url('',name='')
      component: Login,
    },
    {
      path: '/register/',
      // name: 'HelloWorld',  路由别名  url('',name='')
      component: Register,
    },
    {
      path: '/',
      // name: 'HelloWorld',  路由别名  url('',name='')
      component: Home,
    },
    {
      path: '/course',
      // name: 'HelloWorld',  路由别名  url('',name='')
      component: Course,
    },
    {
      path: '/course/detail/:id/',   // /detail/1/  /detail/2/
      // name: 'HelloWorld',  路由别名  url('',name='')
      component: Detail,
    },
    {
      path: '/cart/',
      // name: 'HelloWorld',  路由别名  url('',name='')
      component: Cart,
    },
    {
      path: '/order/',
      // name: 'HelloWorld',  路由别名  url('',name='')
      component: Order,
    },
    // /payments/result
    {
      path: '/payments/result',
      // name: 'HelloWorld',  路由别名  url('',name='')
      component: Success,
    },
    ///my/order/
    {
      path: '/my/order/',
      // name: 'HelloWorld',  路由别名  url('',name='')
      component: UserOrder,
    },
    {
      path: '/course/player/:vid',
      name: "Player",
      component: Player,
    },
  ]
})
