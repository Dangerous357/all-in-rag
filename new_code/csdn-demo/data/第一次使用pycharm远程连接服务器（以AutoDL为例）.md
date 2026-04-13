# 第一次使用pycharm远程连接服务器（以AutoDL为例）

### 1. 下载并安装pycharm（专业版）

关于pycharm的安装教程网上很多，考虑到版权问题我就不在这里详细讲述了。  
 注意如果要远程连接服务器**必须使用pycharm专业版**，可以免费试用30天，或者使用激活码激活。

### 2. 租服务器教程

云服务器很多，这里选择的是**AutoDL**平台。  
 关于AutoDL的使用介绍可以通过下面链接学习：  
 [AutoDL帮助文档](https://www.autodl.com/docs/)  
 [【AutoDL租用服务器在pycharm运行】视频 00:00–02:29 处有讲解](https://www.bilibili.com/video/BV1V8411H7zC/?spm_id_from=autoNext&vd_source=b9903dbe1b7c91d693351ba0e40e8aaa)  
 [【Pycharm连接远程GPU服务器跑深度学习】视频 00:00–01:48 处有讲解](https://www.bilibili.com/video/BV1s34y1t7ow/?spm_id_from=333.337.search-card.all.click&vd_source=b9903dbe1b7c91d693351ba0e40e8aaa)

重点主要了解以下几个概念或者操作步骤：

1. 租用新实例的方式（实例指的就是一个远程主机）以及涉及到的相关环境配置概念
2. 开关机和释放实例（关闭网页不会关掉主机，关机不会影响数据），以及无卡模式开机（不使用GPU，只使用一部分CPU）
3. 如何查看主机的登陆指令和密码
4. 迁移实例和保存镜像（注意迁移实例数据拷贝只能在同地区的实例之间）

*上面的术语和概念可能不太准确，主要是用于提示大概意义，自己清楚就行，也欢迎指正。*

### 3. pycharm远程连接服务器

打开AutoDL，找到租用的实例并开机，提前复制登陆指令和密码到记事本中便于后续使用。  
 ![先找到本服务器的](https://i-blog.csdnimg.cn/blog_migrate/37f62a3199bf3d11e551dfd00fc28dab.png)  
 登陆指令：

```
ssh -p 38076 root@region-1.autodl.com
```

登录密码：

```
123456
```

然后打开pycharm，File→Settings→Project:XXX(你自己的项目名字)→Python Interpreter，如下图。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/869cc7d1f72fa9b6ff6ab106dc312c5b.png)  
 单击右上方"Add Interpreter"添加新的解释器，选择"On SSH"，如下图所示。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7d2749aa60eca6a1cb36001ad8da5fc1.png)  
 在弹出的页面中输入远程主机的信息，如下图。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/82dab10530a2c999d59d6dc304bfd350.png)  
 信息在之前复制出来的**登陆指令**中查看，具体解释如下：

```
ssh -p 38076 root@region-1.autodl.com
                    ↑  对应
                    ↓
ssh -p Port(端口号) Username(用户名)@Host(主机)
```

然后点击Next，输入登陆密码，如下图。登陆密码也是之前从实例中找到的登陆密码，不是让你自己设。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4a698add41cc8c4a568190e57745dc85.png)  
 再次点击Next，到下一步，如下图：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/dc9f68db72c4c3eaa78f76e92f08c79a.png)  
 "Interpreter"指的是远程主机的编译环境，一般我使用默认的，即不需要修改。 *创建的实例中自带了miniconda3，使用miniconda编译，由于我之前没有用过anaconda，所以我也不太清楚miniconda具体怎么解释，如果和我一样可以在后续使用的过程中自行体会，不是很难。*

"Sync folders"指的是本机哪个文件目录同步到远程主机哪个文件目录。本机文件目录默认是整个项目文件，远程主机文件目录默认是新创建的随机名称的文件夹，保存在tmp文件夹内。

勾选"Automatically upload project files to the server"(自动上传项目到服务器)，这样在本地pycharm修改项目可以自动同步到远程主机，在远程主机运行。随便打一个测试文件print “hello”，注意确认编译环境是不是远程主机，运行后控制台输出如图，表示是在远程主机下运行的。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/adf69ca8f4beecead010dbe14d3018bb.png)

### \* pycharm进行ssh时报错

在远程连接的过程中出现报错`the authenticity of host can‘t be established`。*具体错误是在哪里出现的我忘了，因为这篇是我后面补写的。*

**本机** win+R输入cmd，然后按照下面的格式输入命令，替换远程主机对应的信息。

```
ssh -o StrictHostKeyChecking=no xxx 用户名@ip -p 端口号
```

例如：

```
ssh -o StrictHostKeyChecking=no root@24.54.78.56 -p 9095
```

然后关闭窗口重新进行配置即可。

### 4. pycharm的工具栏中添加“远程主机”图标

如果不使用pycharm，想使用服务器，通常要在命令行中去选择文件、编写程序、运行程序等操作，没有任何图形界面，如果对命令行尤其是linux命令行不熟悉，非常不方便。本机目录的文件可以通过远程连接的方式可视化在服务器上运行，不用使用命令行，这样更方便。服务器上的文件结构也可以像本机中一样显示出来，便于操作。

首先，打开pycharm的界面，点击菜单中 tools选项菜单。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/684f89d5973def6047642e189f1d380e.png)  
 弹出tools的下拉菜单选中 deployment 选项。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/abbb35f0545c6534df7a016d2786a377.png)  
 弹出下一级菜单选中 browse remote host 选项。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/8b58be9b22d1cb1e31617223ff99329d.png)

### 5. 使用命令行对远程主机操作

虽然能够使用Remote Host工具对远程主机中的文件进行快捷的操作，但是在使用过程中仍然无法避免直接在服务器的一些操作，比如`git clone`等，所以还是需要使用命令行。除了在AutoDL提供的命令行中进行，也可以在本地pycharm中打开远程主机的终端。如下图，点击Local后的"➕"可以添加终端，"✔️"可以选择不同的终端。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c1524c3f08c9054e180ba68d48f7da42.png)

### 6. 数据盘和系统盘的使用

AutoDL官网常见两个概念：数据盘和系统盘。对于大的数据，比如深度学习的训练数据集、训练过程中的缓存文件、tensorboard文件等，要放在数据盘中，否则会影响运行内存。如何区分数据盘和系统盘？不考虑物理结构，我们通过文件目录去区分。在`/root/autodl-tmp`下放置文件表示存储在**数据盘**，此外其他所有文件都是在系统盘中。你可以把你的数据放在该目录下。  
 如果你的代码里生成的各种文件都是在系统盘进行读写操作的，可以先在数据盘中创建好对应名字的目录，然后再在系统盘对应位置建立软连接即可。

### 7. tensorboard的使用

深度学习过程中使用了tensorboard，但是按照常规的方法无法调用，解决方法如下：

> AutoDL实例中已内置TensorBoard工具，您只需将tensorboard的event文件保存到/root/tf-logs/路径

需要将event文件保存到指定文件目录下，就可以直接通过实例里的TensorBoard查看。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/15b2263db6205df441dfabf0bd056af5.png)

**【在个人浏览器中查看远程服务器tensorboard的方法】** 在服务器终端输入：

```
tensorboard --logdir logs --port 6006 --host xx.xx.xx.xx
```

* logdir：存放文件的地址
* port：服务器用于显示tensorboard的端口，一般默认6006（注意这个端口和你连服务器的时候用的端口不一样）
* host：服务器ip

然后终端会给一个地址`http://xx.xx.xx.xx:6006/`，用浏览器打开即可。

### 8. 想更换同步文件的路径

pycharm菜单Tools→Deployment→Configuration→Mappings，在如下图处更改  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/97cdd4d2fbdb78356af1f1ebe39fef91.png)

### \* 引包出错

自己的python包，引包的时候出错提示`No module named 'lib.utils.cython_bbox'`。*自己的python包在正常使用之前要先编译，我还不会自己写python包，是用别人的代码的过程中出现的问题。*  
 错误原因是由于两个操作系统不同，在windows11编译的文件，在远程服务器Linux系统可能无法正确使用，所以要在远程服务器的终端再编译一遍。比如在我的项目中，我要进入服务器的终端，运行`setup.py build_ex`命令（具体过程略），不能在本机的终端运行，再将生成的文件同步到远程服务器。

### \* 修改代码后不能自动同步文件

发现修改代码后不能自动同步文件，原来是因为没有设置默认服务器。可以右键要修改的文件，点上传到指定服务器，也可以直接切换默认服务器。

方法一：  
 <http://www.taodudu.cc/news/show-4895180.html>

方法二：  
 <https://www.likecs.com/show-203269134.html>

### 关闭pycharm后仍然保持代码运行

连接AutoDL关闭pycharm后只要不关AutoDL的主机仍能正常运行代码，但是换成课题组的服务器，只要关掉pycharm，代码就会停止。使用会话功能可以保证关闭pycharm窗口之后，代码仍然正常在服务器运行。

1. 新建会话  
    tmux new -s 名字
2. 退出会话  
    第一步：Ctrl+B  
    第二步：D
3. 查看会话  
    tmux attach -t 名字
4. 结束会话  
    exit

### end. 参考来源

[Pycharm连接远程GPU服务器跑深度学习](https://www.bilibili.com/video/BV1s34y1t7ow/?spm_id_from=333.337.search-card.all.click&vd_source=b9903dbe1b7c91d693351ba0e40e8aaa)  
 [AutoDL租用服务器在pycharm运行](https://www.bilibili.com/video/BV1V8411H7zC/?spm_id_from=autoNext&vd_source=b9903dbe1b7c91d693351ba0e40e8aaa)  
 [pycharm连接到远程服务器（啰嗦版，有基础的不用听，适合正在到处搜索资料的…](https://www.bilibili.com/video/BV1WZ4y1i7jc/?spm_id_from=333.337.search-card.all.click&vd_source=b9903dbe1b7c91d693351ba0e40e8aaa)  
 [Pycharm连接远程GPU服务器跑YOLOV6(训练）](https://www.bilibili.com/video/BV1K24y1Q7k5/?spm_id_from=autoNext&vd_source=b9903dbe1b7c91d693351ba0e40e8aaa)  
 [pycharm 添加远程项目interpreter 报 the authenticity of host can‘t be established 解决方法](https://blog.csdn.net/weixin_44190201/article/details/127102169)  
 [pycharm怎么浏览远端主机服务器代码](https://jingyan.baidu.com/article/48a4205720a577a9242504b8.html)  
 [AutoDL帮助文档](https://www.autodl.com/docs/)  
 [Fast R-CNN训练自己的数据集时遇到的报错及解决方案](https://www.shuzhiduo.com/A/kPzOnlx7dx/)  
 [服务器运行Tensorboard本地查看的方法](https://zhuanlan.zhihu.com/p/555311181)

---

 欢迎指正