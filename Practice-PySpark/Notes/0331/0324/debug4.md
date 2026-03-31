我帮你把这页内容整理成 **清晰 + 可打印版（结构化）**👇

---

# 🧠 2.1 课程服务器环境（整理版）

## 📌 一、整体说明

本课程使用 **3台 Linux 虚拟机服务器** 来学习大数据集群。

---

## 🖥️ 二、三台机器角色分配

### ✅ node1（主节点）

* Master：

  * HDFS（NameNode）
  * YARN（ResourceManager）
  * Spark（Master）
* 同时也是 Worker：

  * HDFS
  * YARN
  * Spark

👉 **一句话：主控 + 计算都在 node1**

---

### ✅ node2（从节点）

* Worker：

  * HDFS
  * YARN
  * Spark

👉 **纯计算节点**

---

### ✅ node3（从节点 + Hive）

* Worker：

  * HDFS
  * YARN
  * Spark
* 额外：

  * Hive

👉 **计算 + 数据仓库**

---

## 📊 三、整体架构（你面试可以这样说）

👉 一个 Master + 两个 Worker 的经典分布式架构：

```
        node1 (Master + Worker)
           /           \
      node2           node3
    (Worker)        (Worker + Hive)
```

---

## ⚙️ 四、环境搭建方式（2种）

### 方式1：自己搭建

* 自己创建 3 台 Linux 虚拟机
* 手动部署集群

#### 要求：

* ✅ Hadoop 集群（HDFS + YARN）

  * 版本 ≥ Hadoop 3.x
* ✅ JDK 1.8
* ✅ OS：CentOS 7（推荐 7.6）

---

### 方式2：使用课程提供虚拟机（推荐）

* 已提供 3 台虚拟机压缩包
* 直接导入 VMware 使用

#### 要求：

* ✅ VMware Workstation ≥ 15
* ✅ 网络：192.168.88.x 网段

---

## 🎯 五、面试重点总结（超重要）

👉 面试官最爱问：

### ⭐ 为什么这样设计？

* Master 负责：

  * 调度（YARN）
  * 元数据（HDFS）
* Worker 负责：

  * 计算任务执行

---

### ⭐ 为什么 node1 也做 Worker？

👉 提高资源利用率（不浪费机器）

---

### ⭐ Hive 为什么单独放 node3？

👉 避免影响 Master，分离计算和查询负载

---

## 🧾 一句话总结（面试版）

👉
**“This is a typical Hadoop + Spark cluster with one master node and multiple worker nodes, where the master handles scheduling and metadata, and workers handle distributed computation.”**

---

如果你要，我可以帮你做👇
✅ 一页 A4「Spark + Hadoop 架构速记图」
✅ AWS Data Platform 对应（S3 + EMR + Glue）
✅ 面试 10 个高频问题 + 答案

直接说：**要面试版 / 要AWS版** 👍


我帮你把这份 **Spark课件（前3章核心）压缩成一套“面试 + 学习双用知识体系”**，你可以直接当笔记背👇

---

# 🧠 Spark课件核心知识点（精华版）

（基于你上传的PDF整理 ）

---

# 🚀 一、Spark是什么（最重要开场）

### ✅ 定义（必须会背）

👉
**Spark = 大规模数据的统一分布式计算引擎**

---

### ✅ 核心本质

* 基于 **RDD（分布式数据抽象）**
* 支持：

  * 批处理
  * 流处理
  * SQL
  * 机器学习

📌 关键词：

* in-memory（内存计算）
* distributed（分布式）
* unified（统一引擎）

---

# ⚔️ 二、Spark vs Hadoop（面试必问）

| 对比   | Hadoop (MR) | Spark      |
| ---- | ----------- | ---------- |
| 计算方式 | 磁盘          | 内存         |
| 性能   | 慢           | 快（10~100倍） |
| 编程   | MapReduce   | RDD API    |
| 执行   | 进程          | 线程         |
| 适合   | 离线          | 批 + 实时     |

---

### ⭐ 本质区别一句话：

👉
**Hadoop = 磁盘计算
Spark = 内存计算**

---

# ⚡ 三、Spark四大特点（必背）

1. **速度快**

   * 内存计算 + DAG 

2. **易用**

   * 支持 Python / Java / SQL

3. **通用性强**

   * SQL + Streaming + ML + Graph

4. **运行灵活**

   * Local / Standalone / YARN / K8s

---

# 🧩 四、Spark核心模块（架构）

```
Spark Core（基础）
 ├── Spark SQL（结构化）
 ├── Streaming（流处理）
 ├── MLlib（机器学习）
 └── GraphX（图计算）
```

👉 核心：**所有都基于 Spark Core**

---

# 🏃 五、Spark运行模式（重点）

### 1️⃣ Local（单机）

* 一个进程 + 多线程
* 用于学习

---

### 2️⃣ Standalone（集群）

* Spark 自带集群

---

### 3️⃣ YARN（最常用）

* 运行在 Hadoop 上

---

### 4️⃣ Kubernetes

* 云原生部署

---

# 👷 六、Spark核心角色（高频面试）

| 角色       | 作用       |
| -------- | -------- |
| Master   | 管理集群     |
| Worker   | 提供资源     |
| Driver   | 程序入口（大脑） |
| Executor | 执行任务     |

---

### ⭐ 面试一句话：

👉
**Driver负责调度，Executor负责执行**

---

# 🔄 七、Spark执行流程（非常重要）

### 一条完整流程：

1️⃣ 创建 SparkContext
2️⃣ 连接集群
3️⃣ 分配 Executor
4️⃣ 切分 Job → Stage → Task
5️⃣ Executor 执行任务

---

### ⭐ 层级关系（必考）

```
Application
 └── Job
      └── Stage
           └── Task
```

📌 记住：

* **Task = 最小单位**
* **Partition数 = Task数**

---

# 🧱 八、Standalone集群结构（你刚问的）

```
Master（资源管理）
   ↓
Worker（资源提供）
   ↓
Executor（执行任务）
   ↓
Task（线程执行）
```

---

# 🧪 九、Local模式核心原理（高频）

👉 本质：

**一个 JVM 进程 + 多线程模拟集群** 

---

### 特点：

* Driver = Executor
* 没有真正分布式
* 用线程跑 Task

---

# 🌐 十、Spark Web UI（面试必问）

| 端口    | 作用     |
| ----- | ------ |
| 4040  | 当前任务   |
| 8080  | Master |
| 18080 | 历史记录   |

---

# 🔥 十一、经典代码（一定会考）

```python
sc.parallelize([1,2,3,4,5]) \
  .map(lambda x: x + 1) \
  .collect()
```

👉 流程：

* parallelize → RDD
* map → 转换
* collect → action（触发执行）

---

# 🧠 十二、最核心总结（面试速答）

### ⭐ Spark解决什么问题？

👉
**大规模数据计算（批处理 + 实时）**

---

### ⭐ 为什么Spark快？

👉
**内存计算 + DAG优化**

---

### ⭐ Spark核心结构？

👉
**Driver + Executor + Task**

---

### ⭐ Spark最重要抽象？

👉
**RDD**

---

# 🧾 一页终极总结（建议背）

👉
**Spark is a distributed in-memory computing engine that uses RDD abstraction and DAG execution to process large-scale data efficiently.**

---

# 🚀 如果你下一步想冲面试（建议）

我可以帮你继续做👇

### 1️⃣ Spark面试高频50题

### 2️⃣ AWS Data Platform对应（S3 + EMR + Glue）

### 3️⃣ Spark执行流程图（超清一页）

### 4️⃣ PySpark常见坑（你已经踩过的我帮你总结）

直接说：**要面试版 / 要AWS版 / 要速记表** 👍



我帮你把这段代码整理成 **面试级理解（极简 + 能讲清）**👇

---

# 🧠 1. 这段代码在做什么？

👉 一句话：

**创建RDD → 查看分区 → 执行计算 → 收集结果**

---

# 📥 2. Input / Output

### Input

```python
[1,2,3,4,5,6,7,8,9]
[1,2,3]
```

### Output（示例）

```text
默认分区数:  8   # 取决于CPU核数
分区数:  3
rdd的内容是:  [1, 2, 3]
```

---

# ⚠️ 3. 关键概念（面试重点）

## ✅ 1）SparkContext

```python
sc = SparkContext(conf=conf)
```

👉 Spark程序入口（Driver）

---

## ✅ 2）parallelize

```python
sc.parallelize(data, numPartitions)
```

👉 作用：

* 本地数据 → 分布式RDD

---

## ✅ 3）分区（Partition）

```python
rdd.getNumPartitions()
```

👉 规则：

* 不指定 → **CPU核心数**
* 指定 → 用你给的

---

## ✅ 4）collect（⚠️高危操作）

```python
rdd.collect()
```

👉 作用：

* 分布式 → Driver（本地List）

---

# 🚨 4. 面试最重要的点（必讲）

## ❗ collect为什么危险？

👉
**会把所有数据拉到Driver内存**

* 小数据 ✅
* 大数据 ❌（OOM）

---

# 🧠 5. 执行流程（必须会讲）

```text
Driver
  ↓
RDD（分布式）
  ↓
分区（Partition）
  ↓
Task（线程执行）
  ↓
collect → 回到Driver
```

---

# ⚙️ 6. local[*] 是什么？

```python
.setMaster("local[*]")
```

👉
**使用所有CPU核心运行**

等价于：

```text
线程数 = CPU cores
```

---

# 💡 7. 分区和Task关系（高频）

👉
**1 Partition = 1 Task**

---

# 🧪 8. Dry Run（一步步）

```python
rdd = sc.parallelize([1,2,3], 3)
```

👉 变成：

```text
Partition 1 → [1]
Partition 2 → [2]
Partition 3 → [3]
```

---

```python
rdd.collect()
```

👉 执行：

```text
Task1 → 1
Task2 → 2
Task3 → 3
```

👉 Driver收集：

```text
[1,2,3]
```

---

# 🧾 9. 面试一句话总结（直接背）

👉
**parallelize creates distributed RDD from local data, partitions determine parallelism, and collect brings data back to driver which can cause memory issues.**

---

# 🔥 10. 面试 follow-up（你一定会被问）

### Q1：如何优化分区？

👉

* 根据数据量
* 一般：CPU * 2~3

---

### Q2：collect替代方案？

👉

* take()
* foreach()
* saveAsTextFile()

---

### Q3：为什么分区重要？

👉
**决定并行度 + 性能**

---

# 🚀 如果你要更强一版（推荐）

我可以帮你补👇
✅ 这段代码对应的 **Spark执行DAG图**
✅ 10个 PySpark 面试坑（你已经踩到 collect了）
✅ AWS EMR 对应执行流程

直接说：**要面试强化版** 👍


可以，用 Docker 很适合**本地模拟 3 个 Linux 节点**。
但先说结论：

# 结论

你要的“三个 node”有两种层次：

## 方案 A：只为了学 Spark / Hadoop 架构

最简单：
**3 个 Docker 容器 + 同一个自定义网络**
每个容器起个名字：

* node1
* node2
* node3

这样它们就像 3 台机器，可以互相 ping、ssh、跑进程。

## 方案 B：真的模拟课程里那种 3 节点集群

需要在 3 个容器里继续装：

* Java
* SSH
* Hadoop
* Spark
* 可能还有 Hive / Zookeeper

这个能做，但比虚拟机更折腾，因为：

* 容器默认不是完整 OS
* systemd/service 管理不自然
* SSH、hostname、持久化、权限都要手动配

所以：

**如果你目标是学习 Spark 概念和提交作业，Docker 可以。**
**如果你目标是一比一照课件搭完整 Hadoop + Spark + Hive HA 环境，虚拟机更稳。**

---

# 最小可行方案：先搭 3 个 Docker 节点

---

## 1. 先创建 Docker 网络

```bash
docker network create spark-net
```

这相当于给这 3 个节点一个局域网。

---

## 2. 启动 3 个容器

用 Ubuntu 先模拟最简单。

```bash
docker run -dit --name node1 --hostname node1 --network spark-net ubuntu:22.04 bash
docker run -dit --name node2 --hostname node2 --network spark-net ubuntu:22.04 bash
docker run -dit --name node3 --hostname node3 --network spark-net ubuntu:22.04 bash
```

说明：

* `--name`：容器名
* `--hostname`：容器内看到的主机名
* `--network spark-net`：都放到同一个网络里
* `-dit`：后台运行

---

## 3. 进入容器

```bash
docker exec -it node1 bash
docker exec -it node2 bash
docker exec -it node3 bash
```

---

## 4. 安装基础工具

每个容器里都执行：

```bash
apt update
apt install -y openjdk-8-jdk openssh-server openssh-client vim net-tools iputils-ping procps
```

如果你课程要求 JDK 1.8，这样更贴近课件。

---

## 5. 测试三台机器互通

在 node1 里：

```bash
ping node2
ping node3
```

如果通了，说明 3 个“节点”已经模拟出来了。

---

# 更推荐：用 docker-compose 一次起 3 个 node

这样更方便管理。

## docker-compose.yml

```yaml
version: '3.8'

services:
  node1:
    image: ubuntu:22.04
    container_name: node1
    hostname: node1
    tty: true
    stdin_open: true
    command: bash
    networks:
      - spark-net

  node2:
    image: ubuntu:22.04
    container_name: node2
    hostname: node2
    tty: true
    stdin_open: true
    command: bash
    networks:
      - spark-net

  node3:
    image: ubuntu:22.04
    container_name: node3
    hostname: node3
    tty: true
    stdin_open: true
    command: bash
    networks:
      - spark-net

networks:
  spark-net:
    driver: bridge
```

启动：

```bash
docker compose up -d
```

进入：

```bash
docker exec -it node1 bash
```

---

# 如果你想继续做成“像课件那样的三节点”

你下一步要补这几个东西：

## node1

* HDFS NameNode
* YARN ResourceManager
* Spark Master
* 也可以兼 Worker

## node2

* HDFS DataNode
* YARN NodeManager
* Spark Worker

## node3

* HDFS DataNode
* YARN NodeManager
* Spark Worker
* Hive

---

# Docker 里搭三节点的关键点

## 1. 固定节点名

Hadoop / Spark 很依赖 hostname。
所以 `node1/node2/node3` 要固定。

## 2. SSH

很多 Hadoop/Spark 脚本默认依赖 SSH 分发或远程启动。
你需要在容器里开 sshd。

### 安装后初始化：

```bash
mkdir /var/run/sshd
echo 'root:123456' | chpasswd
sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
/usr/sbin/sshd
```

## 3. Java

Spark/Hadoop 必须有 Java。

```bash
java -version
echo $JAVA_HOME
```

## 4. 时间 / 挂载目录

你最好挂载数据目录，不然容器删了数据就没了。

---

# 更实际的做法：自己做一个基础镜像

你可以先做一个带 Java + SSH 的基础镜像，再复制出 3 个节点。

## Dockerfile

```dockerfile
FROM ubuntu:22.04

RUN apt update && apt install -y \
    openjdk-8-jdk \
    openssh-server \
    openssh-client \
    vim \
    net-tools \
    iputils-ping \
    procps \
    rsync

RUN mkdir /var/run/sshd

RUN echo 'root:123456' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

CMD ["/usr/sbin/sshd", "-D"]
```

构建：

```bash
docker build -t spark-node:1.0 .
```

然后起 3 个：

```bash
docker run -dit --name node1 --hostname node1 --network spark-net spark-node:1.0
docker run -dit --name node2 --hostname node2 --network spark-net spark-node:1.0
docker run -dit --name node3 --hostname node3 --network spark-net spark-node:1.0
```

---

# 你真正需要理解的本质

Docker 模拟三节点，本质上是：

* **3 个独立容器**
* 每个容器有自己的 hostname、进程空间、文件系统
* 放在同一个 Docker 网络里互联

所以它们就能扮演：

* node1
* node2
* node3

虽然它们都跑在你一台 Mac 上，但逻辑上已经是 3 台机器。

---

# 这个方案的优缺点

## 优点

* 启动快
* 删除重建方便
* 节省内存
* 很适合练 hostname / 网络 / 分布式部署概念

## 缺点

* 不像真实 VM 那么完整
* 某些 Hadoop/Hive 脚本不如 VM 顺手
* systemd/service 管理麻烦
* 课程如果按 CentOS 7 写，Ubuntu 容器会有差异

---

# 最适合你的建议

你现在有两个方向：

## 方向 1：先理解概念，快速上手

用 Docker 起 3 个节点就够了。

## 方向 2：完全跟课件一步步做

直接用 VMware 三台 Linux 虚拟机，更接近课件环境。

---

# 给你的最短建议

如果你现在只是问“如何模拟三个 node”：

```bash
docker network create spark-net

docker run -dit --name node1 --hostname node1 --network spark-net ubuntu:22.04 bash
docker run -dit --name node2 --hostname node2 --network spark-net ubuntu:22.04 bash
docker run -dit --name node3 --hostname node3 --network spark-net ubuntu:22.04 bash
```

这就已经完成了 **3-node 模拟**。

---

如果你愿意，我下一条可以直接给你一套
**“Mac 上用 Docker 搭 node1/node2/node3 + Java + SSH 的完整可复制命令版”**。


短答案：
👉 **不会，比虚拟机更流畅，明显更轻。**

---

# 🧠 1. Docker vs 虚拟机（你这个场景）

| 对比       | Docker（容器） | 虚拟机（VMware） |
| -------- | ---------- | ----------- |
| 启动速度     | 秒级         | 分钟级         |
| 内存占用     | 低（共享宿主机）   | 高（每台独立OS）   |
| CPU开销    | 小          | 大           |
| 卡顿概率     | 低          | 高           |
| 你现在Mac体验 | 👍 流畅      | 😭 容易卡      |

---

# 🚨 2. 你的情况（重点）

你现在是：

👉 M1 Mac + 已经感觉卡

再开 3 台虚拟机：

👉 **100% 会更卡**

原因：

* 每台 VM 至少 2GB 内存
* 3 台 = 6GB+
* 再加 Chrome / PyCharm / Spark
  👉 直接爆

---

# ⚡ 3. Docker为什么更轻？

👉 本质区别：

### 虚拟机

```text
Mac
 └── VM1（完整Linux）
 └── VM2（完整Linux）
 └── VM3（完整Linux）
```

👉 每个都是一个完整系统 ❌

---

### Docker

```text
Mac
 └── Docker Engine
      ├── node1（共享内核）
      ├── node2（共享内核）
      └── node3（共享内核）
```

👉 共用一个内核 ✔️

---

# 📊 4. 实际资源对比（真实经验）

| 场景       | 内存         |
| -------- | ---------- |
| 3台VM     | 6GB ~ 10GB |
| 3个Docker | 1GB ~ 2GB  |

👉 差一个数量级

---

# ⚠️ 5. 但有一个坑（你要知道）

Docker不会卡，但：

👉 **Hadoop + Spark + Hive + SSH 全开**
仍然会吃资源

---

# 🧠 6. 推荐你最优方案（很关键）

## ✅ 最舒服（推荐）

👉 Docker + 只跑 Spark（先学）

---

## ❗ 中等

👉 Docker + Spark + Hadoop（OK）

---

## ❌ 不推荐你现在

👉 Docker + Hadoop + Hive + HA + ZK

👉 对你当前电脑 = 会卡

---

# 🎯 7. 最佳实践（给你定一个标准）

### 你的 Mac（M1）

👉 建议配置：

```text
Docker Desktop:
Memory: 4GB
CPU: 4 cores
```

---

### 容器数量建议：

| 场景     | 建议    |
| ------ | ----- |
| 学Spark | 1~2容器 |
| 模拟集群   | 3容器   |
| 全家桶    | ❌     |

---

# 🧾 8. 一句话总结（面试 + 实战）

👉
**Docker is much lighter than VMs because containers share the host OS kernel, while VMs run full OS instances.**

---

# 🚀 9. 给你一个真实建议（很重要）

你现在目标是：

👉 学 Spark + AWS Data Platform

其实：

👉 ❗你根本不需要 3 台机器

---

## 更聪明的路径：

### Step 1

👉 local[*] 学Spark（你已经在做了）

### Step 2

👉 Docker模拟1个节点（理解）

### Step 3

👉 AWS EMR / Glue（真实环境）

---

# 🔥 最关键一句话（帮你避坑）

👉
**面试官不会问你“你能不能搭3台虚拟机”，只会问你“Spark怎么运行”。**

---

如果你要，我可以帮你👇

✅ 给你一个 **最省资源 Docker三节点模板（不会卡）**
✅ 或直接帮你画 **Spark执行流程（面试100%问）**
✅ 或告诉你 **Spark怎么映射到AWS（你入职最有用）**

直接说：
👉 **要轻量版 / 要面试版 / 要AWS版** 👍



可以，下面我直接给你一套 **Mac 上用 Docker 模拟 3 个 node** 的最具体步骤。
目标是先做到这件事：

* 起 3 个容器：`node1` `node2` `node3`
* 它们在同一个网络里
* 每个容器都能互相通信
* 每个容器里有基础 Linux 工具 + Java + SSH
* 你后面可以继续在上面装 Spark / Hadoop

---

# 先说结果

做完后你会有：

* `node1`
* `node2`
* `node3`

然后你可以在 `node1` 里执行：

```bash
ping node2
ping node3
ssh node2
ssh node3
```

如果都通，就说明你已经用 Docker 模拟出 3 台“机器”了。

---

# 第 0 步：先准备 Docker Desktop

如果你还没装 Docker Desktop，先安装并打开它。
打开后，在终端先验证：

```bash
docker --version
docker compose version
```

如果都能输出版本号，就可以继续。

---

# 第 1 步：创建一个工作目录

在终端执行：

```bash
mkdir -p ~/docker-spark-3nodes
cd ~/docker-spark-3nodes
```

---

# 第 2 步：创建 Dockerfile

在这个目录里新建一个文件，名字叫：

```bash
Dockerfile
```

把下面内容完整复制进去：

```dockerfile
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    openjdk-8-jdk \
    openssh-server \
    openssh-client \
    vim \
    nano \
    net-tools \
    iputils-ping \
    procps \
    rsync \
    curl \
    wget \
    && apt clean

RUN mkdir /var/run/sshd

RUN echo 'root:123456' | chpasswd

RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config || true
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config || true
RUN echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config
RUN echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

CMD ["/usr/sbin/sshd", "-D"]
```

---

# 第 3 步：创建 docker-compose.yml

在同一个目录下，新建文件：

```bash
docker-compose.yml
```

把下面内容完整复制进去：

```yaml
services:
  node1:
    build: .
    container_name: node1
    hostname: node1
    networks:
      spark-net:
        ipv4_address: 172.28.0.11

  node2:
    build: .
    container_name: node2
    hostname: node2
    networks:
      spark-net:
        ipv4_address: 172.28.0.12

  node3:
    build: .
    container_name: node3
    hostname: node3
    networks:
      spark-net:
        ipv4_address: 172.28.0.13

networks:
  spark-net:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16
```

---

# 第 4 步：启动 3 个节点

在当前目录执行：

```bash
docker compose up -d --build
```

第一次会稍微慢一点，因为要下载镜像和安装软件。

启动后检查：

```bash
docker ps
```

你应该能看到：

* node1
* node2
* node3

都在运行。

---

# 第 5 步：进入 node1

```bash
docker exec -it node1 bash
```

进去后先看 hostname：

```bash
hostname
```

应该输出：

```bash
node1
```

再测试 Java：

```bash
java -version
```

再测试网络：

```bash
ping -c 2 node2
ping -c 2 node3
```

如果能收到响应，说明 3 个节点网络通了。

---

# 第 6 步：在 3 个节点里配置免密 SSH

这一步很关键。
很多 Hadoop / Spark 脚本都喜欢用 SSH。

## 6.1 在 node1 里生成密钥

先确保你还在 `node1` 容器里：

```bash
docker exec -it node1 bash
```

执行：

```bash
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

先测试本机 ssh：

```bash
ssh -o StrictHostKeyChecking=no root@node1
```

如果能进去，输入：

```bash
exit
```

---

## 6.2 把 node1 的公钥复制到 node2 和 node3

先把公钥打印出来：

```bash
cat ~/.ssh/id_rsa.pub
```

复制整行输出。

然后进入 node2：

```bash
docker exec -it node2 bash
```

执行：

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
```

把刚才复制的公钥追加进去：

```bash
echo '这里替换成你刚才复制的整行公钥' >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
exit
```

再进入 node3：

```bash
docker exec -it node3 bash
```

执行：

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo '这里替换成你刚才复制的整行公钥' >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
exit
```

---

## 6.3 回到 node1 测试 ssh 到另外两台

进入 node1：

```bash
docker exec -it node1 bash
```

测试：

```bash
ssh -o StrictHostKeyChecking=no root@node2
```

如果成功，输入：

```bash
exit
```

再测：

```bash
ssh -o StrictHostKeyChecking=no root@node3
```

如果也成功，就说明 3-node + SSH 已经搭好了。

---

# 第 7 步：给三个节点都准备 hosts（可选但推荐）

虽然 Docker 自带 DNS，通常 `node1/node2/node3` 已经能解析。
但你要更像课程环境，可以加 `/etc/hosts`。

分别进入三个节点，把下面内容追加进去：

```bash
cat >> /etc/hosts <<EOF
172.28.0.11 node1
172.28.0.12 node2
172.28.0.13 node3
EOF
```

可以在每台里执行：

```bash
ping -c 2 node1
ping -c 2 node2
ping -c 2 node3
```

---

# 第 8 步：检查你现在已经有什么

现在你的 Docker 三节点已经具备：

* 3 个独立节点
* 固定 hostname
* 同网段通信
* Java 1.8
* SSH 服务
* node1 可 ssh 到 node2/node3

这已经足够模拟课程里的三台 Linux 机器。

---

# 第 9 步：常用管理命令

## 查看运行状态

```bash
docker ps
```

## 停止

```bash
docker compose down
```

## 重新启动

```bash
docker compose up -d
```

## 删除并重建

```bash
docker compose down -v
docker compose up -d --build
```

---

# 第 10 步：接下来怎么映射到课件

你课件里那种分工是：

* `node1`: Master + Worker
* `node2`: Worker
* `node3`: Worker + Hive

你现在已经完成了机器层面的模拟。
后面只是“往机器里装东西”：

## node1

* Hadoop NameNode
* YARN ResourceManager
* Spark Master

## node2

* Hadoop DataNode
* YARN NodeManager
* Spark Worker

## node3

* Hadoop DataNode
* YARN NodeManager
* Spark Worker
* Hive

---

# 最短验证清单

你把下面这几个都跑通，就算成功：

在宿主机：

```bash
docker ps
```

在 node1：

```bash
hostname
java -version
ping -c 2 node2
ping -c 2 node3
ssh root@node2
ssh root@node3
```

---

# 你最可能遇到的 3 个问题

## 1. `docker compose` 命令报错

试这个：

```bash
docker-compose up -d --build
```

有些机器是旧写法。

## 2. ssh 连不上

先确认容器里 sshd 在跑：

```bash
ps -ef | grep sshd
```

如果没有，就手动启动：

```bash
/usr/sbin/sshd
```

## 3. `openjdk-8-jdk` 安装失败

Ubuntu 某些源可能没有 8，可以改成 11：

把 Dockerfile 里的

```dockerfile
openjdk-8-jdk
```

改成

```dockerfile
openjdk-11-jdk
```

同时把

```dockerfile
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
```

改成

```dockerfile
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

---

# 最后一句

你现在这套是 **最轻量的三节点模拟方案**，比虚拟机轻很多，足够你先把“集群、节点、hostname、通信、SSH”这些概念跑通。

下一步你要是愿意，我可以直接继续给你：

**在这 3 个 Docker 节点上安装 Spark Standalone 的完整步骤。**


下面给你一套 **从 0 到 1、完整不省略** 的内容。
你直接照着做，就能在 Mac 上用 Docker 模拟出 `node1 / node2 / node3` 三个节点。

我会给你：

1. 完整目录创建命令
2. 完整 `Dockerfile` 内容
3. 完整 `docker-compose.yml` 内容
4. 完整启动命令
5. 完整进入容器命令
6. 完整网络测试命令
7. 完整 SSH 配置命令
8. 完整 `/etc/hosts` 配置命令
9. 完整验证命令
10. 完整重启/删除命令
11. 出错时的完整修复命令

---

# 一、先确认 Docker 可以用

先在 Mac 终端执行：

```bash
docker --version
docker compose version
```

如果第二条不行，再试：

```bash
docker-compose --version
```

---

# 二、创建项目目录

```bash
mkdir -p ~/docker-spark-3nodes
cd ~/docker-spark-3nodes
pwd
```

你应该看到类似：

```bash
/Users/你的用户名/docker-spark-3nodes
```

---

# 三、创建 Dockerfile

先执行：

```bash
touch Dockerfile
```

然后打开编辑：

```bash
nano Dockerfile
```

把下面 **全部内容原样复制进去**：

```dockerfile
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    openjdk-11-jdk \
    openssh-server \
    openssh-client \
    vim \
    nano \
    net-tools \
    iputils-ping \
    procps \
    rsync \
    curl \
    wget \
    less \
    telnet \
    netcat-openbsd \
    python3 \
    && apt clean

RUN mkdir -p /var/run/sshd
RUN mkdir -p /root/.ssh

RUN echo 'root:123456' | chpasswd

RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config || true
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config || true
RUN echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config
RUN echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config
RUN echo 'PubkeyAuthentication yes' >> /etc/ssh/sshd_config
RUN echo 'AuthorizedKeysFile .ssh/authorized_keys' >> /etc/ssh/sshd_config

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

CMD ["/usr/sbin/sshd", "-D"]
```

保存退出：

* `Ctrl + O`
* 回车
* `Ctrl + X`

然后查看内容：

```bash
cat Dockerfile
```

---

# 四、创建 docker-compose.yml

执行：

```bash
touch docker-compose.yml
nano docker-compose.yml
```

把下面 **全部内容原样复制进去**：

```yaml
services:
  node1:
    build: .
    container_name: node1
    hostname: node1
    tty: true
    stdin_open: true
    privileged: true
    networks:
      spark-net:
        ipv4_address: 172.28.0.11

  node2:
    build: .
    container_name: node2
    hostname: node2
    tty: true
    stdin_open: true
    privileged: true
    networks:
      spark-net:
        ipv4_address: 172.28.0.12

  node3:
    build: .
    container_name: node3
    hostname: node3
    tty: true
    stdin_open: true
    privileged: true
    networks:
      spark-net:
        ipv4_address: 172.28.0.13

networks:
  spark-net:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16
```

保存退出：

* `Ctrl + O`
* 回车
* `Ctrl + X`

检查：

```bash
cat docker-compose.yml
```

---

# 五、构建并启动 3 个节点

执行：

```bash
docker compose up -d --build
```

如果你的机器只支持旧命令，就用：

```bash
docker-compose up -d --build
```

查看容器状态：

```bash
docker ps
```

你应该能看到类似：

```bash
CONTAINER ID   IMAGE                     NAMES
xxxxxx         docker-spark-3nodes...   node1
xxxxxx         docker-spark-3nodes...   node2
xxxxxx         docker-spark-3nodes...   node3
```

再查看更详细状态：

```bash
docker ps -a
```

---

# 六、分别进入三个节点

进入 `node1`：

```bash
docker exec -it node1 bash
```

进入 `node2`：

```bash
docker exec -it node2 bash
```

进入 `node3`：

```bash
docker exec -it node3 bash
```

---

# 七、在每个节点里做基础检查

下面这些命令，进入每个节点后都可以执行一次。

## 1）看主机名

```bash
hostname
```

在 `node1` 应该输出：

```bash
node1
```

在 `node2` 应该输出：

```bash
node2
```

在 `node3` 应该输出：

```bash
node3
```

---

## 2）看 Java

```bash
java -version
echo $JAVA_HOME
```

---

## 3）看 IP

```bash
ip addr
```

或者：

```bash
hostname -I
```

---

## 4）看 sshd 进程

```bash
ps -ef | grep sshd
```

---

# 八、测试三节点网络互通

先进入 `node1`：

```bash
docker exec -it node1 bash
```

执行：

```bash
ping -c 2 node1
ping -c 2 node2
ping -c 2 node3
```

然后退出：

```bash
exit
```

进入 `node2`：

```bash
docker exec -it node2 bash
```

执行：

```bash
ping -c 2 node1
ping -c 2 node2
ping -c 2 node3
```

退出：

```bash
exit
```

进入 `node3`：

```bash
docker exec -it node3 bash
```

执行：

```bash
ping -c 2 node1
ping -c 2 node2
ping -c 2 node3
```

退出：

```bash
exit
```

---

# 九、给三个节点都追加 hosts

虽然 Docker 自带 DNS，但你要模拟课程集群环境，最好还是加上。

下面 3 组命令分别执行。

## 给 node1 加 hosts

```bash
docker exec -it node1 bash -c "cat >> /etc/hosts <<EOF
172.28.0.11 node1
172.28.0.12 node2
172.28.0.13 node3
EOF"
```

## 给 node2 加 hosts

```bash
docker exec -it node2 bash -c "cat >> /etc/hosts <<EOF
172.28.0.11 node1
172.28.0.12 node2
172.28.0.13 node3
EOF"
```

## 给 node3 加 hosts

```bash
docker exec -it node3 bash -c "cat >> /etc/hosts <<EOF
172.28.0.11 node1
172.28.0.12 node2
172.28.0.13 node3
EOF"
```

检查 `node1`：

```bash
docker exec -it node1 bash
cat /etc/hosts
exit
```

检查 `node2`：

```bash
docker exec -it node2 bash
cat /etc/hosts
exit
```

检查 `node3`：

```bash
docker exec -it node3 bash
cat /etc/hosts
exit
```

---

# 十、配置 SSH 免密登录

这一步最关键。

---

## 第 1 步：在 node1 生成密钥

进入 `node1`：

```bash
docker exec -it node1 bash
```

执行下面全部命令：

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

查看公钥：

```bash
cat ~/.ssh/id_rsa.pub
```

把输出的这一整行复制下来。

先测试 node1 ssh 自己：

```bash
ssh -o StrictHostKeyChecking=no root@node1
```

如果进去了，执行：

```bash
hostname
exit
```

现在还留在 `node1` 里，不退出。

---

## 第 2 步：把公钥复制到 node2

新开一个宿主机终端，执行：

```bash
docker exec -it node2 bash
```

执行：

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
nano ~/.ssh/authorized_keys
```

把你刚才从 `node1` 复制出来的整行公钥粘贴进去。

保存退出：

* `Ctrl + O`
* 回车
* `Ctrl + X`

然后执行：

```bash
chmod 600 ~/.ssh/authorized_keys
cat ~/.ssh/authorized_keys
exit
```

---

## 第 3 步：把公钥复制到 node3

宿主机终端执行：

```bash
docker exec -it node3 bash
```

执行：

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
nano ~/.ssh/authorized_keys
```

把刚才同一行公钥粘贴进去。

保存退出：

* `Ctrl + O`
* 回车
* `Ctrl + X`

然后执行：

```bash
chmod 600 ~/.ssh/authorized_keys
cat ~/.ssh/authorized_keys
exit
```

---

## 第 4 步：从 node1 测试 ssh 到 node2 和 node3

回到 `node1` 容器里，如果你已经退出了，就重新进入：

```bash
docker exec -it node1 bash
```

执行：

```bash
ssh -o StrictHostKeyChecking=no root@node2
```

如果成功，执行：

```bash
hostname
exit
```

再执行：

```bash
ssh -o StrictHostKeyChecking=no root@node3
```

如果成功，执行：

```bash
hostname
exit
```

---

# 十一、三节点完整验证命令

下面是一套完整验证流程。

---

## 验证 node1

```bash
docker exec -it node1 bash
hostname
java -version
echo $JAVA_HOME
ping -c 2 node2
ping -c 2 node3
ssh -o StrictHostKeyChecking=no root@node2 hostname
ssh -o StrictHostKeyChecking=no root@node3 hostname
cat /etc/hosts
exit
```

---

## 验证 node2

```bash
docker exec -it node2 bash
hostname
java -version
echo $JAVA_HOME
ping -c 2 node1
ping -c 2 node3
cat /etc/hosts
exit
```

---

## 验证 node3

```bash
docker exec -it node3 bash
hostname
java -version
echo $JAVA_HOME
ping -c 2 node1
ping -c 2 node2
cat /etc/hosts
exit
```

---

# 十二、查看容器详细信息

查看所有容器：

```bash
docker ps -a
```

查看网络：

```bash
docker network ls
```

查看你建的网络详情：

```bash
docker network inspect docker-spark-3nodes_spark-net
```

如果你的 compose 项目名不一样，也可能叫别的名字。
先执行：

```bash
docker network ls
```

找到带 `spark-net` 的名字再 inspect。

---

# 十三、停止、启动、重启、删除

## 停止容器

```bash
docker compose stop
```

或者：

```bash
docker-compose stop
```

---

## 启动容器

```bash
docker compose start
```

或者：

```bash
docker-compose start
```

---

## 重启容器

```bash
docker compose restart
```

或者：

```bash
docker-compose restart
```

---

## 停止并删除容器

```bash
docker compose down
```

或者：

```bash
docker-compose down
```

---

## 停止并删除容器、网络、卷

```bash
docker compose down -v
```

或者：

```bash
docker-compose down -v
```

---

## 重新构建并启动

```bash
docker compose up -d --build
```

或者：

```bash
docker-compose up -d --build
```

---

# 十四、如果 sshd 没起来，完整修复命令

分别对每个节点都可以这样检查。

## 检查 node1

```bash
docker exec -it node1 bash
ps -ef | grep sshd
/usr/sbin/sshd
ps -ef | grep sshd
exit
```

## 检查 node2

```bash
docker exec -it node2 bash
ps -ef | grep sshd
/usr/sbin/sshd
ps -ef | grep sshd
exit
```

## 检查 node3

```bash
docker exec -it node3 bash
ps -ef | grep sshd
/usr/sbin/sshd
ps -ef | grep sshd
exit
```

---

# 十五、如果你要一键重置所有环境

在宿主机目录 `~/docker-spark-3nodes` 下执行：

```bash
docker compose down -v
docker rm -f node1 node2 node3 2>/dev/null || true
docker network prune -f
docker compose up -d --build
docker ps
```

如果你用的是旧版命令：

```bash
docker-compose down -v
docker rm -f node1 node2 node3 2>/dev/null || true
docker network prune -f
docker-compose up -d --build
docker ps
```

---

# 十六、完整文件内容再给你一遍

## Dockerfile 完整版

```dockerfile
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    openjdk-11-jdk \
    openssh-server \
    openssh-client \
    vim \
    nano \
    net-tools \
    iputils-ping \
    procps \
    rsync \
    curl \
    wget \
    less \
    telnet \
    netcat-openbsd \
    python3 \
    && apt clean

RUN mkdir -p /var/run/sshd
RUN mkdir -p /root/.ssh

RUN echo 'root:123456' | chpasswd

RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config || true
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config || true
RUN echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config
RUN echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config
RUN echo 'PubkeyAuthentication yes' >> /etc/ssh/sshd_config
RUN echo 'AuthorizedKeysFile .ssh/authorized_keys' >> /etc/ssh/sshd_config

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

CMD ["/usr/sbin/sshd", "-D"]
```

---

## docker-compose.yml 完整版

```yaml
services:
  node1:
    build: .
    container_name: node1
    hostname: node1
    tty: true
    stdin_open: true
    privileged: true
    networks:
      spark-net:
        ipv4_address: 172.28.0.11

  node2:
    build: .
    container_name: node2
    hostname: node2
    tty: true
    stdin_open: true
    privileged: true
    networks:
      spark-net:
        ipv4_address: 172.28.0.12

  node3:
    build: .
    container_name: node3
    hostname: node3
    tty: true
    stdin_open: true
    privileged: true
    networks:
      spark-net:
        ipv4_address: 172.28.0.13

networks:
  spark-net:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16
```

---

# 十七、最短执行顺序

如果你想只看主流程，顺序就是：

```bash
mkdir -p ~/docker-spark-3nodes
cd ~/docker-spark-3nodes
nano Dockerfile
nano docker-compose.yml
docker compose up -d --build
docker ps
docker exec -it node1 bash
docker exec -it node2 bash
docker exec -it node3 bash
```

然后：

* 配 hosts
* 配 ssh key
* 测试 ping
* 测试 ssh

---

# 十八、你做完后，成功的标准

你在 `node1` 里执行下面这几条都成功，就说明三节点已经模拟好了：

```bash
hostname
ping -c 2 node2
ping -c 2 node3
ssh -o StrictHostKeyChecking=no root@node2 hostname
ssh -o StrictHostKeyChecking=no root@node3 hostname
java -version
```

---

你要的话，我下一条直接继续给你：

**把 Spark 安装到这 3 个 Docker 节点上的完整命令版。**


下面直接继续。
这是 **在你刚刚那 3 个 Docker 节点上安装 Spark Standalone 集群** 的 **完整命令 + 完整文件内容**，不省略。

目标：

* `node1` = Spark Master
* `node2` = Spark Worker
* `node3` = Spark Worker
* 最后你可以打开：

  * `http://localhost:8080` 看 Master
  * `http://localhost:8081` 看 Worker1
  * `http://localhost:8082` 看 Worker2

---

# 一、先修改 `docker-compose.yml`

先回到宿主机项目目录：

```bash
cd ~/docker-spark-3nodes
pwd
```

打开原来的 `docker-compose.yml`：

```bash
nano docker-compose.yml
```

把 **整个文件** 替换成下面这份完整内容：

```yaml
services:
  node1:
    build: .
    container_name: node1
    hostname: node1
    tty: true
    stdin_open: true
    privileged: true
    ports:
      - "8080:8080"
      - "7077:7077"
    networks:
      spark-net:
        ipv4_address: 172.28.0.11

  node2:
    build: .
    container_name: node2
    hostname: node2
    tty: true
    stdin_open: true
    privileged: true
    ports:
      - "8081:8081"
    networks:
      spark-net:
        ipv4_address: 172.28.0.12

  node3:
    build: .
    container_name: node3
    hostname: node3
    tty: true
    stdin_open: true
    privileged: true
    ports:
      - "8082:8081"
    networks:
      spark-net:
        ipv4_address: 172.28.0.13

networks:
  spark-net:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16
```

保存退出：

* `Ctrl + O`
* 回车
* `Ctrl + X`

检查内容：

```bash
cat docker-compose.yml
```

---

# 二、重建容器

执行：

```bash
docker compose down
docker compose up -d --build
docker ps
```

如果你机器上是旧版命令：

```bash
docker-compose down
docker-compose up -d --build
docker ps
```

你应该能看到 `node1` `node2` `node3` 都启动了。

---

# 三、下载 Spark 安装包到宿主机

回到项目目录：

```bash
cd ~/docker-spark-3nodes
```

下载 Spark 3.2.0：

```bash
curl -L -o spark-3.2.0-bin-hadoop3.2.tgz https://archive.apache.org/dist/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz
ls -lh spark-3.2.0-bin-hadoop3.2.tgz
```

---

# 四、把 Spark 包复制到三个节点

```bash
docker cp spark-3.2.0-bin-hadoop3.2.tgz node1:/root/
docker cp spark-3.2.0-bin-hadoop3.2.tgz node2:/root/
docker cp spark-3.2.0-bin-hadoop3.2.tgz node3:/root/
```

---

# 五、在三个节点上解压 Spark

## 1）node1

```bash
docker exec -it node1 bash
```

执行：

```bash
cd /root
tar -zxvf spark-3.2.0-bin-hadoop3.2.tgz
mv spark-3.2.0-bin-hadoop3.2 spark
ls /root
exit
```

## 2）node2

```bash
docker exec -it node2 bash
```

执行：

```bash
cd /root
tar -zxvf spark-3.2.0-bin-hadoop3.2.tgz
mv spark-3.2.0-bin-hadoop3.2 spark
ls /root
exit
```

## 3）node3

```bash
docker exec -it node3 bash
```

执行：

```bash
cd /root
tar -zxvf spark-3.2.0-bin-hadoop3.2.tgz
mv spark-3.2.0-bin-hadoop3.2 spark
ls /root
exit
```

---

# 六、配置三个节点的环境变量

## 1）配置 node1

```bash
docker exec -it node1 bash
```

执行：

```bash
cat >> /root/.bashrc <<'EOF'

export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export SPARK_HOME=/root/spark
export PATH=$JAVA_HOME/bin:$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH
EOF
source /root/.bashrc
echo $JAVA_HOME
echo $SPARK_HOME
exit
```

## 2）配置 node2

```bash
docker exec -it node2 bash
```

执行：

```bash
cat >> /root/.bashrc <<'EOF'

export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export SPARK_HOME=/root/spark
export PATH=$JAVA_HOME/bin:$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH
EOF
source /root/.bashrc
echo $JAVA_HOME
echo $SPARK_HOME
exit
```

## 3）配置 node3

```bash
docker exec -it node3 bash
```

执行：

```bash
cat >> /root/.bashrc <<'EOF'

export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export SPARK_HOME=/root/spark
export PATH=$JAVA_HOME/bin:$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH
EOF
source /root/.bashrc
echo $JAVA_HOME
echo $SPARK_HOME
exit
```

---

# 七、先确保三节点 `/etc/hosts` 正确

如果你前面已经配过，也可以再执行一次。

## node1

```bash
docker exec -it node1 bash -c "cat > /etc/hosts <<'EOF'
127.0.0.1 localhost
172.28.0.11 node1
172.28.0.12 node2
172.28.0.13 node3
EOF"
```

## node2

```bash
docker exec -it node2 bash -c "cat > /etc/hosts <<'EOF'
127.0.0.1 localhost
172.28.0.11 node1
172.28.0.12 node2
172.28.0.13 node3
EOF"
```

## node3

```bash
docker exec -it node3 bash -c "cat > /etc/hosts <<'EOF'
127.0.0.1 localhost
172.28.0.11 node1
172.28.0.12 node2
172.28.0.13 node3
EOF"
```

检查：

```bash
docker exec -it node1 bash -c "cat /etc/hosts"
docker exec -it node2 bash -c "cat /etc/hosts"
docker exec -it node3 bash -c "cat /etc/hosts"
```

---

# 八、重新配置 node1 到 node2/node3 的 SSH 免密

如果前面已经成功配过，也建议再确认一遍。

## 1）在 node1 生成 key

```bash
docker exec -it node1 bash
```

执行：

```bash
mkdir -p /root/.ssh
chmod 700 /root/.ssh
rm -f /root/.ssh/id_rsa
rm -f /root/.ssh/id_rsa.pub
ssh-keygen -t rsa -P '' -f /root/.ssh/id_rsa
cat /root/.ssh/id_rsa.pub
```

复制输出的整行公钥。

先让自己也能 ssh 自己：

```bash
cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys
chmod 600 /root/.ssh/authorized_keys
ssh -o StrictHostKeyChecking=no root@node1 hostname
```

看到 `node1` 后继续，先不要退出 node1。

---

## 2）把公钥放到 node2

新开宿主机终端执行：

```bash
docker exec -it node2 bash
```

执行：

```bash
mkdir -p /root/.ssh
chmod 700 /root/.ssh
nano /root/.ssh/authorized_keys
```

把刚才从 node1 复制的那一整行公钥粘贴进去。

保存退出后执行：

```bash
chmod 600 /root/.ssh/authorized_keys
cat /root/.ssh/authorized_keys
exit
```

---

## 3）把公钥放到 node3

宿主机执行：

```bash
docker exec -it node3 bash
```

执行：

```bash
mkdir -p /root/.ssh
chmod 700 /root/.ssh
nano /root/.ssh/authorized_keys
```

把同一行公钥粘贴进去。

保存退出后执行：

```bash
chmod 600 /root/.ssh/authorized_keys
cat /root/.ssh/authorized_keys
exit
```

---

## 4）回到 node1 测试 ssh

如果你刚才退出了 node1，就重新进入：

```bash
docker exec -it node1 bash
```

执行：

```bash
ssh -o StrictHostKeyChecking=no root@node2 hostname
ssh -o StrictHostKeyChecking=no root@node3 hostname
```

如果分别输出：

```bash
node2
node3
```

说明免密成功。

退出：

```bash
exit
```

---

# 九、配置 Spark 的 `spark-env.sh`

只需要在 `node1` 配好，再复制到 `node2` `node3`。

## 1）在 node1 创建配置

```bash
docker exec -it node1 bash
```

执行：

```bash
cd /root/spark/conf
cp spark-env.sh.template spark-env.sh
cp workers.template workers
nano spark-env.sh
```

把 `spark-env.sh` **整个文件内容** 改成下面这样：

```bash
#!/usr/bin/env bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export SPARK_MASTER_HOST=node1
export SPARK_MASTER_PORT=7077
export SPARK_MASTER_WEBUI_PORT=8080
export SPARK_WORKER_CORES=1
export SPARK_WORKER_MEMORY=1g
export SPARK_WORKER_WEBUI_PORT=8081
export SPARK_LOG_DIR=/root/spark/logs
```

保存退出。

然后编辑 `workers`：

```bash
nano workers
```

把 `workers` 文件内容改成：

```text
node2
node3
```

保存退出。

检查：

```bash
cat /root/spark/conf/spark-env.sh
cat /root/spark/conf/workers
```

退出：

```bash
exit
```

---

# 十、把 Spark 配置复制到 node2 和 node3

## 复制 `spark-env.sh`

```bash
docker cp node1:/root/spark/conf/spark-env.sh ./spark-env.sh
docker cp node1:/root/spark/conf/workers ./workers
ls -l spark-env.sh workers
```

## 拷贝到 node2

```bash
docker cp ./spark-env.sh node2:/root/spark/conf/spark-env.sh
docker cp ./workers node2:/root/spark/conf/workers
```

## 拷贝到 node3

```bash
docker cp ./spark-env.sh node3:/root/spark/conf/spark-env.sh
docker cp ./workers node3:/root/spark/conf/workers
```

---

# 十一、在三个节点上检查配置

## node1

```bash
docker exec -it node1 bash
cat /root/spark/conf/spark-env.sh
cat /root/spark/conf/workers
exit
```

## node2

```bash
docker exec -it node2 bash
cat /root/spark/conf/spark-env.sh
cat /root/spark/conf/workers
exit
```

## node3

```bash
docker exec -it node3 bash
cat /root/spark/conf/spark-env.sh
cat /root/spark/conf/workers
exit
```

---

# 十二、启动 Spark Master 和 Workers

## 方式 A：推荐，直接从 node1 启动整个集群

进入 node1：

```bash
docker exec -it node1 bash
```

执行：

```bash
source /root/.bashrc
cd /root/spark
sbin/start-master.sh
sbin/start-workers.sh
jps
```

如果 `start-workers.sh` 不行，再手动启动 worker。

先别退出，继续看下面。

---

# 十三、如果 `start-workers.sh` 因 ssh 或脚本问题失败，就手动启动

## 1）node1 启动 master

在 node1：

```bash
source /root/.bashrc
cd /root/spark
sbin/start-master.sh
jps
```

应该看到类似：

```text
Master
Jps
```

---

## 2）node2 启动 worker

宿主机新开终端：

```bash
docker exec -it node2 bash
```

执行：

```bash
source /root/.bashrc
cd /root/spark
sbin/start-worker.sh spark://node1:7077 --webui-port 8081
jps
```

应该看到类似：

```text
Worker
Jps
```

退出：

```bash
exit
```

---

## 3）node3 启动 worker

宿主机新开终端：

```bash
docker exec -it node3 bash
```

执行：

```bash
source /root/.bashrc
cd /root/spark
sbin/start-worker.sh spark://node1:7077 --webui-port 8081
jps
```

应该看到类似：

```text
Worker
Jps
```

退出：

```bash
exit
```

---

# 十四、检查集群是否起来

## 1）检查 node1 的 Master 日志和进程

```bash
docker exec -it node1 bash
source /root/.bashrc
jps
ls /root/spark/logs
exit
```

## 2）检查 node2 的 Worker

```bash
docker exec -it node2 bash
source /root/.bashrc
jps
ls /root/spark/logs
exit
```

## 3）检查 node3 的 Worker

```bash
docker exec -it node3 bash
source /root/.bashrc
jps
ls /root/spark/logs
exit
```

---

# 十五、在浏览器打开 Web UI

现在在你的 Mac 浏览器打开：

```text
http://localhost:8080
```

这是 Master 页面。

你应该看到：

* Master URL
* Alive Workers
* worker 数量 = 2

还可以打开：

```text
http://localhost:8081
http://localhost:8082
```

分别看两个 Worker 页面。

---

# 十六、提交一个 Spark 程序测试

进入 node1：

```bash
docker exec -it node1 bash
```

执行：

```bash
source /root/.bashrc
cd /root/spark
bin/spark-submit \
  --master spark://node1:7077 \
  --class org.apache.spark.examples.SparkPi \
  examples/jars/spark-examples_2.12-3.2.0.jar \
  10
```

如果成功，你会看到类似：

```text
Pi is roughly 3.14...
```

这说明集群已经真的跑起来了。

退出：

```bash
exit
```

---

# 十七、再做一个交互式测试

进入 node1：

```bash
docker exec -it node1 bash
```

执行：

```bash
source /root/.bashrc
cd /root/spark
bin/pyspark --master spark://node1:7077
```

进入 PySpark 后执行：

```python
sc.parallelize([1,2,3,4,5]).map(lambda x: x + 1).collect()
```

你应该看到：

```python
[2, 3, 4, 5, 6]
```

退出 PySpark：

```python
exit()
```

退出容器：

```bash
exit
```

---

# 十八、停止集群的完整命令

## 停止 node2 worker

```bash
docker exec -it node2 bash -c "source /root/.bashrc && cd /root/spark && sbin/stop-worker.sh"
```

## 停止 node3 worker

```bash
docker exec -it node3 bash -c "source /root/.bashrc && cd /root/spark && sbin/stop-worker.sh"
```

## 停止 node1 master

```bash
docker exec -it node1 bash -c "source /root/.bashrc && cd /root/spark && sbin/stop-master.sh"
```

---

# 十九、重新启动集群的完整命令

## node1 启动 master

```bash
docker exec -it node1 bash -c "source /root/.bashrc && cd /root/spark && sbin/start-master.sh"
```

## node2 启动 worker

```bash
docker exec -it node2 bash -c "source /root/.bashrc && cd /root/spark && sbin/start-worker.sh spark://node1:7077 --webui-port 8081"
```

## node3 启动 worker

```bash
docker exec -it node3 bash -c "source /root/.bashrc && cd /root/spark && sbin/start-worker.sh spark://node1:7077 --webui-port 8081"
```

---

# 二十、完整配置文件再给你一遍

## `spark-env.sh`

```bash
#!/usr/bin/env bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export SPARK_MASTER_HOST=node1
export SPARK_MASTER_PORT=7077
export SPARK_MASTER_WEBUI_PORT=8080
export SPARK_WORKER_CORES=1
export SPARK_WORKER_MEMORY=1g
export SPARK_WORKER_WEBUI_PORT=8081
export SPARK_LOG_DIR=/root/spark/logs
```

## `workers`

```text
node2
node3
```

---

# 二十一、最短主流程命令汇总

如果你想只看主线，顺序就是这个：

```bash
cd ~/docker-spark-3nodes
nano docker-compose.yml
docker compose down
docker compose up -d --build

curl -L -o spark-3.2.0-bin-hadoop3.2.tgz https://archive.apache.org/dist/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz

docker cp spark-3.2.0-bin-hadoop3.2.tgz node1:/root/
docker cp spark-3.2.0-bin-hadoop3.2.tgz node2:/root/
docker cp spark-3.2.0-bin-hadoop3.2.tgz node3:/root/
```

然后分别进入三个节点解压并设环境变量，再：

```bash
docker exec -it node1 bash
cd /root/spark/conf
cp spark-env.sh.template spark-env.sh
cp workers.template workers
nano spark-env.sh
nano workers
```

再启动：

```bash
docker exec -it node1 bash -c "source /root/.bashrc && cd /root/spark && sbin/start-master.sh"
docker exec -it node2 bash -c "source /root/.bashrc && cd /root/spark && sbin/start-worker.sh spark://node1:7077 --webui-port 8081"
docker exec -it node3 bash -c "source /root/.bashrc && cd /root/spark && sbin/start-worker.sh spark://node1:7077 --webui-port 8081"
```

测试：

```bash
docker exec -it node1 bash -c "source /root/.bashrc && cd /root/spark && bin/spark-submit --master spark://node1:7077 --class org.apache.spark.examples.SparkPi examples/jars/spark-examples_2.12-3.2.0.jar 10"
```

---

# 二十二、成功标准

你只要满足下面 4 条，就算成功：

1. `http://localhost:8080` 能打开
2. Master 页面里显示 **2 个 Alive Workers**
3. `jps` 看到：

   * node1: `Master`
   * node2: `Worker`
   * node3: `Worker`
4. `SparkPi` 能跑出结果

---

# 二十三、你现在已经学到的本质

这套环境对应课件里的知识点就是：

* Docker 容器 = 模拟 3 台机器
* `node1` 跑 `Master`
* `node2/node3` 跑 `Worker`
* `spark://node1:7077` 是集群入口
* Web UI:

  * `8080` = Master
  * `8081/8082` = Workers
* 提交任务后：

  * Driver 调度
  * Workers 提供资源
  * Executors 执行 Tasks

---

下一条我可以继续直接给你：

**把 PySpark、WordCount、4040 页面、Job/Stage/Task 观察步骤也全部写成完整命令版。**



下面继续给你 **完整不省略** 的下一部分：
在你已经搭好的 Docker 三节点 Spark Standalone 集群上，做：

1. PySpark 连接集群
2. WordCount 完整测试
3. 看 4040 页面
4. 观察 Job / Stage / Task
5. 常见命令和验证方法

我默认你现在已经完成前一步，并且：

* `node1` 是 Master
* `node2`、`node3` 是 Worker
* `http://localhost:8080` 可以打开
* 集群入口是 `spark://node1:7077`

---

# 一、先确认集群在运行

在宿主机执行：

```bash
docker ps
```

然后检查进程。

## 检查 node1

```bash
docker exec -it node1 bash -c "source /root/.bashrc && jps"
```

你应该看到类似：

```text
Master
Jps
```

## 检查 node2

```bash
docker exec -it node2 bash -c "source /root/.bashrc && jps"
```

你应该看到类似：

```text
Worker
Jps
```

## 检查 node3

```bash
docker exec -it node3 bash -c "source /root/.bashrc && jps"
```

你应该看到类似：

```text
Worker
Jps
```

---

# 二、给 node1 准备测试文件

我们先在 `node1` 里准备一个文本文件，后面做 WordCount。

进入 `node1`：

```bash
docker exec -it node1 bash
```

执行：

```bash
source /root/.bashrc
mkdir -p /root/data
cat > /root/data/words.txt <<'EOF'
hello spark
hello docker
hello cluster
spark docker spark
cluster docker hello
EOF
```

检查内容：

```bash
cat /root/data/words.txt
```

你应该看到：

```text
hello spark
hello docker
hello cluster
spark docker spark
cluster docker hello
```

先不要退出，后面继续用。

---

# 三、用 PySpark 连接集群

还在 `node1` 里，执行：

```bash
cd /root/spark
bin/pyspark --master spark://node1:7077
```

如果成功，你会进入 PySpark 交互环境，看到类似提示符：

```python
>>>
```

---

# 四、先做最简单的集群计算测试

在 PySpark 里输入下面代码：

```python
sc.parallelize([1, 2, 3, 4, 5]).map(lambda x: x + 10).collect()
```

你应该看到：

```python
[11, 12, 13, 14, 15]
```

这说明：

* Driver 在 node1
* 任务被提交到 Spark 集群
* Worker 在执行 Task
* 结果返回到 Driver

---

# 五、在 PySpark 里做 WordCount

继续在 PySpark 里输入下面完整代码：

```python
rdd = sc.textFile("file:///root/data/words.txt")
words = rdd.flatMap(lambda line: line.split(" "))
pairs = words.map(lambda word: (word, 1))
result = pairs.reduceByKey(lambda a, b: a + b)
result.collect()
```

你应该看到类似：

```python
[('hello', 4), ('spark', 3), ('docker', 3), ('cluster', 2)]
```

有时顺序可能不同，例如：

```python
[('spark', 3), ('hello', 4), ('docker', 3), ('cluster', 2)]
```

顺序不同是正常的。

---

# 六、把 WordCount 代码写成一行版本

如果你想测试课件里那种链式写法，在 PySpark 里继续执行：

```python
sc.textFile("file:///root/data/words.txt").flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b).collect()
```

---

# 七、查看默认分区数

在 PySpark 里执行：

```python
rdd = sc.textFile("file:///root/data/words.txt")
rdd.getNumPartitions()
```

你会得到一个数字，例如：

```python
2
```

这个数字表示这个 RDD 当前有几个 Partition。

---

# 八、手动指定分区数，再观察 Task 数量

在 PySpark 里执行：

```python
rdd = sc.textFile("file:///root/data/words.txt", 4)
rdd.getNumPartitions()
```

你应该看到：

```python
4
```

再执行：

```python
result = rdd.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
result.collect()
```

这个版本后面在 4040 里更容易看到多个 Task。

---

# 九、如何打开 4040 页面

当你在 `node1` 里跑着 PySpark 程序时，Spark 会在 Driver 所在机器打开 4040 端口。
但现在 `node1` 是 Docker 容器，所以你需要把容器的 4040 暴露到宿主机。

---

# 十、修改 `docker-compose.yml`，暴露 4040

回到宿主机项目目录：

```bash
cd ~/docker-spark-3nodes
nano docker-compose.yml
```

把 `node1` 改成下面这样。
为了不遗漏，我把整个文件再给你一遍。

```yaml
services:
  node1:
    build: .
    container_name: node1
    hostname: node1
    tty: true
    stdin_open: true
    privileged: true
    ports:
      - "8080:8080"
      - "7077:7077"
      - "4040:4040"
      - "4041:4041"
      - "4042:4042"
    networks:
      spark-net:
        ipv4_address: 172.28.0.11

  node2:
    build: .
    container_name: node2
    hostname: node2
    tty: true
    stdin_open: true
    privileged: true
    ports:
      - "8081:8081"
    networks:
      spark-net:
        ipv4_address: 172.28.0.12

  node3:
    build: .
    container_name: node3
    hostname: node3
    tty: true
    stdin_open: true
    privileged: true
    ports:
      - "8082:8081"
    networks:
      spark-net:
        ipv4_address: 172.28.0.13

networks:
  spark-net:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16
```

保存退出后执行：

```bash
docker compose down
docker compose up -d --build
```

注意：
这一步会重建容器。
如果你之前容器里的 Spark、配置、数据都没做持久化，这一步可能把你前面容器内手动改的内容清掉。
所以现在最稳的是：

**先不要重建。**
先继续在当前容器里学习逻辑。
等你确认想长期保留环境时，再做持久化版本。

你当前如果只是想学习观察，先在容器内部看日志和 Web UI 即可。

---

# 十一、在当前环境中看 Driver 日志和 Worker 日志

## 看 node1 日志

```bash
docker exec -it node1 bash
source /root/.bashrc
ls /root/spark/logs
```

看 Master 日志：

```bash
cat /root/spark/logs/*Master*.out
```

如果日志多，也可以：

```bash
tail -n 100 /root/spark/logs/*Master*.out
```

退出：

```bash
exit
```

---

## 看 node2 Worker 日志

```bash
docker exec -it node2 bash
source /root/.bashrc
ls /root/spark/logs
tail -n 100 /root/spark/logs/*Worker*.out
exit
```

---

## 看 node3 Worker 日志

```bash
docker exec -it node3 bash
source /root/.bashrc
ls /root/spark/logs
tail -n 100 /root/spark/logs/*Worker*.out
exit
```

这些日志可以帮你确认：

* Worker 是否注册到 Master
* 有没有收到任务
* Executor 有没有启动

---

# 十二、用 `spark-submit` 跑官方例子

比 PySpark 更适合稳定观察集群任务。

进入 node1：

```bash
docker exec -it node1 bash
```

执行：

```bash
source /root/.bashrc
cd /root/spark
bin/spark-submit \
  --master spark://node1:7077 \
  --class org.apache.spark.examples.SparkPi \
  examples/jars/spark-examples_2.12-3.2.0.jar \
  10
```

你应该看到类似：

```text
Pi is roughly 3.14...
```

这说明：

* 程序成功提交给 Master
* Worker 成功执行任务
* 最终结果返回

---

# 十三、看 Master Web UI 里的内容

现在打开浏览器：

```text
http://localhost:8080
```

你应该重点看这些地方：

## 1）Workers

你会看到：

* `node2`
* `node3`

## 2）Alive Workers

应该是 2

## 3）Memory / Cores

能看到每个 Worker 提供的资源

## 4）Running Applications / Completed Applications

当你运行程序后，这里会出现应用记录

---

# 十四、Job / Stage / Task 到底怎么看

这个很重要。

---

## 1）Application

你每提交一个 Spark 程序，就是一个 Application。

例如：

* 一个 `pyspark`
* 一个 `spark-submit SparkPi`

都算一个 Application。

---

## 2）Job

通常一个 Action 会触发一个 Job。

例如在 PySpark 里：

```python
result.collect()
```

这个 `collect()` 就会触发 Job。

---

## 3）Stage

一个 Job 会根据是否有 Shuffle 被拆成多个 Stage。

例如：

```python
rdd.flatMap(...).map(...).reduceByKey(...).collect()
```

这里 `reduceByKey` 通常会引入 Shuffle，
所以通常会看到不止一个 Stage。

---

## 4）Task

每个 Stage 会被切成多个 Task。
一般来说：

**Task 数量 ≈ Partition 数量**

例如：

```python
rdd = sc.textFile("file:///root/data/words.txt", 4)
```

如果后续 Stage 还是 4 个分区，那通常就会有 4 个 Task。

---

# 十五、最适合观察 Job / Stage / Task 的 Python 示例

进入 node1：

```bash
docker exec -it node1 bash
source /root/.bashrc
cd /root/spark
bin/pyspark --master spark://node1:7077
```

在 PySpark 中执行下面代码：

```python
rdd = sc.parallelize(
    ["hello spark", "hello docker", "spark cluster", "docker cluster", "hello hello"],
    4
)

rdd.getNumPartitions()
```

你应该看到：

```python
4
```

继续执行：

```python
words = rdd.flatMap(lambda line: line.split(" "))
pairs = words.map(lambda word: (word, 1))
counts = pairs.reduceByKey(lambda a, b: a + b)
counts.collect()
```

你应该看到类似：

```python
[('hello', 4), ('spark', 2), ('docker', 2), ('cluster', 2)]
```

这个例子非常适合看：

* `collect()` 触发 Job
* `reduceByKey()` 产生 Shuffle
* 所以 Job 会被切成多个 Stage
* 4 个 Partition 对应多个 Task

---

# 十六、如果你已经暴露了 4040，怎么观察

如果你后面把 4040 映射到宿主机了，打开：

```text
http://localhost:4040
```

重点看这几个标签：

## Jobs

能看到：

* Job ID
* Description
* Duration
* Stages

## Stages

能看到：

* 每个 Stage 有多少个 Task
* 每个 Task 完成情况

## Executors

能看到：

* Driver
* Executors 分布
* 每个 Executor 的 Task 数

## Storage

如果你做了 cache/persist，这里能看到缓存信息

---

# 十七、如何故意制造多个 Job，便于观察

在 PySpark 里执行下面代码：

```python
rdd = sc.parallelize([1, 2, 3, 4, 5], 3)
rdd.map(lambda x: x + 1).collect()
rdd.map(lambda x: x * 2).collect()
rdd.filter(lambda x: x % 2 == 0).collect()
```

这里有 3 个 Action：

* 第一个 `collect()`
* 第二个 `collect()`
* 第三个 `collect()`

所以通常会看到 **3 个 Job**。

---

# 十八、如何故意制造 Shuffle，便于看多个 Stage

在 PySpark 里执行：

```python
rdd = sc.parallelize(["a b c", "a b", "a"], 3)
rdd.flatMap(lambda x: x.split(" ")).map(lambda x: (x, 1)).reduceByKey(lambda a, b: a + b).collect()
```

因为用了 `reduceByKey`，会产生 Shuffle。
通常你会看到 **多个 Stage**。

---

# 十九、如何用代码看 Partition

在 PySpark 里执行：

```python
rdd = sc.parallelize([1, 2, 3, 4, 5, 6], 3)
rdd.getNumPartitions()
```

查看每个分区里是什么：

```python
rdd.glom().collect()
```

你可能看到类似：

```python
[[1, 2], [3, 4], [5, 6]]
```

这非常适合你理解：

* 数据先被切成分区
* 每个分区通常对应一个 Task

---

# 二十、一个完整观察实验

下面给你一个 **从头到尾完整实验**。

进入 node1：

```bash
docker exec -it node1 bash
source /root/.bashrc
cd /root/spark
bin/pyspark --master spark://node1:7077
```

在 PySpark 里执行：

```python
rdd = sc.parallelize(
    ["apple banana apple", "banana orange", "apple orange banana", "banana"],
    4
)

rdd.getNumPartitions()
rdd.glom().collect()

words = rdd.flatMap(lambda line: line.split(" "))
pairs = words.map(lambda word: (word, 1))
counts = pairs.reduceByKey(lambda a, b: a + b)

counts.collect()
counts.collect()
pairs.collect()
```

这里你会观察到：

* `counts.collect()` 第一次：1 个 Job
* `counts.collect()` 第二次：又 1 个 Job
* `pairs.collect()` 再 1 个 Job

并且 `reduceByKey` 会让 Job 里面出现多个 Stage。

退出：

```python
exit()
```

退出容器：

```bash
exit
```

---

# 二十一、如果你想用脚本文件跑 PySpark

可以在 node1 创建一个 `.py` 文件。

进入 node1：

```bash
docker exec -it node1 bash
```

执行：

```bash
cat > /root/wordcount.py <<'EOF'
from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("WordCountOnCluster")
sc = SparkContext(conf=conf)

rdd = sc.textFile("file:///root/data/words.txt")
result = (
    rdd.flatMap(lambda line: line.split(" "))
       .map(lambda word: (word, 1))
       .reduceByKey(lambda a, b: a + b)
)

print(result.collect())

sc.stop()
EOF
```

检查：

```bash
cat /root/wordcount.py
```

执行：

```bash
cd /root/spark
bin/spark-submit --master spark://node1:7077 /root/wordcount.py
```

---

# 二十二、如果你想看更明显的 Worker 分工

让数据量更大一些。

进入 node1：

```bash
docker exec -it node1 bash
```

执行：

```bash
python3 - <<'EOF'
with open('/root/data/big_words.txt', 'w') as f:
    for i in range(10000):
        f.write('hello spark docker cluster\n')
EOF
```

检查：

```bash
wc -l /root/data/big_words.txt
```

然后跑：

```bash
cat > /root/big_wordcount.py <<'EOF'
from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("BigWordCount")
sc = SparkContext(conf=conf)

rdd = sc.textFile("file:///root/data/big_words.txt", 8)
result = (
    rdd.flatMap(lambda line: line.split(" "))
       .map(lambda word: (word, 1))
       .reduceByKey(lambda a, b: a + b)
)

print(result.collect())
sc.stop()
EOF
```

执行：

```bash
cd /root/spark
bin/spark-submit --master spark://node1:7077 /root/big_wordcount.py
```

这样更容易让多个 Worker 都参与。

---

# 二十三、最常用查看命令

## 查看 Master 页面

```text
http://localhost:8080
```

## 看 node1 进程

```bash
docker exec -it node1 bash -c "source /root/.bashrc && jps"
```

## 看 node2 进程

```bash
docker exec -it node2 bash -c "source /root/.bashrc && jps"
```

## 看 node3 进程

```bash
docker exec -it node3 bash -c "source /root/.bashrc && jps"
```

## 看 node2 Worker 日志

```bash
docker exec -it node2 bash -c "tail -n 100 /root/spark/logs/*Worker*.out"
```

## 看 node3 Worker 日志

```bash
docker exec -it node3 bash -c "tail -n 100 /root/spark/logs/*Worker*.out"
```

---

# 二十四、你现在应该能理解的知识点

通过这套实验，你应该建立下面这个映射：

## 1）程序入口

* `pyspark`
* `spark-submit`

这两个都是提交 Spark Application 的方式。

## 2）Application

* 一个完整 Spark 程序

## 3）Driver

* 程序大脑
* 负责切分 Job / Stage / Task

## 4）Worker

* 提供资源的节点

## 5）Executor

* 真正执行 Task 的进程

## 6）Task

* 最小执行单位
* 一般和 Partition 强相关

## 7）Shuffle

* 如 `reduceByKey`
* 往往会引入多个 Stage

---

# 二十五、最短实验清单

你只做这几步，也足够掌握核心：

```bash
docker exec -it node1 bash
source /root/.bashrc
cd /root/spark
bin/pyspark --master spark://node1:7077
```

然后在 PySpark 里：

```python
rdd = sc.parallelize(["hello spark", "hello docker", "spark cluster"], 4)
rdd.getNumPartitions()
rdd.glom().collect()
rdd.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b).collect()
```

再去浏览器看：

```text
http://localhost:8080
```

---

# 二十六、建议你下一步做什么

现在最适合你的下一步是这两个方向之一：

**方向 1：继续本地集群学习**

* 缓存 `cache/persist`
* `repartition/coalesce`
* `map` vs `flatMap`
* `reduceByKey` vs `groupByKey`

**方向 2：开始往 AWS 映射**

* Docker 三节点 Spark → 类比 EMR
* 本地文件 → 类比 S3
* Master/Worker → 类比 Driver/Executor on EMR

如果你愿意，我下一条直接给你：

**“PySpark 10 个最常见实验，每个都有完整命令和现象解释”**


下面直接给你 **PySpark 10 个最常见实验**，每个都带：

* 目的
* 完整命令
* 完整代码
* 预期现象
* 你该观察什么

我默认你现在已经有：

* Docker 三节点
* Spark Standalone 集群
* `node1` 是 Master
* `node2` / `node3` 是 Worker
* 可以进入 `node1`
* 可以运行：

```bash
docker exec -it node1 bash
source /root/.bashrc
cd /root/spark
bin/pyspark --master spark://node1:7077
```

---

# 实验 0：先进入 PySpark

每次做实验前，先执行：

```bash
docker exec -it node1 bash
source /root/.bashrc
cd /root/spark
bin/pyspark --master spark://node1:7077
```

进入后你会看到：

```python
>>>
```

后面的 Python 代码都在这里执行。

退出时：

```python
exit()
```

然后：

```bash
exit
```

---

# 实验 1：parallelize 创建 RDD

## 目的

理解：

* 本地集合怎么变成 RDD
* RDD 是分布式对象

## 代码

```python
rdd = sc.parallelize([1, 2, 3, 4, 5])
print(rdd)
print(rdd.collect())
```

## 预期现象

你会看到类似：

```python
ParallelCollectionRDD[0] at readRDDFromFile at PythonRDD.scala:...
[1, 2, 3, 4, 5]
```

## 你该理解什么

* `parallelize()`：本地集合 -> RDD
* `collect()`：RDD -> 本地 Python list

---

# 实验 2：看默认分区数

## 目的

理解：

* RDD 有分区
* 分区影响并行度

## 代码

```python
rdd = sc.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9])
print(rdd.getNumPartitions())
```

## 预期现象

你会得到一个数字，比如：

```python
2
```

或者别的数字。

## 你该理解什么

* `getNumPartitions()` = 当前 RDD 的分区数
* 分区数通常和默认并行度有关

---

# 实验 3：手动指定分区数

## 目的

理解：

* 可以自己指定分区数
* Task 数量通常和分区有关

## 代码

```python
rdd = sc.parallelize([1, 2, 3, 4, 5, 6], 3)
print(rdd.getNumPartitions())
print(rdd.collect())
```

## 预期现象

```python
3
[1, 2, 3, 4, 5, 6]
```

## 你该理解什么

* 第二个参数 `3` 表示 3 个分区
* 后续执行时通常会对应多个 Task

---

# 实验 4：用 glom 看每个分区里有什么

## 目的

理解：

* 分区不是抽象概念
* 每个分区里真有一部分数据

## 代码

```python
rdd = sc.parallelize([1, 2, 3, 4, 5, 6], 3)
print(rdd.glom().collect())
```

## 预期现象

类似：

```python
[[1, 2], [3, 4], [5, 6]]
```

也可能分布略有不同。

## 你该理解什么

* `glom()`：把每个分区里的元素收成一个列表
* 结果是“按分区查看数据”

---

# 实验 5：map 转换

## 目的

理解：

* `map` 是一对一转换
* transformation 是惰性执行

## 代码

```python
rdd = sc.parallelize([1, 2, 3, 4, 5], 2)
rdd2 = rdd.map(lambda x: x * 10)

print(rdd2)
print(rdd2.collect())
```

## 预期现象

```python
PythonRDD...
[10, 20, 30, 40, 50]
```

## 你该理解什么

* `map()` 不会立刻执行真正计算
* 只有 `collect()` 这种 action 出现时，才触发执行

---

# 实验 6：filter 过滤

## 目的

理解：

* 过滤操作怎么做
* transformation + action 的配合

## 代码

```python
rdd = sc.parallelize([1, 2, 3, 4, 5, 6], 2)
rdd2 = rdd.filter(lambda x: x % 2 == 0)
print(rdd2.collect())
```

## 预期现象

```python
[2, 4, 6]
```

## 你该理解什么

* `filter()` 保留满足条件的数据
* 这是 transformation

---

# 实验 7：flatMap 和 map 的区别

## 目的

理解：

* `map`：一条进去，一条出来
* `flatMap`：一条进去，多条出来，再打平

## 代码 1：map

```python
rdd = sc.parallelize(["hello spark", "hello docker"], 2)
result = rdd.map(lambda line: line.split(" "))
print(result.collect())
```

## 预期现象

```python
[['hello', 'spark'], ['hello', 'docker']]
```

## 代码 2：flatMap

```python
rdd = sc.parallelize(["hello spark", "hello docker"], 2)
result = rdd.flatMap(lambda line: line.split(" "))
print(result.collect())
```

## 预期现象

```python
['hello', 'spark', 'hello', 'docker']
```

## 你该理解什么

* `map` 保留嵌套结构
* `flatMap` 会打平

---

# 实验 8：reduceByKey 做 WordCount

## 目的

理解：

* WordCount 最经典
* `reduceByKey` 会引入 Shuffle
* 会产生多个 Stage

## 代码

```python
rdd = sc.parallelize(
    ["hello spark", "hello docker", "spark docker", "hello hello"],
    4
)

result = (
    rdd.flatMap(lambda line: line.split(" "))
       .map(lambda word: (word, 1))
       .reduceByKey(lambda a, b: a + b)
)

print(result.collect())
```

## 预期现象

类似：

```python
[('hello', 4), ('spark', 2), ('docker', 2)]
```

顺序可能不一样。

## 你该观察什么

* Master UI 上会出现一个应用
* 这个 Job 通常不止一个 Stage
* 因为 `reduceByKey` 发生了 Shuffle

## 你该理解什么

* `reduceByKey` 是面试高频
* 比 `groupByKey` 更推荐

---

# 实验 9：groupByKey 和 reduceByKey 对比

## 目的

理解：

* 两者都能做聚合
* `reduceByKey` 更高效

## 代码 1：groupByKey

```python
rdd = sc.parallelize(
    [("a", 1), ("a", 2), ("b", 1), ("b", 3)],
    2
)

result = rdd.groupByKey().mapValues(lambda values: list(values))
print(result.collect())
```

## 预期现象

```python
[('a', [1, 2]), ('b', [1, 3])]
```

## 代码 2：reduceByKey

```python
rdd = sc.parallelize(
    [("a", 1), ("a", 2), ("b", 1), ("b", 3)],
    2
)

result = rdd.reduceByKey(lambda a, b: a + b)
print(result.collect())
```

## 预期现象

```python
[('a', 3), ('b', 4)]
```

## 你该理解什么

* `groupByKey`：先把所有值聚一起
* `reduceByKey`：先本地聚合，再全局聚合
* 所以通常 `reduceByKey` 更省网络、更高效

---

# 实验 10：cache 缓存

## 目的

理解：

* RDD 默认不缓存
* 重复 action 会重复算
* `cache()` 可以减少重复计算

## 代码

```python
rdd = sc.parallelize([1, 2, 3, 4, 5], 2).map(lambda x: x * 10)

rdd.cache()

print(rdd.collect())
print(rdd.collect())
```

## 预期现象

两次都输出：

```python
[10, 20, 30, 40, 50]
```

## 你该观察什么

如果你后面能看 4040 / Storage 页面，会看到缓存信息。

## 你该理解什么

* 不加 cache：每次 action 都可能重新算
* 加 cache：第一次算完后缓存，后面复用

---

# 实验 11：distinct 去重

## 目的

理解：

* 去重也是常用操作
* 去重通常涉及 Shuffle

## 代码

```python
rdd = sc.parallelize([1, 2, 2, 3, 3, 3, 4, 4], 3)
print(rdd.distinct().collect())
```

## 预期现象

```python
[1, 2, 3, 4]
```

顺序可能不同。

## 你该理解什么

* `distinct()` 经常伴随重新分布数据
* 可能产生 Shuffle

---

# 实验 12：union 合并两个 RDD

## 目的

理解：

* 怎么把两个 RDD 合并
* union 不是去重

## 代码

```python
rdd1 = sc.parallelize([1, 2, 3], 2)
rdd2 = sc.parallelize([3, 4, 5], 2)

rdd3 = rdd1.union(rdd2)
print(rdd3.collect())
```

## 预期现象

```python
[1, 2, 3, 3, 4, 5]
```

## 你该理解什么

* `union()` 只是拼接
* 不会自动去重

---

# 实验 13：intersection 交集

## 目的

理解：

* 两个 RDD 的交集
* 常见集合操作

## 代码

```python
rdd1 = sc.parallelize([1, 2, 3, 4], 2)
rdd2 = sc.parallelize([3, 4, 5, 6], 2)

print(rdd1.intersection(rdd2).collect())
```

## 预期现象

```python
[3, 4]
```

## 你该理解什么

* 这是集合交集
* 一般也会涉及数据重分布

---

# 实验 14：sortBy 排序

## 目的

理解：

* 排序怎么做
* 排序通常涉及全局重分布

## 代码

```python
rdd = sc.parallelize([5, 1, 3, 2, 4], 2)
print(rdd.sortBy(lambda x: x).collect())
print(rdd.sortBy(lambda x: x, ascending=False).collect())
```

## 预期现象

```python
[1, 2, 3, 4, 5]
[5, 4, 3, 2, 1]
```

## 你该理解什么

* 排序通常成本较高
* 面试里常问是不是宽依赖 / 会不会 Shuffle

---

# 实验 15：repartition 重新分区

## 目的

理解：

* 可以增加或减少分区
* `repartition` 通常会 Shuffle

## 代码

```python
rdd = sc.parallelize([1, 2, 3, 4, 5, 6], 2)
print(rdd.getNumPartitions())

rdd2 = rdd.repartition(4)
print(rdd2.getNumPartitions())
print(rdd2.glom().collect())
```

## 预期现象

```python
2
4
...
```

每个分区的数据分布可能不固定。

## 你该理解什么

* `repartition()` 会重新洗牌分区
* 用来调整并行度

---

# 实验 16：coalesce 减少分区

## 目的

理解：

* `coalesce` 更适合减少分区
* 比 `repartition` 更轻一些

## 代码

```python
rdd = sc.parallelize([1, 2, 3, 4, 5, 6], 4)
print(rdd.getNumPartitions())

rdd2 = rdd.coalesce(2)
print(rdd2.getNumPartitions())
print(rdd2.glom().collect())
```

## 预期现象

```python
4
2
...
```

## 你该理解什么

* `coalesce()` 常用于减少分区
* 通常比 `repartition()` 更省

---

# 实验 17：多个 action 触发多个 Job

## 目的

理解：

* 一个 action 常常触发一个 Job
* 多个 action 通常对应多个 Job

## 代码

```python
rdd = sc.parallelize([1, 2, 3, 4, 5], 3)

print(rdd.map(lambda x: x + 1).collect())
print(rdd.map(lambda x: x * 2).collect())
print(rdd.filter(lambda x: x % 2 == 0).collect())
```

## 预期现象

```python
[2, 3, 4, 5, 6]
[2, 4, 6, 8, 10]
[2, 4]
```

## 你该观察什么

如果能看 4040 / Jobs 页面，会看到 3 个 Job。

## 你该理解什么

* `collect()` 是 action
* 每次 action 都可能形成一个新 Job

---

# 实验 18：用文本文件做 textFile

## 目的

理解：

* 真实场景更常见的是读文件
* 不是只用 `parallelize`

先退出 PySpark：

```python
exit()
```

然后在 node1 容器中执行：

```bash
mkdir -p /root/data
cat > /root/data/test.txt <<'EOF'
apple banana
banana orange
apple orange banana
EOF
```

再重新进入 PySpark：

```bash
cd /root/spark
bin/pyspark --master spark://node1:7077
```

执行：

```python
rdd = sc.textFile("file:///root/data/test.txt")
print(rdd.collect())
```

## 预期现象

```python
['apple banana', 'banana orange', 'apple orange banana']
```

---

# 实验 19：完整文件版 WordCount

## 目的

把前面的知识串起来。

## 代码

```python
rdd = sc.textFile("file:///root/data/test.txt", 4)

result = (
    rdd.flatMap(lambda line: line.split(" "))
       .map(lambda word: (word, 1))
       .reduceByKey(lambda a, b: a + b)
       .sortBy(lambda x: x[0])
)

print(result.collect())
```

## 预期现象

```python
[('apple', 2), ('banana', 3), ('orange', 2)]
```

## 你该理解什么

这就是最经典的 Spark 面试和教学案例。

---

# 实验 20：保存结果

## 目的

理解：

* Spark 不只是 collect 回 Driver
* 也可以把结果输出到文件系统

在 PySpark 里执行：

```python
result = sc.parallelize([("a", 1), ("b", 2), ("c", 3)], 2)
result.saveAsTextFile("file:///root/output_test")
```

然后退出 PySpark：

```python
exit()
```

在 node1 shell 里执行：

```bash
ls -R /root/output_test
cat /root/output_test/part-*
```

## 预期现象

你会看到：

```text
('a', 1)
('b', 2)
('c', 3)
```

## 你该理解什么

* Spark 输出通常是目录，不是单文件
* 每个分区可能对应一个 `part-*` 文件

---

# 一套最推荐的学习顺序

如果你不想一次做太多，最建议按这个顺序练：

## 第 1 组：基础

先做这 5 个：

```python
# 1
rdd = sc.parallelize([1,2,3,4,5])
rdd.collect()

# 2
rdd.getNumPartitions()

# 3
rdd = sc.parallelize([1,2,3,4,5,6], 3)
rdd.glom().collect()

# 4
rdd.map(lambda x: x * 10).collect()

# 5
rdd.filter(lambda x: x % 2 == 0).collect()
```

---

## 第 2 组：字符串和 WordCount

再做这 4 个：

```python
rdd = sc.parallelize(["hello spark", "hello docker"], 2)
rdd.map(lambda line: line.split(" ")).collect()

rdd.flatMap(lambda line: line.split(" ")).collect()

rdd = sc.parallelize(["hello spark", "hello docker", "spark hello"], 4)
rdd.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b).collect()

rdd.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).groupByKey().mapValues(lambda values: list(values)).collect()
```

---

## 第 3 组：性能和分区

最后做这 4 个：

```python
rdd = sc.parallelize([1,2,3,4,5], 2).map(lambda x: x * 10)
rdd.cache()
rdd.collect()
rdd.collect()

rdd = sc.parallelize([1,2,3,4,5,6], 2)
rdd.repartition(4).glom().collect()

rdd = sc.parallelize([1,2,3,4,5,6], 4)
rdd.coalesce(2).glom().collect()

sc.parallelize([5,1,3,2,4], 2).sortBy(lambda x: x).collect()
```

---

# 你最该背下来的结论

## 1

`parallelize`：本地集合 -> RDD

## 2

`collect`：RDD -> Driver，本地 list

## 3

`map`：一对一转换

## 4

`flatMap`：一对多并打平

## 5

`filter`：过滤

## 6

`reduceByKey`：聚合，更高效

## 7

`groupByKey`：能用，但通常不如 `reduceByKey`

## 8

`cache`：避免重复计算

## 9

`repartition`：重新分区，常伴随 Shuffle

## 10

`coalesce`：通常用来减少分区

---

# 最后一套“面试演示版”

如果面试官让你快速展示几个常见 API，你可以直接跑这一套：

```python
rdd = sc.parallelize(["hello spark", "hello docker", "spark cluster", "hello hello"], 4)

print(rdd.getNumPartitions())
print(rdd.glom().collect())

words = rdd.flatMap(lambda line: line.split(" "))
print(words.collect())

pairs = words.map(lambda word: (word, 1))
print(pairs.collect())

counts = pairs.reduceByKey(lambda a, b: a + b)
print(counts.collect())

counts.cache()
print(counts.collect())
print(counts.collect())
```

---

如果你愿意，我下一条直接给你：

**“这 20 个实验整理成一份 A4 速记版”** 或者
**“每个实验对应的 Job / Stage / Task 应该怎么看”**



很好，你这一步 **已经基本成功了**。

# 你现在确认成功的点

从你贴的输出看：

* `ssh node2 hostname` 成功
* `ssh node3 hostname` 成功
* `java -version` 正常
* `JAVA_HOME` 正常
* `ping node2` 正常
* `ping node3` 正常
* `ssh root@node2 hostname` 正常
* `ssh root@node3 hostname` 正常

这说明：

## 结论

你已经完成了这几个关键目标：

* `node1 / node2 / node3` 三节点网络互通
* SSH 免密可用
* Java 环境可用
* `node1` 能远程访问 `node2` 和 `node3`

也就是说，**三节点基础环境已经搭好了**。

---

# 你输出里有两个需要解释的点

## 1）`bash: docker: command not found`

这个**完全正常**。

你执行的是：

```bash
docker exec -it node1 bash
```

但你当时已经在 `node1` 容器里面了，所以容器内部没有 `docker` 命令。

### 记住这个原则

* 在 **Mac 宿主机终端** 执行：

```bash
docker exec -it node1 bash
```

* 进入容器后，就不要再执行 `docker ...` 了
  因为容器里默认没有 Docker CLI。

### 你这次相当于：

* 已经在房间里了
* 又想在房间里用“进入房间”的命令
* 所以报错

这个不影响环境。

---

## 2）`/etc/hosts` 里目前只看到 `node1`

你贴出来的是：

```text
127.0.0.1 localhost
::1 localhost ip6-localhost ip6-loopback
fe00:: ip6-localnet
ff00:: ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
172.28.0.11 node1
```

这里说明：

* `node2`
* `node3`

**没有被写进 `/etc/hosts`**

但是你仍然能 ping 通、ssh 通，是因为：

## 原因

Docker 自带内部 DNS 解析。
同一个 Docker network 里的容器名本来就能互相解析。

所以即使 `/etc/hosts` 不完整，你现在仍然能连通。

---

# 现在建议你补一下 `/etc/hosts`

虽然现在能用，但为了更像真实集群，建议把三台机器都补全。

## 在宿主机执行

### 给 node1 写 hosts

```bash
docker exec -it node1 bash -c "cat > /etc/hosts <<'EOF'
127.0.0.1 localhost
::1 localhost ip6-localhost ip6-loopback
fe00:: ip6-localnet
ff00:: ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
172.28.0.11 node1
172.28.0.12 node2
172.28.0.13 node3
EOF"
```

### 给 node2 写 hosts

```bash
docker exec -it node2 bash -c "cat > /etc/hosts <<'EOF'
127.0.0.1 localhost
::1 localhost ip6-localhost ip6-loopback
fe00:: ip6-localnet
ff00:: ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
172.28.0.11 node1
172.28.0.12 node2
172.28.0.13 node3
EOF"
```

### 给 node3 写 hosts

```bash
docker exec -it node3 bash -c "cat > /etc/hosts <<'EOF'
127.0.0.1 localhost
::1 localhost ip6-localhost ip6-loopback
fe00:: ip6-localnet
ff00:: ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
172.28.0.11 node1
172.28.0.12 node2
172.28.0.13 node3
EOF"
```

---

# 然后验证

## 查看 node1

```bash
docker exec -it node1 bash
cat /etc/hosts
ping -c 2 node2
ping -c 2 node3
exit
```

## 查看 node2

```bash
docker exec -it node2 bash
cat /etc/hosts
ping -c 2 node1
ping -c 2 node3
exit
```

## 查看 node3

```bash
docker exec -it node3 bash
cat /etc/hosts
ping -c 2 node1
ping -c 2 node2
exit
```

---

# 你现在的阶段判断

你不是卡住了。
你现在其实已经完成了 **三节点 Docker 基础层**。

## 当前状态

你已经有：

* 3 个节点
* 节点名
* 网络互通
* SSH 互通
* Java 正常

这已经够进入下一步：

# 下一步

安装 Spark Standalone：

* `node1` 启动 Master
* `node2` 启动 Worker
* `node3` 启动 Worker

---

# 你刚才那段输出，面试角度怎么解释

你可以这样理解：

* `ping` 成功 → 网络层通
* `ssh` 成功 → 远程访问通
* `java -version` 成功 → Spark 运行依赖满足
* `JAVA_HOME` 正确 → 环境变量正确
* `/etc/hosts` 不完整但通信成功 → Docker 内置 DNS 生效

---

# 最简结论

你现在不用回退，不用重做。
只需要：

1. 补全三个节点的 `/etc/hosts`
2. 继续装 Spark

先把上面 3 组 `hosts` 命令执行掉。
执行完后，把 `node1` 的 `cat /etc/hosts` 结果贴给我。



你这里是 **命令执行位置混了**，不是环境坏了。

# 发生了什么

你输入的是：

```bash
docker exec -it node2 bash
hostname
java -version
echo $JAVA_HOME
ping -c 2 node1
ping -c 2 node3
cat /etc/hosts
exit
root@node2:/opt# docker exec -it node3 bash
...
```

问题在于：

## 你当时还在 `node2` 容器里

所以这句：

```bash
docker exec -it node3 bash
```

是在 **node2 容器内部** 执行的，不是在 Mac 宿主机执行的。

而容器里没有 Docker 命令，所以报错：

```bash
bash: docker: command not found
```

然后你后面那几条：

```bash
hostname
java -version
echo $JAVA_HOME
ping -c 2 node1
ping -c 2 node2
cat /etc/hosts
```

其实已经不是在 `node3` 里执行了，而是在 **你的 Mac 本机** 执行了。
所以才会出现：

* 主机名变成 `Yonggans-MacBook-Pro.local`
* Java 变成你 Mac 上的 Java 17
* `ping node1` 解析失败

这说明 **最后那一段根本不是 node3 的结果**。

---

# 你现在的真实状态

## node2 是正常的

你贴的 node2 输出说明：

* hostname 正常：`node2`
* Java 正常：11
* ping `node1` 正常
* ping `node2` 正常
* `/etc/hosts` 里目前只有：

  ```text
  172.28.0.12 node2
  ```

## node3 目前还没有正确检查

因为你并没有真正进入 node3。

## node1 / node2 / node3 网络本身大概率没问题

因为你前面已经验证过：

* node1 可以 ping node2 / node3
* node1 可以 ssh node2 / node3

所以现在不是网络挂了，而是 **终端上下文弄错了**。

---

# 现在正确做法

## 先回到 Mac 宿主机终端

你现在提示符应该像这样：

```bash
(base) yonggan@Yonggans-MacBook-Pro docker-spark-3nodes %
```

只有在这个提示符下，才能执行：

```bash
docker exec -it ...
```

---

# 第一步：正确检查 node3

请在 **Mac 宿主机** 执行下面这一整段：

```bash
docker exec -it node3 bash
hostname
java -version
echo $JAVA_HOME
ping -c 2 node1
ping -c 2 node2
cat /etc/hosts
exit
```

你应该看到：

* hostname = `node3`
* Java 11
* ping node1 成功
* ping node2 成功

---

# 第二步：一次性补全三个节点的 `/etc/hosts`

你现在 `node1` 和 `node2` 的 `/etc/hosts` 都还没补全。
直接在 **Mac 宿主机** 运行下面三段。

## 写 node1

```bash
docker exec -it node1 bash -c "cat > /etc/hosts <<'EOF'
127.0.0.1 localhost
::1 localhost ip6-localhost ip6-loopback
fe00:: ip6-localnet
ff00:: ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
172.28.0.11 node1
172.28.0.12 node2
172.28.0.13 node3
EOF"
```

## 写 node2

```bash
docker exec -it node2 bash -c "cat > /etc/hosts <<'EOF'
127.0.0.1 localhost
::1 localhost ip6-localhost ip6-loopback
fe00:: ip6-localnet
ff00:: ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
172.28.0.11 node1
172.28.0.12 node2
172.28.0.13 node3
EOF"
```

## 写 node3

```bash
docker exec -it node3 bash -c "cat > /etc/hosts <<'EOF'
127.0.0.1 localhost
::1 localhost ip6-localhost ip6-loopback
fe00:: ip6-localnet
ff00:: ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
172.28.0.11 node1
172.28.0.12 node2
172.28.0.13 node3
EOF"
```

---

# 第三步：重新验证三个节点

## 验证 node1

```bash
docker exec -it node1 bash
hostname
ping -c 2 node2
ping -c 2 node3
cat /etc/hosts
exit
```

## 验证 node2

```bash
docker exec -it node2 bash
hostname
ping -c 2 node1
ping -c 2 node3
cat /etc/hosts
exit
```

## 验证 node3

```bash
docker exec -it node3 bash
hostname
ping -c 2 node1
ping -c 2 node2
cat /etc/hosts
exit
```

---

# 你要记住的最重要规则

## 规则 1

看到这种提示符：

```bash
(base) yonggan@Yonggans-MacBook-Pro ...
```

说明你在 **Mac 宿主机**

这时可以运行：

```bash
docker exec -it node1 bash
docker exec -it node2 bash
docker exec -it node3 bash
```

---

## 规则 2

看到这种提示符：

```bash
root@node1:/opt#
root@node2:/opt#
root@node3:/opt#
```

说明你已经在 **容器内部**

这时 **不要再执行**：

```bash
docker exec ...
```

因为容器里没有 Docker。

---

# 你现在不用重做

你的环境没有崩。
只是：

* `node3` 还没正确检查
* `/etc/hosts` 还没补全
* 命令上下文混了

---

# 你现在只做这一件事

在 **Mac 宿主机** 按顺序执行：

1. 上面那 3 段 `/etc/hosts` 写入命令
2. 再执行 node3 检查命令

然后把这三段结果贴出来就行：

```bash
docker exec -it node1 bash -c "cat /etc/hosts"
docker exec -it node2 bash -c "cat /etc/hosts"
docker exec -it node3 bash -c "cat /etc/hosts"
```


你现在已经 **成功进入 node3 了**。
看到这个：

```bash
root@node3:/opt#
```

就说明你已经在 **node3 容器内部**。

你现在就在这个提示符后面，**一行一行输入下面这些命令**：

```bash
hostname
java -version
echo $JAVA_HOME
ping -c 2 node1
ping -c 2 node2
cat /etc/hosts
exit
```

注意：

* **不要输入** `root@node3:/opt#`
* **不要输入** `--`
* 只输入我上面那 6 行命令

---

## 你现在应该这样操作

在当前这个位置：

```bash
root@node3:/opt#
```

先输入：

```bash
hostname
```

回车后再输入下一行：

```bash
java -version
```

再继续：

```bash
echo $JAVA_HOME
ping -c 2 node1
ping -c 2 node2
cat /etc/hosts
exit
```

---

## 你应该期待看到什么

正常的话应该类似这样：

```bash
node3
```

```bash
openjdk version "11..."
```

```bash
/usr/lib/jvm/java-11-openjdk-amd64
```

`ping node1` 和 `ping node2` 应该都成功。

---

## 如果 `/etc/hosts` 还是不完整

退出回到 Mac 终端后，再执行这 3 条：

```bash
docker exec -it node1 bash -c "cat > /etc/hosts <<'EOF'
127.0.0.1 localhost
::1 localhost ip6-localhost ip6-loopback
fe00:: ip6-localnet
ff00:: ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
172.28.0.11 node1
172.28.0.12 node2
172.28.0.13 node3
EOF"
```

```bash
docker exec -it node2 bash -c "cat > /etc/hosts <<'EOF'
127.0.0.1 localhost
::1 localhost ip6-localhost ip6-loopback
fe00:: ip6-localnet
ff00:: ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
172.28.0.11 node1
172.28.0.12 node2
172.28.0.13 node3
EOF"
```

```bash
docker exec -it node3 bash -c "cat > /etc/hosts <<'EOF'
127.0.0.1 localhost
::1 localhost ip6-localhost ip6-loopback
fe00:: ip6-localnet
ff00:: ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
172.28.0.11 node1
172.28.0.12 node2
172.28.0.13 node3
EOF"
```

然后验证：

```bash
docker exec -it node1 bash -c "cat /etc/hosts"
docker exec -it node2 bash -c "cat /etc/hosts"
docker exec -it node3 bash -c "cat /etc/hosts"
```

你先把 `node3` 里这几条命令的输出贴出来：

```bash
hostname
java -version
echo $JAVA_HOME
ping -c 2 node1
ping -c 2 node2
cat /etc/hosts
```


你现在这个状态其实是 **两件事混在一起了**，我帮你一刀切清楚👇

---

# 🧠 一、你现在发生了什么

你这段输出：

```text
/Users/yonggan/Library/Java/JavaVirtualMachines/...
ping: cannot resolve node1
```

说明：

👉 **你现在不在 Docker 容器里，而是在 Mac 本机终端里**

因为：

* 路径是 `/Users/...`（Mac）
* Java 是 17（你本机）
* `node1` 解析失败（本机没有 Docker DNS）

---

# ❗为什么会这样？

你之前在容器里执行了：

```bash
exit
```

👉 你已经 **退出容器，回到 Mac 了**

---

# 🧯 二、你问的“怎么结束”

你看到：

```text
[Process completed]
```

👉 已经结束了，不用再结束

---

# ✅ 正确操作方式（非常重要）

以后记住这两个环境：

---

## 🟢 1. Mac 宿主机（可以用 docker）

提示符长这样：

```bash
(base) yonggan@Yonggans-MacBook-Pro %
```

👉 在这里才能运行：

```bash
docker exec -it node1 bash
docker exec -it node2 bash
docker exec -it node3 bash
```

---

## 🔵 2. 容器内部（不能用 docker）

提示符长这样：

```bash
root@node1:/opt#
root@node2:/opt#
root@node3:/opt#
```

👉 在这里不能运行：

```bash
docker exec ❌
```

---

# 🔥 三、你现在的问题本质

👉 node3 的 `/etc/hosts` 还没配好

因为你在 node3 里看到：

```text
ping: cannot resolve node1
```

说明：

👉 node3 不认识 node1 / node2

---

# ⚡ 四、一键修复（最关键）

现在 **回到 Mac 终端**（你已经在了）

直接执行👇（3条）

---

## 修 node1

```bash
docker exec -it node1 bash -c "cat > /etc/hosts <<'EOF'
127.0.0.1 localhost
::1 localhost ip6-localhost ip6-loopback
fe00:: ip6-localnet
ff00:: ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
172.28.0.11 node1
172.28.0.12 node2
172.28.0.13 node3
EOF"
```

---

## 修 node2

```bash
docker exec -it node2 bash -c "cat > /etc/hosts <<'EOF'
127.0.0.1 localhost
::1 localhost ip6-localhost ip6-loopback
fe00:: ip6-localnet
ff00:: ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
172.28.0.11 node1
172.28.0.12 node2
172.28.0.13 node3
EOF"
```

---

## 修 node3（你现在最需要的）

```bash
docker exec -it node3 bash -c "cat > /etc/hosts <<'EOF'
127.0.0.1 localhost
::1 localhost ip6-localhost ip6-loopback
fe00:: ip6-localnet
ff00:: ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
172.28.0.11 node1
172.28.0.12 node2
172.28.0.13 node3
EOF"
```

---

# 🧪 五、验证（必须做）

```bash
docker exec -it node3 bash
```

然后在 node3 里执行：

```bash
hostname
ping -c 2 node1
ping -c 2 node2
cat /etc/hosts
exit
```

---

# ✅ 正确结果应该是

```text
node3
```

```text
PING node1 ...
64 bytes from node1 ...
```

```text
PING node2 ...
64 bytes from node2 ...
```

---

# 🎯 六、你现在进度

你已经完成：

* Docker 三节点 ✔️
* SSH ✔️
* Java ✔️
* 网络（node1）✔️
* node3 hosts ❌（正在修）

👉 修完这一步，你就可以：

🔥 下一步直接启动 Spark 集群

---

# 🚀 下一步（马上可以做）

等你验证成功后，直接说：

👉 **继续**

我带你：

* 启动 Spark Master（node1）
* 启动 Worker（node2 / node3）
* 打开 Web UI（8080）
* 跑 SparkPi（真实集群运行）

一步到位，不再卡 👍


很好，这个问题其实很简单👇

# 🧠 你现在的状态

你看到：

```text
[Process completed]
```

👉 说明：

**这个终端会话已经结束了（关闭了）**

所以：

👉 ❗你当然“不能输入任何东西”了

---

# 🚨 为什么会这样

你刚才是在：

👉 **PyCharm / VSCode / 某个内置终端窗口**

运行了一个命令（可能是 ssh 或 docker exec）

执行完后：

👉 这个窗口自动结束了（不是交互式 shell）

---

# ✅ 正确做法（2种）

---

## 🟢 方法 1（推荐）：用 Mac Terminal

打开一个新的终端窗口：

### 👉 Mac 操作

* `Command + Space`
* 输入 `Terminal`
* 回车

你会看到：

```bash
(base) yonggan@Yonggans-MacBook-Pro %
```

---

然后重新进入 node3：

```bash
docker exec -it node3 bash
```

你应该看到：

```bash
root@node3:/opt#
```

👉 这才是“可以输入”的状态

---

## 🔵 方法 2：用 IDE 但要开交互终端

如果你用 PyCharm / VSCode：

👉 不要用 “Run”
👉 要用 “Terminal” 面板

---

# 🔥 快速判断你在哪个环境

## ❌ 错误状态（不能输入）

```text
[Process completed]
```

👉 结束了

---

## ✅ 正确状态（可以输入）

### Mac 终端：

```bash
(base) yonggan@Yonggans-MacBook-Pro %
```

### 容器里：

```bash
root@node3:/opt#
```

---

# ⚡ 你现在只需要做这一步

👉 打开一个新的 Terminal

然后执行：

```bash
docker exec -it node3 bash
```

然后执行：

```bash
hostname
ping -c 2 node1
ping -c 2 node2
```

---

# 🎯 如果还是卡住

你可以直接做一个“强制恢复”：

```bash
docker ps
```

确认 node3 在跑

如果不在：

```bash
docker compose up -d
```

---

# 🧾 一句话总结

👉
**[Process completed] = 这个窗口已经结束，不是卡住，是已经退出了**

---

你现在重新开 Terminal，进去 node3，把这三条输出贴我👇：

```bash
hostname
ping -c 2 node1
ping -c 2 node2
```

我帮你确认下一步直接进 Spark 🚀


给你一份 **Linux 高频参数速记表（面试直接背版）**👇
👉 核心目标：**看到 -v / -f / -n / -r 能快速说出“通用语义 + 常见命令”**

---

# 🚀 Linux 参数高频总结（直接背）

---

# 🧠 一、-v（verbose）

### 👉 含义

**显示详细过程（verbose）**

---

### ✅ 常见命令

```bash
cp -v file1 file2
mv -v file1 file2
rm -v file
```

---

### 🎯 面试一句话

👉
**-v means verbose, used to show detailed execution output**

---

### 📌 记忆点

👉
“我做了什么，都告诉你”

---

# ⚡ 二、-f（force）

### 👉 含义

**强制执行，不询问（force）**

---

### ✅ 常见命令

```bash
rm -f file
cp -f file1 file2
mv -f file1 file2
```

---

### 🎯 面试一句话

👉
**-f forces the operation without confirmation**

---

### ⚠️ 高危点（面试加分）

```bash
rm -rf /
```

👉
递归 + 强制删除（极其危险）

---

# 🔢 三、-n（number / no overwrite）

### 👉 含义（根据命令不同）

## 1）显示行号（number）

```bash
cat -n file.txt
nl file.txt
```

👉 给每一行加编号

---

## 2）不覆盖（no overwrite）

```bash
cp -n file1 file2
mv -n file1 file2
```

👉 目标存在就不覆盖

---

### 🎯 面试一句话

👉
**-n usually means number or no-overwrite depending on command**

---

# 🔁 四、-r（recursive）

### 👉 含义

**递归处理目录（recursive）**

---

### ✅ 常见命令

```bash
rm -r dir
cp -r dir1 dir2
chmod -r ???（❌没有）
```

---

### 🎯 面试一句话

👉
**-r is used for recursive operations on directories**

---

### 📌 高频组合

```bash
rm -rf dir
```

👉
递归 + 强制 = 删除整个目录

---

# 🔥 五、最常考组合（必须背）

---

## 1️⃣ rm -rf

```bash
rm -rf folder
```

👉 删除整个目录，不提示

---

## 2️⃣ cp -rv

```bash
cp -rv dir1 dir2
```

👉 递归复制 + 显示过程

---

## 3️⃣ mv -vf

```bash
mv -vf file1 file2
```

👉 强制移动 + 显示过程

---

## 4️⃣ cat -n

```bash
cat -n file.txt
```

👉 显示行号

---

# 🧠 六、面试思维（关键）

面试官不是让你死记命令，而是看你是否理解：

---

## 🎯 参数设计规律

| 参数 | 本质          |
| -- | ----------- |
| -v | 可观测性（debug） |
| -f | 强制执行        |
| -n | 安全（不覆盖）     |
| -r | 处理目录        |

---

## 🎯 一句话总结（强烈建议背）

👉
**Linux flags are usually shorthand for behavior: -v for visibility, -f for force, -n for safety, and -r for recursion.**

---

# 🧪 七、面试追问（你大概率会被问）

---

## ❓ Q1：为什么 rm -rf 很危险？

👉

* 不提示
* 递归删除
* 可能删系统

---

## ❓ Q2：-r 和 -R 区别？

👉
通常一样（recursive）

---

## ❓ Q3：为什么 cp -r 必须加 -r？

👉
默认 cp 不会复制目录

---

## ❓ Q4：什么时候用 -n？

👉
避免覆盖已有文件（安全）

---

# 📌 最后一页速记（你可以截图）

```text
-v → verbose → 打印过程
-f → force → 强制执行
-n → number / no overwrite → 行号 / 不覆盖
-r → recursive → 递归目录

经典：
rm -rf → 删除目录（危险）
cp -rv → 复制目录 + 打印
mv -vf → 强制移动 + 打印
cat -n → 显示行号
```

---

# 🚀 如果你要进阶（很推荐）

我可以给你👇

👉 Linux 50个面试高频命令（带场景）
👉 Bash + 文件系统 + 权限 一页总结
👉 AWS + Linux + DevOps 面试组合题

直接说：**要Linux面试全套** 👍
