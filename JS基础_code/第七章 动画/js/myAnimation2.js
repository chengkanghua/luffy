var speed = 0;
/**
 * 动画的函数
 * @param {Object} obj 当前的对象
 * @param {Object} attr 当前元素对象的属性
 * @param {Object} endTarget 末尾位置
 */
function startAnimation(obj, json, fn) {
	// 针对于多物体运动,定时器的返回值要绑定当前的对象中.
	clearInterval(obj.timer);
	obj.timer = setInterval(function() {
		var cur = 0;
		var flag = true; //标杆 如果true，证明所有的属性都到达终点值
		for (var attr in json) {
			// 0 获取样式属性
			// 透明度变化处理
			switch (attr) {
				case 'opacity':
					cur = Math.round(parseFloat(getStyle(obj, attr)) * 100);
					break;
				case 'scrollTop':
					cur = obj[attr]
					break;
				default:
					cur = parseInt(getStyle(obj, attr));
					break;
			}
			// 1.求速度
			speed = (json[attr] - cur) / 10;
			speed = json[attr] > cur ? Math.ceil(speed) : Math.floor(speed);
			// 2.临界处理
			if (json[attr] !== cur) {
				flag = false;
			}
			// 3.运动起来
			switch (attr) {
				case 'opacity':
					obj.style[attr] = `alpha(opacity: ${cur + speed})`;
					obj.style[attr] = (cur + speed) / 100;
					break;
				case 'scrollTop':
					obj.scrollTop = cur + speed;
				default:
					obj.style[attr] = cur + speed + 'px';
					break;
			}
		}

		if (flag) {
			clearInterval(obj.timer);
			if (fn) {
				fn();
			}
			return;
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
