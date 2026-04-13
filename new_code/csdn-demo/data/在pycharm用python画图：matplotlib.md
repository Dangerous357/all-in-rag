# 在pycharm用python画图：matplotlib

安装matplotlib
------------

先找到自己的python位置，再进入Scripts文件夹，我的是C:\Users\mi\AppData\Local\Programs\Python\Python39\Scripts  
 **一定要找对！否则下面的命令没有任何反应**

**以管理员身份**打开cmd，用`pip install --upgrade pip`命令升级pip

若升级失败（没用管理员身份），回到上一级python39文件夹，用这个命令`python -m ensurepip`，然后`python -m pip install --upgrade pip`重新升级一下。

然后用`python -m pip install matplotlib`这个命令安装。

打开pycharm，点击File - Settings - Project: Python（我这里是Project: Lagrange） - Project Interpreter，检查是否安装成功。

使用`import matplotlib`，如果没报错即可正常使用。

如果还是报错，大概是因为从国外下载，修改下载源即可解决。  
 贴心复制清华大学：`https://pypi.tuna.tsinghua.edu.cn/simple/`  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/860d66c9a29c92e926dbd5cc369f58b5.png)

画图举例
----

先举一个简单的小例子，是**用线性插值拟合绘图**。代码样例：

```
# 导入库
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl
from scipy.optimize import leastsq


# 多项式函数
# np.polyld([c1,c0])函数用于生成多项式函数c1x^1+c0x^0
def fit_func(p, x):
    f = np.poly1d(p)
    return f(x)


# 残差函数
def error_func(p, x, y):
    err = fit_func(p, x) - y
    return err


# 需要使用numpy.array()将样本数据(xi,yi)转换成数组形式
x_data = np.array([1.51, 1.64, 1.6, 1.73, 1.82, 1.87])  # 创建x列表存储数据的x值
y_data = np.array([1.63, 1.7, 1.71, 1.72, 1.76, 1.86])  # 创建y列表存储数据的y值
x_predict = np.arange(1.5, 2, 0.1)  # 预测区间


# 使用最小二乘函数求解参数
# leastsq()函数位于Scipy的optimize模块中，利用leastsq()函数可以对数据进行拟合。
# 参数residuals_func表示误差函数
# 参数p_init表示初始c0、c1
# 数据点
p_init = np.random.randn(2)   # 生成2个随机数，作为各项系数的初始值，用于迭代修正
plsq = leastsq(error_func, p_init, args=(x_data, y_data))
# leastsq返回的是一个元组，元组的第一个元素是多项式系数数组
print("[c0,c1] = ", end='')
print(plsq[0])


# 绘制图像
plt.scatter(x_data, y_data, label="样本点", color="black", zorder=2)
plt.plot(x_predict, fit_func(plsq[0], x_predict), label="拟合结果", color="red", zorder=1)
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
plt.title("父亲身高(x)与孩子身高(y)数据集")
plt.legend(loc="upper left")
plt.show()
```

点击运行就可以。如下：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3b19576e71fb215860641bfeb5244c2b.png)

matplotlib教程
------------

> Matplotlib 是 Python 的绘图库，它能让使用者很轻松地将数据图形化，并且提供多样化的输出格式。Matplotlib 可以绘制线图、散点图、等高线图、条形图、柱状图、3D 图形、甚至是图形动画等等。  
>  Matplotlib 通常与 NumPy 和 SciPy（Scientific Python）一起使用， 这种组合广泛用于替代 MatLab

### Pyplot

> Pyplot 是 Matplotlib 的子库，提供了和 MATLAB 类似的绘图 API。

可以使用 import 导入 pyplot 库，并设置一个别名 plt：

```
import matplotlib.pyplot as plt
```

绘制好之后要使用`plt.show()`语句可以显示该语句上面的所有操作（上面写了几个图，就一次性显示几个图），而下面的操作则需要再写一个show()去显示。

**首先需要知道几个重要的字符使用：** （使用时需要加引号）

* **颜色字符**：（多条曲线不指定颜色时，会自动选择不同颜色。）

| 字符 | 颜色 |
| --- | --- |
| b | 蓝色 |
| m | 洋红色 |
| g | 绿色 |
| y | 黄色 |
| r | 红色 |
| k | 黑色 |
| w | 白色 |
| c | 青绿色 |
| #008000 | RGB 颜色符串 |
| SeaGreen | 颜色名 |

其他颜色可以参考：[HTML 颜色值](https://www.runoob.com/html/html-colorvalues.html)

* **线型参数**：

| 类型 | 简写字符 | 线型 |
| --- | --- | --- |
| solid（默认） | ‐ | 实线 |
| dashed | ‐‐ | 破折线 |
| dashdot | ‐. | 点划线 |
| dotted | : | 虚线 |

* **标记字符**：

| 字符 | 标记 |
| --- | --- |
| . | 点标记 |
| , | 像素标记(极小点) |
| o | 实心圈标记 |
| v | 倒三角标记 |
| ^ | 上三角标记 |
| > | 右三角标记 |
| < | 左三角标记 |
| 1 | 下三叉 |
| 2 | 上三叉 |
| 3 | 左三叉 |
| 4 | 右三叉 |
| 8 | 八角形 |
| s | 正方形 |
| p | 五边形 |
| P | 加号（填充） |
| \* | 星号 |
| h | 六边形 1 |
| H | 六边形 2 |
| + | 加号 |
| x | 乘号 x |
| X | 乘号 x (填充) |
| D | 菱形 |
| d | 瘦菱形 |
| (这里写不出来，就是竖线符号） | 竖线 |
| \_ | 横线 |
| markers.0 (markers.TICKLEFT) | 左横线 |
| markers.1 (markers.TICKRIGHT) | 右横线 |
| markers.2 (markers.TICKUP) | 上竖线 |
| markers.3 (markers.TICKDOWN) | 下竖线 |
| markers.4 (markers.CARETLEFT) | 左箭头 |
| markers.5 (markers.CARETRIGHT) | 右箭头 |
| markers.6 (markers.CARETUP) | 上箭头 |
| markers.7 (markers.CARETDOWN) | 下箭头 |
| markers.8 (markers.CARETLEFTBASE) | 左箭头 (中间点为基准) |
| markers.9 (markers.CARETRIGHTBASE) | 右箭头 (中间点为基准) |
| markers.10 (markers.CARETUPBASE) | 上箭头 (中间点为基准) |
| markers.11 (markers.CARETDOWNBASE) | 下箭头 (中间点为基准) |
| “None” 、" "、 “” | 没有任何标记 |
| $ … $*（注意：中间没有空格）* | 渲染指定的字符。例如 " $ f $ " 以字母 f 为标记。 |

#### plot()方法

```
import matplotlib.pyplot as plt
import numpy as np

"""
语法：

# 画单条线
plot([x], y, [fmt], *, data=None, **kwargs)

# 画多条线
plot([x], y, [fmt], [x2], y2, [fmt2], ..., **kwargs)

参数说明：
x, y：点或线的节点，x 为 x 轴数据，y 为 y 轴数据，数据可以是列表或数组。
fmt：可选，定义基本格式（如颜色、标记和线条样式）。（后面会讲）
**kwargs：可选，用在二维平面图上，设置指定属性，如标签，线的宽度等。（后面会讲）
"""

xpoints = np.array([1, 8, 9])
ypoints = np.array([3, 10, 30])  # 必须确保x和y的数量相同

plt.plot(xpoints, ypoints)  # 使用默认样式（直线）
plt.show()

plt.plot(xpoints, ypoints, 'o')  # 不想要线，只需要描点（实心圈的标记）
plt.show()

plt.plot(ypoints)  # 如果不指定x轴上的点，则x会根据y的值来设置
plt.show()

# 当x间隔足够小时（如0.1），可以绘制出曲线
x = np.arange(0, 4*np.pi, 0.1)   # start,stop,step
y = np.sin(x)  # 两个周期的正弦
z = np.cos(x)  # 两个周期的余弦
plt.plot(x, y, x, z)  # 绘制两条曲线在同一个图像中
plt.show()
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/fdb3f58ed652bfd5ab9227ea6704cc25.png)  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/8c6dd566b0de4270ad6c390046cf0e2f.png)  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/02abce612d5a55370cbc4d7f1b8a3b95.png)  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9ea82d74bf4f79aa3e8cbd77c9a70952.png)

##### fmt详解

> fmt参数定义了基本格式，如标记、线条样式和颜色。

`fmt = '[marker][line][color]'`，fmt可以理解为是三种格式的简单集合，我们既可以一次性指定三种属性如`plt.plot(ypoints, 'o:r')`，也可以不适用fmt参数，而是单独使用后面的三个参数如`plt.plot(ypoints, marker='o')`、`plt.plot(ypoints, linestyle = 'dotted')`来指定某种格式。（设置绘图样式可查询本章中的表格）

**绘图标记marker**  
 marker参数表示绘图标记，此外，还有一些额外的参数可以设置标记。

* markersize，简写为 ms：定义标记的大小。如：`ms = 20`
* markerfacecolor，简写为 mfc：定义标记内部的颜色。
* markeredgecolor，简写为 mec：定义标记边框的颜色。

**绘图线linestyle**  
 绘图过程如果我们自定义线的样式，包括线的类型、颜色和大小等。

* 线的类型可以使用`linestyle`参数来定义，简写为`ls`。
* 线的颜色可以使用`color`参数来定义，简写为`c`。
* 线的宽度可以使用`linewidth`参数来定义，简写为`lw`，值可以是浮点数。

#### 轴标签和标题

使用`xlabel()`和`ylabel()`方法来设置 x 轴和 y 轴的标签；使用`title()`方法来设置标题。  
 **标签和标题的定位：**

* `title()`方法提供了`loc`参数来设置标题显示的位置，可以设置为: `'left'`， `'right'`，和`'center'`，默认值为`'center'`。
* `xlabel()`方法提供了`loc`参数来设置 x 轴显示的位置，可以设置为: `'left'`， `'right'`，和`'center'`，默认值为`'center'`。
* `ylabel()`方法提供了`loc`参数来设置 y 轴显示的位置，可以设置为: `'left'`， `'right'`，和`'center'`，默认值为`'center'`。

```
import numpy as np
import matplotlib.pyplot as plt

x = np.array([1, 2, 3, 4])
y = np.array([1, 4, 9, 16])
plt.plot(x, y)
plt.title("RUNOOB TEST TITLE")  # 设置标题
plt.xlabel("x - label")  # x轴的轴标签
plt.ylabel("y - label")  # y轴的轴标签

plt.show()
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9589af8e1e5ac1b7e572097fd5c66f49.png)  
 **设置字体**  
 Matplotlib默认情况不支持中文，需要额外设置字体。使用`fontproperties`参数设置字体的中文显示，使用`fontsize`或`size`设置字体大小，使用`fontdict`可以用css来设置字体样式。  
 *若使用自己下载的字体，需要将字体文件放在当前执行的代码文件中。*

```
import numpy as np
from matplotlib import pyplot as plt
import matplotlib

# 自定义字体
'''
# fname 为你下载的字体库路径（此处以SourceHanSansSC-Bold.otf字体文件为例）
font1 = matplotlib.font_manager.FontProperties(fname="SourceHanSansSC-Bold.otf", size=20)
'''

# 使用系统字体
"""
查看系统支持的字体：

a = sorted([f.name for f in matplotlib.font_manager.fontManager.ttflist])
for i in a:
    print(i)
    
在输出中找到要用的字体，如STFangsong
"""
plt.rcParams['font.family'] = ['STFangsong']  # 将字体添加到plt中

x = np.arange(1, 11)
y = 2 * x + 5
font1 = {'color': 'blue', 'size': 20}  #使用CSS设置字体样式
# fontproperties设置中文显示，fontsize或size设置字体大小，fontdict设置字体样式
plt.title("标题", fontdict=font1)
plt.xlabel("x轴", fontproperties='STFangsong', fontsize=18)
plt.ylabel("y轴", fontproperties='STFangsong', size=18)
plt.plot(x, y)
plt.show()
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a5bc5ee562f97e6e13abe8815149c44e.png)

#### grid()方法

可以使用pyplot中的`grid()`方法来设置图表中的网格线。

```
import numpy as np
from matplotlib import pyplot as plt
import matplotlib

'''
matplotlib.pyplot.grid(b=None, which='major', axis='both', )

参数说明：
b：可选，默认为 None，可以设置布尔值，true 为显示网格线，false 为不显示，如果设置 **kwargs 参数，则值为 true。
which：可选，可选值有 'major'、'minor' 和 'both'，默认为 'major'，表示应用更改的网格线。
axis：可选，设置显示哪个方向的网格线，可以是取 'both'（默认），'x' 或 'y'，分别表示两个方向，x 轴方向或 y 轴方向。
**kwargs：可选，设置网格样式，可以是 color='r', linestyle='-' 和 linewidth=2，分别表示网格线的颜色，样式和宽度。
'''

x = np.array([1, 2, 3, 4])
y = np.array([1, 4, 9, 16])

plt.title("RUNOOB grid() Test")
plt.xlabel("x - label")
plt.ylabel("y - label")
plt.plot(x, y)
plt.grid(color='r', linestyle='--', linewidth=0.5)
plt.show()
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d0867c4a9328231c1e678552e659861e.png)

#### subplot()和subplots()

可以使用pyplot中的`subplot()`和`subplots()`方法来绘制多个子图。`subplot()`方法在绘图时需要指定位置，`subplots()`方法可以一次生成多个，在调用时只需要调用生成对象的 ax 即可。

**subplot()：**

```
subplot(nrows, ncols, index, **kwargs)
```

subplot函数将整个绘图区域分成 nrows 行和 ncols 列，然后从左到右、从上到下对每个子区域进行编号1…N，左上的子区域的编号为 1、右下的区域编号为N，index参数表示下面要绘制的子图的编号。  
 例如设置 numRows ＝ 2，numCols ＝ 2，就是将图表绘制成 2x2 的图片区域, 对应的编号为：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1d6a9a448f12a9641371681aab97e183.png)  
 例：

```
import matplotlib.pyplot as plt
import numpy as np

# plot 1:
x = np.array([0, 6])
y = np.array([0, 100])

plt.subplot(2, 2, 1)
plt.plot(x, y)  # 子图的绘制方法像大图一样，就是上面用subplot指定了位置而已
plt.title("plot 1")

# plot 2:
x = np.array([1, 2, 3, 4])
y = np.array([1, 4, 9, 16])

plt.subplot(2, 2, 2)
plt.plot(x, y)
plt.title("plot 2")

# plot 3:
x = np.array([1, 2, 3, 4])
y = np.array([3, 5, 7, 9])

plt.subplot(2, 2, 3)
plt.plot(x, y)
plt.title("plot 3")

# plot 4:
x = np.array([1, 2, 3, 4])
y = np.array([4, 5, 6, 7])

plt.subplot(2, 2, 4)
plt.plot(x, y)
plt.title("plot 4")

plt.suptitle("RUNOOB subplot Test")  # 设置标题
plt.show()
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/04c82dc0861960458313755d3f7ed3a4.png)  
 **subplots()：**

```
import matplotlib.pyplot as plt
import numpy as np

"""
matplotlib.pyplot.subplots(nrows=1, ncols=1, *, sharex=False, sharey=False, squeeze=True, subplot_kw=None, gridspec_kw=None, **fig_kw)

参数说明：
nrows：默认为 1，设置图表的行数。
ncols：默认为 1，设置图表的列数。
sharex、sharey：设置 x、y 轴是否共享属性，默认为 false，可设置为 'none'、'all'、'row' 或 'col'。
        False 或 none 每个子图的 x 轴或 y 轴都是独立的，True 或 'all' 所有子图共享 x 轴或 y 轴；
        'row' 设置每个子图行共享一个 x 轴或 y 轴，'col' 设置每个子图列共享一个 x 轴或 y 轴。
squeeze：布尔值，默认为 True，表示额外的维度从返回的 Axes(轴)对象中挤出，对于 N*1 或 1*N 个子图，返回一个 1 维数组，对于 N*M，N>1 和 M>1 返回一个 2 维数组。
    如果设置为 False，则不进行挤压操作，返回一个元素为 Axes 实例的2维数组，即使它最终是1x1。
subplot_kw：可选，字典类型。把字典的关键字传递给 add_subplot() 来创建每个子图。
gridspec_kw：可选，字典类型。把字典的关键字传递给 GridSpec 构造函数创建子图放在网格里(grid)。
**fig_kw：把详细的关键字参数传给 figure() 函数。
"""

x = np.linspace(0, 2*np.pi, 400)
y = np.sin(x**2)

# subplots初步了解
fig, ax = plt.subplots()  # 返回一个元组，第二个元素ax是matplotlib.axes._subplots.AxesSubplot类型
ax.plot(x, y)  # matplotlib.axes._subplots.AxesSubplot也有plot方法？
ax.set_title('Simple plot')  # 设置标题的方法
plt.show()

# 共享y轴的两个子图
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)  # 每个子图都有名字
ax1.plot(x, y)
ax1.set_title('Sharing Y axis')  # 给子图设置标题
ax2.scatter(x, y)  # scatter方法用来描点，后面会讲
plt.show()

# 创建四个子图
fig, axs = plt.subplots(2, 2, subplot_kw=dict(projection="polar"))  # 子图也可以用坐标
# subplot_kw=dict(projection="polar") 应该是用来设置坐标轴，具体情况暂时不研究了
axs[0, 0].plot(x, y)
axs[1, 1].scatter(x, y)
plt.show()

# 每个列共享x轴
plt.subplots(2, 2, sharex='col')
# 每个行共享y轴
plt.subplots(2, 2, sharey='row')
# 每个列共享x轴且每个行共享y轴
plt.subplots(2, 2, sharex='all', sharey='all')
# 同上
plt.subplots(2, 2, sharex=True, sharey=True)
plt.show()

# 创建标识（左上角窗口编号）为10的图，已经存在的则删除
fig, ax = plt.subplots(num=10, clear=True)  # num和clear参数之前没见过
plt.show()
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9090bf470effdff1805c1233f31efdd8.png)  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b0c59605671a1d37e8c8f6aa83b09dfd.png)  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4e150c30df110b0189bac69f89e7554f.png)  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/cf9807596ea62f84337f9c24c039e826.png)  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c2252808b5657a01c3bdb3271b6c0902.png)

#### scatter()

`scatter()`方法来绘制散点图。

```
import matplotlib.pyplot as plt
import numpy as np

"""
matplotlib.pyplot.scatter(x, y, s=None, c=None, marker=None, cmap=None, norm=None, vmin=None, vmax=None, alpha=None, 
                            linewidths=None, *, edgecolors=None, plotnonfinite=False, data=None, **kwargs)

参数说明：
x，y：长度相同的数组，也就是我们即将绘制散点图的数据点，输入数据。
s：点的大小，默认 20，也可以是个数组，数组每个参数为对应点的大小。
c：点的颜色，默认蓝色 'b'，也可以是个 RGB 或 RGBA 二维行数组。
marker：点的样式，默认小圆圈 'o'。
cmap：Colormap，选择颜色条，Matplotlib 模块提供了很多可用的颜色条，其中每种颜色（color）都有一个范围从0到100的值。
    如果要在图中显示颜色条，需要使用plt.colorbar()方法。颜色条的名称见附录。
norm：Normalize，默认 None，数据亮度在 0-1 之间，只有 c 是一个浮点数的数组的时才使用。
vmin，vmax：亮度设置，在 norm 参数存在时会忽略。
alpha：透明度设置，0-1 之间，默认 None，即不透明。
linewidths：标记点的长度。
edgecolors：颜色或颜色序列，默认为 'face'，可选值有 'face', 'none', None。
plotnonfinite：布尔值，设置是否使用非限定的 c ( inf, -inf 或 nan) 绘制点。
**kwargs：其他参数。
"""

# 自定义大小和颜色
x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
y = np.array([1, 4, 9, 16, 7, 11, 23, 18])
sizes = np.array([20, 50, 100, 200, 500, 1000, 60, 90])
colors = np.array(["red", "green", "black", "orange", "purple", "beige", "cyan", "magenta"])
plt.scatter(x, y, s=sizes, c=colors)
plt.show()

# 设置两组散点图
x = np.array([5, 7, 8, 7, 2, 17, 2, 9, 4, 11, 12, 9, 6])
y = np.array([99, 86, 87, 88, 111, 86, 103, 87, 94, 78, 77, 85, 86])
plt.scatter(x, y, color='hotpink')
x = np.array([2, 2, 8, 1, 15, 8, 12, 9, 7, 3, 11, 4, 7, 14, 12])
y = np.array([100, 105, 84, 105, 90, 99, 90, 95, 94, 100, 79, 112, 91, 80, 85])
plt.scatter(x, y, color='#88c999')
plt.title("RUNOOB Scatter Test")  # 设置标题
plt.show()
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/42701ee7ff45d938a298270f82dd1c86.png)  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/684e494dcbf32f60743479e53c7a0fea.png)

#### bar()和barh()

使用pyplot中的`bar()`方法来绘制柱形图。

```
import matplotlib.pyplot as plt
import numpy as np

"""
matplotlib.pyplot.bar(x, height, width=0.8, bottom=None, *, align='center', data=None, **kwargs)

参数说明：
x：浮点型数组，柱形图的 x 轴数据。
height：浮点型数组，柱形图的高度。
width：浮点型数组，柱形图的宽度。
bottom：浮点型数组，底座的 y 坐标，默认 0。
align：柱形图与 x 坐标的对齐方式，'center' 以 x 位置为中心，这是默认值。
    'edge'：将柱形图的左边缘与 x 位置对齐。要对齐右边缘的条形，可以传递负数的宽度值及 align='edge'。
**kwargs：：其他参数。
"""

# 简单使用
x = np.array(["Runoob-1", "Runoob-2", "Runoob-3", "C-RUNOOB"])
y = np.array([12, 22, 6, 18])
plt.bar(x, y)
plt.show()

# 垂直方向的柱形图可以使用barh()方法来设置
plt.barh(x, y)
plt.show()
# bar()方法使用width设置宽度，barh()方法使用height设置

# 参数color = "#4CAF50" 设置颜色
# color = ["#4CAF50","red","hotpink","#556B2F"] 自定义各个柱形的颜色
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/75bd3e640a146499964e9c632b8b1964.png)  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a98727cbbe440b5d74722210303ef525.png)

#### pie()

使用pyplot中的`pie()`方法来绘制饼图。

```
import matplotlib.pyplot as plt
import numpy as np

"""
matplotlib.pyplot.pie(x, explode=None, labels=None, colors=None, autopct=None, pctdistance=0.6, shadow=False, 
                        labeldistance=1.1, startangle=0, radius=1, counterclock=True, wedgeprops=None, textprops=None, 
                        center=0, 0, frame=False, rotatelabels=False, *, normalize=None, data=None)[source]
                        
参数说明：
x：浮点型数组，表示每个扇形的面积。
explode：数组，表示各个扇形之间的间隔，默认值为0。
labels：列表，各个扇形的标签，默认值为 None。
colors：数组，表示各个扇形的颜色，默认值为 None。
autopct：设置饼图内各个扇形百分比显示格式，%d%% 整数百分比，%0.1f 一位小数， %0.1f%% 一位小数百分比， %0.2f%% 两位小数百分比。
labeldistance：标签标记的绘制位置，相对于半径的比例，默认值为 1.1，如 <1则绘制在饼图内侧。
pctdistance：：类似于 labeldistance，指定 autopct 的位置刻度，默认值为 0.6。
shadow：：布尔值 True 或 False，设置饼图的阴影，默认为 False，不设置阴影。
radius：：设置饼图的半径，默认为 1。
startangle：：起始绘制饼图的角度，默认为从 x 轴正方向逆时针画起，如设定 =90 则从 y 轴正方向画起。
counterclock：布尔值，设置指针方向，默认为 True，即逆时针，False 为顺时针。
wedgeprops ：字典类型，默认值 None。参数字典传递给 wedge 对象用来画一个饼图。例如：wedgeprops={'linewidth':5} 设置 wedge 线宽为5。
textprops ：字典类型，默认值为：None。传递给 text 对象的字典参数，用于设置标签（labels）和比例文字的格式。
center ：浮点类型的列表，默认值：(0,0)。用于设置图标中心位置。
frame ：布尔类型，默认值：False。如果是 True，绘制带有表的轴框架。
rotatelabels ：布尔类型，默认为 False。如果为 True，旋转每个 label 到指定的角度。
"""

# 简单使用
y = np.array([35, 25, 25, 15])

plt.pie(y,
        labels=['A', 'B', 'C', 'D'],  # 设置饼图标签
        colors=["#d5695d", "#5d8ca8", "#65a479", "#a564c9"],  # 设置饼图颜色
        explode=(0, 0.2, 0, 0),  # 第二部分突出显示，值越大，距离中心越远
        autopct='%.2f%%',  # 格式化输出百分比
       )
plt.title("RUNOOB Pie Test")
plt.show()
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ffc1e8087e2c52dc33132cb267534d9f.png)

### 附录

**颜色条**

| 颜色名称 | 保留关键字 |
| --- | --- |
| Accent | Accent\_r |
| Blues | Blues\_r |
| BrBG | BrBG\_r |
| BuGn | BuGn\_r |
| BuPu | BuPu\_r |
| CMRmap | CMRmap\_r |
| Dark2 | Dark2\_r |
| GnBu | GnBu\_r |
| Greens | Greens\_r |
| Greys | Greys\_r |
| OrRd | OrRd\_r |
| Oranges | Oranges\_r |
| PRGn | PRGn\_r |
| Paired | Paired\_r |
| Pastel1 | Pastel1\_r |
| Pastel2 | Pastel2\_r |
| PiYG | PiYG\_r |
| PuBu | PuBu\_r |
| PuBuGn | PuBuGn\_r |
| PuOr | PuOr\_r |
| PuRd | PuRd\_r |
| Purples | Purples\_r |
| RdBu | RdBu\_r |
| RdGy | RdGy\_r |
| RdPu | RdPu\_r |
| RdYlBu | RdYlBu\_r |
| RdYlGn | RdYlGn\_r |
| Reds | Reds\_r |
| Set1 | Set1\_r |
| Set2 | Set2\_r |
| Set3 | Set3\_r |
| Spectral | Spectral\_r |
| Wistia | Wistia\_r |
| YlGn | YlGn\_r |
| YlGnBu | YlGnBu\_r |
| YlOrBr | YlOrBr\_r |
| YlOrRd | YlOrRd\_r |
| afmhot | afmhot\_r |
| autumn | autumn\_r |
| binary | binary\_r |
| bone | bone\_r |
| brg | brg\_r |
| bwr | bwr\_r |
| cividis | cividis\_r |
| cool | cool\_r |
| coolwarm | coolwarm\_r |
| copper | copper\_r |
| cubehelix | cubehelix\_r |
| flag | flag\_r |
| gist\_earth | gist\_earth\_r |
| gist\_gray | gist\_gray\_r |
| gist\_heat | gist\_heat\_r |
| gist\_ncar | gist\_ncar\_r |
| gist\_rainbow | gist\_rainbow\_r |
| gist\_stern | gist\_stern\_r |
| gist\_yarg | gist\_yarg\_r |
| gnuplot | gnuplot\_r |
| gnuplot2 | gnuplot2\_r |
| gray | gray\_r |
| hot | hot\_r |
| hsv | hsv\_r |
| inferno | inferno\_r |
| jet | jet\_r |
| magma | magma\_r |
| nipy\_spectral | nipy\_spectral\_r |
| ocean | ocean\_r |
| pink | pink\_r |
| plasma | plasma\_r |
| prism | prism\_r |
| rainbow | rainbow\_r |
| seismic | seismic\_r |
| spring | spring\_r |
| summer | summer\_r |
| tab10 | tab10\_r |
| tab20 | tab20\_r |
| tab20b | tab20b\_r |
| tab20c | tab20c\_r |
| terrain | terrain\_r |
| twilight | twilight\_r |
| twilight\_shifted | twilight\_shifted\_r |
| viridis | viridis\_r |
| winter | winter\_r |

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f7c4679f7efa74ba31b1d521977b2208.png)  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9c3c921e0b69b4c87ab2b055c04cc1dc.png)  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/014f5c720aa965d215e5ce67e89c86c9.png)  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ee43b10c2116fac7f830820d4a6bc899.png)  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4b0888c480673c09d525ce08a8d8f44e.png)  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/fe83c01c5c28294a0e2b6285ddee58b8.png)  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/43b52582dec003615d8c2aac89880c99.png)

---

参考来源：  
 [在Pycharm中安装matplotlib](https://blog.csdn.net/WEN8910/article/details/109105109)  
 [Matplotlib安装](https://blog.csdn.net/weixin_44768795/article/details/120613424)  
 [在Pycharm中安装matplotlib](https://blog.csdn.net/WEN8910/article/details/109105109)  
 [pip install XXX总是报错，例如：Exception: Traceback (most recent call last):这种错误怎么办？](https://blog.csdn.net/ywxjy/article/details/123488709)