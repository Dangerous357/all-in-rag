# 第一次使用PyCharm写C++（失败）

前言：  
 由于我已经非常习惯使用PyCharm远程连接服务器了，我认为非常方便，所以希望C++也能直接用Pycharm。于是尝试在PyCharm上部署C++环境。

但是，我失败了。如果您知道问题所在，欢迎给我留言。我认为Pycharm并没有编译C/C++的功能，因此希望看到这篇文章后能转换思路，少走弯路。

### step1 下载PyCharm

我的PyCharm版本是PyCharm 2024.1.4 (Professional Edition)，直接从官网下载即可，这里无详细教程。

### step2 安装C/C++编译器

下载地址：<https://sourceforge.net/projects/mingw-w64/files/mingw-w64/mingw-w64-release/>  
 下拉到页面最下方，选择`x86_64_win32_seh`。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/15c4564cfe6f49a786a6f329cac14ce4.png)  
 它会自动跳转到新的页面开始下载，但是下载速度很慢。点`Problems Downloading`：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/8e116a50d95d4fadad717cb568c0fee3.png)  
 弹出下面的窗口，点击蓝色字体下载。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/f48b9dfe4203402dadb070bc95d03507.png)  
 最后得到的压缩包是`x86_64-91.0-release-win32-seh-rt_v6-rev0.7z`。我解压后的路径为`D:\mingw64`：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/546cdb3975a84b4280fceeeddd5e90fe.png)  
 设置环境变量，新建一个名为MingGW的用户变量，地址为bin目录，如下图：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e3726a2a9b4847b3afe032adf6f2d3be.png)  
 同理，然后再将`D:\mingw64\bin`添加到系统变量的path中。

打开命令行，输入gcc -v，出现如下图版本号即为安装成功。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/1f18d3091e0944c7b97e768489fa24a4.png)

### step3 在PyCharm中配置

打开PyCharm -> Settings  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/ea5ea9121d694e758cd0215f6909f2bf.png)  
 在Python Interpreter窗口右上方选择Interpreter，如下图，下拉菜单中选择Show All。但是显然我这里选择的只能是Python的编译器，而且按照网上在Settings -> Language& Frameworks中选择C/C++的方法，也没有找到C/C++。在Settings -> Plugins中我只搜索到一个名为New Executabe C/C++的插件，似乎和网上的教程中说的C/C++C插件不一样。至此，我无法使用PyCharm成功编译C++。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/9e2e7f8e9b9c40358bab0f4983a418db.png)

### 参考来源：

[MinGW安装与环境配置（Window）](https://zhuanlan.zhihu.com/p/690958462)  
 [探索PyCharm的C/C++支持：一站式配置指南](https://blog.csdn.net/2401_85339615/article/details/140912361?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522172483509716800178554453%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=172483509716800178554453&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~baidu_landing_v2~default-1-140912361-null-null.142%5Ev100%5Epc_search_result_base5&utm_term=pycharm%E9%85%8D%E7%BD%AEc%2b%2b&spm=1018.2226.3001.4187)  
 [pycharm配置c/c++环境](https://wenku.csdn.net/answer/37tixxoymz)