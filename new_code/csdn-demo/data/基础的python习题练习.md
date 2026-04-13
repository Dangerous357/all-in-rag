# 基础的python习题练习

1. 用户输入一个三位自然数，计算并输出其佰位、十位和个位上的数字

```
x = input("请输入一个三位自然数：")
x = int(x)
a = x // 100
b = ( x - a*100 ) // 10
c = x % 10
print(a,b,c)
```

2. 已知三角形的两边长及其夹角，求第三边长。

```
import math
a,b,c = input("请输入两边长及其夹角:").split(',')
a,b,c = float(a),float(b),float(c)
x = a**2 + b**2 - 2 * a * b * math.cos( math.radians(c) )
x = math.sqrt(x)
print(x)
```

*radians()-----将角度转换为弧度  
degrees()-----将弧度转换为角度*

3. 任意输入三个英文单词，按字典顺序输出。

```
x = input("请输入三个英文单词:")
a,b,c = x.split(',')
a,b,c = sorted([a,b,c])
print(a,b,c)
```

4. 计算两点间曼哈顿距离。  
   ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a06de55d7b80f4a99be5698163011b64.png)

```
x = input("请输入x坐标:").split(',')
y = input("请输入y坐标:").split(',')
x = list( map(int,x) )
y = list( map(int,y) )
if len(x) == 2:
    print( abs(x[0]-x[1]) + abs(y[0]-y[1]) )
else:
    sum = 0
    for xi,yi in zip(x,y):
        sum += abs(xi-yi)
    print(sum)
```

5. 统计一个字符串中所有字符在另一个字符串中出现的总次数。

```
knowstr = input("请输入已知字符串：")
goalstr = input("请输入目标字符串：")
sum = 0
for k in knowstr:
    for g in goalstr:
        if k==g:
            sum +=1
print(sum)
```

6. 编写程序，输出所有由1、2、3、4这四个数字组成的素数，并且在每个素数中每个数字只使用一次

```
from itertools import  compress
x = [1,2,3,4]
ans = []
a = []
for i1 in x:
    a.append(i1)
    #ans.append(i1)
    for i2 in x:
        if i2 in a:
            continue
        a.append(i2)
        #ans.append(i1*10+i2)
        for i3 in x:
            if i3 in a:
                continue
            a.append(i3)
            #ans.append(i1 * 100 + i2 * 10 + i3)
            for i4 in x:
                if i4 not in a:
                    ans.append(i1 * 1000 + i2 * 100 + i3 * 10 + i4)
            a.pop()
        a.pop()
    a.pop()
for i in range(0,len(ans)):
    for j in range(2,ans[i]):
        if (ans[i]%j==0):
            ans[i]=0
            break
print(list(compress(ans,ans)))
```

（我不知道是四个数字全用上还是可以用更少的数字，如果不是必须使用，可以把代码里注释掉的地方还原）  
7. 编写程序，实现分段函数计算。

| x | y |
| --- | --- |
| x<0 | 0 |
| 0≤x<5 | x |
| 5≤x<10 | 3x-5 |
| 10≤x<20 | 0.5x-2 |
| 20≤x | 0 |

```
x = input("请输入x:")
x = int(x)
if x<0:
    y = 0
elif 0<=x<5:
    y = x
elif 5<=x<10:
    y = 3*x-5
elif 10<=x<20:
    y = 0.5*x-2
else:
    y = 0
print(y)
```

8. 编写程序，生成包含1000个0~100之间的随机整数，并统计每个元素的出现次数

```
import random
ans = [ random.randint(0,100) for i in range(1000)]
print(ans)
p = []
for i in ans:
    if i not in p:
        print(i,":",ans.count(i))
        p.append(i)
```

9. 编写程序，用户输入一个列表和2个整数作为下标，然后输出列表中介于2个下标之间的元素组成的子列表。例如用户输入[1,2,3,4,5,6]和2，5，程序输出[3,4,5,6]。

```
x = input("请输入一个列表：").split(',')
listx = [ int(i) for i in x]
low = input("请输入起始位置：")
high = input("请输入终止位置：")
print( list(listx[int(low):int(high)+1]) )
```

10. 设计一个字典，并编写程序，用户输入内容作为“键”，然后输出字典中对应的“值”，如果用户输入的“键”不存在，则输出“您输入的键不存在！”

```
a = dict(name='dangerous',age=21,score=100)
x = input("请输入键：")
print(a.get(x,"您输入的键不存在！"))
```

11. 编写程序，生成包含20个随机数的列表，然后将前10个元素升序排列，后10个元素降序排列，并输出结果。

```
import random
a = [random.randint(0,100) for i in range(20)]
a[0:10] = sorted(a[0:10])
a[10:20] = sorted(a[10:20],reverse=True)
print(a)
```

12. 假设有一段英文，其中有单独的字母I误写为i，请编写程序进行纠正。

```
import re
havetext = '''
i would spend the most of my PE lesson to exercise rather than study in class.
While, i just love running, especially the long-distance running 
for it exercises my endurance and perseverance.
'''
p = re.compile(r'\bi\b')
print(p.sub('I',havetext))
```

13. 假设有一段英文，其中有单词中间的字母i误写为I，请编写程序进行纠正。

```
import re
havetext = '''
I would spend the most of my PE lesson to exercIse rather than study In class.
While, I just love runnIng, especially the long-distance running 
for It exercises my endurance and perseverance.
'''
#只替换I而不替换其他字母，要用到子模式扩展语法
p = re.compile('I(?=\w)')#找出I后面带其他字母的单词
havetext = p.sub('i',havetext)
p = re.compile('(?<=\w)I')#找出I前面带其他字母的单词
havetext = p.sub('i',havetext)
#剩下没有替换的就算I前面和后面都没有字母的单词
print(havetext)
```

14. 有一段英文文本，其中有单词连续重复了2次，编写程序检查重复的单词并只保留一个。例如，文本内容为"This is is a desk.“，程序输出为"This is a desk.”。

```
import re
havetext = '''
This is is a desk.
Welcome Welcome to Python.
'''
#因为\w是随机匹配的，要给匹配的值起个名字便于以后使用，即?=word
p = re.compile('(?P<word>\\b\w+[ .])(?=(?P=word))')#用?P=name再一次匹配之前找到的字符串
#只返回第一个字符串，便于直接删去，故第二个字符串用?=
havetext = re.sub(p,'',havetext)
print(havetext)
```

15. 编写程序，用户输入一段英文，然后输出这段英文中所有长度为3个字母的单词。

```
import re
havetext = input("请输入一段英文：")
'''
I would spend the most of my PE lesson to exercIse rather than study In class.While, I just love runnIng, especially the long-distance running for It exercises my endurance and perseverance.
'''
p = re.compile('\\b\w{3}\\b')
print(p.findall(havetext))
```

16. 编写函数，判断一个整数是否为素数，并编写主程序调用该函数。

```
import math


def main(n):
    maxlen = int(math.sqrt(n)) + 1
    for i in range(2, maxlen):
        if n % i == 0:
            return False
    return True


x = input("请输入一个整数：")
x = int(x)
if main(x) is True:
    print("是")
else:
    print("否")
```

17. 编写函数，接收一个字符串，分别统计大写字母、小写字母、数字、其他字符的个数，并以元组的形式返回结果。

```
def main(s):
    ans = [0, 0, 0, 0]
    for i in s:
        if i.isupper() is True:  # 判断大写
            ans[0] += 1
        elif i.islower() is True:  # 判断小写
            ans[1] += 1
        elif i.isdigit() is True:  # 判断数字
            ans[2] += 1
        else:  # 其他
            ans[3] += 1
    return tuple(ans)


x = input("请输入一个字符串：")
print(main(x))
```

18. 编写函数，可以接收任意多个整数并输出其中的最大值和所有整数之和。

```
def main(s):
    s = s.split()
    s = list(map(int, s))
    print("最大值为：", max(s))
    print("所有整数之和为：", sum(s))


x = input("请输入任意多个整数(以空格为分隔符）：")
main(x)
```

19. 编写函数，模拟内置函数sum()。

```
def main(s):
    ans = 0
    for i in s:
        ans += i
    return ans


x = [1, 2, 3, 4, 5]
print(main(x))
x = (6, 7, 8, 9, 10)
print(main(x))
```

20. 编写函数，模拟内置函数sorted()。

```
def main(s, reverse=False):
    if reverse is True:
        for i in range(0, len(s) - 1):
            for j in range(i + 1, len(s)):
                if s[j] > s[i]:
                    temp = s[i]
                    s[i] = s[j]
                    s[j] = temp
    else:
        for i in range(0, len(s)-1):
            for j in range(i+1, len(s)):
                 if s[j] < s[i]:
                     temp = s[i]
                     s[i] = s[j]
                     s[j] = temp
    return s


x = [3, 5, 7, 2, 1, 4, 6, 8]
print(main(x))
x = [3, 5, 7, 2, 1, 4, 6, 8]
print(main(x, True))
```

---

***【新手练习 欢迎指正】***