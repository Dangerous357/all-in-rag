# 【深度学习】计算机视觉（九）——Faster RCNN（基础篇）

#### 文章目录

* [理论知识](#_4)
* [代码精读](#_11)
* + [前言一：代码介绍](#_12)
  + [前言二：本节内容概述](#_21)
  + [1：imdb.roidb.gt\_overlaps](#1imdbroidbgt_overlaps_26)
  + [2：imdb类和imdb.roidb](#2imdbimdbroidb_36)
  + [3：voc.eval()](#3voceval_55)
  + [4：batch和ims\_per\_batch](#4batchims_per_batch_291)
  + [5：im\_info](#5im_info_311)
  + [6：anchor的生成机制](#6anchor_314)
  + [7：blobs](#7blobs_321)
* [README【选看】](#README_331)
* + [前言](#_332)
  + [1. Install tensorflow, preferably GPU version.](#1_Install_tensorflow_preferably_GPU_version_337)
  + [2. Checkout this branch](#2_Checkout_this_branch_344)
  + [3. Install python packages](#3_Install_python_packages_346)
  + [4. Run python setup.py build\_ext](#4_Run_python_setuppy_build_ext_359)
  + - [解决报错：Unable to find vcvarsall.bat](#Unable_to_find_vcvarsallbat_371)
    - [解决完毕](#_395)
  + [5. Download PyCoco database.](#5_Download_PyCoco_database_410)
  + [6. Download pre-trained VGG16](#6_Download_pretrained_VGG16_421)
  + [7. Run `train.py`](#7_Run_trainpy_434)
  + [附1：修改参数](#1_456)
  + [附2：使用gpu进行num的计算](#2gpunum_471)

关于为什么要学习Faster RCNN，主要就是该算法的精度比较高、理论比较成熟，看过一些文章说比较适用于我目前的方向，再加上时间原因没有办法把所有的基础都打好，只能直接开始算法的学习了。

理论知识
----

*本来看到一个博主说，要想了解Faster RCNN，就要先学习RCNN和Fast RCNN，不过我发现它们之间的差别还是有些大的，而且似乎目前也没什么必要去了解，我比较认同另一个博主说“只关注最新的”即可，所以既然我目前学习的重点是Faster RCNN，那么就暂时不去学习其他的RCNN了。*

学习完前面基于锚框的算法和RPN之后，基本对于学习Faster RCNN的全部内容都没有问题了，关于Faster RCNN的理论知识介绍有很多，由于时间问题不作过多赘述，将网络结构的笔记总结附上：

![请添加图片描述](https://i-blog.csdnimg.cn/blog_migrate/19a5bca89509d389cb10f829b087699c.jpeg)  
 主要参考：[一文读懂Faster RCNN](https://zhuanlan.zhihu.com/p/31426458)

代码精读
----

### 前言一：代码介绍

源码链接：<https://gitcode.net/mirrors/dbeker/faster-rcnn-tensorflow-python3?utm_source=csdn_github_accelerator>

本节笔记全部基于上述代码，不同版本某些变量的存储、使用方式可能会有不同。

ps：***注意这篇文章和下一篇的源码不一样。** 因为这个源码我最后用的有点问题，所以实际训练的时候换了。但是这个代码我从头到尾看下来，觉得它的文件结构非常合理，对我理解很有帮助，所以代码部分还是按照它来写。*

提醒一下，选择源码一定要慎重！一定要做好功课，提前检查代码的运行环境是否符合自己的要求，否则后面会有很大的问题。

### 前言二：本节内容概述

由于我认为对代码不够熟练无法很好地掌握，所以决定仔细看一下代码以及体会每一个函数、变量等的作用，以及Faster RCNN是如何实现的。

关于源代码的详细笔记我用的是另一个软件所以没有放在这里。由于一些细节总是容易弄混，所以这里写一下注意事项，另外还涉及到一些代码是参考了网上的教程，因为时间问题暂时未写在笔记里，所以放在这里。

### 1：imdb.roidb.gt\_overlaps

解释一下标题，因为实在不知道怎么描述，指imdb类中的roidb这个变量中的gt\_overlaps。对它的结构解释如下（不看代码可能看不懂）：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2d8661baa3f6a18a183472ef0353134f.png)

在训练阶段，gt\_overlaps的生成方法如下：

* 如果`roidb`是真实框，那么`gt_overlaps`的结构就直接是这样，每个数据的值非0即1，若为1表示该真实框的类别，为0则表示该框不属于这类。
* 如果`roidb`是锚框，仍以图片i为例，首先要得到所有锚框的坐标`bbox`和原图所有真实框的坐标`gt_bbox`，计算出每个`bbox`与每个`gt_bbox`的重叠度`overlaps`（二维数组，第一维表示锚框，第二维表示真实框），然后找到每行的最大值`max`，和索引`argmax`（每个锚框重叠度最高的真实框）。根据`argmax`在真实框`gt_roidb`中找到真实框`gt_roidb[argmax]`，再找到该真实框r的类`class`，此时关联真实框成功。此时真实框的坐标和索引已经不重要了，因为得到了锚框的类信息，只要给第i个roidb赋值`gt_overlaps[j][k]=max`即可。

**另外注意，当roidb是锚框的时候，代码将`gt_classes`参数赋值为0，说明锚框不使用`gt_classes`参数体现类别，说明`gt_classes`应该只是`gt_roidb`独有的，用以标明真实框的类别。**

### 2：imdb类和imdb.roidb

以下是学至目前的感想，因为还没看完所有代码，对某些地方可能理解有误或只是“某个阶段”的解读。

imdb是对数据集操作的类，比如我们的操作对象是`trainval.txt`文件时，我们特意为trainval类型的数据集新建一个imdb，对trainal.txt中包含的图像进行一系列的处理。因此可以说imdb是以数据集为单位的。

其中，imdb.roidb是一个成员变量，roidb可以理解为一个“结构体”，每个`roidb[i]`是以图片为单位的，每张图片对应的roidb[i]构成了一个列表——imdb.roidb。再分析每个roidb[i]，虽然roidb[i]是以图片为单位，但是有些数据又体现了框的数量，其中包含：

* **boxes**：存储图片中每个框的坐标信息，shape为`boxes[框数量][4]`。
* **gt\_classes**：存储图片中每个框的类别信息，用类标号表示。
* **gt\_overlaps**：存储图片中每个框对应每个真实框的重叠度，shape为`gt_overlaps[框数量][真实框数量]`。
* **flipped**：指明该图片是否是翻转后的，shape为1。
* **seg\_areas**：存储图片中每个框的面积，shape为`seg_areas[框数量]`。

除此之外，还有一些额外信息在roidb中，使用roidb.py文件生成，其中包含：

* **image**：图片名称，长度为1。
* **width**：图片宽，长度为1。
* **height**：图片高，长度为1。
* **max\_classes**：取每个锚框的最大gt\_overlaps对应的class，长度为锚框数量。
* **max\_overlaps**：取每个锚框的最大gt\_overlaps，长度为锚框数量。

### 3：voc.eval()

这里主要参考网上的注释（链接放在文末），然后加了一点我自己的解析。

```
def voc_eval(detpath,
             annopath,
             imagesetfile,
             classname,
             cachedir,
             ovthresh=0.25,
             use_07_metric=False):
    """rec, prec, ap = voc_eval(detpath,
                                annopath,
                                imagesetfile,
                                classname,
                                [ovthresh],
                                [use_07_metric])
    Top level function that does the PASCAL VOC evaluation.
    detpath: Path to detections
        detpath.format(classname) should produce the detection results file.
    annopath: Path to annotations
        annopath.format(imagename) should be the xml annotations file.
    imagesetfile: Text file containing the list of images, one image per line.
    classname: Category name (duh)
    cachedir: Directory for caching the annotations
    [ovthresh]: Overlap threshold (default = 0.5)
    [use_07_metric]: Whether to use VOC07's 11 point AP computation
        (default False)
    """
    # assumes detections are in detpath.format(classname)
    # assumes annotations are in annopath.format(imagename)
    # assumes imagesetfile is a text file with each line an image name
    # cachedir caches the annotations in a pickle file

#################################################################################################
##### 第一步：获取所有的GT标签信息，存入字典recs中或文件annots.pkl中，便于使用 #####################
#################################################################################################
    # 标签信息都是GT的信息
    # 提取annotations标签文件缓存路径
    # 如果没有缓存文件，就读取信息并创建一个二进制缓存文件annots.pkl
    if not os.path.isdir(cachedir):
        os.mkdir(cachedir)
    cachefile = os.path.join(cachedir, 'annots.pkl')
    # 从图像名称文件中读取图像名称，存入imagenames列表中
    with open(imagesetfile, 'r') as f:
        lines = f.readlines()
    imagenames = [x.strip() for x in lines]

    # 根据imagenames列表存储或读取标签信息
    if not os.path.isfile(cachefile):
        # 载入标签文件，recs这个字典中，存储了验证集所有的GT信息
        recs = {}
        for i, imagename in enumerate(imagenames):
            #解析标签xml文件，annopath为/{}.xml文件，加format表示为{}中赋值
            #imagename来源于从imagesetfile中提取，循环采集所有的的信息
            recs[imagename] = parse_rec(annopath.format(imagename))
            #解析标签文件图像进度条
            if i % 100 == 0:
                print('Reading annotation for {:d}/{:d}'.format(
                    i + 1, len(imagenames)))
        # 将读取标签内容存入缓存文件annots.pkl，这是个数据流二进制文件
        print('Saving cached annotations to {:s}'.format(cachefile))
        with open(cachefile, 'wb') as f:
            pickle.dump(recs, f)#使用了pickle.dump，存入后保存成二进制文件
    else:
        # 有标签缓存文件，直接读取,recs中存的是GT标签信息
        with open(cachefile, 'rb') as f:
            recs = pickle.load(f)
	""" Dangerous
	cachefile文件中保存的是Annotations中每张图片的信息。
	信息是从.XML文件中解析得到的，每行代表一张图片，信息之间的内容用空格分隔
	"""

#################################################################################################
##### 第二步：从字典recs中提取当前类型的GT标签信息，存入字典class_recs中，key为图片名imagename #####
#################################################################################################
    # 针对某个class名称的result文件提取对应的每个图片文件中GT的信息，存入R
    # bbox中保存该类型GT所有的box信息，difficult、det、npos等都从R中提取
    # 提取完毕针对每个图片生成一个字典，存入class_recs
    # 这里相当于根据class对图片中新不同类型目标进行归纳，每个类型计算一个AP
    class_recs = {}
    npos = 0
    
    # 上篇文章中说了当result文件名前面含有comp4_det_test_时的2种方法，这里还有个更简单的，即将classname后加上[15:]
    # 表示读取第15位开始到结束的内容，这是第3种方法
    for imagename in imagenames:
        #R中为所有图片中，类型匹配上的GT信息
        R = [obj for obj in recs[imagename] if obj['name'] == classname[15:]]
        #bbox中存储了该文件中该类型的所有box信息
        bbox = np.array([x['bbox'] for x in R])
        #difficult转化成bool型变量
        difficult = np.array([x['difficult'] for x in R]).astype(np.bool)
        #该图片中，没有匹配到当前类型det=[],匹配到1个，det=[False]，匹配到多个det=[False, ...]
        #det将是和difficult不同的地方，当不是difficult的时候，det也是false，这是一个区别
        det = [False] * len(R)
        """Dangerous
        det类似一个flag，在后面的遍历中起到选择或跳过的作用，首先全部初始化为0，具体意义可以在后面感受
        """
        #利用difficult进行计数，这里所有的值都是difficult，如果有就不计入
        npos = npos + sum(~difficult)
        #class_recs是一个字典，第一层key为文件名，一个文件名对应的子字典中，存储了key对应的图片文件中所有的该类型的box、difficult、det信息
        #这些box、difficult、det信息可以包含多个GT的内容
        class_recs[imagename] = {'bbox': bbox,
                                 'difficult': difficult,
                                 'det': det}              
		"""Dangerous
		class_recs[i]中存储的全部是属于指定类别的真实框（类型在调用voc.eval函数的时候就指定了)
		bbox记录了第i张图片中，所有属于class类的真实框的坐标信息
		"""                                 
        
#################################################################################################
##### 第三步：从当前class的result文件中读取结果，并将结果按照confidence从大到小排序 ################
#####        排序后的结果存在BB和image_ids中                                      ################
#################################################################################################

    # 读取当前class的result文件内容，这里要去result文件以class命名
    detfile = detpath.format(classname)
    with open(detfile, 'r') as f:
        lines = f.readlines()
    
    # 删除result文件中的''，对于非voc数据集，有的就没有这些内容
    splitlines = [x.strip().split(' ') for x in lines]
    """Dangerous
    detfile读取的是保存候选框结果的文件（注意和上面cache区分）， 每个候选框独占一行
    所以splitlines保存的候选框x的信息包括：所在图像名字、置信度、bd坐标   
    """
    # 将每个结果条目中第一个数据，就是图像id,这个image_ids是文件名
    image_ids = [x[0] for x in splitlines]
    # 提取每个结果的置信度，存入confidence
    confidence = np.array([float(x[1]) for x in splitlines])
    # 提取每个结果的结果，存入BB
    BB = np.array([[float(z) for z in x[2:]] for x in splitlines])
    
    # 对confidence从大到小排序，获取id
    sorted_ind = np.argsort(-confidence)
    # 获得排序值，这个值后来没有再用过
    sorted_scores = np.sort(-confidence)
    # 按confidence排序对BB进行排序
    BB = BB[sorted_ind, :]
    """Dangerous
    全都是给候选框排序
    """
    # 对相应的图像的id进行排序，其实每个图像对应一个id，即对应一个目标，当一个图中识别两个相同的GT,是可以重复的
    # 这样image_ids中，不同位置就会有重复的内容
    image_ids = [image_ids[x] for x in sorted_ind]
    """Dangerous
    因为一张图片可能有好多候选框，所以有可能好多个候选框的image_ids参数是相同的，例如这些候选框都属于第一张图片，那么image_ids都是1
    按照置信度排序，image_ids的顺序也要相应改变
    """


#################################################################################################
##### 第四步：对比GT参数和result，计算出IOU，在fp和tp相应位置标记1 #################################
#################################################################################################

    # go down dets and mark TPs and FPs
    nd = len(image_ids)#图像id的长度
    tp = np.zeros(nd)#设置TP初始值
    fp = np.zeros(nd)#设置FP初始值

    #对一个result文件中所有目标进行遍历，每个图片都进行循环，有可能下次还会遇到这个图片，如果
    for d in range(nd): ''' Dangerous：遍历所有候选框 '''
        #提取排序好的GT参数值，里面可以有多个目标，当image_ids[d1]和image_ids[d2]相同时，两个R内容相同，且都可能存了多个目标信息
        R = class_recs[image_ids[d]] 
        ''' Dangerous: 取这个候选框所在图片的所有class_recs信息，之前说过好几个候选框属于同一张图片，那么它们的R相同'''
        #将BB中confidence第d大的BB内容提取到bb中，这是result中的信息，只可能包含一个目标
        bb = BB[d, :].astype(float) '''Dangerous: 第d个候选框的bd信息'''
        ovmax = -np.inf
        #BBGT就是当前confidence从大到小排序条件下，第d个GT中bbox中的信息
        BBGT = R['bbox'].astype(float) '''Dangerous: 第d个候选框所属图片的所有真实框bd信息'''

        #当BBGT中有信息，就是没有虚警目标，计算IOU
        #当一个图片里有多个相同目标，选择其中最大IOU，GT和检测结果不重合的IOU=0
        if BBGT.size > 0:
            # compute overlaps
            # intersection
            ixmin = np.maximum(BBGT[:, 0], bb[0])
            iymin = np.maximum(BBGT[:, 1], bb[1])
            ixmax = np.minimum(BBGT[:, 2], bb[2])
            iymax = np.minimum(BBGT[:, 3], bb[3])
            #大于0就输出正常值，小于等于0就输出0
            iw = np.maximum(ixmax - ixmin + 1., 0.)
            ih = np.maximum(iymax - iymin + 1., 0.)
            inters = iw * ih
            '''Dangerous
            解释一下BBGT[:, x]的意思：
            为第d个锚框分别计算与该张图片每一个真实框的IOU，注意ixmin、iymin等的长度都等于真实框的数量。
            '''

            # union
            uni = ((bb[2] - bb[0] + 1.) * (bb[3] - bb[1] + 1.) +
                   (BBGT[:, 2] - BBGT[:, 0] + 1.) *
                   (BBGT[:, 3] - BBGT[:, 1] + 1.) - inters)

            overlaps = inters / uni#计算交并比，就是IOU
            ovmax = np.max(overlaps)#选出最大交并比，当有
            jmax = np.argmax(overlaps)#求出两个最大交并比的值的序号
            '''Dangerous: 为第d个候选框匹配出最接近的真实框'''

        #当高于阈值，对应图像fp = 1
        #ovmax > ovthresh的情况肯定不存在虚警，ovmax原始值为-inf，则没有目标肯定不可能进入if下面的任务
        if ovmax > ovthresh:
            #如果不存在difficult，初始状态，difficult和det都是False
            #找到jamx后，第一任务是确定一个tp，第二任务就是将R['det'][jmax]翻转，下次再遇到就认为是fp
            if not R['difficult'][jmax]:
                if not R['det'][jmax]:
                    tp[d] = 1.
                    R['det'][jmax] = 1
                else:
                    fp[d] = 1.#一个目标被检测两次
                '''Dangerous
                被关联的真实框jmax对应的det初始化是0，意思就是还没有被关联
                将tp[d]修改为1表示第d个锚框作为正样本，对应真实框jmax的det改为1，则表示已经被关联
                假设当循环到第k个锚框时，它的最大IOU还是出现在jmax，由于锚框是根据置信度排序的，k一定比d弱，就算它与jmax最接近，也打不过d
                所以jmax的det设置为1之后，k就不能作为正样本了，进入else分支标记为负样本
                因此参数det可以用于区分锚框是否冗余，即用来判断同一个物体重复检测
                '''
        else:
            fp[d] = 1.

#################################################################################################
##### 第五步：计算ap,rec，prec ###################################################################
#################################################################################################
##difficult用于标记真值个数，prec是precision，rec是recall
    # compute precision recall
    fp = np.cumsum(fp)#采用cumsum计算结果是一种积分形式的累加序列
    tp = np.cumsum(tp)
    rec = tp / float(npos)
    # avoid divide by zero in case the first detection matches a difficult
    # ground truth
    prec = tp / np.maximum(tp + fp, np.finfo(np.float64).eps)#maximum这一大串表示防止分母为0
    ap = voc_ap(rec, prec, use_07_metric)

    return rec, prec, ap
```

### 4：batch和ims\_per\_batch

batch值的是训练的过程中每次训练的批次，比如说我们更新权重时计算损失函数和梯度一次性要使用多少图片。而ims\_per\_batch指的是每次传入神经网络中的图片数量，比如说我们卷积的时候做数学运算的图片数量。batch就是我们最常用的batch，是我们要修改的参数，而ims\_per\_batch只是说明了图片在前向传播时进入网络的顺序，在源代码中设置为1，即图片是一张一张地传入。

然后再总结一下训练的过程。在代码中，我们对锚框进行了三次筛选，前两次是在pro（pro指RPN网络输出两个分支后的建议部分）的筛选，第三次是roi部分的筛选。

* **第一次（proposal\_layer）** 主要依据每个锚框的得分（得分指以每个像素点为中心生成锚框的得分）。  
   第一步，取得分前top1个锚框。  
   第二步，根据指定的IoU阈值对它们进行nms筛选，这里的IoU指的是每两个锚框之间的IoU，即取每组“非常相似框”中得分最高的那个框。  
   第三步，再取前top2个锚框。
* **第二次（anchor\_target\_layer）** 主要依据每个锚框与真实框关联的情况筛选，第一次筛选的框直接丢弃，而第二次筛选的框则通过标签来表示它的取舍（不做具体分类）。  
   第一步，丢弃不满足条件的锚框。对于每个锚框，计算它的最大IoU，如果最大IoU在负样本范围，则将它标签置为负样本。  
   第二步，保证每个真实框都被关联。对于每个真实框，将其IoU最大的锚框标签置为正样本。  
   第三步，选择满足条件的锚框。对于每个锚框，如果其最大IoU在正样本范围，则将它的标签置为正样本。  
   第四步，控制样本数量。我们设置好pro“输出”（只是通过标签筛选，并不是真正的输出）固定数量的锚框，同时设置好正负样本的比例。将正负样本数量剔除至规定数量，剩下的都作为不关心的样本。
* **第三次（proposal\_target\_layer）** 主要依据batch\_size和阈值筛选，跳过第二次的结果，输入为第一次输出的全部锚框，输出为经过筛选后的锚框（做具体分类），改变了锚框数量，同时也为每个锚框打标签。  
   第一步，计算每个锚框的IoU，根据设置的前景和背景阈值将它们分为两类。  
   第二步，保证输出为batch\_size的情况下，根据指定的前景框比例（背景框比例也能计算出）选择合适数量的前景和背景锚框。若都充足则随机选择；若前景充足、背景不足，则前景随机选中、背景重复选择；若前景不足、背景充足，前景全部选中、背景随机选择；若前景数量为0或背景数量为0，则对应选择batch\_size个数量不为零的类别（充足则随机选择，不足则重复选择）。

第二次的结果用于计算RPN两个分支的损失，而第三次的结果用于计算FC两个分支的损失。两次分别筛选应该是为了分别纠正上一层的输出，它们之间没有任何关系。

### 5：im\_info

im\_info（其结构为`im_info[batch_size][3]`）里装了一些信息，与Proposal结合生成输出，其中batch\_size指的是每次处理图片的数量，即ims\_per\_batch。由于源代码中我们将ims\_per\_batch设置为1，所以只需要用到im\_info[0]，而从未见过im\_info[1]或其他。 `im_info[0][0:2]`指的就是所有图片的shape信息，其中`im_info[0][0]`为height、`im_info[0][1]`为width、`im_info[0][2]`为channel。

### 6：anchor的生成机制

这里的代码有点多，各种互相调用，所以我刚开始理解有些错误，觉得有必要在这里记录一下。首先要明确，锚框的缩放比和高宽比都是先设置了一个参考锚框的，比如源代码里设置`[0, 0, 15, 15]`是一个面积为`16*16`的锚框，我们所有的尺寸都是在这个基础上去改变的，找到这个锚框的中心点，根据“面积相同高宽比不同”得到不同宽和高的锚框、然后根据这些锚框再用不同的缩放比缩放边长。

对于一张图片，我们设置步长去分割它，因为它是从左上角开始按照区域分的，而不是去预先定义好所有中心点，我刚开始就以为它并不是从中心点生成的，而是从左上角分，再固定左上角调整锚框尺寸，推翻了之前“以每个点为中心生成锚框”的想法。后来又仔细看了代码才明白，它确实是先分割成好多区域，因为区域用左上角和右下角体现，所以代码中才强调了左上角这个概念，划分好区域之后，将已知不同尺寸的锚框作用在这个区域，这样最后的效果实际上就是以中心点去生成锚框，最后再把锚框的表示方法改成两角表示法就行。

比如共有9种尺寸的基础框，它们都是在参考框的基础上变化，最后生成的这9种中心点是一样的，并不是都是起点在`(0, 0)`。所以我们知道每个区域的左上角坐标，可以把基础框看成平移单位，这样生成的锚框中心点一定在这个区域的中心点。如下，红框和绿框是基础框，`起点坐标（蓝色点）+平移坐标（红框左上角）=目标坐标（虚线左上角）`。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d7de1528b62b843e2a1dc9141a0dfe43.png)

### 7：blobs

blob和roidb很像，都是存储图片的一些信息，所以特此作区分。

blob中包含三个内容：

* `'data'`：经统一修改后的图片像素数组。
* `'gt_boxes'`：图片中所有目标框信息。长度为5，前四位是左上角和右下角坐标，最后一位是类标号。
* `'im_info'`：缩放后的图片信息。格式为`[[宽], [高], [缩放比]]`。

由于ims\_per\_batch设置为1，我们每次只处理一张图片，所以每个blob都只对应一个图片。

README【选看】
----------

### 前言

本文主要以理论以及算法结构为主，环境配置及训练虽然都认真参考教程进行了，但是因为各种原因我没有完整地测试过，所以我不确定接下来内容最后的运行效果，只是因为做了很多配置，做了很多修改，有点舍不得把记录全都删掉。  
 如果你使用本文下载的源码，希望本节能够给你提供思路和参考。

编程软件：Pycharm

### 1. Install tensorflow, preferably GPU version.

> Follow instructions. If you do not install GPU version, you need to comment out all the GPU calls inside code and replace them with relavent CPU ones.

安装tensorflow，我之前已经安装过了。

这里提到，“最好是安装GPU版本的”，如果没有GPU就要把代码中GPU相关的参数都改成CPU。但是这个源码中没见到使用GPU的部分，应该是作者已经改成CPU版本了，所以可以跳过。

### 2. Checkout this branch

这步没有实质性操作。

### 3. Install python packages

打开`requirements.txt`文件，该文件里提示了我们需要安装的库。有**cython、opencv-python、easydict、Pillow、matplotlib、scipy**。

> Cython是一种通过python语法编写C扩展的编程语言

> easydict允许以属性的方式访问dict类型,且可以递归地访问,使用起来比较方便。

可以先查看自己已安装的库，然后下载没有的，因为我懒得一个一个比对，所以我直接在项目文件里引包，报错的就是我没有的。需要注意，opencv-python引包时用的是cv2，Pillow引包使用PIL，前面已经下载过了。我这里缺少cython和easydict。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2bbc4f2ebf07993b6f23c4b5b34247d2.png)  
 接下来下载cython和easydict，具体方法略，参考：[在pycharm用python画图：matplotlib](https://blog.csdn.net/RK_Dangerous/article/details/125056104?spm=1001.2014.3001.5501)

使用`pip list` 命令检查一下是否安装成功以及版本号。然后添加到pycharm中，具体方法略，参考同上。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3ed9b0a6cfa4ccfc58222b74505cf7d9.png)

### 4. Run python setup.py build\_ext

> Go to ./data/coco/PythonAPI  
>  Run `python setup.py build_ext --inplace`  
>  Run `python setup.py build_ext install`  
>  Go to ./lib/utils and run `python setup.py build_ext --inplace`

这里我说不清楚具体的作用，出于时间关系我就先不研究了，通俗一点讲就是在使用代码前需要配置一些东西。比如目录里某些`.pyx`文件用的是C语言，是需要编译生成对应的`.c`文件才能正常使用的，利用`setup.py`得到我们需要的文件。

按照提示的步骤，先打开`Faster-RCNN/data/coco/PythonAPI`目录，右键切换到终端，如下图。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/51cdbc2b896d24259454c2a8cb8533c4.png)  
 也可以不在pycharm里，直接打开cmd，使用`cd`命令进入PythonAPI目录，如图（因为cd的用法太简单了我就不解释了，为了更直观一点，整个代码目录所在的无关路径我都打码了）：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1941b0d3b592811493b52b4ddd0e75f8.png)

#### 解决报错：Unable to find vcvarsall.bat

但是我这里报错了，提示`Unable to find vcvarsall.bat`，这个vcvarsall.bat是Visual Studio里自带的文件，我想到之前学习Faster RCNN时看的一些代码涉及到**Caffe**，由于了解也不是很多，我猜测是由于Faster RCNN是用C++写的，但是提供了python的接口，所以可以在pycharm上面使用，但还是要使用C++编译器。

由于我之前写c/c++的时候用的是软件自带的编译器，我也没有anaconda，所以可能我的电脑里没有c++编译器，也就是说我们需要下载VS。**先查看自己python版本对应的VC版本，再根据VC和VS的对应关系，下载对应的VS版本。**

使用IDEL依次输入以下代码：

```
from Lib.distutils.msvc9compiler import get_build_version
get_build_version()
```

我的结果为：

```
>>> from Lib.distutils.msvc9compiler import get_build_version
>>> get_build_version()
14.2
```

查阅：[Visual Studio各个版本对应关系](https://blog.csdn.net/yzf279533105/article/details/53677300)

我下载的是VS2015。

下载中……可自行参考网上教程，由于这里涉及到版权之类的问题，我就不放链接了。下载完毕后，再进入`\Faster-RCNN\data\coco\PythonAPI`目录，终端输入`python setup.py build_ext --inplace`不再提示报错。如下图：

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/19df24feb26fb309e078df6c2541824b.png)

#### 解决完毕

解决完问题后，还是按照要求进行下一步。

> Go to ./data/coco/PythonAPI  
>  Run `python setup.py build_ext --inplace`  
>  Run `python setup.py build_ext install`  
>  Go to ./lib/utils and run `python setup.py build_ext --inplace`

同理，输入`python setup.py build_ext install`，完成coco/PythonAPI的相关配置。

再进入`E:/Faster-RCNN/lib/utils`目录，输入`python setup.py build_ext --inplace`，关闭cmd。

打开pycharm，可以看到文件目录与之前相比多了些内容（新增内容已标注），如图：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e13d4af0d29b42d4c1acf257490a4d42.png)

### 5. Download PyCoco database.

> I will be glad if you can contribute with a batch script to automatically download and fetch. The final structure has to look like `data\VOCDevkit2007\VOC2007`

将数据集存放在`data\VOCDevkit2007\VOC2007`路径中。

要求下载coco数据集，我没有下载，所以这里不提供下载步骤。我使用的是自己制作的数据集，相关介绍见笔记：  
 [【深度学习】计算机视觉（11）——Faster RCNN（工具篇）](https://mp.csdn.net/mp_blog/creation/success/130473546)

特别注意数据集采用六位数字编码，如000001.jpg、000002.jpg。

### 6. Download pre-trained VGG16

> place it as `data\imagenet_weights\vgg16.ckpt`

因为我们在已经训练好的model的基础上去训练RPN，也就是说Faster RCNN的卷积网络是直接采用VGG-16的，而初始权重也是VGG-16中保存的对任何数据集都表现比较好的一组。

下载地址：<http://download.tensorflow.org/models/vgg_16_2016_08_28.tar.gz>

如果要使用其他模型（选看）：<https://github.com/tensorflow/models/tree/master/research/slim#pre-trained-models>

下载好压缩包之后，需要在`data`文件夹中手动新建`imagenet_weights`文件夹，解压缩并重命名为`vgg16.ckpt`放在`data\imagenet_weights\`此路径。（重命名是因为代码中对vgg的使用就是“vgg16.ckpt”）  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/87e56b9a5de6737374bee0d95d43170d.png)  
 （这里我的项目名称因为是无关的，所以打码了）

### 7. Run `train.py`

要想训练还需要修改一些内容，首先找到文件`Faster-RCNN\lib\datasets\pascal_voc.py`，找到：

```
        self._classes = ('__background__',  # always index 0
                         'aeroplane', 'bicycle', 'bird', 'boat',
                         'bottle', 'bus', 'car', 'cat', 'chair',
                         'cow', 'diningtable', 'dog', 'horse',
                         'motorbike', 'person', 'pottedplant',
                         'sheep', 'sofa', 'train', 'tvmonitor')
```

**background不变**，将之后改为自己数据集的类别，如：

```
        self._classes = ('__background__',  # always index 0
                         'cat', 'dog')
```

**注意**：每次生成的模型都保存在`Faster-RCNN\default\voc_2007_trainval\default`中，还有`Faster-RCNN\data\cache`目录下有一个后缀为pkl的文件也是每次训练生成的，在下一次训练前要**删掉整个cache文件夹和default文件夹**，每次运行train.py时都要删掉上一次的缓存文件，否则会直接获取上次的结果继续训练。

我的运行并不顺利，遇到的报错以及解决办法详见：  
 [【深度学习】计算机视觉（11）——Faster RCNN（工具篇）](https://mp.csdn.net/mp_blog/creation/success/130473546)

### 附1：修改参数

在`lib/config`下的`config.py`文件，是专门的配置文件，其中定义了模型的诸多参数，可以根据自己的需要修改相关参数，下面介绍较为重要的几个参数。

1. **network**  
    定义预训练使用的模型，源码默认使用vgg16，也可以使用resnet等模型。
2. **learning\_rate**  
    指学习率，学习率定义的太小收敛速度会很慢，学习率定义的太大可能会导致不收敛。这个参数可以多次调整，分别训练，取一个最优的学习率。
3. **batch\_size**  
    定义的是每一个梯度的大小，一般用的比较多的是32，64，128，256。batch\_size太大，内存容量可能撑不住，但是大的batch\_size相对于小的下降方向更准确，震荡更小，而且训练相同量的数据集速度更快；batch\_size太小，内存利用率就变小了，但是容易陷入局部最优。
4. **max\_iters**  
    这个参数定义的是最大的迭代次数。
5. **snap\_iterations**  
    这个参数定义的是迭代多少次保存一次模型。snap\_iterations和max\_iters要比较匹配修改，如果max\_iters参数定义的比snap\_iterations小就会导致看不到自己生成的模型了。模型保存的路径是`default/voc_2007_trainval/default`，每次保存生成4个文件。
6. **roi\_bg\_threshold\_low**  
    这个参数定义的是background（背景）认定的ROI的最小阈值。在运行train.py文件进行训练的时候如果产生`Exception：image invalid，skipping`，此时修改此处的值为0.0，会解决问题。

### 附2：使用gpu进行num的计算

这个版本的代码**完全使用CPU**，计算nms的时候也舍弃了使用GPU的选项，所以我参考其他版本的源码尝试添加“使用GPU计算nms”的方法。

首先需要下载三个文件，我选择的下载来源为<https://gitee.com/daleyang96/Faster-RCNN_TF.git>。这三个文件分别是：

1. lib/nms/gpu\_nms.pyx
2. lib/nms/gpu\_nms.hpp
3. lib/nms/nms\_kernel.cu

修改本地`/lib/utils/setup.py`文件为：

```
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy
import os
from os.path import join as pjoin


def find_in_path(name, path):
    "Find a file in a search path"
    #adapted fom http://code.activestate.com/recipes/52224-find-a-file-given-a-search-path/
    for dir in path.split(os.pathsep):
        binpath = pjoin(dir, name)
        if os.path.exists(binpath):
            return os.path.abspath(binpath)
    return None


def locate_cuda():
    """Locate the CUDA environment on the system

    Returns a dict with keys 'home', 'nvcc', 'include', and 'lib64'
    and values giving the absolute path to each directory.

    Starts by looking for the CUDAHOME env variable. If not found, everything
    is based on finding 'nvcc' in the PATH.
    """

    # first check if the CUDAHOME env variable is in use
    if 'CUDAHOME' in os.environ:
        home = os.environ['CUDAHOME']
        nvcc = pjoin(home, 'bin', 'nvcc')
    else:
        # otherwise, search the PATH for NVCC
        default_path = pjoin(os.sep, 'usr', 'local', 'cuda', 'bin')
        nvcc = find_in_path('nvcc', os.environ['PATH'] + os.pathsep + default_path)
        if nvcc is None:
          return None;
        home = os.path.dirname(os.path.dirname(nvcc))

    cudaconfig = {'home':home, 'nvcc':nvcc,
                  'include': pjoin(home, 'include'),
                  'lib64': pjoin(home, 'lib64')}
    for k, v in cudaconfig.items():
        if not os.path.exists(v):
            return None;

    return cudaconfig


CUDA = locate_cuda()


def customize_compiler_for_nvcc(self):
    """inject deep into distutils to customize how the dispatch
    to gcc/nvcc works.

    If you subclass UnixCCompiler, it's not trivial to get your subclass
    injected in, and still have the right customizations (i.e.
    distutils.sysconfig.customize_compiler) run on it. So instead of going
    the OO route, I have this. Note, it's kindof like a wierd functional
    subclassing going on."""

    # tell the compiler it can processes .cu
    self.src_extensions.append('.cu')

    # save references to the default compiler_so and _comple methods
    default_compiler_so = self.compiler_so
    super = self._compile

    # now redefine the _compile method. This gets executed for each
    # object but distutils doesn't have the ability to change compilers
    # based on source extension: we add it.
    def _compile(obj, src, ext, cc_args, extra_postargs, pp_opts):
        if os.path.splitext(src)[1] == '.cu':
            # use the cuda for .cu files
            self.set_executable('compiler_so', CUDA['nvcc'])
            # use only a subset of the extra_postargs, which are 1-1 translated
            # from the extra_compile_args in the Extension class
            postargs = extra_postargs['nvcc']
        else:
            postargs = extra_postargs['gcc']

        super(obj, src, ext, cc_args, postargs, pp_opts)
        # reset the default compiler_so, which we might have changed for cuda
        self.compiler_so = default_compiler_so

    # inject our redefined _compile method into the class
    self._compile = _compile


# run the customize_compiler
class custom_build_ext(build_ext):
    def build_extensions(self):
        customize_compiler_for_nvcc(self.compiler)
        build_ext.build_extensions(self)


ext_modules = [
    Extension("cython_bbox", ["cython_bbox.pyx"]),
]

if CUDA:
    ext_modules.append(
        Extension('gpu_nms',
            ['nms_kernel.cu', 'gpu_nms.pyx'],
            library_dirs=[CUDA['lib64']],
            libraries=['cudart'],
            runtime_library_dirs=[CUDA['lib64']],
            language="c++",
            # this syntax is specific to this build system
            # we're only going to use certain compiler args with nvcc and not with gcc
            # the implementation of this trick is in customize_compiler() below
            extra_compile_args={'gcc': ["-Wno-unused-function"],
                                'nvcc': ['-arch=sm_35',
                                         '--ptxas-options=-v',
                                         '-c',
                                         '--compiler-options',
                                         "'-fPIC'"]},
            include_dirs = [numpy.get_include(), CUDA['include'], os.path.dirname(os.path.abspath(__file__))]
        )
    )


setup(
    include_dirs=[numpy.get_include()] ,cmdclass = {'build_ext': custom_build_ext},
    ext_modules = ext_modules
)
```

其中，找到`extra_compile_args`。

`extra_compile_args`参数中有个`-arch`是根据自己CUDA的版本填写的，我没有查到具体的版本，所以在命令行使用`nvcc -arch-ls`随便选了一个最大的sm\_86。后来发现GPU算力和CUDA算力的关系很复杂，我查了一下我的GPU算力：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b70e4e7688c1e9991f76279ba4e96e88.png)  
 保险起见，改为75。

然后注意要按照上面【4. Run python setup.py build\_ext】的要求，再重新运行一下setup.py文件。

在运行setup.py文件中出现报错，可能和服务器gcc的环境配置有关，相关介绍以及解决报错的方式见：  
 [【深度学习】计算机视觉（11）——Faster RCNN（工具篇）](https://mp.csdn.net/mp_blog/creation/success/130473546)

然后需要修改几个文件中的内容，修改的部分我用注释标注了。

1. 修改config.py

```
# 添加语句
##################
# RPN Parameters #
##################
tf.app.flags.DEFINE_float('rpn_negative_overlap', 0.3, "IOU < thresh: negative example")
tf.app.flags.DEFINE_float('rpn_positive_overlap', 0.7, "IOU >= thresh: positive example")
tf.app.flags.DEFINE_float('rpn_fg_fraction', 0.5, "Max number of foreground examples")
tf.app.flags.DEFINE_float('rpn_train_nms_thresh', 0.7, "NMS threshold used on RPN proposals")
tf.app.flags.DEFINE_float('rpn_test_nms_thresh', 0.7, "NMS threshold used on RPN proposals")

'''dangerous(start)'''
if tf.test.is_gpu_available():
    tf.app.flags.DEFINE_boolean('USE_GPU_NMS', True, "Whether to use GPU implementation of non-maximum suppression")
    tf.app.flags.DEFINE_integer('GPU_ID', 0, "Default GPU device id")
else:
    tf.app.flags.DEFINE_boolean('USE_GPU_NMS', False, "Whether to use GPU implementation of non-maximum suppression")
'''dangerous(end)'''
```

2. 修改nms\_wrapper.py

```
from .py_cpu_nms import py_cpu_nms
'''dangerous(start)'''
from lib.config import config as cfg
if cfg.FLAGS.USE_GPU_NMS:
    from lib.utils.gpu_nms import gpu_nms
'''dangerous(end)'''


def nms(dets, thresh, force_cpu=False):
    """Dispatch to either CPU or GPU NMS implementations."""

    if dets.shape[0] == 0:
        return []
    # if cfg.USE_GPU_NMS and not force_cpu:
    #  return gpu_nms(dets, thresh, device_id=cfg.GPU_ID)
    # else:
    # return cpu_nms(dets, thresh)
    """dangerous(start)"""
    if cfg.FLAGS.USE_GPU_NMS and not force_cpu:
        return gpu_nms(dets, thresh, device_id=cfg.FLAGS.GPU_ID)
    else:
        return py_cpu_nms(dets=dets, thresh=thresh)
    """dangerous(end)"""
    # return py_cpu_nms(dets=dets, thresh=thresh)
```