import Vue from 'vue'
import Router from 'vue-router'


Vue.use(Router)

import Home from "../components/Home"
import Course from "../components/Course"
import Cart from "../components/Cart"
import Detail from "../components/Detail"

export default new Router({
  mode:'history',
  routes: [
    {
      path: "/",
      name:"Home",
      component: Home,
    },{
      path: "/home",
      name:"Home",
      component: Home,
    },
    {
      path:"/course",
      name: "Course",
      component:Course,
    },
    {
      path:"/cart",
      name:"Cart",
      component:Cart,
    },
    {
      path:"/detail",
      name:"Detail",
      component:Detail,
    }
  ]
})
