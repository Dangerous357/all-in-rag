# JSP学习笔记【一】

主要学习资料来源：[JSP 教程](https://www.w3cschool.cn/jsp/)

一、关于JSP的前期准备
------------

### 1.1 什么是JSP

> JSP全称Java Server Pages，是一种动态网页开发技术。它使用JSP标签在HTML网页中插入Java代码。JSP是一种Java servlet，主要用于实现Java web应用程序的用户界面部分。

> 当浏览器请求JSP页面时，JSP引擎会首先去检查是否需要编译这个文件。如果这个文件没有被编译过，或者在上次编译后被更改过，则编译这个JSP文件。  
>  编译的过程包括三个步骤：解析JSP文件。将JSP文件转为servlet。编译servlet。

通俗地讲，我们如果要实现java的可视化，用网页完成用户和java的交互，要用到一种叫servlet的东西。而JSP就是一种servlet，实现web与java的交互，写网页更方便。

JSP可以用它自己的语法结构，将JAVA代码和HTML代码结合起来，所以如果之前学习了java和html，那么学JSP是很快的。便于说明，本文中所有XML语法我都用html解释，可能解释的不准确甚至有误，可及时向我反馈。

*我是在一周内完成了数据库课程设计，JSP的学习大概也就两三天吧，除了前面软件下载，代码部分完全是自学，前端的代码还有一些交互过程中细节部分花费的时间比较长，总体来讲就JSP部分而言上手其实很快。*

### 1.2 配置环境

*我自己按照网上的教程没有配置成功，找了个大佬给我弄好的，硬件配置永远是我的弱点……*

* 配置JDK（之前已经配置过，这里就不讲了）
* 配置web环境（下载Tomcat，按照相关提示配置）  
   尝试过安装的都知道，要成功运行Tomcat才能说明配置成功。如果环境变量出问题导致系统提示“指定的服务未安装”，可以参考这个[运行tomcat8w.exe未安装指定的服务](https://www.cnblogs.com/louby/p/6123835.html)   
   如果要更改Tomcat的路径，需要改很多东西。[Tomcat安装后修改路径方法](https://www.cnblogs.com/happy-xiaoxiao/p/11739606.html)
* 使用eclipse搭建JSP开发环境  
   [使用eclipse编写运行jsp文件](https://blog.csdn.net/cm_xiaomo/article/details/78541700)  
   [eclipse怎么创建web项目](https://blog.csdn.net/weixin_39958025/article/details/117989644)

### 1.3 创建并运行

（1.2中的几个链接里都有创建web项目的方法，这里再介绍一遍。）

* 在工具栏依次点击【File】>>>【New】>>>【Dynamic Web Project】，表示创建了一个web项目（web项目里也可以写java类，不冲突）  
   如果在NEW的选项中没有找到Dynamic Web Project，选择others，然后在Web选项中找到Dynamic Web Project  
   ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/aeebbb29ca5b44317b94b8bf32418d39.png)
* 写入项目名称  
   ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/13fb0a8fe06e874dcaf2acdb0663e3b6.png)点击Next按钮→继续选择next按钮→将Generate web.xml前面的复选按钮钩中后，点击Finish完成。创建好的项目如下：  
   ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5a986d2c4323277efe91df3e8369740b.png)
* 新建jsp文件：在项目上右键选择New→ JSP File（如果找不到JSP File，还是选择others）→在File name中填写文件名称（这里的jsp文件名是可以随便定义的）→Finish  
   ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5ac80fe93fc2f1a8ace8d6e1afccfd9b.png)
* 修改、编写代码  
   文件创建后，自动生成了一部分代码。  
   **需要注意的是，在生成的部分代码中，要将charset后的参数改成“utf-8”，否则显示中文会出现乱码**  
   编辑代码，加入代码行`<h1>Hello JSP !</h1>`  
   ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/523dbe91e1ce267f30927a8bcbef1b53.png)
* 测试运行  
   在servers的tomcat中右键选择clean tomcat work directory，具体是干嘛的我也说不清。[Clean Tomcat Work Directory](https://blog.csdn.net/yeyiting/article/details/82900016)  
   保存代码后直接运行即可。  
   ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/888c50e41a0180af132e6640ddc93c39.png)  
   点Finish，等待一段时间（刚开始运行需要配置的时间会久一点）  
   弹出页面，运行成功！  
   ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6c5a8f94896a05a22e952e65ac67d154.png)  
   地址栏里的网址“http://localhost:8080/WebLearn/Hello.jsp”可以通过浏览器打开。显然这个网址的结构是http://localhost:8080/你的web/你的jsp文件地址

### 1.4 常见问题

*这里看不懂没关系，遇到问题的时候来这里找解决办法就好。*

* 端口占用  
   在学习的时候，我发现eclipse打开时间太久，运行的时候会警示端口被占用。最简单的方法就是彻底关掉eclipse，等一会再重新打开。  
   如果不知道是哪里的问题，可以参考[eclipse tomcat报Several ports(8005 8080 8009)端口被占用问题解决方案](https://www.cnblogs.com/liuurick/p/10713685.html)  
   或者参考[如何解决Tomcat端口号被占用](https://blog.csdn.net/gao_sl/article/details/80845989)  
   基本上关于端口占用的问题，按照他们的方法都可以解决。
* 中文乱码  
   我们学了前端知道，在web中用户可以通过填写form表单提交自己的信息数据。在我写项目的时候发现，我在text文本框中提交的中文数据，反馈给后台的都是火星文。  
   改正前的代码：

```
<%! String name; %>
<% name = request.getParameter("name"); %>
```

最后是怎么解决的呢，首先我把上面所有编码方式后面的值都改成gb2312，然后代码改成下面这样：

```
<%! String name; %>
<% request.setCharacterEncoding("UTF-8"); %>
<% name = request.getParameter("name"); 
response.setCharacterEncoding("gb2312");//通知服务器发送数据时查阅的码表
response.setContentType("text/html;charset=gb2312");//通知浏览器以何种码表打开
PrintWriter outchar1 = response.getWriter();
outchar1.write(name);
%>
```

具体什么原理我也不清楚，参考文章在这里：[form提交数据中文乱码问题总结](https://www.cnblogs.com/yyz666/p/4051294.html)

完成上述步骤后，就可以开始JSP脚本内容的学习了

二、JSP的脚本内容
----------

### 2.1 注释

```
<%--注释的内容--%>
```

**快捷键：ctrl+shift+/**  
 不同情况下使用注释的语法规则：

| 语法 | 描述 |
| --- | --- |
| `<%-- 注释 --%>` | JSP注释，注释内容不会被发送至浏览器甚至不会被编译 |
| `<!-- 注释 -->` | HTML注释，通过浏览器查看网页源代码时可以看见注释内容 |
| `<\%` | 代表静态 <%常量 |
| `%\>` | 代表静态 %> 常量 |
| `\'` | 在属性中使用的单引号 |
| `\"` | 在属性中使用的双引号 |

### 2.2 java脚本段

```
<%代码片段%>
```

脚本段写的是通常在java程序中写在方法体中的java脚本，里面不能继续写方法。脚本程序可以包含任意量的java语句、变量、方法或表达式，只要它们在脚本语言中是有效的，写的java代码要满足格式规范。

注意：任何文本、HTML标签、JSP元素必须写在脚本程序的外面。

```
<html>
<head>
<title>Hello World</title>
</head>
<body>
Hello World!<br/>
<% out.println("Hello World!"); %>
</body>
</html>
```

<这里输出语句为什么没有加类名System我也不知道>

### 2.3 jsp声明

```
<%!代码片段 %>
```

一个声明语句可以声明一个或多个变量、方法，供后面的java代码使用。在jsp文件中，必须先声明这些变量和方法然后才能使用它们。

jsp声明写在类中，根据类体规范来写。程序示例：

```
<%! int i = 0; %> 
<%! int a, b, c; %> 
<%! Circle a = new Circle(2.0); %>
```

**注意：** 声明语句只声明，一定不要赋值！赋值和声明要分开。因为这个页面从打开到关闭只声明一次，若声明的同时初始化，刷新页面时不会再编译声明语句，变量不会重新初始化，而是会以刷新前的值为初值，结果就是你的数越刷越大。

### 2.4 jsp表达式

```
<%= 代码片段 %>
```

将表达式（变量，方法的调用）输出在页面中。这个JSP表达式中包含的脚本语言表达式，先被转化成String，然后插入到表达式出现的地方。

实现将java语言的返回值直接输出在html语言中然后编译出来

表达式元素中可以包含任何符合Java语言规范的表达式，但是不能使用分号来结束表达式。

程序示例：

```
<html> 
<head>
<title>A Comment Test</title>
</head> 
<body>
<p>   
  Today's date: <%= (new java.util.Date()).toLocaleString()%>
</p>
</body> 
</html>
```

其中`(new java.util.Date()).toLocaleString()`的作用是获取当前时间  
 运行后得到以下结果：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/cdb275cbd6c8a2e74911a33eb3a00d3d.png)

三、jsp行为（动作）
-----------

JSP行为标签本质上是html代码。它能够动态插入一个文件，引导用户去另一个页面，为Java插件产生相关的HTML等等。

* JSP动作元素在请求处理阶段起作用。
* **行为标签只有一种语法格式，它严格遵守HTML标准：**

```
 <jsp:action_name attribute="value" />
```

* 动作可以用`< ></ >`写，也可以用`< />`写，效果是一样的。

### 3.1 动作属性

所有的动作要素都有两个属性：id属性和scope属性

1. **id属性**  
    id属性是动作元素的唯一标识，可以在JSP页面中引用。动作元素创建的id值可以通过PageContext来调用。
2. **scope属性**  
    该属性用于识别动作元素的生命周期。id属性和scope属性有直接关系，scope属性定义了相关联id对象的寿命。  
    scope属性有四个可能的值： page 、request 、session 和 application。

### 3.2 < jsp:include >动作元素

用于在当前页面中包含静态或动态资源（**在页面被请求的时候**引入一个文件），通俗地讲就是把文件直接导入到你的页面里。  
 **语法格式：**

```
<jsp:include page="relative URL" flush="true" />
```

* page属性：包含在页面中的相对URL地址。
* flush属性：布尔属性，定义在包含资源前是否刷新缓存区。

### 3.3 < jsp:useBean >动作元素

用于寻找和初始化一个JavaBean组件。（据说这个功能非常有用，目前我还没有用到过）JavaBean到底是什么……有待补充。

**语法格式：**

```
<jsp:useBean id="name" class="package.class" />
```

在类载入后，我们既可以通过 jsp:setProperty 和 jsp:getProperty 动作来修改和检索bean的属性。

* `jsp:setProperty`：设置 JavaBean组件的值
* `jsp:getProperty`：将JavaBean组件的值插入到 output中，输出。

**相关属性：**

* class：指定Bean的完整包名
* type：指定将引用该对象变量的类型
* beanName：通过通过 java.beans.Beans 的 instantiate() 方法指定Bean的名字。

### 3.4 < jsp:setProperty >动作元素

jsp:setProperty用来设置已经实例化的Bean对象的属性（通俗讲是类的数据成员的初始化吧）。

**有两种用法：**

1. 可以在jsp:useBean元素的外面（后面）使用jsp:setProperty，例：

```
<jsp:useBean id="myName" ... />
<jsp:setProperty name="myName" property="someProperty" .../>
```

此时，不管jsp:useBean是找到了一个现有的Bean，还是新创建了一个Bean实例，jsp:setProperty都会执行。

2. 把jsp:setProperty放入jsp:useBean元素的内部，例：

```
<jsp:useBean id="myName" ... >
...
   <jsp:setProperty name="myName" property="someProperty" .../>
</jsp:useBean>
```

此时，jsp:setProperty只有在新建Bean实例时才会执行，如果是使用现有实例则不执行jsp:setProperty。

#### 3.4.1 name属性

name属性是必需的。它表示要设置属性的是哪个Bean。

#### 3.4.2 property属性

property属性是必需的。它表示要设置哪个属性。  
 有一个特殊用法：如果property的值是"\*"，表示所有名字和Bean属性名字匹配的请求参数都将被传递给相应的属性set方法。

#### 3.4.3 value属性

value 属性是可选的。该属性用来指定Bean属性的值。  
 字符串数据会在目标类中通过标准的valueOf方法自动转换成数字、boolean、Boolean、 byte、Byte、char、Character。例如，boolean和Boolean类型的属性值（比如"true"）通过 Boolean.valueOf转换，int和Integer类型的属性值（比如"42"）通过Integer.valueOf转换。  
 **注意：value和param不能同时使用，但可以使用其中任意一个。**

#### 3.4.4 param属性

param 是可选的。它指定用哪个请求参数作为Bean属性的值。  
 如果当前请求没有参数，则什么事情也不做，系统不会把null传递给Bean属性的set方法。因此，你可以让Bean自己提供默认属性值，只有当请求参数明确指定了新值时才修改默认属性值。

### 3.5 < jsp:getProperty >动作元素

jsp:getProperty动作提取指定Bean属性的值，转换成字符串，然后输出。  
 **语法格式如下：**

```
<jsp:useBean id="myName" ... />
...
<jsp:getProperty name="myName" property="someProperty" .../>
```

#### 3.5.1 name属性

要检索的Bean属性名称。Bean必须已定义。

#### 3.5.2 property属性

表示要提取Bean属性的值

### 3.6 < jsp:forward >动作元素

从一个JSP文件向另一个文件传递一个包含用户请求的request对象（把请求转到一个新的页面），实现页面间的相互跳转。  
 **语法格式：**

```
<jsp:forward page="跳转页面文件名"></jsp:forward>
```

**参数传递：** 直接在标签头写`?key=value`（这里key是参数名称，value是传递值），例：

```
<jsp:forward page="success.jsp?key=value"></jsp:forward>
```

或在标签里写`<jsp:param>`，例：

```
<jsp:forward page="success.jsp">
    <jsp:param value="bbb" name="aaa"/>
</jsp:forward>
```

**注意：** 若要进行参数传递，另一个jsp页面获取时需用request.getParameter(“key”)进行获取，不传参数时，两个标签中间不能有空格或换行，不然会报错。  
 *获取参数的方法见笔记【二】*

### 3.7 其他动作元素

行为标签基本上是一些预定义好的函数，下表罗列出了一些可用的JSP行为标签：

| 语法 | 描述 |
| --- | --- |
| `jsp:plugin` | 用于在生成的HTML页面中包含Applet和JavaBean对象，根据浏览器类型为Java插件生成OBJECT或EMBED标记。 |
| `jsp:element` | 动态创建一个XML元素 |
| `jsp:attribute` | 定义动态创建的XML元素的属性 |
| `jsp:body` | 定义动态创建的XML元素的主体内容 |
| `jsp:text` | 用于封装模板数据，在JSP页面和文档中使用写入文本的模板 |

四、JSP的编译指令
----------

就是这些东西，用来设置整个JSP页面相关的属性，如网页的编码方式和脚本语言。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/339cf69c14310a43af7ef233f9f353b0.png)

书写格式:

```
<%@ directive attribute="value" %>
```

<%@ 编译指令 属性=”代码”，属性=”代码” %>

指令可以有很多个属性，它们以键值对的形式存在，并用逗号隔开。

### 4.1 pgae指令

定义网页依赖属性，比如脚本语言、error页面、缓存需求等等。

#### 4.1.1 重要、常用的page属性

1. pageEncoding属性：用于设置jsp页面的字符集
2. contentType属性：设置jsp的响应类型，指定当前JSP页面的MIME类型和字符编码（一般是html或plain）
3. import属性：导包
4. errorPage属性：当页面执行代码出现异常时，跳转的页面
5. session属性：表示当请求到本页面时，是否为其创建一个session对象（默认为true）

举例：

```
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ page import="java.util.*,java.text.*" %>
<%@ page errorPage="error.jsp" session="false" %>
<% int a = 1/0; %>  
<%--这里1/0是会报错的，结果会跳转到error.jsp页面-->
```

#### 4.1.2 其他的page属性

下表列出与Page指令相关的属性：

| 属性 | 描述 |
| --- | --- |
| buffer | 指定out对象使用缓冲区的大小 |
| autoFlush | 控制out对象的缓存区 |
| isErrorPage | 指定当前页面是否可以作为另一个JSP页面的错误处理页面 |
| extends | 指定servlet从哪一个类继承 |
| import | 导入要使用的Java类 |
| info | 定义JSP页面的描述信息 |
| isThreadSafe | 指定对JSP页面的访问是否为线程安全 |
| language | 定义JSP页面所用的脚本语言，默认是Java |
| isELIgnored | 指定是否执行EL表达式 |
| isScriptingEnabled | 确定脚本元素能否被使用 |

### 4.2 include指令

通过include指令来包含其他文件。被包含的文件可以是JSP文件、HTML文件或文本文件。包含的文件就好像是该JSP文件的一部分，会被同时编译执行。

* **file属性**  
   用来将一个页面包含在本页面（将两个jsp混合成一个java文件），注意两个页面中不要有相同的变量名。  
   语法格式：`<%@ include file="relative url" %>`  
   代码案例：`<%@includ file=”includ.jsp”%>`称为静态导入

静态导入是因为将两个文件混成一个文件，提高效率。也可利用include行为（动作）动态导入，即一个文件调用另一个文件，两个jsp文件分开执行，变量不会冲突。

### 4.3 taglib指令

JSP允许用户自定义标签，用Taglib指令引入一个自定义标签集的定义，包括库路径、自定义标签。

* 语法格式：`<%@ taglib uri="uri" prefix="prefixOfTag" %>`
* uri属性：确定标签库的位置
* prefix属性：指定标签库的前缀

*这篇笔记就到这里，具体怎么用见JSP学习笔记【二】*  
 *【新手笔记，欢迎指正】*