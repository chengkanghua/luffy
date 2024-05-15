import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

import Home from "../components/Home";
import Course from "../components/Course";
import Detail from "../components/Detail";
import Cart from "../components/Cart";

export default new Router({
  mode:'history',
  routes: [
    {
      path: '/home/',
      // name: 'HelloWorld',  路由别名  url('',name='')
      component: Home,
    },
    {
      path: '/',
      // name: 'HelloWorld',  路由别名  url('',name='')
      component: Home,
    },
    {
      path: '/course/',
      // name: 'HelloWorld',  路由别名  url('',name='')
      component: Course,
    },
    {
      path: '/detail/',
      // name: 'HelloWorld',  路由别名  url('',name='')
      component: Detail,
    },
    {
      path: '/cart/',
      // name: 'HelloWorld',  路由别名  url('',name='')
      component: Cart,
    },

  ]
})
