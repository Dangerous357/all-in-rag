# 【深度学习】计算机视觉（七）——使用GPU进行目标检测详解（上）

1. 使用GPU训练
----------

一直在纠结把GPU的使用放在哪里，觉得放在pytorch那里也不太合适，所以就放在这里了。  
 按照唱歌和不唱歌太难区分了，所以我用星黛露和草莓熊新建的训练集：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6a8ccd85608bae6472c36fff02eebe30.png)  
 测试集：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/596632c8bd48257b8f30cb6c7f9bd269.png)

### 方法一

使用GPU训练需要在：①网络模型、②损失函数、③数据，三个地方调用`.cuda()`即可。严谨一点，我们需要加上判断`torch.cuda.is_available()`。完整代码如下：

```
import torch
from torch.nn import Sequential, Conv2d, MaxPool2d, Flatten
import os
from PIL import Image
from torch import nn
from torch.nn import Linear, ReLU
from torch.utils.data import Dataset, DataLoader
from torchvision.transforms import transforms


class MyModule(nn.Module):
    def __init__(self):
        super(MyModule, self).__init__()
        self.seq = Sequential(
            Conv2d(3, 32, 5, padding=2),
            ReLU(),
            MaxPool2d(2),
            Conv2d(32, 32, 5, padding=2),
            ReLU(),
            MaxPool2d(2),
            Conv2d(32, 64, 5, padding=2),
            ReLU(),
            MaxPool2d(2),
            Flatten(),
            Linear(1024, 64),
            Linear(64, 2)
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


# 导入训练集
train_dataset = MyData("hzhfData", 'Train32')
train_loader = DataLoader(train_dataset, batch_size=1)

# 导入测试集
test_dataset = MyData("hzhfData", "Test")
test_loader = DataLoader(test_dataset, batch_size=1)
total = len(test_loader)

# 神经网络
module = MyModule()
if torch.cuda.is_available():
    module = module.cuda()

# 损失函数
loss = nn.CrossEntropyLoss()
if torch.cuda.is_available():
    loss = loss.cuda()

# 优化器
learning = 0.01
optim = torch.optim.SGD(module.parameters(), lr=learning)  # 参数直接调用网络中的parameters

# 开始训练
for epoch in range(30):

    # 训练
    module.train()
    for data in train_loader:  # 这个for循环可以看成是做题和学习的过程，每循环一次就做一道题，就相当于一个周期
        imgs, targets = data
        if torch.cuda.is_available():
            imgs = imgs.cuda()
            targets = targets.cuda()
        outputs = module(imgs)  # 将打包的图片前向传播得到得分函数
        result = loss(outputs, targets)  # 用得分函数和正确标签计算损失函数
        optim.zero_grad()  # 因为backward计算时会累加上一次的结果，我们需要清空上次计算的权重再训练
        result.backward()  # 利用反向传播计算权重
        optim.step()  # 对每个参数进行调整

    # 测试
    module.eval()
    right = 0  # 记录正确分类的个数
    with torch.no_grad():
        for data in test_loader:
            imgs, targets = data
            if torch.cuda.is_available():
                imgs = imgs.cuda()
                targets = targets.cuda()
            outputs = module(imgs)  # 得分情况
            right = right + (outputs.argmax(1)==targets).sum()  # 计数
    accuracy = right / total  # 准确率
    if (epoch+1) % 5 == 0:
        print("第{}轮训练的正确率为：{}".format(epoch+1, accuracy))
```

得到结果：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/be1b44698512102d2166439eada78946.png)  
 由于每次初始参数是随机的，所以每次运行程序的结果不太一样。但是基本属30次就可以达到100%正确。显然我的数据集数量是不够的，反正先学会就行。

### 方法二

和方法一类似。我们先新建一个设备`device = torch.device("cuda:0")`，其中数字表示电脑的第几个显卡，如果只有一个显然只能选择0，也可以简写为`device = torch.device("cuda")`。然后将方法一中所有的`.cuda()`全部换成`.to(device)`即可。

2. 目标检测进阶（上）
------------

> 目标检测可以理解为是物体识别和物体定位的综合，不仅仅要识别出物体属于哪个分类，更重要的是得到物体在图片中的具体位置。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/364f0f5865209de8cefea2621d66ce6f.png)

### 2.1 重要概念

**目标检测的分类有两种方式：**

1. **是否存在候选区**：按照是否存在候选区分类可以分为**两阶段目标检测算法**和**一阶段目标检测**算法。两阶段目标检测算法的第一级网络用于候选区的提取，产生候选区域（region proposals），第二级网络用于对候选区进行分类和回归（一般还需要对位置精修）。一阶段目标检测算法不对候选区进行提取，只用了一级网络就完成了分类和回归。
2. **是否存在先验框**：按照是否存在先验框分类可以分为**基于锚框的目标检测算法**和**无锚框的目标检测算法**。基于锚框的目标检测算法首先建立不同长宽比的检测框，然后对锚框中的内容进行分类和回归。无锚框的目标检测算法是基于中心区域和关键点的目标检测算法，取消了锚框生成机制，加快了速度。

**如何理解候选区和先验框的区别呢？** 候选区是以“很可能有目标物体”去设置的，而先验框是以“不管有没有目标物体我先画很多框”去设置的。  
 还有一个特点在多分类任务中体现地比较清晰，候选区（以Faster R-CNN为例），区域建议网络RPN(Regional Proposal)不负责图像的分类，它只负责选取出图像中可能属于数据集其中一类的候选区域，接下来就是把RPN产生的候选区域输入到分类网络中进行最终的分类。先验框（详见本文2.2内容）是以每个像素为中心画框，所有这些初始框都不能确定是否包含目标物体。

**各类目标检测算法总结如下：**

| 算法类别 | 机制 | 优势 | 局限性 | 适用场景 | 经典网络 |
| --- | --- | --- | --- | --- | --- |
| one-stage | 不生成候选区,直接进行分类和回归 | 实时性高 | 成群目标和小目标检测精度低 | 实时目标检测 | SSD；Yolo系列；Retina-Net |
| two-stage | 先生成候选区，再对候选区进行分类和回归 | 算法精确度高 | 实时性差，检测小目标效果差 | 高精度目标检测 | R-CNN；SPPNet；Fast R-CNN；Faster R-CNN；Mask R-CNN |
| Anchor-Based | 先生成锚框，对锚框进行分类和回归 | 技术较成熟 | 算法泛化能力差，训练效率低 | 通用目标检测 | R-CNN；Fast R-CNN；Faster R-CNN；SSD |
| Anchor-Free | 根据中心点和关键点生成边界框 | 算法泛化能力强，检测小目标精度高 | 不适合进行通用目标检测，精度低于基于锚框的算法 | 多尺度目标检测，小物体目标检测 | Yolov1；Yolov2；CenterNet；CornorNet；Fcos |

### 2.2 基于锚框的检测算法

一类目标检测算法是基于锚框，预测每个锚框里是否含有关注的物体，如果是，预测从这个锚框到真实边缘框的偏移。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a96115ef7fc83b46b6da7e9950ff9772.png)

#### 2.2.1 IoU：交并比

> Intersection over Union（IoU）是一种测量在特定数据集中检测相应物体准确度的一个标准。IoU是一个简单的测量标准，只要是在输出中得出一个预测范围(bounding boxes)的任务都可以用IoU来进行测量。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9dd5ec13c2e96f5fbdd9d9f878f91469.png)  
 IoU用来计算两个框之间的相似度，可以用杰卡德系数（Jaccard Index）来理解。

> **杰卡德系数**，又称为杰卡德相似系数，用于比较两个样本之间的差异性和相似性。杰卡德系数越高，则两个样本相似度越高。

给定两个集合A和B，其杰卡德系数为：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/acafa860087d9599359a7fee57529c8f.png)  
 值为0表示无重叠，1表示完全重合。

#### 2.2.2 基于锚框的检测的训练

在训练集中，我们需要给每个锚框两种类型的标签。一个是预测锚框中是否含有要检测的物体，另一个是锚框相对于边界框的偏移量（offset）。这里简单说一下算法的原理：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0ae4be7f1681070ae28cb38e9484e264.png)  
 首先输入图片中包含感兴趣的对象以及它真实的标注，这里用绿色方框表示出来了。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/bb3cc471386e810427ddaa1625fff565.png)

所以注意锚框不是像上图一样把图片简单的分割的，可能会有很多的锚框重叠、交叉等等，此时得到的锚框可以认为是最初的检测结果，然后需要筛选。

> 在训练集中，我们将每个锚框视为一个训练样本。 为了训练目标检测模型，我们需要每个锚框的类别（class）和偏移量（offset）标签，其中前者是与锚框相关的对象的类别，后者是真实边界框相对于锚框的偏移量。 在预测时，我们为每个图像生成多个锚框，预测所有锚框的类别和偏移量，根据预测的偏移量调整它们的位置以获得预测的边界框，最后只输出符合特定条件的预测边界框。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/42751806f0ad8e314fa9d6fc5f6ceb77.png)  
 对锚框进行分类，即对这9个锚框分类哪些是背景，哪些是前景。如图，我们这里通过筛选得到了一个属于感兴趣对象的锚框，其他框就舍去了。这里简单介绍一个常用的分类算法：  
 我们的任务就是把锚框看成训练样本，对锚框进行分类，要么标注为背景（负类样本），要么关联上一个真实的**边缘框**。

> **边缘框（bounding box）** 是图片中物体的真实位置和范围，有两种表示方式，一种是边角坐标表示法，通过物体左上和右下两个角的坐标表示一个矩形框，还有一种是中心表示法，用物体的中心和宽高表示矩形框。

分类的时候，我们需要对锚框标号，如图，使用一个矩阵，列表示所有的边缘框，行表示所有的锚框。例如此处的边缘框是4个，锚框是9个。用每一个锚框和每一个边缘框计算IoU值组成的矩阵x。首先要找到矩阵中的x最大值，例如此处为x23，那么就把锚框2与边缘框3关联起来。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/03880941f02667d98985e9e86e3731b0.png)  
 找到边缘框3对应的锚框之后，我们需要找其他的边缘框对应的锚框。忽略边缘框3所在的列和锚框2所在的行（因为边缘框3和锚框2都已经匹配了，不可能再匹配其他的了），在剩下的矩阵值中再找最大值。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e8b6967bff49e2443d29a7f954bd7b3f.png)  
 例如x71是此时的最大值，那么就把锚框7和边缘框1关联起来。以此类推，直到我们将所有的边缘框都找到一个锚框对应。而剩余的锚框可以全部看作是负类样本，但通常我们设置一个threshold（阈值），遍历剩余的所有锚框，找到每一个锚框与其他边缘框的最大IoU，如果最大IoU都小于这个阈值，那就把它看成背景，否则可以认为是该边缘框的类别（即使之前已经找到了最合适的锚框对应这个边缘框）。这里注意，如果狗用0表示，猫用1表示，即类别数组为[0, 1]，在实际标记锚框的过程中，我们需要将背景表示为0，其他类别的标签均+1，即类别数组为[0, 1, 2]分别表示背景、狗、猫。

我们将锚框与边缘框对应就是标记类别的过程，显然可以直接把锚框标记为关联的边缘框表示的类别，然后就需要计算它的偏移量。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/748273aa82f5cb6a37bf3dc5f8b73b30.png)  
 回到这个例子，得到匹配的锚框后，需要进行锚框的回归，即对它的位置和大小进行调整，使它更接近真实的标注。

> 鉴于数据集内不同的框的位置和大小不同，我们可以对那些相对位置和大小应用变换，使其获得分布更均匀且易于拟合的偏移量。

一种常用的方法表示偏移量是：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/db4ea28cf9ca62643f7bd46610b11a69.png)  
 在修正的过程中，我们给正类样本设置掩码为`[1, 1, 1, 1]`，负类样本设置掩码为`[0, 0, 0, 0]`，偏移量和掩码都类似于锚框坐标的系数，所以数据与4个偏移分量对应，通过元素乘法，掩码变量中的零将在计算目标函数之前过滤掉负类偏移量。

（我的理解，不知道对不对），锚框的回归即偏移量的计算像分类问题一样，用锚框加偏移量得到的预测框与真实边界框之间的损失、锚框分类的损失共同作用为整个模型的损失，在减小损失的过程中得到参数的合适值。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f8b61cc39649b2561ed05a83a808e093.png)  
 全过程如下：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d57bf7a7b7813a0cd802c64c4acf1cd2.png)  
 我们可以用回归后的锚框作为初始框再次进行学习，级联地重复这个过程，如果是多次级联称为多阶段法，多阶段法是高精度的；如果只进行一次，称为单阶段法，单阶段法是高效率的。

#### 2.2.3 基于锚框的检测的预测

在预测时，我们先为图像生成多个锚框，再为这些锚框一一预测类别和偏移量，接着根据预测的偏移量调整锚框位置从而得到预测边界框，最后筛选需要输出的预测边界框。我们**将锚框和偏移量预测作为输入，并应用逆偏移变换来返回预测的边界框坐标**。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a42cc96fc163a67a983b4fcc7e5a6963.png)  
 我自己的理解：  
 在训练时，我们可以将锚框的训练和图像分类的训练分开。已知输入图像的边缘框，可以先根据边缘框训练如何画锚框，得到设计锚框的合适的相关参数。然后将真实边缘框裁剪下来作为输入，再去对它进行分割、特征提取和学习，而不是对一整个包含很多目标物体的图片进行学习。

举个例子，这是一个小鸡的训练集：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ca43c32aef600168812f8607b16fdf92.png)  
 在训练的时候，我们可能以某一像素点T为中心画了很多锚框，这些锚框有不同的缩放比、宽高比。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1c277a71371d0f8ab77cd2cbaca5679d.png)  
 根据“基于锚框的检测的训练”中的方法，找到了一个真实边缘框关联的锚框，然后得到了偏移量。根据多次反复的学习（因为训练集的数据量很大，会得到很多锚框的尺寸和偏移量，可以对这些数据进行拟合，找到几组合适的参数）我们就得到了设计锚框的方法。仍以第一个小鸡为例，我们去进行特征提取，这里顺便复习一下：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1ec93f384d7aeaa865db9608bd16809f.png)  
 首先分成多个区域，由于每个区域的贡献不同，赋予不同的滤波器去提取每个区域的特征。经过学习我们就可以得到卷积核和偏置参数。

预测时，我们根据上面对于锚框的训练可以得到一些参数，这些参数是对锚框的尺寸和偏移量进行设置，能够较好地拟合数据集。我们仍使用训练锚框的方法，以每个像素为中心，以学习得到的尺寸和偏移量设置锚框，得到很多很多的锚框，每个锚框看成是一个输入，对该区域的像素进行分类，得到预测结果。然后只要将概率非常小的锚框舍弃，就可以留下一部分粗略的预测结果。

举个例子，还是小鸡。假设我们已经得到了两组设计锚框的参数，我们以每一个像素为中心去画锚框，会得到非常多的锚框。由于画出来的锚框太多了，所以这里以两个点T1和T2为例：![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3cc83a30d17dfe9ba329c2788419357c.png)  
 我们将得到的锚框作为输入，去计算这个框能够被分类为小鸡的概率。假如绿色框概率为0.86，蓝色框概率为0.90，粉色框概率为0.15，黄色框概率为0.14，显然我们可以通过设置一个阈值删掉不满足条件的锚框，即将它们视为负类锚框。留到最后的锚框，就是我们目标检测的一个粗略结果（为什么是粗略，因为还要有优化呀！但是这里只是为了理解锚框检测的过程，所以不详细讲了。）  
 这样就很好的将“锚框的训练和预测”与“图像的训练与预测”结合起来，得到的结果（局部）可能是这样的：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/777acce837700e4118420b602ef05840.png)  
 这是一组锚框参数`(si, rj)`以不同的像素为中心预测到的可能是小鸡类的区域。

这是我刚开始自己的理解，但是根据查阅资料，我发现锚框并不是遍历了每一个像素点。

> Anchor box 通常是以CNN提取到的Feature Map 的点为中心位置

Feature Map就是图像经过滤波器处理后得到的特征图。以Faster R-CNN为例，就是说假如我们对输入的图像下采样了16倍，也就是Feature Map上的一个点对应于输入图像上的一个16×16的感受野，我们在原图上画锚框，由于Faster R-CNN给定了三组s和三组r，所以这个点最多可以在原图上画出9种锚框。由此可见和我之前想的不太一样，我们首先对图片进行卷积操作，然后标注锚框（这样可以大大减少锚框的数量），再进行分类。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7331a6080e75c2719ba9e2a3ffd4da27.png)  
 回到开头，将锚框和偏移量预测作为输入，并应用**逆偏移变换**来返回预测的边界框坐标。这里就可以理解了，锚框是不进行偏移的，就是我们根据像素点直接生成的那个框，只是得到了锚框和偏移量，根据公式算出来的边界框才是最后的结果，然后根据这个结果再去分类。为什么叫做逆偏移变换呢？大概是因为计算偏移量时，已知锚框和边界框，而已知偏移量和锚框去求边界框的坐标，就是逆偏移了。

##### NMS：非极大值抑制

在实际预测的时候，会得到很多锚框，如图：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d36f3a36eefd9ca0078cb531e4d60f16.png)  
 这些锚框都是我们预测的边缘框，使用NMS可以合并相似的预测。首先选中某一非背景类的最大值，例如dog=0.9，然后计算其他锚框与该锚框的IoU值，并设置一个阈值。若计算得到的IoU大于阈值，说明相似度太高，即这些框高度重叠，去掉这些锚框。重复上述过程，直到所有锚框要么被选中，要么被去掉。  
 官方的说法如下：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5849dac12128c300a9fb12f18faaf480.png)  
 我在思考像上面那张图片，一个小鸡藏在另一个小鸡后面，我们用两个中心位置距离很大的锚框，其实是可以区分出来的，虽然它们重合度非常高。类比到其他分类的情况，如果两个物体很难完全重合，比如花草树木的形态可能是直立或者倾斜，又或是并排，那么我们即使是以同一中心点，绘制宽高比不同的锚框，或者以不同中心点绘制同样的锚框，也能很好地区分两个物体。可见我对于IoU会不会误判这个想法多虑了，我们绘制的锚框数量是巨大的，就算去掉了很多重复度很高的锚框，也能留下足以区分两个物体的两个锚框。

#### 2.2.4 总结

在这里需要复述一遍基于锚框的检测算法，如果复述不下来，上面的内容再看一遍！  
 由于上述内容是我在初学时的笔记，有很多不太清楚的地方、找不到教程的地方是加入了我自己的理解，所以可能会存在错误的理解和表述（因为现在没时间再从头到尾检查一下）。后面复习的时候又看了一篇文章[单阶段目标检测模型YOLO-V3](https://www.bookstack.cn/read/paddlepaddle-tutorials/spilt.3.e8213770efa524bc.md)，利用yolo模型更细致地学习。

### 2.3 目标检测的评价指标

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f97b5e683521cb8948ddae746b2472fe.png)  
 注意正例在目标检测中一般是满足`IoU>=设置阈值`的。

* **精确率**（precision）：如上图，文字理解是指在所有检测到的样本物体中正样本的比例；
* **准确率**（accuracy）：准确率是指有在所有的判断中有多少判断正确的，`Acc = (TP+TN) / (TP+TN+FN+FP)`；
* **召回率**（recall）：如上图，文字理解是指本应检测出的正确物体（所有目标对象）中正确检测到的比例；
* **帧率每秒**（Frames Per Second，FPS）：每秒识别图像的数量，用于评估目标检测模型的检测速度；
* **P-R曲线**：以Recall、Precision为横纵坐标的曲线；
* **平均精度**（Average Precision，AP）：对不同召回率点上的精确率进行平均，在PR曲线图上表现为某一类别的 PR 曲线下的面积；
* **平均精度均值**（mean Average Precision，mAP）：所有类别AP的均值。

以下是一些重要概念的详解。

**F1-score**  
 F1分数（F1-score）是分类问题的一个衡量指标。一些多分类问题的机器学习竞赛常常将F1-score作为最终测评的方法。它是精确率和召回率的**调和平均数**，最大为1，最小为0。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2bc6fa74af35d7e411b1e5df220ea8c8.png)

> 调和平均数（harmonic mean）又称倒数平均数，是总体各统计变量倒数的算术平均数的倒数。  
>  ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/19d520c09f058c99a9470a6a563a55cb.png)  
>  算术平均数和调和平均数是平均指标的两种表现形式。不能根据同一资料既计算算术平均数，又计算调和平均数，否则就是纯数字游戏，而非统计研究。

算术平均数和调和平均数的用法根据实际意义有不同的应用，调和平均数主要用于解决在无法掌握单位总数的情况下，只需要每组的变量值和对应的总标记数，需要求平均值的问题。如下图，对于不同情况，列出的式子符合两种平均数的定义，表示不同的“平均”值。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/292473490c0426a212c47efa7ec12645.png)  
 那么放在这里，我们所求的是精确率和召回率的调和平均数，可以简单分析其意义。可以与上述例题对应着看，查准率`TP/P`对应乙种糖果`每元/1.5公斤`，即每TP反映P；查全率`TP/(TP+FN)`对应丙种糖果`每元/2公斤`，即每TP反映（TP+FN）。我们要求平均值，即求TP和总值的平均关系，如果我们各拿出一个单位的TP，算每TP反映多少总值，即为例1中各买1元问每元可买多少公斤；但我们的应用场景是根据分母去评价分子，所以我们不能以TP为单位来计算，我们各拿出一个单位的分母，然后再算每TP反映多少总值，即在已知公斤的情况下算平均数，这样得到的就是平均了两种标准（查准率和查全率）的准确率F1-score。可以看到公式中查准率和查全率的分母是不同的，显然不能简单的相加，要通分，也就可以理解为什么要用倒数计算，所以调和平均数的意义可能就在于我们要算的平均数分母意义不同时去标准化。

**PR曲线**  
 PR曲线中的P代表的是precision（精准率），R代表的是recall（召回率），其代表的是精准率与召回率的关系，一般情况下，将recall设置为横坐标，precision设置为纵坐标。  
 我们需要多次改变阈值后重新对样本进行分类，每一次实验都计算其查准率和查全率，并以此作为坐标值在平面坐标图上标示出来，通过大量的检索，就可以得到检索系统的性能曲线。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b682fe2805728e2251e8c7cb845afbbb.png#pic_center)  
 根据我的观察，一般PR曲线的都大致是一个递减趋势，在查全率和查准率之间存在着相反的相互依赖关系，如果提高输出的查全率，就会降低其查准率。相对来说，PR曲线越靠近右上角效果越好。  
 我们对不同的深度学习模型A和B进行评价，如果A的PR曲线能够完全包住B的PR曲线，即说明A的性能更优。但如果A和B的曲线交叉，难以判断哪个模型更好，一般利用 **平衡点（BEP）** 的概念。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/be22f92839f11941460c38b6194714ad.png)  
 平衡点是P=R时的取值（斜率为1），此时`BEP=P=R=F1`，BEP越大，我们可以认为该学习器的性能较好。

### 2.4 图像的预处理操作

#### 2.4.1 零中心化、归一化和标准化

##### 零中心化

**零中心化的概念：**  
 **零中心化**也叫**均值减法**、**零均值化**。零中心化指的是令处理后的数据均值为0的过程，从数学上说就是令每一个维度的数据减去该维度上数据的均值。如果在图像领域，一般有两种处理方法：

1. 可以将三通道的像素值减去整幅图像的均值；
2. 也可以三通道的像素值分别减去各自通道的均值。

为什么要进行零中心化呢？接下来的知识点有点散，可能左一句右一句的。

* 以激活函数Relu为例，当`x≤0`时，`f(x)=0`、f’(x)=0；当`x>0`时，`f(x)=x`、f’(x)=1，如下图：![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/8c3d8b5051ec3d2f335817989e1f37a2.png)
* 当输入数据不做零中心化时，由于输入图像范围在`[0, 255]`，显然输入都大于零；而进行零中心化后，数据有正有负。
* 我在最开始说神经网络的表达式为`ωx+b`，我以为是要把图片全部拆成全连接网络结构；后来才认识到，大部分都是卷积网络，权重是通过滤波器体现的，经过`k×k`的卷积核后得到新的输出，推翻了我之前`ωx+b`的认识；经过这里的学习，我发现其实我中间阶段的认识不全面，因为显然我没有把卷积的过程公式化，要想正确认识神经网络的计算就要先明确如何用数学公式表达出来每次卷积，我们发现其实一张图片经过卷积，虽然每个像素都发生着复杂的变化，但是这些变化叠加在一起，效果其实和每个像素都使用了`ωx+b`一样，可见“全连接”和“`ωx+b`”并没有绝对的联系，所以我们把前面两种理解结合起来看，神经网络并没有每一层都拉开成全连接的结构，但是每一层的计算公式都可以表示为：  
   ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/27e5ab4a2cb5bcf6d25f97bf5a618ddf.png#pic_center)
* 参考【李飞飞CS231n part4：Introduction to Neural Networks】，之前在反向传播时讲到我们可以运用链式法则，以神经网络第一层隐藏层为例，损失函数反向传播时计算权重的梯度可以表示为（其中f为Relu函数）：

![其中f是激活函数Relu，由于f对](https://i-blog.csdnimg.cn/blog_migrate/6395cf25bb814c527af995786e375cbc.png#pic_center)  
 所以在这里，有很多文章说上层传下来的梯度是不变的，我认为作者的表述是有问题的，不是不变而是如果输入已经确定的时候上层传下来的梯度也确定。假设最简单的情况，网络只有一层卷积+激活函数，如果损失函数最高次数为1，那么损失函数对激活函数的偏导数就是f的系数，这样上层传下来的梯度不变，但我们所知有很多损失函数是2次方的，那么损失函数对激活函数的偏导数势必会受f的值的影响，如果输入不同的x，会得到不同的f进行前向传播，又会改变反向传播的结果。

##### 归一化

**归一化的概念：**

> 归一化是一种简化计算的方式，即将有量纲的表达式，经过变换，化为无量纲的表达式，成为标量。 在多种计算中都经常用到这种方法。  
>  归一化是一种无量纲处理手段，使物理系统数值的绝对值变成某种相对值关系。简化计算，缩小量值的有效办法。

**归一化(Normalization)**：将一列数据变化到某个固定区间(范围)中，通常，这个区间是[0, 1]，广义的讲，可以是各种区间，比如映射到[0，1]一样可以继续映射到其他范围，图像中可能会映射到[0,255]，其他情况可能映射到[-1,1]。（我理解的，之前使用softmax分类器得到的每个类别的概率，就很像归一化的作用）**最大最小值归一化**（简称归一化）的变换方法为：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/94ab513d9fb1f4ce89f3b93e2221c51b.png)  
 另一种**均值归一化**的变换方法为：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/967b57a92eb1c4004f047cca7e018c65.png)  
 其实就是零中心化除以数据的标准差。

##### 标准化

**标准化的概念：**  
 **标准化(Standardization)**：将数据变换为均值为0，标准差为1的分布（标准差能够反应一个数据集的离散程度），变换后依然保留原数据分布。**标准化又叫z值归一化**，其变换方法为：![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/35e124d86e431fd7a638a087099f510b.png)  
 如何将归一化运用到计算机视觉中呢？可以使用OpenCV中的`normalize()`进行归一化。举个例子（以最大最小值归一化为例）：

```
import cv2
import numpy

image_path = "xdl.jpg"  # 星黛露图片的文件名
img_before = cv2.imread(image_path)
cv2.imshow("before", img_before)  # 显示图片
cv2.waitKey(0)  # 因为cv2.imshow()是会闪退的，所以要设置延迟，默认为0毫秒（表示暂停）


print("This is the data before normalization:")
print(img_before)
img_before = numpy.float32(img_before)  # 进行归一化操作要把图片格式变为numpy.float32
img_after = numpy.zeros(img_before.shape, dtype=numpy.float32)  # 创建一个新的img_after存储归一化后的图片

"""
cv2.normalize(src, dst, alpha=None, dtype=None, mask=None)

参数说明：
src：表示输入图像，numpy类型
dst：表示归一化之后的图像，numpy类型
alpha：归一化结果范围中的最大值max，如果norm_type为NORM_MINMAX，则alpha为大值或小值；如果norm_type为其他类型时，则为归一化要乘的系数
beta：归一化结果范围中的最小值min，如果norm_type为NORM_MINMAX，则beta为和alpha对应的小值或大值；如果norm_type为其他类型beta被忽略，一般传入0
norm_type：归一化方法如NORM_MINMAX、NORM_INF、NORM_L1、NORM_L2，默认最大最小值归一化（NORM_MINMAX）
dtype：归一化之后numpy的数据类型，默认类型与src相同，一般选择cv2.CV_32F
mask：遮罩层
"""

cv2.normalize(img_before, img_after, alpha=1, beta=0, norm_type=cv2.NORM_MINMAX)

print("This is the data after normalization:")
print(img_after)
cv2.imshow("after", numpy.uint8(img_after))
cv2.waitKey(0)

print("This is the data after normalization and ×255:")
print(img_after*255)  # 如果要得到原图，通过改变img的系数重新设置图像范围为0-255（但不能完全恢复，具体原因可分析归一化公式）
cv2.imshow("after*255", numpy.uint8(img_after*255))
cv2.waitKey(0)

print("This is the data after normalization and ×150:")
print(img_after*150)
cv2.imshow("after*150", numpy.uint8(img_after*150))
cv2.waitKey(0)

cv2.destroyAllWindows()  # 关闭cv
```

代码对应输出的四组图像和img数值分别为：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/81fc653d430eb2476a4b7c3cbda4d9cc.png)  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e673de8e595f12c5930d66653d9d53ae.png)  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/45781c8608b0037fa0738dec9e062453.png)  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0f5d59c72c758e75445658d96ca981a0.png)  
 如何进行图像的标准化操作呢？仍使用OpenCV读取和显示图片举例，并使用tensorflow中的标准化函数进行操作（由于tensorflow还没有系统学习，所以代码中只作了简单注释，能看懂即可），代码和结果如下：

```
import cv2
import tensorflow as tf

image_path = "xdl.jpg"  # 星黛露图片的文件名
img_before = cv2.imread(image_path)
cv2.imshow("before", img_before)  # 显示图片

"""
对图像标准化预处理：
tensorflow.image.per_image_standardization(image)

参数说明：
image：参数表示一个三维的张量（tensor）分别对应图像高、宽、通道
"""

tf.compat.v1.disable_eager_execution()  # 设置tensorflow与旧版本兼容，否则无法使用接下来的函数
image = tf.image.per_image_standardization(img_before)

"""
TensorFlow中只有让Graph上的节点在Session中执行才会得到结果，而且在使用结束后必须关闭Session

手动关闭的方法：
res = a + b
sess = tf.Session()
sess.run(res)  # 执行运算
sess.close()

自动关闭的方法（指定Session的有效范围）：
res = a + b
with tf.Session() as sess:
    sess.run(res)

"""
# 由于tensorflow新版本移除了Session，所以改用tensorflow.compat.v1.Session()
with tf.compat.v1.Session() as sess:
    img_after = sess.run(image)
    print(img_after)
    cv2.imshow("after", img_after)

cv2.waitKey(0)  # 一个程序窗口可以只写一个，所有图片会一起展示
cv2.dsetroyAllWindows()
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/278ca59abe8355bbcd3e9f87f6e58238.png)

#### 2.4.2 图像噪声

图像噪声是指存在于图像数据中的不必要的或多余的干扰信息，图像噪声的产生来自图像获取中的环境条件和传感元器件自身的质量。

**什么是噪声？** 噪声样本大概分为四大类：

* 第一类是粗粒度错误，比如车标成了人；
* 第二类是细粒度错误，一种是特征难区分（比如狼和狗），另一种是有重复的样本（比如一条泰迪可以标成“泰迪”也可以标成“狗”；
* 第三类是背景噪声，一种是单标签图片（比如标签是“人”，但是人只占一小部分图，其他都是背景），另一种是内含多标签的图片（比如一个人抱着一条狗，图片标记为“人”，那狗就是噪声）；
* 第四类是分布不一致错误，比如真实狗数据里面出现一张卡通狗。

**为什么要加入噪声？** 神经网络中噪声的注入可以有很多种，如输入层，隐层，权重，输出层等。输入层注入噪声，其实可以看作是数据集增强的一种手段，本质是一种正则化，为了让训练出的模型能够对抗噪声，让神经网络更加鲁棒。真实数据中噪声是很常见的，如果训练时候不加入噪声，那么测试的时候模型在有噪声的样本上表现将会很差。

根据前面对归一化和标准化的学习，我明白其实计算机视觉方面对图像的操作都是基于每个像素值数字的改动，那么根据我的理解，给图像添加噪声，它的本质也是改变某些像素的值，这样图片上小色块的颜色应该会随之改变。只不过如何改变值、改变哪些值，是设置了约束和规范的，因此有多种添加噪声的方法。同理，不仅有加噪的操作，由于图像采集出现的噪声，我们可以通过去噪进行图像的预处理，从而便于后续对图像的操作。

**一、高斯噪声**

> 高斯噪声是指它的**概率密度函数** 服从高斯分布（即正态分布）的一类噪声。**高斯噪声是几乎每个点上都出现噪声、噪点深度随机的噪声。**

连续型随机变量的概率密度函数，是一个描述这个随机变量z的输出值，“ 在某个确定的取值点附近的可能性 ” 的函数。而随机变量的取值落在某个区域之内的概率则为概率密度函数在这个区域上的积分。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2c92ebb1b39d92dac96804f0fe159e10.png#pic_center)

> 高斯分布，也称正态分布，又称常态分布，记为N（μ，σ2），其中μ，σ2为分布的参数，分别为高斯分布的期望和方差。当有确定值时，p(z)也就确定了，特别当μ=0，σ2=1时，z的分布为标准正态分布。

> 在数字图像中的高斯噪声的主要来源出现在采集期间。 由于不良照明、高温引起的传感器噪声。 用于噪声去除的常规空间滤波技术包括：平均（卷积）滤波，中值滤波和高斯平滑。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/73828c450854c9a43a829f2ce509a324.png)  
 其中z表示灰度值，u表示z的均值，σ表示z的标准差。当z服从高斯分布时，其值有大约70%落在范围[(u-σ),(u+σ)]内，有大约95%落在范围[(u-2σ),(u+2σ)]内。我初步地、通俗地理解就是，在我这个计算机图像中，灰度值在z附近的噪声比例大概有`PG(z±Δ)`这么多。但是我仍然不知道它如何运用到我们的图像中，因此边学习代码边理解。

之前说过“高斯噪声是几乎每个点上都出现噪声、噪点深度随机的噪声”，所以对于每个输入像素，通过与随机数（符合高斯分布的随机数）相加, 得到输出像素，即`Pout = Pin + PG(means,sigma)`，其中PG(means,sigma)表示满足u为means、σ为sigma的高斯分布式，已经是一个已知的图像了。我们知道大概如何运用，接下来要解决的问题显然就是如何设置means、sigma以及如何设置随机数的序列。

```
from PIL import Image
from numpy import *
import random
from torch.utils.tensorboard import SummaryWriter

# 读取图片并转为数组
img = Image.open('xdl.jpg')
writer = SummaryWriter("logs")
im = array(img)
writer.add_image("old", im, 1, dataformats='HWC')

# step1: 设定高斯函数的偏移和标准差
means = 0   # 应该是自己定的输入值，根据什么原理去设定有待进一步学习
sigma = 25  # sigma越大添加的噪声越多、图片损坏的越厉害

# step2: 根据输入像素计算出输出像素
"""
ndarray.flatten(order='C')是对多维数据的降维函数。
numpy.ndarray.flatten的一个函数，返回一个折叠成一维的数组。但是该函数只能适用于numpy对象（即array或者mat），普通的list列表是不行的。
其中，order可选项分别为：
‘C’—— means to flatten in row-major (C-style) order, The default is ‘C’.
‘F’—— means to flatten in column-major (Fortran- style) order
‘A’—— means to flatten in column-major order if a is Fortran contiguous in memory, row-major order otherwise
‘K’—— means to flatten a in the order the elements occur in memory. 

举例体会下面将会要用到的多维数组的操作：
test_array = array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])  # 定义一个3维数组
new_test_1 = test_array.flatten()  # 全部展开，得到[1,2,3,4,5,6,7,8]
new_test_2 = test_array[:, :, 0].flatten()  # 只展开第3维0层，得到[1,3,5,7]
new_test_3 = test_array[1, :, :].flatten()  # 只展开第一维1层，得到[5,6,7,8]
"""
# 分离r通道
r = im[:, :, 0].flatten()  # （切片）第三维0层的全部行和全部列
# 分离g通道
g = im[:, :, 1].flatten()  # （切片）第三维1层的全部行和全部列
# 分离b通道
b = im[:, :, 2].flatten()  # （切片）第三维2层的全部行和全部列
# 新的像素值 = 原像素 + 高斯噪声
for i in range(im.shape[0]*im.shape[1]):
    # shape[0]和shape[1]中存储图像的长、宽信息，shape[0]*shape[1]可得到每个通道一维数组的长度
    pr = int(r[i]) + random.gauss(means,sigma)
    pg = int(g[i]) + random.gauss(means,sigma)
    pb = int(b[i]) + random.gauss(means,sigma)
    # 利用random.gauss(means, sigma)产生高斯随机数，不必要一次性把所有高斯噪声的值都排列出来再统一相加，
    # 因为random就是随机的，它取到每个数的概率就是服从高斯分布，所以每次都用random取到的这些数宏观上看是服从高斯分布的。

    # 由于图像的像素值应在[0, 255]之间，所以对新像素进行值限制或放缩
    if pr < 0:
        pr = 0
    elif pr > 255:
        pr = 255
    if pg < 0:
        pg = 0
    elif pg > 255:
        pg = 255
    if pb < 0:
        pb = 0
    elif pb > 255:
        pb = 255

    # 重新赋值给提取的三个通道
    r[i] = pr
    g[i] = pg
    b[i] = pb


im[:, :, 0] = r.reshape([im.shape[0], im.shape[1]])  # 把一维数组再变回长为shape[0]、宽为shape[1]后更新图像值
im[:, :, 1] = g.reshape([im.shape[0], im.shape[1]])
im[:, :, 2] = b.reshape([im.shape[0], im.shape[1]])

writer.add_image("new", im, 1, dataformats='HWC')
writer.close()
```

输入图像和输入图像分别为：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ffd3487f26fa5643538cd507f72792df.png#pic_center)  
 至此，高斯加噪部分的基础知识基本掌握。上述代码实现起来似乎比较麻烦，总觉得以我们对python的认识来看应该还有更方便、更简单的办法，果然，我无意间就找到了一篇博客。

```
import cv2
import numpy as np

img = cv2.imread("xdl.jpg")  # 用opencv读取到的图像是以ndarray存储的
# img.shape为(402, 285, 3)分别对应以下
img_height = img.shape[0]
img_width = img.shape[1]
img_channels = img.shape[2]

means = 0
sigma = 25

"""
numpy.random.normal(loc, scale, size): 从正态（高斯）分布中抽取随机样本

参数说明：
loc: 分布的均值（中心）,浮点型数据或者浮点型数据组成的数组。
scale: 分布的标准差，浮点型数据或者浮点型数据组成的数组。
size: 输出值的维度（可选），整数或者整数组成的元组，默认为None。如果给定的维度为(m, n, k)，那么就从分布中抽取m * n * k个样本。
      如果size为None（默认值）并且loc和scale均为标量，那么就会返回一个值。
"""
gauss = np.random.normal(means, sigma, (img_height, img_width, img_channels))  # 直接获取大量噪声值（维度对应）

noisy_img = img + gauss  # 整体更新

"""
numpy.clip(a, a_min, a_max, out=None):将数组a中的元素限制在a_min, a_max之间.
                                      大于a_max的就使得它等于 a_max，小于a_min,的就使得它等于a_min。
当out指定为a时，会把np.clip函数的返回值赋给a。
"""
# 设置图片添加高斯噪声之后的像素值的范围
noisy_img = np.clip(noisy_img, a_min=0, a_max=255)

#保存图片
cv2.imwrite("noisy_img.jpg", noisy_img)
```

**椒盐噪声**

> **椒盐噪声也称为脉冲噪声**，是图像中经常见到的一种噪声。所谓椒盐，椒就是黑，盐就是白。它是一种随机出现的白点或者黑点，可能是亮的区域有黑色像素或是在暗的区域有白色像素（或是两者皆有）。

> 可能是影像讯号受到突如其来的强烈干扰而产生、类比数位转换器或位元传输错误等，例如失效的感应器导致像素值为最小值，饱和的感应器导致像素值为最大值。去除脉冲干扰及椒盐噪声最常用的算法是中值滤波。

我的理解就是，在正常图像上的某些像素点出现RGB为`(255, 255, 255)`或`(0, 0, 0)`的情况。至于是哪些位置出现噪声、噪声是黑还是白，需要进一步学习。详见代码：

```
import cv2
import numpy as np

# 读取图片
img = cv2.imread("xdl.jpg")  # 使用cv2读取的图像为ndarray格式

# 设置添加椒盐噪声的数目比例（p = 白/(黑+白））
s_vs_p = 0.5
# 设置添加噪声图像像素的数目比例（p = （黑+白）/总像素）
amount = 0.04

noisy_img = np.copy(img)

'''
numpy.ceil():函数用于对数组中的元素进行向上取整
'''
# 添加salt噪声（白）
num_salt = np.ceil(amount * img.size * s_vs_p)  # 计算得到白噪声的数量

'''
numpy.random.randint(low, high=None, size=None, dtype='l'):函数的作用是，返回一个随机整型数，范围[low, high)。

参数说明：
low(int): 生成的数值最低要大于等于low。
high(int): 可选，如果使用这个值，则生成的数值在[low, high)区间，如果没有写参数high的值，则返回[0,low)的值。
size(int or tuple of ints): 可选，输出随机数的尺寸，若为(m*n*k)则输出规模为m*n*k的随机数组；若为默认None则返回满足要求的单一随机数。
dtype(dtype): 可选，想要输出的格式，如int64、int等。
'''
# 设置添加噪声的坐标位置
coords = [np.random.randint(0, i - 1, int(num_salt)) for i in img.shape]  # 在三个维度分别得到num_salt数量的随机数表示坐标
# coords得到了二维数组[[...], [...], [...]]，第一维长度为3表示高、宽、通道分类，第二维长度为num_salt表示取值
noisy_img[coords[0], coords[1], :] = [255, 255, 255]  # 取noisy_img三维中（RGB三层）第coords[0]行、coords[1]列的所有元素
# 注意：要想把像素值变成白色，必须三个通道的颜色全部改变，所以实际上coords第一维的通道类用不上

# 添加pepper噪声（黑）
num_pepper = np.ceil(amount * img.size * (1. - s_vs_p))
# 设置添加噪声的坐标位置
coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in img.shape]
noisy_img[coords[0], coords[1], :] = [0, 0, 0]

# 保存图片
cv2.imwrite("noisy_img.jpg", noisy_img)
```

添加噪声前后的图片对比如下：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f1b3a2d5fc221879df50ae169804dccc.png#pic_center)  
 为保证总体学习进度，其他噪声暂时不学了，若需补充可参考

1. https://blog.csdn.net/sinat\_29957455/article/details/123977298
2. ……

#### 2.4 3 数据增强

> 数据增强是指从给定数据导出的新数据的添加，这可能被证明对预测有益。例如，如果你使光线变亮，可能更容易在较暗的图像中看到猫，或者例如，数字识别中的9可能会稍微倾斜或旋转。在这种情况下，旋转将解决问题并提高我们的模型的准确性。  
>  ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/76571e259434c3e07c4e1b83ce816990.png)  
>  **通过旋转或增亮，我们正在提高数据的质量。这被称为数据增强。**

##### 几何变换——镜像

总是用某粉色软件P图，对镜像非常了解了。目前没有看到直接对图像进行镜像操作的函数，那就自己写一下吧，逻辑和翻转数组一样，非常简单。

```
import cv2
import numpy as np

img = cv2.imread("xdl.jpg")

iUD = np.copy(img)  # 用来操作上下镜像
iLR = np.copy(img)  # 用来操作左右镜像
iAcross = np.copy(img)  # 用来操作上下左右翻转

h = img.shape[0]-1  # 图像高末端所在序号
w = img.shape[1]-1  # 图像宽末端所在序号

for i in range(h):  # 处理行

    for j in range(w):  # 处理列

        iUD[i][j] = img[h-i][j]  # 上下镜像
        iLR[i][j] = img[i][w-j]  # 左右镜像
        iAcross[i][j] = img[h-i][w-j]  # 上下左右翻转

cv2.imshow("xdl", img)
cv2.imshow("i_UD", iUD)
cv2.imshow("i_LR", iLR)
cv2.imshow("i_Across", iAcross)

cv2.waitKey(0)
```

结果如下：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/22e8aca1586d6f5f16acae6ffb20e816.png#pic_center)  
 整了一堆图片出来我已经完全忘记原图长啥样了。关于cv2.waitKey()的用法详见：

1. [【深度学习】计算机视觉（三）——pytorch（上）](https://blog.csdn.net/RK_Dangerous/article/details/126010312?spm=1001.2014.3001.5501)
2. [cv2.waitKey()](https://blog.csdn.net/weixin_54977011/article/details/120208280)

##### 几何变换——平移

平移的概念非常好理解，将图像中的所有像素点按照给定的平移量进行水平或垂直方向上的移动。出画的部分就不要了，移出来的用黑色填补。我的理解就是遍历改变存储图像的数组的值即可，但是openCV提供了函数。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2b346f1c32c38e7fc43ebf5462306c6c.png#pic_center)

```
import cv2
import numpy as np

# 读取图片
src = cv2.imread("xdl.jpg")

# 设置图像平移矩阵的前两列矩阵M（第三列默认为[0, 0, 1])
M = np.float32([[1, 0, 100], [0, 1, 50]])  # Δx为100，Δy为50

# 获取原始图像列数和行数
rows, cols = src.shape[:2]  # 大括号切片表示2前面所有值，左闭右开，即0、1
print(rows)
print(cols)

"""
cv2.warpAffine(src, M, dsize[, dst[(w, h), flags[, borderMode[, borderValue]]]]): 平移图像
– src表示原始图像
– M表示平移矩阵
– dsize表示变换后的输出图像的尺寸大小
– dst为输出图像，其大小为dsize，类型与src相同
– flag表示插值方法的组合和可选值
– borderValue表示像素外推法，当borderMode = BORDER_TRANSPARENT时，表示目标图像中的像素不会修改源图像中的“异常值”。
– borderValue用于边界不变的情况，默认情况下为0
"""
# 图像平移
result = cv2.warpAffine(src, M, (cols, rows))

#显示图像
cv2.imshow("original", src)
cv2.imshow("result", result)
cv2.waitKey(0)
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ad52b3d83d57bcf33c4f34fbef8d8f46.png)

##### 改变亮度

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a234722bc83150ed4737f532a0d03962.png#pic_center)

> 对于RGB三个通道，改变亮度的方法就是每个通道增加相同的增量。而对于HSL颜色空间，显然只改变亮度对应的数值L即可。

根据之前的学习（[【深度学习】计算机视觉（二）——认识和基础（下）](https://blog.csdn.net/RK_Dangerous/article/details/126264474?spm=1001.2014.3001.5501)），而我的疑惑是，根据公式看，如果三个通道都增加相同的增量后，一定会改变其色相和饱和度，如何在不改变二者的情况下只改变图像的亮度呢？我认为这是个复杂的计算过程，所以上述“每个通道增加相同的增量”其严谨性有待进一步商榷。  
 根据我对公式的分析（初步计算，没有经过多次严谨的验证，不确定推导过程有没有错误），当R=G=B时，只要同增同减相同的数，均能在色相、饱和度不变的情况下，改变亮度。而不同的情况，均能得出一定的关系从而设置新的RGB值，由于h和s表达式的条件不同，细分应该会有`1+9*2*9*2`种情况，太多了，我只试了2种。举个例子，当初始值`b=g＜r 且 l ≤ 1/2`时，若将亮度增加至`l' (l' ≤ 1/2)`，则 `r' = (2 * b * l') / (r + b)`, `b' = g' = (2 * r * l') / (r + b)`，我的计算过程不在身边，这个结论是我凭记忆写的，公式大概就是这样，反正如果输入改变后的亮度， 应该总能输出对应的结果，只不过判断的过程会麻烦一些。  
 为了比较我查阅到的“正经”方法，我自己先实现了对于RGB图像的亮度改变，对于每个像素值、每个通道，增加或减少相同的数值。

```
import cv2
import numpy as np

# 自制一张图片，尺寸为2×2
img = np.array([[[204, 170, 196],
                 [184, 105, 148]],
                [[199, 120, 121],
                 [199, 145, 168]]])  # 注意cv2.imread格式是BGR

# 保存图片
cv2.imwrite("LightnessRGB_Test.png", img)
old = cv2.imread("LightnessRGB_Test.png")
"""
这里有个巨大的注意事项！我刚开始一直设置保存格式为jpg，然后我发现imread读取的和我自己写的数组不一样，除非4个像素值一模一样
经过很艰辛的查阅资料，我才知道png是无损压缩，jpg是有损压缩。果然改成png格式后就不再出现这样的问题了！
"""

add = np.ones(old.shape) * 50  # 因为做实验，逻辑保证设置的数据不超过0——255即可

new_1 = old + add
cv2.imwrite("LightnessRGB_TestAdd.png", new_1)

new_2 = old - add
cv2.imwrite("LightnessRGB_TestSub.png", new_2)
```

结果如下：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ada96a648877143c7136d86cd977ac8a.png#pic_center)  
 以上是我自己的实验，接下来在此基础上学习使用skimage改变图像的亮度。  
 使用`pip install scikit-image`安装。参考：[在pycharm用python画图：matplotlib](https://blog.csdn.net/RK_Dangerous/article/details/125056104?spm=1001.2014.3001.5501)  
 首先，有几个概念需要先了解一下，图片用不同的格式表示是不一样的，常用的是uint8表示图片范围在0到255之间，一般`cv2.imread()`读取到的就是这个格式的图片。对图像的数值进行运算一般都不能用uint8，所以会进行转换。

| Data type | Range |
| --- | --- |
| uint8 | 0 to 255 |
| uint16 | 0 to 65535 |
| uint32 | 0 to 232 |
| float | -1 to 1 or 0 to 1 |
| int8 | -128 to 127 |
| int16 | -32768 to 32767 |
| int32 | -231 to 231 - 1 |

在skimage中提供了多种直接转换图像格式的函数，如：

| Function name | Description |
| --- | --- |
| img\_as\_float | Convert to 64-bit floating point. |
| img\_as\_ubyte | Convert to 8-bit uint. |
| img\_as\_uint | Convert to 16-bit uint. |
| img\_as\_int | Convert to 16-bit int. |

除此之外，skimage还提供了可以直接改变色彩空间的函数，如下，使用这些函数处理后的图片会自动以float的格式存储。

| Function name | Description |
| --- | --- |
| color.rgb2grey(image) | 将RGB空间转换为灰度空间 |
| color.rgb2hsv(image) | 将RGB空间转换为HSV空间 |
| color.rgb2lab(image) | 将RGB空间转换为lab空间 |
| color.gray2rgb(image) | 将灰度空间转换为RGB空间 |
| color.hsv2rgb(image) | 将HSV空间转换为RGB空间 |
| color.lab2rgb(image) | 将lab空间转换为RGB空间 |
| color.convert\_colorspace(arr, fromspace, tospace) | 将arr从fromspace颜色空间转换到tospace颜色空间，例如`color.convert_colorspace(img,'RGB','HSV')` |

利用skimage改变图像亮度，代码如下：

```
import cv2
import numpy as np
from skimage import img_as_float, exposure, img_as_ubyte

# 自制一张图片，尺寸为2×2
img = np.array([[[204, 170, 196],
                 [184, 105, 148]],
                [[199, 120, 121],
                 [199, 145, 168]]])  # 注意cv2.imread格式是BGR

# 保存图片
cv2.imwrite("LightnessHSL_Test.png", img)
old = cv2.imread("LightnessHSL_Test.png")

# 使用skimage.img_as_float更改图片格式
old = img_as_float(old)

# 使用skimage.exposure.adjust_gamma改变图像亮度
"""
skimage.exposure.adjust_gamma(image, gamma=1)：对图像的像素进行幂运算得到新的像素值，新像素 = 原像素 ^ gamma

如果gamma>1，新图像比原图像暗；如果gamma<1，新图像比原图像亮；gamma参数默认为1，原像不发生变化。
"""
img_light = exposure.adjust_gamma(old, 0.7)
img_dark = exposure.adjust_gamma(old, 1.5)
img_light = img_as_ubyte(img_light)  # 为了便于分析实验结果，统一变回为uint8
img_dark = img_as_ubyte(img_dark)

# 保存图片
cv2.imwrite("LightnessHSL_TestLight.png", img_light)
cv2.imwrite("LightnessHSL_TestDark.png", img_dark)
```

结果如下，亮度都有了一定的改变，但不知道是因为uint8和float的转换导致的精度损失还是它本身就无法保证色相与饱和度不变，根据我上面对公式的分析，我猜测skimage这样单纯地把像素进行幂运算，无法输出控制H和S不变的结果。分析结果，利用我自己的方法至少可以保证色相不变，但是饱和度会有较大的变化，而利用skimage得到的变化对色相和饱和度的影响相对较小。可见我们广义上亮度的改变常常伴随着其他值的调整，不过肉眼看上去确实是感受到亮度变化。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7c4cd47dca79715d488e511a159fa607.png)  
 此外，我发现RGB数值与gamma是成反比例的，这很奇怪，我想到用float存储，由于图片都在0-1之间，小数的幂函数图像是单调递减的，这也就说明为什么gamma小的时候RGB数值反而增大。

很不幸，我尝试使用`color.convert_colorspace(img,'RGB','HSL')`，但报错提示skimage里没有HSL空间，看来没有办法直接调整L的值。

### 2.5 特征金字塔（FPN）

#### 2.5.1 基本概念

1. **尺度、尺度空间**  
    图像的尺度并非指图像的大小，而是指**图像的模糊程度（σ）** 。尺度的概念是用来模拟观察者距离物体的远近程度，具体来说，观察者距离物体远，看到物体可能只有大概的轮廓；观察者距离物体近，更可能看到物体的细节，比如纹理，表面的粗糙等等。例如，人近距离看一个物体和远距离看一个物体模糊程度是不一样的，从近距离到远距离图像越来越模糊的过程，也是图像的尺度越来越大的过程。  
    图像的尺度空间是指同一图像不同尺度的集合。在构建图像尺度空间的过程中，唯一使用的核函数是高斯核（因为高斯核是唯一可以产生多尺度空间的核）。即**图像的尺度空间是一幅图像经过几个不同高斯核后形成的模糊图片的集合**，用来模拟人眼看到物体的远近程度以及模糊程度。  
    ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5fe0476a4ad413abc6ab5449fb3a75df.png)
2. **特征**  
    **颜色特征**是最为广泛的视觉特征。颜色特征无需进行大量计算，只需将数字图像中的像素值进行相应转换，表现为数值即可。  
    **形状特征**的表达必须以对图像中物体或区域的分割为基础。 两种经典的算法是SIFT和HOG： SIFT是先找特征点，而HOG是对图片进行分割。  
    **纹理特征**是一种反映图像中同质现象的视觉特征，它体现了物体表面的具有缓慢变化或者周期性变化的表面结构组织排列属性。  
    **边缘特征**是检测一张数字图像中有明显变化的边缘或者不连续的区域。边缘是一幅图像中不同区域之间的边界线，通常一个边缘图像是一个二值图像。边缘检测的目的是捕捉亮度急剧变化的区域，而这些区域通常是我们关注的。
3. **上采样和下采样**  
    **上/下采样可对应为放/缩。** 下图按金字塔的方式特征提取，以黄色特征图为基础，那么橙色就可以理解为是相对于黄色的下采样（缩），灰色就是上采样（放）。一张图片可以解析为n个（上采样特征，基值，下采样特征）向量。以眼睛的特征向量为例可以形象的解释为，上采样特征—猫的眼睛、基值—动物的眼睛、下采样特征—眼睛。  
    ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f2b2ef4a15b69de0b478e2ad86c02cdc.png)  
    缩小图像，我们可以更加清楚地关注到图像的全局信息（比如缩略图）；放大图像，我们可以精细地了解图像的局部信息。一般在目标检测过程中，上采样为了识别较大物体，而下采样为了识别更小物体。  
    特征金字塔能够将图像信息分解为局部、一般、全局信息的特征图，将这3种特征图交由计算机处理便能够进行图像信息的多尺度处理。若更关注局部，则可将局部或一般信息进行下采样，此过程称为resize，重新恢复尺寸。

#### 2.5.2 FPN的网络结构

> **特征金字塔网络FPN（Feature Pyramid Networks）** 是用于检测不同尺度的对象的识别系统中的基本组件。多尺度上识别目标是计算机视觉的一个挑战,通过提取多尺度的特征信息进行融合,进而提高模型精度。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/95dc030761ed52ce4742de6a1d47526d.png)  
 **a. 基础的CNN网络结构：**  
 自底向上卷积，然后使用最后一层特征图进行预测，即仅采用网络最后一层的特征。卷积神经网络不仅可以表达高阶语义特征，在面临物体尺度变化时的表现也更加稳健。  
 应用举例：分类器  
 **b. 图片金字塔：**  
 将图像做成不同的scale（缩放成多个比例），然后不同scale的图像生成对应的不同scale的特征，用每个比例单独提取的特征图进行预测。  
 应用举例：Mtcnn的pent；TTA  
 **c. 多尺度特征融合：**  
 从网络不同层抽取不同尺度的特征做预测。  
 优点：不会增加额外的计算量。  
 应用举例：SSD(Single Shot Detector)目标检测算法  
 **d. FPN：**  
 在多尺度特征融合的基础上还增加了通过高层特征进行上采样和低层特征进行自顶向下的连接（特征融合），然后进行下一步预测。  
 优点：主要解决物体检测中的多尺度问题，在基本不增加原有模型计算量的情况下，大幅度提升了小物体检测的性能。  
 应用举例：Retinanet

举例说明FPN的过程，以32倍下采样和16倍下采样特征图进行FPN操作，图示如下：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/150a050a1e879743533b9b9960b177ea.png)

其中，**“特征融合”常用的两种方法是`concat`和`add`**。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f386c09c0ee0175aa7d6c8fd92a5f9ee.png)

* concat：张量拼接，会扩充两个张量的维度。
* add：张量相加，张量直接相加，不会扩充维度

concat能够完整地保留特征信息，比add的信息保留程度高，但是通道数会增加，卷积核参数变多。add需要保证C、H、W三个参数完全一致才能进行，concat则只需要H和W一致即可。如果采用轻量级的网络一般以add为主，add是FPN官方的特征融合方式。

**FPN的动机包括：**

* 高层特征不断往底层融合，增强低层特征的表达能力，提升性能；
* 不同尺度的目标物可以分配到不同层进行预测，分而治之。

#### 2.5.3 下采样和上采样

> **下采样（subsampled）**，又称为降采样（downsampled）。可以通俗地理解为缩小图像，减少矩阵的采样点数。

我的理解，在卷积的过程中，卷积操作、池化操作都是下采样，因为它们可以缩小图像尺寸。除卷积操作外，另外介绍常用的下采样方法如下：

* 隔位取值：每行每列每隔`k`个点取一个点
* 合并区域：每`(row/k)*(col/k)`窗口内所有像素的均值作为一个像素

> **上采样（upsampling）**，又称为插值（interpolating）。可以通俗地理解为放大图像，增加矩阵的采样点数。

我们说的反卷积就是上采样，在卷积提取特征后需要通过上采样将feature map还原到原图中。反卷积常用的操作是**双线性插值**以及**转置卷积**，具体方法在`【深度学习】计算机视觉（五）——神经网络详解`中已经介绍过，另外介绍常用的上采样方法如下：

* 内插值：每行每列每相邻两点间增加新的k-1个采样点，包括最邻近元法、双线性插值法、三次内插法等
* 频域补0：根据傅里叶变换性质等同于在空域插值

---

参考来源：

🤩[目标检测 YOLOv5 开源代码项目调试与讲解实战【土堆 x 布尔艺数】](https://www.bilibili.com/video/BV1tf4y1t7ru?p=1&vd_source=b9903dbe1b7c91d693351ba0e40e8aaa)  
 [目标检测中One-stage的检测算法](https://blog.csdn.net/shentanyue/article/details/84860600)  
 [RuntimeError: CUDA out of memory.Tried to allocate 20.00 MiB](https://blog.csdn.net/gyl1050097468/article/details/108726882)  
 [[人工智能-深度学习-80]：开发环境 - OSError: [WinError 1455] 页面文件太小，无法完成训练问题的多种解决办法](https://blog.51cto.com/u_11299290/5144768?b=totalstatistic)  
 [杰卡德系数（Jaccard Index）](https://blog.csdn.net/u012948161/article/details/122640601)  
 [锚框和边缘框](https://blog.csdn.net/loki2018/article/details/124347168)  
 [【字幕版】基于锚框的物体算法检测流程（可能是B站最全面清晰的讲述）](https://www.bilibili.com/video/BV1uY4y1b7hF/?spm_id_from=333.788&vd_source=b9903dbe1b7c91d693351ba0e40e8aaa)  
 🤩[42 锚框【动手学深度学习v2】](https://www.bilibili.com/video/BV1aB4y1K7za/?spm_id_from=333.337.search-card.all.click&vd_source=b9903dbe1b7c91d693351ba0e40e8aaa)  
 🤩[13.4. 锚框](https://zh-v2.d2l.ai/chapter_computer-vision/anchor.html#id4)  
 [目标检测 1 ： 目标检测中的Anchor详解](https://www.cnblogs.com/wangguchangqing/p/12012508.html)   
 [什么是feature map（个人理解）](https://www.cnblogs.com/spore/p/13282959.html)  
 [目标检测算法的分类和优缺点](https://blog.csdn.net/dlyyds_/article/details/123207294)  
 [锚框：Anchor box综述](https://zhuanlan.zhihu.com/p/63024247)  
 [动手深度学习13：计算机视觉——目标检测：锚框算法原理与实现、SSD、R-CNN](https://blog.csdn.net/qq_56591814/article/details/124916601)  
 [【深度学习】锚框损失 IoU Loss、GIoU Loss、 DIoU Loss 、CIoU Loss、 CDIoU Loss、 F-EIoU Loss](https://blog.csdn.net/x1131230123/article/details/123751062)  
 [目标检测算法——anchor free](https://blog.csdn.net/u012863603/article/details/118395468)  
 [计算机视觉之正负样本不均衡问题](https://www.pianshen.com/article/90462042266/)  
 [Anchor Free的目标检测](https://blog.csdn.net/juluwangriyue/article/details/118398877)  
 [什么是anchor-based 和anchor free？](https://www.zhihu.com/question/356551927)  
 [标准化与归一化](https://blog.csdn.net/ANobility/article/details/124600804?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2~default~CTRLIST~Rate-1-124600804-blog-125750741.pc_relevant_multi_platform_whitelistv4&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2~default~CTRLIST~Rate-1-124600804-blog-125750741.pc_relevant_multi_platform_whitelistv4&utm_relevant_index=2)  
 [OpenCV–cv2.imshow无法显示图像，闪一下就关闭](https://blog.csdn.net/weixin_52012241/article/details/122288969)  
 [KeyError: ((1, 1, 512), ‘|u1‘) 报错](https://blog.csdn.net/weixin_45660485/article/details/115393729)  
 [OpenCV中的归一化](https://blog.csdn.net/djstavaV/article/details/123013659)  
 [TensorFlow中Session的使用](https://blog.csdn.net/androidchanhao/article/details/79595004)  
 [AttributeError: module ‘tensorflow’ has no attribute 'Session’错误解决](https://blog.csdn.net/sinat_36502563/article/details/102302392)  
 [RuntimeError: The Session graph is empty. Add operations to the graph before calling run().解决办法](https://blog.csdn.net/MclarenSenna/article/details/105323356)  
 [【CV】图像标准化与归一化](https://blog.csdn.net/xylin1012/article/details/81217988?spm=1001.2101.3001.6650.11&utm_medium=distribute.pc_relevant.none-task-blog-2~default~BlogCommendFromBaidu~Rate-11-81217988-blog-125750741.pc_relevant_multi_platform_whitelistv4&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2~default~BlogCommendFromBaidu~Rate-11-81217988-blog-125750741.pc_relevant_multi_platform_whitelistv4&utm_relevant_index=12)  
 [图像的尺度、尺度空间等概念](https://blog.csdn.net/weixin_45560365/article/details/118424177)  
 [图像尺度空间](https://blog.csdn.net/weixin_50281629/article/details/124542695)  
 [常见的图像特征](https://blog.csdn.net/qq_30815237/article/details/94751325)  
 [图像处理基础：特征金字塔](https://blog.csdn.net/qq_37631708/article/details/121600477)  
 [Concat和Add操作](https://www.pudn.com/news/62a44926b21f69194407deb3.html)  
 [理解FPN特征金字塔网络结构](https://www.bilibili.com/video/BV12v411K79Z/?spm_id_from=333.337.search-card.all.click&vd_source=b9903dbe1b7c91d693351ba0e40e8aaa)  
 [上采样、下采样到底是个啥](https://www.jianshu.com/p/fd9e2166cfcc)  
 [下采样与上采样](https://blog.csdn.net/qq_43368044/article/details/118670228)  
 [神经网络中难样本和噪音样本有什么区别？](https://www.zhihu.com/question/405532510)  
 [神经网络的样本为何要增加噪声？](https://www.zhihu.com/question/275255350)  
 [图像噪声种类–高斯噪声 椒盐噪声](https://blog.csdn.net/qq_34244712/article/details/124306145)  
 [高斯噪声\_百度百科](https://baike.baidu.com/item/%E9%AB%98%E6%96%AF%E5%99%AA%E5%A3%B0/8587563?fr=aladdin)  
 [概率密度函数\_百度百科](https://baike.baidu.com/item/%E6%A6%82%E7%8E%87%E5%AF%86%E5%BA%A6%E5%87%BD%E6%95%B0/5021996?fr=aladdin)  
 [图像加噪（高斯噪声和椒盐噪声）](https://blog.csdn.net/JaxonChan/article/details/118908163)  
 [flatten()函数用法](https://blog.csdn.net/youhuakongzhi/article/details/87535868)  
 [高斯噪声](https://blog.csdn.net/sunmc1204953974/article/details/50623071)  
 [numpy.random.normal详解](https://blog.csdn.net/wzy628810/article/details/103807829)  
 [Numpy中clip函数](https://blog.csdn.net/hjxu2016/article/details/110238033)  
 [python中numpy.random.randint用法](https://zhuanlan.zhihu.com/p/111736243)  
 [numpy\_ceil函数](https://blog.csdn.net/fukangwei_lite/article/details/122331559)  
 [python使用opencv对图像添加(高斯/椒盐/泊松/斑点)噪声](https://blog.csdn.net/sinat_29957455/article/details/123977298)  
 [python数组 冒号：与逗号，的使用](https://zhuanlan.zhihu.com/p/567477555)  
 [cv2.waitKey的入门级理解](https://blog.csdn.net/weixin_44049693/article/details/106271643)  
 [cv2.waitKey()](https://blog.csdn.net/weixin_54977011/article/details/120208280)  
 [python图像处理之镜像实现方法](https://www.h5w3.com/z/340505.html)  
 [OPENCV学习之：如何将矩阵转换成图片，如何将图片转换成矩阵](https://www.freesion.com/article/96981242220/#_27)  
 [RGB模式\_百度百科](https://baike.baidu.com/item/RGB%E6%A8%A1%E5%BC%8F/7362104?fr=aladdin)  
 [opencv的cv2.imwrite()函数写图像之后，再次读取，其像素值不相等的bug](https://www.ngui.cc/el/1235077.html?action=onClick)  
 [怎样用 rgb 三元组理解色相、亮度和饱和度？](https://www.zhihu.com/question/265265004)  
 [Python更改图像亮度](https://blog.csdn.net/WYKB_Mr_Q/article/details/124768667)  
 [七、skimage对比度与亮度调整](https://blog.csdn.net/s294878304/article/details/103485342)  
 [python数字图像处理（4）：图像数据类型及颜色空间转换](https://blog.csdn.net/haoji007/article/details/52063149)  
 [python数字图像处理之对比度与亮度调整示例](https://www.jb51.net/article/253352.htm)  
 [RGB、HSL、HSB颜色模式的转化](https://www.bilibili.com/read/cv13338599)  
 [[Python从零到壹] 三十八.图像处理基础篇之图像几何变换（平移缩放旋转）](https://blog.csdn.net/Eastmount/article/details/122723951)  
 [调和平均数到底有什么意义「科普」](https://www.lqgrdj.com/xiaoxue/1189311.html)  
 [准确率、精确率、召回率](https://www.jianshu.com/p/579342e092c2)  
 [调和平均数-MBA智库百科](https://wiki.mbalib.com/wiki/%E8%B0%83%E5%92%8C%E5%B9%B3%E5%9D%87%E6%95%B0)  
 [机器学习F1值的概念](https://blog.csdn.net/jkkbiancheng/article/details/124147230)  
 [调和平均数\_百度百科](https://baike.baidu.com/item/%E8%B0%83%E5%92%8C%E5%B9%B3%E5%9D%87%E6%95%B0/9661021?fr=aladdin)  
 [ROC曲线和PR曲线的区别及相应的应用场景](https://blog.csdn.net/m0_48520385/article/details/118640623)  
 [PR曲线详解](https://blog.csdn.net/guzhao9901/article/details/107961184)  
 [单阶段目标检测模型YOLO-V3](https://www.bookstack.cn/read/paddlepaddle-tutorials/spilt.3.e8213770efa524bc.md)  
 [Lecture4,5,6：Neural Networks](https://www.jianshu.com/p/90ad25fbd84a?utm_campaign=maleskine&utm_content=note&utm_medium=seo_notes&utm_source=recommendation)  
 [数据预处理](https://blog.csdn.net/lanmengyiyu/article/details/78976819)  
 [神经网络图像输入零均值化的作用](https://blog.csdn.net/wtrnash/article/details/87893725)  
 [深度学习图像预处理中为什么使用零均值化(zero-mean)](https://blog.csdn.net/mooneve/article/details/81943904)  
 [【双语字幕】斯坦福CS231n《深度视觉识别》课程(2017)](https://www.bilibili.com/video/BV1Dx411n7UE?p=4&vd_source=b9903dbe1b7c91d693351ba0e40e8aaa)   
 [深度之眼《李飞飞斯坦福CS231n计算机视觉课训练营》第七期】第三周【任务4】学习反向传播](https://zhuanlan.zhihu.com/p/98862433)