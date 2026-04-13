# nlkt中BigramAssocMeasures.pmi()方法的传参和使用

这个问题找遍全网没看到详细的介绍，最后用读代码+数学公式的方法才理解怎么用。

**BigramAssocMeasures.pmi**

作用：计算x和y的互信息（互信息是什么我就不科普啦）

这里有个误区刚开始我以为是计算两个词之间的依赖程度，但是它其实是可以计算词和类别的依赖程度的。

对照这个：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0e71f912146d905efbb3ca452502c34b.png)

所以我就拿t表示特征，c表示类别，要想使用BigramAssocMeasures.pmi()计算t和c的互信息（这里举的例子是二分类问题），需要传参如下：

注意，文档数量也可以理解为词频。且参数1和参数3不能为0。

* 参数1：“是这个特征也是这个类”的文档数量，是int类型
* 参数2：[积极类的文档数量， 消极类的文档数量]，是一个列表（不是列表也可以，可以迭代就行）
* 参数3：文档总数，是int类型

```
from nltk import BigramAssocMeasures

ngram = 2
total = 7
unigram = [4, 3]

# 使用BigramAssocMeasures.pmi()计算互信息
score = BigramAssocMeasures.pmi(ngram, unigram, total)
print(score)
```