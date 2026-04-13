# 如何自己开发一个Android APP（7）——发布

### 版本

需要为自己的应用程序设置一个版本号并为其命名。这部分信息应该被包含在根manifest元素中manifest下的android:versionCode与android:versionName属性当中。

versionCode属性应该为一个整数，且每一个应用程序新版本分配到的数字都需要比前一个更大。可以随意选择自己想要的数字，只要比上一个版本数值更大即可。终端用户无法看到应用程序的版本代码值，该数值仅用于在发布过程中衡量应用程序的当前版本号是否比原先已经安装的版本更新。

versionName属性是一个可被终端用户查看的字符串。版本名称并不需要一定与版本代码相匹配，但从逻辑上讲其同样应该遵循递进关系。举例来说，从1.0开始，接下来应该是1.1，当我们发布的新内容更新幅度较大时则将其提升为2.0。

### 签名

要在Android系统上安装一款应用程序，该应用必须利用具备私有密钥的证书进行签名验证。

在Android应用程序的创建过程中，系统会选择debug或者release两种模式之一进行创建。在release模式下，需要利用自己的私有密钥完成应用程序签名。也可以利用keytool程序为自己的应用程序生成一个密钥，在Java Development Kit（或者简称为JDK）当中能够找到该程序。在为私有密钥创建了keystore之后，即可选择alias name以及password，从而在日后进行应用程序签名时加以使用。

在JDK 1.4以后的版本中都包含了这一工具，它的位置为%JAVA\_HOME%\bin\keytool.exe。创建证书主要是使用" -genkeypair"，该命令的可用参数如下Cmd代码举例生成一个名称为test1的证书：

```
 keytool -genkeypair -alias "test1" -keyalg "RSA" -keystore "test.keystore"
```

功能：  
 创建一个别名为test1的证书，该证书存放在名为test.keystore的密钥库中，若test.keystore密钥库不存在则创建。

参数说明：

* genkeypair：生成一对非对称密钥;
* alias：指定密钥对的别名，该别名是公开的;
* keyalg：指定加密算法，本例中的采用通用的RAS加密算法;
* keystore：密钥库的路径及名称，不指定的话，默认在操作系统的用户目录下生成一个".keystore"的文件。

注意：

1. 密钥库的密码至少必须6个字符，可以是纯数字或者字母或者数字和字母的组合等等。
2. "名字与姓氏"应该是输入域名，而不是我们的个人姓名，其他的可以不填。
3. 执行完上述命令后，在操作系统的用户目录下生成了一个"test.keystore"的文件。如果希望用户无缝升级到新的版本，那么必须用同一个证书进行签名。这是由于只有以同一个证书签名，系统才会允许安装升级的应用程序。如果你采用了不同的证书，那么系统会要求你的应用程序采用不同的包名称，在这种情况下相当于安装了一个全新的应用程序。如果想升级应用程序，签名证书要相同，包名称要相同！

**创建一个发布版本：**

* 在Eclipse当中，通过Package Explorer选中自己的应用程序项目，右键点击该项目或者选择“File”、“Export”。展开其Android文件夹后，选择“Export Android Application”并点击“Next”。  
   ![16.1export_project](https://i-blog.csdnimg.cn/blog_migrate/9345775db643a7eac4f94cb4ad7f9581.png)  
   Eclipse将突出显示创建过程中所遇到的全部错误信息，全部解决才能继续进行下一步。点击“Next”继续。
* 在Keystore Selection容器中，浏览至我们的keystore文件并为其输入密码。接下来，从菜单中选择我们为密钥指定的alias并输入自己设定的密码内容。点击“Next”进入下一步。  
   ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4d765403b78b084a5df276edd095974e.png)
* 选择一个位置并为我们应用程序的APK文件指定一个名称，该APK文件也就是我们将要上传到Google Play商店中的文件。在点击“Finish”之后，该APK文件就会出现在所选定的保存位置。现在我们应该已经可以将该APK文件复制到Android设备上了。在复制工作完成之后，利用文件管理器应用选择该APK文件，并依据说明进行安装。

### 发布

其他
--

### 反编译apk

#### 获取图片素材

下载apk文件，重命名将后缀名改为.zip，然后解压。解压得到文件夹，进入res目录即可获取图片文件资源。

#### 获取代码

**工具准备：**

* apktool：获取资源文件，提取图片文件，布局文件，还有一些XML的资源文件
* dex2jar：将APK反编译成Java源码(将classes.dex转化为jar文件)
* jd-gui：查看2中转换后的jar文件，即查看Java文件

具体参考这个吧……我还没有用到反编译这步。 [反编译APK获取代码&资源](https://www.runoob.com/w3cnote/android-tutorial-decompile-apk-get-code-resources.html)

问题参考
----

[Reasons for receiving “RadioGroup is not applicable for the arguments”](https://stackoverflow.com/questions/15761597/reasons-for-receiving-radiogroup-is-not-applicable-for-the-arguments)

[setTextColor()的参数设置方式](https://blog.csdn.net/chiuan/article/details/7058686)

[Android RadioButton设置选中时文字和背景颜色同时改变](https://blog.csdn.net/liuwan1992/article/details/52688408)

[keytool使用方法总结](https://blog.csdn.net/dzyj211/article/details/52705455)

【未完待续】