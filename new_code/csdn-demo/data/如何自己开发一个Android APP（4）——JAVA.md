# 如何自己开发一个Android APP（4）——JAVA

资源使用
----

在java文件中，通过资源id完成对资源的访问。可以通过`对象.getId()`的方法得到组件。

因为XML布局文件与java文件实际上是不互通的，也就是说我们的xml只控制外观，当你需要为某个地方作出某些设置时，java必须先获取到这个组件。

* 文字：`txtName.setText(getResources().getText(R.string.name));`
* 图片：`imgIcon.setBackgroundDrawableResource(R.drawable.icon);`
* 颜色：`txtName.setTextColor(getResouces().getColor(R.color.red));`
* 布局：`setContentView(R.layout.main);`
* 控件：`txtName = (TextView)findViewById(R.id.txt_name);`

### 资源文件

如何启动资源文件：

```
ImageView.postDelayed(new Runnable() {
    @Override
    public void run()
    {
        AnimationDrawable.start();
    }
}, 100);
```

外观（动态设置XML）
-----------

**在java中，任何xml里面系统规定的资源文件、组件都是一个类，都可以用对象声明的方法。**

设置weight属性：

```
setLayoutParams(new LayoutParams(LayoutParams.FILL_PARENT,     
        LayoutParams.WRAP_CONTENT, 1));
```

**我们注意到，常用的XML属性都对应着java文件的某个set方法。所以如果本文有遗漏，可以尝试自己用某种set方法。**

### 对TextView的操作

* 修改drawable图片的大小。在Activity中，声明一个TextView变量如txt\_name，在onCreate方法中：

```
txtName = (TextView) findViewById(R.id.txt_name);
Drawable[] drawable = txtName.getCompoundDrawables();
// 获得四个不同方向上的图片资源，数组下标0~3，依次是：左、上、右、下。

drawable[1].setBounds(100, 0, 200, 300);
// 获得资源后，设置图片坐标点。以上方的图片为例，四个参数的含义分别为长宽的起止。
// 本例中，图片长度为离文字最左边起100dp处至200dp处，宽为从文字上方0dp处往上延伸至200dp处。

txtName.setCompoundDrawables(drawable[0], drawable[1], drawable[2], drawable[3]);  
// 为TextView重新设置四个方向的图片（若没有图片可用null）。
```

* 设置autoLink。TextView通过调用`setAutoLinkMask(Linkify.ALL);`和`setMovementMethod(LinkMovementMethod.getInstance());`超链接方法设置autoLink全部识别。
* 利用HTML代码实现功能。在已有XML的TextView布局上，添加HTML语法字符串，调用`Html.fromHtml()`方法将字符串转换为CharSequence接口。  
   **此功能支持的常见标签有**：`<font>`设置颜色和字体、`<big>`设置字体大号、`<small>`设置字体小号、`<i><b>`斜体粗体、`<a>`连接网址、`<img>`图片。

```
TextView t1 = (TextView)findViewById(R.id.txtOne);

// 超链接
String s1 = "<font color='blue'><b>百度一下，你就知道~：</b></font><br>";
s1 += "<a href = 'http://www.baidu.com'>百度</a>";
t1.setText(Html.fromHtml(s1));
t1.setMovementMethod(LinkMovementMethod.getInstance()); // 超链接需要用到的设置

// 插入图片
String s2 = "图片：<img src = 'icon'/><br>";
t1.setText(Html.fromHtml(s2, new Html.ImageGetter() 
{
	@Override
    public Drawable getDrawable(String source)
    {
    	Drawable draw = null;
        try
        {
        	Field field = R.drawable.class.getField(source);
            int resourceId = Integer.parseInt(field.get(null).toString());
            draw = getResources().getDrawable(resourceId);
            draw.setBounds(0, 0, draw.getIntrinsicWidth(), draw.getIntrinsicHeight());
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
        return draw;
    }
}, null));
```

* 利用SpannableString和SpannableStringBuilder设置文本样式。区别在于，SpannableString是针对不可变文本定值TextView的样式，可以理解为字符串常量；SpannableStringBuilder针对可变文本，在用户使用过程中动态可变的（例如朋友圈点赞列表）。

```
TextView t1 = (TextView) findViewById(R.id.txtOne);

SpannableString span = new SpannableString("红色超链接斜体删除线下划线图片:.");

// 使用setSpan方法，参数列表中包括指定起止位置（左闭右开）、Spanned.SPAN_EXCLUSIVE_EXCLUSIVE表示前后都不包括。

//ForegroundColorSpan：设置文本颜色（前景色）
span.setSpan(new ForegroundColorSpan(Color.RED), 0, 2, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);

// URLSpan：用超链接标记文本
span.setSpan(new URLSpan("tel:4155551212"), 2, 5, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);

// StyleSpan：字体样式，如粗体、斜体等
span.setSpan(new StyleSpan(Typeface.BOLD_ITALIC), 5, 7, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);

// StrikethroughSpan：删除线
span.setSpan(new StrikethroughSpan(), 7, 10, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);

// UnderlineSpan：下划线
span.setSpan(new UnderlineSpan(), 10, 13, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);

// ImageSpan：用图片替换文本
Drawable d = getResources().getDrawable(R.drawable.icon); // 获取Drawable资源
d.setBounds(0, 0, d.getIntrinsicWidth(), d.getIntrinsicHeight()); // 设置图片边界
ImageSpan imgspan = new ImageSpan(d, ImageSpan.ALIGN_BASELINE); // 设置对齐方式
span.setSpan(imgspan, 18, 19, Spannable.SPAN_INCLUSIVE_EXCLUSIVE);

t1.setText(span);

/* 其他：
BackgroundColorSpan：背景色
ClickableSpan：文本可点击，有点击事件
MaskFilterSpan：修饰效果，如模糊(BlurMaskFilter)、浮雕(EmbossMaskFilter)
RasterizerSpan：光栅效果
SuggestionSpan：相当于占位符
AbsoluteSizeSpan：绝对大小（文本字体）
DynamicDrawableSpan：设置图片，基于文本基线或底部对齐。
RelativeSizeSpan：相对大小（文本字体）
ScaleXSpan：基于x轴缩放
SubscriptSpan：下标（数学公式会用到）
SuperscriptSpan：上标（数学公式会用到）
TextAppearanceSpan：文本外貌（包括字体、大小、样式和颜色）
TypefaceSpan：文本字体
*/
```

* 设置文本段落格式。`setScaleX()`设置字间距，如`setScaleX(2.0f);` 。`setLineSpacing()`设置行间距。

### 对EditText的操作

* 让EditText获得焦点与清除焦点

```
edit.requestFocus(); //请求获取焦点
edit.clearFocus(); //清除焦点
```

* 控制光标位置  
   `setSelection()`。该方法有两种类型，一个参数的是设置光标位置的，两个参数的是设置起始位置与结束位置的中间括的部分，即部分选中。  
   `setSelectAllOnFocus(true);`让EditText获得焦点时选中全部文本。  
   `setCursorVisible(false);`设置光标不显示。  
   `getSelectionStart()`和`getSelectionEnd()`获得当前光标的前后位置。

### 对ImagView的操作

* 前景(对应src属性):`setImageDrawable( );`
* 背景(对应background属性):`setBackgroundDrawable( );`
* 设置图片缩放的移动方式：`setScaleType(ImageView.ScaleType.CENTER);`

动态加载图像时固定大小：

```
LinearLayout.LayoutParams layoutParam = new LinearLayout.LayoutParams(48, 48);    
layout.addView(组件名, layoutParam);
```

动态调用Bitmap资源文件的方法：

```
组件名.setBacklgroundResource(R.drawable.文件名);
```

```
img_pgbar = (ImageView) findViewById(R.id.img_pgbar);
        ad = (AnimationDrawable) img_pgbar.getDrawable();
        img_pgbar.postDelayed(new Runnable() {
            @Override
            public void run() {
                ad.start();
            }
        }, 100);
```

### 对RadioButton的操作

* `RadioGroup.getChildCount()`：获取按钮组中的单选按钮的数目。
* `(RadioButton) radgroup.getChildAt(i)`：获取第i个单选钮对象。
* `RadioButton.isChecked()`：返回该单选钮是否被选中。
* `RadioButton.getText()`：返回该单选钮的文字。
* `RadioButton.setPadding(rb_paddingLeft, 0, 0, 0)`：设置padding。
* `getResources().getDrawable(R.mipmap.checkbox图片名字).getIntrinsicWidth()`：获取现有padding，返回值为int。

### 对ProgressBar的操作

* `getMax()`：返回这个进度条的范围的上限。
* `getProgress()`：返回进度。
* `getSecondaryProgress()`：返回次要进度。
* `incrementProgressBy(int diff)`：指定增加的进度。
* `isIndeterminate()`：指示进度条是否在不确定模式下。
* `setIndeterminate(boolean indeterminate)`：设置不确定模式下。

**自定义圆形进度条**  
 通过自定义java类（继承View）的方法，自定义圆形进度条。

```
public class CirclePgBar extends View {


    private Paint mBackPaint;
    private Paint mFrontPaint;
    private Paint mTextPaint;
    private float mStrokeWidth = 50;
    private float mHalfStrokeWidth = mStrokeWidth / 2;
    private float mRadius = 200;
    private RectF mRect;
    private int mProgress = 0;
    //目标值，想改多少就改多少
    private int mTargetProgress = 90;
    private int mMax = 100;
    private int mWidth;
    private int mHeight;


    public CirclePgBar(Context context) {
        super(context);
        init();
    }

    public CirclePgBar(Context context, AttributeSet attrs) {
        super(context, attrs);
        init();
    }

    public CirclePgBar(Context context, AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
        init();
    }


    //完成相关参数初始化
    private void init() {
        mBackPaint = new Paint();
        mBackPaint.setColor(Color.WHITE);
        mBackPaint.setAntiAlias(true);
        mBackPaint.setStyle(Paint.Style.STROKE);
        mBackPaint.setStrokeWidth(mStrokeWidth);

        mFrontPaint = new Paint();
        mFrontPaint.setColor(Color.GREEN);
        mFrontPaint.setAntiAlias(true);
        mFrontPaint.setStyle(Paint.Style.STROKE);
        mFrontPaint.setStrokeWidth(mStrokeWidth);


        mTextPaint = new Paint();
        mTextPaint.setColor(Color.GREEN);
        mTextPaint.setAntiAlias(true);
        mTextPaint.setTextSize(80);
        mTextPaint.setTextAlign(Paint.Align.CENTER);
    }


    //重写测量大小的onMeasure方法和绘制View的核心方法onDraw()
    @Override
    protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
        super.onMeasure(widthMeasureSpec, heightMeasureSpec);
        mWidth = getRealSize(widthMeasureSpec);
        mHeight = getRealSize(heightMeasureSpec);
        setMeasuredDimension(mWidth, mHeight);

    }


    @Override
    protected void onDraw(Canvas canvas) {
        initRect();
        float angle = mProgress / (float) mMax * 360;
        canvas.drawCircle(mWidth / 2, mHeight / 2, mRadius, mBackPaint);
        canvas.drawArc(mRect, -90, angle, false, mFrontPaint);
        canvas.drawText(mProgress + "%", mWidth / 2 + mHalfStrokeWidth, mHeight / 2 + mHalfStrokeWidth, mTextPaint);
        if (mProgress < mTargetProgress) {
            mProgress += 1;
            invalidate();
        }

    }

    public int getRealSize(int measureSpec) {
        int result = 1;
        int mode = MeasureSpec.getMode(measureSpec);
        int size = MeasureSpec.getSize(measureSpec);

        if (mode == MeasureSpec.AT_MOST || mode == MeasureSpec.UNSPECIFIED) {
            //自己计算
            result = (int) (mRadius * 2 + mStrokeWidth);
        } else {
            result = size;
        }

        return result;
    }

    private void initRect() {
        if (mRect == null) {
            mRect = new RectF();
            int viewSize = (int) (mRadius * 2);
            int left = (mWidth - viewSize) / 2;
            int top = (mHeight - viewSize) / 2;
            int right = left + viewSize;
            int bottom = top + viewSize;
            mRect.set(left, top, right, bottom);
        }
    }


}
```

### 对ScrollView的操作

* `ScrollView.fullScroll(ScrollView.FOCUS_DOWN);`滚动到底部。
* `ScrollView.fullScroll(ScrollView.FOCUS_UP);`滚动到顶部。
* `View.scrollTo(x, y);`参数依次为x，y滚到对应的x，y位置。
* `scrollview.setVerticalScrollBarEnabled(false);`设置隐藏滑块。

**设置滚动速度**  
 通过自己编写一个类，继承ScrollView，然后重写其中的 public void fling (int velocityY)的方法，如：

```
@Override
public void fling(int velocityY)
{
    super.fling(velocityY / 2);    //速度变为原来的一半
}
```

### 对TextClock的操作

* `is24HourModeEnabled()`方法查看系统是否在使用24进制时间显示。
* `setFormat12Hour(CharSequence)`设置12时制的格式。
* `setFormat24Hour(CharSequence)`设置24时制的格式。
* `setTimeZone(String)`设置时区。

### 对DatePicker的操作

获得日期的方法：

```
Calendar calendar = Calendar.getInstance();
int year=calendar.get(Calendar.YEAR);
int monthOfYear=calendar.get(Calendar.MONTH);
int dayOfMonth=calendar.get(Calendar.DAY_OF_MONTH);
```

### 对ListView的操作

**ListView的表头和表尾：**  
 注意：添加表头表尾后，positon是从表头开始算的，即添加的第一个数据本来的 postion 是0，但是此时却变成了1。

* `addHeaderView(View v)`：添加headView(表头)，括号中的参数是一个View对象。
* `addFooterView(View v)`：添加footerView(表尾)，括号中的参数是一个View对象。
* `addHeaderView(headView, null, false)`：添加表头，设置Header是否可以被选中。**这个方法必须放在listview.setAdapter前面，否则会报错。**
* `addFooterView(View,view,false)`：添加表尾，设置Footer是否可以被选中。

举个例子，如下图：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6b0e902da09dc5b1951f9a8fd43644c2.png)  
 要实现表头表尾的添加，我们需要在java代码里绑定列表和表头表尾，先写好xml布局文件，然后作为表头和表尾的格式。感觉过程很繁琐，为什么已经写好了布局文件，还要和列表捆绑在一起呢？直接上下放置不行吗？或许是因为更灵活更方便吧，这样列表长度更改时，表头表尾的位置也灵活移动了。  
 表头和表尾的xml文件按照上面的样子写好了之后，java代码：

```
public class MainActivity extends AppCompatActivity implements AdapterView.OnItemClickListener
{

    private List<Animal> mData = null;
    private Context mContext;
    private AnimalAdapter mAdapter = null;
    private ListView list_animal;
    private LinearLayout ly_content;

    @Override
    protected void onCreate(Bundle savedInstanceState) 
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        mContext = MainActivity.this;
        list_animal = (ListView) findViewById(R.id.list_animal);
        
        //这里用LayoutInflater就可以获取xml布局文件
        final LayoutInflater inflater = LayoutInflater.from(this);
        View headView = inflater.inflate(R.layout.view_header, null, false);
        View footView = inflater.inflate(R.layout.view_footer, null, false);
        /* LayoutInflater的使用
        我们需要先获得布局文件，然后获得view，利用findViewById设置view中各组件
        LayoutInflater inflater = getLayoutInflater();
    	View view = inflater.inflate(R.layout.view_toast_custom,
            (ViewGroup) findViewById(R.id.lly_toast));
    	ImageView img_logo = (ImageView) view.findViewById(R.id.img_logo);
    	TextView tv_msg = (TextView) view.findViewById(R.id.tv_msg);
		*/

		//添加数据到List
        mData = new LinkedList<Animal>();
        mData.add(new Animal("狗说", "你是狗么?", R.mipmap.ic_icon_dog));
        mData.add(new Animal("牛说", "你是牛么?", R.mipmap.ic_icon_cow));
        mData.add(new Animal("鸭说", "你是鸭么?", R.mipmap.ic_icon_duck));
        mData.add(new Animal("鱼说", "你是鱼么?", R.mipmap.ic_icon_fish));
        mData.add(new Animal("马说", "你是马么?", R.mipmap.ic_icon_horse));
        mAdapter = new AnimalAdapter((LinkedList<Animal>) mData, mContext);
        
        //添加表头和表尾需要写在setAdapter方法调用之前（因为要将所有UI布局设置好之后，再统一建立接口
        list_animal.addHeaderView(headView);
        list_animal.addFooterView(footView);

        list_animal.setAdapter(mAdapter);
    }
}
```

**ListView的item焦点问题：**  
 由于ListView中组件太多，item点击不了，触发不了对应的onItemClick的方法，也触发不了onItemLongClick方法，即ListView的焦点被其他控件抢了。  
 可以在代码中获得控件后调用：`setFocusable(false)`。

**列表无内容时的布局**  
 使用`setEmptyView(View)`方法，可以设置当ListView中没有任何内容时显示的布局。  
 除此之外，还有一种方法：写好一个布局，然后设置其， `android:visibility="gone"`，在Java代码中对数据集合的size进行判断，根据是否等于零改变此布局的可见性。

**动态刷新，改变列表内容**

**1. 添加内容**  
 举个例子，有一个“添加”按钮，点击之后就能在列表里添加一行。下面给出在指定第五行添加数据的例子（可以不写位置，默认添加在最后）：

在Adapter类里写一个方法：

```
public void add(int position,Data data)
{
    if (mData == null)
    {
        mData = new LinkedList<>();
    }
    mData.add(position,data); //添加数据
    notifyDataSetChanged(); //刷新，系统会自动判断是否需要全部重绘，否则只重绘修改了的部分
}
```

“添加”按钮的相关设置：

```
private Button btn_add;
btn_add = (Button) findViewById(R.id.btn_add2);
btn_add.setOnClickListener(this);

@Override
public void onClick(View v)
{
    switch (v.getId())
    {
        case R.id.btn_add:
            mAdapter.add(4，new Data(R.mipmap.ic_icon_qitao, "这是第" + flag + "条数据"));
            //指定第五行，但是position是从0开始的，所以position=4
            flag++;
            break;
    }
}
```

**2. 删除内容**

```
// 指定数据删除
public void remove(Data data)
{
    if(mData != null)
    {
        mData.remove(data);
    }
    notifyDataSetChanged();
}
// 指定位置删除
public void remove(int position)
{
    if(mData != null)
    {
        mData.remove(position);
    }
    notifyDataSetChanged();
}
// 添加两个按钮分别调用两种方法
case R.id.btn_remove1:
    mAdapter.remove(mData_5);
    break;
case R.id.btn_remove2:
    mAdapter.remove(2);
    break;
```

**3. 移除所有记录**

```
public void clear()
{
    if(mData != null)
    {
        mData.clear();
    }
    notifyDataSetChanged();
}
```

### 对GridView的操作

我暂时用不到，不写了

### 对Spinner的操作

Spinner会默认选中第一个值，即默认调用`spinner.setSection(0)`，也可以设置默认的选中值。

注意：由于Spinner有默认值，会触发一次`OnItemSelectedListener`事件。可以通过以下方法判断是自动触发还是手动选择：添加一个boolean值，然后设置为false，在onItemSelected时进行判断，false说明是默认触发的，不做任何操作，将boolean值设置为true；true的话则正常触发事件。

Spinner同样也是一般和Adapter结合使用，只是存放数组则可以不用。例子暂时省略了。

### 对AutoCompleteTextView的操作

我暂时用不到！

### 对ExpandableListView的操作

需要重写BaseExpandableListAdpter。我暂时也用不到！因为时间不够，我马上要交作业了，所以我不能研究这么多……

### 对ViewFlipper的操作

无论是静态设置还是动态设置，都需要在java文件中使用`ViewFlipper.startFlipping()`方法执行。

动态设置通过`addView`方法填充View。如图：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/988d55e0d115547e4e46a4aae3182bf1.png)  
 还有一些常用方法：

* `setInAnimation`：设置View进入屏幕时使用的动画。
* `setOutAnimation`：设置View退出屏幕时使用的动画。
* `showNext`：调用该方法来显示ViewFlipper里的下一个View。
* `showPrevious`：调用该方法来显示ViewFlipper的上一个View。
* `setFilpInterval`：设置View之间切换的时间间隔。
* `setFlipping`：使用上面设置的时间间隔来开始切换所有的View，切换会循环进行。
* `stopFlipping`：停止View切换。

除了自动播放之外，还可以设置手势滑动。这里暂时不写了……

使用过程中的提示信息
----------

### Toast吐司

Toast是一种很方便的消息提示框，没任何按钮，也不会获得焦点，一段时间过后自动消失。

**用法举例：**

* `Toast.makeText(MainActivity.this, "提示的内容", Toast.LENGTH_LONG).show();`  
   参数列表中，第一个是上下文对象；第二个是显示的内容；第三个是显示的时间，只有LONG和SHORT两种。
* 设置显示位置：`toast.setGravity(Gravity.CENTER_VERTICAL|Gravity.CENTER_HORIZONTAL , 0, 0);`
* 设置字体颜色：  
   `TextView v = (TextView) toast.getView().findViewById(android.R.id.message);`  
   `v.setTextColor(Color.YELLOW);`   
   其中toast是实例化的java对象哦！
* 带图片的设置：  
   `LinearLayout layout = (LinearLayout) toast.getView();`  
   `layout.setBackgroundColor(Color.BLUE);`  
   `ImageView image = new ImageView(this);`  
   `image.setImageResource(R.mipmap.ic_icon_photo);`  
   `layout.addView(image, 0);`
* 给toast实现更多自定义的布局：`toast.setView(view);`其中view是实例化的view对象。
* `toast.show()`：用于显示toast，必须调用。

### Notification状态栏通知

我暂时用不到，不写了。

### AlertDialog对话框

**使用步骤：**

1. 创建AlertDialog.Builder对象：  
    `private AlertDialog.Builder builder = new AlertDialog.Builder(mContext);`
2. 创建AlertDialog对象：`private AlertDialog alert = null;`
3. 利用Builder的方法为alert初始化。调用`setIcon()`设置图标；`setTitle()`或`setCustomTitle()`设置标题；`setMessage()`设置对话框的内容；`setPositiveButton()`、`setNegativeButton()`、`setNeutralButton()`分别设置确定、取消、中立按钮；再调用`create()`方法创建这个对象。
4. `alert.show();`显示对话框。

```
public class MainActivity extends AppCompatActivity implements View.OnClickListener
{
	// 用四个按钮分别演示四种对话框
    private Button btn_dialog_one;
    private Button btn_dialog_two;
    private Button btn_dialog_three;
    private Button btn_dialog_four;

    private Context mContext;
    private boolean[] checkItems;

    private AlertDialog alert = null;
    private AlertDialog.Builder builder = null;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        mContext = MainActivity.this;
        bindView();
    }

    private void bindView()
    {
        btn_dialog_one = (Button) findViewById(R.id.btn_dialog_one);
        btn_dialog_two = (Button) findViewById(R.id.btn_dialog_two);
        btn_dialog_three = (Button) findViewById(R.id.btn_dialog_three);
        btn_dialog_four = (Button) findViewById(R.id.btn_dialog_four);
        btn_dialog_one.setOnClickListener(this);
        btn_dialog_two.setOnClickListener(this);
        btn_dialog_three.setOnClickListener(this);
        btn_dialog_four.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) 
    {
        switch (v.getId()) 
        {
            //普通对话框
            case R.id.btn_dialog_one:
                alert = null;
                builder = new AlertDialog.Builder(mContext);
                alert = builder.setIcon(R.mipmap.ic_icon_fish)
                        .setTitle("系统提示：")
                        .setMessage("这是一个最普通的AlertDialog")
                        .setNegativeButton("取消", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) 
                            {
                                Toast.makeText(mContext, "你点击了取消按钮~", Toast.LENGTH_SHORT).show();
                            }
                        })
                        .setPositiveButton("确定", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) 
                            {
                                Toast.makeText(mContext, "你点击了确定按钮~", Toast.LENGTH_SHORT).show();
                            }
                        }).create();
                alert.show();
                break;
                
            //普通列表对话框
            case R.id.btn_dialog_two:
                final String[] lesson = new String[]{"语文", "数学", "英语", "化学", "生物", "物理", "体育"};
                alert = null;
                builder = new AlertDialog.Builder(mContext);
                alert = builder.setIcon(R.mipmap.ic_icon_fish)
                        .setTitle("选择你喜欢的课程")
                        .setItems(lesson, new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) 
                            {
                                Toast.makeText(getApplicationContext(), "你选择了" + lesson[which], Toast.LENGTH_SHORT).show();
                            }
                        }).create();
                alert.show();
                break;
                
            //单选列表对话框
            case R.id.btn_dialog_three:
                final String[] fruits = new String[]{"苹果", "雪梨", "香蕉", "葡萄", "西瓜"};
                alert = null;
                builder = new AlertDialog.Builder(mContext);
                alert = builder.setIcon(R.mipmap.ic_icon_fish)
                        .setTitle("选择你喜欢的水果")
                        .setSingleChoiceItems(fruits, 0, new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) 
                            {
                                Toast.makeText(getApplicationContext(), "你选择了" + fruits[which], Toast.LENGTH_SHORT).show();
                            }
                        }).create();
                alert.show();
                break;
                
            //多选列表对话框
            case R.id.btn_dialog_four:
                final String[] menu = new String[]{"红色", "黄色", "黑色", "橙色"};
                //定义一个用来记录个列表项状态的boolean数组
                checkItems = new boolean[]{false, false, false, false};
                alert = null;
                builder = new AlertDialog.Builder(mContext);
                alert = builder.setIcon(R.mipmap.ic_icon_fish)
                        .setMultiChoiceItems(menu, checkItems, new DialogInterface.OnMultiChoiceClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which, boolean isChecked) 
                            {
                                checkItems[which] = isChecked;
                            }
                        })
                        .setPositiveButton("确定", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) 
                            {
                                String result = "";
                                for (int i = 0; i < checkItems.length; i++) 
                                {
                                    if (checkItems[i])
                                        result += menu[i] + " ";
                                }
                                Toast.makeText(getApplicationContext(), "你选择的颜色:" + result, Toast.LENGTH_SHORT).show();
                            }
                        }).create();
                alert.show();
                break;
        }
    }
}
```

点击对话框的外部区域，对话框就会消失。通过为builder设置`setCancelable(false)`即可解决这个问题。

**自定义对话框中的view**

```
private View view_custom;

final LayoutInflater inflater = MainActivity.this.getLayoutInflater();
view_custom = inflater.inflate(R.layout.view_dialog_custom, null,false);
builder.setView(view_custom);
```

#### ProgressDialog进度条对话框

使用方法有两种：

1. 直接调用ProgressDialog提供的静态方法show()显示。
2. 创建ProgressDialog对象，再设置对话框的参数，最后show()出来。

```
public class MainActivity extends AppCompatActivity implements View.OnClickListener{

	// 三个按钮点击后分别弹出圆形进度条、不带进度的条形进度条、带进度的条形进度条
    private Button btn_one;
    private Button btn_two;
    private Button btn_three;
    
    private ProgressDialog pd1 = null;
    private ProgressDialog pd2 = null;
    private final static int MAXVALUE = 100;
    private int progressStart = 0;
    private int add = 0;
    private Context mContext = null;


    //定义一个用于更新进度的Handler,因为只能由主线程更新界面,所以要用Handler传递信息
    final Handler hand = new Handler()
    {
        @Override
        public void handleMessage(Message msg)
        {
            //如果接受到信息码是123
            if(msg.what == 123)
            {
                //设置进度条的当前值
                pd2.setProgress(progressStart);
            }
            //如果当前大于或等于进度条的最大值，调用dismiss()方法关闭对话框
            if(progressStart >= MAXVALUE)
            {
                pd2.dismiss();
            }
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        mContext = MainActivity.this;
        bindViews();
    }

    private void bindViews()
    {
        btn_one = (Button) findViewById(R.id.btn_one);
        btn_two = (Button) findViewById(R.id.btn_two);
        btn_three = (Button) findViewById(R.id.btn_three);
        btn_one.setOnClickListener(this);
        btn_two.setOnClickListener(this);
        btn_three.setOnClickListener(this);
    }


    @Override
    public void onClick(View v)
    {
        switch (v.getId())
        {
            case R.id.btn_one:
                // 参数依次为：上下文、标题、内容,是否显示进度,是否可以用取消按钮关闭
                ProgressDialog.show(MainActivity.this, "资源加载中", "资源加载中,请稍后...",false,true);
                break;
            
            case R.id.btn_two:
                pd1 = new ProgressDialog(mContext);
                // 依次设置标题、内容、是否用取消按钮关闭
                pd1.setTitle("软件更新中");
                pd1.setMessage("软件正在更新中,请稍后...");
                pd1.setCancelable(true);
                // 设置进度条的风格，HORIZONTAL是水平进度条，SPINNER是圆形进度条
                pd1.setProgressStyle(ProgressDialog.STYLE_HORIZONTAL);
                // 设置是否隐藏进度
                pd1.setIndeterminate(true);
                // 调用show()方法将ProgressDialog显示出来
                pd1.show();
                break;
                
            case R.id.btn_three:
                // 初始化属性
                progressStart = 0;
                add = 0;
                // 依次设置一些属性
                pd2 = new ProgressDialog(MainActivity.this);
                pd2.setMax(MAXVALUE);
                pd2.setTitle("文件读取中");
                pd2.setMessage("文件加载中,请稍后...");
                pd2.setCancelable(false); // 不可以通过按取消按钮关闭进度条
                pd2.setProgressStyle(ProgressDialog.STYLE_HORIZONTAL);
                pd2.setIndeterminate(false); // 设置是否隐藏进度，设为false显示进度
                pd2.show();
                // 新建一个线程，重写run()方法
                new Thread()
                {
                    public void run()
                    {
                        while(progressStart < MAXVALUE)
                        {
                            // 这里的算法是决定进度条变化的,可以按需要写
                            progressStart = 2 * usetime() ;
                            // 把信息码发送给handle让更新界面
                            hand.sendEmptyMessage(123);
                        }
                    }
                }.start();
                break;
        }
    }

    //这里设置一个耗时的方法:
    private int usetime() 
    {
        add++;
        try
        {
            Thread.sleep(100);
        }
        catch (InterruptedException e)
        {
            e.printStackTrace();
        }
        return add;
    }
}
```

#### DatePickerDialog日期选择对话框

构造方法：`DatePickerDialog(上下文；DatePickerDialog.OnDateSetListener()监听器；年；月；日)`

```
public class MainActivity extends AppCompatActivity implements View.OnClickListener{

    private Button btn_date;
    private String result = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) 
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        bindViews();
    }

    private void bindViews() {
        btn_date = (Button) findViewById(R.id.btn_date);
        btn_date.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) 
    {
        result = "";
        Calendar cale1 = Calendar.getInstance();
        new DatePickerDialog(MainActivity.this,new DatePickerDialog.OnDateSetListener() {
            @Override
            public void onDateSet(DatePicker view, int year, int monthOfYear, int dayOfMonth)
            {
                // 注意这里获取到的月份需要加上1
                result += "你选择的是"+year+"年"+(monthOfYear+1)+"月"+dayOfMonth+"日";
                Toast.makeText(getApplicationContext(), result, Toast.LENGTH_SHORT).show();
             }
		},cale1.get(Calendar.YEAR),cale1.get(Calendar.MONTH),cale1.get(Calendar.DAY_OF_MONTH)).show();
    }
}
```

#### TimePickerDialog时间选择对话框

构造方法：`TimePickerDialog(上下文；TimePickerDialog.OnTimeSetListener()监听器；小时，分钟，是否采用24小时制)`

```
public class MainActivity extends AppCompatActivity implements View.OnClickListener
{
    private Button btn_time;
    private String result = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) 
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        bindViews();
    }

    private void bindViews() 
    {
        btn_time = (Button) findViewById(R.id.btn_time);
        btn_time.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) 
    {
        result = "";
        Calendar cale2 = Calendar.getInstance();
        new TimePickerDialog(MainActivity.this, new TimePickerDialog.OnTimeSetListener() {
        	@Override
            public void onTimeSet(TimePicker view, int hourOfDay, int minute) 
            {
            	result = "";
                result += "您选择的时间是:"+hourOfDay+"时"+minute+"分";
                Toast.makeText(getApplicationContext(), result, Toast.LENGTH_SHORT).show();
            }
        }, cale2.get(Calendar.HOUR_OF_DAY), cale2.get(Calendar.MINUTE), true).show();
    }
}
```

### PopupWindow悬浮框

Adapter对view的设置
---------------

如何理解Adapter的问题：我们知道无论是在xml还是在java中，页面布局都必须利用view组件完成设置。虽然Adapter是对view进行操作的，但它属于java的功能，不是UI组件，所以理解为它依附于view组件，可以对格式有一个控制。

### ArrayAdapter

支持泛型操作（举个例子，可以理解为利用数组批量操作一组view），只能展现一行文字。  
 ArrayAdapter一般要结合ListView使用，这里列举出系统提供给我们的ListView布局样例：

* `simple_list_item_1`:单独一行的文本框
* `simple_list_item_2`:两个文本框组成（上行为重点，下行为解释，类似于英语词典的格式）
* `simple_list_item_checked`:每项都是由一个已选中的列表项
* `simple_list_item_multiple_choice`:都带有一个复选框
* `simple_list_item_single_choice`:都带有一个单选钮

**举个例子：**  
 在java文件中：

```
//把要显示的数据放在数组里
String[] strs = {"no.1","no.2","no.3","no.4","no.5"};
//注意：除了通过数组外，还可以在res\valuse下创建一个数组资源文件arrays.xml

//创建ArrayAdapter
ArrayAdapter<String> adapter = new ArrayAdapter<String>(this, android.R.layout.系统提供的布局样例, strs);
/*
除了通过字符串数组外，我们还可以：

1.在res\valuse下创建一个数组资源文件arrays.xml，然后将ArrayAdapter写为：
ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(this, R.array.数组名, android.R.layout.系统提供的布局样例);

2.利用List集合，也可以写为：
List<String> data = new ArrayList<String>();
data.add("no.1");
data.add("no.2")；
ArrayAdapter<String> adapter = new ArrayAdapter<String>(this, android.R.layout.系统提供的布局样例, data);
*/

//获取ListView对象，通过调用setAdapter方法为ListView设置Adapter设置适配器
ListView list_test = (ListView) findViewById(R.id.list_test);
list_test.setAdapter(adapter);
```

在ListView文件中：

```
<ListView  
        android:id="@id/list_test"  
        android:layout_height="match_parent"  
        android:layout_width="match_parent"   
        android:entries="@array/数组名"/>
```

### SimpleAdapter

这个Adapter使用广泛，功能比较多。怎么说呢，就是自由度比较高吧。

**举个例子，模拟展示QQ好友列表：** 通过设置map映射，将一个框架中的每个组件放在map里，再将多个map放进一个List中构成列表。  
 在ListView文件中先编写一个列表项目中每一项的布局：

```
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="horizontal">

    <!-- 显示头像 -->
    <ImageView
        android:id="@+id/imgtou"
        android:layout_width="64dp"
        android:layout_height="64dp"
        android:baselineAlignBottom="true"
        android:paddingLeft="8dp" />

    <!-- 用于显示QQ昵称与说说的竖直布局 -->
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical">

        <TextView
            android:id="@+id/name"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:paddingLeft="8dp"
            android:textColor="#1D1D1C"
            android:textSize="20sp" />

        <TextView
            android:id="@+id/says"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:paddingLeft="8px"
            android:textColor="#B4B4B9"
            android:textSize="14sp" />

    </LinearLayout>

</LinearLayout>
```

在MainActivity.java文件中添加布局:

```
public class MainActivity extends AppCompatActivity {
	private String[] names = new String[]{"张三", "李四", "王五"};
    private String[] says = new String[]{"鸡同鸭讲，无趣至极", "百无禁忌，诸事皆宜", "坚持对我来说就是以刚克刚"};
    private int[] imgIds = new int[]{R.mipmap.头像1, R.mipmap.头像2, R.mipmap.头像3};

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        List<Map<String, Object>> listitem = new ArrayList<Map<String, Object>>();
        for (int i = 0; i < names.length; i++)
        {
            Map<String, Object> showitem = new HashMap<String, Object>();
            showitem.put("touxiang", imgIds[i]);
            showitem.put("name", names[i]);
            showitem.put("says", says[i]);
            listitem.add(showitem);
        }

        //创建一个simpleAdapter
        SimpleAdapter myAdapter = new SimpleAdapter(getApplicationContext(), listitem, R.layout.list_item, new String[]{"touxiang", "name", "says"}, new int[]{R.id.imgtou, R.id.name, R.id.says});
        ListView listView = (ListView) findViewById(R.id.list_test);
        listView.setAdapter(myAdapter);
    }
}
```

### SimpleCursorAdapter

这个目前用不到，不写了。

### 自定义BaseAdapter

BaseAdapter和上面三个适配器并不是并列关系，以上三个都属于BaseAdapter，即BaseAdapter是他们的父类。如何自定义一个BaseAdapter呢？以下面这个为例：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/8b18a89c53ac4f017468f966bc9d7660.png)  
 前期工作：已经完成listview的布局设计、声明一个Animal类包含三个成员（头像、昵称、对话）。  
 **自定义BaseAdapter**：自己写一个类（名字随便编），通过继承BaseAdapter实现。

```
public class AnimalAdapter extends BaseAdapter
{

    private LinkedList<Animal> mData;
    private Context mContext;

    public AnimalAdapter(LinkedList<Animal> mData, Context mContext)
    {
        this.mData = mData;
        this.mContext = mContext;
    }

    @Override
    public int getCount() {
        return mData.size();
        //新知识：LinkedList.size() 可以统计列表中的item数量
    }
    @Override
    public Object getItem(int position) {
        return null;
    }
    @Override
    public long getItemId(int position) {
        return position;
    }
    
    //界面上有多少列，就会调用多少次getView
    @Override
    public View getView(int position, View convertView, ViewGroup parent) 
    {
        convertView = LayoutInflater.from(mContext).inflate(R.layout.item_list_animal,parent,false);
        //常用方法：使用inflater寻找自己的xml布局文件
        //convertView是系统提供的View的缓存对象。将上述语句增加判断，可以不用每次都访问xml。
        /*
        if(convertView == null)
        {
       		convertView = LayoutInflater.from(mContext).inflate(R.layout.item_list_animal,parent,false);
    	}
    	但是由于convertView是用来缓存的，当列表内容溢出屏幕时，滚动到屏幕上方的组件（已经离开屏幕的组件）会回到缓存，再次利用于当前屏幕下方新出现的列表内容。如果给列表项设置了多选框，结果会出错。在item数目不大的情况下，不能重用convertView，或者每次getView都将convertView写为null。
    	*/
        
        //获取三个UI组件
        ImageView img_icon = (ImageView) convertView.findViewById(R.id.img_icon);
        TextView txt_aName = (TextView) convertView.findViewById(R.id.txt_aName);
        TextView txt_aSpeak = (TextView) convertView.findViewById(R.id.txt_aSpeak);
        //由于每次都要访问，此处也可以进行优化，将第一次寻找到的id给一个重用组件ViewHolder。
        /*
        
        在getView方法中：
        
		ViewHolder holder = null;
    	if(convertView == null)
    	{
        	convertView = LayoutInflater.from(mContext).inflate(R.layout.item_list_animal,parent,false);
        	holder = new ViewHolder();
        	holder.img_icon = (ImageView) convertView.findViewById(R.id.img_icon);
        	holder.txt_aName = (TextView) convertView.findViewById(R.id.txt_aName);
        	holder.txt_aSpeak = (TextView) convertView.findViewById(R.id.txt_aSpeak);
        	convertView.setTag(holder);   //将Holder存储到convertView中
    	}
    	else
    	{
        	holder = (ViewHolder) convertView.getTag();
    	}
    	holder.img_icon.setBackgroundResource(mData.get(position).getaIcon());
    	holder.txt_aName.setText(mData.get(position).getaName());
    	holder.txt_aSpeak.setText(mData.get(position).getaSpeak());
    	return convertView;
		
		（getView方法外）在自定义baseadapter类里面再定义一个ViewHolder类：

		static class ViewHolder
		{
		    ImageView img_icon;
    		TextView txt_aName;
    		TextView txt_aSpeak;
		}
		*/
        
        //设置组件内容（因为不是事先放在xml中的，需要从java中获取）
        img_icon.setBackgroundResource(mData.get(position).getaIcon());
        txt_aName.setText(mData.get(position).getaName());
        txt_aSpeak.setText(mData.get(position).getaSpeak());
        
        return convertView;
    }
}
```

MainActivity.java中：

```
public class MainActivity extends AppCompatActivity
{

    private List<Animal> mData = null; //自定义的元素列表
    private Context mContext; //用于显示的Activity页面
    private AnimalAdapter mAdapter = null; //自定义的BaseAdapter
    private ListView list_animal; //列表UI组件

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        mContext = MainActivity.this; //就运用于这个activity里
        list_animal = (ListView) findViewById(R.id.list_animal); //获得ListView
        mData = new LinkedList<Animal>(); //用linkedlist声明而不是list
        //添加元素到list中（Java层）
        mData.add(new Animal("狗说", "你是狗么?", R.mipmap.ic_icon_dog));
        mData.add(new Animal("牛说", "你是牛么?", R.mipmap.ic_icon_cow));
        mData.add(new Animal("鸭说", "你是鸭么?", R.mipmap.ic_icon_duck));
        mData.add(new Animal("鱼说", "你是鱼么?", R.mipmap.ic_icon_fish));
        mData.add(new Animal("马说", "你是马么?", R.mipmap.ic_icon_horse));
        //使用适配器，添加list到该activity
        mAdapter = new AnimalAdapter((LinkedList<Animal>) mData, mContext);
        //将适配器与UI布局链接
        list_animal.setAdapter(mAdapter);
    }

}
```

此外，还可以实现重用BadeAdapter，由于我暂时用不到，而且这部分的内容比较难以掌握，所以我也不写了。

java绘图
------

自定义组件类，继承View。构造函数传参，参数列表为Context c，该类的构造函数中要有超类的构造`super(c);`。

`onDraw()`方法：参数列表为Canvas c，重写该方法时要有语句`super.onDraw(canvas);`。

创建实例化Paint的对象：`Paint paint = new Paint();`

根据图片生成位图对象：`Bitmap bitmap = BitmapFactory.decodeResource(this.getResources(), R.drawable.s_jump);`

绘制图片：`canvas.drawBitmap(位图对象, X坐标对象, Y坐标对象,paint对象);`

强制收回图片：`bitmap对象.recycle();`

判断是否回收图片：`bitmap对象.isRecycled()`，返回布尔值

添加布局到java文件中：

```
final view类名 view实例化名 = new view类名(MainActivity.this);
```

设置布局方式：

```
FrameLayout frame = (FrameLayout) findViewById(R.id.布局名字);
frame.addView(继承了view的java文件名);
```

设置前景图片：

```
FrameLayout frame = null;
//该语句初始化变量，不添加具体FrameLayout，在onCreat方法中添加

//下面语句放在方法体中
Drawable a = getResources().getDrawable(R.drawable.图片名称);
frame.setForeground(a);
```

```
TextView t1 = (TextView) findViewById(R.id.txtOne);

StringBuilder str = new StringBuilder();
str.append("点击文字跳转");
t1.setMovementMethod(LinkMovementMethod.getInstance());
t1.setText(addClickPart(str), TextView.BufferType.SPANNABLE);


//定义一个点击每个部分文字的处理方法
private SpannableStringBuilder addClickPart(String str) {

	//创建一个SpannableStringBuilder对象，连接多个字符串
	SpannableStringBuilder ssb = new SpannableStringBuilder(spanStr);
	ssb.append(str);
	ssb.setSpan(new ClickableSpan() {
	@Override
    public void onClick(View widget) 
    {
    	Toast.makeText(MainActivity.this, name,Toast.LENGTH_SHORT).show();
    }

    @Override
    public void updateDrawState(TextPaint ds) 
    {
    	super.updateDrawState(ds);
    	//删除下划线，设置字体颜色为蓝色
    	ds.setColor(Color.BLUE);
    	ds.setUnderlineText(false);
    }
    },start,start + name.length(),0);
}
```

线程问题
----

当App第一次启动时，Android会自动启动一条UI线程（主线程），负责处理与UI相关的事件，如触发事件、修改UI组件等。为了保证线程安全，只允许在UI线程中进行修改。

启动新线程的方法（可以通过继承Thread自定义一个线程类）：

```
Thread thread; // 声明

thread = new Thread();  
thread.start();
```

### Handler消息传递机制

Handler可以使新启动的线程周期性地修改UI组件的属性值。系统在创建UI线程的时候会初始化一个Looper对象，同时也会创建一个与其关联的MessageQueue消息队列，当子线程想修改Activity中的UI组件时，可以新建一个Handler对象，通过这个对象向主线程发送信息，发送的信息会先到主线程的MessageQueue进行等待，由Looper按先入先出顺序取出，再根据message对象的what属性分发给对应的Handler进行处理。

消息message相当于一个“结构体”，其中的what是可以区分消息类别的值，data里可以有很多个成员及其对应的值，传递消息后就可以使用data的数据了，像传参一样。

**Handler的相关方法:**

* `void handleMessage(Message msg)`：处理消息的方法，通常是用于被重写。
* `sendEmptyMessage(int what)`：发送空消息。
* `sendEmptyMessageDelayed(int what,long delayMillis)`：指定延时多少毫秒后发送空信息。
* `sendMessage(Message msg)`：立即发送信息。
* `sendMessageDelayed(Message msg)`：指定延时多少毫秒后发送信息。
* `final boolean hasMessage(int what)`：检查消息队列中是否包含what属性为指定值的消息。如果是参数为`(int what,Object object)`，除了判断what属性，还需要判断Object属性是否为指定对象的消息。

**关于Handler的使用方法举例：**

1. 在主线程中。举例：制作帧动画，每隔一定时间切换图片形成。（布局文件省略）

```
public class MainActivity extends Activity {  
  
    //定义切换的图片的数组id  
    int imgids[] = new int[]{  
        R.drawable.s_1, R.drawable.s_2,R.drawable.s_3,  
        R.drawable.s_4,R.drawable.s_5,R.drawable.s_6,  
        R.drawable.s_7,R.drawable.s_8  
    };  
    int imgstart = 0;  
      
    final Handler myHandler = new Handler(){  
		@Override  
      	//重写handleMessage方法,根据msg中what的值判断是否执行后续操作  
      	public void handleMessage(Message msg)
      	{  
      		if(msg.what == 0x123) // what值类似flag标志，可以自己设计
        	{  
            	imgchange.setImageResource(imgids[imgstart++ % 8]);  
        	}  
      	}  
    };  
    
    @Override  
    protected void onCreate(Bundle savedInstanceState)
    {  
        super.onCreate(savedInstanceState);  
        setContentView(R.layout.activity_main);
        
        final ImageView imgchange = (ImageView) findViewById(R.id.imgchange);  
         
        //使用定时器,每隔200毫秒让handler发送一个空信息  
        new Timer().schedule(new TimerTask() {            
            @Override  
            public void run() 
            {  
                myHandler.sendEmptyMessage(0x123);         
            }  
        }, 0,200);  
    }   
}
```

2. Handler写在子线程中  
    Handler正常工作需要当前线程中有一个Looper对象，所以如果将Handler写在子线程中，需要使用`Looper.prepare();` 创建一个Looper对象，设计好Handler的消息处理方法后，调用`Looper.loop()`方法启动Looper。举例：利用EditText输入一个数，输出从0到这个数经历的每个偶数。XML布局文件省略。

```
public class CalPrime extends Activity  
{  
    static final String UPPER_NUM = "upper";  
    EditText etNum;
    Button btnNum;
    CalThread calThread;  
    // 定义一个线程类  
    class CalThread extends Thread  
    {  
        public Handler mHandler;  
  
        public void run()  
        {  
            Looper.prepare();  
            mHandler = new Handler(){  
                // 定义处理消息的方法  
                @Override  
                public void handleMessage(Message msg)  
                {  
                    if(msg.what == 0x123)  
                    {  
                        int upper = msg.getData().getInt(UPPER_NUM);  
                        List<Integer> nums = new ArrayList<Integer>();  
                        // 寻找从0开始到upper的所有偶数  
                        outer:  
                        for (int i = 0 ; i <= upper ; i++)  
                        {    
                            if(i % 2 ！= 0)  
                            {  
                                continue outer;  
                            }  
                        	nums.add(i);  
                        }  
                        // 使用Toast显示统计出来的所有偶数  
                        Toast.makeText(CalPrime.this , nums.toString()  
                            , Toast.LENGTH_LONG).show();  
                    }  
                }  
            };  
            Looper.loop();  
        }  
    }
    
    @Override  
    public void onCreate(Bundle savedInstanceState)  
    {  
        super.onCreate(savedInstanceState);  
        setContentView(R.layout.main);  
        etNum = (EditText)findViewById(R.id.etNum);
        btnNum = (Button)findViewById(R.id.btnNum);
        calThread = new CalThread();    
        calThread.start();  
    }
    
    // 省略与监听者相关的语句，下面代码展示点击按钮触发的事件处理
    {
    	// 创建消息  
        Message msg = new Message();  
        msg.what = 0x123;  
        // Bundle用于传递数据，它保存的数据是以key-value(键值对)的形式存在的
        Bundle bundle = new Bundle();
        // putInt可以将键值对绑定
        bundle.putInt(UPPER_NUM ,  
            Integer.parseInt(etNum.getText().toString())); // 可以理解为将etNum中输入的数字赋给变量UPPER_NUM
        msg.setData(bundle);
        // 向新线程中的Handler发送消息  
        calThread.mHandler.sendMessage(msg);  
    }  
}
```

### AsyncTask异步任务

暂时不写

---

学完java applet我知道了，要对动作进行相应的方法是对组件添加监听。那么像之前写web一样设置动作可以吗？学习的过程中会逐步找到问题的答案。

事件和监听者
------

**设置监听者有5种方法，分别为：**

1. 使用匿名内部类

```
对象.setxxxListener(new xxxListener() {
	//重写方法
    } ); // 将监听者的方法设置在括号内
```

2. 使用内部类（写在Activity内部）

```
对象.setxxxListener(new xxxxxListener());
 
 // 类名自拟
class xxxxxListener implements View.xxxListener  
{   
	// 以OnClickListener为例，需要重写对应的onClick方法 
    @Override    
    public void onClick(View v)
    {     
    }    
}
```

3. 使用外部类  
    和使用内部类相似，但是由于不在同一个java文件，不能直接使用Activity里的私有成员组件，需要传参。
4. 直接使用Activity作为事件监听器

```
// 使Activity实现接口
对象.setxxxListener(this);

// 重写方法：
@Override
public void xxx(参数列表)
{
}
```

5. 直接绑定到标签  
    在java文件中自定义一个方法，传入一个view组件作为参数，代码如下 。然后在XML需要监听的组件中设置属性`onclick = "myclick（对应方法名）"`。

```
    public void myclick(View source)    
    {    
        Toast.makeText(getApplicationContext(), "按钮被点击了", Toast.LENGTH_SHORT).show();    
    }
```

### 事件的传播处理机制

在学习监听者之前，需要了解到，组件本身也存在一种基于回调的事件处理机制。

**事件的传播处理步骤如下：**  
 当事件发生在某组件身上，先触发组件所绑定的监听器对应的事件处理方法，然后回调除法组件本身的事件处理方法，最后还可以再触发activity的回调方法。其中如果处理方法返回值为false，表示对该事件的处理未结束，才会执行下一步的处理，若为true则不会触发下一步。

**常见View组件的回调方法：**

1. 在该组件上触发屏幕事件：`boolean onTouchEvent(MotionEvent event);`
2. 在该组件上按下某个按钮时：`boolean onKeyDown(int keyCode,KeyEvent event);`
3. 松开组件上的某个按钮时：`boolean onKeyUp(int keyCode,KeyEvent event);`
4. 长按组件某个按钮时：`boolean onKeyLongPress(int keyCode,KeyEvent event);`
5. 键盘快捷键事件发生：`boolean onKeyShortcut(int keyCode,KeyEvent event);`
6. 在组件上触发轨迹球屏事件：`boolean onTrackballEvent(MotionEvent event);`（轨迹球可以显示鼠标轨迹，不用管它，用不上）
7. 当组件的焦点发生改变：`protected void onFocusChanged(boolean gainFocus, int direction, Rect previously FocusedRect)`（这个方法只能够在View中重写）

以按钮为例，已经写好的xml文件省略，java文件中需要继承基本的GUI组件（此例中为Button），自定义View类，重写组件的事件处理方法。

```
public class MyButton extends Button{  
    private static String TAG = "Dangerous";  
    public MyButton(Context context, AttributeSet attrs) {  
        super(context, attrs);  
    }  
  
    //重写键盘按下触发的事件  
    @Override  
    public boolean onKeyDown(int keyCode, KeyEvent event) {  
        super.onKeyDown(keyCode,event);  
        Log.i(TAG, "onKeyDown方法被调用"); // Log用于显示日志
        return true;  
    }  
  
    //重写弹起键盘触发的事件  
    @Override  
    public boolean onKeyUp(int keyCode, KeyEvent event) {  
        super.onKeyUp(keyCode,event);  
        Log.i(TAG,"onKeyUp方法被调用");  
        return true;  
    }  
  
    //组件被触摸了  
    @Override  
    public boolean onTouchEvent(MotionEvent event) {  
        super.onTouchEvent(event);  
        Log.i(TAG,"onTouchEvent方法被调用");  
        return true;  
    }  
}
```

#### onTouchEvent( )回调方法

举个例子：定义一个简单的view，绘制一个蓝色的小圆，可以跟随手指进行移动。

```
public class MyView extends View
{  
    public float X = 50;  
    public float Y = 50;  
  
    //创建画笔  
    Paint paint = new Paint();  
  
    public MyView(Context context,AttributeSet set)  
    {  
        super(context,set);  
    }  
  
    @Override  
    public void onDraw(Canvas canvas) {  
        super.onDraw(canvas);  
        paint.setColor(Color.BLUE);  
        canvas.drawCircle(X,Y,30,paint);  
    }  
  
    @Override  
    public boolean onTouchEvent(MotionEvent event) {  
        this.X = event.getX();  
        this.Y = event.getY();  
        //通知组件进行重绘  
        this.invalidate();  
        return true;  
    }  
}
```

### 触摸事件监听者

例子：通过设置触摸事件监听器，使图片随着手指触摸移动。

```
组件类名.setOnTouchListener(new OnTouchListener() {  
    @Override  
    public boolean onTouch(View view, MotionEvent event) {  
        //设置组件显示的位置  
        组件实例对象.成员变量（表示坐标x） = event.getX() - 150;  
        组件实例对象.成员变量（表示坐标y） = event.getY() - 150;  
        //调用重绘方法  
        组件实例对象.invalidate();  
        return true;  
    } 
});
```

上述案例中，`event.getX()`和`event.getY()`方法可以获取点击焦点。另外，通过event.getX(int)或者event.getY(int)可以来获得不同触摸点的位置，实现对多点触摸（例如两个手指实现缩放图片）的控制： 比如event.getX(0)可以获得第一个接触点的X坐标，event.getX(1)获得第二个接触点的X坐标，以此类推……

其中onTouch(View v, MotionEvent event)方法中的参数依次是触发触摸事件的组件、触碰事件event（封装了触发事件的详细信息，同样包括事件的类型、触发时间等信息）。

可以使用`event.getAction( )`和`event.getAction() & MotionEvent.ACTION_MASK`对触摸的动作类型进行判断：  
 注意：这里的&是位运算，因为每一种结果其实都是已经定义好的常量

* `event.getAction == MotionEvent.ACTION_DOWN`：按下事件。
* `event.getAction == MotionEvent.ACTION_MOVE`：移动事件。
* `event.getAction == MotionEvent.ACTION_UP`：弹起事件。
* `event.getAction == MotionEvent.ACTION_POINTER_DOWN`：当屏幕上已经有一个点被按住，此时再按下其他点时触发。
* `event.getAction == MotionEvent.ACTION_POINTER_UP`：当屏幕上有多个点被按住，松开其中一个点时触发（即非最后一个点被放开时）。

还可以在调用MotionEvent对象event的`getPointerCount()`方法判断当前有多少个手指在触摸。

### 单击事件监听者

以button为例：

```
private Button 对象名（如：btn）;
    
@Override
protected void onCreate(Bundle savedInstanceState) 
{
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main);
    btn = (Button) findViewById(R.id.组件id);
    
    // 使用setOnClickListener添加监听者
    btn.setOnClickListener(new OnClickListener() {
        @Override
        public void onClick(View v) // 参数View v为必填项
        {
        	// 通过点击按钮，使文字实现X和O的交替
            if(btn.getText().toString().equals("X"))
            {
                btn.setText("O");
            }
            else
            {
                btn.setText("X");
            }
        }
    }); // 将监听者OnClickListener的方法设置在括号内
}
```

### 选中事件监听者

接口为`CompoundButton.OnCheckedChangeListener`。  
 引包：`import android.widget.RadioGroup.OnCheckedChangeListener;`

以单选事件为例，直接获取选中的选项：

```
RadioGroup radgroup = (RadioGroup) findViewById(R.id.radioGroup);

//为radioGroup设置一个监听器:setOnCheckedChanged()  
radgroup.setOnCheckedChangeListener(new OnCheckedChangeListener() {
    @Override
    public void onCheckedChanged(RadioGroup group, int checkedId) 
    {
        RadioButton radbtn = (RadioButton) findViewById(checkedId);
        Toast.makeText(getApplicationContext(), "按钮组值发生改变,你选了" + radbtn.getText(), Toast.LENGTH_LONG).show();
        // Toast控制的是页面下方弹出的提示窗口
    }
});
```

以多选事件为例，直接获取选中的选项：

```
checkbutton对象名.setOnCheckedChangeListener(this);

@Override
public void onCheckedChanged(CompoundButton compoundButton, boolean b)
{
   if(compoundButton.isChecked()) Toast.makeText(this,compoundButton.getText().toString(),Toast.LENGTH_SHORT).show();
}
```

开关所用的监听者类型也是CheckedChange。

### 拖动条事件监听者

`SeekBar.OnSeekBarChangeListener`需要重写三个对应的方法：

* `onProgressChanged()`：进度发生改变时会触发。
* `onStartTrackingTouch()`：按住SeekBar时会触发。
* `onStopTrackingTouch()`：放开SeekBar时触发。

```
sb.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
	
	@Override
	public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) 
	{
        textview名.setText("当前进度值:" + progress + "  / 100 ");
    }

    @Override
    public void onStartTrackingTouch(SeekBar seekBar)
    {
        Toast.makeText(指定activity.this, "触碰SeekBar", Toast.LENGTH_SHORT).show();
    }

    @Override
    public void onStopTrackingTouch(SeekBar seekBar)
    {
        Toast.makeText(指定activity.this, "放开SeekBar", Toast.LENGTH_SHORT).show();
    }
});
```

### 星级评分事件监听者

设置`OnRatingBarChangeListener`事件，重写`onRatingChanged()`方法。

### 日期选择事件监听者

`DatePicker.OnDateChangedListener`可以重写`onDateChanged()`方法。  
 `CalendarView.OnDateChangeListener`可以重写`onSelectedDayChange`方法。

### 时间选择事件监听者

若TimePicker中组件为spinner类型，可以设置监听者：  
 `TimePicker.OnTimeChangedListener`可以重写`onTimeChanged`方法。

### 列表选择事件监听者

在一个ListView中单击选择某一项，可以通过接口实现`implements AdapterView.OnItemClickListener`设置监听者：

```
ListView组件名.setOnItemClickListener(this);
```

```
@Override
public void onItemClick(AdapterView<?> parent, View view, int position, long id) 
{
    Toast.makeText(mContext,"你点击了第" + position + "项",Toast.LENGTH_SHORT).show();
}
```

### 文本内容变化事件监听者

这个监听者用于监听EditText的内容变化，调用`EditText.addTextChangedListener(mTextWatcher);` 方法。该类需要实现三个方法分别为：

* `public void beforeTextChanged(CharSequence s, int start,int count, int after);`：内容变化前触发。
* `public void onTextChanged(CharSequence s, int start, int before, int count);`：内容变化中触发。
* `public void afterTextChanged(Editable s);`：内容变化后触发。

举例：自定义EditText，输入内容后文本框会弹出“清空”按钮

```
public class DelEditText extends EditText
{
    private Drawable imgClear; // “清空”按钮的图片资源
    private Context mContext;

	// 自定义EditText的方法
    public DelEditText(Context context, AttributeSet attrs) {
        super(context, attrs);
        this.mContext = context;
        init(); //需要启动哦
    }

    private void init()
    {
        imgClear = mContext.getResources().getDrawable(R.drawable.delete_gray);
        addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after)
            {
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count)
            {
            }

            @Override
            public void afterTextChanged(Editable editable)
            {
                setDrawable();
            }
        });
    }

    //绘制删除图片
    private void setDrawable()
    {
        if (length() < 1)
            setCompoundDrawablesWithIntrinsicBounds(null, null, null, null);
        else
            setCompoundDrawablesWithIntrinsicBounds(null, null, imgClear, null);
    }

    //当点击“清空”按钮附近时，清除文字（但是我这里看不懂）
    @Override
    public boolean onTouchEvent(MotionEvent event) {
        if(imgClear != null && event.getAction() == MotionEvent.ACTION_UP)
        {
            int eventX = (int) event.getRawX();
            int eventY = (int) event.getRawY();
            Rect rect = new Rect();
            getGlobalVisibleRect(rect);
            rect.left = rect.right - 100;
            if (rect.contains(eventX, eventY))
                setText("");
        }
        return super.onTouchEvent(event);
    }


    @Override
    protected void finalize() throws Throwable
    {
        super.finalize();
    }
}
```

举例：通过点击按钮设置密码可见。

```
public class MainActivity extends AppCompatActivity
{

    private EditText edit_pawd;
    private Button btnChange;
    private boolean flag = false;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        edit_pawd = (EditText) findViewById(R.id.edit_pawd);
        btnChange = (Button) findViewById(R.id.btnChange);
        
        btnChange.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view)
            {
                if(flag == true)
                {
                    edit_pawd.setTransformationMethod(HideReturnsTransformationMethod.getInstance());
                    flag = false;
                    btnChange.setText("密码不可见");
                }
                else
                {
                    edit_pawd.setTransformationMethod(PasswordTransformationMethod.getInstance());
                    flag = true;
                    btnChange.setText("密码可见");
                }
            }
        });
    }
}
```

Button对象
--------

**提前写好xml布局文件后，在使用前需要：**  
 引包：`import android.widget.Button;`  
 声明：`private Button myButton;`  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/8058a87ca25fa07d847d35a810dc953d.png)

Activity
--------

通过前面的使用，大致能感受到Activity的用途，可以看做是一个界面。Android系统使用Task（栈）存储Activity，后进先出，当按下回退键时，activity栈中栈顶的activity弹出。

### 启动

**启动新的activity的方法：** 调用startActivity(Intent);

```
// 第一种：
Intent it = new Intent(MainActivity.this, MyActivity.class);
startActivity(it);

// 第二种（最常用）：
startActivity(new Intent(当前Act.this, 要启动的Act.class));

// 第三种：
ComponentName cn = new ComponentName("当前Act的全限定类名","启动Act的全限定类名") ;
Intent intent = new Intent() ;
intent.setComponent(cn) ;
startActivity(intent) ;

// 第四种：
Intent intent = new Intent("android.intent.action.MAIN");
intent.setClassName("当前Act的全限定类名","启动Act的全限定类名");
startActivity(intent);

// 第五种：
Intent intent = getPackageManager().getLaunchIntentForPackage("apk第一个启动的Activity的全限定类名") ;
if(intent != null) startActivity(intent) ;
```

另外还有一种隐式启动的方法，通过Intent-filter：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/126f11db9b91e43f8f1f5ee44de05d01.png)

**关闭activity的方法：**

```
finish();
```

### Activity的回调方法

Activity生命周期回调方法用于控制Activity处于不同状态下时应用程序的运行方式，例如当用户切出或者切回应用。Android系统会在我们的Activity进入某种特定状态后调用这些方法，从而通过一系列步骤确保应用程序能够继续起效、不至于丢失数据而且在用户不与之交互时不会使用非必要性资源。

注意：回调方法只能重写其内容，不能调用，由Activity决定什么时候调用。

#### onCreate方法

Activity首次被创建时会首先回调onCreate方法，相当于重复用户启动应用程序后的流程。这时候onCreate方法会使应用程序进入Created状态。

重写onCreat方法：

```
@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_home);  // 设置要显示的视图
	}
```

* Bundle参数：负责自动进行视图信息保存。

**横竖屏时想加载不同的布局：**  
 一般是在onCreate()方法中加载布局文件的，可以创建两个布局文件夹分别为“layout-land横屏”、“layout-port竖屏”，然后把这两套文件名一样的布局文件放在两个文件夹里，Android会自己根据横竖屏加载不同布局。

也可以自己在代码中进行判断：

```
if (this.getResources().getConfiguration().orientation == Configuration.ORIENTATION_LANDSCAPE)
{  
     setContentView(R.layout.横屏布局);
}  
else if (this.getResources().getConfiguration().orientation ==Configuration.ORIENTATION_PORTRAIT) 
{  
    setContentView(R.layout.竖屏布局);
}
```

**设置Activity全屏：**  
 方法一：在onCreate中使用`getActionBar.hide();`代码隐藏ActionBar。

```
ActionBar act_bar = getActionBar();
act_bar.hide();
```

方法二：在onCreate中使用`requestWindowFeature(Window.FEATURE_NO_TITLE);` ，注意该代码需要在setContentView ()之前调用，不然会报错。

#### onStart方法

让已经被创建的Activity显示给用户。

#### onRestart方法

使已经不可见的Activity再次显示给用户。

#### onResume方法

使已经显示给用户的Activity获得焦点，或用户按了回退键，退到前一个Activity重新获得焦点。

onResume方法负责提供Resumed状态，获得焦点，这时应用程序可以接受用户的直接操作。其它各类回调方法都以onResume为核心，即将应用程序引导至Resumed状态或者从该状态脱离、启动该状态或者将其停止。

#### onPause方法

有另一个Activity覆盖到本Activity前面，新的Activity获得焦点，保存前一个Activity的数据。

#### onStop方法

新的Activity已经获得焦点，本Activity不可见。

#### onDestroy方法

Activity完成工作或由系统销毁。销毁之后可以通过`finish()`关闭Activity。

### 其他方法

1. onSaveInstanceState  
    当系统"未经你许可"销毁了你的activity，则onSaveInstanceState会被系统调用， 它提供一个机会让你保存你的数据。

```
public void onSaveInstanceState(Bundle outState, PersistableBundle outPersistentState)
```

触发该方法的情况：点击home键回到主页或长按后选择运行其他程序、按下电源键关闭屏幕、启动新的Activity、横竖屏切换时（因为横竖屏切换的时候会先销毁Act，然后再重新创建）。

**详细介绍Bundle savedInstanceState参数：**  
 重写onSaveInstanceState()方法，利用`Bund.leputInt()`方法可以往bundle中写入数据，比如：

```
outState.putInt("num",1);
```

然后在onCreate或者onRestoreInstanceState（这个下面会讲）中就可以拿出里面存储的数据（拿之前要判断是否为null），如：

```
savedInstanceState.getInt("num"); // savedInstanceState是bundle对象
```

2. onRestoreInstanceState  
    可以获取到保存的数据，一般是在onStart()和onResume()之间执行，避免Act跳转而没有关闭， 然后不走onCreate()方法。

```
public void onRestoreInstanceState(Bundle savedInstanceState, PersistableBundle persistentState)
```

### 数据传递

**前一个act向后一个act传递：**

1. 传递一个数据

存数据：

```
Intent it1 = new Intent(A.this, B.class);
it1.putExtra("key", value);
startActivity(it1);
```

取数据：

```
Intent it2 = getIntent();
getStringExtra("key"); // 不同数据类型有不同方法名：get数据类型Extra()
```

2. 传递多个数据

存数据：

```
Intent it1 = new Intent(A.this, B.class);
Bundle bd = new Bundle();
bd.putInt("num", 1);
bd.putString("detail", "哈喽");
it1.putExtras(bd);
startActivity(it1);
```

取数据：

```
Intent it2 = getIntent();
Bundle bd = it2.getExtras();
int n = bd.getInt("num");
String d = bd.getString("detail");
```

注意：Bundle的大小是有限制的，必须< 0.5MB。

**后一个act传回给前一个act：**  
 步骤如下：  
 1：使用`startActivityForResult(Intent intent, int requestCode)`启动一个Activity。  
 2：在启动的Activity中重写`onActivityResult(Int requestCode, int resultCode, Intent data)`。requestCode可以用来区分同一个Activity中不同的启动方式对应不同的值，是子Activity通过setResult()返回的。  
 3：在子Activity重写`setResult(int reaultCode, Intent data)`。

### 退出

我们知道activity栈中，可以使用`finish()`方法弹出栈顶的act。还有一种方法！！其实可以指定退出本activity！使用`当前activity.this.finish();`即可！

双击退出程序：

```
// 第一种方法：定义一个变量，来标识是否退出
private static boolean isExit = false;
Handler mHandler = new Handler() {
    @Override
    public void handleMessage(Message msg) {
        super.handleMessage(msg);
        isExit = false;
    }
};

public boolean onKeyDown(int keyCode, KeyEvent event)
{
    if (keyCode == KeyEvent.KEYCODE_BACK)
    {
        if (!isExit)
        {
            isExit = true;
            Toast.makeText(getApplicationContext(), "再按一次退出程序", Toast.LENGTH_SHORT).show();
            // 利用handler延迟发送更改状态信息
            mHandler.sendEmptyMessageDelayed(0, 2000);
        } 
        else
        {
            exit(this);
        }
        return false;
    }
	return super.onKeyDown(keyCode, event);
}

// 第二种方法：保存点击的时间
private long exitTime = 0;
public boolean onKeyDown(int keyCode, KeyEvent event) 
{
    if (keyCode == KeyEvent.KEYCODE_BACK) 
    {
        if ((System.currentTimeMillis() - exitTime) > 2000) 
        {
            Toast.makeText(getApplicationContext(), "再按一次退出程序", Toast.LENGTH_SHORT).show();
            exitTime = System.currentTimeMillis();
        }
        else
        {
        	exit();
        }
        return false;
    }
    return super.onKeyDown(keyCode, event);
}
```

Intent(意图)
----------

### 显式与隐式

显式Intent：通过组件名指定启动的目标组件，比如`startActivity(new Intent(A.this,B.class));` ，每次启动的组件只有一个。

隐式Intent：不指定组件名，而指定Intent的Action、Data、或Category，启动组件时会匹配AndroidManifest.xml相关组件的Intent-filter，逐一匹配出满足属性的组件。当不止一个满足时, 会弹出一个选择启动哪个的对话框。

### 属性

1. ComponentName(组件名称)  
    ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/fd2394679b9adedf791b8cd0c5c9f9d7.png)
2. Action(动作)  
    ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/bbe7ed2e8a6ef317e0b774cfb60bfd13.png)
3. Category(类别)  
    ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6dc556cedeb916752a127f5ca40ccd89.png)
4. Data(数据)，Type(MIME类型)  
    ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/40d43d913d63102eacfeb2a9c45f3eed.png)
5. Extras(额外)  
    ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/492bcc7f149f309fde6435c998a9fc0f.png)
6. Flags(标记)  
    ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b164fac709e882812c163a19e212153c.png)

【未完待续】

[Android 列表 notifyDataSetChanged 不刷新](https://blog.csdn.net/ysthuigui/article/details/105656807)