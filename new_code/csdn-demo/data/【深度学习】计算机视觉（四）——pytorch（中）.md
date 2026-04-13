# 【深度学习】计算机视觉（四）——pytorch（中）

#### 文章目录

* [一、torchvision](#torchvision_14)
* + [1： torchvision.datasets](#1_torchvisiondatasets_17)
  + - [CIFAR10](#CIFAR10_22)
  + [2：torchvision.transforms](#2torchvisiontransforms_82)
  + [3：torchvision.io](#3torchvisionio_85)
  + [4：torchvision.utils](#4torchvisionutils_87)
  + [5：torchvision.models](#5torchvisionmodels_89)
  + [6：torchvision.ops](#6torchvisionops_91)
* [二、torch（上）——torch.utils](#torchtorchutils_94)
* + [1：torch.utils.tensorboard](#1torchutilstensorboard_95)
  + [2：torch.utils.data](#2torchutilsdata_98)
  + - [（1）Dataset](#1Dataset_100)
    - [（2）DataLoader](#2DataLoader_102)

上一单元的学习比较混乱，很多模块之间的关系没有搞清楚，pytorch（中）以及pytorch（下）会以模块关系梳理的结构比较清晰系统地进行。CV主要有两个包：

1. **torchvision**  
    包含transforms（图片处理）、datasets（内置数据集）、io（输入输出）、utils（实用工具）、models（网络模型）、ops（特殊操作）等。
2. **torch**  
    包含utils（实用工具）、nn（神经网络）等。其中utils中又包含tensorboard（用于过程调试）、data（数据集）。

在pytorch（上）学习的基础知识部分，涉及到的图片处理、数据集处理，都是包含在上述两个包内的。我所理解torchvision主要就是一些封装的工具，便于进行CV项目的编写，而torch更主要是为神经网络服务的，它定义了神经网络的一些架构。

*本文章开头的总结是我自己的理解，所以知识结构和话术可能不严谨。*

一、torchvision
-------------

根据pytorch处理的数据类型不同，分为几个模块：**torchaudio**、**torchtext**、**torchvision**等，我之前下载的就是torchvision，这次的学习也主要以视觉为主。  
 下面介绍torchvision中的常用模块。

### 1： torchvision.datasets

torchvision中的常用数据集了解：

1. COCO：常用于目标检测和语义分割。
2. MNIST：手写文字数据集。
3. CIFAR10：用于物体识别。

#### CIFAR10

CIFAR10中包括六万张32x32像素的彩色照片，共有10个类别，每个类别有六千张图像。其中5万张训练图片，1万张测试图片。

基础操作：

```
from torchvision import datasets

"""
torchvision.datasets.CIFAR10(root, train, transform, target_transform, download)

参数说明:
root：string类型，数据集的位置
train：bool类型，若为true则表示训练集，否则表示测试集
transform：对数据集的操作
target_transform：对target进行transform操作
download：bool类型，若为true可以之间从网上下载。
"""

# 构造训练集
train_set = datasets.CIFAR10(root="./dataset", train=True, download=True)
# 构造测试集
test_set = datasets.CIFAR10(root="./dataset", train=False, download=True)
# 查看数据集
print(test_set[0])
'''
输出为：
(<PIL.Image.Image image mode=RGB size=32x32 at 0x1DC608371D0>, 3)
其中”3“参数表示数据的target，由于数据集中对target放在了一个列表里，每个target对应一个数字。列表如下：
['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
所以3表示cat。
'''
img, target = test_set[0]  # 分别获得img和target
```

与transforms结合使用（我不想下载了，所以只抄了代码没有运行结果）：

```
from torchvision import datasets
from torchvision import transforms
from torch.utils.tensorboard import SummaryWriter

dataset_transform = transforms.Compose(
    [transforms.ToTensor]
)

# 构造tensor类型的训练集
train_set = datasets.CIFAR10(root="./dataset", train=True, transform=dataset_transform, download=True)
# 构造tensor类型的测试集
test_set = datasets.CIFAR10(root="./dataset", train=False, transform=dataset_transform, download=True)

writer = SummaryWriter("datasets_transforms_logs")
for i in range(10):
    img, target = test_set[i]
    writer.add_image("test_set", img, i)

writer.close()
```

### 2：torchvision.transforms

用于图片的处理，之前已经学习过。  
 详见笔记：[深度学习（三）——pytorch（上）](https://blog.csdn.net/RK_Dangerous/article/details/126010312)

### 3：torchvision.io

用于输入输出。

### 4：torchvision.utils

里面有很多实用的工具，类似torch.utils。

### 5：torchvision.models

一些常见的神经网络。

### 6：torchvision.ops

一些特殊操作。

二、torch（上）——torch.utils
-----------------------

### 1：torch.utils.tensorboard

utils有很多实用的类和工具，比如之前学的Tensorboard就是。  
 详见笔记：[深度学习（三）——pytorch（上）](https://blog.csdn.net/RK_Dangerous/article/details/126010312)

### 2：torch.utils.data

这里有很多关于数据集的操作，比如之前学的Dataset类。

#### （1）Dataset

详见笔记：[深度学习（三）——pytorch（上）](https://blog.csdn.net/RK_Dangerous/article/details/126010312)

#### （2）DataLoader

Dataset是获取到了一整个数据集，DataLoader可以从数据集中取若干个数据打包（可取若干次且不重复），是将数据们的img和target分别打包然后一起返回。因为我觉得对自己的数据集去操作比较重要，所以我还是自己弄的数据集，代码和教程中不太一样。

```
import os
from PIL import Image
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from torchvision import transforms


# 新建Dataset
class MyData(Dataset):
    def __init__(self, root_dir, label_dir):
        self.root_dir = root_dir
        self.label_dir = label_dir
        self.path = os.path.join(self.root_dir, self.label_dir)
        self.img_path = os.listdir(self.path)

    def __getitem__(self, idx):
        img_name = self.img_path[idx]
        img_item_path = os.path.join(self.path, img_name)
        img = Image.open(img_item_path)
        trans_tensor = transforms.ToTensor()
        return trans_tensor(img), self.label_dir  # 返回tensor类型的数据集而不是PIL.image

    def __len__(self):
        return len(self.img_path)


Sing_label_dir = "Sing"
Sing_dataset = MyData("hzhfData", Sing_label_dir)
# 注意：DataLoader要求数据集中的每个图片的大小都一样，我这里提前全部都裁剪成了300x300

"""
DataLoader的重要参数说明：
dataset: 实例化的Dataset
batch_size: 每次取几个
shuffle: 是否打乱，若为True表示打乱，默认为False
sampler: 
batch_sampler: 
num_workers:用于设置多进程，默认为0（使用主进程）。注意在Windows可能会报错BrokenPipeError
collate_fn: 
pin_memory: 
drop_last: 若设置一次取多个，当最后一次取不够时是否舍去，为Ture则舍去不取。
timeout: 
worker_init_fn: 
generator: 
prefetch_factor: 
persistent_workers: 
"""

# 对自定义的数据集进行操作
# 设置DataLoader并返回
test_loader = DataLoader(Sing_dataset, batch_size=2, shuffle=True, drop_last=True)
# 获得DataLoader中的每一次打包
for data in test_loader:
    imgs, targets = data
    print(imgs.shape)
    print(targets)
"""
输出：
torch.Size([2, 3, 300, 300])  # 第一次选取共2张图片，3个通道，高为300，宽为300
('Sing', 'Sing')  # 第一次选取，每张图片的标签
torch.Size([2, 3, 300, 300])  # 第二次选取
('Sing', 'Sing')
"""
```

可以通过tensorboard更直观地查看：

```
import os
from PIL import Image
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from torchvision import transforms
from torch.utils.tensorboard import SummaryWriter


# 新建Dataset
class MyData(Dataset):
    def __init__(self, root_dir, label_dir):
        self.root_dir = root_dir
        self.label_dir = label_dir
        self.path = os.path.join(self.root_dir, self.label_dir)
        self.img_path = os.listdir(self.path)

    def __getitem__(self, idx):
        img_name = self.img_path[idx]
        img_item_path = os.path.join(self.path, img_name)
        img = Image.open(img_item_path)
        trans_tensor = transforms.ToTensor()
        return trans_tensor(img), self.label_dir

    def __len__(self):
        return len(self.img_path)


Sing_label_dir = "Sing"
Sing_dataset = MyData("hzhfData", Sing_label_dir)

# 设置drop_last为不舍弃，通过logs查看结果
test_loader = DataLoader(Sing_dataset, batch_size=2, shuffle=True, drop_last=False)

writer = SummaryWriter("logs")
for epoch in range(3):  # 设置三轮选取，迭代完一轮后会再次打乱
    step = 0
    for data in test_loader:
        imgs, targets = data
        writer.add_images("Epoch:{}".format(epoch), imgs, step)  # 这里format格式化字符串，用{}来标明被替换的字符串
        # 注意这里因为有多张图片，要用add_images()而不是add_image()，我忽略了这个细节所以一直报错
        # add_image()要求tensor的shape是CHW形式，如[3, 300, 300]，2张图片时tensor的shape是[2, 3, 300, 300]
        step = step + 1
writer.close()
```

可以看到使用DataLoader打包后图片会一起展示，两轮的图片顺序不一样。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3ad5433378a11d74dc6ea7cfe1483cc1.png)  
 拖动滑块至最后一个step：图片不足一次取的数量的时候，因为设置了不舍弃，所以最后只有一个图片。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b3afbed9bd1883215b2796ad0d63f1be.png)