

import Vue from 'vue'

import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
  // 数据仓库,类似vue组件里面的data
  state: {
    cart:{
      cart_length:0,
    }
  },
  // 数据操作方法,类似vue里面的methods
  mutations: {
    add_cart(state,cart_len){
      state.cart.cart_length = cart_len;
    },

  }
});














