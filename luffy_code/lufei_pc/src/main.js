// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import settings from "./settings"
import axios from 'axios'; // 从node_modules目录中导入包
import '../static/css/reset.css'
import store from './store/index';  //Vuex

import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';  // 需要import引入一下css文件，和我们的link标签引入是一个效果，而import .. from ..是配合export default来使用的
// 调用插件
Vue.use(ElementUI);

require('video.js/dist/video-js.css');
require('vue-video-player/src/custom-theme.css');
import VideoPlayer from 'vue-video-player'
Vue.use(VideoPlayer);


// 客户端配置是否允许ajax发送请求时附带cookie，false表示不允许
// axios.defaults.withCredentials = true;
Vue.prototype.$axios = axios; // 把对象挂载vue中
Vue.prototype.$settings = settings

Vue.config.productionTip = false


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
