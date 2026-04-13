# 如何用JAVA写一个简单的电脑客户端应用

**前言：**  
 我们学习了JAVA的application和applet，其中applet是需要打开编译软件或命令行才能弹出的那种窗口，和我们平时可以下载的软件不太一样。如何开发一个.exe文件？  
 其实和写正常的application差不多，界面是用GUI实现的。先用AWT/Swing写出图形界面窗口，然后打包成.exe即可。**主要：据我初步了解，打包成的exe要想运行，必须有jre环境。**

特别说明
----

**因为我是为了快速、简单写一个申请软著，所以这篇blog只总结【用JAVA开发exe】的大概流程，心里有个概念，具体怎么开发需要各位自学。一篇经验帖，写的匆忙，最好先概览一遍，再决定是否细看。**

我使用的工具：  
 语言：JAVA  
 开发软件：eclipse  
 GUI工具：Swing

一、Swing
-------

Swing的入门应该已经学过了，定义、概念之类的我就不讲了。

### 常用包

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/322448d8630ae2f1e005402524a4810e.png)

### 容器

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/42736cde7da1681f8a3382b404d1b0a0.png)

#### 顶层容器

> 顶层容器是进行图形编程的基础，一切图形化的东西都必须包括在顶层容器中。顶层容器是任何图形界面程序都要涉及的主窗口，是显示并承载组件的容器组件。

在 Swing 中有三种可以使用的顶层容器，分别是 JFrame、JDialog 和 JApplet。

* JFrame：用于框架窗口的类，此窗口带有边框、标题、关闭和最小化窗口的图标。带 GUI 的应用程序至少使用一个框架窗口。
* JDialog：用于对话框的类。
* JApplet：用于使用 Swing 组件的 Java Applet 类。

##### JFrame

**一、构造方法：**  
 `JFrame()`：构造一个初始时不可见的新窗体。  
 `JFrame(String title)`：创建一个具有 title 指定标题的不可见新窗体。

**二、常用方法：**  
 使用样例：（复习一下java的知识：这里可以有两种使用方法，一种是像这样自定义一个对象继承基类，然后在构造函数里设置方法；另一种是先声明对象，然后通过`对象.方法`的形式设置某一对象的方法）

```
package MoneySystem;
import java.awt.*;
import javax.swing.JFrame;
import javax.swing.JLabel;

public class MoneyJFrame extends JFrame
{
	public MoneyJFrame()
	{
		setTitle("这里是窗口标题"); //设置显示窗口标题
	    setSize(400,200); //设置窗口显示尺寸
	    setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); //设置窗口是否可以关闭
	    JLabel jl=new JLabel("这是使用JFrame类创建的窗口"); //创建一个标签
	    Container c=getContentPane(); //获取当前窗口的内容窗格
	    c.add(jl); //将标签组件添加到内容窗格上
	    setVisible(true); //设置窗口是否可见
	}
	
	public static void main(String[] agrs)
	{
		new MoneyJFrame(); //创建一个实例化对象
	}      

}
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c0b6b40280613aa3a69624e0e838dbcd.png)

常用方法总结：

1. `getContentPane()`：返回此窗体的 contentPane 对象
2. `getDefaultCloseOperation()`：返回用户在此窗体上单击“关闭”按钮时执行的操作
3. `setContentPane(Container contentPane)`：设置 contentPane 属性
4. `setDefaultCloseOperation(int operation)`：设置用户在此窗体上单击“关闭”按钮时默认执行的操作。`JFrame.EXIT_ON_CLOSE`设置关闭。
5. `setDefaultLookAndFeelDecorated (boolean defaultLookAndFeelDecorated)`：设置 JFrame 窗口使用的 Windows 外观（如边框、关闭窗口的 小部件、标题等）
6. `setIconImage(Image image)`：设置要作为此窗口图标显示的图像  
    关于图标的使用：[setIconImage(icon)；设置JFrame窗口标题图标](https://blog.csdn.net/weixin_42950079/article/details/86764577)
7. `setJMenuBar( JMenuBar menubar)`：设置此窗体的菜单栏
8. `setLayout(LayoutManager manager)`：设置 LayoutManager 属性。如`setLayout(new BorderLayout())`
9. `setTitle("窗口标题")`：设置显示窗口标题
10. `setSize(宽,高)`：设置窗口显示尺寸
11. `setVisible(true)`：设置窗口是否可见
12. `setBounds(横偏移，纵偏移, 宽, 高)`：设置窗口大小和位置

#### 中间容器

> 中间容器是容器组件的一种，也可以承载其他组件，但中间容器不能独立显示，必须依附于其他的顶层容器。

常见的中间容器有 JPanel、JScrollPane、JTabbedPane 和 JToolBar。

* JPanel：表示一个普通面板，是最灵活、最常用的中间容器。
* JScrollPane：与 JPanel 类似，但它可在大的组件或可扩展组件周围提供滚动条。
* JTabbedPane：表示选项卡面板，可以包含多个组件，但一次只显示一个组件，用户可在组件之间方便地切换。
* JToolBar：表示工具栏，按行或列排列一组组件（通常是按钮）。

##### JPanel

**一、构造方法：**  
 `JPanel()`：使用默认的布局管理器创建新面板，默认的布局管理器为 FlowLayout。  
 `JPanel(LayoutManagerLayout layout)`：创建指定布局管理器的 JPanel 对象。

**二、常用方法：**  
 使用样例：

```
package MoneySystem;
import java.awt.*;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;

public class MoneyJFrame
{
	public static void main(String[] agrs)
	{
		JFrame jf=new JFrame("Java第二个GUI程序");    //创建一个JFrame对象
        jf.setBounds(300, 100, 400, 200);    //设置窗口大小和位置
        JPanel jp=new JPanel();    //创建一个JPanel对象
        JLabel jl=new JLabel("这是放在JPanel上的标签");    //创建一个标签
        jp.setBackground(Color.white);    //设置背景色
        jp.add(jl);    //将标签添加到面板
        jf.add(jp);    //将面板添加到窗口
        jf.setVisible(true);    //设置窗口可见
	}      

}
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0970e57e08507fe796aac50795284d48.png)  
 常用方法；

* `Component add(Component comp)`：将指定的组件追加到此容器的尾部
* `void remove(Component comp)`：从容器中移除指定的组件
* `void setFont(Font f)`：设置容器的字体
* `void setLayout(LayoutManager mgr)`：设置容器的布局管理器
* `void setBackground(Color c)`：设置组件的背景色

### 布局

#### 边框布局管理器BorderLayout

> BorderLayout（边框布局管理器）是 Window、JFrame 和 JDialog 的默认布局管理器。边框布局管理器将窗口分为 5 个区域：North、South、East、West 和 Center。其中，North 表示北，将占据面板的上方；Soufe 表示南，将占据面板的下方；East表示东，将占据面板的右侧；West 表示西，将占据面板的左侧；中间区域 Center 是在东、南、西、北都填满后剩下的区域。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f193d3739cc61689b3da9a742bfe83d3.png)  
 **一、构造方法：**

* `BorderLayout()`：创建一个 Border 布局，组件之间没有间隙。
* `BorderLayout(int hgap,int vgap)`：创建一个 Border 布局，其中 hgap 表示组件之间的横向间隔；vgap 表示组件之间的纵向间隔，单位是像素。

**二、设置组件布局的方法：**

```
JFrame.add(button1,BorderLayout.NORTH);
JFrame.add(button2,BorderLayout.WEST);
JFrame.add(button3,BorderLayout.CENTER);
JFrame.add(button4,BorderLayout.EAST);
JFrame.add(button5,BorderLayout.SOUTH);
```

（如果没有设置某一区域，其他区域就会填充进去。）

#### 流式布局管理器FlowLayout

FlowLayout（流式布局管理器）是 JPanel 和 JApplet 的默认布局管理器。FlowLayout 会将组件按照从上到下、从左到右的放置规律逐行进行定位。  
 **一、构造方法：**

* `FlowLayout()`：创建一个布局管理器，使用默认的居中对齐方式和默认 5 像素的水平和垂直间隔。
* `FlowLayout(int align)`：创建一个布局管理器，使用默认 5 像素的水平和垂直间隔。其中，align 表示组件的对齐方式，对齐的值必须是 `FlowLayout.LEFT`、`FlowLayout.RIGHT` 和 `FlowLayout.CENTER`，指定组件在这一行的位置是居左对齐、居右对齐或居中对齐。
* `FlowLayout(int align, int hgap,int vgap)`：创建一个布局管理器，其中 align 表示组件的对齐方式；hgap 表示组件之间的横向间隔；vgap 表示组件之间的纵向间隔，单位是像素。

#### 卡片布局管理器CardLayout

> CardLayout（卡片布局管理器）能够帮助用户实现多个成员共享同一个显不空间，并且一次只显示一个容器组件的内容。 CardLayout布局管理器将容器分成许多层，每层的显示空间占据整个容器的大小，但是每层只允许放置一个组件。

**一、构造方法：**

* CardLayout()：构造一个新布局，默认间隔为 0。
* CardLayout(int hgap, int vgap)：创建布局管理器，并指定组件间的水平间隔（hgap）和垂直间隔（vgap）。

**二、使用方法：**  
 样例：

```
JFrame frame=new JFrame("Java程序");    //创建Frame窗口
JPanel p1=new JPanel();    //面板1
JPanel p2=new JPanel();    //面板2
JPanel cards=new JPanel(new CardLayout());    //卡片式布局的面板
p1.add(new JButton("登录按钮"));
p1.add(new JButton("注册按钮"));
p2.add(new JTextField("用户名文本框",20));
p2.add(new JTextField("密码文本框",20));
cards.add(p1,"card1");    //向卡片式布局面板中添加面板1，第二个参数用来标识面板
cards.add(p2,"card2");    //向卡片式布局面板中添加面板2
/*
CardLayout cl=(CardLayout)(cards.getLayout());
cl.show(cards,"card1");    //调用show()方法显示面板2，使用之前标识面板的参数
*/
frame.add(cards);
frame.setBounds(300,200,400,200);
frame.setVisible(true);
frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
```

#### 网格布局管理器GridLayout

> GridLayout（网格布局管理器）为组件的放置位置提供了更大的灵活性。它将区域分割成行数（rows）和列数（columns）的网格状布局，组件按照由左至右、由上而下的次序排列填充到各个单元格中。  
>  GridLayout 布局管理器总是忽略组件的最佳大小，而是根据提供的行和列进行平分。该布局管理的所有单元格的宽度和高度都是一样的。

**一、构造函数：**

* `GridLayout(int rows,int cols)`：创建一个指定行（rows）和列（cols）的网格布局。布局中所有组件的大小一样，组件之间没有间隔。
* `GridLayout(int rows,int cols,int hgap,int vgap)`：创建一个指定行（rows）和列（cols）的网格布局，并且可以指定组件之间横向（hgap）和纵向（vgap）的间隔，单位是像素。

#### 网格包布局管理器GridBagLayout

> GridBagLayout（网格包布局管理器）是在网格基础上提供复杂的布局，是最灵活、 最复杂的布局管理器。GridBagLayout 不需要组件的尺寸一致，允许组件扩展到多行多列。每个 GridBagLayout 对象都维护了一组动态的矩形网格单元，每个组件占一个或多个单元，所占有的网格单元称为组件的显示区域。

#### 盒布局管理器BoxLayout

略

### 参考学习教程

[Java Swing](http://c.biancheng.net/view/1206.html)

**【此处必看】说明：** swing教程我几乎没有找到很详细的，而且我的软件写出来之后很丑，和平时用的客户端差很多，开发过程中也感受到软件布局比web要困难很多，可能是因为我掌握的知识不多，也可能是因为确实存在更好用的GUI工具，只是我没找到而已。还有就是，做出来的软件性能很差，我本身就不太了解JAVA的性能控制，所以只实现了逻辑，没有管性能，但我开发的软件处理大量数据的速度超级慢。总之就是，要想认真写一个高质量软件，需要多搜集搜集相关资料，不然效果会很差。

二、打包
----

写好的代码要先打成jar包，然后jar包再用特定软件（具体什么我忘了，因为我没用到）生成exe应该就可以用了。  
 因为这个教程一抓一大把，我就不说了，这里总结一下打包遇到的问题吧！

1. 软件logo：  
    写GUI的时候一直想用个logo，于是在程序里写了（代码在下面），但是打包成jar之后就不显示了，因为要把jpeg放在jar的根目录（代码里对应的位置）。而且好像生成exe会有额外的上传logo的步骤，所以建议暂时不用管他。

```
Toolkit toolkit = Toolkit.getDefaultToolkit();
Image logo = toolkit.getImage("logo.jpeg");
Jframe jf = new Jframe();
jf.setIconImage(logo);
```

2. 打包成jre后无法点开？显示找不到主函数？  
    首先要确定，你真的添加了主函数（我刚开始就没有添加），这里不是说你代码里没有主函数，而是用eclipse导出项目的时候，有个步骤是需要添加主函数的（大概在最后一步），因为eclipse是英文，很容易忽略。  
    如果确定有主函数，还是打不开？可以试一下进cmd命令，看一下自己的java版本、javac版本和javaw是不是都正常（我用的命令是java -version），用1.8以上的版本。因为我之前下载过两个版本的jre，一个1.4一个1.8，我用命令行看的时候发现我的java是旧版，javac是新版，于是我把环境变量里的旧版路径全都删掉了，之后就统一了。统一版本之后，javaw还是有问题，这时候可能就要去注册表里了。参考文章：[安装了jdk和jre无法打开jar文件（测试过多个jdk版本和win系统，绝对百试百灵）](https://blog.csdn.net/qq_44915645/article/details/121668642?spm=1001.2014.3001.5506)果然，我打开我的注册表之后发现它里面还是旧版的，但我还是从上到下都按照文章里的步骤改了一遍，然后就可以用了。

---

 【欢迎指正】