// 动物园

namespace.sub = (function(sub){
	// 定义一个子的命名空间
	// 动物类
	sub.Animal = function(name,color){
		this.name = name;
		this.color = color;
	}
	sub.Animal.prototype.sleep = function(){
		console.log('睡懒觉');
	}
	// 猫类
	sub.Cat = function(name,color){
		// 继承属性
		sub.Animal.call(this,name,color);
	}
	// 继承方法
	sub.Cat.prototype = Object.create(sub.Animal.prototype);
	sub.Cat.prototype.constructor = sub.Animal;
	return sub;
})(window.namespace.sub || {});