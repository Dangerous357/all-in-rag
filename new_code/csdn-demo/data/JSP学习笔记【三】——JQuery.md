# JSP学习笔记【三】——JQuery

前言
--

在写项目的时候需要动态对某组件的属性进行调整，我看网上的教程都是使用`document.getElementById`等，但我在eclipse编写`.jsp`文件的时候，却提示**document cannot be resolved**。由于我对jsp没有系统的了解以及无人可咨询，网上也没遇到过相关解释，所以至今无解。通过查阅各种资料作出猜测如下：

1. 可能是因为document只能写在`.html`文件中的`<script>`下，而不能直接写在`.jsp`文件里。
2. 可能类似`var`变量的使用，由于jdk版本太低而无法使用。
3. 可能我的tomcat有点问题，或者哪些库没有使用正确。

**【ps：如果你能为我解答欢迎留言，非常感谢！】**

在查阅资料的过程中，了解到还有一种方法可以实现我的要求：JQuery。简单来说，JQuery的使用方法就是使用特定的语法将java代码嵌入到html中（经我简略测验，也可以写到.jsp文件里），以此来对某标签进行操作。

一、下载安装
------

jQuery 是一个 JavaScript 函数库，下载地址：<http://www.jq22.com/jquery-info122>

使用方法：

1. 直接将文件下载到项目中去使用（我这里写的不详细，因为我用的是第二种），找到要下载的版本，点击下载。  
    ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/30454a79f98b7000f95247e921b094fa.png)
2. 使用网址访问。如上图，下载地址中还给出了引用地址，可以复制代码到 **`<head>`** 中，例如：

```
<script src="https://s3.pstatp.com/cdn/expire-1-M/jquery/3.2.1/jquery.min.js"></script>
```

可以测试一下：

```
<head>
       <script type="text/javascript" src="https://s3.pstatp.com/cdn/expire-1-M/jquery/3.2.1/jquery.min.js" ></script>
       <title>JQuery 练习</title>
       <!-- 测试JQuery 是否加载     如果是undefinition 就是没引入。-->
       <script>
           if(typeof jQuery== "undefined")
           {
              window.alert("jQuery引用失败!");
           }
           else
           {
              window.alert("jQuery引用成功!");
           }
      </script>
</head>
```

二、使用工具大全
--------

### 基础语法

基础语法是：`$(selector).action()`  
 其中：

* $：定义 jQuery
* selector：选择符，“查询”和“查找” HTML 元素
* action()：执行对元素的操作。

注意，所有的JQuery都要写在`<script></script>`标签内。

### selector

| 类型 | 选择符 | 含义 |
| --- | --- | --- |
|  | `$(this).action()` | 对当前元素操作 |
| 元素选择器 | `$("p").action()` | 对所有段落（p）操作 |
| 元素选择器 | `$("p.intro").action()` | 对所有class="intro"的段落（p）操作 |
| 元素选择器 | `$("p#demo").action()` | 对所有id="demo"段落（p）操作 |
|  | `$(".test").action()` | 对class="test"的所有元素操作 |
|  | `$("#test").action()` | 对所有id="test"的元素操作 |
| 属性选择器 | `$("[href]").action()` | 对所有带有href属性的元素操作 |
| 属性选择器 | `$("[href='#']").action()` | 对所有href值等于"#"的元素操作 |
| 属性选择器 | `$("[href!='#']").action()` | 对所有href值不等于"#"的元素操作 |
| 属性选择器 | `$("[href$='.jpg']").action()` | 对所有href值以".jpg"结尾的元素操作 |
|  | `$("ul li:first").action()` | 对每个`<ul>`的第一个`<li>`元素操作 |
|  | `$("div#intro .head").action()` | 对id="intro"的`<div>`元素中的所有class="head"的元素操作 |

完整参考手册：[jQuery 参考手册 - 选择器](https://www.w3school.com.cn/jquery/jquery_ref_selectors.asp)

### action()

#### 事件

> jQuery 事件处理方法是 jQuery 中的核心函数。事件处理程序指的是当 HTML 中发生某些事件时所调用的方法。**通常会把 jQuery 代码放到 `<head>`部分的事件处理方法中**。

| 事件 | 含义 |
| --- | --- |
| ready(`function(){}`) | 将函数绑定到文档的就绪事件（当文档完成加载时） |
| click(`function(){}`) | 触发或将函数绑定到被选元素的点击事件 |
| dblclick(`function(){}`) | 触发或将函数绑定到被选元素的双击事件 |
| focus(`function(){}`) | 触发或将函数绑定到被选元素的获得焦点事件 |
| mouseover(`function(){}`) | 触发或将函数绑定到被选元素的鼠标悬停事件 |

完整参考手册：[jQuery 参考手册 - 事件](https://www.w3school.com.cn/jquery/jquery_ref_events.asp)

##### ※ ready()

所有jQuery函数需要位于一个`document ready`函数中：

```
$(document).ready
(
	function()
	{
  		// jQuery functions go here
	}
);
```

这是为了防止文档在完全加载（就绪）之前运行 jQuery 代码。

> 如果在文档没有完全加载之前就运行函数，操作可能失败。下面是两个具体的例子：
>
> * 试图隐藏一个不存在的元素
> * 获得未完全加载的图像的大小

#### 效果

效果一般配合事件使用，例如当鼠标点击时进行的某种操作，写在`function(){}`里。

| 效果 | 含义 | 备注 |
| --- | --- | --- |
| css(“background-color”,“red”) | 改变css属性 |  |
| hide(speed,callback) | 隐藏 | speed参数（可选）规定隐藏/显示的速度，callback参数（可选）是隐藏或显示完成后所执行的函数名称。 |
| show(speed,callback) | 显示 |  |
| toggle(speed,callback) | 切换显示和隐藏 |  |

### 重定向

JQuery是在页面全部加载完毕后对某些html组件进行操作，因此如果在`<script>`中写java后端的代码，不仅不会生效，还会影响其他的代码。

我的诉求：在鼠标点击时，更改效果，且同步数据库。

解决方法：由于很多教程都说要使用`$.ajax()`，这里牵扯到的知识太多了，因此我想到了另一种方法，就是先跳转到另一个jsp页面，执行后端代码，再关闭新建的页面（亲测有效）。

1. 跳转方法：

```
window.open("xxx.jsp?xx="+xx+"&&xx="+xx, "_blank");
```

其中，第一个参数是jsp页面的url，注意如果有变量，必须是在`<script>`里用var获取的，如果是当前页面中的全局java变量，在这里无法使用。

2. 关闭新建的页面

```
window.close();
```

同样要写在`<script>`中。

---

 参考来源：

[JQuery安装与下载教程](https://blog.csdn.net/qq_40976321/article/details/90552297)  
 [jQuery 教程](https://www.w3school.com.cn/jquery/index.asp)