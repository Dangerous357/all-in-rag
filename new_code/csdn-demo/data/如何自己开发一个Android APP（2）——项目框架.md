# 如何自己开发一个Android APP（2）——项目框架

.java文件
-------

### activity类

在我们创建自己的项目时，Eclipse会对应用进行设置并将主Activity作为主类——它在项目清单当中也将被作为主Activity进行显示。

这里的Activity类用于使Android系统处理向用户呈现的屏幕内容，而各方法则用于不同变量状态下的屏幕内容（创建、暂停与消除等）。

activity是java文件，用于程序最主要的开发。

```
public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }
}
```

以MainActivity类为例，首先要继承Activity类，实现`onCreate()`抽象方法。其中要调用父类方法`super.onCreate(savedInstanceState);`，并通过加载布局文件设置布局`setContentView(R.layout.activity_main);`。注意，要在AndroidManifest.xml文件中声明。

**onCreate方法**  
在主Activity类当中，其中包含的代码将在Activity被创建——也就是应用程序启动时开始执行。

其中`setContentView(R.layout.activity_main);`用于指定我们所创建的布局文件，告诉Android将其作为内容视图，为Activity创建类文件时，需要利用setContentView进行布局设置。其中的“R”代表应用资源，后面的部分则用于指定保存在“res/layout”目录下的条目类型——在这里就是布局。

```
Eclipse以及管理系统的ADT都会引用应用中来自Java的资源，在项目中对这些资源进行添加或者编辑时，Eclipse会将对应内容写入“R.java”文件，保存在“gen”文件夹中。
千万不要直接编辑这个文件，它会在我们编辑项目资源时自动生成。系统会通过为应用中的每项资源分配唯一整数ID的形式管理这一过程。
如果Eclipse显示任何与R相关的错误信息，特别是“R无法被解析为一个变量”，则需要检查类文件的起始内容，看看其中是否存在“R”的导入语句，例如“import android.R;”。如果找到了对应内容，特别是在已经将代码复制并粘贴到文件中后，请删除这一导入语句。如果遇到其它与R相关的提示，请确保资源文件当中不存在错误。如果问题仍然存在，尝试利用“Project”， “Clean”清理项目。当一切努力皆告失败时，试着重新启动Eclipse。
```

框架——资源部分
--------

### layout文件夹

显然，layout用于存放各种布局。  
创建项目时，Eclipse会提供一套基础布局用于主屏幕的布局方案，供我们进行个性化修改，用户在启动应用之后最先看到的就是它。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/99ae768ee77b2fbcefa06bb8b6aa8a64.png)  
在上面的示例中，根元素为RelativeLayout。Android当中还提供其它几种布局类型，我们可以将一种布局嵌套到另一种当中。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f30c570fb9faf7c8b193062e0c8766cb.png)  
查看编辑器右侧的Outline视图，显示的是另一套指向文件元素的界面。双击列出的项目以跳转到对应代码位置，可以展开或者折叠主元素。

切换到Graphical Layout标签，把右上角安卓图标的API调小一点，就可以直接查看自己的布局了。界面左侧的Palette区域允许我们选择UI组件并将其拖动到布局当中。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9af868ee0a89c588beb9f8ad42d287d1.png)

### drawable文件夹

用于保存应用程序所使用的图片文件。这些图片文件可以是我们在Eclipse之外所准备的数字图片文件，格式包括PNG或者JPEG等。或者，大家也可以通过XML代码来描述形状、颜色以及外观，从而定义特定可绘制资源。一旦我们在drawable文件夹中创建了文件，就可以在应用布局文件或者Java代码中进行引用。

资源目录中会保留针对每一种尺寸的drawable文件夹。这些尺寸是各类运行Android系统的设备在像素密度方面的通用型分类依据。具体类别分为低、中、高、超高与超超高密度四种。如果某资源在合适的文件夹下不存在，原则是使用最接近的密度级别。

### values文件夹

用于容纳应用程序中所使用的数据值。

可以包含文本字符串以及数字，包含XML文件的值文件会列出其中的一项或者多项值。应用中的其它文件，例如Java类或者布局文件，能够通过这些名称引用这些值。

应用程序中的不同值文件，允许大家针对特定屏幕尺寸及API级别对值进行修改。如果同样的值足以应对多种设备，则可以被直接保存在“Values”文件夹内。

* demens.xml：定义尺寸资源
* string.xml：定义字符串资源
* styles.xml：定义样式资源
* colors.xml：定义颜色资源
* arrays.xml：定义数组资源
* attrs.xml：自定义控件时用的较多，自定义控件的属性
* theme主题文件，和styles很相似，但是会对整个应用中的Actvitiy或指定Activity起作用，一般是改变窗口外观的。可在Java代码中通过setTheme使用，或者在Androidmanifest.xml中为<application…>添加theme的属性！  
  *说明：你可能看到过这样的values目录：values-w820dp，values-v11等，前者w代表平板设备，820dp代表屏幕宽度；而v11这样代表在API(11)，即android 3.0后才会用到的！*

### menu文件夹

菜单在以前有物理菜单按钮（即menu键）的手机上用的较多。

### raw目录

用于存放各种原生资源(音频，视频，一些XML文件等)，可以通过openRawResource(int id)来获得资源的二进制流！

### animator：存放属性动画的XML文件

### anim：存放补间动画的XML文件

框架——其他
------

### Manifest文件

这个文件将应用程序的各个方面定义成统一整体。Eclipse与ADT会在创建应用的同时，在清单中创建特定元素，具体创建方式取决于在项目创建过程中的设置。  
**注意：每一个Activity都必须在应用程序清单当中列出。Android中的四大组件，只要定义了，无论用没用，都要在AndroidManifest.xml对这个组件进行声明**  
（Android 开发的四大组件分别是：活动activity——用于表现功能；服务service——后台运行服务，不提供界面呈现；广播接受者Broadcast Receive——用于接收广播；内容提供者Content Provider——支持多个应用中存储和读取数据，相当于数据库。）

### APK文件

当我们在虚拟或者物理设备上编译并运行自己的Android应用时，Eclipse以及ADT会为我们的应用创建一个APK文件，同时将其安装在我们所使用的设备上。APK文件也就是用户们从Google Play商店中所下载的应用文件格式。

【未完待续】