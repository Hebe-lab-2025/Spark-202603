下面是我帮你整理好的 **Spark 环境部署笔记（精简 + 结构化版）**，方便你直接看、复制、做笔记。

---

# Spark 环境部署整理笔记

## 1. 下载地址

### Spark

* `https://dlcdn.apache.org/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz`
* 这是 **mac + Homebrew Python 的正常保护机制**，不是你装错了。

意思是：
👉 你现在的 `pip` 在系统管理的 Python 环境里，mac 不让你直接乱装包，怕把系统 Python 或 Homebrew 搞坏。

---

# 最推荐解决方法：用虚拟环境

直接复制下面这几行：

```bash
python3 -m venv ~/spark-env
source ~/spark-env/bin/activate
pip install pyspark
```

安装完后检查：

```bash
python --version
pip --version
python -c "import pyspark; print(pyspark.__version__)"
```

---

# 以后怎么用

每次要用 Spark 前，先开环境：

```bash
source ~/spark-env/bin/activate
```

然后启动：

```bash
pyspark
```

---

# 如果提示没有 venv

先装：

```bash
python3 -m ensurepip --upgrade
```

如果还是不行，再告诉我报错。

---

# 不推荐但能用的方法

你也可以强行装：

```bash
pip install pyspark --break-system-packages
```

但这个不稳，容易把 Homebrew Python 搞乱。
**你现在不要用这个。**

---

# 你现在该走的完整流程

```bash
python3 -m venv ~/spark-env
source ~/spark-env/bin/activate
pip install pyspark
pyspark
```

---

# 这个错误一句话理解

**PEP 668** 在阻止你往系统 Python 里直接装第三方包，所以要改用虚拟环境。

把你下一步终端输出发我，我可以直接帮你继续看。


### 环境要求

* **Python**：推荐 `3.8`
* **JDK**：`1.8`
* **Anaconda**
* Linux 和 Windows 都需要配置 Python 环境

---

# 2. Spark Local 模式部署

## 2.1 上传并解压 Spark

把安装包上传到 Linux 服务器后，执行：

```bash
tar -zxvf spark-3.2.0-bin-hadoop3.2.tgz -C /export/server/
```

由于目录名太长，建议创建软链接：

```bash
ln -s /export/server/spark-3.2.0-bin-hadoop3.2 /export/server/spark
```

---

## 2.2 环境变量配置

需要配置以下 **5 个环境变量**：

* `SPARK_HOME`：Spark 安装路径
* `PYSPARK_PYTHON`：Spark 运行 Python 程序时使用的 Python 解释器
* `JAVA_HOME`：JDK 安装路径
* `HADOOP_CONF_DIR`：Hadoop 配置文件路径
* `HADOOP_HOME`：Hadoop 安装路径

### 配置位置

* 这 5 个变量都需要配置到：

  * `/etc/profile`
* 其中这 2 个还需要额外配置到：

  * `/root/.bashrc`
  * `PYSPARK_PYTHON`
  * `JAVA_HOME`

---

## 2.3 测试 Local 模式

### 1）pyspark 解释器

```bash
bin/pyspark
```

这个命令会进入交互式 Python + Spark 环境。

可以测试：

```python
sc.parallelize([1,2,3,4,5]).map(lambda x: x + 1).collect()
```

---

### 2）Spark Web UI

Spark 程序运行时默认绑定：

* `4040`
* 如果 4040 被占用，会顺延到 `4041`、`4042` ...

浏览器访问：

```bash
服务器IP:4040
```

在 Local 模式下：

* 只有一个 **Driver**
* 因为是 Local 模式，Driver 既负责管理，也负责执行任务

---

### 3）查看进程

```bash
jps
```

Local 模式下通常只有一个 Spark 相关进程。

---

## 2.4 spark-shell（Scala）

```bash
bin/spark-shell
```

这是 Scala 的交互式环境，不是 Python。

测试代码：

```scala
sc.parallelize(Array(1,2,3,4,5)).map(x => x + 1).collect()
```

结果：

```scala
Array(2, 3, 4, 5, 6)
```

---

## 2.5 spark-submit

用于正式提交 Spark 程序运行。

### 语法

```bash
bin/spark-submit [选项] jar包或python文件路径 [程序参数]
```

### 示例：运行官方 PI 程序

```bash
bin/spark-submit /export/server/spark/examples/src/main/python/pi.py 10
```

说明：

* `10` 是主函数参数
* 数字越大，圆周率估算越准确

---

## 2.6 三个命令对比

| 工具                 | 功能                                    | 使用场景                 |
| ------------------ | ------------------------------------- | -------------------- |
| `bin/spark-submit` | 提交 Java / Scala / Python 程序到 Spark 运行 | 正式运行程序               |
| `bin/pyspark`      | Python 交互式解释器环境                       | 学习、测试、写一行跑一行         |
| `bin/spark-shell`  | Scala 交互式解释器环境                        | 学习、测试 Scala Spark 代码 |

### 结论

* **Local 模式** 是 7 天 Spark 课程的主力模式
* 学习用 `pyspark`
* 正式提交用 `spark-submit`

---

# 3. Spark Standalone 集群部署

---

## 3.1 历史服务器（History Server）

### 作用

记录 Spark 程序运行历史，方便后续查看历史日志和作业信息。

### 是否必须

* **不是必须**
* 但集群环境中 **强烈建议配置**

---

## 3.2 集群规划

课程中使用三台 Linux 虚拟机：

* `node1`
* `node2`
* `node3`

### 角色分配

* `node1`

  * 1 个 Master
  * 1 个 Worker
* `node2`

  * 1 个 Worker
* `node3`

  * 1 个 Worker

### 集群总共

* `1 个 Master`
* `3 个 Worker`

---

## 3.3 所有机器都要做的事

### 1）安装 Python（Anaconda）

参考附录：Linux 上安装 Anaconda

### 2）创建虚拟环境

### 3）安装依赖包

* `pyspark`
* `jieba`
* `pyhive`

### 4）配置环境变量

和 Local 模式一致，三台机器都要配好。

---

## 3.4 配置 workers 文件

进入目录：

```bash
cd $SPARK_HOME/conf
```

重命名：

```bash
mv workers.template workers
```

编辑 `workers` 文件，删除 `localhost`，加入：

```bash
node1
node2
node3
```

### 作用

告诉 Spark Standalone 集群有哪些 Worker 节点。

---

## 3.5 配置 spark-env.sh

重命名：

```bash
mv spark-env.sh.template spark-env.sh
```

在文件底部追加：

```bash
JAVA_HOME=/export/server/jdk
HADOOP_CONF_DIR=/export/server/hadoop/etc/hadoop
YARN_CONF_DIR=/export/server/hadoop/etc/hadoop

export SPARK_MASTER_HOST=node1
export SPARK_MASTER_PORT=7077
SPARK_MASTER_WEBUI_PORT=8080

SPARK_WORKER_CORES=1
SPARK_WORKER_MEMORY=1g
SPARK_WORKER_PORT=7078
SPARK_WORKER_WEBUI_PORT=8081

SPARK_HISTORY_OPTS="-Dspark.history.fs.logDirectory=hdfs://node1:8020/sparklog/ -Dspark.history.fs.cleaner.enabled=true"
```

### 说明

* `SPARK_MASTER_HOST`：Master 节点主机名
* `SPARK_MASTER_PORT`：Master 通讯端口
* `SPARK_MASTER_WEBUI_PORT`：Master UI 端口
* `SPARK_WORKER_CORES`：每个 Worker 可用 CPU 核数
* `SPARK_WORKER_MEMORY`：每个 Worker 可用内存
* `SPARK_HISTORY_OPTS`：历史日志配置

---

## 3.6 创建 Spark 历史日志目录

在 HDFS 上创建目录：

```bash
hadoop fs -mkdir /sparklog
hadoop fs -chmod 777 /sparklog
```

---

## 3.7 配置 spark-defaults.conf

重命名：

```bash
mv spark-defaults.conf.template spark-defaults.conf
```

追加：

```bash
spark.eventLog.enabled true
spark.eventLog.dir hdfs://node1:8020/sparklog/
spark.eventLog.compress true
```

### 作用

开启 Spark 历史日志记录功能。

---

## 3.8 配置 log4j.properties（可选）

重命名：

```bash
mv log4j.properties.template log4j.properties
```

建议把日志级别改成 `WARN`

### 原因

Spark 默认日志很多，像“话痨”一样。
改成 `WARN` 后：

* 只输出警告和错误
* 日志更干净

---

## 3.9 分发 Spark 到其他节点

```bash
scp -r spark-3.1.2-bin-hadoop3.2 node2:/export/server/
scp -r spark-3.1.2-bin-hadoop3.2 node3:/export/server/
```

然后在 `node2` 和 `node3` 上也创建软链接：

```bash
ln -s /export/server/spark-3.1.2-bin-hadoop3.2 /export/server/spark
```

---

## 3.10 检查环境变量

每台机器都要检查：

* `JAVA_HOME`
* `SPARK_HOME`
* `PYSPARK_PYTHON`

确保都指向正确目录。

---

## 3.11 启动集群

### 启动历史服务器

```bash
sbin/start-history-server.sh
```

### 启动全部 Master 和 Worker

```bash
sbin/start-all.sh
```

### 单独启动

```bash
sbin/start-master.sh
sbin/start-worker.sh
```

### 停止

```bash
sbin/stop-all.sh
sbin/stop-master.sh
sbin/stop-worker.sh
```

---

## 3.12 查看 Master Web UI

默认端口：

* `8080`
* 如果被占用，会顺延到 `8081`、`8082` ...

日志里会提示：

```bash
Service 'MasterUI' could not bind on port 8080. Attempting port 8081.
```

---

## 3.13 连接到 Standalone 集群

### pyspark

```bash
bin/pyspark --master spark://node1:7077
```

### spark-shell

```bash
bin/spark-shell --master spark://node1:7077
```

### spark-submit

```bash
bin/spark-submit --master spark://node1:7077 /export/server/spark/examples/src/main/python/pi.py 100
```

如果不写 `--master`，默认就是 Local 模式。

---

## 3.14 查看历史服务器 UI

历史服务器默认端口：

* `18080`

访问：

```bash
node1:18080
```

---

# 4. Spark Standalone HA 高可用部署

---

## 4.1 前提

需要先确保：

* `Zookeeper` 已启动
* `HDFS` 已启动

---

## 4.2 修改 spark-env.sh

### 删除

```bash
SPARK_MASTER_HOST=node1
```

### 原因

固定 Master 后，无法使用 Zookeeper 的动态主备切换。

---

### 增加

```bash
SPARK_DAEMON_JAVA_OPTS="-Dspark.deploy.recoveryMode=ZOOKEEPER -Dspark.deploy.zookeeper.url=node1:2181,node2:2181,node3:2181 -Dspark.deploy.zookeeper.dir=/spark-ha"
```

### 含义

* `spark.deploy.recoveryMode=ZOOKEEPER`

  * 使用 Zookeeper 实现 HA
* `spark.deploy.zookeeper.url`

  * Zookeeper 地址
* `spark.deploy.zookeeper.dir`

  * Spark 在 ZK 中注册临时节点的路径

---

## 4.3 分发配置到其他机器

```bash
scp spark-env.sh node2:/export/server/spark/conf/
scp spark-env.sh node3:/export/server/spark/conf/
```

---

## 4.4 重启集群

先停掉：

```bash
sbin/stop-all.sh
```

### 在 node1 上启动

```bash
sbin/start-all.sh
```

### 在 node2 上额外启动一个备用 Master

```bash
sbin/start-master.sh
```

---

## 4.5 主备切换测试

提交任务：

```bash
bin/spark-submit --master spark://node1:7077 /export/server/spark/examples/src/main/python/pi.py 1000
```

提交成功后，把当前活跃 Master 直接 kill 掉。

### 结果

* 任务不会失败
* 新 Master 接管后，程序继续执行
* 可能会中断约 **30 秒**

### 结论

HA 模式下，Master 切换不会影响正在运行的程序。

---

# 5. Spark on YARN 部署

---

## 5.1 前提

确保以下变量已经配置在：

* `spark-env.sh`
* 系统环境变量文件中

需要有：

* `HADOOP_CONF_DIR`
* `YARN_CONF_DIR`

---

## 5.2 连接到 YARN

### pyspark

```bash
bin/pyspark --master yarn --deploy-mode client
```

### spark-shell

```bash
bin/spark-shell --master yarn --deploy-mode client
```

### spark-submit

```bash
bin/spark-submit --master yarn --deploy-mode client|cluster /xxx/xxx/xxx.py
```

---

## 5.3 deploy-mode 说明

* `client`

  * Driver 在客户端运行
* `cluster`

  * Driver 在集群里运行

### 注意

交互式工具：

* `pyspark`
* `spark-shell`

**不能使用 `cluster` 模式**

只有 `spark-submit` 才适合正式跑 `cluster` 模式。

---

# 6. Linux 安装 Anaconda

---

## 6.1 安装

上传安装包：

* `Anaconda3-2021.05-Linux-x86_64.sh`

执行：

```bash
sh ./Anaconda3-2021.05-Linux-x86_64.sh
```

一路输入 `yes` 即可。

安装完成后，重新登录终端。
如果看到类似：

```bash
(base)
```

说明安装成功。

---

## 6.2 如果没有看到 base

可以检查 `/root/.bashrc`，并配置国内源。

---

## 6.3 Anaconda 国内源配置

可写入 `.condarc`：

```yaml
channels:
  - defaults
show_channel_urls: true
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
```

---

# 7. Windows 安装 Anaconda

---

## 7.1 安装步骤

安装文件：

* `Anaconda3-2021.05-Windows-x86_64.exe`

安装时一直点 **Next** 即可。

### 注意

* 可以修改安装路径
* 某些额外勾选项不一定要选

安装完成后，在开始菜单搜索 **Anaconda Prompt**。

打开后如果看到：

```bash
(base)
```

说明安装成功。

---

## 7.2 Windows 配置国内源

先执行：

```bash
conda config --set show_channel_urls yes
```

然后编辑：

```bash
C:\Users\用户名\.condarc
```

填入和 Linux 一样的国内源配置。

---

## 7.3 创建 pyspark 虚拟环境

```bash
conda create -n pyspark python=3.8
conda activate pyspark
pip install pyhive pyspark jieba -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

# 8. Spark 常用客户端工具参数

常用 4 个客户端工具：

* `bin/pyspark`
* `bin/spark-shell`
* `bin/spark-submit`
* `bin/spark-sql`

这几个工具参数基本通用。

---

## 8.1 常见参数

### 指定运行模式

```bash
--master
```

可选值：

* `spark://host:port`
* `yarn`
* `local`

---

### 指定部署模式

```bash
--deploy-mode client|cluster
```

默认：

* `client`

---

### 指定依赖

```bash
--jars
--packages
--py-files
--files
--archives
```

---

### 手动传配置

```bash
--conf key=value
```

---

### 资源相关

```bash
--driver-memory
--executor-memory
--executor-cores
--num-executors
--total-executor-cores
```

---

### 其他

```bash
--help
--verbose
--version
```

---

# 9. 最后总结

## 学习阶段重点

### 你最常用的会是这三个：

1. `bin/pyspark`

   * 学习、测试、交互运行
2. `bin/spark-submit`

   * 正式提交任务
3. `bin/spark-shell`

   * Scala 版本解释器，了解即可

---

## 模式区别

### Local 模式

* 单机运行
* 简单
* 适合学习和测试

### Standalone 模式

* 自己搭建 Spark 集群
* 有 Master / Worker

### HA 模式

* 用 Zookeeper 做主备切换
* Master 挂了可自动切换

### YARN 模式

* 依赖 Hadoop / YARN
* 企业里更常见

---

如果你要，我下一步可以继续帮你整理成 **“考试速记版”**，就是压缩成 1 页的重点背诵笔记。
