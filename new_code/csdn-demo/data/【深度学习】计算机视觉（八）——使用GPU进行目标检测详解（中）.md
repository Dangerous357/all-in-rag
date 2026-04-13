# 【深度学习】计算机视觉（八）——使用GPU进行目标检测详解（中）

#### 文章目录

* [3. 目标检测进阶（下）](#3__1)
* + [3.1无锚框的检测算法](#31_2)
  + - [3.1.1 Keypoint-based Detection](#311_Keypointbased_Detection_15)
    - * [\*\*一、Corner pooling\*\*](#Corner_pooling_21)
      * [\*\*二、扩大学习区域\*\*](#_33)
      * [\*\*三、Embeddings——组合corner\*\*](#Embeddingscorner_46)
    - [3.1.2 Center-based Detection](#312_Centerbased_Detection_59)
  + [3.2 关于模型结构方面一些概念的解释](#32__68)
  + - [3.2.1 超参数](#321__69)
    - [3.2.2 训练集、验证集和测试集](#322__76)
  + [3.3 区域建议网络（RPN）](#33_RPN_94)
  + [3.4 损失函数（上）](#34__133)
  + - [3.4.1 MAE（L1损失）和MSE（L2损失）](#341_MAEL1MSEL2_143)
    - [3.4.2 Huber （Smooth L1）](#342_Huber_Smooth_L1_146)
    - [3.4.3 Log-Cosh](#343_LogCosh_154)
    - [3.4.4 分位数损失](#344__159)
  + [3.5 损失函数（下）](#35__165)
  + [3.6 ROI Pooling 和 ROI Align【选看】](#36_ROI_Pooling__ROI_Align_168)
  + [3.7 丢弃](#37__182)
* [4. 算法使用——YOLOv5](#4_YOLOv5_194)

3. 目标检测进阶（下）
------------

### 3.1无锚框的检测算法

看惯了论文中的Anchor-Free，同时找不到合适的中文翻译，暂且叫它无锚框吧，后续就直接用英文术语了。

首先理解一下为什么会使用Anchor-Free，即Anchor-Based有一些弊端：

1. 对于不同数据集需要设计不同的Anchor（长宽比，尺度大小，anchor的数量），会较明显的影响最终预测效果；
2. Anchor的匹配机制使得极端尺度(特别大和特别小的object)被匹配到的频率相对于大小适中的object被匹配到的频率更低，预置的锚点大小、比例在检测差异较大物体时不够灵活；
3. Anchor的数量庞大，耗费巨大的算力，降低了效率；
4. 容易导致训练时negative与positive的比例失衡（因为训练的时候好像不止需要目标物体，背景也需要参与训练，就是我们要让模型知道什么是对的，也要让它知道什么是错的，但是参与训练的正负样本的比例不好控制，负样本太多了模型没有意义）。

**Anchor-Free的技术包括Keypoint-bsaed Detection（基于关键点）与Center-based Detection（基于中心）两类**：  
 ![](https://i-blog.csdnimg.cn/blog_migrate/c88e56275b89ba9ac3de1235aa2cfd67.png)  
 上图分表是两类技术的代表算法。

#### 3.1.1 Keypoint-based Detection

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/085f6ec607e8e6fbcd5a0fa7da6cee5b.png)  
 因为该算法是无锚框的，如何生成最终的检测框？（注意这里检测框即目标检测的结果可视化，可以理解为得到目标后额外的标注，并不是在检测过程中生成的，和锚框的本质并不同），底层的逻辑就是要给点来打标签，然后再通过这些点组合起来形成上层的语意。因此，keypoint-based的主要任务就是检测左上角和右下角的点，然后将他们组合起来。之所以选择角点，是因为角点相比中心点更有利于训练的，比如说左上角的点，只会和两条边相关，而中心点要和四条边相关。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/76774e21a431e08d2f2abcb6df586a44.png#pic_center)  
 上图以及本节的学习都主要以CornerNet为例，体会基于关键点的算法大概步骤，可能某些细节并不适用于别的算法，接下来讲解一些重点部分便于理解。

##### **一、Corner pooling**

下图是完整的结构。Hourglass Network作为特征提取网络的骨干网络，最后一层输出的特征图作为预测模型的输入，预测模型包括Top-left Corners左上角点和Bottom-right Corners右上角点，在上图Heatmaps和Embeddings的基础上还额外添加了Offsets用于优化和调整。后续的分析均以左上角点的预测模型为例。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9e353817a1778912aa24216f9fd19cf5.png)

> corner pooling layer来帮助更好的定位物体bounding box的对角，因为有时物体bounding box的两个对角处会没有信息。这种情况下corner就很难通过局部特征进行定位。为了确定某个像素点是否是一个top-left corner，我们就需要从该点出发向其水平有方向去看看，以及向其垂直向下方向看看。

corner pooling layer输入两个特征层（Hourglass Network输出的特征图），第一个特征层，在每个像素点作该点水平右边所有像素的最大池化得到该点的一个值，第二个特征层则对每个像素点做该点垂直下面所有像素的最大池化，最后将两个池化结果相加。如下图：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b9fbd4571b4d190f90a5bff7a1f5605c.png)

我的理解：特征图的作用是区别正样本和负样本，对于一张图片，我们感兴趣的部分则其值较大，背景赋予较小的值。在对图片进行识别时，权重用于为不同物体设置不同的结构，然后通过对特征图的激活比较最终的得分，来判断结果。所以我们要找的最大值，就是为了给正样本划定范围。

##### **二、扩大学习区域**

heatmap的形状是`(N,C,H,W)`，其中N是批量大小、C是通道数（类别数，不包括背景）、H和W是高与宽，经Cormer pooling输出的特征图，通过与heatmap计算，可以得到对于不同类别的特征图，将图片中包含的多个类别的物体分开考虑。heatmap具体值的设置规则：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ef5c491174e6ec596bdccec175b8fb1f.png#pic_center)  
 在找角点的过程中，每个正样本只会有两个点，即左上角点（用1表示），右下角点（用1表示），其他点的位置都是0，因此mask应该是二值的，但这样的话，所有的负样本的点就都被舍弃掉了，惩罚力度太大不利于训练。为了调整惩罚力度，为这个角点设置一个半径为R的区域（图中两个角点的圆圈部分），虽然区域中只有一个是真实的角点，大部分都是负样本，但上图中 `角点生成的红框`与`(在圆圈中的)负样本生成的绿色虚线的框`具有高度重叠性，**半径R的值设置为能使红框与绿框有足够的IoU**。  
 这个圆圈中的监督信息通过非归一化的二维高斯函数产生，越接近圆心的部分它的目标值越接近1，越接近圆圈边界的位置它的目标值越接近于0，用这种监督信息来替代二值mask。注意：超过半径的部分仍为0  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2b332b2c198ab48915c2e8a16aa09d7a.png#pic_center)

经heatmaps处理的特征图已经只包含角点信息。

注意，在训练时，我们显然已知真实的角点位置，通过设置半径、使用高斯函数，可以得到heatmaps。但是每一张图片的目标位置都不同，在预测时，我们如何设置heatmaps？看下图可知，heatmaps其实并不是人为设置的，而是由Backbone输出的特征图经过多次卷积等操作生成的，这样才能保证适用于不同的图片，因此我们训练模型的参数，使模型可以生成有用的heatmaps。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/82a1193440c6d5371ceab6dfd485d226.png)

##### **三、Embeddings——组合corner**

对于同一类别的目标，其两个角点的相似度较大；对于不同的目标，左上角点和右下角点的相似度应相差较大。这里将两个点的距离作为相似度。

Embeddings将heatmaps的特征图格式从`(N,C,H,W)`降维输出至`(N,1,H,W)`，用以区分合并通道后的每个类别的物体。

由于没找到具体值的设置方法，所以这里说一下我自己的猜测，并不正确，只是为了更好地理解它。通常我们的分类工作都是在得到某一区域的得分之后，比较得分从而得到最终的结果，但是在这里，由于heatmaps是`(N,C,H,W)`的，那么其实已经把每种类别对应物体的两个角点都找到了，也就是说在一定程度上已经完成了分类任务，所以Embeddings这里只需要匹配角点组合即可，而不需要再计算得分，也就是说只要能完成配对，那么特征图的值具体是多少并不重要了（因为除了这几个角点之外值都为零）。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/48835ac962ca94cb218322d29d9254b2.png#pic_center)

> embeddings是根据heatmap上每个点及其周围的特征产生的一个n维向量

实际上， 根据前面的图我们可以知道，embeddings并不是用值简单代表一个类别，它和heatmaps一样，也是特征图根据多次操作生成的，我们要训练这些操作的参数，从而生成表示每个像素点的相似度embeddings，然后再将heatmaps的结果与embeddings的结果相结合。

etk表示第k个目标的左上角角点的embedding vector，ebk表示第k个目标的右下角角点的embedding vector，ek表示etk和ebk的均值。pull loss用来缩小属于同一个目标（第k个目标）的两个角点的embedding vector（etk和ebk）距离。push loss用来扩大不属于同一个目标的两个角点的embedding vector距离，令Δ=1。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f384f32890413472e50d2f06649a7762.png)

#### 3.1.2 Center-based Detection

基于中心点的预测有很多地方都和基于关键点的预测比较像，所以这里不详细学习了。本节内容以CenterNet为例介绍。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/48fc6ff6181ad631d7604ea7ff66c6a1.png)  
 CenterNet将目标当成一个点来检测，即用目标框的中心点来表示这个目标，预测目标的中心点偏移量(offset)，宽高(size)来得到物体实际box，用heatmap表示分类信息。每一个类别都有一张heatmap，每一张heatmap上，若某个坐标处有物体目标的中心点，即在该坐标处产生一个keypoint(用高斯圆表示）。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/490b8314bce0e5abcd236938b829a18b.png)  
 然后根据中心点产生的尺寸的监督信息去预测物体的尺寸（我的理解就是根据特征图和尺寸的映射去生成，具体怎么生成的我还不知道）。

总结（FCOS也是基于中心点的，此处不作详细了解）：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/dadbc2cabe198bb0bda72aea022286a7.png)

### 3.2 关于模型结构方面一些概念的解释

#### 3.2.1 超参数

> 在机器学习的上下文中，超参数是在开始学习过程之前设置值的参数，而不是通过训练得到的参数数据。通常情况下，需要对超参数进行优化，给学习机选择一组最优超参数，以提高学习的性能和效果。
>
> * 定义关于模型的更高层次的概念，如复杂性或学习能力。
> * 不能直接从标准模型培训过程中的数据中学习，需要预先定义。
> * 可以通过设置不同的值，训练不同的模型和选择更好的测试值来决定

#### 3.2.2 训练集、验证集和测试集

* **训练数据集（Training Set）:**  
   用来学习的样本集，用于分类器参数的拟合。  
   是一些我们已经知道输入和输出的数据集训练机器去学习，通过拟合去寻找模型的初始参数。例如在神经网络（Neural Networks)中， 我们用训练数据集和反向传播算法（Backpropagation）去每个神经元找到最优的比重（Weights)。
* **验证数据集（Validation Set）：**  
   用来调整分类器超参数的样本集，如在神经网络中选择隐藏层神经元的数量。  
   也是一些我们已经知道输入和输出的数据集，通过让机器学习去优化调整模型的参数，在神经网络中， 我们用验证数据集去寻找最优的网络深度（number of hidden layers)，或者决定反向传播算法的停止点；在普通的机器学习中常用的交叉验证（Cross Validation) 就是把训练数据集本身再细分成不同的验证数据集去训练模型。
* **测试数据集（Test Set）：**  
   仅用于对已经训练好的分类器进行性能评估的样本集。  
   用户测试模型表现的数据集，根据误差（一般为预测输出与实际输出的不同）来判断一个模型的好坏。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/bf522a248332a7d738a8c2614680395a.png)

感觉训练集和验证集没什么区别，都是为了调整模型的参数，只不过训练集是机器用来学习的，而验证集是学习完之后，在完全投入使用之前，用非训练集去看看模型的效果，再做进一步优化、为了发现模型的本质缺陷。最后通过验证集的结果去评价模型的结构设计的是否合理，如果没什么问题就能使用测试集进行测试了（测试集不能用作训练集和验证集，因为拿测试集训练相当于作弊）。

### 3.3 区域建议网络（RPN）

我最近在脑子里整理，我们在训练模型的时候，用损失函数来训练参数，使模型检测到的目标和真实目标的“差异”越来越小，但这是不是也不能保证背景的真的被明显区分了？就拿anchor-based举例，因为训练的时候总是关联先验框和边缘框，有没有可能背景的特征只是被弱化了，并不处于最像物体的前几名，但如果检测的时候把阈值稍微设置地低一点，就极大可能把背景也选进去？因为我没有严谨地用数学方式去整理逻辑，所以这个推论只是我自己的一个疑问。  
 在复习one-stage和two-stage时，我看了前面的笔记，发现RPN可以先生成可能存在目标物体的候选区域，我还不知道它的原理，但我推测用RPN去区分前景和背景应该可以解决我前面所说的损失函数考虑不到的问题。

**Region Proposal Network：区域建议网络**

以特征图的每个像素为中心生成了多个锚框（如下图，特征图的每个像素点分别对应下采样前输入的原始图像的像素），锚框传给 RPN, 让 RPN 判断其中哪些 anchor boxes 可能存在目标，并进一步回归坐标，得到 proposals 输给后面的网络。模型回归的目标是真实 boxes 与 anchor boxes 之间坐标的偏置，将偏置和 anchor boxes 的坐标带入预先设定的公式中，就得到了最终预测的boxes坐标。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/389673ac40348980a44a0003cc040f73.png)  
 以Faster-RCNN为例，RPN 的结构如下图，backbone输出的特征图经过一次（512个 `3 ∗ 3 ∗ 512` 的卷积核）卷积之后分别再进入不同的分支进行 1 ∗ 1 卷积（36个 `1 ∗ 1 ∗ 512` 的卷积核、18个`1 ∗ 1 ∗ 512`的卷积核）。第一个卷积为定位层，输出 anchor 的4个坐标偏移（中心点坐标x和y、w、h）。第二个卷积为分类层，输出anchor的前后景概率。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b43da88d41a148fa114c07834ec05dfa.png)  
 如上图，每个位置会生成 2×9 个目标分数和 4×9 个坐标分数。训练时，首先将定位层输出的坐标偏移应用到所有生成的 anchor，然后将所有 anchor 按照前景的概率（得分）从高到低进行排序，提取前N1个修正位置后的anchors，另外要剔除严重超出边界的和非常小的anchors，最后按照 nms 后的 softmax scores 由大到小排序提取前N2个结果作为 proposal 输出，称为**RoI(感兴趣区域)** 。

> 根据 Anchor 对应的 refrence box 与 ground truth 的 IoU 值标记正样本，如果 Anchor 对应的 reference box 与 ground truth 的 IoU<0.3，标记为负样本。剩下的既不是正样本也不是负样本，不用于最终训练。

*注意，按照上面的说法，我开头的猜测是有些偏差的，因为模型训练的过程中是有负样本参与的。*

训练 RPN 的Loss是由 classification loss(即softmax loss）和 regression loss（即**L1 loss**）按一定比重组成的。由于softmax之前已经有比较详细的学习，而前面说锚框的时候对坐标的参数调整不是很清楚，所以这里再说一下如何修正位置。

如下图所示，绿色框为飞机的真实框Ground Truth(GT)，红色为提取的positive anchors，即便红色的框被分类器识别为飞机，但是由于红色的框定位不准，这张图相当于没有正确的检测出飞机，所以我们希望采用一种方法对红色的框进行微调，使得positive anchors和GT更加接近。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/48b26276242732e9d6bfbed35d169f98.png#pic_center)  
 我们的目标是寻找一种关系，使得输入原始的anchor A经过映射得到一个跟真实窗口G更接近的回归窗口G’。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d775b7c6063008891f326046af872ca6.png#pic_center)  
 上图是Faster RCNN的结构图，输入的图像经过卷积层输出Feature Map，此时我们以每个像素为中心生成锚框（原图尺寸是Feature Map的16倍，注意生成锚框的时候是在原图上），此处笔记省略训练模型时锚框与真实框的关联以及取舍的过程，将每个锚框记为`A`，而特征图再经过卷积生成A的特征向量`ΦA`。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3de55a23fbeb1999c00171b7cf799620.png)  
 我们目前只考虑简单的情况。当输入的anchor A与GT相差较小时，可以认为这种变换是一种线性变换， 那么就可以用线性回归来对窗口进行微调（注意，只有当anchors A和GT比较接近时，才能使用线性回归模型，否则就是复杂的非线性问题了）。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7b13e0bd4d0c3eff74bf8d6e3f8b002f.png)  
 Anchor与GT的差距`t`为训练的监督信号。

综上，Faster RCNN的损失函数解释为：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3f48e99721feec08607a95029ef87517.png)

---

 RPN网络的最后，由Proposal Layer负责综合所有变换量`d`和positive anchors，计算出精准的proposal，送入后续RoI Pooling Layer。

由网络结构图可知除了上一步两个分支的输出，RoI需要输入的参数还有im\_info，该参数用来存放图片在输入卷积网络之前进行的一次尺寸变换的相关信息（还需要知道采样比例用于设置每个锚框中心点的步长`feat_stride=16`），步骤如下：

1. 生成锚框并根据d对所有的anchors做bbox regression回归；
2. 按照positive的scores由大到小排序anchors，提取前pre\_nms\_topN(e.g. 6000)个anchors，即提取修正位置后的positive anchors（其他舍去）；
3. 由M/16×N/16先映射回M×N限定超出图像边界的positive anchors为图像边界（所以最后输出的proposal是对应MxN输入图像尺度的），剔除尺寸非常小的positive anchors；
4. 对剩余的positive anchors进行NMS（nonmaximum suppression），输出前proposal(e.g. 300)个结果作为输出。（这里的全部输出已经和特征图无关了，全部是锚框的相关参数，所以后续RoI层除了接收Proposal的输出作为输入，还要再输入之前提取的Feature Map）

### 3.4 损失函数（上）

前面已经讲过一些关于损失函数的知识，也穿插地提到了它的概念被、作用，这里从目标检测的角度对损失函数进行更系统地、进一步学习。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/395763039cf4280ededd73f0edfc7b7c.png#pic_center)  
 如上图，根据问题的不同，可以分为适用于**分类**问题和**回归**问题两类的损失函数。

*翻了之前的笔记，竟然没有找到关于分类和回归的，我自认为分类和回归是初学时会比较困扰我的两个概念，也是比较基础的概念，所以这里再复习一下。*

> **分类（Classification）**：分类是指将数据映射到预先定义好的群组或类，构造一个分类函数(分类模型)，把具有某些特征的数据项映射到某个给定的类别上。 因为在分析测试数据之前，类别就已经确定了，所以分类通常被称为有监督的学习。分类算法要求基于数据属性值来定义类别，通常通过已知所属类别的数据的特征来描述类别。  
>  **回归（Regression）**：用属性的历史数据预测未来趋势。回归首先假设一些已知类型的函数（例如线性函数、Logistic 函数等）可以拟合目标数据，然后利用某种误差分析确定一个与目标数据拟合程度最好的函数。回归模式采用连续的预测值。许多问题可以用线性回归解决，对于许多非线性问题可以通过对变量进行变化，从而转换为线性问题来解决。

#### 3.4.1 MAE（L1损失）和MSE（L2损失）

全称Mean Square Error(MSE)与Mean Absolute Error(MAE)，话不多说，我直接总结成了表格的形式，如图。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f01a066066898e08c1b588ca79d386ee.png#pic_center)

#### 3.4.2 Huber （Smooth L1）

MAE与MSE二者兼有的问题是：在某些情况下，上述两种损失函数都不能满足需求。例如，若数据中存在少数异常点，使用MSE的模型会向异常点偏移，而MAE则可能会忽视这些异常点。  
 **Huber损失：平滑的平均绝对误差。**  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4bc904b737f98de0b4f34ba6e8e6847a.png)  
 Huber损失对数据中的异常点没有平方误差损失那么敏感。它在0也可微分。本质上，Huber损失是绝对误差，只是在误差很小时，就变为平方误差。误差降到多小时变为二次误差由超参数δ（delta）来控制。当Huber损失在[0-δ,0+δ]之间时，等价为MSE，而在[-∞,δ]和[δ,+∞]时为MAE。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1b42f525471014231d5dffa0605985f2.png#pic_center)  
 由此可知，Huber损失结合了MSE和MAE的优点，但是**超参数delta的选择非常重要**，我们需要不断地调整。

#### 3.4.3 Log-Cosh

Log-cosh是另一种应用于回归问题中的，且比L2更平滑的的损失函数。它的计算方式是预测误差的双曲余弦的对数。它具有Huber损失所有的优点，但不同于Huber损失的是，Log-cosh二阶处处可微。（许多机器学习模型如XGBoost，采用牛顿法来寻找最优点需要求解二阶导数Hessian，因此对于诸如此类机器学习框架损失函数的二阶可微是很有必要的。）  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6ac48f53e808d9ea6586b26ef5bbfae7.png#pic_center)  
 但Log-cosh损失也并非完美，其仍存在某些问题。比如误差很大的话，一阶梯度和Hessian会变成定值，这就导致XGBoost出现缺少分裂点的情况。

#### 3.4.4 分位数损失

> 当我们更关注区间预测而不仅是点预测时，分位数损失函数就很有用。使用最小二乘回归进行区间预测，基于的假设是残差（y-y\_hat）是独立变量，且方差保持不变。

由于教程并不是特别清楚，学到这里我还有些困了，而且我目前的学习重点似乎不在区间预测上面，所以这里决定暂时不进行学习了。

### 3.5 损失函数（下）

3.4主要讲了用于回归的损失函数。还需要了解用于分类的损失函数。后续补充在这里。

### 3.6 ROI Pooling 和 ROI Align【选看】

（其实纠结了很久，不知道应该把这节放在哪里，好了不跑题了……）根据前面的学习，以Faster RCNN为例，当RPN网络输出为每一张图片生成的每个提议框之后，我们希望统一这些提议框的尺寸，便于后面的批量操作。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b179ad5a042792b977ca473bb98f9357.png)  
 如图，原图为800×800，其中提议框为650×650，当经过骨干卷积网络后，图片尺寸缩放到原来的1/32，原图尺寸变为25×25，提议框其宽高经缩放实际上应该为20.78，但由于需要取整变为20，而这0.78反馈到原图上就是25个像素的差距，对于小目标而言这个误差可能会有较大的影响。

我们换一个图片继续看，如果经骨干网络得到了8×8的的特征图，有一个bbox坐标为[0,3,7,8]，如下图。我们希望将所有提议框的尺寸统一为2×2，若使用最大池化，由于宽和高分别为7和5，无法均等分为两份，所以h被分割为(2, 3)，w被分割成(3, 4)，在每一小块中做max pooling得到结果。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d625e7b8902a460a88d9e0cbc5121138.png#pic_center)  
 这样由于max pooling的划分也会对最终结果有一定影响。由此提出ROI Align用于提高精度。

在经缩放后特征图的提议框不再进行取整，如下图所示：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a9e9f875f8d3f6d053b309b4d43d3d4f.png)  
 我们先将提议框区域根据所指定的统一的bbox尺寸划分，仍以2×2为例，则提议框被划分为四个小区域。每个小区域中取均匀的4个点（见下图蓝点标示），对这四个点取max作为这个区域的最终输出。由于这四个点可能无法对应到真实的像素上面，所以知道点的坐标但是无法得到其对应的特征值，对于每一个蓝点，我们找到距离它最近的4个真实像素点的值加权(双线性插值)，求得这个蓝点的值作为该点的“特征值”参与后面的max计算。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/603ff7550a8e3d74b40dd68ffeaa009f.png)

### 3.7 丢弃

简单推测一下，丢弃也是预防过拟合的一种手段。

> Dropout是对具有深度结构的人工神经网络进行优化的方法，在学习过程中通过将隐含层的部分权重或输出随机归零，降低节点间的相互依赖性从而实现神经网络的正则化，降低其结构风险。

具体来说：在前向传播的时候，当经过某一层神经元的时候，以一定的概率p丢弃这一层的部分神经元，只允许另一部分神经元进行计算，这时网络的输出值便不会依赖丢弃的神经元，在反向传播时，与丢弃神经元相关的权重梯度均为0。**由于在训练过程中神经元的丢弃时随机的，这样可以使模型不会太依赖某些局部特征，从而在训练模型时起到正则化的作用，并可用来应对过拟合的问题。**  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c3d51c038deaa2c73414106cc454a9e0.png#pic_center)  
 如图，x是原始输入，h表示其中一个隐藏层经激活函数的输出，o是全连接神经网络，最后y进行softmax分类。注意：

1. 丢弃不仅将原来的输入置为0，还将参数放缩为原来的`1/(1-p)`倍。
2. 在测试和训练时dropout的表现不同，在测试时所有神经元都不会被丢弃。

4. 算法使用——YOLOv5
---------------

学了这么多理论知识，总该实践了吧！虽然前面学的概念都是非常基础的，但是以我目前学习情况来看，似乎没有人真的从头到尾自己写网络（可能也有但是我没见过），都是使用已有的网络模型（不考虑创新点）。因为初学的时候老师提供了几个算法供我们选择，我当时选择了YOLOv5，所以这里先拿YOLOv5举例。这里只是简单描述了下载和使用，关于训练自己的数据集等内容，不作过多讲解，参考教程：  
 [目标检测 YOLOv5 开源代码项目调试与讲解实战【土堆 x 布尔艺数】](https://www.bilibili.com/video/BV1tf4y1t7ru/?p=1&vd_source=b9903dbe1b7c91d693351ba0e40e8aaa)

**step1 下载**  
 通俗一点讲YOLOv5意思是YOLO的版本5。  
 在：<https://github.com/ultralytics/yolov5> 下载YOLOv5。下载好之后在pycharm里打开文件夹，并设置好编译环境（和往常一样写python项目差不多，没什么特别要说的）。

**step2 环境配置**  
 打开项目之后，可能会跳出提示有些Packages不太满足要求，可以直接按照它的提示安装，如下：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6ba24b76baa740e1f8080061c1c6b086.png)  
 也可以找到文件`requirements.txt`，可以看到里面的内容，有详细写明哪些包是我们需要的，并且我们可以打开pycharm的终端，输入命令`pip install -r requirements.txt`直接安装：

```
# YOLOv5 requirements
# Usage: pip install -r requirements.txt

# Base ----------------------------------------
matplotlib>=3.2.2
numpy>=1.18.5
opencv-python>=4.1.1
Pillow>=7.1.2
PyYAML>=5.3.1
requests>=2.23.0
scipy>=1.4.1
torch>=1.7.0
torchvision>=0.8.1
tqdm>=4.64.0
protobuf<4.21.3  # https://github.com/ultralytics/yolov5/issues/8012

# Logging -------------------------------------
tensorboard>=2.4.1
# wandb

# Plotting ------------------------------------
pandas>=1.1.4
seaborn>=0.11.0

# Export --------------------------------------
# coremltools>=4.1  # CoreML export
# onnx>=1.9.0  # ONNX export
# onnx-simplifier>=0.4.1  # ONNX simplifier
# nvidia-pyindex  # TensorRT export
# nvidia-tensorrt  # TensorRT export
# scikit-learn==0.19.2  # CoreML quantization
# tensorflow>=2.4.1  # TFLite export
# tensorflowjs>=3.9.0  # TF.js export
# openvino-dev  # OpenVINO export

# Extras --------------------------------------
ipython  # interactive notebook
psutil  # system utilization
thop>=0.1.1  # FLOPs computation
# albumentations>=1.0.3
# pycocotools>=2.0  # COCO mAP
# roboflow
```

**step3 模型**  
 默认yolov5s.pt，如果没有下载的话运行的时候会自动下载。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/bb2c897b25666d374edb7ce01968f7e7.png)  
 它说检测结果（两张图片）保存在了`runs\detect\exp`路径中，打开其中的一张。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/81810e6ddcf299241411b5b4dad95033.png)

---

 参考来源：

[损失函数｜交叉熵损失函数](https://zhuanlan.zhihu.com/p/35709485)  
 [论文阅读笔记 | 目标检测算法——CornerNet算法](https://blog.csdn.net/weixin_44751294/article/details/119351915)  
 [AnchorFree系列算法详解](https://blog.csdn.net/SMF0504/article/details/109214527)  
 [深度学习中Embedding的解释](https://blog.csdn.net/yuanmiyu6522/article/details/120930840)  
 [【论文笔记】CornerNet：预测左上角和右下角来实现目标检测](https://www.cnblogs.com/SpicyWonton/p/15259528.html)  
 [CornerNet详解](https://wenku.baidu.com/view/923d7e2b874769eae009581b6bd97f192379bf47.html?_wkts_=1678288724636&bdQuery=cornernet%E8%A6%81%E8%AE%AD%E7%BB%83%E7%9A%84%E5%8F%82%E6%95%B0)  
 [CornerNet: 成对关键点物体检测 | CSDN博文精选](http://www.senlt.cn/article/277355472.html)  
 [【目标检测论文3】——CornerNet](https://blog.csdn.net/qq_29750461/article/details/90451307)  
 [CenterNet原理详解](https://blog.csdn.net/weixin_42398658/article/details/117514336)  
 [Centernet论文详解](https://zhuanlan.zhihu.com/p/363999119)  
 [超参数\_百度百科](https://baike.baidu.com/item/%E8%B6%85%E5%8F%82%E6%95%B0/3101858)  
 [【机器学习】验证集和测试集有什么区别](https://blog.csdn.net/weixin_44211968/article/details/120814758)  
 [深度学习之 RPN（RegionProposal Network）- 区域候选网络](https://blog.csdn.net/fenglepeng/article/details/117898968)  
 [机器学习之分类和回归区别阐述](https://www.ngui.cc/el/1353249.html?action=onClick)  
 [收藏 | 机器学习中常用的5种回归损失函数](https://mp.weixin.qq.com/s?__biz=MzU0NjgzMDIxMQ==&mid=2247597295&idx=3&sn=7d81b2abfa21ce7e304cae46d0731dac&chksm=fb549e03cc23171598688c42ca9011ce356df1e5e53bfa53da62782aad1631333267b9208ec0&scene=27)  
 [一文读懂Faster RCNN](https://zhuanlan.zhihu.com/p/31426458)  
 【系列】[目标检测 YOLOv5 开源代码项目调试与讲解实战【土堆 x 布尔艺数】](https://www.bilibili.com/video/BV1tf4y1t7ru/?p=1&vd_source=b9903dbe1b7c91d693351ba0e40e8aaa)  
 [机器学习笔记：训练集、验证集与测试集](https://blog.csdn.net/mooyuan/article/details/123544318)  
 [RoI Pooling 和 RoI Align](https://blog.csdn.net/Tian__Gao/article/details/124474448)  
 [ROI Pooling和ROI Align](https://zhuanlan.zhihu.com/p/73138740)  
 [nn.Dropout](https://blog.csdn.net/weixin_41978699/article/details/121189603)  
 [深度学习基础算法系列（4）-正则化之Dropout](https://zhuanlan.zhihu.com/p%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0%E5%9F%BA%E7%A1%80%E7%AE%97%E6%B3%95%E7%B3%BB%E5%88%97%EF%BC%884%EF%BC%89-%E6%AD%A3%E5%88%99%E5%8C%96%E4%B9%8BDropout11541)