# 第一次使用Docker（Ubuntu）

#### 文章目录

* [1 简介](#1__1)
* + [1.1 核心概念](#11__2)
  + [1.2 Docker工作流程](#12_Docker_7)
* [2 安装](#2__12)
* [3 启动](#3__38)
* [4 镜像](#4__55)
* + [4.1 拉取](#41__58)
  + [4.2 查看](#42__77)
  + [4.3 标签](#43__84)
  + [4.4 导出和导入](#44__87)
  + [4.5 删除](#45__93)
* [5 容器](#5__98)
* + [5.1 创建](#51__99)
  + [5.2 进入退出](#52__127)
  + [5.3 启动和终止](#53__139)
  + [5.4 查看](#54__149)
  + [5.5 导入和导出](#55__156)
  + [5.6 删除](#56__167)
* [6 Docker Compose](#6_Docker_Compose_173)

1 简介
----

### 1.1 核心概念

1. **容器（Container）** 是Docker技术的核心运行单元，与传统的虚拟机不同，容器不需要模拟完整的硬件环境，也不需要运行独立的操作系统内核。容器在运行时与其他容器和宿主机共享操作系统内核，容器之间相互独立，每个容器都拥有自己的文件系统、网络和进程空间。
2. **镜像（Image）** 是用于创建容器的模板，包含了运行应用所需的代码、库和配置文件，用户可以从Docker Hub下载镜像或自己构建。镜像采用分层存储结构，每一层代表一个修改步骤。镜像中不包含任何的动态数据，其内容在构建之后不再变动。
3. **Dockerfile**是一个文本文件，写明了如何一步步构建镜像，通过执行其中的指令能够自动生成镜像。
4. **镜像仓库（Image Repository）** 是集中存储和分发镜像的地方。最常用的公共仓库是Docker Hub，提供了大量官方和社区维护的镜像。

### 1.2 Docker工作流程

1. 开发者编写Dockerfile定义环境，构建Docker镜像。
2. 将构建好的镜像推送到镜像仓库。
3. 在任何支持Docker的机器上拉取镜像并运行容器。

2 安装
----

使用`cat /etc/os-release`命令查看操作系统信息：“Ubuntu 24.04.3 LTS”。

1. **更新和安装工具**

   ```
   # 更新软件包索引
   sudo apt update

   # 安装必要的依赖工具
   sudo apt install -y \
   	ca-certificates \
   	curl \
   	gnupg \
   	lsb-release \
   	software-properties-common
   ```
2. **安装Moby**

   > 2017年，Docker公司决定将软件产品“Docker”和开源项目“Docker”区分开来，将开源项目“Docker”更名为“Moby”，基于Moby构建Docker社区版和企业版等软件产品。

   安装 Docker的多个组件，包括 Docker 引擎、命令行工具、构建镜像的插件工具、多容器应用的编排管理工具。

   ```
   sudo apt install -y moby-engine moby-cli moby-buildx moby-compose
   ```

   检查安装：

   ```
   docker --version
   ```

3 启动
----

*由于我是在容器化环境下、以“非服务形式”安装的，无需通过`systemctl`启动，可以直接运行。*

```
sudo systemctl enable docker
sudo systemctl start docker
```

使用`docker ps`命令验证。  
 常用的Docker服务命令包括：

| 命令 | 说明 |
| --- | --- |
| `systemctl start docker` | 启动服务 |
| `systemctl stop docker` | 停止服务 |
| `systemctl restart docker` | 重启服务 |
| `systemctl enable docker` | 设置开机启动服务 |
| `systemctl status docker` | 查看服务状态 |

4 镜像
----

Docker 镜像是创建容器的基础模板，包含了运行应用所需的代码、库、环境变量和配置文件，用户可以直接使用现成的镜像，也可以基于现有镜像定制自己的镜像。

> Docker Hub 是 Docker 官方的公共镜像仓库，提供了大量官方和社区维护的镜像。

### 4.1 拉取

```
docker pull [OPTIONS] NAME[:TAG|@DIGEST]
```

* `OPTIONS`（可选）：
  + `--all-tags`/`-a`：下载指定镜像的所有**标签**。镜像标签是用来表示和管理镜像版本的重要工具，通常用于区分不同版本或环境。
  + `--disable-content-trust`：跳过镜像签名验证。
* `NAME`：镜像名称，通常包含注册表地址，不带注册表地址则默认从Docker Hub拉取。
* `TAG`（可选）：镜像标签，默认为`latest`。
* `DIGEST`（可选）：镜像的SHA256摘要。

举例，在Docker Hub中找到想拉取的镜像，从“Tag”中可以看到详细信息：  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/de08cff355d944a6abc0081d0dc6119f.png)  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/53e14c13aaff420cbe54494830568c8b.png)  
 如上图，在命令行中输入：

```
docker pull langchain/langchain:0.1.0
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e21dfa458784446d8ba0f44aaaee0e16.png)

### 4.2 查看

* 使用`docker images`查看本地所有镜像。
* 使用`docker inspect [镜像名(含标签)]`查看镜像的详细信息。  
   ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e7e5bd7d226e4d408bcca55800a5aaa2.png)
* 使用`docker history [镜像名(含标签)]`查看镜像的构建历史。
* 使用`docker system df`查看磁盘使用情况。

### 4.3 标签

使用`docker tag [原镜像名(含标签)] [新镜像名(含标签)]`命令为镜像创建新标签。  
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/689f675a98a840c2887f3b8a1e7edb5d.png)

### 4.4 导出和导入

* **导出**：  
   使用`docker save -o [镜像名].tar [镜像名]`命令将镜像打包成tar文件。
* **导入**：  
   使用`docker load -i [镜像名].tar`命令将镜像导入到Docker中。

### 4.5 删除

使用`docker rmi [镜像名/镜像ID]`命令删除镜像。当镜像有多个标签时，删除一个标签只会移除该标签引用，不会真正删除掉镜像数据，需要使用镜像ID才能彻底删除镜像文件。

Docker使用过程中会基类大量未使用的镜像缓存，通过`docker image prune`命令可以清理没有标签且不被任何镜像引用的悬空镜像，加上`-a`参数还会删除所有未被容器引用的镜像。

5 容器
----

### 5.1 创建

```
docker run [OPTIONS] [IMAGE]
```

*注意：所有参数都放在镜像名前面*

| OPTIONS |  |
| --- | --- |
| `--name [name]` | 指定容器名称 |
| `-it` | 保持交互式终端连接 |
| `-v [主机目录]:[容器目录]` | 将主机的目录挂载到容器中 |
| `--network` | 指定容器的网络模式，设置为`=host`可以让容器共享主机的网络命名空间 |
| `--gpus` | `all`表示分配所有可用的GPU给容器 |
| `-m` | 指定容器最多可以使用的内存，例如`150G` |
| `--oom-kill-disable=true` | 禁用OOM(Out of Memory)杀手 |
| `ulimit memlock` | `=-1`表示不限制内存锁的大小 |
| `ulimit stack` | 线程栈大小限制，例如64MB`=67108864` |
| `shm-size` | 设置容器中共享内存的大小，例如`32GB` |
| `-d` | 以后台模式运行容器 |
| `-p` | 端口映射，格式为`[主机端口号]:[容器端口号]` |
| `--rm` | 容器停止时自动删除容器 |
| `--env [变量名]=[变量值]` `-e [变量名]=[变量值]` | 设置环境变量 |
| `--restart` | 容器的重启策略 |
| `-u [用户名]` | 指定用户运行 |

例如，使用`langchain/langchain:0.1.0`镜像构建容器，指定容器名称为`sweety_cake`。

```
docker run --name sweety_cake  -it -v ~:/workspace --network=host langchain/langchain:0.1.0
```

### 5.2 进入退出

`-it`参数会创建一个bash shell，保持终端的交互连接。

1. **退出**：

   ```
   exit()
   ```
2. **进入**：

   ```
   docker exec -it [容器名/容器ID] /bin/bash
   ```

   在进入前，要保证容器已经在后台运行（启动状态）。

### 5.3 启动和终止

1. **启动**：

   ```
   docker start [容器名/容器ID]
   ```
2. **终止**：

   ```
   docker stop [容器名/容器ID]
   ```

### 5.4 查看

* `docker ps`：查看正在运行的容器。
* `docker ps -a`：查看所有容器，包括已经停止的容器。
* `docker inspect [容器名/容器ID]`：查看容器的详细信息，返回JSON格式数据。
* `docker logs [容器名/容器ID]`：查看容器的日志输出。
* `docker stats`：查看容器的资源使用情况。

### 5.5 导入和导出

1. **导出**：

   ```
   docker export -o [容器名].tar [容器名]
   ```

   将容器的文件系统打包成tar归档文件。
2. **导入**：

   ```
   docker import [容器名].tar [镜像名]:[镜像标签]
   ```

### 5.6 删除

```
docker rm [容器名/容器ID]
```

注意：需要先使用`docker stop`停止容器，或者添加`-f`参数强制删除运行中的容器。

6 Docker Compose
----------------

> Docker Compose是用于定义和管理多容器应用的工具，通过一个YAML文件来配置所有服务配置，用一条命令就能启动这个应用。

常用操作命令：

| 命令 | 说明 |
| --- | --- |
| `docker-compose up -d` | **启动服务**，会在后台启动所有服务。`-d`表示detached模式。 |
| `docker-compose down` | **停止服务**，停止并移除所有容器、网络和卷 |
| `docker-compose ps` | **查看状态**，显示各容器的运行状态 |
| `docker-compose logs` | **查看日志**，输出容器日志，加`-f`可以跟踪实时日志 |
| `docker-compose build` | **构建镜像**，如果服务使用本地Dockerfile，重新构建镜像 |
| `docker-compose restart` | **重启服务**，重启所有服务或指定服务。 |
| `docker-compose start wordpress` | **单服务操作**，可以针对单个服务执行命令 |

---

参考来源：  
 AIGC  
 [**Docker 万字教程：从入门到掌握**](https://mp.weixin.qq.com/s/u2es87JU5FNlGo3qDLY_ng)  
 [Ubuntu 24.04 国内环境下 Docker 安装完整指南](https://juejin.cn/post/7521998095049080895)  
 [对于 Docker 改名 Moby ，大家怎么看？](https://www.zhihu.com/question/58805021)  
 [Docker - 基础docker-compose命令](https://zhuanlan.zhihu.com/p/689723007)  
 [手动下载和导入Docker镜像：全面指南](https://blog.csdn.net/ab13631152127/article/details/142955901)