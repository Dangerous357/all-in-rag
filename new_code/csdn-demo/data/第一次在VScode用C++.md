# 第一次在VScode用C++

文章参考：  
 [【终结】vscode“检测到 #include 错误，请更新 includepath。”的问题解决办法](https://zhuanlan.zhihu.com/p/352958631?ivk_sa=1024320u)  
 [codeblocks安装(自带gcc编译器)](http://t.zoukankan.com/jiu0821-p-9086060.html)  
 [如何用vsCode写C/C++？](https://blog.csdn.net/he_r_o/article/details/103130569)

由于我截图工具不知道为什么坏了，可能需要偷别人几张图……

关于VScode
--------

vscode主要就是写前端的，有些功能不是特别全，后端开发不建议使用。

VScode的C++配置
------------

### 一、下载C/C++插件

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a8e6091f65d6a338ccc715fcd8963578.png)  
 这个就是比较简单，直接搜索插件下载就行

### 二、下载GCC

写C++需要GCC大概是一个小小的常识（因为我比赛的时候总能看到编译环境GCC之类的话，具体我也不清楚），我之前一直用codeblocks写C/C++程序，它好像是内置GCC，所以没怎么配置就可以用，但VScode就不行了。

下载GCC就要先下载MinGW，但是MinGW需要登外网，怎么办？

在网上搜寻了一圈，无果。但我发现由于codeblocks是自带gcc的，可不可以直接用呢？

1. 打开codeblocks，选择settings，compiler settings  
    ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4303d78653b0045792dc716268b8c789.png)  
    由于我截图工具坏了……你看到了吗，MinGW就是我们要的那个文件夹。
2. 配置GCC环境变量。环境变量这个东西已经很熟悉了，先添加一个名为MinGW的系统变量，再在Path中添加C:\MinGW\bin（这个图我不放了，路径别写错就行），然后确认。用命令行检查一下，输入gcc -v，成功。  
    ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/936a34098332ec4505cffae8e5368bab.png)

### 三、配置VS里的环境

1. 在工作空间中创建一个.vscode文件夹。
2. 新建一个tasks.json文件。内容如下：

```
   {
"version": "2.0.0",
"tasks": [{
        "label": "g++",
        "command": "g++",
        "args": [
            "-g",
            "${file}",
            "-o",
            "${fileDirname}/${fileBasenameNoExtension}.exe"
        ],
        "problemMatcher": {
            "owner": "cpp",
            "fileLocation": [
                "relative",
                "${workspaceRoot}"
            ],
            "pattern": {
                "regexp": "^(.*):(\\d+):(\\d+):\\s+(warning|error):\\s+(.*)$",
                "file": 1,
                "line": 2,
                "column": 3,
                "severity": 4,
                "message": 5
            }
        },
        "group": {
            "kind": "build",
            "isDefault": true
        }
    }
]
}
```

3. 新建一个launch.json文件。内容如下：  
    注意miDebuggerPath 这一条，要与GCC安装路径一致，且`在路径中 '\'要替换为'\\'`。

```
    {
"version": "0.2.0",
"configurations": [{
        "name": "(gdb) Launch",    // 配置名称，将会在启动配置的下拉菜单中显示
        "type": "cppdbg",         // 配置类型，这里只能为cppdbg
        "request": "launch",    // 请求配置类型，可以为launch（启动）或attach（附加）
        "program": "${fileDirname}/${fileBasenameNoExtension}.exe",// 将要进行调试的程序的路径
        "args": [],                // 程序调试时传递给程序的命令行参数，一般设为空即可
        "stopAtEntry": false,     // 设为true时程序将暂停在程序入口处，一般设置为false
        "cwd": "${workspaceRoot}",// 调试程序时的工作目录，一般为${workspaceRoot}即代码所在目录
        "environment": [],
        "externalConsole": true,// 调试时是否显示控制台窗口，一般设置为true显示控制台
        "MIMode": "gdb",
        "miDebuggerPath": "C:\\TDM-GCC-64\\bin\\gdb64.exe",// miDebugger的路径，注意这里要与MinGw的路径对应
        "preLaunchTask": "g++",    // 调试会话开始前执行的任务，一般为编译程序，c++为g++, c为gcc
        "setupCommands": [
            {
                "description": "Enable pretty-printing for gdb",
                "text": "-enable-pretty-printing",
                "ignoreFailures": true
            }
        ]
    }
]
}
```

4. （可选）配置运行方式  
    这个步骤的作用是将程序运行在vscode的集成终端上，不会额外弹出一个控制台黑窗口，如下配置：  
    ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/8f572b2b6f8d479f1867c7d93be6285f.png)  
    这个选项我没找到……

### 四、测试配置

随便写个文件，然后运行。**注意在return 0处设置断点，否则好像调试窗口会直接关闭**。断点就是代码左边编号再左边那个红色小圆点。

VScode编码注意事项
------------

1. 中文乱码问题  
    使用printf输出中文时，会出现问题。点击右下角的"UTF-8"，选择“通过编码保存”，输入“GB 2312”，选择“Simplified Chinese(GB 2312)”，将UTF-8转换成GB 2312。  
    ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/09c47ecdad49d4dc9cd6889ae320e4bd.png)  
    [vscode：四个乱码问题及解决方法](https://blog.csdn.net/weixin_50697073/article/details/122789632)