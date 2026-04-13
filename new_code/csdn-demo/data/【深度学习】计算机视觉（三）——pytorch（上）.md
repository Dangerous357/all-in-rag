# 【深度学习】计算机视觉（三）——pytorch（上）

> PyTorch是一个[开源](https://baike.baidu.com/item/%E5%BC%80%E6%BA%90/246339 "开源")的[Python](https://baike.baidu.com/item/Python "Python")机器学习库，基于Torch，用于自然语言处理等应用程序。

深度学习通常是使用GPU实现，如何理解CPU和GPU？

> CPU擅长逻辑控制，是串行计算，而GPU擅长高强度计算，是并行计算。
>
> 打个比方，GPU就像成千上万的苦力，每个人干的都是类似的苦力活，相互之间没有依赖，都是独立的，简单的人多力量大；CPU就像包工头，虽然也能干苦力的活，但是人少，所以一般负责任务分配，人员调度等工作。

安装
--

我看到有人说“为了防止冲突，pytorch安装自带cuda runtime。所以不需要下载Cuda单纯下载pytorch就可以使用GPU计算了。” 我是安装完cuda才看到的这句话，那么你可以直接跳到“安装pytorch”部分试试。如果你希望中途不出任何错误，那么你需要按部就班往下走。

![](https://i-blog.csdnimg.cn/blog_migrate/c0aebb461a60829e9cb902377e701408.png)

别管为什么，跟着做：

首先要看一下这个表，根据你的python版本找到可以安装的torch和torchvision范围，记住它。

然后打开这个：[https://download.pytorch.org/whl/torch\_stable.html](https://download.pytorch.org/whl/torch_stable.html "https://download.pytorch.org/whl/torch_stable.html")，找到你的torch对应的cuda版本范围，记住它。如果不会找，可以参考后面“安装pytorch”，里面有讲参数含义。

然后你根据本文“安装cuda”步骤进行操作，在此过程中你可以查询到你电脑限制安装的最高cuda版本，如果这个cuda版本低于你刚才查到的cuda版本最小值，那就需要**升级你的NIVIDA**！如果你不需要升级，那么可以跳过“升级NVIDIA”，否则你就要看了。

你猜我是怎么知道的！（哭）

### 升级NVIDIA驱动（选看）

在开始菜单找到GEFORCE EXPERIENCE软件，打开并登陆账户。

![](https://i-blog.csdnimg.cn/blog_migrate/7cee85e3a87e1c022679ef9ad6802048.png)

按照上图检查更新，并更新驱动GeForce Game Ready Driver。如果更新失败，提示“无法继续安装”、“出现一个错误”，说明你的GeForce Experience软件版本低，我没有找到直接升级的办法，所以先卸载再安装。打开控制面板→程序，卸载你已有的GeForce Experience，然后在NVIDIA官网下载新的GeForce Experience并安装。注意安装的时候要**以管理员身份**，并且**关闭你所有的电脑管家、安全卫士、杀毒软件**，不然会报错！

[GeForce Experience下载![](https://csdnimg.cn/release/blog_editor_html/release2.3.8/ckeditor/plugins/CsdnLink/icons/icon-default.png?t=P1C7)https://www.nvidia.cn/geforce/geforce-experience/](https://www.nvidia.cn/geforce/geforce-experience/ "GeForce Experience下载")

![](https://i-blog.csdnimg.cn/blog_migrate/7b8be560319c47ed18a16583873cac68.png)

（截至目前，软件版本已经到3.25.1.27了，如果你的小于这个，那毫无疑问是要升级的）

安装完驱动之后就好了。

![](https://i-blog.csdnimg.cn/blog_migrate/2a4f716926c85215c42d112009361a6c.png)

### 安装CUDA

> CUDA（Compute Unified Device Architecture），是显卡厂商[NVIDIA](https://baike.baidu.com/item/NVIDIA "NVIDIA")推出的运算平台。 CUDA™是一种由NVIDIA推出的通用[并行计算](https://baike.baidu.com/item/%E5%B9%B6%E8%A1%8C%E8%AE%A1%E7%AE%97/113443 "并行计算")架构，该架构使[GPU](https://baike.baidu.com/item/GPU "GPU")能够解决复杂的计算问题。
>
> CUDA 是 NVIDIA 发明的一种并行计算平台和编程模型。它通过利用图形处理器 (GPU) 的处理能力，可大幅提升计算性能。

我的环境：

* Windows11家庭版
* NVIDIA GeForce MX250
* cuda11.3.1版本。
* cuDNN v8.4.0 (April 1st, 2022), for CUDA 11.x
* torch1.10.2
* torchvision0.11.3

**step1：**

右键开始菜单，选择设备管理器→显示适配器，查看是否有独立的NVIDIA显卡。

![](https://i-blog.csdnimg.cn/blog_migrate/40716cef93e6479c72d9fe9fc603927f.png)

从任务栏右边打开NVIDIA设置：

![](https://i-blog.csdnimg.cn/blog_migrate/6b0f8895db0441f1eb91247c9f5999b4.png)

 选择左下角“系统信息”，查看驱动程序版本。

![](https://i-blog.csdnimg.cn/blog_migrate/8ce0651fe184a1999b7892376e6ad441.png)

继续，点击“组件”，3D设置中第三行NVCUDA.DLL的产品名称表示最高支持的CUDA版本。

![](https://i-blog.csdnimg.cn/blog_migrate/054f0feb612e7b1b5d267d97055ed23b.png)

**step2：**

安装CUDA，以CUDA 10.0为例 。（注意如果你这里显示的版本非常新，建议安装稍微低一点的版本，因为相关资源比较难找）为什么以cuda10.0为例，因为我第一次装错了，但是别的版本都大同小异，举一反三就好。

下载链接：[cuda-toolkit-archive](https://developer.nvidia.com/cuda-toolkit-archive "cuda-toolkit-archive")

![](https://i-blog.csdnimg.cn/blog_migrate/c4661e260c2ab45a115299893dbbb3b9.png)

按照如上所述选择target platform后下载。

下载好安装文件后，双击打开。弹出对话框选择解压路径，新建一个空白文件夹用于存放临时解压目录，安装完成之后会自动删除。解压好之后选择精简安装，如果需要更改安装路径，要选择自定义安装。参考文章的作者提示：“由于VS的原因，导致无法正常安装，于是我换成了自定义的安装方式，并将VS勾给去掉，便可以正常安装了”。我选择了精简安装。

由于我新建的文件夹消失了，不知道它安装到哪里去了，可以用win+r进入cmd验证。使用**nvcc -V**可以查看版本，使用**set cuda**可以查看安装路径，如图。

![](https://i-blog.csdnimg.cn/blog_migrate/fb2e6a56d314da13a8c629e1bd584474.png)

**step3：**

设置环境变量。要添加的变量如下：

![](https://i-blog.csdnimg.cn/blog_migrate/f8ca974550ea9d1eaf06cd34cf70b397.png)

注意这里是默认安装目录，需要修改变量值为你安装的目录。注意区分ProgramData和Program Files文件夹，这两个文件夹配置环境变量的时候都会用到。

![](https://i-blog.csdnimg.cn/blog_migrate/968e8e69f7dc2004f321e91d47578724.png)

![](https://i-blog.csdnimg.cn/blog_migrate/8a506594a084f7088f3e74e129e72571.png)

![](https://i-blog.csdnimg.cn/blog_migrate/b498c509384e05df532fe8a608e72eaf.png)

![](https://i-blog.csdnimg.cn/blog_migrate/a59715a20c68219b83d2a2dce70200b2.png)

即配置为（有相同的可以直接复制）：

CUDA\_SDK\_PATH = C:\ProgramData\NVIDIA Corporation\CUDA Samples\v11.3  
 CUDA\_LIB\_PATH = %CUDA\_PATH%\lib\x64  
 CUDA\_BIN\_PATH = %CUDA\_PATH%\bin  
 CUDA\_SDK\_BIN\_PATH = %CUDA\_SDK\_PATH%\bin\win64  
 CUDA\_SDK\_LIB\_PATH = %CUDA\_SDK\_PATH%\common\lib\x64

然后在系统变量path中新建（橘色部分注意更改成你的自定义路径）：

%CUDA\_LIB\_PATH%

%CUDA\_BIN\_PATH%

%CUDA\_SDK\_LIB\_PATH%

%CUDA\_SDK\_BIN\_PATH%

C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.3\lib\x64

C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.3\bin

C:\ProgramData\NVIDIA Corporation\CUDA Samples\v11.3\common\lib\x64

C:\ProgramData\NVIDIA Corporation\CUDA Samples\v11.3\bin\win64

添加好的path环境变量如下：

![](https://i-blog.csdnimg.cn/blog_migrate/bdb0a1ff2c39dd64e25fcae4142fa4c0.png)

 完成之后，win+r进入cmd，验证是否配置成功。

使用cd命令进入安装目录，然后再进入extras文件夹。

![](https://i-blog.csdnimg.cn/blog_migrate/3d0e5ac5d933d04eff414c9a14109fd9.png)

 再进入demo\_suite文件夹，执行bandwidthTest.exe：

![](https://i-blog.csdnimg.cn/blog_migrate/67ca8d33e60cd19e1647a507248bc7c5.png)

可以看到倒数第二行**Result = PASS** 。然后再执行deviceQuery.exe：

![](https://i-blog.csdnimg.cn/blog_migrate/06ec11d254912bcd6f9860dfac518d1f.png)

可以看到最后有**Result = PASS** 。说明配置成功。

### 安装cudnn

> cuDNN（CUDA Deep Neural Network library）：是NVIDIA打造的针对深度神经网络的加速库，是一个用于深层神经网络的GPU加速库。如果你要用GPU训练模型，cuDNN不是必须的，但是一般会采用这个加速库。

下载链接：[cuDNN Archive![](https://csdnimg.cn/release/blog_editor_html/release2.3.8/ckeditor/plugins/CsdnLink/icons/icon-default.png?t=P1C7)https://developer.nvidia.com/rdp/cudnn-archive#a-collapse742-10](https://developer.nvidia.com/rdp/cudnn-archive#a-collapse742-10 "cuDNN Archive")

注意cuDNN的版本要和CUDA对应，我的cuda是v11.3，所以我下载cuDNN v8.4.0 (April 1st, 2022), for CUDA 11.x。

![](https://i-blog.csdnimg.cn/blog_migrate/ed05c0257046903541f80b326ba7baef.png)

安装需要登陆NVIDIA账号，因为我之前注册过了，所以我直接登陆就可以。随便下载到什么地方，然后把下载的压缩包解压。打开解压目录，可以看到有bin文件夹、lib文件夹、include文件夹、还有一个文本文件。然后再打开cuda的安装目录，找到对应的这几个文件夹，把cudnn解压目录中文件夹里面对应的文件，复制到cuda对应文件夹下（这里说的有点绕，假设cudnn的bin文件夹里面有一个文件cudnn64\_8.dll，就把这个文件复制到cuda的bin文件夹下，以此类推，lib和include也是如此）。然后刚才的解压目录就可以删掉了。

### 安装pytorch

我之前作死把anaconda卸载了，我下面试试pip安装（听说根本装不上）。

**下载安装库文件：**

因为PyTorch官网下载很慢而且频繁报错，所以我选择先下载到本地，然后本地安装。（不使用国内镜像源的原因是，国内镜像源提供的torch都是使用CPU的，我们需要的是GPU）。

下载链接：

[torch\_stable![](https://csdnimg.cn/release/blog_editor_html/release2.3.8/ckeditor/plugins/CsdnLink/icons/icon-default.png?t=P1C7)https://download.pytorch.org/whl/torch\_stable.html](https://download.pytorch.org/whl/torch_stable.html "torch_stable")

记得刚开始让你记住的torch和torchvision版本吗？下载对应的两个文件。此处我选择的是：

* cu113/torch-1.10.2%2Bcu113-cp39-cp39-win\_amd64.whl
* cu113/torchvision-0.11.3%2Bcu113-cp39-cp39-win\_amd64.whl

注意看文件名，第一部分是cpu代表的就是CPU版本，如果是cuxxx（xxx是对应的版本号）就是CUDA；第二部分是torch或torchvision的版本号；第三部分cp39，是对应的python版本python3.9，注意不要选错；第四部分是对应的操作系统。

**安装：**

下载好两个文件之后，使用pip安装。使用pip安装本地文件时，需要进入到文件所在的目录，但是使用pip也需要在pip所在的目录，当两个目录不一样时，我们可以把pip所在的目录添加到系统的环境变量上，这样无论在哪里都可以使用pip命令了。

进入到文件的保存位置，分别使用下面的命令安装（注意先安装torch）：

* pip install torch-1.10.2+cu113-cp39-cp39-win\_amd64.whl
* pip install torchvision-0.11.3+cu113-cp39-cp39-win\_amd64.whl

使用pip list查看已经安装的库，可以看到安装成功。

![](https://i-blog.csdnimg.cn/blog_migrate/77605ae7f3fa2729bc4d7e24e2283806.png)

 安装和配置python包的方法可以参考我之前的笔记：[在pycharm用python画图：matplotlib](https://blog.csdn.net/RK_Dangerous/article/details/125056104 "在pycharm用python画图：matplotlib")

然后打开pycharm，把torch和torchvision加进来，然后**import torch**没有报错。

```
print(torch.cuda.is_available())
```

输出True说明可以使用cuda啦。

至此，全部安装成功。

pytorch是基于torch的机器学习库，因为和torch所用的语言不一样，所以我们下载的torch实际上是用python作为torch的接口，而torchvision可以理解为为了更好地使用torch，去针对计算机视觉方面单独创建的库，在pytorch名下。

基础学习
----

首先介绍两个实用的函数：

**dir()**：打开。例如，打开一个库，你可以看到库里的内容。

**help()**：帮助，查看帮助文档。

```
import torch
# print(torch.cuda.is_available())
# 打开torch，里面有AVG
print(dir(torch))
# 再打开AVG，里面有SUM
print(dir(torch.AVG))  # 注意带有前后双下划线的变量是没办法篡改的，有这个说明AVG是一个函数，里面的东西不能再打开了
# 用help看一下AVG
print(help(torch.AVG))  # 注意使用help时，函数后面的括号不写，即不需要写成AVG()
```

![](https://i-blog.csdnimg.cn/blog_migrate/da1dd225dcd15620d2b9d1d48887f08c.png)

### 数据集

深度学习需要数据集，数据集通常是由图片和它的标签构成的。而数据集的组织形式一般有三种方式：

1. 以文件夹名为标签，将标签所对应的图片放入文件夹中。
2. 将图片和标签分开两个文件夹。图片文件夹中，给图片有序地重命名；标签文件夹中，对应每个图片新建一个txt文件，命名为对应图片的序号，txt文件中存放具体信息。
3. 直接将图片重命名为标签。

#### 读取图片

**使用PIL.Image读取图片**

读取图片可以用**PIL**包，不知道为什么我已经有这个包了，可能是我之前下载过？或者是安装自带的？

因为初学，我拿npy的照片简单做一下数据集，分为唱歌的阿黄和不唱歌的阿黄两种。学到后面才发现会有一些调整照片格式的操作，**不是故意恶搞**。

把数据集文件夹放在项目里面，复制粘贴就可以，像这样：

![](https://i-blog.csdnimg.cn/blog_migrate/27f06a9b67f5c9d3bf4177de414b4080.png)

现在需要用到所需图片的路径。以第一张图片为例，右键复制路径，注意区分**Copy Absolute Path**（复制绝对路径）和**Copy Relative Path**（复制相对路径）。注意绝对路径**Windows中‘ \ ’ 要用‘ \\ ’转义**或**在字符串前加r取消转义**。

```
from PIL import Image

img_path = "hzhfData/NotSing/100.jpg"  # 第一步先设置好图片路径
img = Image.open(img_path)  # 第二步获得图片
img.show()  # show()可以显示图片
```

![](https://i-blog.csdnimg.cn/blog_migrate/c0f57143b862dafe2ed511fcfd1a1634.png)

如果需要读取文件夹中的所有图片，需要知道每一个图片的路径。手动输入和设置肯定很麻烦，我们可以批量获取。

```
import os

dir_path = "hzhfData/NotSing"  # 第一步先设置好文件夹路径
"""
# 文件夹的路径也可以更层次地组织
root_dir = "hzhfData"
label_dir = "NotSing"
dir_path = os.path.join(root_dir, label_dir)  # os.path.join()的作用是把两个路径连接起来
"""
# 使用os.listdir()，作用是将文件夹里的内容变成一个列表
img_path_list = os.listdir(dir_path)  # 得到的列表是图片的全称（字符串）组成的
print(img_path_list[3])
```

![](https://i-blog.csdnimg.cn/blog_migrate/b3488f101a14028dc40aa02fa9d3df31.png)

如此，将得到的字符串与文件夹路径拼接起来就得到了图片的完整路径。

**使用cv2.imread()读取文件**

这个用到的是OpenCV，它的功能非常强大，后续会讲解。

#### Dataset类

Dataset类用于找出数据集中的某类数据和它的标签，这些图片有从0到n-1的序号，并提供找出的数据总数。

```
from PIL import Image
import os
# 引包
from torch.utils.data import Dataset


# 新建一个MyData类继承Dataset
class MyData(Dataset):
    # __init__是创建一个实例时要运行的函数
    def __init__(self, root_dir, label_dir):
        self.root_dir = root_dir  # self.root_dir创建的是全局变量
        self.label_dir = label_dir
        self.path = os.path.join(self.root_dir, self.label_dir)
        self.img_path = os.listdir(self.path)  # 获得了label_dir文件夹下的所有图片名字列表

    # 重写父类Dataset的__getitem__(self, item)方法，参数idx是图片在列表中的位置（0，1，……，n-1）
    def __getitem__(self, idx):
        img_name = self.img_path[idx]
        img_item_path = os.path.join(self.path, img_name)  # 这里就获得了某一个图片的完整路径
        img = Image.open(img_item_path)  # 获得了图片
        return img, self.label_dir  # 这个函数需要返回img和label

    # 重写父类Dataset的__len__(self)方法
    def __len__(self):
        return len(self.img_path)  # 返回数据数量，就是图片名字列表的长度

root_dir = "hzhfData"
NotSing_label_dir = "NotSing"
Sing_label_dir = "Sing"
NotSing_dataset = MyData(root_dir, NotSing_label_dir)
Sing_dataset = MyData(root_dir, Sing_label_dir)
# 魔法方法：
img, label = Sing_dataset[0]  # 当实例对象做p[key]运算时，会调用类中的方法__getitem__
"""
魔法方法是在Python的类中被双下划线前后包围的方法,如常见的 :init、new、__del__等。
这些方法在类或对象进行特定的操作时会自动被调用,我们可以使用或重写这些魔法方法,给自定义的类添加各种特殊的功能来满足自己的需求。
"""
print(label)
img.show()

img, label = NotSing_dataset[0]
print(label)
img.show()

train_dataset = NotSing_dataset + Sing_dataset  # 可以把两个数据集拼接，数据的顺序也相应拼接
img, label = train_dataset[4]
print(label)
img, label = train_dataset[5]
print(label)
```

![](https://i-blog.csdnimg.cn/blog_migrate/dae7fffd5a911731e15b78fcf5fe1377.png)

### Tensorboard

> Tensorboard原本是Google [TensorFlow](https://so.csdn.net/so/search?q=TensorFlow&spm=1001.2101.3001.7020 "TensorFlow")的可视化工具，可以用于记录训练数据、评估数据、网络结构、图像等，并且可以在web上展示，对于观察神经网络的过程非常有帮助。PyTorch也推出了自己的可视化工具。

直接用可能会报错，需要安装一下。使用pip install tensorboard，方法不再赘述。

引包：

from torch.utils.tensorboard import SummaryWriter

#### **SummaryWriter.add\_scalar()**

怎么说呢，它生成的东西具体我也说不清楚，但是你看完使用介绍之后就大概了解了。

```
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter("logs")  # 一般固定就这么写

# writer.add_scalar()  # 添加一个标量数据
"""
add_scalar(self, tag, scalar_value, global_step=None, walltime=None)

重要参数说明：
tag：标题
scalar_value：y轴
global_step：x轴
"""
# 举个例子
for i in range(100):
    writer.add_scalar("y=x", i, i)
"""
注意修改参数的时候，如果不改tag，只改了后面的值，图像会在原来的基础上绘制并有一些奇怪的变化
如果必须这样操作的时候，建议删掉之前的logs文件
"""

writer.close()  # 也是固定的
```

运行之后，左侧侧边栏的文件目录中会多出一个名为logs的文件夹，如下：

![](https://i-blog.csdnimg.cn/blog_migrate/3641c744b393f0b72693c9ffe648beb5.png)

 如何打开logs文件夹？在pycharm的控制台中输入tensorboard --logdir=logs，这里logdir="事件文件所在文件夹名"。

![](https://i-blog.csdnimg.cn/blog_migrate/e1a5628dee221b063550fef3ed1070fa.png)

 可以看到最后一行有一个链接，其中localhost:6006是访问用的端口名。（如果一台服务器有很多人同时使用，为了避免端口一样，可以通过tensorboard --logdir=logs --port=6007更改端口。）点击链接就可以看到了：

![](https://i-blog.csdnimg.cn/blog_migrate/fe6534f12e50ff4c998c161d64b02b7c.png)

 （看到学习视频的弹幕中有很多人说没有数据，可以试试把logs加上绝对路径。）

小tips：我安装了腾讯电脑管家，会拦截tensorboard.exe，我有一次手滑点成了阻止（永不询问），然后就再也打不开了，每次都关掉腾讯电脑管家肯定很麻烦，我想办法再重新启用。

![](https://i-blog.csdnimg.cn/blog_migrate/ba230b0f2ed93077cffbc5edc413f6b5.png)

 如何取消腾讯电脑管家的拦截？我找了很久终于解决了。就在首页体检处！

![](https://i-blog.csdnimg.cn/blog_migrate/99ea58d280a1681e6ac7f3ecaf307dbf.png)

打开这个猎鹰全景防御，可以在防护记录中看到你手滑的那次操作，然后在信任管理中找到tensorboard.exe操作一下就可以啦。

![](https://i-blog.csdnimg.cn/blog_migrate/089db1510f0acfcb3e88c985ec27b1bb.png)

#### **SummaryWriter.add\_image()**

add\_image()与上面类似，它记录的是一个图片。用处暂时不知道，但是可以先了解一下怎么用。

```
from torch.utils.tensorboard import SummaryWriter
from PIL import Image
import numpy as np

writer = SummaryWriter("logs")  # 一般固定就这么写

# writer.add_image()  # 添加图片
"""
add_image(self, tag, img_tensor, global_step=None, walltime=None, dataformats='CHW')

重要参数说明：
tag：标题
img_tensor：图片，注意必须是torch.Tensor、numpy.array或string/blobname类型
global_step：步骤？
"""

image_path = "hzhfData/NotSing/102.jpg"
img_PIL = Image.open(image_path)  # PIL.JpegImagePlugin.JpegImageFile类型
img_array = np.array(img_PIL)  # ndarray类型
"""
add_image()对img_array.shape是有要求的，要求图片格式为：(C, H, W)即（通道，宽度，高度）
查看img_array.shape可以看到它的图片格式为(H, W, C)，需要修改
可以在add_image()中添加参数dataformats='HWC'来调整格式
"""
writer.add_image("test", img_array, 1, dataformats='HWC')

writer.close()  # 也是固定的
```

关于image的使用还有一点要注意，png格式是四个通道，除了RGB三通道外，还有一个透明度通道，我们可以使用image = image.convert('RGB')来保留其颜色通道。

还是在pycharm终端使用tensorboard --logdir=logs然后打开网址，打开后需要切换上面的菜单项为IMAGES才可以看到图片哦。如果你刚才没有关掉这个网页，直接刷新也行。如果手动删掉了logs下面的文件，刷新就不起作用了。

![](https://i-blog.csdnimg.cn/blog_migrate/b7d3d83cf51d16fcf271d3b021fd10d2.png)

### OpenCV

> [OpenCV](https://www.leixue.com/so/OpenCV "OpenCV") 是一个基于 BSD 许可（开源）发行的跨平台[计算机视觉](https://www.leixue.com/so/%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%A7%86%E8%A7%89 "计算机视觉")和[机器学习](https://www.leixue.com/so/%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0 "机器学习")[软件库](https://www.leixue.com/so/%E8%BD%AF%E4%BB%B6%E5%BA%93 "软件库")，可以运行在 Linux、Windows、Android 和 Mac OS 操作系统上。OpenCV 可用于开发实时的图像处理、计算机视觉以及模式识别程序。

**安装**：pip install opencv-python

![](https://i-blog.csdnimg.cn/blog_migrate/9a66c65d9af96efe9aeadac92d7bab0f.png)

**引包**：import cv2

使用OpenCV操作图片：

```
import cv2

img_path = "hzhfData/Sing/100.jpg"
cv_img = cv2.imread(img_path)
print(type(cv_img))
```

![](https://i-blog.csdnimg.cn/blog_migrate/99c76819b1afeeb408bde0d293901d18.png)

注意这里有个比较特殊的就是引包是import cv2。

使用cv2读取到的图片是ndarray格式的。在Tensorboard中说过，图片格式必须是Tensor、numpy.array等，所以cv2得到的ndarray格式的图片就可以用在这里。

在PIL读取图像时可以使用show，cv2也同样，不仅可以用imread获取图片，还有其他操作。

```
import cv2

# 读取图片
img = cv2.imread("xdl.jpg")

# 保存图片
cv2.imwrite("This_is_a_photo.jpg", img)  # 可以将符合格式的数组保存为图片

# 显示图片
cv2.imshow("This_is_a_photo.jpg", img)
cv2.waitKey(0)  # 注意K大写，我写错了找了好久原因
"""
cv2.imshow()的显示时间很短，所以用waitKey控制着imshow的持续时间。
cv2.waitKey(delay)会在一定时间内等待用户输入键盘任意值。
    1. 参数说明：
        若 delay ≤ 0 ，表示一直等待按键；若delay取正整数：表示等待按键的时间，单位为milliseconds，即视频中一帧数据显示（停留）的时间。
    2. 返回值说明：
        若等待期间有按键：返回按键的ASCII码；若等待期间没有按键：返回-1。
    涉及到返回值的使用举例：
        if cv2.waitKey(5) & 0xFF == 27:
            break  # 为什么这么用此处不详细学习
    注意，它与time.sleep不同，waitKey只有在至少一个HighGUI窗口存在的情况下才会起作用。此处不详细说了……
"""
```

### TransForms

> TransForms主要用于对图片的变换。预处理以提高泛化能力。

使用TransForms的引包方法：

```
from torchvision import transforms
```

在学习TransForms的过程中，我感受到它的用法有些特殊，总是需要2步以上：第1步搞一个过滤器，第2步把图片传入过滤器得到新图片。

#### TransForms.ToTensor()

ToTensor()可以把**PIL Image**或**numpy.ndarray**转换成**Tensor**类型的对象。先看代码：

```
from torchvision import transforms
from PIL import Image

image_path = "hzhfData/NotSing/104.jpg"
img = Image.open(image_path)

# transforms.ToTensor()返回ToTensor对象
tensor_trans = transforms.ToTensor()
# __call__：传入picture时，返回Tensor类型的图片
tensor_img = tensor_trans(img)  # 还是魔法方法，用实例对象直接调用
```

**Tensor数据类型包装了我们深度学习所需要的一些参数**（如反向传播、梯度等）。在Tensorboard中说过，图片格式必须是Tensor、numpy.array等，所以ToTensor()得到的Tensor格式的图片就可以用在这里。

```
from torchvision import transforms
from PIL import Image
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter("logs")

image_path = "hzhfData/NotSing/104.jpg"
img = Image.open(image_path)
tensor_trans = transforms.ToTensor()
tensor_img = tensor_trans(img)

writer.add_image("test tensor", tensor_img, 1)

writer.close()
```

![](https://i-blog.csdnimg.cn/blog_migrate/dd23d73983f6739ddb8e2b661de1ad6f.png)

#### TransForms.Normalize()

Normalize()的作用是对Tensor图片归一化（这里up主表述的也不是很清楚，有很多弹幕质疑，我不知道到底什么才是标准的词语去形容），我的理解是对像素颜色的统一处理。

```
from torchvision import transforms
from PIL import Image
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter("logs")

# 先把img变成tensor格式
image_path = "hzhfData/NotSing/104.jpg"
img = Image.open(image_path)
tensor_trans = transforms.ToTensor()
tensor_img = tensor_trans(img)
writer.add_image("test tensor", tensor_img, 1)

# transforms.Normalize() 作用是把tensor图片归一化处理
"""
transforms.Normalize([xx1, xx2, xx3], [xx4, xx5, xx6])

参数说明：参数列表中的三个值分别处理R,G,B三个信道的值
[xx1, xx2, xx3]是mean[chanel]，均值
[xx4, xx5, xx6]是std[chanel]，标准差
计算公式：input[chanel] = (input[chanel]-mean[chanel]) / std[chanel]
"""
trans_norm = transforms.Normalize([6, 7, 9], [3, 4, 2])
img_norm = trans_norm(tensor_img)
writer.add_image("test normalize", img_norm, 1)  # 放在step1
trans_norm = transforms.Normalize([1, 3, 5], [3, 2, 1])
img_norm = trans_norm(tensor_img)
writer.add_image("test normalize", img_norm, 2)  # 放在step2，这里顺便感受一下step的作用
# 可以用tensor[0][0][0]查看数值

writer.close()
```

![](https://i-blog.csdnimg.cn/blog_migrate/bd95c5081f05e62f2b852f0ad0293728.png)![](https://i-blog.csdnimg.cn/blog_migrate/9dc2fa9c73635a50c0afd39fa2b778e9.png)

 图片上面有一个滑块，拖动滑块可以调整显示step。

#### TransForms.Resize()

Resize()的作用是改变**PIL**图片的大小（不裁剪）。新的版本好像也提供了修改tensor的功能，不只是PIL了。

```
from torchvision import transforms
from PIL import Image
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter("logs")

image_path = "hzhfData/NotSing/104.jpg"
img = Image.open(image_path)

# transforms.Resize()
"""
transforms.Resize()用于修改PIL图片的尺寸（调整图片比例），返回PIL格式的图片
当参数为一个序列，如 (x,y) ，则修改图片尺寸高为x、宽为y
当参数为一个数，如 x ，则修改图片使图片的最短边匹配x，等比例缩放
"""
trans_size = transforms.Resize((250, 512))
img_size = trans_size(img)

# 将图片修改为tensor类型
trans_tensor = transforms.ToTensor()
tensor_img_size = trans_tensor(img_size)

writer.add_image("test Resize", tensor_img_size, 1)

# 与原图比较
tensor_img = trans_tensor(img)
writer.add_image("test", tensor_img, 1)

writer.close()
```

![](https://i-blog.csdnimg.cn/blog_migrate/6e61221e3afe1ee776a0f37f1c86beed.png)

如果图片没有变化，可以试试点击一下图片。

#### TransForms.Compose()

Compose()就是函数级联，合成了许多功能。

```
from torchvision import transforms
from PIL import Image
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter("logs")

image_path = "hzhfData/Sing/102.jpg"
img = Image.open(image_path)

"""
Compose()的参数是一个列表，列表中的数据都是transforms类型，即[transforms参数1, transforms参数2, ...]
上一个transforms的输出是下一个transforms的输入
"""
trans_size = transforms.Resize((250, 512))
trans_tensor = transforms.ToTensor()
trans_compose = transforms.Compose([trans_size, trans_tensor])
tensor_img = trans_compose(img)

writer.add_image("test Compose", tensor_img, 1)

writer.close()
```

![](https://i-blog.csdnimg.cn/blog_migrate/6a86017bcb2c82836b9878962980eae2.png)

#### TransForms.RandomCrop()

RandomCrop()用于随机裁剪图片。与Resize()的参数使用方法类似。

---

参考：

[怎么检查cuda是否安装成功（以及查看cuda的安装位置）](https://blog.csdn.net/qq_41897154/article/details/115273699?spm=1001.2101.3001.6661.1&utm_medium=distribute.pc_relevant_t0.none-task-blog-2~default~CTRLIST~default-1-115273699-blog-110210033.pc_relevant_sortByAnswer&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2~default~CTRLIST~default-1-115273699-blog-110210033.pc_relevant_sortByAnswer&utm_relevant_index=1 "怎么检查cuda是否安装成功（以及查看cuda的安装位置）")

[Pytorch安装，这一篇就够了，绝不踩坑](https://blog.csdn.net/love_respect/article/details/124681233 "Pytorch安装，这一篇就够了，绝不踩坑")

[GPU, CUDA,cuDNN三者的关系总结](https://blog.csdn.net/qq_36697196/article/details/124329433 "GPU, CUDA,cuDNN三者的关系总结")

[pytorch官网不支持cuda10.2](https://blog.csdn.net/weixin_45681381/article/details/124276134 "pytorch官网不支持cuda10.2")

[英伟达NVIDIA驱动程序安装失败/解决N卡安装失败问题](https://zhuanlan.zhihu.com/p/110530306 "英伟达NVIDIA驱动程序安装失败/解决N卡安装失败问题")

[亲测可用！解决GeForce Experience安装失败的几种方法](https://www.bilibili.com/read/cv10869322 "亲测可用！解决GeForce Experience安装失败的几种方法")

[Solving NVIDIA Installer Issues](https://nvidia.custhelp.com/app/answers/detail/a_id/4223 "Solving NVIDIA Installer Issues")

[英伟达驱动安装出现了一个错误怎么解决？](https://www.xitongzhijia.net/xtjc/20211228/236706.html "英伟达驱动安装出现了一个错误怎么解决？")

[Win11电脑更新Nvidia显卡驱动出现一个错误怎么办](https://www.downkr.com/news/232971_1.html "Win11电脑更新Nvidia显卡驱动出现一个错误怎么办")

[完美解决torch.cuda.is\_available()一直返回False的玄学方法](https://www.jb51.net/article/205490.htm "完美解决torch.cuda.is_available()一直返回False的玄学方法")

[Windows端pytorch镜像快速安装【清华源】](https://blog.csdn.net/Thebest_jack/article/details/123455215 "Windows端pytorch镜像快速安装【清华源】")

[python：在pycharm中安装pytorch的绝对可行的方法！！要是这个不行..........那你就换一种](https://blog.csdn.net/ccutyear/article/details/106507310 "python：在pycharm中安装pytorch的绝对可行的方法！！要是这个不行..........那你就换一种")

[(conda + pip) 配置各版本 Pytorch 深度学习环境](https://blog.csdn.net/Wenyuanbo/article/details/119382460 "(conda + pip) 配置各版本 Pytorch 深度学习环境")

[PyTorch深度学习快速入门教程（绝对通俗易懂！）【小土堆】](https://www.bilibili.com/video/BV1hE411t7RN?p=1&vd_source=b9903dbe1b7c91d693351ba0e40e8aaa "PyTorch深度学习快速入门教程（绝对通俗易懂！）【小土堆】")

[cv2.waitKey的入门级理解](https://blog.csdn.net/weixin_44049693/article/details/106271643 "cv2.waitKey的入门级理解")

[cv2.waitKey()](https://blog.csdn.net/weixin_54977011/article/details/120208280 "cv2.waitKey()")