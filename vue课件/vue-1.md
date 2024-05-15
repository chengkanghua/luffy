[TOC]

吴超  大型金融业务系统  金融量化分析  爬虫  指数基金走势分析等等。。。

前后端分离的项目，路飞学城  vue  + drf(djangorestframework后端接口)  开发项目

crm项目， 非前后端分离    index.html  {{ msg }}  --  views.py def index(request):render(request,'index.html',{'msg':'xxoo'})    /index/     

Vue 前端框架   MVVM -- model -- view -- viewmodel      ---  template模板渲染

model--数据

view -- 视图   -- html标签   类似于jquery  $('#d1').text('xxx')



viewmodel：数据驱动视图 vue的核心，model数据直接驱动到视图中(html标签中)

django  -- MTV模式   model  template  view + url控制器    template这一块功能就去掉了

view--视图：  后端逻辑  FBV和CBV



前端  ECMAScript5 -- es5

vue多数用的都是es6语法



# 前戏

## es6的基本语法

```js
let a   ：特点：  1.a是局部作用域的function xx(){let a = 'xxoo';}  if(){let a = 'ss';} 
				2.不存在变量提升  3.不能重复声明（var可以重复声明），  

// var a;  -- undefined

console.log(a); -- undefined
var a = 10;

var b = '景顺';

console.log(c);  -- 报错

let c = '谢景顺'；
const ：特点：  1.局部作用域  2.不存在变量提升  3.不能重复声明  4.一般声明不可变的量
const pi = 3.1415926;
//pi = 'xx' -- 报错

模板字符串：tab键上面的反引号，${变量名}来插入值  类似于python的三引号 """adfadsf"""，可以写多行文本
另外还可以通过它来完成字符串格式化
示例：
	let bb = 'jj';
	var ss = `你好${bb}`;
  console.log(ss); -- '你好jj'
```

## es5和es6的函数对比

```js
    //ES5写法
    function add(x){
        return x
    }
    add(5);
    //匿名函数
    var add = function (x) {
        return x
    };
		add(5);
    //ES6的匿名函数
    let add = function (x) {
        return x
    };
    add(5);
    //ES6的箭头函数,就是上面方法的简写形式
    let add = (x) => {
        return x
    };
    console.log(add(20));
    //更简单的写法，但不是很易阅读
    let add = x => x;
    console.log(add(5));
    多个参数的时候必须加括号，函数返回值还是只能有一个，没有参数的，必须写一个()
    let add = (x,y) => x+y;
```



## 自定义对象中封装函数的写法



```js
   //es5对象中封装函数的方法
    var name = '子俊';
    var person1 = {
        name:'超',
        age:18,
        f1:function () {  //在自定义的对象中放函数的方法
            console.log(this);//this指向的是当前的对象,{name: "超", age: 18, f1: ƒ}
            console.log(this.name)  // '超'
        }
    };
    //<h1 id='d1'>xxx</h1>
    //document.getElementById('d1').onclick = function(){this.innerText;};
    person1.f1();  //通过自定对象来使用函数

    //ES6中自定义对象中来封装箭头函数的写法
    let name = '子俊'; // window.name
    let person2 = {
        name:'超',
        age:18,
        //f1:function(){};
        f1: () => {  //在自定义的对象中放函数的方法
            console.log(this); //this指向的不再是当前的对象了，而是指向了person的父级对象(称为上下文)，而此时的父级对象是我们的window对象，Window {postMessage: ƒ, blur: ƒ, focus: ƒ, close: ƒ, frames: Window, …}
            console.log(window);//还记得window对象吗，全局浏览器对象，打印结果和上面一样：Window {postMessage: ƒ, blur: ƒ, focus: ƒ, close: ƒ, frames: Window, …}
            console.log(this.name)  //子俊
            console.log(window.name); // 子俊
        }
    };
    person2.f1(); //通过自定对象来使用函数
    //person2 -- window.person2

    //而我们使用this的时候，希望this是person对象，而不是window对象，所以还有下面这种写法
    let person3 = {
        name:'超',
        age:18,
        //f1:function(){};
        //f1(){}
        f1(){  //相当于f1:function(){},只是一种简写方式,称为对象的单体模式写法，写起来也简单，vue里面会看用到这种方法
            console.log(this);//this指向的是当前的对象,{name: "超", age: 18, f1: ƒ}
            console.log(this.name)  //'超'
        }
    };
    person3.f1()


```



## es5和es6的类写法对比（了解）

```js
<script>
    //es5写类的方式
    
    function Person(name,age) {
        //封装属性
        this.name = name;  //this--Python的self
        this.age = age;
    }
    //封装方法，原型链
    Person.prototype.f1 = function () {
        console.log(this.name);//this指的是Person对象, 结果：'超'
    };
    //封装方法，箭头函数的形式写匿名函数
    Person.prototype.f2 = ()=>{
        console.log(this); //Window {postMessage: ƒ, blur: ƒ, focus: ƒ, close: ƒ, frames: Window, …}  this指向的是window对象
    };

    var p1 = new Person('超',18);
    p1.age
    
    p1.f1();
    p1.f2();
    //其实在es5我们将js的基本语法的时候，没有将类的继承，但是也是可以继承的，还记得吗，那么你想，继承之后，我们是不是可以通过子类实例化的对象调用父类的方法啊，当然是可以的，知道一下就行了，我们下面来看看es6里面的类怎么写

    class Person2{
        constructor(name,age){ //对象里面的单体模式，记得上面将函数的时候的单体模式吗，这个方法类似于python的__init__()构造方法，写参数的时候也可以写关键字参数 constructor(name='超2',age=18)
            //封装属性
            this.name = name;
            this.age = age;
        }  //注意这里不能写逗号
        
        showname(){  //封装方法
            console.log(this.name);
        }  //不能写逗号
        showage(){
            console.log(this.age);
        }
    }
    let p2 = new Person2('超2',18);
    p2.showname()  //调用方法  '超2'
    //es6的类也是可以继承的，这里咱们就不做细讲了，将来你需要的时候，就去学一下吧，哈哈，我记得是用的extends和super


</script>

```





# 1. vue.js的快速入门使用

## 1.1 vue.js库的下载

vue.js是目前前端web开发最流行的工具库，由尤雨溪在2014年2月发布的。

另外几个常见的工具库：react.js /angular.js

官方网站：

​	中文：https://cn.vuejs.org/

​	英文：https://vuejs.org/

官方文档：https://cn.vuejs.org/v2/guide/

vue.js目前有1.x、2.x和3.x 版本，我们学习2.x版本的。2.x到3.x是平滑过渡的，也就是说你之前用2.x写的代码，用3.x的版本的vue.js也是没问题的。



## 1.2 vue.js库的基本使用

在github下载：https://github.com/vuejs/vue/releases

在官网下载地址： <https://cn.vuejs.org/v2/guide/installation.html>

vue的引入类似于jQuery，开发中可以使用开发版本vue.js，产品上线要换成vue.min.js。

学习时候 可以引入cdn地址 https://www.bootcdn.cn/vue/

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
    <script src="js/vue.min.js"></script>
    
</head>
<body>
<div id="app">
    <!-- {{ message }} 表示把vue对象里面data属性中的对应数据输出到页面中 -->
    <!-- 在双标签中显示数据要通过{{  }}来完成 -->
    <p>{{ message }}</p>
</div>
</body>
  <script>
    
      	// vue.js的代码开始于一个Vue对象。所以每次操作数据都要声明Vue对象开始。
        var vm = new Vue({
            el:'#app',   // 设置当前vue对象要控制的标签范围。
          	// data属性写法方式1
            data:{  // data是将要展示到HTML标签元素中的数据。
              message: 'hello world!',
            }
          	// 方式2
            // data:function () {
            //     return {
            //         'msg':'掀起你的盖头来1！'
            //     }
            // }
						// 方式3
            data(){   // 单体模式  这种写法用的居多，并且后面学习中有个地方一定要这样写，所以我们就记下来这种写法就可以了
                  return {
                      'msg':'掀起你的盖头来2！',
                  }
              }
            });
    
    </script>
</html>
```





总结：

```html
1. vue的使用要从创建Vue对象开始
   var vm = new Vue();
   
2. 创建vue对象的时候，需要传递参数，是自定义对象，自定义对象对象必须至少有两个属性成员
   var vm = new Vue({
     el:"#app",
	 data: {
         数据变量:"变量值",
         数据变量:"变量值",
         数据变量:"变量值",
     },
   });
   
   el:圈地，划地盘，设置vue可以操作的html内容范围，值就是css的id选择器,其他选择器也可以，但是多用id选择器。
   data: 保存vue.js中要显示到html页面的数据。
   
3. vue.js要控制器的内容外围，必须先通过id来设置。
  <div id="app">
      <h1>{{message}}</h1>
      <p>{{message}}</p>
  </div>
```



vue中的变量可以直接进行一些简单直接的js操作

```vue
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>test vue</title>
</head>
<body>

<div id="app">
    <!-- vue的模板语法，和django的模板语法类似 -->
    <h2>{{ msg }}</h2> <!-- 放一个变量，会到data属性中去找对应的值 -->
    <!-- 有人说，我们直接这样写数据不就行吗，但是你注意，我们将来的数据都是从后端动态取出来的，不能写死这些数据啊，你说对不对 -->
    <h2>{{ 'hello beautiful girl!' }}</h2>  <!-- 直接放一个字符串 -->
    <h2>{{ num+1 }}</h2>  <!-- 四则运算 -->
  	<h2>{{ 2+1 }}</h2>  <!-- 四则运算 -->
    <h2>{{ {'name':'chao'} }}</h2> <!-- 直接放一个自定义对象 -->
    <h2>{{ person.name }}</h2>  <!-- 下面data属性里面的person属性中的name属性的值 -->
    <h2>{{ 1>2?'真的':'假的' }}</h2>  <!-- js的三元运算 -->
    <h2>{{ msg2.split('').reverse().join('') }}</h2>  <!-- 字符串反转 -->


</div>

<!-- 1.引包 -->
<script src="vue.js"></script>
<script>
//2.实例化对象
    new Vue({
        el:'#app',
        data:{
            msg:'黄瓜',
            person:{
                name:'超',
            },
            msg2:'hello Vue',
            num:10,
        }
    })

</script>
</body>
</html>
```





## 1.3 vue.js的M-V-VM思想

MVVM 是Model-View-ViewModel 的缩写，它是一种基于前端开发的架构模式。

`Model` 指代的就是vue对象的data属性里面的数据。这里的数据要显示到页面中。

`View`  指代的就是vue中数据要显示的HTML页面，在vue中，也称之为“视图模板” 。

`ViewModel ` 指代的是vue.js中我们编写代码时的vm对象了，它是vue.js的核心，负责连接 View 和 Model，保证视图和数据的一致性，所以前面代码中，data里面的数据被显示中p标签中就是vm对象自动完成的。



编写代码，让我们更加清晰的了解MVVM：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="js/vue.min.js"></script>
    <script>
    window.onload = function(){
        // 创建vm对象
        var vm = new Vue({
            el: "#app",
            data: {
                name:"大标题",
                age:16,
            },
        })
    }
    </script>
</head>
<body>
    <div id="app">
        <!-- 在双标签中显示数据要通过{{  }}来完成 -->
        <h1>{{name}}</h1>
        <p>{{age}}</p>
        <!-- 在表单输入框中显示数据要使用v-model来完成，模板语法的时候，我们会详细学习 -->
        <input type="text" v-model="name">
    </div>
</body>
</html>
```

代码执行效果：





在浏览器中可以在 console.log通过 vm对象可以直接访问el和data属性,甚至可以访问data里面的数据

```javascript
console.log(vm.$el)     # #box  vm对象可以控制的范围
console.log(vm.$data);  # vm对象要显示到页面中的数据
console.log(vm.message);# 这个 message就是data里面声明的数据,也可以使用 vm.变量名显示其他数据,message只是举例.
```





总结：

```
1. 如果要输出data里面的数据作为普通标签的内容，需要使用{{  }}
   用法：
      vue对象的data属性：
          data:{
            name:"小明",
          }
      标签元素：
      		<h1>{{ name }}</h1>
2. 如果要输出data里面的数据作为表单元素的值，需要使用vue.js提供的元素属性v-model
   用法：
      vue对象的data属性：
          data:{
            name:"小明",
          }
      表单元素：
      		<input v-model="name">
      
   使用v-model把data里面的数据显示到表单元素以后，一旦用户修改表单元素的值，则data里面对应数据的值也会随之发生改变，甚至，页面中凡是使用了这个数据都会发生变化。
```







# 2.  Vue指令系统的常用指令

指令 (Directives) 是带有“v-”前缀的特殊属性。每一个指令在vue中都有固定的作用。

在vue中，提供了很多指令，常用的有：v-html、v-if、v-model、v-for等等。





## 2.1 文本指令v-html和v-text

​	v-text相当于js代码的innerText，相当于我们上面说的模板语法，直接在html中插值了，插的就是文本，如果data里面写了个标签，那么通过模板语法渲染的是文本内容，这个大家不陌生，这个v-text就是辅助我们使用模板语法的

​	v-html相当于innerHtml

```vue
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>test vue</title>
</head>
<body>

<div id="app">
    <!-- vue的模板语法 -->
    <div>{{ msg }}</div>
    <div v-text="msg"></div>
    <div v-html="msg"></div>

</div>

<script src="vue.js"></script>
<script>

    new Vue({
        el:'#app',
        data(){
            //记着data中是一个函数，函数中return一个对象，可以是一个空对象，但必须return
            return{
                msg:'<h2>超</h2>', //后端返回的是标签，那么我们就可以直接通过v-html渲染出来标签效果
            }
        }
    })

</script>
</body>
</html>
```





指令会在vm对象的data属性的数据发生变化时，会同时改变元素中的其控制的内容或属性。

因为vue的历史版本原因，所以有一部分指令都有两种写法：

```
vue1.x写法             vue2.x的写法
v-html         ---->   {{  }}   # vue2.x 也支持v-html
v-bind:属性名   ---->   :属性
v-on:事件名     ---->   @事件名
```



## 2.2 条件渲染指令v-if和v-show

vue中提供了两个指令可以用于判断是否要显示元素，分别是v-if和v-show。

### 2.4.1 v-if

```html
  标签元素：
      <!-- vue对象最终会把条件的结果变成布尔值 -->
			<h1 v-if="ok">Yes</h1>
  data数据：
  		data:{
      		ok:false    // true则是显示，false是隐藏
      }
```





### 2.2.2 v-else

v-else指令来表示 v-if 的“else 块”，v-else 元素必须紧跟在带 v-if 或者 v-else-if 的元素的后面，否则它将不会被识别。

```html
  标签元素：
			<h1 v-if="ok">Yes</h1>
			<h1 v-else>No</h1>
  data数据：
  		data:{
      		ok:false    // true则是显示，false是隐藏
      }
```



### 2.2.3 v-else-if

在vue2.1.0版本之后，又添加了v-else-if，`v-else-if`，顾名思义，充当 `v-if` 的“else-if 块”，可以连续使用。

可以出现多个v-else-if语句，但是v-else-if之前必须有一个v-if开头。后面可以跟着v-else，也可以没有。

```html
  标签元素：
			<h1 v-if="num===1">num的值为1</h1>
			<h1 v-else-if="num===2">num的值为2</h1>
		  <h1 v-else>num的值是{{num}}</h1>
  data数据：
  		data:{
      		num:2
      }
```



### 2.2.4 v-show

```vue
标签元素：
			<h1 v-show="ok">Hello!</h1>
  data数据：
  		data:{
      		ok:false    // true则是显示，false是隐藏
      }
```





简单总结v-if和v-show

```

v-show后面不能v-else或者v-else-if

v-show隐藏元素时，使用的是display:none来隐藏的，而v-if是直接从HTML文档中移除元素[DOM操作中的remove]

v-if 是“真正”的条件渲染，因为它会确保在切换过程中条件块内的事件监听器和子组件适当地被销毁和重建。

v-if 也是惰性的：如果在初始渲染时条件为假，则什么也不做——直到条件第一次变为真时，才会开始渲染条件块。

相比之下，v-show 就简单得多——不管初始条件是什么，元素总是会被渲染，并且只是简单地基于 CSS 进行切换。

一般来说，v-if 有更高的切换开销，而 v-show 有更高的初始渲染开销。因此，如果需要非常频繁地切换，则使用 v-show 较好；如果在运行时条件很少改变，则使用 v-if 较好。
```





## 2.3 操作属性v-bind

格式：

```
<标签名 :标签属性="data属性"></标签名>
```



```html
<p :title="str1">{{ str1 }}</p> <!-- 也可以使用v-html显示双标签的内容，{{  }} 是简写 -->
<a :href="url2">淘宝</a>
<a v-bind:href="url1">百度</a>  <!-- v-bind是vue1.x版本的写法 -->

```

显示wifi密码效果：配合v-on事件绑定

```vue
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="js/vue.js"></script>
</head>
<body>

<div id="index">
    <img :src="url" :alt="title"><br>
    <input :type="type" placeholder="请输入wifi密码"> <button @click="type='text'">显示密码</button>
  <!--切换密码显示写法，但是一般不建议将这么复杂的逻辑直接写到属性值里面，一般通过事件操作来玩，下面就说一下事件操作-->
  <button @click="type=(type=='password'?'text':'password')">切换显示密码</button>
  
  // 还可以按照下面的方式用，但必须是{}包裹
  <p v-bind:class="{active:status===false}">你是个p</p>
  <p v-bind:class="{active:status}">你是个p</p>
</div>

<script>
    let vm = new Vue({
        el:"#index",
        data:{
          url:"https://www.luffycity.com/static/img/head-logo.a7cedf3.svg",
          title:"路飞学成",
          type:"password",
          status:false,
        }
    })
</script>
</body>
</html>
```



## 2.4 事件绑定v-on和methods属性

有两种事件操作的写法，@事件名 和 v-on:事件名

```html
<button v-on:click="num++">按钮</button>   <!-- v-on 是vue1.x版本的写法 -->
<button @click="num+=5">按钮2</button>
```

总结：

```
1. 使用@事件名来进行事件的绑定
   语法：
      <h1 @click="num++">{{num}}</h1>

2. 绑定的事件的事件名，全部都是js的事件名：
   @submit   --->  onsubmit
   @focus    --->  onfocus
   ....

```

#### 例1:wifi密码切换显示

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="js/vue.js"></script>
</head>
<body>

<div id="index">
    <img :src="url" :alt="title"><br>
    <input :type="type" placeholder="请输入wifi密码">
    <button @click="clickhander">{{type_tips}}</button>
  	<button @mouseover="clickhander">{{type_tips}}</button> <!--事件名称都是按照js中的事件名称来的，所以可以使用的事件很多-->
    <button v-on:click="clickhander">{{type_tips}}</button>
</div>

<script>
    let vm = new Vue({
        el:"#index",
        // 在data可以定义当前vue对象调用的属性,调用格式: this.变量名,例如： this.title
        data:{
          url:"https://www.luffycity.com/static/img/head-logo.a7cedf3.svg",
          title:"路飞学成",
          type:"password",
          type_tips: "显示密码",
        },
        methods:{ // 在methods中可以定义当前vue对象调用的方法,调用格式：this.方法名(),例如： this.clickhander()
            clickhander(){
                // alert(this.type); // 调用上面的data里面的数据
                if(this.type=="password"){
                    this.type="text";
                    this.type_tips="隐藏密码";
                }else{
                    this.type="password";
                    this.type_tips="显示密码";
                }
            }
        }
    })
</script>
</body>
</html>
```



#### 例2:完成商城的商品增加减少数量

步骤：

1. 给vue对象添加操作数据的方法
2. 在标签中使用指令调用操作数据的方法

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="js/vue.js"></script>
</head>
<body>
    <div id="box">
        <button @click="++num">+</button>
        <input type="text" v-model="num">
        <button @click="sub">-</button> <!-- 有人说--也可以，是的，但是单纯的使用--你会发现，数据会出现负数，负数是不合理的，所以要加判断，逻辑就复杂一些了，直接写在属性值里面不太好，那么想到的就是事件 -->
    </div>

    <script>
        let vm = new Vue({
            el:"#box",
            data:{
                num:0,
            },
            methods:{
              	// sub:function(){},下面是这个写法的缩写
                sub(){
                    if(this.num<=1){
                        this.num=0;
                    }else{
                        this.num--;
                    }
                }
            }
        })
    </script>
</body>
</html>

<!--#box>(button+input+button) tab键，快速生成html标签-->

```



## 2.5 操作样式

### 2.5.1 控制标签class类名

```
格式：
   <h1 :class="值">元素</h1>  值可以是对象、对象名、数组（数组的方式用的比较少）
```



```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="js/vue.js"></script>
    <style>
    .box1{
        color: red;
        border: 1px solid #000;
    }
    .box2{
        background-color: orange;
        font-size: 32px;
    }
    </style>
</head>
<body>
    <div id="box">
        <!--- 添加class类名，值是一个对象
        {
         class类1:布尔值变量1,
         class类2:布尔值变量2,
        }
         -->
        <p :class="{box1:myclass1}">一个段落</p>
        <p @click="myclass3=!myclass3" :class="{box1:myclass2,box2:myclass3}">一个段落</p>
    </div>
    <script>
        let vm1=new Vue({
            el:"#box",
            data:{
                myclass1:false, // 布尔值变量如果是false，则不会添加对象的属性名作为样式
                myclass2:true,  // 布尔值变量如果是true，则不会添加对象的属性名作为样式
                myclass3:false,
            },
        })
    </script>

    <!-- 上面的代码可以:class的值保存到data里面的一个变量，然后使用该变量作为:class的值 -->
    <style>
    .box4{
        background-color: red;
    }
    .box5{
        color: green;
    }
    </style>
    <div id="app">
        <button @click="mycls.box4=!mycls.box4">改变背景</button>
        <button @click="mycls.box5=!mycls.box5">改变字体颜色</button>
        <p :class="mycls">第二个段落</p>
      	<!-- 还有下面这种将类值当作属性值来操作的方式 -->
        <p :class="status?'bg1':'bg2'">一段文本</p> <!-- 注意，bg1必须加引号 -->

    </div>
    <script>
        let vm2 = new Vue({
            el:"#app",
            data:{
                mycls:{
                    box4:false,
                    box5:true
                },
              	status:true,
            }
        })
    </script>

    <!-- 批量给元素增加多个class样式类 -->
    <style>
    .box6{
        background-color: red;
    }
    .box7{
        color: green;
    }
    .box8{
        border: 1px solid yellow;
    }
    </style>
    <div id="app2">
            <p :class="[mycls1,mycls2]">第三个段落</p>
    </div>
    <script>
        let vm3 = new Vue({
            el:"#app2",
            data:{
                mycls1:{
                    box6:true,
                    box7:true,
                },
                mycls2:{
                    box8:true,
                }
            }
        })
    </script>
</body>
</html>
```





总结：

```html
1. 给元素绑定class类名，最常用的就是第二种。
    vue对象的data数据：
        data:{
          myObj:{
            complete:true,
            uncomplete:false,
          }
        }

		html元素：    
    		<div class="box" :class="myObj">2222</div>
    最终浏览器效果：
		    <div class="box complete">2222</div>
```





### 2.5.2 控制标签style样式

```html
格式1：值是json对象，对象写在元素的:style属性中
	 标签元素：
		     <div :style="{color: activeColor, fontSize: fontSize + 'px' }"></div>
				<!-- 注意：不能出现中横杠，有的话就套上'font-size'，或者去掉横杠，后一个单词的首字母大写，比如fontSize -->
	 data数据如下：
         data: {
             activeColor: 'red',
             fontSize: 30
         }
格式2：值是对象变量名，对象在data中进行声明
   标签元素：
   			<div v-bind:style="styleObject"></div>
   data数据如下：
         data: {
            	styleObject: {
             		color: 'red',
             		fontSize: '13px'  
			  			}
				 }

格式3：值是数组
  标签元素：
				<div v-bind:style="[style1, style2]"></div>
	data数据如下：
				data: {
                     style1:{
                       color:"red"
                     },
                     style2:{
                       background:"yellow",
                       fontSize: "21px"
                     }
				}
```



### 2.5.2 实例-vue版本选项卡

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        #card{
            width: 500px;
            height: 350px;
        }
        .title{
            height:50px;
        }
        .title span{
            width: 100px;
            height: 50px;
            background-color:#ccc;
            display: inline-block;
            line-height: 50px; /* 设置行和当前元素的高度相等,就可以让文本内容上下居中 */
            text-align:center;
        }
        .content .list{
            width: 500px;
            height: 300px;
            background-color: yellow;
            display: none;
        }
        .content .active{
            display: block;
        }

        .title .current{
            background-color: yellow;
        }
    </style>
    <script src="js/vue.js"></script>
</head>
<body>

    <div id="card">
        <div class="title">
            <span @click="num=0" :class="num==0?'current':''">国内新闻</span>
            <span @click="num=1" :class="num==1?'current':''">国际新闻</span>
            <span @click="num=2" :class="num==2?'current':''">银河新闻</span>
            <!--<span>{{num}}</span>-->
        </div>
        <div class="content">
            <div class="list" :class="num==0?'active':''">国内新闻列表</div>
            <div class="list" :class="num==1?'active':''">国际新闻列表</div>
            <div class="list" :class="num==2?'active':''">银河新闻列表</div>
        </div>
    </div>
    <script>
        // 思路：
        // 当用户点击标题栏的按钮[span]时，显示对应索引下标的内容块[.list]
        // 代码实现：
        var card = new Vue({
            el:"#card",
            data:{
                num:0,
            },
        });
    </script>

</body>
</html>
```





## 2.6 列表渲染指令v-for

在vue中，可以通过v-for指令可以将一组数据渲染到页面中，数据可以是数组或者对象。

```html
数据是数组：        
        <ul>
            <!--i是列表的每一个元素-->
            <li v-for="book in book_list">{{book.title}}</li>
        </ul>

        <ul>
           
          	<!-- v-for不仅可以遍历数组，还可以遍历对象，这里大家记住v-for里面的一个东西 :key, 就是v-bind:key，这个key是干什么的呢，就是为了给现在已经渲染好的li标签做个标记，以后即便是有数据更新了，也可以在这个li标签里面进行数据的更新，不需要再让Vue做重新生成li标签的dom操作，提高页面渲染的性能，因为我们知道频繁的添加删除dom操作对性能是有影响的，我现在将数据中的id绑定到这里，如果数据里面有id，一般都用id，如果没有id，就绑定v-for里面那个index(当然你看你给这个索引取的变量名是什么，我这里给索引取的名字是index)，这里面它用的是diff算法，回头再说这个算法 -->
        <!--  <li v-for="(item,index) in data.users" :key="item.id" @click> 还可以绑定事件 -->
        <li v-for="(item,index) in book_list" :key="item.id"> 第{{index+1}}本图书：{{book.title}}</li>
        <!-- v-for的优先级最高，先把v-for遍历完，然后给:key加数据，还有，如果没有bind这个key，有可能你的页面都后期用动态数据渲染的时候，会出现问题，所以以后大家记着，一定写上v-bind:key -->
        </ul>


        <script>
            var vm1 = new Vue({
                el:"#app",
                data:{
                    book_list:[
                        {"id":1,"title":"图书名称1","price":200},
                        {"id":2,"title":"图书名称2","price":200},
                        {"id":3,"title":"图书名称3","price":200},
                        {"id":4,"title":"图书名称4","price":200},
                    ]
                }
            })
        </script>

数据是对象：
        <ul>
            <!--i是每一个value值-->
            <li v-for="value in book">{{value}}</li>
        </ul>
        <ul>
            <!--value是每一个value值,attr是每一个键名-->
            <li v-for="value,attr in book">{{attr}}:{{value}}</li>
        </ul>
        <script>
            var vm1 = new Vue({
                el:"#app",
                data:{
                    book: {
                        // "attr属性名":"value属性值"
                        "id":11,
                        "title":"图书名称1",
                        "price":200
                    },
                },
            })
        </script>

```

练习：

```html
goods:[
	{"name":"python入门","price":150},
	{"name":"python进阶","price":100},
	{"name":"python高级","price":75},
	{"name":"python研究","price":60},
	{"name":"python放弃","price":110},
]

# 把上面的数据采用table表格输出到页面，价格大于60的那一条数据需要添加背景色
```







# 3. Vue对象提供的属性功能

## 3.1 过滤器

过滤器，就是vue允许开发者自定义的文本格式化函数，可以使用在两个地方：输出内容和操作数据中。

定义过滤器的方式有两种,全局和局部过滤器

### 3.1.1 使用Vue.filter()进行全局定义

```javascript
Vue.filter("RMB1", function(v){
  	//就是来格式化(处理)v这个数据的
  	if(v==0){
    		return v
  	}

  	return v+"元"
})
```



### 3.1.2 在vue对象中通过filters属性来定义

```javascript
var vm = new Vue({
  el:"#app",
  data:{},
  filters:{
    RMB2:function(value){
      if(value==''){
        return;
      }else{
      	return '¥ '+value;
      }
    }
	}
});
```



示例：数据小数点保留3位，并在后面加上一个元字

​	Filter.js

```js
// 全局过滤器
// Vue.filter("过滤器名称","调用过滤器时执行的函数")
Vue.filter("RMB",function(value){
    return value+"元";
});
```



​	html文件

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="js/vue.js"></script>
    <script src="js/filters.js"></script>
</head>
<body>

    <div id="app">
        价格：{{price.toFixed(3)}}<br>
        价格：{{price|keepdot2(3)|RMB}}<br>
        价格：{{price|keepdot2(3)|RMB}}<br>  
        价格：{{price|keepdot2(3)|RMB}}<br>
        价格：{{price|keepdot2(3)}}<br>
    </div>

    <script>

        var vm1 = new Vue({
            el:"#app",
            data:{
                price: 20.3
            },
            methods:{},
            // 普通过滤器[局部过滤器]
            filters:{
                keepdot2(value,dot){  //这里有两个参数，第二个参数必须是调用过滤器时过滤器函数名称括号里面的值
                    return value.toFixed(dot)
                }
            }
        })
    </script>

</body>
</html>
```





## 3.2 计算和侦听属性

### 3.2.1 计算属性

我们之前学习过字符串反转，如果直接把反转的代码写在元素中，则会使得其他同事在开发时时不易发现数据被调整了，所以vue提供了一个计算属性(computed)，可以让我们把调整data数据的代码存在在该属性中。其实计算属性主要用于监听，可以监听多个对象，后面学了监听之后再说。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="js/vue.min.js"></script>
		<script>
		window.onload = function(){
        var vm = new Vue({
            el:"#app",
            data:{
                str1: "abcdefgh"
            },
            computed:{   //计算属性：里面的函数都必须有返回值
                strRevs: function(){
                    var ret = this.str1.split("").reverse().join("");
                    return ret
                }
            }
        });
    }
    </script>
</head>
<body>
    <div id="app">
         <p>{{ str1 }}</p>
         <p>{{ strRevs }}</p>
    </div>
</body>
</html>
```



示例：过滤器和计算属性的简单对比

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="js/vue.js"></script>
    <script src="js/filters.js"></script>
</head>
<body>

    <div id="app">
        原价格：{{price|k2}}<br>
        折扣价：{{new_price}}<br>
    </div>

    <script>

        var vm1 = new Vue({
            el:"#app",
            data:{
                price: 20.3,
                sale: 0.6,
            },
            // 过滤器
            filters:{
                k2(value){
                    return value.toFixed(2)
                }
            },
            // 计算属性
            computed:{
                new_price(){
                    return (this.price*this.sale).toFixed(2);
                }
            }
        })
    </script>

</body>
</html>
```





### 3.2.2 监听属性

侦听属性，可以帮助我们侦听data某个数据的变化，从而做相应的自定义操作。

侦听属性是一个对象，它的键是要监听的对象或者变量，值一般是函数，当侦听的data数据发生变化时，会自定执行的对应函数，这个函数在被调用时，vue会传入两个形参，第一个是变化后的数据值，第二个是变化前的数据值。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="js/vue.js"></script>
    <script>
      window.onload = function(){
         var vm = new Vue({
            el:"#app",
            data:{
                num:20
            },
            watch:{
                num:function(newval,oldval){
                    //num发生变化的时候，要执行的代码
                    console.log("num已经发生了变化！",newval,oldval);
                }
            }
        })
      }
    </script>
</head>
<body>
    <div id="app">
        <p>{{ num }}</p>
        <button @click="num++">按钮</button>
    </div>
</body>
</html>
```

示例：用户名长度限制4-10位

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="js/vue.js"></script>
    <script src="js/filters.js"></script>
</head>
<body>

    <div id="app">
        <form action="">
            账号：<input type="text" v-model="form.username"><span :style="user_style">{{user_text}}</span><br><br>
            密码：<input type="password" v-model="form.password"><br><br>
            确认密码：<input type="password" v-model="form.password2"><br><br>
        </form>
    </div>

    <script>

        var vm1 = new Vue({
            el:"#app",
            data:{
                form:{
                    username:"",
                    password:"",
                    password2:"",
                },
                user_style:{
                    color: "red",
                },
                user_text:"用户名长度只能是4-10位"
            },
            // 监听属性
            // 监听属性的变化
            watch:{
                "form.username":function(value){ //注意，使用数据属性中的某个属性的时候，如果使用的是该数据中的内部属性，别忘了加双引号
                    if(value.length>=4 && value.length<=10){
                        this.user_style.color="blue";
                        this.user_text="用户名长度合法！";
                    }else{
                        this.user_style.color="red";
                        this.user_text="用户名长度只能是4-10位！";
                    }
                }
            }
        })
    </script>

</body>
</html>
```





## 3.3 vue对象的生命周期

每个Vue对象在创建时都要经过一系列的初始化过程。在这个过程中Vue.js会自动运行一些叫做生命周期的的钩子函数，我们可以使用这些函数，在对象创建的不同阶段加上我们需要的代码，实现特定的功能。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="js/vue.min.js"></script>
    <script>
    window.onload = function(){
        var vm = new Vue({
            el:"#app",
            data:{
                num:0
            },
            beforeCreate:function(){
                console.log("beforeCreate,vm对象尚未创建,num="+ this.num);  //undefined，就是说data属性中的值还没有放到vm对象中
                this.name=10; // 此时没有this对象呢，所以设置的name无效，被在创建对象的时候被覆盖为0
              	console.log(this.$el) //undefined
            },
            created:function(){
              	// 用的居多，一般在这里使用ajax去后端获取数据，然后交给data属性
                console.log("created,vm对象创建完成,设置好了要控制的元素范围,num="+this.num );  // 0 也就是说data属性中的值已经放到vm对象中
                this.num = 20;
                console.log(this.$el) //undefined
            },
            beforeMount:function(){
                console.log( this.$el.innerHTML ); // <p>{{num}}</p> ,vm对象已经帮我们获取到了这个视图的id对象了
                console.log("beforeMount,vm对象尚未把data数据显示到页面中,num="+this.num ); // 20,也就是说vm对象还没有将数据添加到我们的视图中的时候
                this.num = 30;
            },
            mounted:function(){
              	// 用的居多，一般在这里使用ajax去后端获取数据然后通过js代码对页面中原来的内容进行更改 
                console.log( this.$el.innerHTML ); // <p>30</p>
                console.log("mounted,vm对象已经把data数据显示到页面中,num="+this.num); // 30,也就是说vm对象已经将数据添加到我们的视图中的时候
            },
            
          	// 后面两个简单作为了解吧，测试的时候最好单独测试下面两个方法
            beforeUpdate:function(){
                // this.$el 就是我们上面的el属性了，$el表示当前vue.js所控制的元素#app
                console.log( this.$el.innerHTML );  // <p>30</p>
                console.log("beforeUpdate,vm对象尚未把更新后的data数据显示到页面中,num="+this.num); // beforeUpdate----31
                
            },
            updated:function(){
                console.log( this.$el.innerHTML ); // <p>31</p>
                console.log("updated,vm对象已经把过呢更新后的data数据显示到页面中,num=" + this.num ); // updated----31
            },
        });
    }
    </script>
</head>
<body>
    <div id="app">
        <p>{{num}}</p>
        <button @click="num++">按钮</button>
    </div>
</body>
</html>
```



总结：

```
在vue使用的过程中，如果要初始化操作，把初始化操作的代码放在 mounted 中执行。
mounted阶段就是在vm对象已经把data数据实现到页面以后。一般页面初始化使用。例如，用户访问页面加载成功以后，就要执行的ajax请求。

另一个就是created，这个阶段就是在 vue对象创建以后，把ajax请求后端数据的代码放进 created
```







## 3.4 阻止事件冒泡和刷新页面

使用.stop和.prevent

示例1：阻止事件冒泡

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        .box1{
            width: 200px;
            height: 200px;
            background: #ccc;
        }
        .box2{
            width: 100px;
            height: 100px;
            background: pink;
        }
    </style>
    <!-- <script src="js/vue.js"></script> -->
	<script src="https://cdn.bootcdn.net/ajax/libs/vue/2.7.9/vue.js"></script>
</head>
<body>
    <div id="app">
        <div class="box1" @click="show1('box1')">
		  <!--事件冒泡： 点击box2div时候同时会触发 box1的点击事件，防止这种情况 @click.stop-->
          <div class="box2" @click.stop="show2('box2')"></div>   <!-- @click.stop来阻止事件冒泡,下面再加个prevent也可以 -->
          <div class="box2" @click.stop.prevent="show2('box2')"></div> 
        </div>

        <form action="#">
            <input type="text">
            <input type="submit">
            <input type="submit" value="提交02" @click.prevent=""> <!-- @click.prevent来阻止表单提交，从而不刷新页面 -->
        </form>
    </div>

</body>
  <script>
	
	let vm = new Vue({
	    el:'#app',
	    data(){
	        return {
				currentIndex:1,
				'msg':'hello',
				'price':200.1,
				inp:'',
			}
	    },
	    methods:{
	        show1(val){
	            alert('父级标签'+ val);
	        },
	        show2(val){
	            alert('子标签' + val);
	        }
	    }
	})

</script>
</html>
```



示例2：阻止form表单提交动作

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="js/vue.js"></script>
    <script src="js/filters.js"></script>
</head>
<body>
    <div id="app">
        <form action="">
        账号：<input type="text" v-model="user"><br><br>
        密码：<input type="password" v-model="pwd"><br><br>
        <button @click.prevent="loginhander">登录</button>
        </form>
    </div>

    <script>
        var vm1 = new Vue({
            el:"#app",
            data:{
                user:"",
                pwd:"",
            },
            methods:{
                loginhander(){
                    if(this.user.length<3 || this.pwd.length<3){
                        // 长度太短不能登录
                        alert("长度太短不能登录");
                        // 也可以写个return false; 也可以不写，prevent直接就是阻止form表单的提交动作
                    }else{
                        // 页面跳转
                        location.assign("http://www.baidu.com");
                        //或者：
                        //location.href="http://www.baidu.com";
                    }
                }
            }
        })
    </script>

</body>
</html>
```







## 3.5综合案例-todolist

我的计划列表

html代码:

```html
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>todolist</title>
	<style type="text/css">
		.list_con{
			width:600px;
			margin:50px auto 0;
		}
		.inputtxt{
			width:550px;
			height:30px;
			border:1px solid #ccc;
			padding:0px;
			text-indent:10px;
		}
		.inputbtn{
			width:40px;
			height:32px;
			padding:0px;
			border:1px solid #ccc;
		}
		.list{
			margin:0;
			padding:0;
			list-style:none;
			margin-top:20px;
		}
		.list li{
			height:40px;
			line-height:40px;
			border-bottom:1px solid #ccc;
		}

		.list li span{
			float:left;
		}

		.list li a{
			float:right;
			text-decoration:none;
			margin:0 10px;
		}
	</style>
</head>
<body>
	<div class="list_con">
		<h2>To do list</h2>
		<input type="text" name="" id="txt1" class="inputtxt">
		<input type="button" name="" value="增加" id="btn1" class="inputbtn">

		<ul id="list" class="list">
			<!-- javascript:; # 阻止a标签跳转 -->
			<li>
				<span>学习html</span>
				<a href="javascript:;" class="up"> ↑ </a>
				<a href="javascript:;" class="down"> ↓ </a>
				<a href="javascript:;" class="del">删除</a>
			</li>
			<li><span>学习css</span><a href="javascript:;" class="up"> ↑ </a><a href="javascript:;" class="down"> ↓ </a><a href="javascript:;" class="del">删除</a></li>
			<li><span>学习javascript</span><a href="javascript:;" class="up"> ↑ </a><a href="javascript:;" class="down"> ↓ </a><a href="javascript:;" class="del">删除</a></li>
		</ul>
	</div>
</body>
</html>
```



特效实现效果：

```html
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>todolist</title>
	<style type="text/css">
		.list_con{
			width:600px;
			margin:50px auto 0;
		}
		.inputtxt{
			width:550px;
			height:30px;
			border:1px solid #ccc;
			padding:0px;
			text-indent:10px;
		}
		.inputbtn{
			width:40px;
			height:32px;
			padding:0px;
			border:1px solid #ccc;
		}
		.list{
			margin:0;
			padding:0;
			list-style:none;
			margin-top:20px;
		}
		.list li{
			height:40px;
			line-height:40px;
			border-bottom:1px solid #ccc;
		}

		.list li span{
			float:left;
		}

		.list li a{
			float:right;
			text-decoration:none;
			margin:0 10px;
		}
	</style>
    <script src="js/vue.js"></script>
</head>
<body>
	<div id="todolist" class="list_con">
		<h2>To do list</h2>
		<input type="text" v-model="message" class="inputtxt">
		<input type="button" @click="addItem" value="增加" class="inputbtn">
		<ul id="list" class="list">
			<li v-for="item,key in dolist">
				<span>{{item + key}}</span>
				<a @click="upItem(key)" class="up" > ↑ </a>
				<a @click="downItem(key)" class="down"> ↓ </a>
				<a @click="delItem(key)" class="del">删除</a>
			</li>
		</ul>
	</div>
	
    <script>
    // 计划列表代码
    let vm = new Vue({
        el:"#todolist",
        data:{
            message:"",
            dolist:[
                "学习html",
                "学习css",
                "学习javascript",
            ]
        },
        methods:{
            addItem(){
                if(this.messsage==""){
                    return false;
                }

                this.dolist.push(this.message);
                this.message = ""
            },
            delItem(key){
                this.dolist.splice(key, 1); //splice(从哪个位置开始,删除几个)
            },
            upItem(key){
                if(key==0){
                    return false;
                }
                // 向上移动
                let result = this.dolist.splice(key,1); // 注意返回的是删除的数组  //删除的是当前位置的数组
                this.dolist.splice(key-1,0,result[0]);  // key-1 前一个位置 追加刚刚删除的
            },
            downItem(key){
                // 向下移动
                let result = this.dolist.splice(key, 1);
                console.log(result); 
                this.dolist.splice(key+1,0,result[0]);
            }
        }
    })
    </script>
</body>
</html>
```

