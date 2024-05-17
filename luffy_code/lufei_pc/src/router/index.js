import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

import Home from "../components/Home";
import Login from "../components/Login"
import Register from "../components/Register"


export default new Router({
  mode:"history",
  routes: [
    {
      path: '/',
      // name: 'HelloWorld',
      component: Home
    },
    {
      path: '/home/',
      // name: 'HelloWorld',  路由别名  url('',name='')
      component: Home,
    },
   {
      name:"Login",
      path: "/user/login",
      component:Login,
    },
    {
      name:"Register",
      path:"/register",
      component:Register,
    }
  ],

})
