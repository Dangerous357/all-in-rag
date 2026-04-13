# JSP学习笔记【二】

主要学习资料来源：[JSP 教程](https://www.w3cschool.cn/jsp/)

一、控制流语句
-------

### 1.1 if-else判断语句

样例：

```
<body>
<%! int day = 3; %> 
<% if (day == 1 | day == 7) { %>      
  <p> Today is weekend</p>
<% } else { %>      
  <p> Today is not weekend</p>
<% } %>
</body>
```

运行结果：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/adaa67d95c8caed6a4e80e1fc5a79102.png)  
 *这里我们可以看到，各种脚本标识不是为了分隔不同作用的代码，而是对代码起到标注解释的作用，实际上无论是html代码还是java代码都是一个整体。*

### 1.2 switch-case语句

样例：

```
<body>
<%! int day = 3; %> 
<%  
switch(day) { 
case 1:    
  out.println("It\'s Sunday.");    
  break; 
case 2:    
  out.println("It\'s Monday.");    
  break; 
case 3:    
  out.println("It\'s Tuesday.");    
  break; 
case 4:    
  out.println("It\'s Wednesday.");    
  break; 
case 5:    
  out.println("It\'s Thursday.");    
  break; 
case 6:    
  out.println("It\'s Friday.");    
  break; 
default:    
  out.println("It's Saturday."); 
} 
%>
</body>
```

*与上面的例子不同，此处输出未使用html标签，而是利用out.println()，整个代码块都装在脚本程序的标签中。这样写应该更不容易出错。*  
 运行结果：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/eba2616879bd4745097720482d4e9012.png)

### 1.3 循环语句

#### 1.3.1 for循环

样例：

```
</head>
<%! int fontSize; %> 
<body>
<%for ( fontSize = 3; fontSize <= 5; fontSize++){ %>   
  <font color="green" size="<%= fontSize %>">    
  JSP Tutorial   
  </font><br />
<%}%>
</body>
```

运行结果：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/cfcfa71ff9984fb30295116b9bd335eb.png)  
 *虽然把代码块都放在脚本程序的标签中，利用 out.println输出比较简单，但是利用 html标签输出可以很方便地用web方法控制文本的属性。*

#### 1.3.2 while循环

改写1.3.1的样例：

```
</head>
<%! int fontSize = 3; %> 
<body>
<%while ( fontSize <= 5){ %>   
  <font color="green" size="<%= fontSize %>">    
  JSP Tutorial   
  </font><br />
<%fontSize++;%>
<%}%>
</body>
```

#### 1.3.3 do-while循环

改写1.3.1的样例：

```
</head>
<%! int fontSize = 3; %> 
<body>
<%do{ %>   
  <font color="green" size="<%= fontSize %>">    
  JSP Tutorial   
  </font><br />
<%fontSize++;%>
<%} while ( fontSize <= 5) ;%>
</body>
```

二、隐式对象
------

*（选取了现阶段比较使用的例子讲，其他内容待补充）*  
 **用于输出boolean，char，int，double，String，object 等类型数据的重要方法：**

1. `out.print(dataType dt)`:输出Type类型的值
2. `out.println(dataType dt)`:输出Type类型的值然后换行
3. `out.flush()`:刷新输出流

三、JSP表单处理
---------

> 我们在浏览网页的时候，经常需要向服务器提交信息，并让后台程序处理。浏览器中使用 GET 和 POST 方法向服务器提交数据。

### 3.1 GET方法

**即`request.getParameter（）`方法。**

> GET方法将请求的编码信息添加在网址后面，网址与编码信息通过"?"号分隔。

GET方法的简单解释：用户在表单中输入某些信息，后端程序将这些值匹配给对应的key，提交表单后跳转至的页面对应的网址会显示如下：

```
www.w3cschool.cn/hello?key1=value1&key2=value2
```

#### 3.1.1 利用URL访问

除了利用表单，我们可以在已经设置好后端提交参数的规则，通过直接编辑浏览器网址中key和value的值对页面进行访问。  
 例如jsp文件（文件地址为http://localhost:8080/WebLearn/Hello.jsp）：

```
<body>
<h1>Using GET Method to Read Form Data</h1>
<ul>
<li><p><b>Name:</b>
   <%= request.getParameter("name")%>
</p></li>
<li><p><b>Age:</b>
   <%= request.getParameter("age")%>
</p></li>
</ul>
</body>
```

我们在地址栏中输入`http://localhost:8080/WebLearn/Hello.jsp?name=Dangerous&age=21`并访问。  
 运行结果：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/94ea452b9f9b501904cf3495422903fa.png)

#### 3.1.2 利用表单访问

**先创建一个HTML表单**（可以写在html文件里，也可以写在jsp文件里）：

*注意文件直接创建在该文件夹的第一层，别创建到其他文件夹里面*

```
<body>
<form action="Hello.jsp" method="GET">
    Name: <input type="text" name="name">
    <br />
    Age:&nbsp&nbsp&nbsp&nbsp<input type="text" name="age" />
    <input type="submit" value="Submit" />
</body>
```

(Hello.jsp文件与3.1.1中相同)

*关于form的用法在web笔记里有，这里简单说明一下action是指表单提交后跳转到的页面*

**表单打开如下**：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3de514b5a1d4df4f915c7cf4d81be05b.png)  
 **输入数据**：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c71a89e6581b0e8ddd90480fcd44dd30.png)

#### 3.1.3 总结

> GET方法是浏览器默认传递参数的方法，一些敏感信息，如密码等建议不使用GET方法。

显然，由于值是直接显示在网址中的，非常不安全。  
 **注意：** 用get时，传输数据的大小有限制 （不是参数的个数有限制），最大为1024字节。

### 3.2 POST方法

POST方法本质与GET方法相同，也是使用`request.getParameter()`来获得传递的参数。

与GET通过url传递数据不同，POST隐式提交数据是不可见的。一些敏感信息，如密码等我们可以同过POST方法传递。

**例如：**  
 修改Form.html代码：

```
<body>
<form action="Hello.jsp" method="POST">
    Name: <input type="text" name="name">
    <br />
    Age:&nbsp&nbsp&nbsp&nbsp<input type="text" name="age" />
    <input type="submit" value="Submit" />
</body>
```

修改Hello.jsp代码：

```
<body>
<h1>Using POST Method to Read Form Data</h1>
<ul>
<li><p><b>Name:</b>
   <%= request.getParameter("name")%>
</p></li>
<li><p><b>Age:</b>
   <%= request.getParameter("age")%>
</p></li>
</ul>
</body>
```

输入数据并提交：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/16e3f844253d7dd4a50fb736b1ec5c71.png)  
 其效果与GET方法相同，但地址栏中的数据都被隐藏起来了。

---

### 3.3 传递Checkbox数据

我们知道，复选框checkbox可以传递一个甚至多个数据。利用POST方法`request.getParameter()`同样可以获取Checkbox中的数据。

#### 3.3.1 使用方法

**样例：**  
 新建一个CheckBox.html文件：

```
<body>
<form action="Hello.jsp" method="POST" target="_blank">
<!-- target是打开窗口方式，_blank表示在新窗口中打开 -->
    <input type="checkbox" name="maths" /> Maths
    <input type="checkbox" name="physics" /> Physics
	<input type="checkbox" name="chemistry" /> Chemistry
	<input type="submit" value="Select Subject" />
</form>
</body>
```

修改Hello.jsp文件：

```
<body>
<h1>Checkbox Data</h1>
<ul>
<li><p><b>Maths Flag:</b>
   <%= request.getParameter("maths")%>
</p></li>
<li><p><b>Physics Flag:</b>
   <%= request.getParameter("physics")%>
</p></li>
<li><p><b>Chemistry Flag:</b>
   <%= request.getParameter("chemistry")%>
</p></li>
</ul>
</body>
```

打开网址，选中复选框并提交：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9f28d076f0eb700d3056e25ce290a478.png)  
 窗口中显示：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/cea2fd94c002feac0b1e5566bd5bb28c.png)  
 我们可以看到，复选框通过POST方法提交的值若选中则显示为"on"，未选中则显示为"null"。

#### 3.3.2 拓展：怎么对Checkbox未选中的数据进行操作

返回值虽然是以字符串形式显示的，可以直接赋值给另一个字符串并输出，但是不能对得到的字符串进行String方法的操作如判空、判等。因为没有选中的不会提交任何内容给后台，此时字符串为空，但是可以利用`s == null`或`s ！= null`判断。  
 `s.empty()`和`s == null` 的区别：`s.empty()` 表示虽然字符串中没有数据，但是指向一个内存，和 `s == ""` 效果是一样的；而 `s == null` 表示s未指向任何对象，也不指向任何内存。  
 我看了很多关于复选框未提交怎么处理的方法，有很多说要用hidden，而这个是最简单的。

**对checkbox提交数据的判断方法举例：**

更改jsp代码为：

```
<h1>Checkbox Data</h1>
<ul>
<li><p><b>Maths Flag:</b>
<% if (request.getParameter("maths") != null )  out.println("YES"); 
	else out.println("NO");
%>
<li><p><b>Physics Flag:</b>
<% if (request.getParameter("physics") != null)  out.println("YES"); 
	else out.println("NO");
%>
<li><p><b>Chemistry Flag:</b>
<% if (request.getParameter("chemistry") != null)  out.println("YES"); 
	else out.println("NO");
%>
</ul>
```

同样选中复选框并提交，窗口显示：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/cc7f198fc3d9da6f62bb75462a42cb8a.png)  
 显然，我们的操作成功

### 3.4 读取所有表单数据

> 我们将使用 HttpServletRequest  
>  的getParameterNames()来读取所有可用的表单参数,该方法可以取得所有变量的名称，该方法返回一个Emumeration。  
>  一旦我们有了一个Enumeration（枚举），我们就可以调用hasMoreElements（）方法来确定何时停止使用和nextElement（）方法来获得每个参数的名称。

以3.3复选框举例，改写jsp文件：  
 先引包：`<%@ page import = "java.io.*,java.util.*" %>`

```
<h1>Data</h1>
<table width="100%" border="1" align="center">
<tr bgcolor="#949494">
<th>Param Name</th><th>Param Value(s)</th>
</tr>
<%    Enumeration PNames = request.getParameterNames(); //枚举name集
	  while(PNames.hasMoreElements())//如果集合中还有其他的枚举
	  {       
		  String Name = (String)PNames.nextElement();//指针指向下一个枚举，且强制转换成字符串     
		  out.print("<tr><td>" + Name + "</td>\n");
     	  String[] Value = request.getParameterValues(Name);//获取name对应的value
      	  out.println("<td> " + Value[0] + "</td></tr>\n");
   }
%>
</table>
```

运行结果：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/32c8fe5d90d5aaefc2260385a072d8e4.png)  
 可以看出未选中的选项仍然没有提交到后台。

### 3.5 读取表单数据的方法

#### 3.5.1 功能总结

1. `getParameter()`：使用 request.getParameter() 方法来获取表单参数的值。
2. `getParameterNames()`：该方法可以取得所有变量的名称，该方法返回一个Emumeration（枚举集）。
3. `getParameterValues()`：获得如checkbox类（名字相同，但值有多个）的数据。**注意返回的是数组类型**。
4. `getInputStream()`：调用此方法来读取来自客户端的二进制数据流。

#### 3.5.2 拓展：通过超链接传递参数

我们知道可以通过`jsp:forward`动作标签实现页面跳转，可以通过form表单与`getParameter()`结合获取数据。另一种方法是利用超链接传递参数，类似GET方法中用URL传参。

在超链接标签`<a>`中插入超链接的网址，用`?key=value`的方法传递参数。（注意此处的网址不是文件名，而是文件url地址），例如：

```
<a href="http://localhost:8080/WebLearn/Hello.jsp?name=Dangerous&age=21"
```

在下一个页面用request.getParameter(“参数名”)得到值。

*实际上，学了这些内容之后，我已经可以独立完成一整套简单的、带有页面的数据库课程设计了*  
 *【新手笔记，欢迎指正】*