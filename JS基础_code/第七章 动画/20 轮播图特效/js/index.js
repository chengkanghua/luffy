window.onload = function() {
	// 1.获取标签
	var slider = document.getElementById('slider');
	var slider_main = document.getElementById('slider_main');
	var allBoxs = slider_main.children;
	var next = document.getElementById('next');
	var prev = document.getElementById('prev');
	var slider_index = document.getElementById('slider_index');
	var iNow = 0; //当前可视元素的索引
	var timer = null;
	// 2.动态创建索引器
	for (var i = 0; i < allBoxs.length; i++) {
		var span = document.createElement('span');
		if (i === 0) {
			span.className = 'slider_index_icon current';
		} else {
			span.className = 'slider_index_icon'
		}
		span.innerText = i + 1;
		slider_index.appendChild(span);
	}
	// 3.让滚动的元素归位
	var scroll_w = parseInt(getStyle(slider, 'width'));
	for (var j = 1; j < allBoxs.length; j++) {
		allBoxs[j].style.left = scroll_w + 'px';
	}
	// 4.监听下一张按钮的事件
	next.onclick = function() {
		/**
		 * 1.让当前可视元素动画左移
		 * 2.让下一张图片 快速的显示到右边
		 * 3.让这个元素动画进入
		 */
		
	}
	
	// 5.监听上一个按钮的事件
	prev.onclick = function (){
		/**
		 * 1.当前元素快速的右移
		 * 2.让上一个元素快速的到左边
		 * 3.让这个元素动画进入
		 */
		startAnimation(allBoxs[iNow],{
			"left":scroll_w
		})
		iNow--;
		if(iNow < 0){
			iNow = allBoxs.length - 1;
		}
		allBoxs[iNow].style.left = - scroll_w + 'px';
		startAnimation(allBoxs[iNow],{
			"left":0
		})
		// 改变索引器
		changeIndex();
		
	}
	
	// 6.开启定时器 自动播放
	timer = setInterval(autoPlay,2000);
	
	 
	
	
	var slider_index_icons = slider_index.children;
	// 6.遍历索引器，添加监听的事件
	for(var i = 0; i < slider_index_icons.length; i++){
		slider_index_icons[i].onmousedown = function (){
			// 6.1 获取当前点击索引
			var index = parseInt(this.innerText) - 1;
			
			// 点击的索引与当前的iNow进行对比
			if(index > iNow){
				// 下一个操作
				startAnimation(allBoxs[iNow],{
					'left':-scroll_w
				})
				allBoxs[index].style.left = scroll_w + 'px';			
			}else if(index < iNow){
				startAnimation(allBoxs[iNow],{
					'left':scroll_w
				})
				allBoxs[index].style.left = -scroll_w + 'px';		
			}
			// 更新索引
			iNow = index;
			startAnimation(allBoxs[iNow],{
				"left": 0
			})
			// 改变索引器
			changeIndex();
		}
	}
	// 控制当前的索引
	function changeIndex() {
		for (var i = 0; i < slider_index_icons.length; i++) {
			slider_index_icons[i].className = 'slider_index_icon';
		}
		slider_index_icons[iNow].className = 'slider_index_icon current';
	}


}
