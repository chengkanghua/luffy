// 业务逻辑
// 1.字面量方式
/* var module1 = new Object({
	count: 0,
	m1:function() {
		// ....
	},
	m2:function() {
		//....
	}
})
 */
// IIFE 立即执行函数
 var module1 = (function() {
	// count是一个私有的变量
	var count = 0;
	var m1 = function() {
		console.log('m1');
		//....
	};
	var m2 = function() {
		console.log('m2');
		//....
	}
	return {
		m1: m1,
		m2: m2
	}
})(); 
// 放大模式
// 宽放大模式
(function(mod){
	mod.m3 = function(){
		console.log('m3');
	}
	return mod;
})(window.module1 || {});

