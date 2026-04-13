# 如何自己开发一个Android APP（3）——XML和Android

XML是一种用于保存数据值的语言。

XML是一种标记语言，类似于HTML——如果之前接触过Web开发的话。XML文件利用树状结构作为数据模型。通常来说，一个布局文件拥有一个根布局元素，并将其作为特定布局类型模型——其中所包含的用于UI条目的子元素则包括按钮、图片及文本等。

基础知识
----

### 语法

在XML中，数据值被保存在元素当中。单一元素通常包含一个开始标记与一个结束标记。例如：

```
<product>Onion</product> 
<!-- 数据值即元素内容，文本字符串“Onion” -->
```

开始标记也可以容纳与数据项目相关的其它属性信息。每项属性都有一个名称与一个值，其中值就是引号内的部分。

```
<product type="vegetable">Onion</product>
```

元素中还可以包含其它元素，例如：

```
<section name="food">
<product type="vegetable">Onion</product>
<product type="fruit">Banana</product>
</section>
<!-- 我们将section元素称为主元素、products元素则被称为子元素。两个子元素之间属于“兄弟关系”。-->
```

*在XML文档当中，必须存在一个root元素作为主元素，或者被称为“嵌套”。这就构成了一种tree结构（如本文开始所述），其中子元素作为自主元素延伸出去的分支。如果某个子元素之下还包含其它子元素，那么它本身同时也具有主元素属性。*

自结束元素，其中开始与结束标记并非独立存在，例：

```
<order number="12345" customerID="a4d45s"/>
```

### 单位

* dp(dip): device independent pixels(设备独立像素)。 不同设备有不同的显示效果，支持WVGA、HVGA和QVGA 。
* px: pixels(像素). 不同设备显示效果相同，一般我们HVGA代表320x480像素，这个用的比较多。
* pt: point，是一个标准的长度单位，1pt＝1/72英寸，用于印刷业，非常简单易用。
* sp: scaled pixels(放大像素). 主要用于字体显示best for textsize。

布局
--

```
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/hello_world" />

</RelativeLayout>
```

### 布局元素

#### LinearLayout（线性布局）

LinearLayout会沿横向或者纵向显示我们打算使用的View。

`android:orientation`属性为线性布局指定方式，组件的排列方向是水平（horizontal）还是竖直（vertical），默认为竖直。若垂直方向显示，则每个View都会沿屏幕下方依次排列；如果采取横向布局，那么各个View将由左至右依次排列。  
 **关于布局内部组件间的位置关系：当android:orientation=“vertical” 时， 只有水平方向的设置才起作用，垂直方向的设置不起作用。 即：left，right，center\_horizontal 是生效的。 当 android:orientation=“horizontal” 时， 只有垂直方向的设置才起作用，水平方向的设置不起作用。 即：top，bottom，center\_vertical 是生效的。**

`android:divider`属性为线性布局设置分割线图片，通过`android:showDividers`属性来设置分割线的所在位置，有四个可选值none（无）, middle（每两个组件间）, begining（开始）, end（结束），还可以通过`dividerPadding`设置分割线的padding（填充）。  
 演示代码：

```
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"  
    xmlns:tools="http://schemas.android.com/tools"  
    android:id="@+id/LinearLayout1"  
    android:layout_width="match_parent"  
    android:layout_height="match_parent"  
    android:divider="@drawable/ktv_line_div"  
    android:orientation="vertical"  
    android:showDividers="middle"  
    android:dividerPadding="10dp"  
    tools:context="com.jay.example.linearlayoutdemo.MainActivity" >  
  
    <Button  
        android:layout_width="wrap_content"  
        android:layout_height="wrap_content"  
        android:text="按钮1" />  
  
    <Button  
        android:layout_width="wrap_content"  
        android:layout_height="wrap_content"  
        android:text="按钮2" />  
  
    <Button  
        android:layout_width="wrap_content"  
        android:layout_height="wrap_content"  
        android:text="按钮3" />  
  
</LinearLayout>
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a0ef10fc6c826f6fe5a4b649cc431d5e.png)

#### RelativeLayout（相对布局）

* `ignoreGravity`属性：设置了该属性为true的属性的组件，将不受gravity属性的影响。

**定位方式属性详解：**  
 语法为：`对应对齐方式='true'`

1. 根据父容器定位  
    `android:layout_alignParentLeft`：左对齐  
    `android:layout_alignParentRight`：右对齐  
    `android:layout_alignParentTop`：顶部对齐  
    `android:layout_alignParentBottom`：底部对齐  
    `android:layout_centerHorizontal`：水平居中  
    `android:layout_centerVertical`：垂直居中  
    `android:layout_centerInParent`：中间位置  
    ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5cf63b048103aedc75fa04423928c751.png)
2. 根据兄弟组件定位  
    `android:layout_toLeftOf`：参考组件的左边  
    `android:layout_toRightOf`：参考组件的右边  
    `android:layout_above`：参考组件的上方  
    `android:layout_below`：参考组件的下方  
    `android:layout_alignTop`：对齐参考组件的上边界  
    `android:layout_alignBottom`：对齐参考组件的下边界  
    `android:layout_alignLeft`：对齐参考组件的左边界  
    `android:layout_alignRight`：对齐参考组件的右边界  
    **典型例子——梅花布局：**  
    ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/32845fc02a73800dc30017884a4d586d.png)

```
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"    
    xmlns:tools="http://schemas.android.com/tools"    
    android:id="@+id/RelativeLayout1"    
    android:layout_width="match_parent"    
    android:layout_height="match_parent" >    
    
    <!-- 这个是在容器中央的 -->    
        
    <ImageView    
        android:id="@+id/img1"     
        android:layout_width="80dp"    
        android:layout_height="80dp"    
        android:layout_centerInParent="true"    
        android:src="@drawable/pic1"/>    
        
    <!-- 在中间图片的左边 -->    
    <ImageView    
        android:id="@+id/img2"     
        android:layout_width="80dp"    
        android:layout_height="80dp"    
        android:layout_toLeftOf="@id/img1"    
        android:layout_centerVertical="true"    
        android:src="@drawable/pic2"/>    
        
    <!-- 在中间图片的右边 -->    
    <ImageView    
        android:id="@+id/img3"     
        android:layout_width="80dp"    
        android:layout_height="80dp"    
        android:layout_toRightOf="@id/img1"    
        android:layout_centerVertical="true"    
        android:src="@drawable/pic3"/>    
        
    <!-- 在中间图片的上面-->    
    <ImageView    
        android:id="@+id/img4"     
        android:layout_width="80dp"    
        android:layout_height="80dp"    
        android:layout_above="@id/img1"    
        android:layout_centerHorizontal="true"    
        android:src="@drawable/pic4"/>    
        
    <!-- 在中间图片的下面 -->    
    <ImageView    
        android:id="@+id/img5"     
        android:layout_width="80dp"    
        android:layout_height="80dp"    
        android:layout_below="@id/img1"    
        android:layout_centerHorizontal="true"    
        android:src="@drawable/pic5"/>    
    
</RelativeLayout>
```

3. 设置margin偏移（即组件和父容器的边距）  
    `layout_margin`：设置组件上下左右的偏移量  
    `layout_marginLeft`：设置组件离左边的偏移量  
    `layout_marginRight`：设置组件离右边的偏移量  
    `layout_marginTop`：设置组件离上面的偏移量  
    `layout_marginBottom`：设置组件离下面的偏移量  
    **注意：margin可以设置为负数。**

**padding（填充）**：设置组件内部元素间的边距（如Textview里的字体位置）

* `android:padding`：往内部元素的上下左右填充一定边距
* `android:paddingLeft`：往内部元素的左边填充一定边距
* `android:paddingRight`：往内部元素的右边填充一定边距
* `android:paddingTop`：往内部元素的上方填充一定边距
* `android:paddingBottom`：往内部元素的下方填充一定边距

#### TableLayout（表格布局）

**基本使用：**  
 一个组件沾满一行，也可以通过添加TableRow容器，将几个组件放在一行（构成几列），TableRow中组件的个数决定了该行有多少列，而列的宽度由该列中最宽的单元格决定。

TableRow的layout\_width属性是fill\_parent固定不变，layout\_height默认是wrap\_content且可以自定义大小。  
 **常用属性：**

1. `android:collapseColumns`：设置需要被隐藏的列的序号。
2. `android:stretchColumns`：设置允许被收缩的列的列序号。收缩到适应父容器宽度的程度。
3. `android:shrinkColumns`：设置允许被拉伸的列的列序号。拉伸到填满整行的程度。  
    **注意：** 以上这三个属性的列号都是从0开始算的；可以设置多个，用逗号隔开；如果所有列都生效则用"\*"号即可。
4. `android:layout_column`：表示跳过第x个，直接显示到第x+1个格子处。注意：从1开始算起。
5. `android:layout_span`：表示合并x个单元格，即这个组件占x个单元格。

#### FrameLayout（帧布局）

FrameLayout(帧布局)直接在屏幕上开辟出一块空白的区域，当我们往里面添加控件的时候会默认把他们放到这块区域的左上角。帧布局的大小由控件中最大的子控件决定，如果控件的大小一样大的话，那么同一时刻就只能看到最上面的那个组件，即后续添加的控件会覆盖前一个。

**前景图像：** 永远处于帧布局最上面，不会被覆盖。

* `android:foreground`:设置改帧布局容器的前景图。
* `android:foregroundGravity`:设置前景图像显示的位置。例如值为right|bottom设置在右下角。

#### AbsoluteLayout（绝对布局）

通过X,Y坐标来控制组件在Activity中的位置。**单位是dp**。

除了通用属性width和height外，还有两个控制位置的属性：

* `android:layout_x`属性：设置组件的X坐标。
* `android:layout_y`属性：设置组件的Y坐标。

#### GridLayout（网格布局）

Android4.0后引入的，最小sdk版本要在14及以上。低版本sdk需要导入v7包的gridlayout包（v7包一般在sdk下的:sdk\extras\android\support\v7\gridlayout目录下）。使用时添加标签：`<android.support.v7.widget.GridLayout>`。此处暂时不过多赘述。

可以自己设置布局中组件的排列方式；自定义网格布局有多少行，多少列；直接设置组件位于某行某列；设置组件横跨几行或者几列。

* `android:orientation`属性：设置排列方式。默认为vertical（竖直），或者设置为水平（horizontal）。
* `android:layout_gravity`属性：设置对齐方式，如center，left，right，bottom等，若想同时使用两种如“bottom|left”
* `android:rowCount`属性：设置行数。
* `android:columnCount`属性：设置列数。
* `android:layout_row`属性：设置组件所在的行（从0开始）。不设置默认每个组件占一个单元格。
* `android:layout_column`属性：设置组件所在的列（从0开始）。不设置默认每个组件占一个单元格。
* `android:layout_rowSpan`属性：设置组件横跨几行。
* `android:layout_columnSpan`属性：设置组件横跨几列。如果需要组件填满横跨的几行或几列，需要给该组件添加属性使`android:layout_gravity = "fill"`。

### xml命名空间

在布局文件中，`xmlns:android="http://schemas.android.com/apk/res/android"` 和 `xmlns:tools="http://schemas.android.com/tools"` 用于在xml命名空间中定义我们所需要使用的架构。有了它就可以按 “alt + / ”作为语法提示。

### tools:context

设置对应的渲染上下文主题。

### 布局通用属性

**通过键入`android：`输入属性。**

* `gravity`属性：  
   控制组件所包含的子元素的对齐方式。可多个组合如（left|buttom）。若以`center_horizontal`作为gravity值，其中包含的元素就会以X轴为中心加以显示。
* `layout_gravity`属性：控制该组件在父容器里的对齐方式。
* `layout_width`属性：  
   若值为`fill_parent`或`match_parent`，布局会被拉伸至横向的最大长度；`wrap_content`使View的宽度足以容纳其显示内容。
* `layout_height`属性：  
   若值为`fill_parent`或`match_parent`，布局会被拉伸至纵向的最大长度；`wrap_content`使View的高度足以容纳其显示内容。
* `layout_margin`属性：边距属性，使用“dp”为数值单位来设置像素的独立密度。
* `id`属性：例如`android:id="@+id/LinearLayout1"`为这个布局设置一个id值标记为LinearLayout1，并添加到R文件的id内部类中。
* `background`属性：为该组件设置一个背景图片，或者直接用颜色覆盖。
* `layout_weight`属性：设置该布局权重，等比例地划分区域。若要按比例划分水平方向，需要将涉及到的view的width属性设置为0dp，然后设置weight的值；若要按比例划分竖直方向，需要将涉及到的view的height属性设置为0dp，然后设置weight的值。或者设置为wrap\_content，但不要设置成fill\_parent，因为它的计算规则和你想要的结果不一样。

view
----

View是绘制在屏幕上的用户能与之交互的一个对象。View属于可见及交互性元素，用以构成我们的应用程序UI。**应用程序中的每套分屏方案都要选择一种View，并在其中包含一种或者多种布局机制。**

在Android系统中，这些布局被称为ViewGroup对象，每个 ViewGroup内包含一套或者多套View。ViewGroup是一个用于存放其他View（和ViewGroup）对象的布局容器。

如果使用java代码自定义了一个组件，需要在布局文件中添加以下代码：

```
<com.作者.包名.类名
        android:layout_width="match_parent"
        android:layout_height="match_parent"/>
```

### 分割线

可以通过直接在布局中添加一个view显示一条分割线。（该例子便于我们了解view的具体用法）如下代码将会显示一条水平方向的黑线。

```
<View  
    android:layout_width="match_parent"  
    android:layout_height="1px"  
    android:background="#000000" />
```

### 通用属性

组件可以使用所在布局中的属性，除了上述提到的布局通用属性外，view还有一些常用属性：

* `android:layout_gravity`属性：值可以为fill。
* `android:layout_marginLeft`属性：左边距。
* `android:layout_marginRight`属性：右边距。

### TextView元素

布局元素当中的TextView允许开发人员显示一条文本字符串。TextView是View的一种。

注意：TextView是很多其他控件的父类（如Button），这些控件均可以使用TextView的属性。

**与文本相关属性：**

* `android:text`属性：通过列举文本字符串实现显示功能。将每一个文本字符串值保存为一项值资源，使用@string资源调用。语法为：`@string/字符串名称`，通过在字符串名称前加上@string的方式告知Android工具需要在哪里寻找字符串资源。
* `android:textSize`属性：设置文本大小。单位为sp。
* `android:textColor`属性：文本颜色。一般通过colors.xml资源来引用。
* `android:textStyle`属性：可以设置normal（无效果）、bold（加粗）、italic（斜体），若多选用" | "分隔。
* `android:textScaleX`属性：设置字间距，控制字体水平方向的缩放，默认值1.0f，值是float。
* `android:lineSpacingExtra`属性：设置行间距，如"3dp"。
* `android:lineSpacingMultiplier`属性：设置行间距的倍数，如"1.2"。

**与文本阴影相关的属性：**

* `android:shadowColor`属性、`android:shadowRadius`属性搭配使用：前者设置阴影颜色，后者设置阴影的模糊程度（0.1为字体颜色，建议使用3.0）。
* `android:shadowDx`属性：设置阴影在水平方向的偏移,就是水平方向阴影开始的横坐标位置。
* `android:shadowDy`属性：设置阴影在竖直方向的偏移,就是竖直方向阴影开始的纵坐标位置。

**添加边框：**

设置边框需要编写一个shapeDrawable资源文件放置在drawable文件夹中（文件名只能由小写英文字母和阿拉伯数字组成），然后将TextView的background设置为这个资源，值为`"@drawable/shape文件名"`。

shapeDrawable文件编写格式如下：  
 注意不要直接复制别人的代码，里面的空格会报错，最好自己往上敲。

```
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" >
	<!-- 在此处添加元素，常用元素在下方列出 -->
	
	<!-- 设置背景颜色 -->
	<solid android:color = "#000000"/>
	
	<!-- 设置边框的粗细、边框颜色 -->
	<stroke
		android:width = "2dp"
		android:color="#111111"/>
	
	<!-- 设置边距（top、bottom、left、right） -->
	<padding android:bottom = "5dp"/>
	
	<!-- 设置四个圆角的半径-->
	<corners
		android:topLeftRadius="10px"
		android:topLeftRadius="10px"
		android:bottomLeftRadius="10px"
		android:bottomRightRadius="10px"/>
	
	<!-- 设置渐变色
		startColor属性:起始颜色。
		endColor属性:结束颜色。
		centerColor属性:中间颜色。
		angle属性:方向角度。angle= 0 度时从左到右逆时针方向转；当angle = 90度时从下往上。
		type属性:设置渐变的类型 -->
	<gradient></gradient>
</shape>
```

**添加图片**

利用四个属性分别给TextView的四个位置添加图片：`drawableTop`(上)，`drawableButtom`(下)，`drawableLeft`(左)，`drawableRight`(右)。

使用`drawablePadding`属性设置图片与文字间的间距。

**添加autoLink识别链接**

使用`android:autoLink`属性后，程序自动识别对应类型，在用户界面可以通过点击文本跳转到对应目的程序中。autoLink的值可以为web、email、phone等，all表示各种类型全部包含（自动识别协议头）。

**设置跑马灯效果**  
 需要将以下代码组合使用：

* `android:singleLine="true"`  
   设置是否自动换行，默认为需要自动换行（false），设置为 true 表示不需要自动换行。注意：若要设置多行显示不完，可添加`maxLines`属性。
* `android:ellipsize="marquee"`
* `android:marqueeRepeatLimit="marquee_forever"`
* `android:focusable="true"`
* `android:focusableInTouchMode="true"`

### EditText输入框

**设置默认提示文本**

* `android:hint="默认提示文本"`，设置提示的文本内容。
* `android:textColorHint="#95A1AA"`，设置提示文本的颜色。

**限制输入类型**  
 `android:inputType`属性可以对输入的数据进行限制。可选参数如下：

```
android:inputType="none"  
android:inputType="text"  
android:inputType="textCapCharacters"  
android:inputType="textCapWords"  
android:inputType="textCapSentences"  
android:inputType="textAutoCorrect"  
android:inputType="textAutoComplete"  
android:inputType="textMultiLine"  
android:inputType="textImeMultiLine"  
android:inputType="textNoSuggestions"  
android:inputType="textUri"  
android:inputType="textEmailAddress"  
android:inputType="textEmailSubject"  
android:inputType="textShortMessage"  
android:inputType="textLongMessage"  
android:inputType="textPersonName"  
android:inputType="textPostalAddress"  
android:inputType="textPassword"  
android:inputType="textVisiblePassword"  
android:inputType="textWebEditText"  
android:inputType="textFilter"  
android:inputType="textPhonetic" 
android:inputType="number"  
android:inputType="numberSigned"  
android:inputType="numberDecimal"  
android:inputType="phone"//拨号键盘  
android:inputType="datetime"  
android:inputType="date"//日期键盘  
android:inputType="time"//时间键盘
```

**设置显示方式**  
 默认多行显示的，自动换行。

* `android:minLines="3"`，设置最小行的行数。
* `android:maxLines="3"`，设置最大的行数。当输入内容超过maxline,文字会自动向上滚动。
* `android:singleLine="true"`，设置单行输入，而且不会滚动。
* `android:textScaleX="1.5"` ，设置字与字的水平间隔。
* `android:textScaleY="1.5"` ，设置字与字的垂直间隔

**弹出小键盘**  
 `android:windowSoftInputMode`属性设置Activity主窗口与软键盘的交互模式（需要与java文件中焦点获取方法配合使用）。该属性控制两个方面的内容：（1）当有焦点产生时，软键盘是隐藏还是显示；（2）是否减少活动主窗口大小以便腾出空间放软键盘。

可选值如下，多选时用"|"分开：

* `stateUnspecified`：软键盘的状态并没有指定，系统将选择一个合适的状态或依赖于主题的设置。
* `stateUnchanged`：当这个activity出现时，软键盘将一直保持在上一个activity里的状态，无论是隐藏还是显示。
* `stateHidden`：用户选择activity时，软键盘总是被隐藏。
* `stateAlwaysHidden`：当该Activity主窗口获取焦点时，软键盘也总是被隐藏的。
* `stateVisible`：软键盘通常是可见的。
* `stateAlwaysVisible`：用户选择activity时，软键盘总是显示的状态。
* `adjustUnspecified`：默认设置，通常由系统自行决定是隐藏还是显示。
* `adjustResize`：该Activity总是调整屏幕的大小以便留出软键盘的空间。
* `adjustPan`：当前窗口的内容将自动移动以便当前焦点从不被键盘覆盖和用户能总是看到输入内容的部分。

**其他属性归纳**

* `android:selectAllOnFocus="true"`，表示点击输入框获得焦点后，全选输入框中所有的文本内容。
* `android:capitalize`属性设置英文字母大写类型，默认为none。三个可选值：`sentences`：仅第一个字母大写；`words`：每一个单词首字母大小，用空格区分单词；`characters`：每一个英文字母都大写。
* 与TextView类似，使用margin相关属性增加组件相对其他控件的距离，比如`android:marginTop = "5dp"`，使用padding增加组件内文字和组件边框的距离，比如`android:paddingTop = "5dp"`。

### Button元素

前面已经提到过，Button是继承了TextView的，我们强调：

* 按钮上显示的是`android:text`属性值。
* `android:id`属性用于识别每一个独特的view。语法为：`android:id="@+id/按钮ID名"`。“@+id”语法会提示Android工具在项目资源“R.java”文件中创建一个新ID，并为其指定一个在应用程序内独一无二的文本字符串。

**设置按钮按下的效果**  
 通过编写**StateListDrawable**资源文件罗列不同状态下组件如何绘画，在java文件中设置动作监听者，将Button的background属性设置为该drawable资源即可实现背景色/背景图片的变化。如：

StateListDrawable的关键节点 是`< selector >`，其属性如下：

* `drawable`:引用的Drawable位图，可以把他放到最前面，就表示组件的正常状态。
* `state_focused`:是否获得焦点。
* `state_window_focused`:是否获得窗口焦点。
* `state_enabled`:控件是否可用。
* `state_checkable`:控件可否被勾选，例如`checkbox`。
* `state_checked`:控件是否被勾选。
* `state_selected`:控件是否被选择，针对有滚轮的情况。
* `state_pressed`:控件是否被按下。
* `state_active`:控件是否处于活动状态，例如`slidingTab`。
* `state_single`:控件包含多个子控件时，确定是否只显示一个子控件。
* `state_first`:控件包含多个子控件时，确定第一个子控件是否处于显示状态。
* `state_middle`:控件包含多个子控件时，确定中间一个子控件是否处于显示状态。
* `state_last`:控件包含多个子控件时，确定最后一个子控件是否处于显示状态。

```
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_pressed="true" android:drawable="@drawable/ic_course_bg_fen"/>
    <item android:state_enabled="false" android:drawable="@drawable/ic_course_bg_pressed"/>
    <item android:drawable="@drawable/ic_course_bg_cheng"/>
</selector>
```

其语法结构可理解为，当组件处于某种状态时，以某种drawable形式展现，无状态条件时其drawable即为默认drawable。

**设置按钮外观**  
 按钮外观的设置和TextView类似，通过编写ShapeDrawable资源文件实现，其标签为`<shape />`。若需要根据状态动态变化，可将shape标签嵌入到item标签中。

注意：我们说ShapeDrawable，指的是该文件的类型，不代表两种不同类型的代码必须分开写，它们的命名也不要求区分。

### ImageView图像视图

用来显示图像的一个View或者控件。常用属性如下：

* `android:src`属性：设置图片，强调组件内容，按照图片大小直接填充，并不会进行拉伸。
* `android:background`属性：设置图片，强调组件背景，会根据ImageView给定的宽度来进行拉伸图片。
* `setAlpha`属性：为src设置透明度。
* `adjustViewBounds`属性、`android:maxHeight`属性、`android:maxWidth`属性配合使用，用于设置缩放时是否保持原图长宽比， 单独设置不起作用。  
   用法：将`adjustViewBounds`的值设置为true，`android:maxHeight`表示设置ImageView的最大高度，`android:maxWidth`表示设置ImageView的最大宽度。
* `scaleType`属性：设置显示的图片如何缩放或者移动以适应ImageView的大小。可选值如下：  
   `fitXY`:对图像的横向与纵向进行独立缩放，使得该图片完全适应ImageView，但是图片的横纵比可能会发生改变。  
   `fitStart`:保持纵横比缩放图片，尽可能大地填充view，缩放完成后将图片放在ImageView的左上角。  
   `fitCenter`:同上，缩放后放于中间。  
   `fitEnd`:同上，缩放后放于右下角。  
   `center`:保持原图的大小，显示在ImageView的中心。当原图的size大于ImageView的size，超过部分裁剪处理。  
   `centerCrop`:保持横纵比缩放图片，完全覆盖ImageView，可能会出现图片的显示不完全。  
   `centerInside`:保持横纵比缩放图片，直到ImageView能够完全地显示图片。  
   `matrix`:默认值，不改变原图的大小，从ImageView的左上角开始绘制原图， 原图超过ImageView的部分作裁剪处理。

**添加图片固定尺寸的图片**  
 已知background会拉伸图片，可以通过编写drawable的Bitmap资源文件，将然后background属性设置为该文件即可。  
 `titleMode`属性是平铺，设置`disabled`表示禁止平铺。

```
<bitmap  
    xmlns:android="http://schemas.android.com/apk/res/android"  
    android:id="@id/pen_bg"  
    android:gravity="top"  
    android:src="@drawable/pen"  
    android:tileMode="disabled" >  
</bitmap>
```

### RadioButton单选按钮

通过把RadioButton放到RadioGroup按钮组中，实现单选功能。可以先为外层RadioGroup组件设置外观属性。**注意一定要为每一个单选按钮添加ID。**  
 举个简单的例子：

```
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:id="@+id/LinearLayout1"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    tools:context=".MainActivity" >

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="请选择性别"
        android:textSize="23dp"
        />

    <RadioGroup
        android:id="@+id/radioGroup"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:orientation="horizontal">

        <RadioButton
            android:id="@+id/btnMan"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="男"
            android:checked="true"/>

        <RadioButton
            android:id="@+id/btnWoman"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="女"/>
    </RadioGroup>

    <Button
        android:id="@+id/btnpost"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="提交"/>

</LinearLayout>
```

### CheckBox复选框

**更改按钮外观**  
 通过编写StateListDrawable资源文件，分别设置选中和未选中状态的item标签`android:drawable="@mipmap/图片名"`。我们注意到图片的存放位置在mipmap（贴图）文件夹中。然后有两个方法：

1. android:button=“@drawable/selctor名字”，设置button属性。
2. 在style资源文件中添加以下style，并设置复选框的`android:style`属性为`"@style/MyCheckBox"`。

```
<style name="style名（如：MyCheckBox）" parent="@android:style/Widget.CompoundButton.CheckBox">
        <item name="android:button">@drawable/selctor名</item>
</style>
```

**改变文字与按钮的位置**  
 与为TextView添加图片类似，通过设置drawable上/下/左/右，改变按钮的位置（或是替换成其他效果）。下面两个属性必须配合使用：

```
android:button="@null"
android:drawableTop="@android:drawable/btn_radio"
```

**修改文字与按钮的距离**  
 通过改变`android:paddingTop`、`android:paddingBottom`、`android:paddingLeft`、`android:paddingRight`的值设置文字与按钮的距离。

### ToggleButton开关按钮

常用属性：

* `android:disabledAlpha`：设置按钮在禁用时的透明度。
* `android:textOff`：按钮没有被选中时显示的文字。
* `android:textOn`：按钮被选中时显示的文字。

除直接设置属性外，可以通过编写selector，然后设置Background属性即可。

### Switch开关

常用属性：

* `android:showText`：设置on/off的时候是否显示文字，值为boolean。
* `android:splitTrack`：是否设置一个间隙，让滑块与底部图片分隔，值为boolean。
* `android:switchMinWidth`：设置开关的最小宽度。
* `android:switchPadding`：设置滑块内文字的间隔。
* `android:switchTextAppearance`：设置开关的文字外观。
* `android:textOff`：滑块没有打开时显示的文字。
* `android:textOn`：滑块打开时显示的文字。
* `android:textStyle`：文字风格（如斜体、粗体、下划线等）。
* `android:track`：底部的图片。
* `android:thumb`：滑块的图片。
* `android:typeface`：设置字体，默认支持这三种：sans，serif，monospace。除此以外还可以使用 其他字体文件(\*.ttf)，首先要将字体文件保存在assets/fonts/目录下，并在Java代码中设置： Typeface typeFace =Typeface.createFromAsset(getAssets(),“fonts/HandmadeTypewriter.ttf”); textView.setTypeface(typeFace);

如果通过编写selector文件设置样式，注意：`state_pressed`指的是滑块是否被点击，`state_checked`指的是开关是否打开。

### ProgressBar进度条

默认为圆形进度条，大小适中。通过设置style修改大小，根据系统提供的参数，分别为：`style="@android:style/Widget.ProgressBar.Large"`和`style="@android:style/Widget.ProgressBar.Small"`。也可以利用系统提供的参数设置水平进度条：`style="@android:style/Widget.ProgressBar.Horizontal"`。

* `android:max`：进度条的最大值。
* `android:progress`：进度条已完成进度值。
* `android:progressDrawable`：设置轨道对应的Drawable对象。
* `android:indeterminate`：如果设置成true，则进度条不精确显示进度。
* `android:indeterminateDrawable`：设置不显示进度的进度条的Drawable对象。可以设置自定义的资源，但是无法改变大小。
* `android:indeterminateDuration`：设置不精确显示进度的持续时间。
* `android:secondaryProgress`：二级进度条，类似于视频播放的缓冲进度。

**设置帧动画，绘制进度条**  
 可以通过编写AnimationDrawable文件，设置进度条动画，使用ImagView组件，将src设置为该drawable资源文件。再与java代码配合使用，当需要进度图的时候该动画可见，不需要的时候该动画不可见。

```
<?xml version="1.0" encoding="utf-8"?>  
<animation-list xmlns:android="http://schemas.android.com/apk/res/android"  
    android:oneshot="false" >  
  
    <item  
        android:drawable="@drawable/第一帧的图片"  
        android:duration="200"/>  
    <item  
        android:drawable="@drawable/第二帧的图片"  
        android:duration="200"/>  
    <item  
        android:drawable="@drawable/第三帧的图片（以此类推）"  
        android:duration="200"/>  
  
</animation-list>
```

### SeekBar拖动条

它是是ProgressBar的子类，常用属性：

* `android:max`：滑动条的最大值。
* `android:progress`：滑动条的当前值。
* `android:secondaryProgress`：二级滑动条的进度。
* `android:thumb`：自定义滑块的drawable。

**自定义滑块**  
 在布局文件中使用`android:thumb`设置为该drawable。

```
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_pressed="true" android:drawable="@mipmap/seekbar_thumb_pressed"/>
    <item android:state_pressed="false" android:drawable="@mipmap/seekbar_thumb_normal"/>
</selector>
```

**自定义条形栏**  
 通过编写layer-list资源文件，表示层叠图片。拖动条的层次依次是：背景、二级进度条、当前进度。在布局文件中使用`progressDrawable`设置为该drawable。

```
<?xml version="1.0" encoding="utf-8"?>
<layer-list
    xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:id="@android:id/background">
        <shape>
            <solid android:color="#FFFFD042" />
        </shape>
    </item>
    <item android:id="@android:id/secondaryProgress">
        <clip>
            <shape>
                <solid android:color="#FFFFFFFF" />
            </shape>
        </clip>
    </item>
    <item android:id="@android:id/progress">
        <clip>
            <shape>
                <solid android:color="#FF96E85D" />
            </shape>
        </clip>
    </item>
</layer-list>
```

### RatingBar星级评分条

RatingBar也是ProgressBar的子类。常用属性：

* `android:isIndicator`：是否用作指示，用户无法更改，默认false。
* `android:numStars`：显示多少个星星，必须为整数。
* `android:rating`：默认评分值，必须为浮点数。
* `android:stepSize`： 评分每次增加的值，必须为浮点数。

**自定义效果**  
 编写资源文件layer-list，类似拖动条。可以在布局文件中设置`progressDrawable`属性，但是这里我们写一个style，然后在布局文件中添加这个style。

```
<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:id="@android:id/background"
        android:drawable="@mipmap/ic_rating_off1" />
    <item android:id="@android:id/secondaryProgress"
        android:drawable="@mipmap/ic_rating_off1" />
    <item android:id="@android:id/progress"
        android:drawable="@mipmap/ic_rating_on1" />
</layer-list>
```

```
<style name="roomRatingBar" parent="@android:style/Widget.RatingBar">
        <item name="android:progressDrawable">@drawable/ratingbar_full</item>
        <item name="android:minHeight">24dip</item>
        <item name="android:maxHeight">24dip</item>
    </style>
```

```
<RatingBar
        android:id="@+id/rb_normal"
        style="@style/roomRatingBar"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content" />
```

### ScrollView滚动条

* `android:scrollbarThumbVertical`属性：设置垂直方向的滚动滑块的图片。
* `android:scrollbarThumbHorizontal`属性：设置水平方向的滚动滑块的图片。
* `android:scrollbars="none"`：值为none即隐藏滑块。

### TextClock文本时钟

**注意：API>17**

* `android:format12Hour`：设置12时制的格式。  
   常用格式：  
   ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ad2fa96641d33f8329f9b0f02b01a3ae.png)
* `android:format24Hour`：设置24时制的格式。
* `android:timeZone`：设置时区。

### AnalogClock模拟时钟

* `android:dial="@mipmap/ "`属性：设置表背景图片。
* `android:hand_hour="@mipmap/ "`属性：设置表的时针图片。
* `android:hand_minute="@mipmap/ "`属性：设置表的分针图片。

### Chronometer计时器

我暂时用不到，所以不写了。

### DatePicker日期选择器

* `android:calendarTextColor` ： 日历列表的文本的颜色。
* `android:calendarViewShown`：是否显示日历视图。
* `android:datePickerMode`：组件外观，可选值：spinner，calendar（默认）。
* `android:dayOfWeekBackground`：顶部星期几的背景颜色。
* `android:dayOfWeekTextAppearance`：顶部星期几的文字颜色。
* `android:endYear`：去年(内容)比如2010。
* `android:firstDayOfWeek`：设置日历列表以星期几开头。
* `android:headerBackground`：整个头部的背景颜色。
* `android:headerDayOfMonthTextAppearance`：头部日期字体的颜色。
* `android:headerMonthTextAppearance`：头部月份的字体颜色。
* `android:headerYearTextAppearance`：头部年的字体颜色。
* `android:maxDate`：最大日期显示在这个日历视图mm / dd / yyyy格式。
* `android:minDate`：最小日期显示在这个日历视图mm / dd / yyyy格式。
* `android:spinnersShown`：是否显示spinner。
* `android:startYear`：设置第一年(内容)，比如19940年。
* `android:yearListItemTextAppearance`：列表的文本出现在列表中。
* `android:yearListSelectorColor`：年列表选择的颜色。

### TimePicker时间选择器

* `android:timePickerMode`属性：设置组件外观，可选值为：spinner、clock(默认)。

### CalendarView日历视图

* `android:firstDayOfWeek`：设置一个星期的第一天。
* `android:maxDate`：最大的日期显示在这个日历视图（mm / dd / yyyy格式）。
* `android:minDate`：最小的日期显示在这个日历视图（mm / dd / yyyy格式）。
* `android:weekDayTextAppearance`：工作日的文本出现在日历标题缩写。

### ListView列表

就是一模一样的布局构成的列表，很方便（可以参考微信好友列表、聊天列表等）。需要结合适配器Adapter一起使用。具体的结合方法在java部分学习。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0b9a6482aa0788c862b4360f7ed131d2.png)  
 ListView的常用属性：

* `footerDividersEnabled`：是否在footerView(表尾)前绘制一个分隔条，默认为true。
* `headerDividersEnabled`：是否在headerView(表头)前绘制一个分隔条，默认为true。
* `divider`：设置分隔条，可以用颜色分割，也可以用drawable资源分割。
* `dividerHeight`：设置分隔条的高度。
* `stackFromBottom`：设置值为true使列表从底部开始显示。
* `cacheColorHint`：设置点击颜色。可以将颜色设置为透明:`#00000000`。
* `scrollbars`：设置值为none隐藏滑动条。
* `focusable`：不是为ListView设置的，而是为其中的组件设置的。设置属性值为false，可使组件不获取焦点，点击ListView时整体有效。**注意：EditText除外，它还是可以获取焦点然后立马又失去了焦点，不会弹出小键盘。**
* `descendantFocusability`：在Item布局的根节点添加，该属性有三个可供选择的值。  
   `beforeDescendants`：viewgroup会优先其子类控件而获取到焦点；  
   `afterDescendants`：viewgroup只有当其子类控件不需要获取焦点时才获取焦点；  
   `blocksDescendants`：viewgroup会覆盖子类控件而直接获得焦点。

### GridView网格视图

网格视图和列表类似，只不过是以网格布局，也需要配合Adapter使用。

常用属性：

* `columnWidth`：设置列的宽度。
* `gravity`：组件对齐方式。
* `horizontalSpacing`：水平方向每个单元格的间距。
* `verticalSpacing`：垂直方向每个单元格的间距。
* `numColumns`：设置列数。
* `stretchMode`：设置拉伸模式，可选值如下：  
   `none`：不拉伸；  
   `spacingWidth`：拉伸元素间的间隔空隙；  
   `columnWidth`：仅仅拉伸表格元素自身；  
   `spacingWidthUniform`：既拉元素间距又拉伸他们之间的间隔空隙。

### Spinner列表选项框

常用属性：

* `dropDownHorizontalOffset`：设置列表框的水平偏移距离。
* `dropDownVerticalOffset`：设置列表框的水平竖直距离。
* `dropDownSelector`：列表框被选中时的背景。
* `dropDownWidth`：设置下拉列表框的宽度。
* `gravity`：设置里面组件的对其方式。
* `popupBackground`：设置列表框的背景。
* `prompt`：设置对话框模式的列表框的提示信息（标题）。只能够引用string.xml 中的资源id，而不能直接写字符串。
* `spinnerMode`：列表框的模式，有两个可选值：  
   `dialog`：对话框风格的窗口；  
   `dropdown`：下拉菜单风格的窗口（默认）。
* `entries`：使用数组资源设置下拉列表框的列表项目，值为对应的@array。

### AutoCompleteTextView自动完成文本框

通俗解释一下，就是输第一个字，下面会有提示补全后面的。

常用属性：

* `completionHint`：设置下拉菜单中的提示标题。
* `completionHintView`：定义提示视图中显示下拉菜单。
* `completionThreshold`：指定用户至少输入多少个字符才会显示提示。
* `dropDownAnchor`：设置下拉菜单的定位"锚点"组件，如果没有指定改属性， 将使用该TextView作为定位"锚点"组件。
* `dropDownHeight`：设置下拉菜单的高度。
* `dropDownWidth`：设置下拉菜单的宽度。
* `dropDownHorizontalOffset`：指定下拉菜单与文本之间的水平间距。
* `dropDownVerticalOffset`：指定下拉菜单与文本之间的竖直间距。
* `dropDownSelector`：设置下拉菜单点击效果。
* `popupBackground`：设置下拉菜单的背景。

### MultiAutoCompleteTextView多提示项的自动完成文本框

和自动完成文本框类似，暂时不补充了。

### ExpandableListView可折叠列表

ListView的子类， 在ListView的基础上把应用中的列表项分为几组，每组里又可包含多个列表项，类似于QQ联系人列表。用法与ListView相似，需结合ExpandableAdapter完成。

常用属性：

* `childDivider`：指定各组内子类表项之间的分隔条，图片不会完全显示， 分离子列表项的是一条直线。
* `childIndicator`：显示在子列表旁边的Drawable对象，可以是一个图像。
* `childIndicatorEnd`：子列表项指示符的结束约束位置。
* `childIndicatorLeft`：子列表项指示符的左边约束位置。
* `childIndicatorRight`：子列表项指示符的右边约束位置。
* `childIndicatorStart`：子列表项指示符的开始约束位置。
* `groupIndicator`：显示在组列表旁边的Drawable对象，可以是一个图像。
* `indicatorEnd`：组列表项指示器的结束约束位置。
* `indicatorLeft`：组列表项指示器的左边约束位置。
* `indicatorRight`：组列表项指示器的右边约束位置。
* `indicatorStart`：组列表项指示器的开始约束位置。

### ViewFlipper翻转视图

Android自带的一个多页面管理控件，且可以自动播放。很多时候用来实现进入应用后的引导页，或者用于图片轮播。既可以通过静态导入实现，也可以通过动态导入实现（java部分学习）。

常用属性：

* `inAnimation`：设置View进入屏幕时使用的动画，格式为"@anim/xml文件名"。
* `outAnimation`：设置View退出屏幕时使用的动画，格式为"@anim/xml文件名"。
* `flipInterval`：设置View之间切换的时间间隔，值为数字不加单位（默认单位为ms）。

```
<ViewFlipper
	android:id="@+id/vflp_help"
	android:layout_width="match_parent"
	android:layout_height="match_parent">

	<include layout="@layout/page_help_one" />
	<include layout="@layout/page_help_two" />
	<include layout="@layout/page_help_three" />
	<include layout="@layout/page_help_four" />

</ViewFlipper>
```

**示例：**  
 先写一个进入动画（关于动画的知识目前还不太清楚）：

```
<?xml version="1.0" encoding="utf-8"?>
<set xmlns:android="http://schemas.android.com/apk/res/android">

    <translate
        android:duration="2000"
        android:fromXDelta="100%p"
        android:toXDelta="0" />

</set>
```

再写一个退出动画：

```
<?xml version="1.0" encoding="utf-8"?>
<set xmlns:android="http://schemas.android.com/apk/res/android" >

    <translate
        android:duration="2000"
        android:fromXDelta="0"
        android:toXDelta="-100%p" />

</set>
```

### 自定义View

在xml布局中使用自定义的view时，需要使用"全限定类名"。举个例子，自定义一个按钮MyButton继承Button类：

```
<example.jay.com.mybutton.MyButton  
        android:layout_width="wrap_content"  
        android:layout_height="wrap_content"  
        android:text="按钮"/>
```

资源
--

在XML中，资源的使用通过@xxx即可得到。比如获取文本和图片:

```
<TextView android:text="@string/hello_world" 
	android:layout_width="wrap_content" 
	android:layout_height="wrap_content" 
	android:background = "@drawable/img_back"/>
```

资源文件都保存在res\valuse下。

### string资源文件

```
<string name="hello">Hello world！</string>
```

注意有些特殊字符是不能作为文本字符串直接写进去的，要用转义字符。[XML里特殊字符的输入](https://blog.csdn.net/liuziyuan333183/article/details/104719805)  
 [XML空格符](https://blog.csdn.net/love_000000/article/details/91490655)

### array资源文件

创建一个数组资源文件arrays.xml：

```
<?xml version="1.0" encoding="utf-8"?>  
<resources>  
    <string-array name="myarray">  
    <item>张三</item>  
    <item>李四</item>  
    <item>王五</item>  
    </string-array>      
</resources>
```

### 其他

如果想设置Android不跟随屏幕密度加载不同文件夹的资源,只需在AndroidManifest.xml文件中添加`android:anyDensity="false"`字段即可。

ActivityManifest文件
------------------

```
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="jay.com.example.firstapp" >

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/AppTheme" >
        <activity
            android:name=".MainActivity"
            android:label="@string/app_name" >
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />

                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
```

其中，`<?xml version="1.0" encoding="utf-8"?>`定义了使用xml的版本与编码方式。

### manifest元素

* `xmlns:android`属性：定义我们需要使用的架构。
* `package`属性：Eclipse会在项目创建时将程序所在的java包名称作为manifest元素的属性。例如：`"com.example.myfirstapp"`，该包名是应用的唯一标识。
* `android:versionCode`属性：版本代码，初始值为1。将应用程序提交到Play商店中并进行后续次级版本更新时，需要为每一次更新分配一个更新数字。用户们是无法看到版本代码的，而且新版本的数字必须高于旧版本，不过每一次递增的幅度并不固定。
* `android:versionName`属性：版本名称，初始值为1.0。版本名称是用户们在Play商店中所看到的应用程序的实际名称，可以随意使用自己喜欢的数字来表示。

### Uses-SDK元素

* `android:versionCode`：定义程序的版本号
* `android:versionName`：定义程序的版本名称
* `android:minSdkVersion`属性：最低必要API级别。
* `android:targetSdkVersion`属性：在测试项目时所设定的目标API级别。

在创建应用程序时就需要选择这些相关值，也可以在项目创建完成后，通过修改Manifest文件内容进行属性变更。如果改变了SDK版本，Eclipse会重新建立整个项目。

如果用户设备所运行的API级别低于项目的最低要求，则无法下载并安装应用程序。列出目标API级别代表着已经对当前应用版本进行过测试。为保证应用产品的可靠性，应该在尽可能多的API级别之下进行应用程序测试。

### Application元素

* `android:allowBackup`属性：是否允许备份文件。值为true表示允许。
* `android:icon`属性：图标，代表应用可绘制资源中的某个文件。在默认情况下项目会直接使用Android图标。例如：`"@drawable/ic_launcher"`
* `android:label`属性：标签，引用来自应用程序资源的字符串。
* `android:theme`属性：主题，引用一种资源。例如：`"@style/AppTheme"`

### 四大组件

Android应用程序当中包含四大组件：Activity、Service、Content Provider以及Broadcast Receiver。**只要创建或者使用其中的任何一种，就必须将对应元素添加到项目Manifest当中。** 语法为：`Server：元素类型`

#### 1.activity元素

每一次向应用程序中添加新的Activity类时，都需要在application元素中添加一个对应activity子元素。例如，添加名称为“About”的Activity类（无需使用完整的应用包名称）：

```
<activity
	android:icon="图标"
	android:name=".About"
	android:label="Activity显示的标题"
	android:theme="要应用的主题" >
</activity>
```

**常用属性：**

* `android:name`属性：声明一个activity，利用应用程序包中所限定的路径引用对应类。例如：`"com.example.myfirstapp.MainActivity"`，前面部分可以用.表示
* `android:label`属性：标签，控制Activity启用时、窗口标题中的显示内容，是显示给用户看的。默认情况下，窗口标题往往就是应用程序名称。例如：`"@string/app_name"`
* `android:persistableMode="persistAcrossReboots"`：写上就行，是为了消灭onCreate方法中的一个参数，使Activity持久化。持久化就是拥有了系统关机后重启的数据恢复能力，而且不影响其他的序列化操作（API版本需要>=21，即5.0以上）
* `android:screenOrientation`：禁止屏幕横竖屏自动切换，有以下可选值：  
   `unspecified`：默认值，由系统来判断显示方向（判定策略与设备系统有关）。  
   `landscape`：横屏显示（宽比高要长）。  
   `portrait`：竖屏显示(高比宽要长)。  
   `user`：用户当前首选的方向。  
   `behind`：和Activity堆栈中的该Activity下面的那个Activity的方向一致。  
   `sensor`：有物理的感应器来决定，如果用户旋转设备屏幕会横竖屏切换。  
   `nosensor`：忽略物理感应器，这样就不会随着用户旋转设备而更改了（"unspecified"设置除外）。
* `android:theme = @android:style/Theme.NoTitleBar.FullScreen`：设置Activity需要全屏（我自己试过，不会用）。

##### intent-filter子元素

**intent-filter元素（意图过滤器）：** 在主activity元素当中，用于描述主activity能够响应哪些“意图”。Android系统中，所谓意图是指在Activity启动时向其传递的数据对象。当大家在自己的应用程序中启用一个又一个Activity时，就需要使用到意图机制了——不过意图也可以在不同应用之间进行传递。

```
<intent-filter>
    <action android:name="android.intent.action.MAIN" />
    <category android:name="android.intent.category.LAUNCHER" />
</intent-filter>
```

* action元素：意图是通过action元素实现这一效果的，也就是上述代码中的“MAIN”操作。action指动作，MAIN表示这是软件打开的第一个activity，还有其他的值这里暂时不说了。
* category元素：通过分类名称描述意图过滤器。LAUNCHER可以理解为创建一个桌面图标，同样还有其他的值暂时不说了。

这两种元素相结合表示我们的应用程序应该利用本Activity作为其主入口点，而且该入口点将在应用程序运行时一并启动。app会被显示在Home的应用程序列表中。

##### metadata子元素

其作用是定义一个数据条目的名值对。

#### 2.Service元素

在Android系统当中，一项Service就相当于一个后台进程。Service通常被用于那些正在进行或者需要持续很长一段时间的进程。

事实上Service并不具备用户界面，因此它们通常需要与其它组件结合起来以实现功效，例如与Activity联手。最典型的例子就是，在应用程序当中Activity会在用户操作的同时启动一项Service，这项Service也许会将数据上传至Web资源当中。用户可以继续与该Activity进行交互，但与此同时Service的运作却不受影响——因为它的执行一直在后台完成。如果以Activity为起点启动一项Service，而用户又通过导航从该Activity切换到了其它应用程序处，那么该Service仍将继续运行。

其它应用程序组件可以与Service绑定，并向其请求并接收数据。如果一项绑定Service正处于运行当中，那么所有与之相绑定的组件停止之后它也将同时进入停止状态。

#### 3.Content Provider元素

Content Provider用于管理数据集。这里指的数据集既可以单纯归属于本应用程序，也可以与其它应用所共享、能够对数据进行查询及修改。

通常是利用Content Resolver类来实现与数据的交互。数据会被Content Provider提交给一系列包含行与列的表格，其中每行（或者每条记录）中的列都包含一个单独的数据值。

#### 4.Broadcast Receiver元素

接收来自Android系统的广播通知，例如电池电量、屏幕关闭以及充电器是否接入插座等等。  
 Android系统将广播通知称为intent，它能够被用于启动Activity。intent-filter，用于指示我们想要接收的操作，例如：

```
<receiver android:name=".YourReceiver">
<intent-filter>
<action android:name="android.intent.action.BATTERY_LOW" />
</intent-filter>
</receiver>
```

此例中Broadcast Receiver能够接收“battery low（电池电量低）”这一intent。

#### 5.Fragment元素

fragment可以将自己的用户界面拆分为逻辑部分，甚至在应用程序的多个屏幕之间重复使用同样的部分。

#### 6.Action Bar

action bar的作用在于为我们的应用程序提供足以作用于整套Android系统的用户界面。一般来说，action bar当中所显示的条目包括用户在应用程序当中所处的位置以及应用程序各个部分之间的导航系统。

要在Activity当中使用action bar，需要保证自己的类当中包含ActionBarActivity类，并在Manifest当中将AppCompat主题应用在该Activity当中。

### uses-permission元素

用于罗列应用所要求的权限——用户会在安装应用之前观看到该列表。权限中包含多种操作条目，例如通过互联网获取数据、写入存储或者访问设备上的其它功能——如相机。如果用户选择继续，则需要接受权限控制提示，而后应用才能正常运行。 在Manifest当中必须强制要求的权限包括使用内部数据、写入外部存储以及访问摄像头等设备功能。例如：

```
<uses-permission android:name="android.permission.INTERNET" />
```

### uses-configuration元素

用于描述应用程序运行所必需的硬件及软件功能，可以为导航、键盘以及触摸屏选项指定相关要求。

### uses-feature元素

可以通过功能名称与布尔标记列举关于硬件或者软件的单一功能要求。这些功能包括蓝牙与摄像头选项，例如闪存、位置检测以及传感器。

### supports-screens元素

则允许大家为应用程序定义所支持的屏幕尺寸，所指定的元素可同时涉及尺寸与像素密度。

### service元素

应用程序通常会利用Android系统中的Service类来处理后台进程，这就要求在Manifest当中添加service元素——与Activity类似，service元素与Service类之间一一对应。

### provider元素

Android应用中的内容提供器负责管理对数据源的访问，具体内容被列入provider元素当中。

### receiver

Manifest中的receiver元素旨在帮助应用接收来自其它应用或者操作系统本身的意图。

---

 【未完待续】