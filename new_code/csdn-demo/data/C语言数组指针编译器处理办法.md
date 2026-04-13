# C语言数组指针编译器处理办法

发现问题
----

### 背景

这个问题是学长提出的。

### 问题描述

```
#include<stdio.h>
void printPtr(void * ptr)
{
    printf("ptr = %p, *ptr = %016lx\n", ptr, *(long *)ptr);
}
int main(int argc, char const * argv[])
{
    printPtr(argv);
    printPtr(&argv);
    printf("--------------------\n");
    char const * arr[10];
    printPtr(arr);
    printPtr(&arr);
}
```

运行以上代码结果截图：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/bbf6edeab47e29a4be11389d88936c5b.png)  
 为什么同样是指针数组（存放指针的数组）调用函数，argv和&argv的结果不一样，arr和&arr的结果却一样呢？

### 代码解释

1. main函数中的参数类似于JAVA，是命令行输入。
2. %p的用法：以16进制输出某指针的地址。（指针也占一个内存，分配地址空间）
3. %lx的用法：将已知的某整数转换成16进制输出。
4. 定义printPtr()时，指针类型为void，原因是使用void可以把其他类型的指针强制转换。
5. printPtr()函数解释：输出指针ptr的地址、输出指针ptr的内容。
6. main函数中调用printPtr()函数解释：以arr为例，printPtr(arr)中参数是指针arr，printPtr(&arr)中参数是指向arr的无名指针，值是arr的地址，地址是另一个随机地址。

问题解决过程
------

### 两组结果不同的原因

#### 指定数组长度

**问题：** 比较两个指针数组的异同，argv没有指定数组长度，而arr指定了数组长度。  
 **验证：** 指针数组必须初始化，否则会报错。换一种写法，在定义时直接赋值，比较结果。

```
#include<stdio.h>
void printPtr(void * ptr)
{
    printf("\tptr = %p, *ptr = %016lx\n", ptr, *(long *)ptr);
}
int main(int argc, char const * argv[])
{
    printPtr(argv);
    printPtr(&argv);
    printf("\t--------------------\n");
    char const * arr[10];
    printPtr(arr);
    printPtr(&arr);
    printf("\t--------------------\n");
    char a = 'A', b = 'B', c = 'C';
    char *ap = &a, *bp = &b, *cp = &c;
    char const * arr_test[] = {ap, bp, cp};
    printPtr(arr_test);
    printPtr(&arr_test);
}
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a52d1ba9a89517a9437843bbb765f30e.png)  
 **结论：** 大概和定义的方式（是否初始化等）没什么关系。

#### 排除变量类型的影响

**问题：** 注意到例子中是char const类型，是否是char或const独有的特性？  
 **验证：** 变换为int、long等其他形式或改变其const属性后，不影响问题的结果。（过程略）  
 **结论：** 与是否为char、const无关。

#### 数组与普通变量的对比

**问题：** 除了char和const外，注意到问题中定义的两个变量都是指针数组。普通数组、普通指针、普通变量是怎样处理的？  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/055f09ac923acf905ba9cf8cfb0a622c.png)

**验证：** 添加对照组普通数组、普通指针、普通变量。

```
#include<stdio.h>
void printPtr(void * ptr)
{
    printf("\tptr = %p, *ptr = %016lx\n", ptr, *(long *)ptr);
}
int main(int argc, char const * argv[])
{
    printPtr(argv);
    printPtr(&argv);
    printf("\t--------------------\n");
    char const * arr[10];
    printPtr(arr);
    printPtr(&arr);

    printf("\tone:--------------------\n"); // 普通数组
    char arr_test_1_1[10];
    printPtr(arr_test_1_1);
    printPtr(&arr_test_1_1);

    printf("\ttwo:--------------------\n"); // 普通指针
    char a = 'A';
    char * arr_test_1_2 = &a;
    printPtr(arr_test_1_2);
    printPtr(&arr_test_1_2);

    printf("\tthree:--------------------\n"); // 普通变量
    char arr_test_1_3 = 'A';
    printPtr(&arr_test_1_3);
}
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d4a5fd41f413e2b80cabde9868594d67.png)  
 **结论：** 数组（包括普通数组和指针数组）实验中两个结果均相同，普通指针中两个结果不同。结合指针与地址的图示分析（见下图），普通指针结果不同的情况是合理的，对数组出现结果相同的情况存疑。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/40cf0b70181b7d196f74b2456ca19f38.png)

#### 数组定义位置

**问题：** 现在知道了问题的核心出在数组，通过观察原始例子中两个指针数组的异同，发现argv是在函数的参数列表中定义的，而arr是在主函数中定义的，我联想到java对象通过函数传参会生成一个临时对象，类比这里是不是也一样呢？**我认为结果不一样是因为函数调用**。接下来就是验证是否只有在主函数的参数列表中才会导致结果不同，还是所有函数都可以。然后继续解决下面的疑问：根据上一个测验，结果不同才是易被认可的，为什么又会出现结果相同的情况？  
 **验证：** 设置一个对照组test，测试在普通函数的参数列表中是否也会出现这种情况。

```
#include<stdio.h>
void printPtr(void * ptr)
{
    printf("\tptr = %p, *ptr = %016lx\n", ptr, *(long *)ptr);
}
void test(char const * argv[])
{
    printPtr(argv);
    printPtr(&argv);
}
int main(int argc, char const * argv[])
{
    printPtr(argv);
    printPtr(&argv);
    printf("\t--------------------\n");
    char const * arr[10];
    printPtr(arr);
    printPtr(&arr);
    printf("\t--------------------\n");
    char const * arr_test[10];
    test(arr_test);
}
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/44a707c2f432c53bc47ac725afbe031f.png)  
 **结论：** 同样是在主函数中声明的指针数组，经传参使结果变得不一样。因此大胆假设，主函数中的参数不是定义，而是另一种形式的调用，可能最初的定义在命令行中，其本质和普通函数的调用类似。  
 学长告诉我，但凡变量声明应该都是会向操作系统申请内存（这就是我猜测的生成临时变量占用内存空间，因为没学过C的形参占不占空间），被调函数的形参是一个局部变量，用主调函数的实参为其初始化。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/12c1648cd51f852378261d14d27d39ec.jpeg)

学长的疑问在于“C默认提供的这个数组和用户自定义的数组，编译器对他们二者在地址输出操作上的效果不同”，我在上面实验的基础上，持不同意见，认为“根本原因不是C默认和用户自定义，**结果不同是经过函数调用的必然结果**”。

#### 数组的地址怎么表示

**问题：** 出于数组的特殊性，我对数组地址的表示法产生了疑问。对于一个数组a[]，我们可以用a表示它的首地址&a[0]（常识），&a是合法的，但&(&a[0])却不合法。学长说不能对地址再取地址，那为什么&a合法？是不是可以理解为a是在你声明数组时，系统自动帮你给数组a[]声明的新变量，为了你用起来方便？  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/95baf15c6224b2b2e0b006a3efa58b96.jpeg)

### 数组表示法

因为封校原因，我没办法及时问老师。第二天，学长对数组地址的表示给出了解释。

```
#include<stdio.h>
void printPtr(void * ptr)
{
    printf("\tptr = %p, *ptr = %016lx\n", ptr, *(long *)ptr);
}
int main(int argc, char const * argv[])
{
    printPtr(argv);
    printPtr(&argv);
    printf("\t--------------------\n");
    char const * arr[10];
    printPtr(arr);
    printPtr(&arr);
    printf("\t--------------------\n");
    printPtr(&arr[0]);
    printPtr(arr);
    printPtr(&arr);
    printPtr(arr+1);
    printPtr(&arr+1);

}
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a67d143ab145f2c50134c1189b803546.png)  
 **结论：** &arr[0]和arr都可以表示数组arr[]的首地址，且二者等价。但&arr的含义却不是指针arr的地址（也可以理解为根本没有arr这个指针，是编译器为了你方便给你提供的语法），&arr表示这整个数组的地址。看上面的代码（arr+1是arr向后移动一个位置，&arr +1同理），所以使用printPtr输出参数的地址，arr+1和arr相差4位，而&arr和&arr+1相差40位。（说明：一个指针变量在内存中占4个字节，所以arr+1相当于&arr[1]，与arr即&arr[0]相差4；&arr+1和&arr相差整个数组的大小，本例中数组大小为10\*4，所以结果中输出的地址F00-EDC=40）  
 虽然arr和&arr的数值是一样的，但是本质上arr是一个指针，表示这个数组，指向数组首地址，而&arr就是这证个数组的地址，它们的类型不一样。所以给`test(char const * arr[])`传参的时候，要想传入整个数组，我们传的是arr或&arr[x]。  
 这就可以解释为什么上面对于数组地址表示的疑问。总之，**arr=&a[0]，但&arr不表示arr的地址**。

总结
--

最开始的问题：

```
#include<stdio.h>
void printPtr(void * ptr)
{
    printf("ptr = %p, *ptr = %016lx\n", ptr, *(long *)ptr);
}
int main(int argc, char const * argv[])
{
    printPtr(argv);
    printPtr(&argv);
    printf("--------------------\n");
    char const * arr[10];
    printPtr(arr);
    printPtr(&arr);
}
```

### 为什么会结果相同

对于数组arr[]，arr表示的是数组arr的首地址（即&arr[0]），而&arr表示的是这整个数组的地址（包含数组的所有元素），值与数组首地址相同。

### 经函数调用后为什么又结果不同

```
#include<stdio.h>
void printPtr(void * ptr)
{
    printf("\tptr = %p, *ptr = %016lx\n", ptr, *(long *)ptr);
}
void test(char const * argv[])
{
    printPtr(argv);
    printPtr(&argv);
    printPtr(argv+1);
}
int main(int argc, char const * argv[])
{
    printPtr(argv);
    printPtr(&argv);
    printf("\t--------------------\n");
    char const * arr[10];
    printPtr(arr);
    printPtr(&arr);
    printf("\t--------------------\n");
    printPtr(&arr[0]);
    printPtr(arr);
    printPtr(&arr);
    printPtr(arr+1);
    printPtr(&arr+1);
    printf("\t--------------------\n");
    test(arr);
    printf("\t.....\n");
    test(&arr[0]);
    printf("\t.....\n");
    test(&arr[1]);
    printf("\t.....\n");
}
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f4c8b62130ac75f84666608c500967c1.png)  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c86e5f6b1fae0620688dfdedd16fcf8e.png)  
 形参相当于定义了一个指向原变量的指针，然后又找个地方存放这个指针。所以对于形参argv，有argv等于arr，其内容等于arr的内容，地址等于arr的地址；也有&argv，其内容为argv指向的数据结构的地址（即arr的地址），地址等于argv指针自己真实所占的地址空间。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6a47e5a65b6ae64fe9928c00903cd88d.jpeg)  
 以上推论可能有不严谨的部分，绝大多数是我们根据自己的猜想和验证得出的（他挺严谨的，最后一个关键问题的答案是他找到的然后告诉我，如果有问题大概是我自己理解的偏差）。  
 他参考的文章有：  
 <https://www.youtube.com/watch?v=ASVB8KAFypk>  
 <https://www.log2base2.com/C/pointer/array-and-pointer-in-c.html>  
 <https://www.log2base2.com/C/pointer/arr+1-vs-address-of-arr+1.html>  
 <https://stackoverflow.com/questions/71736085/why-are-the-two-lines-of-output-in-the-main-function-the-same-c-language>

---

*【欢迎指正】*