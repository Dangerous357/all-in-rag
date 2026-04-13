# 【深度学习】计算机视觉（六）——pytorch（下）

#### 文章目录

* [三、torch（中）——torch.nn](#torchtorchnn_2)
* + [1：nn.Module](#1nnModule_19)
  + [2：nn.Conv2d（卷积）](#2nnConv2d_46)
  + [3：nn.MaxPool2d（池化）](#3nnMaxPool2d_184)
  + [4：nn.ReLu（非线性激活）](#4nnReLu_307)
  + [5：nn.Linear（线性层/全连接层）](#5nnLinear_344)
  + [6：nn.Sequential](#6nnSequential_421)
  + [7：损失函数](#7_471)
  + - [（1）nn.L1Loss](#1nnL1Loss_473)
    - [（2）nn.MSELoss](#2nnMSELoss_497)
    - [（3）nn.CrossEntropyLoss](#3nnCrossEntropyLoss_517)
* [四、torch（下）——torch.optim](#torchtorchoptim_544)
* + [1：反向传播](#1_545)
  + [2：优化器](#2_621)
* [五、模型使用入门](#_703)
* + [1：训练数据的加载和保存](#1_707)
  + [2： 模型训练tips](#2_tips_760)
  + [3： 冻结/解冻骨干网络参数](#3__772)

三、torch（中）——torch.nn
--------------------

神经网络——Neural network，pytorch中关于神经网络的工具在`torch.nn`中。其中主要有以下核心内容：

* Containers：定义了神经网络的结构
* Convolution Layers：卷积层
* Pooling layers：池化层
* Padding Layers：边缘填充
* Non-linear Activations：非线性激活
* Normalization Layers：正则化层。可以加快神经网络的训练速度
* Recurrent Layers：一些特定的网络结构，包含RNN等
* Transformer Layers：也是有一些特定的网络结构
* Linear Layers：线性层
* Dropout Layers：丢弃层。为了防止过拟合，会以p为概率丢弃一些元素，即随机失活
* Sparse Layers：主要用于自然语言处理
* ……

下面的讲解都是一些很重要的**类**。

### 1：nn.Module

`torch.nn.Module`是为所有神经网络的模型提供的一个基本的类。所有神经网络的模型必须继承Module。  
 举个例子：

```
import torch
from torch import nn


class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        print()  # 剩下的自己写

    def forward(self, input):  # 前向传播
        output = input + 1  # 剩下的自己写
        return output


myModel = Model()
output = myModel(torch.tensor(1.0))  # 调用forward()方法，input=1.0
# 注意：调用时类似__call__，因为nn.Module中forward方法是集成在__call__()方法的实现
print(output)
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1ff0fdaaf42c8b86f2eb9c4ba24a91e0.png)

### 2：nn.Conv2d（卷积）

常用的关于卷积层的库有：

* nn.Conv1d（一维）
* nn.Conv2d（二维）
* nn.Conv3d（三维）

由于输入图片是二维的，所以这里我们用到的是`Conv2d`。  
 首先介绍一个“空洞卷积”的概念，在后面表示为`dilation`参数。它控制卷积核之间的距离，如下图，每个小方块之间不是紧凑的：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e166bfc62000798f7561c359fb4cba8d.png)

除了`nn.Conv2d`之外，还有`nn.functional`中也有`conv2d`，它们有什么区别呢？`nn.Conv2d`是在`functional`的基础上集成封装的，可能一些操作更方便。下面将说明它们之间的区别以及用法。先举个例子，用`functional.conv2d`实现下图的卷积操作：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a378b46927076d8c9d6182860c074ee3.png)

```
import torch
import torch.nn.functional as F  # 导入nn.functional
"""
conv2d(input, weight, bias=None, stride=1, padding=0, dilation=1, groups=1)
返回tensor数据类型

参数说明：
input：输入。tensor数据类型，要求它的shape说明minibatch、in_channels（输入通道）、iH、iW
weight：卷积核。要求它的shape说明包含out_channels（输出的通道）、in_channels÷groups（groups一般取1，相除的结果为in_channels）、kH、kW）
bias：偏置
stride：步长，可以是单个数也可以是元组(SH,SW)，默认为1
padding：边缘填充。可以是单个数也可以是元组(pH, pW)，默认为0
dilation
groups
"""

# 首先创建tensor类型的输入input和卷积核kernel
input1 = torch.tensor([[1, 2, 0, 3, 1],
                      [0, 1, 2, 3, 1],
                      [1, 2, 1, 0, 0],
                      [5, 2, 3, 1, 1],
                      [2, 1, 0, 1, 1]])
kernel1 = torch.tensor([[1, 2, 1],
                       [0, 1, 0],
                       [2, 1, 0]])
# 由于input的shape返回torch.size(5, 5)，需要将它的shape设置为4个参数（对应conv2d的参数），kernel同理要对应weight
input1 = torch.reshape(input1, (1, 1, 5, 5))  # 使用torch.reshape()修改
kernel1 = torch.reshape(kernel1, (1, 1, 3, 3))
# 使用conv2d进行卷积
output1 = F.conv2d(input1, kernel1, stride=1)
print(output1)  # 验证结果
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/71536cf4247eb7dd7a6d034d39ee2506.png)  
 输出正确结果。由于stride和padding都是用参数控制的，非常简单，所以不进行模拟了。

如果是用`nn.Conv2d`的话，注意它是一个类，用起来有一些区别。因为两个分开的训练集我还不太会用，所以我把NotSing和Sing放在了一个文件夹Train里，通过修改文件名去设置标签。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c84d1b1645f25961dfd4b11e76f7b093.png)

```
import torch
import torch.nn as nn
import os
from PIL import Image
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from torch.utils.tensorboard import SummaryWriter
from torchvision import transforms


"""
Conv2d(in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1, bias=True, padding_mode='zeros')

参数说明：
in_channels：输入通道数
out_channels：输出通道数
kernel_size：卷积核大小。可以是int或者元组
stride：步长。可以是单个数也可以是元组(SH,SW)，默认为1
padding：边缘填充。可以是单个数也可以是元组(pH, pW)，默认为0
dilation：设置卷积核的距离。int或元组，用于“空洞卷积”，一般不常用
groups：一般都是1，几乎用不到
bias：偏置。一般设置为True
padding_mode：填充模式。'zeros'表示设置填充为0
"""


class MyModule(nn.Module):  # 继承Module主要进行卷积操作
    def __init__(self):
        super(MyModule, self).__init__()
        self.conv = nn.Conv2d(in_channels=3, out_channels=6, kernel_size=3)

    def forward(self, x):
        x = self.conv(x)
        return x


class MyData(Dataset):
    def __init__(self, root_dir, label_dir):
        self.root_dir = root_dir
        self.label_dir = label_dir
        self.path = os.path.join(self.root_dir, self.label_dir)
        self.img_path = os.listdir(self.path)

    def __getitem__(self, idx):
        img_name = self.img_path[idx]
        if img_name.startswith('Not') is True:
            img_label = "NotSing"
        else:
            img_label = "Sing"
        img_item_path = os.path.join(self.path, img_name)
        img = Image.open(img_item_path)
        trans_tensor = transforms.ToTensor()
        return trans_tensor(img), img_label  # 返回tensor类型的数据集而不是PIL.image

    def __len__(self):
        return len(self.img_path)


train_dataset = MyData("hzhfData", 'Train')
train_loader = DataLoader(train_dataset, batch_size=5)

module = MyModule()

writer = SummaryWriter("logs")  # ..表示上一级目录
# 对train_loader中的每一个图像进行卷积操作
step = 0
for data in train_loader:  # 我的数据集有10张图片，每5张打包一次，所以data循环2次
    imgs, targets = data
    output = module(imgs)  # 卷积核是随机生成的，所以只输入图片即可
    print(imgs.shape)  # 输出 torch.Size([10, 3, 300, 300])
    writer.add_images("input", imgs, step)  # 将输入记录在logs中
    print(output.shape)  # 输出 torch.Size([10, 6, 298, 298])
    # 因为图片只有3个通道，6个通道没办法显示可能会报错，所以要重新修改一下图片尺寸
    output = torch.reshape(output, (-1, 3, 298, 298))  # 第一个参数batch_size设置成-1就可以自动计算
    writer.add_images("output", output, step)  # 将输出记录在logs中
    step = step + 1

writer.close()
```

然后看一下SummaryWriter：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0996981ab296beb07f6f788d05f23c96.png)

### 3：nn.MaxPool2d（池化）

池化也有很多对应的库，比如最大池化，也叫做下采样：

* `nn.Maxpool1d`
* `nn.Maxpool2d`
* `nn.Maxpool3d`

还有上采样：

* `nn.MaxUnpool1d`
* `nn.MaxUnpool2d`
* `nn.MaxUnpool3d`

等等，其中最常用的是`nn.Maxpool2d`。  
 举个例子，给如下输入：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/51e146afdc259d66f668b7a1102b2dc1.png)

```
import torch
import torch.nn as nn
"""
MaxUnpool2d(kernel_size, stride=None, padding=0, dilation=1, return_indices=False, ceil_mode=False)

参数说明：
kernel_size：取最大池化的窗口。可以是int或者元组
stride：步长。默认为kernel_size的大小，不重合
dilation：空洞卷积的距离
return_indices：（不常用）
ceil_mode：池化有剩余时如何处理。当设置为True时，使用ceil模式（向上取整）；当设置为false时，使用floor模式（向下取整）
"""


class MyModule(nn.Module):
    def __init__(self):
        super(MyModule, self).__init__()
        self.maxpool = nn.MaxPool2d(kernel_size=3, ceil_mode=True)

    def forward(self, input):
        output = self.maxpool(input)
        return output


input = torch.tensor([[1, 2, 0, 3, 1],
                      [0, 1, 2, 3, 1],
                      [1, 2, 1, 0, 0],
                      [5, 2, 3, 1, 1],
                      [2, 1, 0, 1, 1]], dtype=torch.float32)  # 因为不能对整数进行池化操作
input = torch.reshape(input, (-1, 1, 5, 5))  # Module要求input是四维的
myModule = MyModule()
output = myModule(input)
print(output)
```

由于我们设置了`ceil_mode=True`，得到如下输出：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/8f5273606445a57112841ee576d3030e.png)  
 然后再用自己的数据集试一下：

```
import torch
import torch.nn as nn
import os
from PIL import Image
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from torch.utils.tensorboard import SummaryWriter
from torchvision import transforms


class MyModule(nn.Module):  # 继承Module主要进行卷积操作
    def __init__(self):
        super(MyModule, self).__init__()
        self.maxpool = nn.MaxPool2d(kernel_size=2, ceil_mode=True)

    def forward(self, input):
        output = self.maxpool(input)
        return output


class MyData(Dataset):
    def __init__(self, root_dir, label_dir):
        self.root_dir = root_dir
        self.label_dir = label_dir
        self.path = os.path.join(self.root_dir, self.label_dir)
        self.img_path = os.listdir(self.path)

    def __getitem__(self, idx):
        img_name = self.img_path[idx]
        if img_name.startswith('Not') is True:
            img_label = "NotSing"
        else:
            img_label = "Sing"
        img_item_path = os.path.join(self.path, img_name)
        img = Image.open(img_item_path)
        trans_tensor = transforms.ToTensor()
        return trans_tensor(img), img_label  # 返回tensor类型的数据集而不是PIL.image

    def __len__(self):
        return len(self.img_path)


train_dataset = MyData("hzhfData", 'Train')
train_loader = DataLoader(train_dataset, batch_size=5)

module = MyModule()

writer = SummaryWriter("logs")  # ..表示上一级目录
# 对train_loader中的每一个图像进行卷积操作
step = 0
for data in train_loader:  # 我的数据集有10张图片，每5张打包一次，所以data循环2次
    imgs, targets = data
    output = module(imgs)  # 卷积核是随机生成的，所以只输入图片即可
    print(imgs.shape)  # 输出 torch.Size([5, 3, 300, 300])
    writer.add_images("input", imgs, step)  # 将输入记录在logs中
    print(output.shape)  # 输出 torch.Size([5, 3, 150, 150])
    writer.add_images("output", output, step)  # 将输出记录在logs中
    step = step + 1

writer.close()
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/34236718581085a9e693fe2f901c07d2.png)  
 可以看到小了一半，但是图像变化不大，并没有出现我想象中的难以辨认，说明最大特征还是很好用的。

### 4：nn.ReLu（非线性激活）

非线性激活函数之前学了很多，这里以ReLu为例进行学习。直接看代码：

```
import torch
from torch import nn
from torch.nn import ReLU
"""
nn.ReLu(input)

参数说明：
input：它的shape是(N, *)，N就是batch_size。同样输出output的shape也是(N,*)
inplace：是否替换。若设置inplace=True，会原地操作，覆盖输入；若设置inplace=False，返回新的变量而不改变input本身。默认为False
"""


class MyModule(nn.Module):
    def __init__(self):
        super(MyModule, self).__init__()
        self.relu = ReLU(inplace=True)  # 原地操作

    def forward(self, input):
        input = self.relu(input)
        return input


input = torch.tensor([[1, -0.5],
                      [-1, 3]])
input = torch.reshape(input, (-1, 1, 2, 2))  # 修改shape为 torch.size([1, 1, 2, 2])
module = MyModule()
module(input)  # 进行非线性激活
print(input)
```

可以看到经过ReLu变换，负数全部变为0。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/cb9e0e21a56854df10ca05c8a1e90b01.png)

### 5：nn.Linear（线性层/全连接层）

线性层就是我们说的全连接层，像这样：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/010df533b79216e48d57005cf514d95b.png)  
 没什么可讲的，就直接示范代码：

```
import os

import torch
from PIL import Image
from torch import nn
from torch.nn import Linear
from torch.utils.data import Dataset, DataLoader
from torchvision.transforms import transforms

"""
nn.Linear(in_features, out_features, bias=True)

参数说明：
in_features：输入的特征值个数
out_features：经过全连接之后输出的特征值个数
bias：偏置
"""


class MyModule(nn.Module):
    def __init__(self):
        super(MyModule, self).__init__()
        self.linear = Linear(1350000, 100)  # 输入向量的个数要根据数据集决定

    def forward(self, input):
        output = self.linear(input)
        return output


class MyData(Dataset):
    def __init__(self, root_dir, label_dir):
        self.root_dir = root_dir
        self.label_dir = label_dir
        self.path = os.path.join(self.root_dir, self.label_dir)
        self.img_path = os.listdir(self.path)

    def __getitem__(self, idx):
        img_name = self.img_path[idx]
        if img_name.startswith('Not') is True:
            img_label = "NotSing"
        else:
            img_label = "Sing"
        img_item_path = os.path.join(self.path, img_name)
        img = Image.open(img_item_path)
        trans_tensor = transforms.ToTensor()
        return trans_tensor(img), img_label  # 返回tensor类型的数据集而不是PIL.image

    def __len__(self):
        return len(self.img_path)


train_dataset = MyData("hzhfData", 'Train')
train_loader = DataLoader(train_dataset, batch_size=5)

module = MyModule()

for data in train_loader:  # 我的数据集有10张图片，每5张打包一次，所以data循环2次
    imgs, targets = data
    print(imgs.shape)  # 输出 torch.Size([5, 3, 300, 300])
    # 由于全连接中特征都是以列向量的形式输入的，所以需要把四维向量变换成列向量
    # 第一种方法
    input1 = torch.reshape(imgs, (1, 1, 1, -1))  # 得到 torch.Size([1, 1, 1, 1350000])
    # 第二种方法：使用torch.flatten()可以将tensor摊平成一维
    input2 = torch.flatten(imgs)  # 得到 torch.Size([1350000])
    output = module(input1)
    print(output.shape)  # 得到 torch.Size([1, 1, 1, 100])
```

根据output的输出格式可以看到我们已经得到了自己想要的。由于输入和输出的像素形式都不太好显示，我看了看SummaryWriter觉得没什么意义，所以这里就不放SummaryWriter的结果图了，包括相关代码都删掉了。

### 6：nn.Sequential

![它可以让我们](https://i-blog.csdnimg.cn/blog_migrate/fe014e6f197f1f12148a1cac243e9bf8.png)  
 这里练习实现上图的神经网络，先顺一遍它的步骤。首先一个32×32×3的输入，经过一个5×5的卷积核得到32×32×32的输出，可以算出padding为2；然后经2×2的滤波器池化后变成16×16×32的输出，得到第三组……第七组4×4×64的特征图先Flatten平铺成一维，即长度为4*4*64=1024的一维矩阵；经全连接得到长度为64的一维向量；最后再次全连接输出长度为10的一维向量。

```
import torch
from torch import nn
from torch.nn import Linear, Sequential, Conv2d, MaxPool2d, Flatten


class MyModule(nn.Module):
    def __init__(self):
        super(MyModule, self).__init__()
        # 用sequential可以将神经网络的操作组成一个序列一起使用
        self.seq = Sequential(
            Conv2d(3, 32, 5, padding=2),
            MaxPool2d(2),
            Conv2d(32, 32, 5, padding=2),
            MaxPool2d(2),
            Conv2d(32, 64, 5, padding=2),
            MaxPool2d(2),
            Flatten(),
            Linear(1024, 64),
            Linear(64, 10)
        )

    def forward(self, input):
        output = self.seq(input)
        return output


module = MyModule()
# 利用torch.ones创造一个值全为1的矩阵作为输入，格式按照要求进行
input = torch.ones((64, 3, 32, 32))  # batch_size由于图片中不做要求，这里设置为64
output = module(input)
print(output.shape)
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/201716a5e807150a9caafaaaf1f8d0b7.png)  
 通过输出可以看到，我们得到的output正是batch\_size为64，长度为10。

补充一个小知识，使用SummaryWriter中的`add_graph`可以查看网络的结构，具体用法举例：

```
writer = SummaryWriter("logs")
writer.add_graph(module, input)
writer.close()
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ab628826b6981b2d9d486b81431633fc.png)  
 其中每个部分还可以再放大，记录了详细的数据和步骤。

### 7：损失函数

这里可以先看代码，关于损失函数更系统的总结在[【深度学习】计算机视觉（八）——使用GPU进行目标检测详解（中）](https://blog.csdn.net/RK_Dangerous/article/details/127434667?spm=1001.2014.3001.5501)

#### （1）nn.L1Loss

```
import torch
from torch.nn import L1Loss

"""
nn.L1Loss(size_average=None, reduce=None, reduction='mean')

参数说明：
reduction：设置成'mean'则损失函数的表达式为求均值；设置成'sum'则损失函数的表达式为求最大值。默认为'mean'
"""


inputs = torch.tensor([1, 2, 3], dtype=torch.float32)  # 样本计算值
targets = torch.tensor([1, 2, 5], dtype=torch.float32)  # 正确值（目标值）
inputs = torch.reshape(inputs, (1, 1, 1, 3))
targets = torch.reshape(targets, (1, 1, 1, 3))

loss = L1Loss(reduction='mean')
result = loss(inputs, targets)
print(result)
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/04279fbb4b94b2035e2a4f07ef738a3f.png)

#### （2）nn.MSELoss

MSE和L1Loss差不多，它的算法是先计算差值的平方和，再求平均或最大值。

```
import torch
from torch.nn import MSELoss


inputs = torch.tensor([1, 2, 3], dtype=torch.float32)  # 样本计算值
targets = torch.tensor([1, 2, 5], dtype=torch.float32)  # 正确值（目标值）
inputs = torch.reshape(inputs, (1, 1, 1, 3))
targets = torch.reshape(targets, (1, 1, 1, 3))

loss = MSELoss(reduction='sum')
result = loss(inputs, targets)
print(result)
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7092c1a21d5d41fbed4991a53fbaf192.png)

#### （3）nn.CrossEntropyLoss

CrossEntropyLoss计算交叉熵，之前学的softmax分类器就是这个道理。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/831d0f3842ddd5a561176ee7a5170d66.png)  
 解读一下，`loss=（-正确分类的概率）+log（每一个可能分类的概率的exp加和）`。其中`（-正确分类的概率）`使得如果正确分类的概率越大，损失越小；`每一个可能分类的概率的exp加和`使我们希望被分为各个类别的概率不要全都很大。注意这里log是以e为底的（计算机中的log一般都是以e为底的）。

```
import torch.nn
from torch.nn import CrossEntropyLoss

"""
nn.CrossEntropyLoss(weight=None, size_average=None, ignore_index=-100, reduce=None, reduction='mean')

参数说明：
input：要求shape是(N, C)，其中N是batch_size，C是类别的个数
target：要求shape是(N)
"""


# 例如对一张图片进行三分类，正确类别对应序号为1
input = torch.tensor([0.1, 0.2, 0.3])  # 计算出每个类别的得分分别为0.1、0.2、0.3
input = torch.reshape(input, (1, 3))  # 只有一张图片，所以设置batch_size为1
target = torch.tensor([1])  # 因为只有一张图片，所以矩阵的长度为1，存储正确类别的序号
loss = CrossEntropyLoss()
result = loss(input, target)
print(result)
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/efabb8d77bbf1c9bcc6d078690429926.png)

四、torch（下）——torch.optim
-----------------------

### 1：反向传播

计算出损失函数之后，我们使用`loss.backward()`可以计算梯度。由于之前的数据集是300×300的，为了直接使用学习sequential时的网络结构，我编辑了一下图片的尺寸，编辑成了32×32的。而且我注意到计算反向传播时的targets参数必须是shape为(N)的数据，而我之前的dataset返回的是字符串，所以这里也作了修改。

```
import torch
from torch.nn import Sequential, Conv2d, MaxPool2d, Flatten
import os
from PIL import Image
from torch import nn
from torch.nn import Linear
from torch.utils.data import Dataset, DataLoader
from torchvision.transforms import transforms


class MyModule(nn.Module):
    def __init__(self):
        super(MyModule, self).__init__()
        self.seq = Sequential(
            Conv2d(3, 32, 5, padding=2),
            MaxPool2d(2),
            Conv2d(32, 32, 5, padding=2),
            MaxPool2d(2),
            Conv2d(32, 64, 5, padding=2),
            MaxPool2d(2),
            Flatten(),
            Linear(1024, 64),
            Linear(64, 10)
        )

    def forward(self, input):
        output = self.seq(input)
        return output


class MyData(Dataset):
    def __init__(self, root_dir, label_dir):
        self.root_dir = root_dir
        self.label_dir = label_dir
        self.path = os.path.join(self.root_dir, self.label_dir)
        self.img_path = os.listdir(self.path)

    def __getitem__(self, idx):
        img_name = self.img_path[idx]
        # 因为target必须是tensor数据类型，而且要符合shape为(N)
        if img_name.startswith('Not') is True:
            img_label = torch.tensor(0)  # 用0表示NotSing
        else:
            img_label = torch.tensor(1)  # 用1表示Sing
        img_item_path = os.path.join(self.path, img_name)
        img = Image.open(img_item_path)
        trans_tensor = transforms.ToTensor()
        return trans_tensor(img), img_label  # 返回tensor类型的数据集而不是PIL.image

    def __len__(self):
        return len(self.img_path)


train_dataset = MyData("hzhfData", 'Train32')
train_loader = DataLoader(train_dataset, batch_size=1)

module = MyModule()

loss = nn.CrossEntropyLoss()

for data in train_loader:  # 这个for循环可以看成是做题和学习的过程，每循环一次就做一道题，就相当于一个周期
    imgs, targets = data
    outputs = module(imgs)  # 将打包的图片前向传播得到得分函数
    result = loss(outputs, targets)  # 用得分函数和正确标签计算损失函数
    result.backward()  # 利用反向传播计算权重
```

然后可以在最后一行打个断点然后debugger，在代码结构里面找到grad查看，在最后一行运行之前，`grad=None`。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/42ba1a95923cc503fb45c5c821286aec.png)  
 运行反向传播语句后，代码结构中可以看到grad后面有了数据，它们就是计算得到的梯度。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d583688426ff0016af6bd6d3867c0f78.png)

### 2：优化器

optim中的优化器可以根据梯度调整参数的大小。所有的优化器的使用方法都可以概括为大致如下：  
 `torch.optim.优化器名(params, lr=1.0, 不同优化器需要的特定参数)`，其中params就是要调整的参数，lr是learning rate即学习率。  
 仍用反向传播部分的代码，这里使用SGD（随机梯度下降）练习优化器的使用：

```
import torch
from torch.nn import Sequential, Conv2d, MaxPool2d, Flatten
import os
from PIL import Image
from torch import nn
from torch.nn import Linear
from torch.utils.data import Dataset, DataLoader
from torchvision.transforms import transforms


class MyModule(nn.Module):
    def __init__(self):
        super(MyModule, self).__init__()
        self.seq = Sequential(
            Conv2d(3, 32, 5, padding=2),
            MaxPool2d(2),
            Conv2d(32, 32, 5, padding=2),
            MaxPool2d(2),
            Conv2d(32, 64, 5, padding=2),
            MaxPool2d(2),
            Flatten(),
            Linear(1024, 64),
            Linear(64, 10)
        )

    def forward(self, input):
        output = self.seq(input)
        return output


class MyData(Dataset):
    def __init__(self, root_dir, label_dir):
        self.root_dir = root_dir
        self.label_dir = label_dir
        self.path = os.path.join(self.root_dir, self.label_dir)
        self.img_path = os.listdir(self.path)

    def __getitem__(self, idx):
        img_name = self.img_path[idx]
        # 因为target必须是tensor数据类型，而且要符合shape为(N)
        if img_name.startswith('Not') is True:
            img_label = torch.tensor(0)  # 用0表示NotSing
        else:
            img_label = torch.tensor(1)  # 用1表示Sing
        img_item_path = os.path.join(self.path, img_name)
        img = Image.open(img_item_path)
        trans_tensor = transforms.ToTensor()
        return trans_tensor(img), img_label  # 返回tensor类型的数据集而不是PIL.image

    def __len__(self):
        return len(self.img_path)


train_dataset = MyData("hzhfData", 'Train32')
train_loader = DataLoader(train_dataset, batch_size=1)

module = MyModule()

loss = nn.CrossEntropyLoss()

optim = torch.optim.SGD(module.parameters(), lr=0.01)  # 参数直接调用网络中的parameters

for data in train_loader:  # 这个for循环可以看成是做题和学习的过程，每循环一次就做一道题，就相当于一个周期
    imgs, targets = data
    outputs = module(imgs)  # 将打包的图片前向传播得到得分函数
    result = loss(outputs, targets)  # 用得分函数和正确标签计算损失函数
    optim.zero_grad()  # 因为backward计算时会累加上一次的结果，我们需要清空上次计算的权重再训练
    result.backward()  # 利用反向传播计算权重
    optim.step()  # 对每个参数进行调整
```

在清空权重后，可以看到权重数据被赋值为0：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/45a814044dd2d7b851fcc5b2364553c8.png)  
 根据上面的学习理解到了每次for循环做了一道题，比如batch\_size设置为5，那么我一次学习5张图片，第二次学习另外5张图片……直到学完所有的数据集，学了几次就是经历了几个传播周期，但是for循环结束之后只是把这个数据集整体地学习了一遍，因为每次学习特征可能都不太一样，所以我们一份卷子要做好多遍，就可以在for循环外面再套一层for循环。

五、模型使用入门
--------

**说明：**  
 本节内容作为pytorch笔记的最后部分，记录了一些模型使用过程中的问题和技巧，边学习边补充总结在这里，可能包含模型的使用、优化的手段等等一系列问题。  
 本节`1. 训练数据的加载和保存`和`2. 模型训练tips`写的不是特别详细，出自参考视频：[参考视频教程](https://www.bilibili.com/video/BV1hE411t7RN?p=27)

### 1：训练数据的加载和保存

据我所知，一般是不需要自己些网络结构的，都是用现有模型。模型训练完之后得到的参数我们总要记录下来吧？不然下次打开的时候又要重新训练一遍了。  
 **（1） 保存【模型+参数】**  
 1.1 保存

```
import torch
import torchvision

vgg16 = torchvision.models.vgg16(pretrained=False)  # 先获取模型，pretrained=False表示模型未经过训练

torch.save(vgg16, "vgg16.pth")
```

1.2 加载

```
import torch
import torchvision

from vgg16.pth import *  # 注意如果使用自己写的网络，使用前需要导入这个包

vgg16 = torchvision.models.vgg16(pretrained=False)  # 先获取模型，pretrained=False表示模型未经过训练

model = torch.load("vgg16.pth")
```

**（2）仅保存【参数】**  
 2.1 保存

```
import torch
import torchvision

vgg16 = torchvision.models.vgg16(pretrained=False)  # 先获取模型

"""
修改模型或训练模型中……
"""

torch.save(vgg16.state_dict(), "vgg16.pth")  # 保存参数
```

2.2 加载

```
import torch
import torchvision

vgg16 = torchvision.models.vgg16(pretrained=False)  # 先获取模型

model = torch.load("vgg16.pth")  # 获取参数
vgg16.load_state_dict()  # 装载参数
```

### 2： 模型训练tips

1. 验证集的使用  
    在测试模型时，先写一句`with torch.no_grad():`，然后在下面缩进写代码，这样就不计算梯度了。
2. 由得分得到结果  
    对于多分类问题，我们得到了某图片对应每个分类的得分矩阵后，使用`结果 = 得分.argmax(0)`可以得到每个图片得分的最大值作为它的最终分类结果。其中参数表示标签的存储方式，若为`0`则表示跨行存储，即每列为一个图片的所有得分；若为`1`则表示跨列读取，即每行为一个图片的所有得分。假设我们设置参数为0，对于第一列，第一行表示第一个图片被分为第一类的概率，第二行表示第一个图片被分为第二类的概率，第三行……；对于第二列，第一行表示第二个图片被分为第一类的概率，第二行表示第二个图片被分为第二类的概率，第三行……。
3. 正确率  
    我们可以根据`预测值 == 正确值`返回一个tensor类型保存每个图片判断的结果，形式大致为`tensor([False, True, ……])`。这显然是不够用的，我们只需使用`(预测值 == 正确值).sum()`方法返回分类正确的个数，False和True会被sum()分别视为0和1计算。显然我们知道测试集总数量，现在就可以知道正确率了。
4. 只要数值  
    在之前很多输出的时候，都有类似`tensor(5)`这样格式的输出，如果我们觉得它很啰嗦，可以使用`变量.item()`来输出值。
5. train()和eval()的作用  
    在网络训练前和测试前，分别使用`module实例.train()`和`module实例.eval()`，系统对于神经网络的某些层会做出不同的操作。

### 3： 冻结/解冻骨干网络参数

冻结骨干网络参数可用于迁移学习、finetune（微调）网络等。冻结网络参数，一部分初始权重被冻结在原位，其余权重用于计算损失，并由优化器更新，这需要比正常训练更少的资源，并且允许更快的训练时间。

> **迁移学习**是一种机器学习方法，就是把为任务 A 开发的模型作为初始点，重新使用在为任务 B 开发模型的过程中。  
>  迁移学习是一种有用的方法，可以快速地在新数据上重新训练模型，而不必重新训练整个网络。

在Pytorch中，一般是设置该变量的`require_grad=False`。`requires_grad`是Pytorch中通用数据结构Tensor的一个属性，用于说明当前量是否需要在计算中保留对应的梯度信息，以线性回归为例，容易知道权重w和偏差b为需要训练的对象，为了得到最合适的参数值，我们需要设置一个相关的损失函数，根据梯度回传的思路进行训练，若不输入梯度信息，则无法更新网络。首先要学习几个函数：

* `named_parameters()`：返回一个包含多个元组的list，每个元组打包2个内容，分别是`layer-name`（网络层的名字）和`layer-param`（参数的迭代器）。  
   ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/15fa908a4ad9b3bd31168969c44e1f62.png)  
   先不管model的意思，体会一下它的用法。layer-name定义了第几个神经层、哪些参数，layer-param返回的是一个迭代器，可以用它显示具体的参数值（注意它不仅仅是简单的数值，它是`<class 'torch.nn.parameter.Parameter'>`类型）。大致用法样例如下（省略部分结果）：  
   ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/589f153453715f80512d97f46089c07a.png)
* `parameters()`：类似named\_parameters()，但是只有layer-param（参数的迭代器）。

然后下面来解释`require_grad=False`的详细用法，以及上面讲解中出现的"`model`"表示什么。

```
import torch.nn as nn


# 首先自定义一个网络（具体内容省略）
class MyModule(nn.Module):
    def __init__(self):
        super(MyModule, self).__init__()


model = MyModule()  # 实例化该网络为model

"""
# 也可以实例化现有的网络，例如resnet18
import torchvision.models as models
model = models.resnet18()
"""

# 1. 冻结任意参数
freeze = []  # 存放需要冻结的参数名（里面的内容省略）
for k, v in model.named_parameters():
    v.requires_grad = True  # 在计算中保留对应的梯度信息
    if any(x in k for x in freeze):   # 对freeze中的每一个X都执行"x in k"操作
        print('freezing %s' % k)  # 把freeze用x迭代，如果在freeze中找到了k，则k就是我们需要冻结的参数
        v.requires_grad = False  # 设置该参数冻结

# 2. 冻结前N层参数
N = 7  # 假设N为7
for i, para in enumerate(model.parameters()):  # enumerate()函数用于将一个可遍历的数据对象组合为一个索引序列，同时列出数据和数据下标
    if i < N:
        para.requires_grad = False

# 3. 冻结网络任意层
frozen_layers = [model.layer1, model.layer2, model.layer3]  # 可以先用named_parameters()查看层名
for layer in frozen_layers:
    for name, value in layer.named_parameters():
        value.requires_grad = False
params = filter(lambda p: p.requires_grad, model.parameters())  # filter()函数用于过滤序列,作用是从一个序列中筛选出符合条件的元素。第一个参数接收一个函数，第二个参数接收一个序列
```

---

参考来源：

[PyTorch深度学习快速入门教程（绝对通俗易懂！）【小土堆】](https://www.bilibili.com/video/BV1hE411t7RN?p=20&spm_id_from=pageDriver&vd_source=b9903dbe1b7c91d693351ba0e40e8aaa)  
 [【pytorch】冻结网络参数训练](http://www.360doc.com/content/19/0926/16/42392246_863349001.shtml)  
 [Python 中的 x for y in z for x in y语法详解](https://zhuanlan.zhihu.com/p/344114093)  
 [Pytorch之requires\_grad](https://blog.csdn.net/weixin_44696221/article/details/104269981)  
 [pytorch中Module模块中named\_parameters函数](https://blog.51cto.com/u_15274944/4939965)  
 [yolov5 介绍](https://www.pudn.com/news/6228d47b9ddf223e1ad1c64b.html)  
 [Python内置函数之enumerate() 函数](https://www.cnblogs.com/yifchan/p/python-1-40.html)  
 [filter（）函数](https://www.cnblogs.com/canneddream/p/14210959.html)  
 [细说Python的lambda函数用法，建议收藏](https://zhuanlan.zhihu.com/p/80960485)  
 [微调 — 冻结网络参数](https://blog.csdn.net/baidu_39638008/article/details/121748296)  
 [Pytorch之requires\_grad](https://blog.csdn.net/weixin_44696221/article/details/104269981)

【欢迎指正】