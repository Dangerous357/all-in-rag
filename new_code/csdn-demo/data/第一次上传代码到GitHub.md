# 第一次上传代码到GitHub

以前写代码没有涉及太多对比试验，也没有经历”从无到有“和”从粗略到精细“的过程，所以很少会用到GitHub，现在发现自己的代码版本需要迭代很多次，且需要备份（其实还有一点点原因是yjy在用，效仿一下我的计算机专家男朋友，这样假装我也是专家），所以开始了第一次上次代码到GitHub的尝试，详细的过程记录在此，以便以后随时查阅。

> GitHub是基于git实现的代码托管。  
>  GitHub可以免费使用，并且快速稳定。即使是付费帐户，每个月不超过10美刀的费用也非常便宜。  
>  利用GitHub，你可以将项目存档，与其他人分享交流，并让其他开发者帮助你一起完成这个项目。优点在于，他支持多人共同完成一个项目，因此你们可以在同一页面对话交流。  
>  创建自己的项目，并备份，代码不需要保存在本地或者服务器，GitHub做得非常理想。  
>  学习Git也有很多好处。他被视为一个预先维护过程，你可以按自己的需要恢复、提交出现问题,或者您需要恢复任何形式的代码，可以避免很多麻烦。Git最好的特性之一是能够跟踪错误，这让使用Github变得更加简单。Bugs可以公开，你可以通过Github评论，提交错误。  
>  在GitHub页面，你可以直接开始，而不需要设置主机或者DNS

1 创建仓库
------

### 1.1 登录github

进入github的官方网址：<https://github.com>，点击Sign in登录。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/8fb83618ad9f4c1cad56f493f1dd9881.png)

### 1.2 创建仓库repository

上图左侧有Create repository，点击进入。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/70ae12b91d124e2bbadc00ca66f171c5.png)  
 “Owner”旁边的“Repository name”就是仓库名，是必填项。下面可以选公开还是私有，可以添加Readme、许可等。  
 然后跳转到这个页面：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/4c3b1ff9e2164b63ab4a4f815a747694.png)  
 **使用提示的这些命令需要安装git客户端。**

```
git init //把这个目录变成Git可以管理的仓库
git add README.md //将文件添加到仓库
git add . //不但可以跟单一文件，还可以跟通配符，更可以跟目录。一个点就把当前目录下所有未追踪的文件全部add了 
git commit -m "first commit" //把文件提交到仓库
git remote add origin https://github.com/Dangerous357/Schedule.git //关联远程仓库
git push -u origin main //把本地库的所有内容推送到远程库上
```

2 git下载
-------

### 2.1 Windows

官方下载地址：<https://git-scm.com/downloads>  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/458e2fd7b6344e01ab20a4785d1f7ae3.png)  
 选择Windows：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/c15f911d11054a32956a1e06f71110b4.png)  
 接下来按照提示安装完成后，打开cmd，输入`git -v`，可以输出git版本。（因为我这个电脑安装过，所以没有下载图片里最新版的）  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e4de35ab5474451dac16dd6d993d7531.png)

3 使用
----

### 3.1 绑定用户

```
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱"
```

![我这里输入的是
](https://i-blog.csdnimg.cn/direct/1e3ebb2dd7f24e2aaa01147187b3fdc5.png)

使用下面的命令检查：

```
git config --global --list
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/f367cb9dc33a4120b7977507c21e70f2.png)

### 3.2 本地代码与本地仓库关联

首先进入本地项目的根目录，在该目录下执行`git init`，这会创建一个隐藏的.git/文件夹，使该目录成为一个Git仓库。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/826431b945e749098552d3e10eb18fcd.png)  
 可以通过`git status`查看提交记录和未跟踪文件。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/350570de08974b8081a4a93652c8ace3.png)  
 图中红色的就是未跟踪的文件。

使用`git add .`或`git add 文件或目录名`将对应目录及子目录添加到暂存区（“.”是所有文件的通配符）。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/4d4792edf34d4eb7a47138ff2b46aefe.png)

接下来创建第一次提交，在本地生成一个提交记录。

```
git commit -m "<提交说明>"
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/49fff343c2a24f72b4398650aa6811e9.png)  
 在第一行提示信息中可以看到提交到了master分支上（关于分支后面会有详细介绍）。

### 3.3 本地仓库与远程仓库关联

#### 3.3.1 http方式

之前在GitHub上创建好仓库后，会有自己的仓库地址：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e785313770ac4afa89e1b31375a9d63e.png)  
 仍然是在本地目录使用git remote add <新建远程源名> <HTTPS方式>将远程仓库地址设置为远程源， 并命名。

```
git remote add origin https://github.com/Dangerous357/Schedule.git
```

使用`git remote -v`查看：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/136622e857fc486f96805ccfe9e9d8c3.png)  
 将本地提交推送至远程仓库：

```
git push -u <远程源名> <分支>
```

会提示需要输入用户名密码登录：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/45fca0ed088046b481960bcab5a16496.png)  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/76e96ae57d5c4eaca1e912fab921f867.png)  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/6808b50e9d2f4be7bf3dd2aa48bc3663.png)  
 这里要么就是超时，要么就是连不上：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/50aed72b86e04b1e925dc9b156ee81e2.png)  
 因此我更换为使用SSH的方法配置。

#### 3.3.2 SSH方式

##### （1）密钥生成与设置

> 使用 SSH 方式推送/拉取代码，可以避免每次输入用户名和密码（Token）。

打开本地终端执行：

```
ssh-keygen -t ed25519 -C "你的邮箱@xxxx.com"
```

一路回车，默认会在用户主目录下生成.ssh/id\_ed25519（私钥）和 .ssh/id\_ed25519.pub（公钥）两个文件。

> -t是密钥类型：![这里是引用](https://i-blog.csdnimg.cn/direct/5efd5c0ef15546ffae74f84bc1983b06.png)

生成完成后，windows执行以下命令查看公钥内容（以管理员身份进入终端，注意要到C盘目录下）：

```
more ~\.ssh\id_ed25519.pub
```

linux执行以下命令查看公钥内容：

```
cat ~/.ssh/id_ed25519.pub
```

到GitHub主页右上角头像选择设置：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/a65e3cdc8ffc4a48afda7fcfcfa0f779.png)  
 然后左侧找到SSH and GPG keys进入：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/dbf96e6579204359ae2313c7f4a4f2a0.png)  
 点击New SSH key新增SSH密钥，Title可以自定义，将公钥复制粘贴到下面的文本框中，最后点击Add SSH key确认添加。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e07edaf314654c20a0a8bed2f6eb69d0.png)  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/f544de69956e48859734fccd53c7e8e9.png)  
 这里注意公钥文件里面的全部内容都要复制，不要只复制中间的部分。

最后验证：

```
ssh -T git@github.com
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/60d0c34460db44a8a41c1c1b340b6a2d.png)  
 这里可能网不好需要连接多次噢~

##### （2）将本地仓库与远程仓库连接

之前在GitHub上创建好仓库后，会有自己的仓库地址：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e785313770ac4afa89e1b31375a9d63e.png)  
 仍然是在本地目录使用git remote add <新建远程源名> <SSH方式>将远程仓库地址设置为远程源， 并命名。

```
git remote add origin git@github.com:Dangerous357/Schedule.git
```

我这里需要先删掉之前添加的连接：

```
git remote remove origin
```

使用`git remote -v`查看：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/03df2596fcf34053a4d947064be9cecd.png)  
 将本地提交推送至远程仓库：

```
git branch -a  # 查看分支名
git push -u <远程源名> <分支>
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/09aba3e3f4f1493191440bfffba47431.png)  
 无需输入密码。刷新GitHub可以看到仓库里有代码了。

### 3.4 后续提交

第一次`git push`的时候需要使用`-u`将本地分支与远程分支建立跟踪关系，后续直接使用`git push`即可。如果对代码做了修改，需要先将代码提交到本地仓库，然后按照之前的流程再来一遍。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/3fb5687ed9e84f10b0d84e676cd9a7c9.png)  
 红色的就是需要使用add方法的，变成绿色才可以使用commit方法。

4 其他
----

### 4.1 拉取远程更改

如果远程仓库有了新的提交（多人协作时常见）,在推送之前，可以先拉取远程更新：

```
git pull --rebase <远程源名> <分支>
```

带 --rebase可以保持提交历史线性；不带则会自动创建一个合并提交（Merge commit）。

> 如果你在新建仓库时勾选了“初始化 README”，远程仓库就会自带一个提交记录。这时本地一开始是空的，假如你直接执行git push会被拒绝（提示需先拉取远程更改）。解决方法是先执行：`git pull --rebase <远程源名> <分支>`把远程的那次提交拉下来并合并到本地，然后再git push。

### 4.2 git push time out

可以在Git配置中增加超时时间的设置。例如，修改git config中的http.lowSpeedLimit和http.lowSpeedTime值。例如：

```
git config --global http.lowSpeedLimit 1000
git config --global http.lowSpeedTime 60
```

### 4.3 分支管理

默认情况下是在主分支maste分支上工作，也可以将主分支命名为main，执行：

```
git branch -M main
```

这样与GitHub通用约定保持一致。

如果想开发新功能、修复Bug，通常会新建分支：

```
git checkout -b feature/<新分支名称>
```

开发完成后，切回main分支：

```
git checkout main
```

然后合并分支：

```
git merge feature/<新分支名称>
```

然后删除该分支：

```
git branch -d feature/<新分支名称>
```

5 开源协作
------

1. Fork开源仓库  
    ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/8aa3dec81e8f4b65b6b89433d2da2059.png)
2. 新建分支，填入分支名，如`v1.x`。  
    ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/1cac937e813c4bae9f2cbaeae0bf44ba.png)  
    在终端使用`git remote -v`命令可以查看详情。
3. 拉取上游仓库远程更改：`git pull`。
4. 创建本地分支并关联GitHub远程分支：`git checkout -b v1.0 origin/v1.0`。在GitHub的Codespaces中，新建的云环境相当于已经创建了本地分支。
5. 修改代码。
6. 提交至本地：`git commit -a -m "提交说明"`。
7. 提交至GitHub远程：`git push`。
8. 回到GitHub网页端向上游仓库提交更改。  
    ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/d081e172624449478571cc41db5d8f4f.png)

---

参考来源：  
 @AIGC  
 [手把手教你用git上传项目到GitHub（图文并茂，这一篇就够了），相信你一定能成功！！](https://zhuanlan.zhihu.com/p/193140870)  
 [完整教程：从零开始，学会上传，更新，维护github仓库](https://www.cnblogs.com/ljbguanli/p/18916988)