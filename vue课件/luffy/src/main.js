// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

// elementUi 导入
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
Vue.use(ElementUI); //调用插件

// Vue-video
import 'video.js/dist/video-js.css'
import 'vue-video-player/src/custom-theme.css'
import VideoPlayer from 'vue-video-player'
Vue.use(VideoPlayer);


Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
