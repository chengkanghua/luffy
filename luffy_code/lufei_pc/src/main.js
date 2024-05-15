// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import settings from "./settings"
import axios from 'axios'; // 从node_modules目录中导入包


// 客户端配置是否允许ajax发送请求时附带cookie，false表示不允许
axios.defaults.withCredentials = false;
Vue.prototype.$axios = axios; // 把对象挂载vue中

Vue.prototype.$settings = settings

Vue.config.productionTip = false


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
