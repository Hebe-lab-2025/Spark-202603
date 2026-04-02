下面是你这几轮里**所有高频命令的完整速查表**，我按 **环境配置 → Hadoop/HDFS → YARN → Spark → 排错** 来整理，方便你直接保存。

# Spark + YARN + HDFS 全命令速查表

## 1. 环境变量

先配环境，不然很多命令会直接报错。

```bash
export HADOOP_CONF_DIR=/opt/homebrew/Cellar/hadoop/3.4.3/libexec/etc/hadoop
export YARN_CONF_DIR=/opt/homebrew/Cellar/hadoop/3.4.3/libexec/etc/hadoop
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH=$JAVA_HOME/bin:$PATH
```

作用：

* `HADOOP_CONF_DIR`：告诉 Hadoop / YARN 去哪里读配置。
* `YARN_CONF_DIR`：兼容变量，Hadoop 3 里主要还是看 `HADOOP_CONF_DIR`。
* `JAVA_HOME`：指定 Java 11。
* `PATH`：保证当前 shell 用的是这个 Java。

验证：

```bash
echo $HADOOP_CONF_DIR
echo $YARN_CONF_DIR
java -version
```

你日志里已经验证过，这样设置后 Java 11 和 Hadoop 配置目录都正确。

---

## 2. 查命令路径

确认你实际调用的是哪个程序。

```bash
which hdfs
which yarn
which spark-submit
```

作用：

* 防止系统里有多个版本，跑错。
* 你机器上分别指向 Homebrew Hadoop 和你自己的 Spark 安装。

---

## 3. 进入正确目录

很多脚本依赖相对路径，目录错了就会报文件不存在。

```bash
cd /Users/yonggan/Downloads/Spark-202603/learning/01_RDD
pwd
```

作用：

* 确保 `spark-submit xxx.py` 和相对路径数据文件都能找到。

---

# Hadoop / HDFS

## 4. 查看 HDFS 根目录

```bash
hdfs dfs -ls /
```

作用：

* 检查 HDFS 是否可访问。
* 这是最基础的连通性测试。

你日志里这条能列出 `/Users`、`/tmp` 等，说明当时 HDFS 命令已经可以连上文件系统。

---

## 5. 创建 HDFS 目录

```bash
hdfs dfs -mkdir -p /input
```

作用：

* 在 HDFS 里创建目录。
* `-p` 表示父目录不存在时也一起建。

---

## 6. 上传文件到 HDFS

```bash
hdfs dfs -put -f /Users/yonggan/Downloads/Spark-202603/data/input/order.text /input/
```

作用：

* 把本地文件上传到 HDFS。
* `-f` 表示目标已存在时覆盖。

你之前碰到过上传失败，不是命令本身错，而是当时 `DataNode` 没正常工作，所以 HDFS 没法写 block。

---

## 7. 查看 HDFS 某目录

```bash
hdfs dfs -ls /input
```

作用：

* 确认上传是否成功。

---

## 8. 启动 NameNode

```bash
hdfs namenode
```

作用：

* 直接前台启动 NameNode。

注意：

* 这一般不是日常推荐方式。
* 如果已经有 NameNode 在跑，会报：

```text
namenode is running as process ...
```

你就遇到过这个情况，说明已经有 NameNode 进程在跑。

---

## 9. 格式化 NameNode

```bash
hdfs namenode -format
```

作用：

* 初始化 HDFS 元数据。
* 只在第一次搭建，或者你明确要重置 HDFS 时使用。

注意：

* 会清空原来的 namespace。
* 如果 NameNode 正在运行，必须先停掉，不然会报不能 format。你日志里就出现过这个提示。

---

## 10. 启动 DataNode

```bash
hdfs datanode
```

作用：

* 前台启动 DataNode。

注意：

* 这是手动启动单个 DataNode。
* 平时更推荐用 `start-dfs.sh`。
* 你多次直接运行它，这会有重复启动、端口冲突、进程管理混乱的风险。

---

## 11. 停止 / 启动 HDFS daemon

```bash
hdfs --daemon stop datanode
hdfs --daemon start datanode
```

作用：

* 后台方式管理 DataNode。

---

## 12. 一键启动 HDFS

```bash
start-dfs.sh
```

作用：

* 启动 NameNode、DataNode 等 HDFS 服务。

## 13. 一键停止 HDFS

```bash
stop-dfs.sh
```

作用：

* 停掉 HDFS 整套服务。

---

## 14. 清理 HDFS 本地数据目录

```bash
rm -rf /Users/yonggan/hadoop_data/hdfs/namenode/*
rm -rf /Users/yonggan/hadoop_data/hdfs/datanode/*
```

作用：

* 手动清空 NameNode / DataNode 的本地存储。

注意：

* 这是“重置 HDFS”级别操作。
* 只有你明确知道自己要重建 HDFS 时才做。
* 做完通常需要重新 format。

---

## 15. 查看 NameNode PID 文件

```bash
cat /tmp/hadoop-yonggan-namenode.pid
```

作用：

* 确认 Hadoop 记录的 NameNode PID。

---

## 16. 删除 PID 文件

```bash
rm -f /tmp/hadoop-yonggan-namenode.pid
rm -f /tmp/hadoop-yonggan-datanode.pid
```

作用：

* 当进程已经死掉，但 pid 文件残留时，手动清理。

---

## 17. 杀掉 NameNode 进程

```bash
pkill -f NameNode
```

作用：

* 强制结束 NameNode。

注意：

* 一般用于进程卡死或 pid 状态不一致时。

---

## 18. 看 DataNode 日志

```bash
tail -n 100 /opt/homebrew/var/hadoop/hadoop-yonggan-datanode-Yonggans-MacBook-Pro.local.log
```

作用：

* 这是最直接的 HDFS 排错命令。
* 看注册、heartbeat、block report、异常退出。

你日志里能看到：

* `successfully registered with NN`
* heartbeat
* block report
* `SIGTERM`

说明 DataNode 曾成功注册，也曾被正常停止。

---

# YARN

## 19. 启动 NodeManager

```bash
yarn nodemanager
```

作用：

* 前台启动 NodeManager。

注意：

* 一般不建议单独手动跑，除非你在调试。
* 你日志里启动后打印了很长的 STARTUP_MSG，但后面 `jps` 没保留 NodeManager，说明它没稳定跑住。

---

## 20. 后台启动 ResourceManager / NodeManager

```bash
yarn --daemon start resourcemanager
yarn --daemon start nodemanager
```

作用：

* 后台启动 YARN 的两个核心进程。

你用过这组命令，但当时有配置问题，最终没有稳定起来。

---

## 21. 后台停止 ResourceManager / NodeManager

```bash
yarn --daemon stop resourcemanager
yarn --daemon stop nodemanager
```

作用：

* 停 YARN 服务。

---

## 22. 一键启动 YARN

```bash
start-yarn.sh
```

作用：

* 启动整套 YARN。

## 23. 一键停止 YARN

```bash
stop-yarn.sh
```

作用：

* 停掉整套 YARN。

---

## 24. 查看 YARN 节点

```bash
yarn node -list
```

作用：

* 看 NodeManager 有没有注册到 ResourceManager。
* 这是 YARN 是否健康的核心检查。

正常时会看到：

```text
Total Nodes:1
localhost:xxxxx RUNNING
```

你也确实看到了这种正常状态。

异常时你看到过：

```text
Connecting to ResourceManager at /0.0.0.0:8032
Retrying ...
```

这说明 ResourceManager 地址配置错了。

---

## 25. 查看 YARN 应用

```bash
yarn application -list
```

作用：

* 查看当前提交到 YARN 的 Spark / MapReduce 作业。

## 26. 杀掉 YARN 应用

```bash
yarn application -kill <app_id>
```

作用：

* 杀掉某个卡住或占资源的应用。

---

# Spark

## 27. 本地直接跑 Python Spark 脚本

```bash
python 11_RDD_operators_union.py
python 12_RDD_operators_join.py
python 18_RDD_operators_demo.py
```

作用：

* 用默认 SparkContext 配置运行。
* 如果脚本里没显式指定 `master`，通常走 local。

你这几条里：

* `11_RDD_operators_union.py` 成功
* `12_RDD_operators_join.py` 成功
* `18_RDD_operators_demo.py` 一开始有路径和 API 拼写错误，后来修好后成功。

---

## 28. 提交 Spark 到 YARN

```bash
spark-submit --master yarn 19_RDD_operators_demo_run_yarn.py
```

作用：

* 用 YARN 作为资源调度器。

注意：

* 要先有正确的 `HADOOP_CONF_DIR` / `YARN_CONF_DIR`。
* 不然会报：

```text
either HADOOP_CONF_DIR or YARN_CONF_DIR must be set
```

你已经遇到并修复过这个问题。

---

## 29. 指定 deploy mode

```bash
spark-submit --master yarn --deploy-mode client 19_RDD_operators_demo_run_yarn.py
```

作用：

* Driver 在本机跑，executor 在 YARN 上跑。

---

## 30. 分发 Python 依赖

```bash
spark-submit \
  --master yarn \
  --py-files defs_19.py \
  19_RDD_operators_demo_run_yarn.py
```

作用：

* 把本地 Python 依赖文件传给 executor。

为什么必须：

* 你脚本 import 了 `defs_19`
* executor 不会自动看到你本机文件
* 不加会报：

```text
ModuleNotFoundError: No module named 'defs_19'
```

你后来加上 `--py-files defs_19.py` 后，job 成功完成。

---

## 31. 本地模式提交

```bash
spark-submit --master local[*] xxx.py
```

作用：

* 用本机多线程模拟集群。
* 常用于先验证脚本逻辑。

---

## 32. 进入交互式 shell

```bash
pyspark
```

作用：

* 进入 PySpark REPL。
* 里面才能直接写：

```python
sc.parallelize(range(100)).count()
```

你之前把这条写在 zsh 里了，所以 shell 报错。那个不是 Spark 错，是 shell 把括号当模式匹配了。

---

# 文件 / 路径 / 配置检查

## 33. 检查文件是否存在

```bash
ls -lh ../../data/input/order.text
```

作用：

* 确认相对路径没写错。

---

## 34. 查看 Hadoop 配置文件

```bash
cat /opt/homebrew/Cellar/hadoop/3.4.3/libexec/etc/hadoop/core-site.xml
cat /opt/homebrew/Cellar/hadoop/3.4.3/libexec/etc/hadoop/hdfs-site.xml
```

作用：

* 检查 `fs.defaultFS`
* 检查 `dfs.namenode.name.dir`
* 检查 `dfs.datanode.data.dir`

你日志里能看到这些值，比如：

* `hdfs://localhost:9000`
* `file:///Users/yonggan/hadoop_data/hdfs/...` 

---

## 35. 编辑配置文件

```bash
vim core-site.xml
vim hdfs-site.xml
vim /opt/homebrew/Cellar/hadoop/3.4.3/libexec/etc/hadoop/yarn-site.xml
```

作用：

* 修配置。

你重点改过的就是 `yarn-site.xml`。

---

## 36. 备份配置文件

```bash
cp /opt/homebrew/Cellar/hadoop/3.4.3/libexec/etc/hadoop/yarn-site.xml \
   /opt/homebrew/Cellar/hadoop/3.4.3/libexec/etc/hadoop/yarn-site.xml.bak
```

作用：

* 改配置前先备份。

---

## 37. 查找配置文件

```bash
find /opt/homebrew -name yarn-site.xml 2>/dev/null
```

作用：

* 找系统里到底有哪些 `yarn-site.xml`，避免改错文件。

---

## 38. 查看 Hadoop 安装目录

```bash
brew --prefix hadoop
ls /opt/homebrew/Cellar/hadoop/3.4.3/libexec
ls /opt/homebrew/Cellar/hadoop/3.4.3/libexec/bin
ls /opt/homebrew/Cellar/hadoop/3.4.3/libexec/sbin
ls /opt/homebrew/Cellar/hadoop/3.4.3/libexec/etc/hadoop
```

作用：

* 熟悉 Hadoop 的目录结构。
* 确认 `start-yarn.sh`、`start-dfs.sh`、配置文件都在哪里。

---

# Web UI / 误用命令

## 39. 想打开 Web UI

你输入过：

```bash
http://localhost:8088
```

这是错的。

原因：

* 这是 URL，不是 shell 命令。

正确方式：

* 直接复制到浏览器地址栏
* 或者 macOS 下：

```bash
open http://localhost:8088
open http://localhost:9870
open http://localhost:4040
```

分别对应：

* `8088`：YARN UI
* `9870`：HDFS NameNode UI
* `4040`：Spark UI

---

# 你踩过的典型坑，对应命令总结

## 坑 1：shell 里直接跑 PySpark 代码

错误示例：

```bash
sc.parallelize(range(100)).count()
```

问题：

* 这是 Python，不是 shell 命令。

正确：

* 进 `pyspark`
* 或写到 `.py` 文件里用 `spark-submit`

---

## 坑 2：路径不对

错误表现：

```text
can't open file ...
```

解决命令：

```bash
cd /Users/yonggan/Downloads/Spark-202603/learning/01_RDD
pwd
ls
```

---

## 坑 3：HADOOP_CONF_DIR / YARN_CONF_DIR 没设

错误表现：

```text
When running with master 'yarn' either HADOOP_CONF_DIR or YARN_CONF_DIR must be set
```

解决命令：

```bash
export HADOOP_CONF_DIR=...
export YARN_CONF_DIR=...
```

---

## 坑 4：Python 依赖没传给 executor

错误表现：

```text
ModuleNotFoundError: No module named 'defs_19'
```

解决命令：

```bash
spark-submit --master yarn --py-files defs_19.py 19_RDD_operators_demo_run_yarn.py
```

---

## 坑 5：Spark 还在连旧的 Standalone master

错误表现：

```text
Failed to connect to master node1:7077
UnknownHostException: node1
```

原因：

* 代码或配置里还残留了 `spark://node1:7077`

需要检查：

```bash
cat $SPARK_HOME/conf/spark-defaults.conf
```

以及你 Python 代码里的：

```python
conf.setMaster(...)
```

---

## 坑 6：YARN ResourceManager 地址配错

错误表现：

```text
Connecting to ResourceManager at /0.0.0.0:8032
```

原因：

* `yarn-site.xml` 配错了，RM 主机名没配对。

需要改：

```xml
<property>
  <name>yarn.resourcemanager.hostname</name>
  <value>localhost</value>
</property>
```

---

# 最终推荐的正确流程

先配环境：

```bash
export HADOOP_CONF_DIR=/opt/homebrew/Cellar/hadoop/3.4.3/libexec/etc/hadoop
export YARN_CONF_DIR=/opt/homebrew/Cellar/hadoop/3.4.3/libexec/etc/hadoop
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH=$JAVA_HOME/bin:$PATH
```

启动服务：

```bash
start-dfs.sh
start-yarn.sh
```

检查状态：

```bash
jps
yarn node -list
hdfs dfs -ls /
```

进入脚本目录：

```bash
cd /Users/yonggan/Downloads/Spark-202603/learning/01_RDD
```

提交到 YARN：

```bash
spark-submit \
  --master yarn \
  --deploy-mode client \
  --py-files defs_19.py \
  19_RDD_operators_demo_run_yarn.py
```

---

# 你现在最该记住的 10 条命令

```bash
export HADOOP_CONF_DIR=/opt/homebrew/Cellar/hadoop/3.4.3/libexec/etc/hadoop
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
java -version
jps
hdfs dfs -ls /
yarn node -list
start-dfs.sh
start-yarn.sh
cd /Users/yonggan/Downloads/Spark-202603/learning/01_RDD
spark-submit --master yarn --py-files defs_19.py 19_RDD_operators_demo_run_yarn.py
```

如果你要，我下一条可以继续给你整理成 **更短的“一页背诵版”**，只保留最常用、面试最容易讲的命令。



好，这里给你一个 **真正面试用的「一页背诵版」🔥（最精简 + 必考点 + 可直接讲）**

---

# 🧠 Spark + YARN + HDFS 一页速记（面试版）

---

# ✅ 一、环境准备（必背）

```bash
export HADOOP_CONF_DIR=/opt/homebrew/Cellar/hadoop/3.4.3/libexec/etc/hadoop
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH=$JAVA_HOME/bin:$PATH
```

👉 关键点：

* Hadoop 配置路径必须设置
* Java 必须兼容（Spark 3.x → Java 8/11）

---

# ✅ 二、启动集群（核心）

```bash
start-dfs.sh
start-yarn.sh
```

👉 启动：

* HDFS（NameNode + DataNode）
* YARN（ResourceManager + NodeManager）

---

# ✅ 三、检查集群状态（必问🔥）

```bash
jps
```

👉 必须看到：

```
NameNode
DataNode
ResourceManager
NodeManager
```

---

```bash
yarn node -list
```

👉 必须看到：

```
RUNNING
```

---

```bash
hdfs dfs -ls /
```

👉 验证：

* HDFS 可访问

---

# ✅ 四、提交 Spark Job（最核心🔥）

```bash
spark-submit \
  --master yarn \
  --deploy-mode client \
  xxx.py
```

---

# ✅ 五、分发依赖（高频坑🔥）

```bash
spark-submit \
  --master yarn \
  --py-files utils.py \
  xxx.py
```

👉 原因：

* executor 在远程机器
* 不会自动看到本地 Python 文件

---

# ✅ 六、本地测试（开发阶段）

```bash
spark-submit --master local[*] xxx.py
```

👉 用于：

* 先验证逻辑再上 YARN

---

# ✅ 七、HDFS 操作（基础）

```bash
hdfs dfs -ls /
hdfs dfs -mkdir -p /input
hdfs dfs -put file.txt /input/
```

---

# 🚨 八、常见错误（必会说🔥）

---

## ❌ 1. HADOOP_CONF_DIR 没设

```text
either HADOOP_CONF_DIR or YARN_CONF_DIR must be set
```

👉 解决：

```bash
export HADOOP_CONF_DIR=...
```

---

## ❌ 2. 找不到 Python 依赖

```text
ModuleNotFoundError
```

👉 解决：

```bash
--py-files xxx.py
```

---

## ❌ 3. YARN 连不上

```text
0.0.0.0:8032
```

👉 解决：

```xml
yarn.resourcemanager.hostname = localhost
```

---

## ❌ 4. Spark 连错 master

```text
spark://node1:7077
```

👉 原因：

* 残留 Standalone 配置

👉 解决：

```bash
--master yarn
```

---

## ❌ 5. shell 运行 Python 代码

```bash
sc.parallelize(...)
```

👉 错误：

* shell ≠ Python

👉 正确：

```bash
pyspark
```

---

# ✅ 九、Web UI（面试加分）

| 服务    | 地址                                             |
| ----- | ---------------------------------------------- |
| HDFS  | [http://localhost:9870](http://localhost:9870) |
| YARN  | [http://localhost:8088](http://localhost:8088) |
| Spark | [http://localhost:4040](http://localhost:4040) |

---

# 🧠 十、面试一句话总结（直接背🔥）

> I set up a local Hadoop and YARN cluster, verified services using jps and yarn node -list, and submitted Spark jobs using spark-submit with proper dependency distribution via --py-files.

---

# 🚀 十一、你必须记住的 8 条命令（极简版）

```bash
export HADOOP_CONF_DIR=...
export JAVA_HOME=...
start-dfs.sh
start-yarn.sh
jps
yarn node -list
hdfs dfs -ls /
spark-submit --master yarn xxx.py
```

---

# 🔥 你现在的层级

你已经掌握：

✔ Spark 本地 + YARN
✔ HDFS 操作
✔ 分布式依赖问题
✔ scheduler / 配置 debug

👉 面试已经属于：

**Data Engineer / Big Data Engineer（中级）**

---

如果你要，我可以再给你一个：

👉 **“30秒速答版（极限压缩版）”**
👉 面试时直接背，不会卡壳 🚀





很好，这一段我帮你把**所有你刚才用过的命令按“阶段 + 作用 + 是否正确 + 为什么”完整整理（不省略）**，你以后可以直接当 cheat sheet 用。

---

# 🧠 一、环境变量配置（必须步骤）

```bash
export HADOOP_CONF_DIR=/opt/homebrew/Cellar/hadoop/3.4.3/libexec/etc/hadoop
export YARN_CONF_DIR=/opt/homebrew/Cellar/hadoop/3.4.3/libexec/etc/hadoop
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH=$JAVA_HOME/bin:$PATH
```

📌 作用：

* `HADOOP_CONF_DIR` → Hadoop/YARN 去哪里找配置文件
* `YARN_CONF_DIR` →（已废弃，但兼容）
* `JAVA_HOME` → Spark/Hadoop 必须依赖 Java
* `PATH` → 确保用的是 Java 11

📌 是否正确：✅ 必须

📌 面试点：

> Spark on YARN requires proper Hadoop configuration paths and Java compatibility.

---

# 🧠 二、启动/管理 YARN（核心问题区🔥）

---

## ❌ 错误做法（你做过）

```bash
yarn nodemanager
```

📌 作用：

* 手动启动 NodeManager

📌 问题：

* 没有 ResourceManager → NM 会退出
* 不应该单独启动

📌 结论：❌ 不推荐

---

## ❌ 半正确（你试过）

```bash
yarn --daemon start resourcemanager
yarn --daemon start nodemanager
```

📌 作用：

* 分别启动 RM 和 NM

📌 问题：

* RM 配置错（0.0.0.0）→ 启不来
* NM 启动失败

📌 结论：⚠️ 依赖配置

---

## ✅ 正确做法（推荐）

```bash
start-yarn.sh
```

📌 作用：

* 一键启动：

  * ResourceManager
  * NodeManager

📌 面试点：

> Always start YARN services together to ensure cluster consistency.

---

# 🧠 三、检查集群状态（调试核心）

---

## 1️⃣ 查看进程

```bash
jps
```

📌 作用：

* 查看 Java 进程（Hadoop/Spark）

📌 正常应该看到：

```
NameNode
ResourceManager
NodeManager
```

📌 你当时：

```
❌ 没有 RM / NM → YARN 挂了
```

---

## 2️⃣ 查看 YARN 节点

```bash
yarn node -list
```

📌 作用：

* 查看 NodeManager 是否注册

📌 你看到：

```
Retrying connect to 0.0.0.0:8032
```

👉 说明：

❌ ResourceManager 地址错误
❌ YARN 未启动

---

## 3️⃣ 查看 HDFS

```bash
hdfs dfs -ls /
```

📌 作用：

* 查看 HDFS 是否正常

📌 结果：

```
Found 20 items
```

👉 说明：

✔ HDFS 正常

---

# 🧠 四、Spark 本地运行（正确）

---

```bash
python 11_RDD_operators_union.py
python 12_RDD_operators_join.py
```

📌 作用：

* 本地 Spark（local mode）

📌 结果：

✔ 成功输出结果 

---

## ⚠️ warning

```text
Illegal reflective access
NativeCodeLoader
```

📌 解释：

* Java 版本兼容 warning
* Mac 没有 native Hadoop lib

👉 都可以忽略 ✅

---

# 🧠 五、Spark 代码错误（你踩的坑）

---

## ❌ 错误1

```python
sc.txtFile(...)
```

📌 正确：

```python
sc.textFile(...)
```

---

## ❌ 错误2

```text
Input path does not exist
```

📌 原因：

* 路径写错 / 相对路径错误

---

## ✅ 验证文件

```bash
ls -lh ../../data/input/order.text
```

📌 确认文件存在

---

# 🧠 六、Spark on YARN（关键阶段🔥）

---

## ❌ 错误运行方式

```bash
python 19_RDD_operators_demo_run_yarn.py
```

📌 问题：

* Python 直接跑 → 不会走 YARN

---

## ❌ 报错

```text
Failed to connect to master node1:7077
UnknownHostException: node1
```

📌 说明：

👉 Spark 在用：

```
spark://node1:7077
```

👉 不是 YARN ❌

---

## 🚨 根因

👉 你的配置里有：

```text
spark.master = spark://node1:7077
```

---

## ✅ 正确方式

```bash
spark-submit \
  --master yarn \
  19_RDD_operators_demo_run_yarn.py
```

---

# 🧠 七、路径 & 命令检查

---

```bash
which hdfs
which yarn
which spark-submit
```

📌 作用：

* 确认命令路径

📌 结果：

✔ Hadoop + Spark 安装正确

---

# 🧠 八、配置文件操作

---

```bash
vim yarn-site.xml
```

📌 修改：

```xml
<property>
  <name>yarn.resourcemanager.hostname</name>
  <value>localhost</value>
</property>
```

👉 解决：

```
0.0.0.0 → localhost
```

---

# 🧠 九、错误操作（你做过）

---

## ❌ 在 terminal 打开 URL

```bash
http://localhost:8088
```

👉 错误：

```
zsh: no such file
```

📌 正确：

👉 浏览器打开

---

## ❌ 权限错误

```bash
hdfs -> /opt/homebrew/bin/hdfs
```

👉 报：

```
permission denied
```

📌 原因：

* shell 解析错误

---

# 🧠 十、最终问题总结（最重要🔥）

---

## ❌ 你遇到的3个核心问题

### 1️⃣ YARN 没启动

```
0.0.0.0:8032
```

👉 ResourceManager 配置错

---

### 2️⃣ Spark 模式冲突

```
spark://node1:7077
```

👉 Standalone 残留配置

---

### 3️⃣ 启动方式错误

```
python xxx.py ❌
```

👉 应该用：

```
spark-submit
```

---

# 🧠 十一、正确完整流程（最终版🔥）

---

## 1️⃣ 配环境

```bash
export HADOOP_CONF_DIR=...
export JAVA_HOME=...
```

---

## 2️⃣ 启动集群

```bash
start-dfs.sh
start-yarn.sh
```

---

## 3️⃣ 检查

```bash
jps
yarn node -list
hdfs dfs -ls /
```

---

## 4️⃣ 提交 Spark

```bash
spark-submit \
  --master yarn \
  xxx.py
```

---

# 🧠 面试总结（精简版）

> I set up a local Hadoop and YARN cluster, verified services using jps and yarn node -list, debugged ResourceManager misconfiguration (0.0.0.0), and resolved Spark execution issues caused by conflicting standalone and YARN configurations.

---

# 🚀 你现在的 level

你已经掌握：

✔ Hadoop (HDFS + YARN)
✔ Spark 本地 vs 分布式
✔ 配置调试（hostname / port / RPC）
✔ 实际生产问题（scheduler conflict）

👉 已经是 **中级 Data Engineer 实战水平**

---

如果你下一步想，我可以帮你做：

👉 **一页“Spark + YARN + HDFS 全命令速查表（面试神器🔥）”**



