# 【深度学习】计算机视觉（14）——Transformer新手入门

由于时间紧张，所以对于不影响我阅读代码的理论我暂时不仔细写了，之后有时间再补充。

1 Transformer基础
---------------

**Transformer最早起源于论文Attention is all your need，用于NLP领域。** 这句话似乎是每篇Transformer的文章都会提到的，看得多了就觉得这是介绍它必不可少的一句话，已经成为transformer学习的常识了，所以这里也提一句吧！

### 1.1 注意力机制

**注意力机制（Attention Mechanism）** 是让你在某一时刻将注意力放到某些事物上，而忽略另外的一些事物。在深度学习领域，模型往往需要接收和处理大量的数据，然而在特定的某个时刻，往往只有少部分的某些数据是重要的。

#### 1.1.1 Self-Attention

> self-Attention是Transformer用来找到并重点关注与当前单词相关的词语的一种方法。

举例：`The animal didn’t cross the street because it was too tired.`  
 这里的it究竟是指animal还是street，对于算法来说是不容易判断的，但是self-attention是能够把it和animal联系起来的，达到消歧的目的。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/8680ff47167c7f2e61c3dfd9cdd89872.png)

*仍以上述例子来说，在这句话的每个词语都是以一个一维向量的形式传入网络的，具体怎么存储先不考虑。*

如上图，自注意力机制中有三个重要的输入矩阵（先忽略它们的形状）：查询矩阵**Q（query）**、键矩阵**K（key）**和值矩阵**V（value）**。这三个矩阵都是由输入序列经过不同的线性变换得到的，
W
Q
W^Q
WQ、
W
V
W^V
WV、
W
K
W^K
WK是三个随机初始化的矩阵。

* 使用查询矩阵Q与键矩阵K的乘积计算Score，表示关注单词的相关程度。  
   *有一个查询矩阵
  Q
  1
  Q\_1
  Q1​存储“it”、键矩阵
  K
  1
  K\_1
  K1​存储“animal”、键矩阵K2存储“street”，
  Q
  1
  ×
  K
  1
  =
  112
  Q\_1×K\_1=112
  Q1​×K1​=112，
  Q
  1
  ×
  K
  2
  =
  96
  Q\_1×K\_2=96
  Q1​×K2​=96，表示it和animal的相关程度比it和street的相关程度高。*
* Score经过一个softmax函数，得到一个与输入序列长度相同的概率分布，该分布表示每个元素对于查询矩阵Q的重要性。  
   ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9d52485b5b0aff9ac563b2fa27becd3c.png)  
   *对于查询矩阵
  Q
  1
  Q\_1
  Q1​，有长度为10的概率序列，分别表示“The”、“animal”、“didn’t”、“cross”、“the”、“street”、“because”、“was”、“too”、“tired”对于“it”的相对重要性。*
* 将上述概率分布乘以值矩阵V得到自注意力向量，表示将每个元素的值加权平均后的结果。即通过Q和K的相关性程度来作为某个词的权重，这种方法称为scaled dot-product attention。  
   \*V可以理解为是输入矩阵经特征提取后的输出矩阵，若
  V
  1
  V\_1
  V1​表示“animal”的特征向量、
  V
  2
  V\_2
  V2​表示“street”的特征向量，我们已经计算得到
  Q
  1
  Q\_1
  Q1​与
  K
  1
  K\_1
  K1​、
  K
  2
  K\_2
  K2​的相关程度分别为
  s
  m
  1
  =
  0.88
  sm\_1=0.88
  sm1​=0.88、
  s
  m
  2
  =
  0.12
  sm\_2=0.12
  sm2​=0.12作为V的权重，则 V=sm×V，这样
  V
  2
  V\_2
  V2​的特征（注意力）会被削弱输入到后面的操作中。

提示：softmax处分母
d
k
\sqrt{d\_k}
dk​


​，
d
k
d\_k
dk​是K的维度。

1. 除以
   d
   k
   \sqrt{d\_k}
   dk​


   ​的操作是为了缩放，原始注意力值均聚集在得分最高的那个值，获得的权重为1，缩放后注意力就会分散一些。
2. 原始表征
   V
   k
   V\_k
   Vk​是符合均值为0方差为1的正态分布的，与权重矩阵相乘后，结果符合的是均值为0方差为
   d
   k
   d\_k
   dk​的正态分布，为了不改变原始表征的分布，需要除以
   d
   k
   d\_k
   dk​。

#### 1.1.2 Multi-Headed Attention

Multi-Headed Attention（多头注意力）机制是指有多组Q,K,V矩阵，一组Q,K,V矩阵代表一次注意力机制的运算。如下图，8组Q,K,V矩阵计算会得出8个矩阵（所有的V打包成Z），最终我们还需将8个矩阵经过计算后输出为1个矩阵，才能作为最终多注意力层的输出。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/87c06c4b5bb43ad7ef818d03e6d2a55d.png#pic_center)  
 可以看到下图，不同的Head在it位置上对于不同词语的关注度是不一样的。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4c461ac4c7a02a4cf7fe3eba62f33b3e.png)

#### 1.1.3 进一步解释

在看代码的过程中，还是不知道
q
、
k
、
v
q、k、v
q、k、v输入的依据，以及他们的实际意义，所以和zrc同学进一步探讨了一下，感觉更清晰了（感谢）。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ca1a0a772b233dd29136a1f56ca5651e.png#pic_center)  
 如上图，输入特征为x，分别经过三个权重
W
K
W^K
WK、
W
Q
W^Q
WQ、
W
V
W^V
WV得到
q
、
k
、
v
q、k、v
q、k、v，权重是需要网络学习和反向传播更新的。
x
、
q
、
k
、
v
x、q、k、v
x、q、k、v的形状对于注意力的理解是很重要的。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/760da66485eb99afa28ec016477321fd.png#pic_center)  
 对于
x
x
x，每一行代表一个单词。有多少行就有多少个单词，有多少列就说明存储这个单词词向量有多长。以上图为例，表示我们这个句子中有4个单词，每个单词需要6个单元存储。
Q
Q
Q、
K
K
K和
V
V
V同理，它们是对原始输入的调整，不再简单代表单词的特征，存储方式还是一样的。*比如我可以理解（假设）为
Q
Q
Q更侧重于单词本身的意义，
K
K
K更侧重与这个单词可以和别的单词有什么联系，
V
V
V更侧重表征，为了从多个角度描述这个词。这是我目前的理解，具体是否正确还有待考究。*  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a0fa36394807702453fc02343ef337da.png#pic_center)  
 用
Q
Q
Q和
K
T
K^T
KT相乘得到的为attention，它的意义就是每两个单词之间的相关联性，一个小单元就表示两个词的关联性，即不再用一个词向量组成一个单词了。比如
Q
K
[
2
,
3
]
T
QK^T\_{[2,3]}
QK[2,3]T​表示对第2个单词来说，第3个单词和它的关联性。  
 我是这样理解的，一个单词并不只是和句子里的某一个单词有关，它可能被很多单词影响，可以解释为它还受上下文影响。回归到自然语言处理任务，我们是要根据前文去“编造”下一个单词，用多个单词组成一个句子，在计算机视觉方面，就体现为一个像素和周围像素是相似的。这也就可以解释经过softmax变换，得到的是attention系数（可以结合softmax去理解），代表周围不同像素对它的影响因子。  
 对于
V
V
V的理解，我把这一系列操作看成一个拼图的过程，一个物体（单词）是由几块最重要的拼图（每个小单元）组成的，物体被抽象成3个拼图，表示该物体三个角度的显著特征。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4911eb71fa141e804add2d73f852ddfc.png#pic_center)  
 attention系数
×
V
×V
×V，得到的输出
Z
Z
Z就是我们根据单词之间互相的影响力设计的计算方法得到的新单词。
Z
Z
Z越接近原始输入
X
X
X，说明我们的计算方式越准确、有代表性。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b08c3492dc53dd02fd8a945c80be8d07.png#pic_center)

### 1.2 注意力机制结构

*（本来这节的标题是“Transformer结构”，学了很久一直在学习encoder和decoder，偶然才发现实际Transformer不止这些，所以与其说是Transformer结构不如说是Self-Attention结构）*

在此之前的模型都是以循环神经网络为基础，从本质上来讲，RNN是以串行的方式来处理数据，对应到NLP任务上，即按照句中词语的先后顺序，每一个时间步处理一个词语。

相较于这种串行模式，Transformer的巨大创新便在于**并行化的语言处理**：文本中的所有词语都可以在同一时间进行分析，而不是按照序列先后顺序。为了支持这种并行化的处理方式，Transformer依赖于**注意力机制**。注意力机制可以让模型考虑任意两个词语之间的相互关系，且不受它们在文本序列中位置的影响。通过分析词语之间的两两相互关系，来决定应该对哪些词或短语赋予更多的注意力。

Transformer采用Encoder-Decoder架构，如下图。其中左半部分是encoder，右半部分是decoder。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/8de0999d287ac356c55b5329e8995079.png)

#### 1.2.1 Input Embedding

Input Embedding的作用是将输入（Input）的语言文字（比如：中文，英语，法语等），输出变成计算机可识别的一组向量。在计算机视觉中，输入定义像素颜色值的图像，输出一个组向量。

由于我们学习的重点不在NLP，所以这里只举一个简单的例子来说明Input Embedding的形状。假设词汇表有“白”、“黑”、“狗”和“猫”，这4个词分别赋予一个唯一的编号1, 2, 3, 4，它们的向量表示分别为：
V
白
=
[
1000
]
T
V\_白=[1000]^T
V白​=[1000]T、
V
黑
=
[
0100
]
T
V\_黑=[0100]^T
V黑​=[0100]T、
V
狗
=
[
0010
]
T
V\_狗=[0010]^T
V狗​=[0010]T、
V
猫
=
[
0001
]
T
V\_猫=[0001]^T
V猫​=[0001]T。我们可以将文本看成是词的集合，不考虑词序信息，比如“白狗”表示为
V
白狗
=
[
1010
]
T
=
V
白
+
V
狗
V\_{白狗}=[1010]^T=V\_{白}+V\_{狗}
V白狗​=[1010]T=V白​+V狗​。即Input Embedding输出一组向量，其中每个向量是一个列向量。

Input Embedding在计算机视觉中体现为Encoder和Decoder层的Patches操作。在将特征输入Transformer主体之前，给定的特征被划分为Patches，每个Patch被视为一个“Word”，展开为一维向量。用p表示patch的大小，patch的数量即patches序列的长度为
N
=
H
W
p
2
N=\frac{HW}{p^2}
N=p2HW​，每个patch的长度为
p
2
×
C
p^2×C
p2×C。Encoder 层作用于 Patches 以生成 Encoded Patches 作为输出，Decoder 层以相同的方式作用于 Encoded Patches 以生成 Decoded Patches。

#### 1.2.2 Positional Encoding

向量positional encoding是**可学习**的位置编码，它是为了解释输入序列中单词顺序而存在的，维度和embedding的维度一致。这个向量决定了当前词的位置，或者说是在一个句子中不同的词之间的距离。

> Transformer模型的位置编码过程包括将词汇转换为向量，然后与位置编码相加，以保持位置信息。  
>  位置编码的具体作用是，对于不同的输入序列成分，赋予其不同的位置标识，确保**即使是相同的文本序列也因位置不同而有不同的含义**。

位置编码的数学公式用于为每一个位置（即序列中的词素）分配一个独特的编码，以使其能够在不同的上下文中区别对待。每个值都在-1到1之间。下图展示了一个长为 100，宽为 512 的位置编码矩阵的热图。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/dfed29c2e4c08ff5c0e6cf9fbefabf46.png)

#### 1.2.3 Encoder

Encoder层中有6个一模一样的层结构，每个层结构包含了两个子层，第一个子层是多头注意力层（Multi-Head Attention,橙色部分），第二个子层是前馈连接层（Feed Forward，浅蓝色部分），除此之外，还有一个残差连接。

##### 1.2.3.1 Multi-Head Attention

Multi-Head Self-Attention 机制将 QKV 矩阵分成多个 Head，使模型能够同时关注输入序列的多个部分。每个 Head 都被训练来关注输入序列不同但有希望是互补的方面。这导致了更加鲁棒和可解释的注意力分布。

##### 1.2.3.2 Layer normalization

Normalize层的目的就是对输入数据进行归一化，将其转化成均值为0方差为1的数据。

##### 1.2.3.3 Feed Forward

全连接层

#### 1.2.4 Decoder

Decoder层中也有6个一模一样的层结构，但是比Encoder层稍微复杂一点，它有三个子层结构，第一个子层结构是遮掩多头注意力层（Masked Multi-Head Attention，橙色部分），第二个子层是多头注意力结构(Multi-Head Attention，橙色部分)，第三个子层是前馈连接层（Feed Forward,浅蓝色部分）。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/46d6878c1d791235d522dbc75f42203e.png)

*（我通俗的理解，不确定对不对）需要注意的是，并不是Encoder层的输出直接作为Decoder层的输入，而是在中间环节用到了Encoder层的输出，Decoder层其实是有自己的输入，作用是把输入的序列转换想要的结果，比如输入一句英文句子，得到中文翻译。拿卷积类比一下，可以理解为Encoder层是为了训练参数，Decoder层是为利用训练的参数生成结果。*

##### 1.2.4.1 Masked Multi-Head Attention

和编码器输入一样，我们嵌入和添加位置编码到这些解码器输入中，以指示每个单词的位置。  
 实际上Decoder是按照时间步来解码的，每次处理一个词向量。比如第一步得到第一个单词的翻译，第二步得到第二个单词的翻译，以此类推。每次翻译都从头到尾走一遍Decoder。如下图，当第三个时间步，已经有"I" 和"am"被翻译出来，正在进行"a"的翻译。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1c4aa18c2370bda840ed8d2db2991785.png)  
 重复上述步骤，当第5个时间步的时候，生成一个特殊的结束符号，表示解码已经全部完成。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ad97eaa4db2f94864dd631fdd3da84fe.png)  
 Masked Multi-Head Attention中的mask，它的作用就是防止在训练的时候使用未来的输出的单词。比如训练时，第一个单词是不能参考第二个单词的生成结果的，此时就会将第二个单词及其之后的单词都mask掉。

##### 1.2.4.2 Multi-Head Attention

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/92b159ebff71a3ef17f1f157f244edf4.png)  
 通过Masked Multi-Head Attention创建查询矩阵后，Encoder-Decoder Attention层从编码器堆栈的输出中获取键
k
k
k和值
v
v
v矩阵，帮助解码器将注意力集中在输入序列中的适当位置。

我的理解：Encoder层关注的重点是上下文的关系，所以得到的输出实际上是与原始的输入相比较，如果输出
z
z
z与输入
x
x
x非常接近，说明我们找到了正确的上下文关系，那么该过程中使用的
k
k
k和
v
v
v就能作为解释词语间关系的
k
k
k和
v
v
v用于解码的过程中。而Decoder层关注的重点是问题的解决，仍以翻译句子为例，我们参考前面得到的
k
k
k和
v
v
v来利用上下文关系，而实际如何翻译是要在Decoder层去训练的。

##### 1.2.4.3 Feed Forward

前馈神经网络

#### 1.2.5 Linear & Softmax

> 在深度学习特别是神经网络模型中，logits是指模型最后一层的输出，通常是未经激活函数的原始预测值或得分。在分类任务中，logits是模型在每个类别上的得分，这些得分未经过Softmax或Sigmoid函数转换为概率。

解码器堆栈输出的向量，通过线性层投影成一个更大的向量，称为logits向量。假设我们的模型知道从训练集数据集中学习到的10000个唯一的英语单词（单词库），logits向量长度即为10000，每个单元格对应一个唯一单词的分数。然后Softmax层将这些分数转换为概率，选择概率最高的单元格，并生成与之关联的单词作为此时间步骤的输出。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/afe7c1fce5d9a673549a7e90b8b83041.png)

补充：  
 由于模型每次产生一个输出，可以假设模型从概率分布中选择了概率最高的单词，并丢弃其余的单词，这是一种greedy decoding（贪婪解码）的方法。另一种方法是beam search（光束搜索），保留模型概率最高的前几个单词，然后在下一步中分情况讨论，对于上一个位置输出的是单词a或者单词b分两种情况，后面的位置重复此操作。

### 1.3 Transformer结构解读

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/826b48ead6321b08885e90efdad557c8.png)  
 光看上面出现了无数次的图，以为这一整个就是Self-Attention，其实只有橙色部分是Attention，将橙色和蓝色部分展开出来可以得到下图：

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ed211b5ffe6706b6a66b34b5d6a6c529.png)  
 Attention块主要是Self Attention，前面已经讲过了，其中的Linear层不改变特征向量的大小。  
 MLP块就是Feed Forward，第一个全连接先将维度扩大了4倍，然后第二个又还原回去了。

> 除了注意力子层外，我们的编码器和解码器中的每一层都包含一个全连接的前馈网络，该网络被单独且相同地应用于每个位置。这包括两个线性变换，它们之间有ReLU激活函数。  
>  ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4b7318e505396ad7f81d5bf587c54339.png)

也就是说上面两个图都是Transformer的总体结构，只不过是从两个不同的角度看的。

2 样例展示
------

### 2.0 VIT（Vision Transformer)介绍

> VIT模型（Vision Transformer)，这是一篇Google于2021年发表在计算机视觉顶级会议ICLR上的一篇文章。它首次将Transformer这种发源于NLP领域的模型引入到了CV领域，并在ImageNet数据集上击败了当时最先进的CNN网络。这是一个标志性的网络，代表transformer击败了CNN和RNN，同时在CV领域和NLP领域达到了统治地位，此后基本在ImageNet排行榜上都是基于transformer架构的模型了。  
>  论文地址：<https://arxiv.org/abs/2010.11929>

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/cdd9e5f3e8ff42d690f78e075c7c24f0.png)  
 上图为ViT模型的整体架构，只用了transformer模型的编码器部分，并未涉及解码器。

### 2.1 流程描述

任务：使用CIFAR-10（PyTorch内置的小型图像数据集，包含10类32×32像素的图像）实现一个简化的Vision Transformer。  
 参考<https://cloud.tencent.com/developer/article/2505042>。

#### 2.1.1 数据准备

CIFAR-10中的每张图片是32x32像素，RGB格式。我们将它切成4x4的小块（为了简化示例），总共有64个块（32 ÷ 4 = 8，8x8 = 64）。每个小块有48个数值（4x4x3，因为RGB有3个通道）。

#### 2.1.2 嵌入过程

1. 把每个小块展平成一个48维向量。
2. 通过一个线性层，把48维映射到一个固定维度（比如32维），得到嵌入向量。
3. 加上位置编码，告诉模型每个块的位置。

现在，这张图片变成了一个64x32的矩阵，就像一个有64个“单词”的序列。

#### 2.1.3 自注意力计算

假设猫咪的耳朵在第10个块，眼睛在第20个块。Transformer会：

1. 为每个块生成查询、键和值向量。
2. 计算第10个块的查询和第20个块的键之间的相似度，发现它们关系密切。
3. 根据相似度加权组合值向量，生成一个新的表示。

经过多层自注意力，模型学会关联猫的特征。

#### 2.1.4 分类输出

在最后一层，ViT取一个特殊的“分类标记”（CLS Token），通过全连接层输出10个类别的概率（CIFAR-10有10类），比如“猫”的概率是0.8，“狗”是0.1。

### 2.2 代码实现

由于我只是为了了解ViT的结构，加上服务器最近坏了，所以整个训练对我来说需要的时间比较长，我修改了一部分代码，只训练了猫和狗两种类别的500张图像，虽然最后输出的仍是10个类别的概率。测试代码也是只使用了一张我指定的图片，不涉及DataLoader等的使用，所以测试部分的代码可能不适用于其他场景。  
 测试图片如下，是一张小狼。由于我的模型只能区分猫和狗，所以希望最终得到的结果是狗。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/51865e71245c495bafbdeddddc972aab.png#pic_center)  
 我提前裁剪为32×32的图像，路径为`./data/test_wolf.jpg`（注意我的实验环境是Windows，所有路径都是Windows的`/`）：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/0e7c8bfe95d34f97abae92fcb0a0c596.png#pic_center)

代码：

```
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import Dataset
from torch.utils.data import DataLoader, Subset
from PIL import Image

# 超参数
patch_size = 4  # 切分图像为4x4的小块
embed_dim = 32  # 每个小块的嵌入维度
num_heads = 4   # 注意力头的数量
num_classes = 10  # CIFAR-10有10个类别
num_patches = (32 // patch_size) ** 2  # 64个小块 (公式中的32因为原图尺寸是32x32)

# 数据加载
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
''' torchvision.transforms.transforms.Compose 
    是 PyTorch 中用于组合多个图像变换操作的类。它允许你将多个图像变换操作（如裁剪、缩放、归一化等）组合成一个单一的变换操作，从而简化代码并提高可读性。
'''
trainset = torchvision.datasets.CIFAR10(root='.\data', train=True, download=True, transform=transform)
''' torchvision.datasets.CIFAR10
    - root='./data'
        指定数据集的存储路径。如果数据集尚未下载，它将被下载到这个路径下。在这个例子中，数据集将被下载到当前目录下的 ./data 文件夹中。
    - train=True
        指定加载的是训练集。如果设置为 False，则加载测试集。
    - download=True
        如果设置为 True，当数据集在指定路径下不存在时，torchvision 将自动下载数据集。如果数据集已经存在，则不会重复下载。
    - transform=transform
        指定对数据集中的每个图像应用的变换操作。transform 是一个 torchvision.transforms 对象，通常是一个 Compose 对象，包含了一系列的图像变换操作。
'''
# 裁剪数据集，只保留猫和狗的前500个样本
classes = trainset.classes  # ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
cat_indices = [i for i, label in enumerate(trainset.targets) if label == 3]
cat_indices = cat_indices[:500]
dog_indices = [i for i, label in enumerate(trainset.targets) if label == 5][:500]
selected_indices = cat_indices + dog_indices  # 合并索引
train_subset = Subset(trainset, selected_indices)
# trainloader = DataLoader(trainset, batch_size=1, shuffle=True)  # 使用全部训练集
trainloader = DataLoader(train_subset, batch_size=1, shuffle=True)  # 使用裁剪后的训练集


# 简化的ViT模型
class SimpleViT(nn.Module):
    def __init__(self):
        super(SimpleViT, self).__init__()
        # 将图像块映射到嵌入空间
        self.patch_to_embedding = nn.Linear(patch_size * patch_size * 3, embed_dim)  # 输入为4*4*3,输出为32
        # 位置编码
        self.pos_embedding = nn.Parameter(torch.randn(1, num_patches + 1, embed_dim))
        ''' torch.randn 
            是 PyTorch 中的一个函数，用于生成一个张量（Tensor），其元素从标准正态分布（均值为 0，标准差为 1）中随机采样。
            这个函数在深度学习中常用于初始化权重和生成随机噪声
        '''
        ''' nn.Parameter 
            是一个特殊的张量（Tensor），用于表示模型的可训练参数。这些参数在模型训练过程中会被自动更新，通常用于定义神经网络的权重和偏置。
        '''
        # CLS Token
        self.cls_token = nn.Parameter(torch.randn(1, 1, embed_dim))
        ''' CLS Token
            在 Vision Transformer（ViT）中，CLS Token 用于提取全局图像的特征表示，替代了 CNN 中常用的全局池化操作。
        '''
        # Transformer编码器
        self.transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=embed_dim, nhead=num_heads),
            num_layers=2)
        ''' nn.TransformerEncoder 
            是 PyTorch 中的一个模块，用于构建 Transformer 编码器。
            encoder_layer：一个 nn.TransformerEncoderLayer 实例，定义了单个编码器层的结构。
            num_layers：指定编码器层的数量。
        '''
        ''' nn.TransformerEncoderLayer 
            是 PyTorch 中的一个模块，用于定义单个 Transformer 编码器层。
            d_model：模型的嵌入维度（embed_dim），即每个输入向量的大小。
            nhead：多头注意力机制中的头数（num_heads），用于将输入向量分割成多个子空间进行并行处理。
            dim_feedforward：前馈神经网络的维度，默认值为 4 * d_model。
            dropout：Dropout 的概率，默认值为 0.1。
        '''
        # 分类头
        self.fc = nn.Linear(embed_dim, num_classes)  # 分为10类

    def forward(self, x):
        b, c, h, w = x.shape  # [batch_size, 3, 32, 32]
        # 切分成小块并展平
        x = x.view(b, c, h // patch_size, patch_size, w // patch_size, patch_size)
        x = x.permute(0, 2, 4, 1, 3, 5).contiguous()  # [b, 8, 8, 3, 4, 4]
        x = x.view(b, num_patches, -1)  # [b, 64, 48]
        # 映射到嵌入空间
        x = self.patch_to_embedding(x)  # [b, 64, 32]
        # 添加CLS Token
        cls_tokens = self.cls_token.expand(b, -1, -1)  # [b, 1, 32]
        ''' expand
        可以扩展张量的形状，不会改变张量的数据，利用 PyTorch 的广播机制，使得张量在某些维度上可以被重复使用。
        '''
        x = torch.cat((cls_tokens, x), dim=1)  # [b, 65, 32]
        ''' torch.cat 
        用于将多个张量沿着指定的维度dim拼接在一起。
        '''
        # 加上位置编码
        x = x + self.pos_embedding
        # 通过Transformer
        x = self.transformer(x)  # [b, 65, 32]
        # 取CLS Token的输出进行分类
        x = self.fc(x[:, 0])  # [b, 10]
        return x

# 训练模型
model = SimpleViT()
criterion = nn.CrossEntropyLoss()  # nn.CrossEntropyLoss()是 PyTorch 中用于计算交叉熵损失的类
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)


# 是否加载检查点
load_option = True
load_epoch = 0
train_option = True
if load_option:
    # 加载参数
    checkpoint = torch.load(f'.\checkpoint\checkpoint_{load_epoch}.pth')
    model.load_state_dict(checkpoint['model_state_dict'])
    if train_option:
        # 如果需要恢复优化器状态
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        epoch = checkpoint['epoch']
        loss = checkpoint['loss']


if train_option:
    for epoch in range(load_epoch, 1000):  # 从load_epoch起训练1000个epoch
        for images, labels in trainloader:
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
        print(f'Epoch {epoch+1}, Loss: {loss.item()}')
        if (epoch % 10 == 0 and epoch != load_epoch) or epoch == 0:
            torch.save({
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'epoch': epoch,  # 当前训练的轮数
                'loss': loss  # 当前的损失值
            }, f'.\checkpoint\checkpoint_{epoch}.pth')


# 是否测试
test_option = True
img_list = [r".\data\test_wolf.jpg"]
label_list = ["dog"]
# 新建一个测试类
class testDataset(Dataset):
    def __init__(self, img_list, label_list):
        self.img_list = img_list
        self.label_list = label_list
    def __getitem__(self, index):
        img_name = self.img_list[index]
        img = Image.open(img_name)
        return torch.unsqueeze(transform(img), 0), self.label_list[index]
    def __len__(self):
        return len(self.img_list)

if test_option:
    test_dataset = testDataset(img_list, label_list)
    img, label = test_dataset[0]
    with torch.no_grad():
        classes = trainset.classes
        outputs = model(img)
        answer = torch.max(outputs[0], dim=0)[1]
        if(answer == 5):
            print(f"The classification result is {classes[answer]}, correct answer!")
        else:
            print(f"The classification result is {classes[answer]}, but the real category is {label}..")
```

数据集下载中：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/39ad7fb0060c4dddbd2cda38624f4d6a.png)  
 训练中：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/3bffed091d21473382b2616adf4de333.png)  
 前10个epoch我使用了全部的训练集，时间特别慢，所以在第11个epoch我更改为只使用猫和狗的前500张（共1000张），设置总epoch数为1000，从第10个开始继续训练。然而发现loss不太收敛，期间调整了学习率，也没有发现明显的收敛，模型一直小幅震荡（loss大概在0.68-0.74之间），到980个epoch我简单测试了一下。由于我的目标不是训练，所以我没有对loss曲线进行分析，也没有具体研究模型是在第几个epoch后趋于稳定。

文件目录结构，包含检查点、数据集、python文件：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/42ca1bd09f3c4a12a1d22fdc764bbc1f.png)

测试结果：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/dceaabd75e8a4174ad6262226d595023.png)

---

参考来源：  
 [Transformer模型（3）- Input Embedding](https://zhuanlan.zhihu.com/p/517799507)  
 [Transformer讲解以及在CV领域的应用](https://blog.csdn.net/qq_40585800/article/details/112427990)  
 [支持多种底层视觉任务的预训练图像处理Transformer](https://zhuanlan.zhihu.com/p/634110816)  
 [Transformer进行底层图像处理任务](https://zhuanlan.zhihu.com/p/381618400)  
 [超分算法IPT：Pre-Trained Image Processing Transformer](https://blog.csdn.net/qq_45122568/article/details/124698618)  
 [Transformer模型详解（图解最完整版）](https://zhuanlan.zhihu.com/p/338817680)  
 [一文详解Softmax函数](https://zhuanlan.zhihu.com/p/105722023?ivk_sa=1024320u)  
 [The Illustrated Transformer](http://jalammar.github.io/illustrated-transformer/)  
 [Transformer中的位置编码详解](https://blog.csdn.net/qq_60245590/article/details/137976500)  
 [【“Transformers快速入门”学习笔记8】学习中遇到的一些方法和关键字](https://blog.csdn.net/Miclear/article/details/140080218)  
 [Transformer详解](https://blog.csdn.net/weixin_40005743/article/details/85460869)  
 [深度学习 Transformer 架构详解：代码 + 图示](https://www.vectorexplore.com/tech/transformer-explain/#%E6%9C%80%E5%90%8E%E7%9A%84%E7%BA%BF%E6%80%A7%E5%B1%82%E5%92%8Csoftmax%E5%B1%82)  
 [详解VIT（Vision Transformer)模型原理, 代码级讲解](https://blog.csdn.net/qq_43449643/article/details/135623953)  
 [《Transformer如何进行图像分类：从新手到入门》](https://cloud.tencent.com/developer/article/2505042)