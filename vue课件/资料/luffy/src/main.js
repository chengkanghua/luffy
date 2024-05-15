// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

// @/assets/ -- @src的路径

import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

require('video.js/dist/video-js.css');
//或者 import 'video.js/dist/video-js.css'
require('vue-video-player/src/custom-theme.css');
//或者：import 'vue-video-player/src/custom-theme.css'
import VideoPlayer from 'vue-video-player'
Vue.use(VideoPlayer);



Vue.use(ElementUI);

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
