var a = 1;
var b = 2;
function fn(x) {
	var a = 10;
	function bar(x) {
		var a = 100;
		b = x + a;
		return b;
	}
	bar(20);
	bar(200);
}
fn(0);

// 执行环境 相当于作用域链一样

// 总结：在js中，除了全局作用域，每个函数都会创建自己的作用域。
// 作用域在函数定义的时候已经确定了，与函数调用无关。
// 通过作用域，可以查找作用域范围内的变量和函数有哪些，却不知道变量的值是什么。所以作用域是静态


// 对于函数来说，执行环境在函数调用时确定的。执行环境包含作用域内的所有的变量和函数的值。在同一个作用域下，不同的调用会产生不同的执行环境，从而产生不同的变量和值。所以执行环境是动态
