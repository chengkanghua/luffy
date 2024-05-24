// 1.构造选项卡的函数
function TabSwitch(fatherObj) {
	// 保存this
	var _this = this;
	// 2.绑定实例属性
	this.tabLis = fatherObj.children[0].getElementsByTagName('li');
	this.contentDivs = fatherObj.getElementsByTagName('div');
	for (var i = 0; i < this.tabLis.length; i++) {
		// 绑定i的索引
		this.tabLis[i].index = i;
		this.tabLis[i].onclick = function() {
			// this
			_this.clickFun(this.index);
		}
	}
}
// 3.绑定共享的方法
TabSwitch.prototype.clickFun = function(index) {
	// console.log(this);
	for (var j = 0; j < this.tabLis.length; j++) {
		this.tabLis[j].className = '';
		this.contentDivs[j].style.display = 'none';
	}
	// this
	this.tabLis[index].className = 'active';
	this.contentDivs[index].style.display = 'block';
}

