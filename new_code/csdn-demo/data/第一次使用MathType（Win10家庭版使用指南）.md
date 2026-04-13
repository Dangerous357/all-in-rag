# 第一次使用MathType（Win10家庭版使用指南）

win10家庭版进！！！
------------

你看到这篇文章的时候，一定已经得到了MathType软件的安装包
--------------------------------

**MathType功能简介**（我自己说的）：为了在word里添加公式，不管在哪台电脑，哪个版本的word，都可以随时编辑。如果在新版本word里直接插入公式，用兼容模式打开后，公式基本上都会变成图片，无法再编辑（而且非常容易丢失），所以我们的老师要求使用MathType（可以看成是word插件）。

**（安装路径随便）**

**使用界面如下**：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7b5165459319af3a7f6a288827a209e0.png)

### 一、如果你没有安装任何版本的Word，看这里

**听我的，先装MathType，再装Word，这样当你打开word的时候，MathType已经在菜单栏上了。**  
 后面的内容已经不需要看了，直接使用即可。  
 （word安装包我没有，找我也没用）

---

### 二、如果你使用自带的Word，看这里

因为在word之后安装MathType，它应该是不会装载在word菜单栏的。（如果有，当我没说）

#### 1. 如果你只需要简单的插入公式，而不必对格式有任何要求，看这里

**step 1：插入**  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/78f8c774c8284881b47a07c369fbc8db.png)  
 **step 2：对象**  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5667e369ad486273e7aa3f8a38d0bf3e.png)  
 **setp 3：math type→确定**  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/8842187a0dd68e88f0c45f9355a452f0.png)  
 如果你没有，可能是没装上吧。  
 **step 4：插入公式**  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/442cabd993b05290c4352f512d78e7d7.png)  
 第一次打开的math type工具栏字体非常小，可以在“参数”→“工作区参数”设置：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3f85543ff2240191e688ff2b344cd66b.png)

#### 2. 如果你想用更多功能（像我前面放的图），看这里

**操作系统：win10家庭版**  
 为什么一定要强调操作系统版本，因为我的使用之路非常曲折！win10家庭版和好多windows系列的功能都不太一样。百度无果……  
 **我这里word版本是2019，仅供参考**

以下是网上常见的两种方法

##### （1）选择加载项

**只能针对你打开的某一个文档手动配置，而不是所有的word文档都会自动配置上。也就是说每一个文件都要自己配置一次。**（如果你只配置一次就全部适用，当我没说）  
 好处：装载math type后，word打开的非常慢，会变得很卡。在不需要公式的文件中，根本没必要。  
 坏处：显然，太麻烦了。如果你在很多文件中都需要添加公式……

*——原因在文末——*

**step 1**：左上角“文件”→“选项”  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/de54a88fcc9e98d5b05ee227748c2798.png)  
 **step 2**： “加载项”→“管理”中选择“模板”→“转到”  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/dc9f95e96eb3f5bef6e439be87f19ff9.png)  
 **step 3**：添加文档模板：“选用模板”

在你的安装路径中，在子目录中的文件

```
MathType\Office Support\MathType Commands 6 For Word.dotm
```

如果不行，试试在你的安装路径中，在子目录中的文件

```
MathType\Office Support\MathType Commands 6 For Word.dot
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/aaf5b39c41706b1f216689e0e4b15d71.png)

**step 4**：添加共用加载项：“添加”  
 在你的安装路径中，在子目录中的文件 `\MathType\MathPage\MathPage.wll`  
 如果找不到，把文件格式后面选成“所有文件”即可，如下：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5e5f604f4611c14868b2f8472e2532ac.png)  
 **step 5**：“确定”  
 确定之后，文件会有一段时间处于未响应状态，然后math type加载项就出现在菜单栏。

关闭该文件（此处点保存），再重新打开，math type还是在菜单栏，或者在菜单栏的“加载项”中，不影响使用。但是打开其他文件，是什么都没有的。

##### （2）更改Office自启动目录

很多方法表示，将Math Type中的某些文件拖到Office文件夹中的STARTUP文件夹中。  
 我告诉你，**直接放弃！**

如果你不信，非要尝试，往下看：  
 [word文档中工具栏不显示mathtype怎么处理](https://jingyan.baidu.com/article/eb9f7b6d69d084869264e876.html?qq-pf-to=pcqq.c2c)

（参考这个文章）  
 **你遇到的第一个问题应该是：**

###### 找不到office的安装目录

搜索关键词：Microsoft office word/win10家庭版/安装目录/路径/在哪里  
 **解决办法** ：  
 step 1：打开随便一个word文档  
 step 2：打开任务管理器→选中word文本，打开文件所在的位置  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d332f47a25ef79d0246e6941672eac4e.png)  
 路径应该是在这里：

```
C:\Program Files\WindowsApps\Microsoft.Office.Desktop.Word_16051.14430.20306.0_x86__8wekyb3d8bbwe\Office16
```

**你遇到的第二个问题应该是：**

###### 打不开WindowsApps文件夹

最大的问题就在这里！

1. WindowsApps文件夹是被设置为隐藏的，可以从菜单栏“查看”中，选择显示隐藏的项目。
2. 即使第一点成功。你还是没有权限打开它。右键“属性”→“安全”→“高级”，更改所有者为Users或管理员之类的，就能够成功打开了（子目录也一并更改哦）。  
    **先不要动！！继续往下看！！！**  
    ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/649626f11dde541cac35c609ba95dbfa.png)  
    ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1c3b90644d6e3b82a8dfb1454ca6cbd9.png)
3. 为什么第二点说的那么潦草，是因为第三点，最关键的一点！你已经会修改所有者和其他角色的权限了，即便你获得了管理员权限，你仍然**无法修改startup文件夹**。  
    搜索关键词：win10家庭版/word/office/自启动文件夹/srartup文件夹/访问被拒绝，需要权限/管理员权限/无法修改WindowsApp文件夹里的文件  
    要说明的一点是，不要怀疑你的权限设置步骤，是完全正确的，不信你可以在获得所有权限后随便删除一个文件夹。  
    网上说要找的什么控制面板、计算机管理、用户和组之类的，win10家庭版似乎是找不到的，不要白费力气了。

少走弯路！直接放弃的原因
------------

**为什么能删除文件，却不能修改？** 大概是系统给你的保护行为吧（为了防止我这种人随便搞坏自己的电脑）  
 **对于WindowsApp这个文件夹，即使获取管理员权限后依旧无法修改或放入文件，只能将文件夹里的文件删除。**  
 这也就解释了，为什么你设置好的加载项，只能在当前文档使用，因为office的装机目录是不容修改的。

**说明（必看）：**  
 以上是我研究百度且多次做实验发现的问题，文中提到的大部分内容是根据我的操作结果猜测得出的，仅供参考，或许有别的解决办法（至少我真的找不出来）。但我也不是凭空猜测啦，我有一些专业知识支撑的（虽然我会的不是很多）。  
 写此文的目的是：希望不要再有人像我一样浪费一整天了！！

---

*【新手笔记，欢迎指正】*