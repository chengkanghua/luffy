var speed = 0;
/**
 * 动画的函数
 * @param {Object} obj 当前的对象
 * @param {Object} attr 当前元素对象的属性
 * @param {Object} endTarget 末尾位置
 */
function startAnimation(obj, attr, endTarget,fn) {
	// 针对于多物体运动,定时器的返回值要绑定当前的对象中.
	clearInterval(obj.timer);
	obj.timer = setInterval(function() {
		var cur = 0;
		// 0 获取样式属性
		// 透明度变化处理
		if (attr === 'opacity') {
			cur = Math.round(parseFloat(getStyle(obj, attr)) * 100);
		} else {

			cur = parseInt(getStyle(obj, attr));
		}

		// 1.求速度
		speed = (endTarget - cur) / 20;
		speed = endTarget > cur ? Math.ceil(speed) : Math.floor(speed);

		// 2.临界处理
		if (endTarget === cur) {
			clearInterval(obj.timer);
			if(fn){
				fn();
			}
			return;
		}
		// 3.运动起来
		if (attr === 'opacity') {
			obj.style[attr] = `alpha(opacity: ${cur + speed})`;
			obj.style[attr] = (cur + speed) / 100;

		} else {
			obj.style[attr] = cur + speed + 'px';
		}

	}, 30);
}
/**
 * 获取元素属性的函数
 * @param {Object} obj 当前元素对象
 * @param {Object} attr 当前元素对象的属性
 */
function getStyle(obj, attr) {
	if (obj.currentStyle) {
		// 兼容ie
		return obj.currentStyle[attr];
	} else {
		// 兼容主流浏览器
		return getComputedStyle(obj, null)[attr];
	}
}
