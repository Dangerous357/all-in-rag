# 如何自己开发一个Android APP（6）——程序与操作系统合作

系统的事件处理
-------

### 响应系统设置的事件Configuration类

**获取系统的Configuration对象：**`Configuration cfg = getResources().getConfiguration();`

**Configuration类的常用方法：**

* `densityDpi`：屏幕密度。
* `fontScale`：当前用户设置的字体的缩放因子。
* `hardKeyboardHidden`：判断硬键盘是否可见，有两个可选值：`HARDKEYBOARDHIDDEN_NO`：数值为十六进制的0；  
   `HARDKEYBOARDHIDDEN_YES`：数值为十六进制的1。
* `keyboard`：获取当前关联的键盘类型，该属性的返回值：`KEYBOARD_12KEY`：是只有12个键的小键盘；  
   `KEYBOARD_NOKEYS`：（不知道这是什么……）；  
   `KEYBOARD_QWERTY`：普通键盘。
* `keyboardHidden`：该属性返回一个boolean值用于标识当前键盘是否可用。该属性不仅会判断系统的硬件键盘，也会判断系统的软键盘（位于屏幕）。
* `locale`：获取用户当前的语言环境。
* `mcc`：获取移动信号的国家码。
* mnc：获取移动信号的网络码。
* `ps`：国家代码和网络代码共同确定当前手机网络运营商。
* `navigation`：判断系统上方向导航设备的类型。该属性的返回值：`NAVIGATION_NONAV`：无导航；  
   `NAVIGATION_DPAD`：DPAD导航；  
   `NAVIGATION_TRACKBALL`：轨迹球导航；  
   `NAVIGATION_WHEEL`：滚轮导航。
* `orientation`：获取系统屏幕的方向。该属性的返回值：`ORIENTATION_LANDSCAPE`：横向屏幕；  
   `ORIENTATION_PORTRAIT`：竖向屏幕。
* `screenHeightDp`：屏幕可用高，用dp表示。
* `screenWidthDp`：屏幕可用宽，用dp表示。
* `touchscreen`：获取系统触摸屏的触摸方式。该属性的返回值：  
   `TOUCHSCREEN_NOTOUCH`：无触摸屏；  
   `TOUCHSCREEN_STYLUS`：触摸笔式触摸屏；  
   `TOUCHSCREEN_FINGER`：接收手指的触摸屏。

**重写onConfigurationChanged回调方法响应系统设置更改：**  
 onConfigurationChanged回调方法是activity级别的回调。

注意：targetSdkVersion属性最高只能设置为12，高于12时该方法不会响应。举例：设置一个按钮，点击按钮可以实现横竖屏切换，使用Configuration获取系统当前的屏幕状态。  
 首先要在AndroidManifest.xml中添加权限： `< uses-permission android:name="android.permission.CHANGE_CONFIGURATION" />` ，在activity标签中添加：`android:configChanges="orientation"` 。

```
public class MainActivity extends Activity
{  
  
    @Override  
    protected void onCreate(Bundle savedInstanceState)
    {  
        super.onCreate(savedInstanceState);  
        setContentView(R.layout.activity_main);  
          
        Button btn = (Button) findViewById(R.id.btncahange);  
        btn.setOnClickListener(new OnClickListener() {  
              
            @Override  
            public void onClick(View v) 
            {  
                Configuration config = getResources().getConfiguration();  
                //如果是横屏的话切换成竖屏  
                if(config.orientation == Configuration.ORIENTATION_LANDSCAPE)  
                {  
                    MainActivity.this.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);  
                }  
                //如果竖屏的话切换成横屏  
                if(config.orientation == Configuration.ORIENTATION_PORTRAIT)  
                {  
                    MainActivity.this.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);  
                }  
            }  
        });  
    }  
      
    @Override  
    public void onConfigurationChanged(Configuration newConfig)
    {  
        super.onConfigurationChanged(newConfig);  
        String screen = newConfig.orientation == Configuration.ORIENTATION_LANDSCAPE?"横屏":"竖屏";  
        Toast.makeText(MainActivity.this, "系统屏幕方向发生改变 \n 修改后的方向为" + screen, Toast.LENGTH_SHORT).show();  
    }  
}
```

生命周期
----

### 五种状态

#### Created

#### Started

#### Resumed

当应用程序正处于运行当中且用户与之进行操作交互，这时的应用状态为Resumed。

#### Paused

当另一个Activity处于前台但仅仅使应用被部分隐藏时，这时的应用状态为Paused——在这种状态下用户无法再与应用进行交互。

#### Stopped

当应用完全处于后台之下，而且用户既无法操作、也无法观看到它时，其状态即为Stopped。在这种状态下Activity会保留之前的所有数据，但无法加以执行。

**有七种回调方法能够让应用进入或者脱离上述状态。分别是：onCreate、onStart、onRestart、onResume、onPause、 onStop以及onDestroy。**

### 生命周期

Android在启动后会首先执行主Activity类中的onCreate方法。可以利用通过Intent类启动另一个非主Activity：

```
Intent aboutIntent = new Intent(this, Activity类名.class);
startActivity(aboutIntent);
```

onCreate方法开始执行之后，onStart与onResume两个方法也将开始执行， 从而使该Activity处于Resumed状态。

当应用程序处于退出或者隐藏状态下，则Resumed就会转变为Destroyed。这时候，onPause方法会将应用的Activity 由运行时的Resumed状态转换为Paused状态。在onPause当中，应当停止任何需要占用资源的任务，例如动画播放、传感器数据处理以及广播接收等等。

如果Activity处于Paused或者Stopped状态，则应用程序切换至当前Activity之后该Activity将直接进入前台运行模式，且无需重复调用onCreate方法。如果应用从Paused状态切换回Resumed状态，则Activity的onResume方法将开始执行。如果该应用由Stopped状态切换回运行状态，则执行onRestart方法、而后依次为onStart与onResume方法。**onRestart方法只会在应用程序从Stopped状态恢复至前台之后才会执行**

在onPause之后，如果应用程序进入Stopped状态，onStop也将开始执行。在这种情况下，onRestart、onStart以 及onResume等方法仍然能够使应用程序重新回到Resumed状态。

如果应用程序即将彻底关闭，则onDestroy方法会开始执行。  
 在onDestroy执行之后，如果用户通过导航返回应用程序Activity，则对应onCreate方法将再次被启动。

### 横竖屏切换时的生命周期

App横竖屏切换的时候会销毁当前的Activity然后重新创建一个， 横竖屏切换时Act走下述生命周期：  
 onPause-> onStop-> onDestory-> onCreate->onStart->onResume

文件
--

**Android中的操作模式**  
 Android是基于Linux的，在读写文件的时候，需加上文件的操作模式，Android中的操作模式如下：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/85e74c3cbeb56af5024799c984312792.png)

**文件的相关操作方法**  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d4447c1f15c77711d81fe7b644781df3.png)  
 **文件读写**  
 可以参考一下这篇文章：[Android 在指定目录创建并写入文件](https://www.cnblogs.com/proscientist/p/8447097.html)  
 自己写一个java文件FileHelper，实现文件的读写：

```
public class FileHelper
{

    private Context mContext;

    public FileHelper() {}
    public FileHelper(Context mContext)
    {
        super();
        this.mContext = mContext;
    }

    // 定义一个文件保存的方法，使用输出流将数据输出到文件中
    public void save(String filename, String filecontent) throws Exception
    {
        FileOutputStream output = mContext.openFileOutput(filename, Context.MODE_PRIVATE); // 使用私有模式，创建出来的文件只能被本应用访问，还会覆盖原文件
        output.write(filecontent.getBytes()); // 将String字符串以字节流的形式写入到输出流中
        output.close(); // 关闭输出流
    }


    // 文件读取的方法
    public String read(String filename) throws IOException 
    {
        //打开文件输入流
        FileInputStream input = mContext.openFileInput(filename);
        byte[] temp = new byte[1024];
        StringBuilder sb = new StringBuilder("");
        int len = 0;
        //读取文件内容:
        while ((len = input.read(temp)) > 0)
        {
            sb.append(new String(temp, 0, len));
        }
        input.close(); //关闭输入流
        return sb.toString();
    }

}
```

MainActivity.java中：

```
public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    private EditText editname;
    private EditText editdetail;
    private Button btnsave;
    private Button btnclean;
    private Button btnread;
    private Context mContext;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        mContext = getApplicationContext();
        bindViews();
    }


    private void bindViews() 
    {
        editdetail = (EditText) findViewById(R.id.editdetail); // 编辑文档
        editname = (EditText) findViewById(R.id.editname); // 文件名
        btnsave = (Button) findViewById(R.id.btnsave); // 保存按钮
        btnread = (Button) findViewById(R.id.btnread); // 读取按钮

        btnsave.setOnClickListener(this);
        btnread.setOnClickListener(this);
    }


    @Override
    public void onClick(View v) 
    {
        switch (v.getId()) 
        {
            case R.id.btnsave:
                FileHelper fHelper = new FileHelper(mContext);
                String filename = editname.getText().toString();
                String filedetail = editdetail.getText().toString();
                try
                {
                    fHelper.save(filename, filedetail);
                    Toast.makeText(getApplicationContext(), "数据写入成功", Toast.LENGTH_SHORT).show();
                }
                catch (Exception e)
                {
                    e.printStackTrace();
                    Toast.makeText(getApplicationContext(), "数据写入失败", Toast.LENGTH_SHORT).show();
                }
                break;
                
            case R.id.btnread:
                String detail = "";
                FileHelper fHelper2 = new FileHelper(getApplicationContext());
                try 
                {
                    String fname = editname.getText().toString();
                    detail = fHelper2.read(fname);
                } 
                catch (IOException e) 
                {
                    e.printStackTrace();
                }
                Toast.makeText(getApplicationContext(), detail, Toast.LENGTH_SHORT).show();
                break;
        }
    }
}
```