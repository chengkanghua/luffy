// 个人信息类
// 姓名 性别
var namespace = (function(namespace){
	// 声明了一个顶层的命名空间
	// 个人信息类：构造函数构建对象
	namespace.PersonInfo = function(obj){
		obj = obj || {};
		this.name =  obj.name || '';
		this.gender = obj.gender || "?";
	}
	// 称谓方法
	namespace.PersonInfo.prototype.getAppellation = function(){
		var str = "";
		if(this.gender === '男'){
			str = '男士';
		}else{
			str = '女士';
		}
		return str;	
	}
	// 欢迎的方法
	namespace.PersonInfo.prototype.getHello = function(){
		var s = "Hello " + this.name + this.getAppellation();
		return s;
	}
	// 个人信息工具类
	namespace.personInfoUtil = function(){
		return {
			// p形参是代指是哪个对象
			show:function(p){
				alert('姓名：'+ p.name+ "，性别："+ p.gender);
			}
		}
	}()
	return namespace;
})(window.namespace || {});