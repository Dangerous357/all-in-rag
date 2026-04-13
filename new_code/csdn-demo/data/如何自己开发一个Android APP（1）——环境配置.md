# 如何自己开发一个Android APP（1）——环境配置

关于尝试做一个app的想法已经很久了，但是没有老师教，自己学到的知识也远远不够……管它呢，先慢慢做。下面应该是我在制作app过程中的一些总结和笔记，大多是从网上找的公共资源，主要是给自己看的，若有不妥的地方可以联系我。

前期准备
----

**说明：本app即将使用java语言。**  
 我的blog大概就是我学习的时间线和状态，（除了C、C++、JAVA、Python的基础知识没有电子笔记），如果你顺着我的blog看到了这里，那么你应该能跟我的进度同步，不用担心本文出现哪些超纲的部分。

### 开发环境搭建

所以开发一个app究竟需要哪些软件呢？具体步骤是什么？

#### 使用工具

**使用Eclipse+ADT+SDK开发**  
 ADT：（android development tools）安卓开发工具，用于将Eclipse和SDK建立连接。

SDK必须下载，不能只用JDK。

*据我所知途径有很多种，比较有优势的应该是使用Android Studio平台。我选择了使用Eclipse开发（没错，Eclipse是可以开发安卓程序的），因为有的方式给我的感觉过于新手，作为准程序员，还是希望能用最朴实的办法独立完成，交给自己的任务越多越好，而且Eclipse好像挺强大的，有就用着呗。*

#### 环境搭建的步骤

##### 1.下载eclipse

已经下载好了eclipse，并且配置好了jdk和jre。

##### 2.下载ADT

<https://dl.google.com/android/ADT-23.0.4.zip>  
 直接点击链接就可以下载，下载之后不要解压。  
 放到指定的文件夹中即可。

##### 3.下载SDK

<https://www.androiddevtools.cn/>

1. 在官网选择SDK工具下载SDK Tools并双击安装。安装提示SDK是依附于JDK的，所以你要确保你已经配置好你的JDK了。我自定义安装到android-sdk文件夹中。
2. 还是在官网选择SDK工具下载SDK，我下载了最新版本android 5.0（还要先下载百度网盘）。**sdk路径中不要有中文和空格！** 下载并解压后，将解压出的整个文件夹移动到你的android-sdk路径\patforms文件夹，然后打开SDK Manager，打开 Tools菜单，选择 Options菜单项，打开Android SDK Manager-Setting对话框，点击 Clear Cache(清除缓存)按钮，然后重启SDK Manager，点击Instell将打钩的组件安装（耗时很长），**记得选上最后Extras文件夹里面的Intel x86 Emulator Accelerator……**。  
    **注意：Android SDK Tools 的版本要和Android SDK Build-tools的版本对应。别盲目下载最高版本的SDK。**
3. 配置环境变量。新建环境变量名为ANDROID\_HOME的环境变量，我这里是android-sdk文件夹，然后在path中添加两条路径分别为%ANDROID\_HOME%\platform-tools和%ANDROID\_HOME%\tools。
4. 额外的一步，为了将来开启AVD做准备。在android-sdk里面找到extras，进入intel安装程序。

##### 4.配置ADT

依次点击菜单栏：help -> Install new software -> Add -> Local… ->选中ADT的文件夹。Name设置为ADT Plugin。然后一路next，最后finish，可能会弹出Warning，选择Install anyway。重启Eclipse。

##### 5.配置SDK

重启eclipse后弹出Android SDK窗口提示未启动SDK，选择Open Rreferences -> Android ->选中之前解压的 android-sdk包-> OK。

##### 6.验证ADT配置是否成功

若菜单栏出现下面这个图标，说明ADT配置成功了。  
 ![请添加图片描述](https://i-blog.csdnimg.cn/blog_migrate/34a3e1c438f51fa2690b45371915c472.jpeg)  
 如果没有出现，在eclipse中找到windows->perspective->customize perspective->Action set Availability->最左侧勾选AndroidSDK and AVD Manager(不放心就把所有Android开头的全部勾选)。

##### 7.创建AVD安卓模拟器

先打开SDK管理器清除缓存！  
 依次点击菜单栏：手机小图标 -> Creat -> 把该配置的东西配置好 -> OK -> start。（设备管理里面可以添加新设备使用哦！但是屏幕尺寸有限制不能超过某一值）  
 [【转】Android 创建AVD各参数详解](https://www.cnblogs.com/xuan52rock/p/7478785.html)   
 要开启安卓模拟器，必须关闭hyper-v。彻底关闭/开启hyper-v的方法：

1. 快捷键win+x，使用管理员权限打开Windows Powershell；
2. 关闭：bcdedit /set hypervisorlaunchtype off
3. 开启：bcdedit /set hypervisorlaunchtype auto

##### 8. 下载Genymotion模拟器（选看）

因为我AVD刚开始总报错，所以我也下载了Genymotion。  
 下载步骤附链接[Genymotion模拟器安装](https://www.runoob.com/w3cnote/android-tutorial-genymotion-install.html)  
 因为这个教程可能年代比较久远，和实际下载过程不太一样，但是核心是一样的，按照这个参考安装即可！  
 附链接[Android历史版本](https://www.jianshu.com/p/55564314cac0)  
 **搞好自己的模拟机之后，重启。**

#### 简单使用

1. 在eclipse新建一个Android Application Project。  
    ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/003feaf44d99925d264f3f6ff4b5a617.png)  
    注意最低版本要选择Android4.0及以上，否则可能会报错。  
    参考来源：[Android异常：No resource found that matches the given name 'Theme.AppCompat.Light’解决方法](https://blog.csdn.net/qq_36135335/article/details/82996340)
2. 创建好之后点击安卓图标启动模拟器，软件就在手机里了（可能需要预先通过编译）。
3. 也可以通过运行项目启动AVD。在eclipse的运行按钮中选择Run configurations，在该项目右侧对应的Target（目标）选项卡中选择每次启动应用程序的设备，即可通过AVD启动该项目。下次直接点击运行按钮，程序会按照上一次运行的方法运行，无需再次配置。

参考来源：[怎样用eclipse新建一个android项目？用eclipse新建android项目出错？请看下面](https://blog.csdn.net/hyh17808770899/article/details/105436207/)

---

参考来源：  
 [Android->怎么配置ADT&配置了没有安卓图标怎么办](https://blog.csdn.net/weixin_30682127/article/details/96442090)  
 [打开Eclipse报错：发现了以元素 ‘d:skin’ 开头的无效内容。此处不应含有子元素。 解决方案](https://blog.csdn.net/ermua/article/details/79215706)