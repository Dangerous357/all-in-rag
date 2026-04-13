# 蓝桥杯JAVA训练笔记

### 注意事项

#### 从各处收集的注意事项

* switch的判断字符串是在java1.7才有，一般蓝桥杯环境应该是1.6

#### 自己发现的问题

* 在时间或空间要求比较严格的问题中，用Scanner输入和用println输出可能会超限。解决办法见下文。
* JVM对栈的深度也是有要求的，我测试大概深度1000多栈就会爆，抛出error。如果提交的话应该是runtime error。所以递归次数不能太多。

### eclipse前期准备

设置自动补全代码和引包!!!

### 各数据变量的范围

1. java变量  
    ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2f8be2ba5bfc2a5230939ddbeb5ac6ed.png)
2. 对象  
    空对象占8个字节（64bit），如果有数据成员，要把数据成员按基本数据类型和对象引用分开统计。  
    **对象占用字节数=基本的8字节＋基本数据类型所占的＋对象引用所占的**  
    其中，基本数据类型所占空间累加，然后对齐到8的倍数。 对象引用按每个4字节，累加后对齐到8的倍数。
3. 实用举例  
    (1) 源文件中String按utf-8编码后最长不能超过2个字节，即最大长度为65535。  
    参考来源：[java String大小限制](https://blog.csdn.net/crookshanks_/article/details/93718123)

### 控制格式输入输出

#### 控制格式输入

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ad5f8b524704356d11e2d5e4a15b3158.png)

```
Scanner s = new Scanner(System.in);
int x1 = 0, y1 = 0, x2 = 0, y2 = 0;
// 输入第一行
String[] xy = s.nextLine().split(",");
x1 = Integer.parseInt(xy[0]);
y1 = Integer.parseInt(xy[1]);
x2 = Integer.parseInt(xy[2]);
y2 = Integer.parseInt(xy[3]);
// 输入第二行
xy = s.nextLine().split(",");
x1 = Integer.parseInt(xy[0]);
y1 = Integer.parseInt(xy[1]);
x2 = Integer.parseInt(xy[2]);
y2 = Integer.parseInt(xy[3]);
```

#### 控制格式输出

1. 四舍五入保留小数点后x位

```
double s = 3.14159265358979323;
System.out.println(String.format("%.7f",s);
```

2. printf  
    用`System.out.println();`可以像C一样直接带格式输出。例如：

```
System.out.printf("%d %d %d", p, j, k);
```

### 实用函数

#### String类的常用函数

**1. 构造方法**

* `public String()`:创建String对象
* `public String(byte[] bytes)`:把字节数组转成字符串。
* `public String(byte[] bytes,int index,int length)`:把字节数组中的一部分转成字符串
* `public String(char[] value)`:把字符数组转成字符串
* `public String(char[] value,int index,int count)`:把字符数组的一部分转成字符串
* `public String(String original)`:把字符串转成字符串

**2.判断功能**

* `boolean equals(Object obj)`:比较字符串的内容是否相同，严格区分大小写
* `boolean equalsIgnoreCase(String str)`:比较字符串的内容是否相同，不考虑大小写
* `boolean contains(String str)`:判断是否包含指定的小串
* `boolean startsWith(String str)`:判断是否以指定的字符串开头
* `boolean endsWith(String str)`:判断是否以指定的字符串结尾
* `boolean isEmpty()`:判断字符串的内容是否为空

**3.获取功能**

* `int length()`:返回字符串的长度（字符的个数）。
* `char charAt(int index)`:返回字符串中指定位置的字符。
* `int indexOf(int ch)`:返回指定字符在字符串中第一次出现的位置
* `int indexOf(String str)`:返回指定字符串在字符串中第一次出现的位置
* `int indexOf(int ch,int fromIndex)`:返回指定字符从指定位置开始在字符串中第一次出现的位置
* `int indexOf(String str,int fromIndex)`:返回指定字符串从指定位置开始在字符串中第一次出现的位置
* `String substring(int start)`:返回从指定位置开始到末尾的子串
* `String substring(int start,int end)`:返回从指定位置开始到指定位置结束的子串（左闭右开）

**4.转换功能**

* `byte[] getBytes()`:把字符串转换为字节数组
* `char[] toCharArray()`:把字符串转换为字符数组
* `static String valueOf(char[] chs)`:把字符数组转成字符串
* `static String valueOf(int i)`:把int类型的数据转成字符串
* `String toLowerCase()`:把字符串转小写
* `String toUpperCase()`:把字符串转大写
* `String concat(String str)`:字符串的连接

**5.替换功能**

* `String replace(char old,char new)`
* `String replace(String old,String new)`

**6.去除字符串空格**

* `String trim()`

**7.按字典顺序比较两个字符串**

* `int compareTo(String str)`
* `int compareToIgnoreCase(String str)`

参考来源：[Java中关于String的常用函数](https://blog.csdn.net/qq9764312/article/details/79563031)

#### Math类的常用函数

Math要引包`import java.math.*;`

1. `Math.log(double)`  
    log(x)表示以e为底x的对数。如果想改变底数可以用换底公式：  
    ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/33547d3203343e224d302e7d7973d18a.png)

### BigInteger、BigDecimal类

#### 摘要

若在操作的时候一个数据已经超过了最大类型长度的话，此数据无法装入，引入大数操作：使用BigInteger操作整数；使用BigDecimal指定小数的保留位数。这些大数都将以字符串的形式传入。理论上能表示无限大的数。  
 **这两个类都在`java.math.*`包中。**

#### BigInteger类的实用方法

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7f02a9940191bbe7b76051096d3c1922.png)

* `valueOf(parament)`：将某种类型的参数转换为大数类型
* `pow()`：a.pow(b)=a^b
* `gcd()`：最大公约数
* `abs()`：绝对值
* `negate()`：取反数
* `boolean equals()`：是否相等
* `a.compareTo(b)`：比较大数a和b的大小，若相等返回0，若a大返回值大于0，若a小返回值小于0。
* `toString()`：返回大整数十进制的字符串表示
* `toString(radix)`：返回大整数radix进制的字符串表示

可以用Scanner类定义的对象进行控制台读入。例如：

```
Scanner s = new Scanner(System.in);
BigInteger b = s.BigInteger();
```

#### BigDecimal类的实用方法

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/138f3b02d4de8c8146ee81c61b8d7ae1.png)  
 参考来源：  
 [Java高新技术——大数操作（BigInteger、BigDecimal）](https://blog.csdn.net/zhongkelee/article/details/52289163)  
 [BigInteger详解](https://blog.csdn.net/qfikh/article/details/52832196)

### 进制转换

#### 1. 利用Integer进制转换

(1) 10进制转换为 r 进制  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3d6d895fda0f9c8845602f20ff72b8c8.png)  
 (2) r 进制转换为10进制

利用`Integer.parseInt((String) s,(int) radix)`方法将radix进制的字符串s转换为10进制。

参考来源：[JAVA进制转换的几个方法](https://blog.csdn.net/m0_37961948/article/details/80438113)

#### 2. 大数转换

`BigInteger(String val, int radix)`将指定基数的 BigInteger 的字符串表示形式转换为 十进制BigInteger。  
 `toString(radix)`返回大整数radix进制的字符串表示。

### 队列Queue

Queue接口与List、Set同一级别，都继承了Collection。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4e64ce906a37a0801685acbcfa9bebf9.png)  
 LinkedList类实现了Queue接口，因此可以把LinkedList当成Queue来用。  
 **常用方法：**

* `offer`：添加一个元素并返回true（如果队列已满，则返回false）。
* `poll`：移除并返回队列头部的元素（如果队列为空，则返回null）。
* `peek`：返回队列头部的元素（如果队列为空，则返回null）。

```
import java.util.LinkedList;
import java.util.Queue;
 
public class Main
{
    public static void main(String[] args)
    {
        //add()和remove()方法在失败的时候会抛出异常(不推荐)
        Queue<String> queue = new LinkedList<String>();
        //添加元素
        queue.offer("a");
        queue.offer("b");
        queue.offer("c");
        queue.offer("d");
        queue.offer("e");
        for(String q : queue)
        {
            System.out.println(q);
        }
        // for(String s : args)这个格式是foreach的形式，表示取出数组args[]中的每一个元素，每循环一次就依次取出一个元素赋值给s，直到取完为止
        System.out.println("===");
        System.out.println("poll="+queue.poll()); //返回第一个元素，并在队列中删除
        for(String q : queue)
        {
            System.out.println(q);
        }
        System.out.println("===");
        System.out.println("peek="+queue.peek()); //返回第一个元素 
        for(String q : queue)
        {
            System.out.println(q);
        }
    }
}
```

### 输入输出优化

java代码的时间和内存都比C++更多，对于限制条件比较严格的题目很容易超限。  
 参考来源：  
 [JAVA 输入输出优化](https://blog.csdn.net/weixin_43732798/article/details/109804454)  
 [【Java基础】StreamTokenizer使用详解](https://blog.csdn.net/cy973071263/article/details/105588082?spm=1035.2023.3001.6557&utm_medium=distribute.pc_relevant_bbs_down_v2.none-task-blog-2~default~OPENSEARCH~Rate-2.pc_relevant_bbs_down_v2_default&depth_1-utm_source=distribute.pc_relevant_bbs_down_v2.none-task-blog-2~default~OPENSEARCH~Rate-2.pc_relevant_bbs_down_v2_default)

#### 使用StreamTokenizer输入

注意：要`throws IOException`

```
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.StreamTokenizer;

// 实例化
StreamTokenizer st =new StreamTokenizer(new BufferedReader(new InputStreamReader(System.in))); 
 
st.nextToken(); // 获取下一组标记（默认是按照空格分割的，回车、tab是结束符）
int i=(int) st.nval; //st.navl默认解析出的格式是double
 
st.nextToken();     
double j=st.nval; 
 
st.nextToken();     
String s=st.sval;
```

#### 使用StringBuilder和SYSO输出

```
StringBuilder sb = new StringBuilder();
sb.append("answer" + "\n");
System.out.println(sb.toString());
```

---

 【未完待续】