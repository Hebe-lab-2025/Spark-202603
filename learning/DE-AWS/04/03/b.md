```
(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % python 26_RDD_operators_saveAsTextFile.py
WARNING: An illegal reflective access operation has occurred
WARNING: Illegal reflective access by org.apache.spark.unsafe.Platform (file:/Users/yonggan/opt/spark-3.2.0-bin-hadoop3.2/jars/spark-unsafe_2.12-3.2.0.jar) to constructor java.nio.DirectByteBuffer(long,int)
WARNING: Please consider reporting this to the maintainers of org.apache.spark.unsafe.Platform
WARNING: Use --illegal-access=warn to enable warnings of further illegal reflective access operations
WARNING: All illegal access operations will be denied in a future release
Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/04/03 06:01:22 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
26/04/03 06:01:23 WARN Utils: Service 'SparkUI' could not bind on port 4040. Attempting port 4041.
(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % ---# coding:utf8

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([1, 3, 2, 4, 7, 9, 6], 3)

    # rdd.saveAsTextFile("hdfs://node1:8020/output/out1")
    # rdd.saveAsTextFile("hdfs://localhost:9000/output/out1")
    rdd.saveAsTextFile("hdfs://localhost:9000/output/out2")
```

这次看起来**大概率是成功了，不是报错**。

## 先看结论

你的这段输出里：

* 没有 `Exception`
* 没有 `Traceback`
* 命令行已经回到提示符
  ` (spark38) yonggan@Yonggans-MacBook-Pro 01_RDD %`

这通常说明：

**`rdd.saveAsTextFile("hdfs://localhost:9000/output/out2")` 已经执行完了。**

---

## 这些信息分别是什么意思

### 1. `Illegal reflective access`

```text
WARNING: Illegal reflective access by org.apache.spark.unsafe.Platform ...
```

这个一般是：

* **Spark 3.2.0 比较老**
* 你当前的 **Java 版本偏高**
* Spark 内部用了 Java 的一些“反射访问”老方式

它通常是 **兼容性警告，不一定影响运行**。

### 2. `NativeCodeLoader`

```text
WARN NativeCodeLoader: Unable to load native-hadoop library for your platform...
```

意思是：

* Hadoop 本地加速库没加载到
* 于是退回到 Java 自带实现

通常也是 **警告，不是致命错误**。

### 3. `SparkUI could not bind on port 4040`

```text
WARN Utils: Service 'SparkUI' could not bind on port 4040. Attempting port 4041.
```

意思是：

* 4040 端口已经被别的 Spark 程序占用了
* 所以这次 Spark UI 自动改到 **4041**

这也**不是错误**。

---

# 你现在最该做的验证

直接检查 HDFS 里有没有写进去：

```bash
hdfs dfs -ls /output/out2
```

如果成功，一般会看到类似：

```bash
Found 4 items
-rw-r--r--   1 yonggan supergroup          0 /output/out2/_SUCCESS
-rw-r--r--   1 yonggan supergroup          x /output/out2/part-00000
-rw-r--r--   1 yonggan supergroup          x /output/out2/part-00001
-rw-r--r--   1 yonggan supergroup          x /output/out2/part-00002
```

因为你这里：

```python
rdd = sc.parallelize([1, 3, 2, 4, 7, 9, 6], 3)
```

分区数是 `3`，所以通常会生成 **3 个 part 文件**。

---

## 再看内容

```bash
hdfs dfs -cat /output/out2/part-00000
hdfs dfs -cat /output/out2/part-00001
hdfs dfs -cat /output/out2/part-00002
```

或者直接：

```bash
hdfs dfs -cat /output/out2/part-*
```

---

## 你的代码本身没问题

你现在这段代码：

```python
from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([1, 3, 2, 4, 7, 9, 6], 3)

    rdd.saveAsTextFile("hdfs://localhost:9000/output/out2")
```

逻辑是对的：

1. 创建 SparkContext
2. 构造 RDD
3. 调用 `saveAsTextFile` 写入 HDFS

---

## 最好再补一行

建议加上：

```python
sc.stop()
```

完整写法：

```python
from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([1, 3, 2, 4, 7, 9, 6], 3)
    rdd.saveAsTextFile("hdfs://localhost:9000/output/out2")

    sc.stop()
```

这样更规范，能主动关闭 SparkContext。

---

## 如果你想更确定是不是成功

可以在代码里加打印：

```python
from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([1, 3, 2, 4, 7, 9, 6], 3)

    print("Start saving...")
    rdd.saveAsTextFile("hdfs://localhost:9000/output/out2")
    print("Save finished.")

    sc.stop()
```

如果看到：

```text
Start saving...
Save finished.
```

那就更清楚了。

---

## 你现在最可能的情况

### 情况 A：成功

最可能。因为输出里没有报错。

### 情况 B：其实写了，但是你没检查

很多时候 `saveAsTextFile()` 不会打印“成功”，只是默默完成。

### 情况 C：路径已存在时会报错

如果 `/output/out2` 已经存在，通常会报类似：

```text
FileAlreadyExistsException
```

但你这里没有，所以说明 **大概率第一次写成功了**。

---

## 下一步直接执行这三个命令

```bash
hdfs dfs -ls /output
hdfs dfs -ls /output/out2
hdfs dfs -cat /output/out2/part-*
```

你把结果贴给我，我可以继续帮你逐行解释。


很好，这次**是真正的错误原因出来了，而且非常典型**👇

---

# ❗核心报错（一句话结论）

```text
FileAlreadyExistsException: Output directory ... already exists
```

👉 意思：

> ❌ 你要写的 HDFS 目录 **已经存在了，Spark 不允许覆盖**

📌 原始报错位置：


---

# 🧠 为什么会这样（面试必会）

Spark 的设计原则：

👉 `saveAsTextFile()` **必须写到一个“全新目录”**

原因：

* 分布式写文件（多个 partition → 多个 part 文件）
* 避免数据被意外覆盖
* 保证 job 是 **幂等、安全的**

---

# 🧪 你当前情况

你之前已经成功跑过一次：

```bash
/output/out2
```

所以现在再次运行：

```python
rdd.saveAsTextFile("hdfs://localhost:9000/output/out2")
```

👉 就直接报错了（因为目录已存在）

---

# ✅ 三种解决方案（必须掌握）

## ✅ 方案 1（最常用）：先删再跑

```bash
hdfs dfs -rm -r /output/out2
```

然后再执行你的 python：

```bash
python 26_RDD_operators_saveAsTextFile.py
```

👉 ⭐ 推荐，最标准

---

## ✅ 方案 2：换路径（最简单）

```python
rdd.saveAsTextFile("hdfs://localhost:9000/output/out3")
```

👉 每次换一个目录

---

## ✅ 方案 3：自动生成路径（工程常用）

```python
import time

path = f"hdfs://localhost:9000/output/out_{int(time.time())}"
rdd.saveAsTextFile(path)
```

👉 每次唯一，不冲突

---

# 🚨 注意（非常重要）

❌ Spark 不支持：

```python
overwrite = true   ❌（RDD API 没这个选项）
```

👉 只有 DataFrame 才支持：

```python
df.write.mode("overwrite").save(...)
```

---

# 🧠 面试一句话回答

👉 Why does Spark throw FileAlreadyExistsException?

**Answer:**

> Because `saveAsTextFile()` requires a non-existing output directory to avoid accidental data overwrite in distributed writes.

---

# 🔍 你现在下一步

直接执行：

```bash
hdfs dfs -rm -r /output/out2
```

然后再跑：

```bash
python 26_RDD_operators_saveAsTextFile.py
```

---

# 💡 Bonus（你已经进阶了）

你现在已经踩到的是：

👉 Spark 初学者最经典 3 个坑之一：

1. ❗ 输出目录已存在（你现在这个）
2. Java 版本不兼容
3. HDFS 地址写错（localhost vs node1）

---

如果你愿意，我可以帮你整理一个：

👉 **Spark 常见 10 大报错 + 一句话解决（面试版🔥）**

非常适合你现在这个阶段。



zsh: no matches found---zsh
是啥，bash是啥，什么的缩写，代表啥

很好，这个是**Linux / Mac 面试高频基础题**，我给你一版**极简 + 面试版解释**👇

---

# 🧠 一句话总结（先记住）

👉 **zsh / bash 都是 Shell（命令解释器）**

👉 作用：**帮你把输入的命令翻译给操作系统执行**

---

# 🧩 什么是 Shell？

📌 Shell = “壳”

👉 在 Unix / Linux 里：

```
你 → Shell → 操作系统内核 → 硬件
```

👉 Shell 就是你和系统之间的“翻译官”

---

# 🧩 bash 是啥？

### 全称

👉 **Bash = Bourne Again Shell**

📌 来自：
👉 Bourne shell（最早的 shell）

📌 含义：

* Bourne → 发明人名字
* Again → “改进版”

👉 所以：
**bash = Bourne shell 的增强版**

---

# 🧩 zsh 是啥？

### 全称

👉 **Zsh = Z Shell**

📌 没有特别含义：
👉 “Z”只是命名（作者名字开头）

📌 本质：

👉 是 bash 的“升级版 + 更好用”

---

# 🔥 zsh vs bash（核心区别）

| 特性     | bash | zsh     |
| ------ | ---- | ------- |
| 年代     | 老    | 新       |
| 自动补全   | 一般   | 很强 ⭐    |
| 插件     | 少    | 很多 ⭐    |
| 体验     | 原始   | 更友好 ⭐   |
| Mac 默认 | ❌    | ✅（现在默认） |

👉 你现在 Mac 用的是：**zsh（默认）**

---

# ⚠️ 你这个报错本质

```bash
zsh: no matches found
```

👉 翻译：

> zsh 发现你输入的内容像“通配符”，但找不到匹配的文件

---

## 📌 举个例子

你输入：

```bash
hdfs dfs -cat /output/out2/part-*
```

如果目录不存在：

👉 zsh 会先自己解析 `*`
👉 找不到 → 报错

---

# 🧠 为什么 bash 不报错？

👉 bash 行为更“宽松”：

* 找不到匹配 → 直接原样传给程序

👉 zsh 行为更“严格”：

* 找不到 → 直接报错 ❌

---

# ✅ 解决方法（3个）

## ✅ 方法1：加引号（最推荐）

```bash
hdfs dfs -cat "/output/out2/part-*"
```

---

## ✅ 方法2：关闭 zsh 校验

```bash
setopt NO_NOMATCH
```

---

## ✅ 方法3：用 bash

```bash
bash
```

---

# 🎯 面试回答（超加分版）

👉 What is bash / zsh?

**Answer：**

> Bash and Zsh are both Unix shells, which act as command interpreters between users and the operating system. Bash stands for “Bourne Again Shell,” an enhanced version of the original Bourne shell, while Zsh is a more modern shell with better auto-completion, plugins, and usability.

---

# 🚀 你现在要记住的重点

👉 1️⃣ Shell = 命令解释器
👉 2️⃣ bash = 老版本
👉 3️⃣ zsh = 更强版本（Mac默认）
👉 4️⃣ zsh 更严格 → 会报 `no matches found`

---

如果你愿意，我可以给你一份：

👉 **Linux / Shell 面试速记卡（10分钟速成版🔥）**

（grep / awk / sed / ps / top 全部一页搞定）


```
(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % python 31_RDD_cache.py 
WARNING: An illegal reflective access operation has occurred
WARNING: Illegal reflective access by org.apache.spark.unsafe.Platform (file:/Users/yonggan/opt/spark-3.2.0-bin-hadoop3.2/jars/spark-unsafe_2.12-3.2.0.jar) to constructor java.nio.DirectByteBuffer(long,int)
WARNING: Please consider reporting this to the maintainers of org.apache.spark.unsafe.Platform
WARNING: Use --illegal-access=warn to enable warnings of further illegal reflective access operations
WARNING: All illegal access operations will be denied in a future release
Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/04/03 06:22:27 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Traceback (most recent call last):
  File "31_RDD_cache.py", line 16, in <module>
    rdd3.persist(StorageLevel.MEMORY_AND_DISK_2)
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/pyspark/rdd.py", line 301, in persist
    self._jrdd.persist(javaStorageLevel)
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/py4j/java_gateway.py", line 1309, in __call__
    return_value = get_return_value(
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/py4j/protocol.py", line 326, in get_return_value
    raise Py4JJavaError(
py4j.protocol.Py4JJavaError: An error occurred while calling o31.persist.
: java.lang.UnsupportedOperationException: Cannot change storage level of an RDD after it was already assigned a level
        at org.apache.spark.rdd.RDD.persist(RDD.scala:176)
        at org.apache.spark.rdd.RDD.persist(RDD.scala:200)
        at org.apache.spark.api.java.JavaRDD.persist(JavaRDD.scala:51)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
        at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
        at java.base/java.lang.reflect.Method.invoke(Method.java:566)
        at py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)
        at py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:357)
        at py4j.Gateway.invoke(Gateway.java:282)
        at py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)
        at py4j.commands.CallCommand.execute(CallCommand.java:79)
        at py4j.ClientServerConnection.waitForCommands(ClientServerConnection.java:182)
        at py4j.ClientServerConnection.run(ClientServerConnection.java:106)
        at java.base/java.lang.Thread.run(Thread.java:829)

(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD %
```

这次是**真正的代码逻辑错误**，不是环境警告。

# 一句话结论

```text
Cannot change storage level of an RDD after it was already assigned a level
```

意思是：

> **这个 RDD 已经被 cache / persist 过了，你又给它重新设置了另一个存储级别，Spark 不允许。**

---

# 先区分哪些不是重点

前面这些：

```text
Illegal reflective access
NativeCodeLoader
```

还是老问题，都是**警告**，不是这次失败的原因。

真正失败的是这句：

```text
rdd3.persist(StorageLevel.MEMORY_AND_DISK_2)
```

报错位置就在这里。

---

# 报错翻译

```text
UnsupportedOperationException:
Cannot change storage level of an RDD after it was already assigned a level
```

中文：

> 一个 RDD 一旦已经分配了存储级别，就不能直接改成另一个级别。

---

# 为什么会这样

Spark 里：

* `cache()` 本质上约等于 `persist()`
* 只是 `cache()` 用的是默认级别

对 RDD 来说，默认一般是：

```python
StorageLevel.MEMORY_ONLY
```

所以如果你前面已经写过类似：

```python
rdd3.cache()
```

或者：

```python
rdd3.persist(StorageLevel.MEMORY_ONLY)
```

然后后面又写：

```python
rdd3.persist(StorageLevel.MEMORY_AND_DISK_2)
```

就会报这个错。

---

# 典型错误代码长这样

```python
rdd3.cache()
rdd3.persist(StorageLevel.MEMORY_AND_DISK_2)   # ❌ 报错
```

或者：

```python
rdd3.persist(StorageLevel.MEMORY_ONLY)
rdd3.persist(StorageLevel.MEMORY_AND_DISK_2)   # ❌ 报错
```

---

# 正确做法 1：一开始就选好一种

如果你想用：

```python
MEMORY_AND_DISK_2
```

那就不要先 `cache()`。

直接：

```python
from pyspark import SparkConf, SparkContext, StorageLevel

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd1 = sc.parallelize([1, 2, 3, 4])
    rdd2 = rdd1.map(lambda x: x * 2)
    rdd3 = rdd2.filter(lambda x: x > 2)

    rdd3.persist(StorageLevel.MEMORY_AND_DISK_2)

    print(rdd3.collect())

    sc.stop()
```

---

# 正确做法 2：先取消，再重新 persist

如果你确实已经 cache 了，想改存储级别：

先 `unpersist()`，再重新设。

```python
rdd3.cache()

rdd3.unpersist()
rdd3.persist(StorageLevel.MEMORY_AND_DISK_2)
```

更稳一点可以写：

```python
rdd3.unpersist(blocking=True)
rdd3.persist(StorageLevel.MEMORY_AND_DISK_2)
```

---

# 面试要点

## 1. `cache()` 和 `persist()` 什么关系？

**Answer:**

`cache()` is a shortcut of `persist()` with the default storage level.
For RDDs, the default is usually `MEMORY_ONLY`.

## 2. 为什么会报这个错？

**Answer:**

Because the RDD had already been assigned a storage level, and Spark does not allow changing it directly without unpersisting first.

---

# `MEMORY_AND_DISK_2` 是什么意思

拆开看：

* `MEMORY`：先放内存
* `AND_DISK`：内存放不下就落磁盘
* `_2`：保存 **2 份副本**

所以它比 `MEMORY_ONLY` 更稳，但更占资源。

---

# 你现在该怎么改

你去看 `31_RDD_cache.py`，大概率前面有一行：

```python
rdd3.cache()
```

或者别的 `persist(...)`

把它改成二选一：

## 写法 A：只保留一个 persist

```python
rdd3.persist(StorageLevel.MEMORY_AND_DISK_2)
```

## 写法 B：如果前面已经 cache，就先 unpersist

```python
rdd3.unpersist()
rdd3.persist(StorageLevel.MEMORY_AND_DISK_2)
```

---

# 最简单记忆法

**一个 RDD 的存储级别，第一次定了就不能直接改。**

流程是：

```text
先 cache/persist 过
-> 想改
-> 先 unpersist
-> 再 persist 新级别
```

---

# 你这个报错的本质

不是 Spark 坏了，不是 Java 坏了，不是 HDFS 坏了。

而是：

> **同一个 RDD 被你重复设置了不同的缓存策略。**

把 `31_RDD_cache.py` 贴出来，我可以直接帮你逐行指出哪一行该删、哪一行该改。


```
# coding:utf8

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([1, 3, 2, 4, 7, 9, 6], 3)

    # rdd.saveAsTextFile("hdfs://node1:8020/output/out1")
    # rdd.saveAsTextFile("hdfs://localhost:9000/output/out1")
    rdd.saveAsTextFile("hdfs://localhost:9000/output/out3")
```

你贴出来的这段代码，**不是 `31_RDD_cache.py`**，而是 **`saveAsTextFile` 的代码**。

---

# 你这段代码在做什么

```python
# coding:utf8

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([1, 3, 2, 4, 7, 9, 6], 3)

    rdd.saveAsTextFile("hdfs://localhost:9000/output/out3")
```

意思是：

1. 创建 Spark 程序
2. 建一个 RDD
3. 分成 3 个分区
4. 把结果写到 HDFS 的 `/output/out3`

---

# 这段代码和你刚才的报错无关

你刚才的报错是：

```text
Cannot change storage level of an RDD after it was already assigned a level
```

这个报错只会出现在：

* `cache()`
* `persist()`
* `unpersist()`

这些缓存相关代码里。

---

# 所以现在的结论

## 你刚贴的代码

这是 **写 HDFS 文件** 的代码。

## 你刚才报错的代码

那是 **RDD 缓存** 的代码。

👉 这两个不是同一个文件。

---

# 你现在这段代码会不会有问题

这段代码本身是对的。

只要 `/output/out3` 不存在，就能成功。

如果 `/output/out3` 已经存在，又会报之前那个错误：

```text
FileAlreadyExistsException
```

---

# 你现在如果要验证这个文件写成功了

运行：

```bash
hdfs dfs -ls /output/out3
```

再看内容：

```bash
hdfs dfs -cat /output/out3/part-*
```

如果 zsh 报：

```text
zsh: no matches found
```

就写成：

```bash
hdfs dfs -cat "/output/out3/part-*"
```

---

# 如果你要继续查 `31_RDD_cache.py` 的错误

你需要贴的是 **真正的 `31_RDD_cache.py` 内容**，大概率会长这样：

```python
rdd3.cache()
rdd3.persist(StorageLevel.MEMORY_AND_DISK_2)
```

或者：

```python
rdd3.persist(StorageLevel.MEMORY_ONLY)
rdd3.persist(StorageLevel.MEMORY_AND_DISK_2)
```

这种就会报错。

---

# 你现在要区分两个文件

## 1. 当前你贴的

`26_RDD_operators_saveAsTextFile.py`

作用：
**把 RDD 写到 HDFS**

## 2. 你报错的

`31_RDD_cache.py`

作用：
**测试 RDD cache / persist**

---

把 `31_RDD_cache.py` 真正内容贴出来，我直接帮你逐行解释哪一行错了。


```
# coding:utf8
import time

from pyspark import SparkConf, SparkContext
from pyspark.storagelevel import StorageLevel

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd1 = sc.textFile("../data/input/words.txt")
    rdd2 = rdd1.flatMap(lambda x: x.split(" "))
    rdd3 = rdd2.map(lambda x: (x, 1))

    rdd3.cache()
    rdd3.persist(StorageLevel.MEMORY_AND_DISK_2)

    rdd4 = rdd3.reduceByKey(lambda a, b: a + b)
    print(rdd4.collect())

    rdd5 = rdd3.groupByKey()
    rdd6 = rdd5.mapValues(lambda x: sum(x))
    print(rdd6.collect())

    rdd3.unpersist()
    time.sleep(100000)这是错误output的代码：(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % python 31_RDD_cache.py 
WARNING: An illegal reflective access operation has occurred
WARNING: Illegal reflective access by org.apache.spark.unsafe.Platform (file:/Users/yonggan/opt/spark-3.2.0-bin-hadoop3.2/jars/spark-unsafe_2.12-3.2.0.jar) to constructor java.nio.DirectByteBuffer(long,int)
WARNING: Please consider reporting this to the maintainers of org.apache.spark.unsafe.Platform
WARNING: Use --illegal-access=warn to enable warnings of further illegal reflective access operations
WARNING: All illegal access operations will be denied in a future release
Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/04/03 06:22:27 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Traceback (most recent call last):
  File "31_RDD_cache.py", line 16, in <module>
    rdd3.persist(StorageLevel.MEMORY_AND_DISK_2)
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/pyspark/rdd.py", line 301, in persist
    self._jrdd.persist(javaStorageLevel)
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/py4j/java_gateway.py", line 1309, in __call__
    return_value = get_return_value(
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/py4j/protocol.py", line 326, in get_return_value
    raise Py4JJavaError(
py4j.protocol.Py4JJavaError: An error occurred while calling o31.persist.
: java.lang.UnsupportedOperationException: Cannot change storage level of an RDD after it was already assigned a level
        at org.apache.spark.rdd.RDD.persist(RDD.scala:176)
        at org.apache.spark.rdd.RDD.persist(RDD.scala:200)
        at org.apache.spark.api.java.JavaRDD.persist(JavaRDD.scala:51)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
        at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
        at java.base/java.lang.reflect.Method.invoke(Method.java:566)
        at py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)
        at py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:357)
        at py4j.Gateway.invoke(Gateway.java:282)
        at py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)
        at py4j.commands.CallCommand.execute(CallCommand.java:79)
        at py4j.ClientServerConnection.waitForCommands(ClientServerConnection.java:182)
        at py4j.ClientServerConnection.run(ClientServerConnection.java:106)
        at java.base/java.lang.Thread.run(Thread.java:829)

(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD %
```

对，这次代码已经很清楚了。
**报错就是你自己这两行连着写导致的：**

```python
rdd3.cache()
rdd3.persist(StorageLevel.MEMORY_AND_DISK_2)
```

---

# 一句话结论

`cache()` 已经给 `rdd3` 设置了一个存储级别，
你又马上用 `persist()` 重新设置另一个级别，
所以 Spark 报错：

> **Cannot change storage level of an RDD after it was already assigned a level**

---

# 逐行解释你的代码

## 1. 创建 SparkContext

```python
conf = SparkConf().setAppName("test").setMaster("local[*]")
sc = SparkContext(conf=conf)
```

意思：

* 程序名叫 `test`
* 运行模式是本地模式
* `local[*]` = 用本机所有 CPU 核心

---

## 2. 读文件

```python
rdd1 = sc.textFile("../data/input/words.txt")
```

意思：

* 读取文本文件
* 每一行变成 RDD 的一个元素

比如文件内容是：

```text
hello spark
hello python
```

那么 `rdd1` 大概是：

```python
["hello spark", "hello python"]
```

---

## 3. 切单词

```python
rdd2 = rdd1.flatMap(lambda x: x.split(" "))
```

意思：

* 每一行按空格切开
* `flatMap` 会把多个单词“压平”

结果可能是：

```python
["hello", "spark", "hello", "python"]
```

---

## 4. 变成 `(word, 1)`

```python
rdd3 = rdd2.map(lambda x: (x, 1))
```

结果可能变成：

```python
[("hello", 1), ("spark", 1), ("hello", 1), ("python", 1)]
```

---

# 问题就出在这里

## 5. 第一行：`cache()`

```python
rdd3.cache()
```

这句的意思：

* 把 `rdd3` 缓存起来
* 方便后面重复使用
* 默认存储级别一般是：

```python
MEMORY_ONLY
```

也就是说，这一行执行后，`rdd3` 已经“贴上标签”了：

> 我以后要按 MEMORY_ONLY 来缓存

---

## 6. 第二行：又 `persist(...)`

```python
rdd3.persist(StorageLevel.MEMORY_AND_DISK_2)
```

这句意思：

* 你又想把同一个 `rdd3`
* 改成另一种缓存策略：

  * 先放内存
  * 放不下放磁盘
  * 还保留 2 份副本

但 Spark 说：

> 不行，这个 RDD 已经有存储级别了，不能直接改。

所以报错。

---

# 为什么 Spark 不允许这样改

因为 Spark 认为：

* 一个 RDD 的缓存策略应该在第一次就确定
* 否则运行过程中改来改去，会让执行计划和缓存管理变复杂

所以规则是：

## 规则

* 第一次：可以 `cache()` 或 `persist()`
* 后面：不能直接换
* 如果一定要换：先 `unpersist()`，再重新 `persist()`

---

# 你这段代码怎么改

你有两种正确写法。

---

## 写法 1：只用 `cache()`

如果你只是想演示缓存，写这个就够了：

```python
# coding:utf8
import time

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd1 = sc.textFile("../data/input/words.txt")
    rdd2 = rdd1.flatMap(lambda x: x.split(" "))
    rdd3 = rdd2.map(lambda x: (x, 1))

    rdd3.cache()

    rdd4 = rdd3.reduceByKey(lambda a, b: a + b)
    print(rdd4.collect())

    rdd5 = rdd3.groupByKey()
    rdd6 = rdd5.mapValues(lambda x: sum(x))
    print(rdd6.collect())

    rdd3.unpersist()
    sc.stop()
```

---

## 写法 2：只用 `persist(...)`

如果你想指定存储级别，就不要先 `cache()`：

```python
# coding:utf8
import time

from pyspark import SparkConf, SparkContext
from pyspark.storagelevel import StorageLevel

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd1 = sc.textFile("../data/input/words.txt")
    rdd2 = rdd1.flatMap(lambda x: x.split(" "))
    rdd3 = rdd2.map(lambda x: (x, 1))

    rdd3.persist(StorageLevel.MEMORY_AND_DISK_2)

    rdd4 = rdd3.reduceByKey(lambda a, b: a + b)
    print(rdd4.collect())

    rdd5 = rdd3.groupByKey()
    rdd6 = rdd5.mapValues(lambda x: sum(x))
    print(rdd6.collect())

    rdd3.unpersist()
    sc.stop()
```

---

# 如果你真的想“先 cache 再换级别”

那必须这样：

```python
rdd3.cache()

rdd3.unpersist()
rdd3.persist(StorageLevel.MEMORY_AND_DISK_2)
```

但一般教学里**没必要这么写**，因为有点绕。

---

# 你的后半段代码在干嘛

## 7. 词频统计方法 1：`reduceByKey`

```python
rdd4 = rdd3.reduceByKey(lambda a, b: a + b)
print(rdd4.collect())
```

作用：

* 相同单词聚合
* 把所有 `1` 加起来

比如：

```python
[("hello", 1), ("spark", 1), ("hello", 1)]
```

变成：

```python
[("hello", 2), ("spark", 1)]
```

---

## 8. 词频统计方法 2：`groupByKey + sum`

```python
rdd5 = rdd3.groupByKey()
rdd6 = rdd5.mapValues(lambda x: sum(x))
print(rdd6.collect())
```

作用：

* 先按 key 分组
* 再对每组求和

例如：

```python
("hello", [1, 1])
("spark", [1])
```

再变成：

```python
("hello", 2)
("spark", 1)
```

---

# 为什么这里要缓存 `rdd3`

因为 `rdd3` 后面被用了两次：

1. `reduceByKey`
2. `groupByKey`

如果不缓存：

* Spark 会把 `rdd1 -> rdd2 -> rdd3` 这条链算两遍

如果缓存：

* 第一次算完 `rdd3` 后存起来
* 第二次直接复用

这就是 cache 的意义。

---

# `time.sleep(100000)` 是干嘛

```python
time.sleep(100000)
```

意思：

* 让程序暂停很久
* 方便你去 Spark UI 看缓存情况

但平时练习时，这行不是必须的。

如果你只是想运行完退出，可以删掉。

---

# 最推荐你的最终版本

```python
# coding:utf8
from pyspark import SparkConf, SparkContext
from pyspark.storagelevel import StorageLevel

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd1 = sc.textFile("../data/input/words.txt")
    rdd2 = rdd1.flatMap(lambda x: x.split(" "))
    rdd3 = rdd2.map(lambda x: (x, 1))

    # 指定缓存策略，二选一：cache() 或 persist()
    rdd3.persist(StorageLevel.MEMORY_AND_DISK)

    rdd4 = rdd3.reduceByKey(lambda a, b: a + b)
    print("reduceByKey result:", rdd4.collect())

    rdd5 = rdd3.groupByKey()
    rdd6 = rdd5.mapValues(lambda x: sum(x))
    print("groupByKey result:", rdd6.collect())

    rdd3.unpersist()
    sc.stop()
```

---

# 你现在要记住的面试点

## 1. `cache()` 和 `persist()` 区别

* `cache()` = 默认缓存
* `persist()` = 可指定存储级别

## 2. 为什么报错

* 因为同一个 RDD 已经设置过存储级别了
* 不能直接再设一次

## 3. 怎么改

* 二选一
* 或先 `unpersist()` 再改

---

# 最后给你一个超短记忆版

```text
cache() = persist(默认级别)

同一个 RDD：
第一次能设缓存
第二次不能直接改
想改就先 unpersist()
```

如果你要，我下一条可以直接给你：

**RDD 的 cache / persist / unpersist 一页速记版，附 MEMORY_ONLY、MEMORY_AND_DISK、DISK_ONLY 的区别。**


```
(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % python 31_RDD_cache.py
WARNING: An illegal reflective access operation has occurred
WARNING: Illegal reflective access by org.apache.spark.unsafe.Platform (file:/Users/yonggan/opt/spark-3.2.0-bin-hadoop3.2/jars/spark-unsafe_2.12-3.2.0.jar) to constructor java.nio.DirectByteBuffer(long,int)
WARNING: Please consider reporting this to the maintainers of org.apache.spark.unsafe.Platform
WARNING: Use --illegal-access=warn to enable warnings of further illegal reflective access operations
WARNING: All illegal access operations will be denied in a future release
Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/04/03 06:27:08 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Traceback (most recent call last):
  File "31_RDD_cache.py", line 16, in <module>
    rdd4 = rdd3.reduceByKey(lambda a, b: a + b)
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/pyspark/rdd.py", line 1893, in reduceByKey
    return self.combineByKey(lambda x: x, func, func, numPartitions, partitionFunc)
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/pyspark/rdd.py", line 2138, in combineByKey
    numPartitions = self._defaultReducePartitions()
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/pyspark/rdd.py", line 2583, in _defaultReducePartitions
    return self.getNumPartitions()
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/pyspark/rdd.py", line 2937, in getNumPartitions
    return self._prev_jrdd.partitions().size()
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/py4j/java_gateway.py", line 1309, in __call__
    return_value = get_return_value(
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/py4j/protocol.py", line 326, in get_return_value
    raise Py4JJavaError(
py4j.protocol.Py4JJavaError: An error occurred while calling o22.partitions.
: org.apache.hadoop.mapred.InvalidInputException: Input path does not exist: file:/Users/yonggan/Downloads/Spark-202603/learning/data/input/words.txt
        at org.apache.hadoop.mapred.FileInputFormat.singleThreadedListStatus(FileInputFormat.java:304)
        at org.apache.hadoop.mapred.FileInputFormat.listStatus(FileInputFormat.java:244)
        at org.apache.hadoop.mapred.FileInputFormat.getSplits(FileInputFormat.java:332)
        at org.apache.spark.rdd.HadoopRDD.getPartitions(HadoopRDD.scala:205)
        at org.apache.spark.rdd.RDD.$anonfun$partitions$2(RDD.scala:300)
        at scala.Option.getOrElse(Option.scala:189)
        at org.apache.spark.rdd.RDD.partitions(RDD.scala:296)
        at org.apache.spark.rdd.MapPartitionsRDD.getPartitions(MapPartitionsRDD.scala:49)
        at org.apache.spark.rdd.RDD.$anonfun$partitions$2(RDD.scala:300)
        at scala.Option.getOrElse(Option.scala:189)
        at org.apache.spark.rdd.RDD.partitions(RDD.scala:296)
        at org.apache.spark.api.java.JavaRDDLike.partitions(JavaRDDLike.scala:61)
        at org.apache.spark.api.java.JavaRDDLike.partitions$(JavaRDDLike.scala:61)
        at org.apache.spark.api.java.AbstractJavaRDDLike.partitions(JavaRDDLike.scala:45)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
        at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
        at java.base/java.lang.reflect.Method.invoke(Method.java:566)
        at py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)
        at py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:357)
        at py4j.Gateway.invoke(Gateway.java:282)
        at py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)
        at py4j.commands.CallCommand.execute(CallCommand.java:79)
        at py4j.ClientServerConnection.waitForCommands(ClientServerConnection.java:182)
        at py4j.ClientServerConnection.run(ClientServerConnection.java:106)
        at java.base/java.lang.Thread.run(Thread.java:829)
Caused by: java.io.IOException: Input path does not exist: file:/Users/yonggan/Downloads/Spark-202603/learning/data/input/words.txt
        at org.apache.hadoop.mapred.FileInputFormat.singleThreadedListStatus(FileInputFormat.java:278)
        ... 25 more
---# coding:utf8
import time

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd1 = sc.textFile("../data/input/words.txt")
    rdd2 = rdd1.flatMap(lambda x: x.split(" "))
    rdd3 = rdd2.map(lambda x: (x, 1))

    rdd3.cache()

    rdd4 = rdd3.reduceByKey(lambda a, b: a + b)
    print(rdd4.collect())

    rdd5 = rdd3.groupByKey()
    rdd6 = rdd5.mapValues(lambda x: sum(x))
    print(rdd6.collect())

    rdd3.unpersist()
    sc.stop()
```

```
(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % python 32_RDD_checkpoint.py
WARNING: An illegal reflective access operation has occurred
WARNING: Illegal reflective access by org.apache.spark.unsafe.Platform (file:/Users/yonggan/opt/spark-3.2.0-bin-hadoop3.2/jars/spark-unsafe_2.12-3.2.0.jar) to constructor java.nio.DirectByteBuffer(long,int)
WARNING: Please consider reporting this to the maintainers of org.apache.spark.unsafe.Platform
WARNING: Use --illegal-access=warn to enable warnings of further illegal reflective access operations
WARNING: All illegal access operations will be denied in a future release
Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/04/03 06:30:43 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
26/04/03 06:30:44 WARN FileSystem: Failed to initialize fileystem hdfs://node1:8020/output/ckp/cb67c9a1-d6c6-4aba-9c7b-178ccfab15df: java.lang.IllegalArgumentException: java.net.UnknownHostException: node1
Traceback (most recent call last):
  File "32_RDD_checkpoint.py", line 12, in <module>
    sc.setCheckpointDir("hdfs://node1:8020/output/ckp")
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/pyspark/context.py", line 1070, in setCheckpointDir
    self._jsc.sc().setCheckpointDir(dirName)
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/py4j/java_gateway.py", line 1309, in __call__
    return_value = get_return_value(
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/py4j/protocol.py", line 326, in get_return_value
    raise Py4JJavaError(
py4j.protocol.Py4JJavaError: An error occurred while calling o21.setCheckpointDir.
: java.lang.IllegalArgumentException: java.net.UnknownHostException: node1
        at org.apache.hadoop.security.SecurityUtil.buildTokenService(SecurityUtil.java:466)
        at org.apache.hadoop.hdfs.NameNodeProxiesClient.createProxyWithClientProtocol(NameNodeProxiesClient.java:134)
        at org.apache.hadoop.hdfs.DFSClient.<init>(DFSClient.java:374)
        at org.apache.hadoop.hdfs.DFSClient.<init>(DFSClient.java:308)
        at org.apache.hadoop.hdfs.DistributedFileSystem.initDFSClient(DistributedFileSystem.java:201)
        at org.apache.hadoop.hdfs.DistributedFileSystem.initialize(DistributedFileSystem.java:186)
        at org.apache.hadoop.fs.FileSystem.createFileSystem(FileSystem.java:3469)
        at org.apache.hadoop.fs.FileSystem.access$300(FileSystem.java:174)
        at org.apache.hadoop.fs.FileSystem$Cache.getInternal(FileSystem.java:3574)
        at org.apache.hadoop.fs.FileSystem$Cache.get(FileSystem.java:3521)
        at org.apache.hadoop.fs.FileSystem.get(FileSystem.java:540)
        at org.apache.hadoop.fs.Path.getFileSystem(Path.java:365)
        at org.apache.spark.SparkContext.$anonfun$setCheckpointDir$2(SparkContext.scala:2500)
        at scala.Option.map(Option.scala:230)
        at org.apache.spark.SparkContext.setCheckpointDir(SparkContext.scala:2498)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
        at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
        at java.base/java.lang.reflect.Method.invoke(Method.java:566)
        at py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)
        at py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:357)
        at py4j.Gateway.invoke(Gateway.java:282)
        at py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)
        at py4j.commands.CallCommand.execute(CallCommand.java:79)
        at py4j.ClientServerConnection.waitForCommands(ClientServerConnection.java:182)
        at py4j.ClientServerConnection.run(ClientServerConnection.java:106)
        at java.base/java.lang.Thread.run(Thread.java:829)
Caused by: java.net.UnknownHostException: node1
        ... 27 more
```

这次报错很明确：

# 一句话结论

```text
UnknownHostException: node1
```

意思是：

> 你的机器现在**解析不了 `node1` 这个主机名**，所以 Spark 在设置 checkpoint 目录时连不上这个 HDFS 地址。

---

# 报错发生在这一行

你代码里大概率有：

```python
sc.setCheckpointDir("hdfs://node1:8020/output/ckp")
```

这里的 `node1`，系统不知道它是谁，所以失败了。

---

# 为什么之前你用 `localhost:9000` 可以

因为：

```python
hdfs://localhost:9000/...
```

里的 `localhost` 一定能识别，表示“本机”。

但：

```python
hdfs://node1:8020/...
```

里的 `node1` 只有在这些情况才行：

* 你真的有一台机器叫 `node1`
* 或者你 `/etc/hosts` 配过 `node1`
* 或者 Docker / 集群网络里能解析 `node1`

你现在本机环境里显然没有。

---

# 这次不是 checkpoint 机制有问题

不是 `checkpoint()` 本身错了。
是 **checkpoint 目录地址写错了**。

---

# 最直接的修法

## 方案 1：改成你已经能用的 HDFS 地址

既然你前面 `saveAsTextFile` 已经用过：

```python
hdfs://localhost:9000/output/out3
```

那 checkpoint 也改成同一种：

```python
sc.setCheckpointDir("hdfs://localhost:9000/output/ckp")
```

这是你现在最该试的写法。

---

## 方案 2：如果只是本地练习，直接用本地目录

```python
sc.setCheckpointDir("file:///Users/yonggan/Downloads/Spark-202603/learning/output/ckp")
```

或者相对安全一点，先建目录：

```bash
mkdir -p /Users/yonggan/Downloads/Spark-202603/learning/output/ckp
```

然后代码：

```python
sc.setCheckpointDir("file:///Users/yonggan/Downloads/Spark-202603/learning/output/ckp")
```

---

# 你现在最推荐改成这样

```python
# coding:utf8
from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    sc.setCheckpointDir("hdfs://localhost:9000/output/ckp")

    rdd1 = sc.parallelize([1, 2, 3, 4, 5])
    rdd2 = rdd1.map(lambda x: x * 10)

    rdd2.checkpoint()

    print(rdd2.collect())

    sc.stop()
```

---

# 为什么 `setCheckpointDir()` 这里就报错了

因为 Spark 在你设置 checkpoint 目录时，就会先检查这个路径对应的文件系统能不能访问。

也就是说：

* 不是等 `checkpoint()` 才发现错
* 而是在 `setCheckpointDir(...)` 这里就先连 HDFS
* 一连就发现 `node1` 解析不了

---

# `node1:8020` 和 `localhost:9000` 的区别

## `node1:8020`

常见于：

* Hadoop 集群
* Docker 多节点环境
* 教学环境里给机器起名 `node1`

## `localhost:9000`

常见于：

* 本地单机 HDFS
* NameNode RPC 地址映射到本机

你现在显然更适合第二种。

---

# 如果你非要用 `node1`

那你得让系统认识 `node1`。

比如在 Mac 里配置 `/etc/hosts`：

```text
127.0.0.1   node1
```

但这只是让名字能解析，不代表你的 HDFS 真跑在 `node1:8020` 上。
如果你的 NameNode 实际监听的是 `9000`，那配了也没用。

所以你现在**不要折腾 `node1`**，直接用 `localhost:9000`。

---

# 面试版理解

## 什么是 checkpoint

checkpoint 的作用是：

> 把 RDD 结果真正写到稳定存储里，切断 lineage，避免血缘链过长。

## 为什么要设置 checkpointDir

因为 Spark 需要一个地方存 checkpoint 数据，通常是：

* HDFS
* 或其他可靠文件系统

---

# 你现在该做什么

把：

```python
sc.setCheckpointDir("hdfs://node1:8020/output/ckp")
```

改成：

```python
sc.setCheckpointDir("hdfs://localhost:9000/output/ckp")
```

然后再跑。

---

如果你把 `32_RDD_checkpoint.py` 全部贴出来，我可以直接帮你改成能跑的版本。


```
# coding:utf8
import time

from pyspark import SparkConf, SparkContext
from pyspark.storagelevel import StorageLevel

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    # 1. 告知spark, 开启CheckPoint功能
    sc.setCheckpointDir("hdfs://node1:8020/output/ckp")
    rdd1 = sc.textFile("../../data/input/words.txt")
    rdd2 = rdd1.flatMap(lambda x: x.split(" "))
    rdd3 = rdd2.map(lambda x: (x, 1))

    # 调用checkpoint API 保存数据即可
    rdd3.checkpoint()

    rdd4 = rdd3.reduceByKey(lambda a, b: a + b)
    print(rdd4.collect())

    rdd5 = rdd3.groupByKey()
    rdd6 = rdd5.mapValues(lambda x: sum(x))
    print(rdd6.collect())

    rdd3.unpersist()
    time.sleep(100000)
```

这段代码里有 **2 个问题**，但当前真正先炸的是第 **1 个**。

# 一句话结论

你这行：

```python
sc.setCheckpointDir("hdfs://node1:8020/output/ckp")
```

错在 `node1`。
你本机现在**解析不了这个主机名**，所以报：

```text
UnknownHostException: node1
```

---

# 先看你代码里的两个点

## 问题 1：checkpoint 路径错了

你现在写的是：

```python
sc.setCheckpointDir("hdfs://node1:8020/output/ckp")
```

但你前面已经验证过，你本机能用的是：

```python
hdfs://localhost:9000/...
```

所以这里应该改成：

```python
sc.setCheckpointDir("hdfs://localhost:9000/output/ckp")
```

---

## 问题 2：最后这行不合适

```python
rdd3.unpersist()
```

因为你这份代码里根本没有：

```python
rdd3.cache()
```

也没有：

```python
rdd3.persist(...)
```

所以这里 `unpersist()` 没必要。

`checkpoint()` 不是 `cache()`，两者不是一回事。

---

# 你这份代码的正确思路

## 你的流程是

1. 设置 checkpoint 目录
2. 读文件
3. 做转换
4. 对 `rdd3` 做 checkpoint
5. 后面多次使用 `rdd3`

这个思路是对的。

---

# 但要注意一个知识点

`checkpoint()` 是**懒执行**的。

也就是说：

```python
rdd3.checkpoint()
```

这行不是马上把数据写出去，
只是“标记一下：这个 RDD 之后要 checkpoint”。

真正执行通常发生在后面的 action，比如：

```python
print(rdd4.collect())
```

---

# 最推荐的改法

直接改成下面这样：

```python
# coding:utf8
import time

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    # 设置 checkpoint 目录
    sc.setCheckpointDir("hdfs://localhost:9000/output/ckp")

    rdd1 = sc.textFile("../../data/input/words.txt")
    rdd2 = rdd1.flatMap(lambda x: x.split(" "))
    rdd3 = rdd2.map(lambda x: (x, 1))

    # 标记这个 RDD 需要 checkpoint
    rdd3.checkpoint()

    rdd4 = rdd3.reduceByKey(lambda a, b: a + b)
    print(rdd4.collect())

    rdd5 = rdd3.groupByKey()
    rdd6 = rdd5.mapValues(lambda x: sum(x))
    print(rdd6.collect())

    time.sleep(100000)
    sc.stop()
```

---

# 更好的版本

实际开发或教学里，**checkpoint 常常配合 cache 一起用**，因为：

* checkpoint 会把数据写到稳定存储，比较慢
* cache 可以减少重复计算

所以更常见写法是：

```python
# coding:utf8
import time

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    sc.setCheckpointDir("hdfs://localhost:9000/output/ckp")

    rdd1 = sc.textFile("../../data/input/words.txt")
    rdd2 = rdd1.flatMap(lambda x: x.split(" "))
    rdd3 = rdd2.map(lambda x: (x, 1))

    rdd3.cache()
    rdd3.checkpoint()

    rdd4 = rdd3.reduceByKey(lambda a, b: a + b)
    print(rdd4.collect())

    rdd5 = rdd3.groupByKey()
    rdd6 = rdd5.mapValues(lambda x: sum(x))
    print(rdd6.collect())

    rdd3.unpersist()
    time.sleep(100000)
    sc.stop()
```

这个版本里：

* `cache()`：加速复用
* `checkpoint()`：切断 lineage
* `unpersist()`：这时才合理

---

# 你现在这段代码逐行解释

## 1.

```python
sc.setCheckpointDir("hdfs://node1:8020/output/ckp")
```

作用：

告诉 Spark：

> 以后 checkpoint 文件写到哪里。

你这里的问题是 `node1` 不可解析。

---

## 2.

```python
rdd1 = sc.textFile("../../data/input/words.txt")
```

读取文本文件。

这个路径对不对，要看你当前执行目录。
如果后面再报 `Input path does not exist`，那就是这个路径也要改。

---

## 3.

```python
rdd2 = rdd1.flatMap(lambda x: x.split(" "))
rdd3 = rdd2.map(lambda x: (x, 1))
```

把每行拆成单词，再变成 `(word, 1)`。

---

## 4.

```python
rdd3.checkpoint()
```

标记：这个 RDD 之后要写 checkpoint。

注意：这里不会立刻执行。

---

## 5.

```python
rdd4 = rdd3.reduceByKey(lambda a, b: a + b)
print(rdd4.collect())
```

第一次 action 触发计算。
这时 Spark 才真正去读文件、算 RDD、并执行 checkpoint。

---

## 6.

```python
rdd5 = rdd3.groupByKey()
rdd6 = rdd5.mapValues(lambda x: sum(x))
print(rdd6.collect())
```

第二次复用 `rdd3`。

如果 checkpoint 成功，后面就能减少对原 lineage 的依赖。

---

# 你现在最可能的正确版本

先只修最关键的错误：

```python
sc.setCheckpointDir("hdfs://localhost:9000/output/ckp")
```

---

# 还要提醒你一个小点

你导入了：

```python
from pyspark.storagelevel import StorageLevel
```

但这份代码没用到。

可以删掉，不影响运行，但更干净。

---

# 面试版理解

## cache 和 checkpoint 的区别

**cache**

* 把数据放内存或磁盘
* 主要为了加速
* lineage 还在

**checkpoint**

* 把数据写到可靠存储
* 主要为了切断 lineage
* 容错更强，但更慢

---

# 最短记忆版

```text
cache = 为了快
checkpoint = 为了断血缘、提高容错
```

---

你下一步直接把这行改掉：

```python
sc.setCheckpointDir("hdfs://localhost:9000/output/ckp")
```

如果改完后又报新的错，把完整输出贴给我，我继续按顺序帮你拆。


因为你**这次的任务根本没有提交到 Hadoop/YARN 上**，所以 `8088` 那个 Hadoop 页面不会更新。

# 核心原因

你代码里写的是：

```python
conf = SparkConf().setAppName("test").setMaster("local[*]")
```

这表示：

> **本地模式运行**
> 只在你自己电脑上跑，不走 YARN，不提交 Hadoop 集群任务。

所以：

* `localhost:8088/cluster/apps` 是 **YARN ResourceManager UI**
* 它只显示 **提交到 YARN 的应用**
* 你现在跑的是 `local[*]`
* 所以 **不会出现新的 Hadoop/YARN app**

---

# 你两张图分别说明什么

## 第一张：`localhost:4040/jobs/` 打不开

这说明：

> 当前没有一个正在运行的 Spark Application 占着 4040 端口

常见原因有两个：

1. 程序已经结束了
2. 程序一开始就报错退出了

你前面那个 checkpoint 程序就是在这里报错：

```python
sc.setCheckpointDir("hdfs://node1:8020/output/ckp")
```

因为 `node1` 解析失败，程序很快就挂了。
所以 Spark UI 没机会持续开着。

---

## 第二张：`localhost:8088/cluster/apps`

这个页面是 **Hadoop YARN UI**。

它现在能看到一些旧的 `PySparkShell`、`test-yarn-1`，说明你**之前确实提交过 YARN 任务**。

但你这次没更新，是因为你这次不是这样跑的：

```bash
spark-submit --master yarn ...
```

而是这样跑的：

```bash
python 32_RDD_checkpoint.py
```

再加上代码里还是：

```python
setMaster("local[*]")
```

所以它不会进 YARN。

---

# 一句话区分 4040 和 8088

## `4040`

Spark Application 自己的 UI

* 看当前这个 Spark 程序的 jobs / stages / storage
* 只在程序运行时存在
* 本地模式最常看这个

## `8088`

YARN 集群 UI

* 看提交给 YARN 的应用
* 只有 `--master yarn` 才会出现在这里

---

# 为什么你会觉得“任务没更新”

因为你现在做的是 Spark 学习代码，但运行方式是：

```python
setMaster("local[*]")
```

这类任务：

* 不会提交给 Hadoop/YARN
* 只是在本机 JVM + Python 进程里执行
* 所以 Hadoop 页面不会出现新记录

---

# 如果你想让 Hadoop/YARN 页面更新

你必须用 **YARN 模式** 跑。

例如：

```bash
spark-submit \
  --master yarn \
  32_RDD_checkpoint.py
```

并且代码里最好不要写死：

```python
.setMaster("local[*]")
```

因为外部已经指定 `--master yarn` 了。

更常见写法是：

```python
conf = SparkConf().setAppName("test")
```

然后运行时决定 master：

```bash
spark-submit --master yarn 32_RDD_checkpoint.py
```

---

# 你现在这份代码为什么更不可能更新 YARN

因为你的程序在 very early stage 就报错了：

```python
sc.setCheckpointDir("hdfs://node1:8020/output/ckp")
```

也就是说：

* 没提交到 YARN
* 本地还没正式算起来就挂了

所以：

* `4040` 没保住
* `8088` 也没新任务

---

# 你现在如果只是本地学习

那你应该看的是：

## 本地模式

* 终端输出
* `localhost:4040`（程序运行期间）
* HDFS 输出目录
* checkpoint 目录是否生成

而不是 `8088`

---

# 你现在如果想验证本地 Spark UI

改对代码，保证程序不要立刻退出，比如：

```python
sc.setCheckpointDir("hdfs://localhost:9000/output/ckp")
```

再保留：

```python
time.sleep(100000)
```

然后运行程序。
这时在程序**没有报错、还在睡眠**的时候打开：

```text
localhost:4040
```

就能看到了。

---

# 最短记忆版

```text
local[*]   -> 本地跑，看 4040
--master yarn -> 提交到 YARN，看 8088
```

你这次没更新 Hadoop 页面，因为：

```text
你跑的是 local[*]，不是 yarn
```


```
如果你愿意，我可以下一条直接给你整理一张：

**Spark local 模式 / Standalone / YARN 模式分别看哪个 UI、怎么区分、怎么启动**。


# coding:utf8
import time

from pyspark import SparkConf, SparkContext
from pyspark.storagelevel import StorageLevel
import re

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    # 1. 读取数据文件
    file_rdd = sc.textFile("../../data/input/accumulator_broadcast_data.txt")

    # 特殊字符的list定义
    abnormal_char = [",", ".", "!", "#", "$", "%"]

    # 2. 将特殊字符list 包装成广播变量
    broadcast = sc.broadcast(abnormal_char)

    # 3. 对特殊字符出现次数做累加, 累加使用累加器最好
    acmlt = sc.accumulator(0)

    # 4. 数据处理, 先处理数据的空行, 在Python中有内容就是True None就是False
    lines_rdd = file_rdd.filter(lambda line: line.strip())

    # 5. 去除前后的空格
    data_rdd = lines_rdd.map(lambda line: line.strip())

    # 6. 对数据进行切分, 按照正则表达式切分, 因为空格分隔符某些单词之间是两个或多个空格
    # 正则表达式 \s+ 表示 不确定多少个空格, 最少一个空格
    words_rdd = data_rdd.flatMap(lambda line: re.split("\s+", line))

    # 7. 当前words_rdd中有正常单词 也有特殊符号.
    # 现在需要过滤数据, 保留正常单词用于做单词计数, 在过滤 的过程中 对特殊符号做计数
    def filter_func(data):
        """过滤数据, 保留正常单词用于做单词计数, 在过滤 的过程中 对特殊符号做计数"""
        global acmlt
        # 取出广播变量中存储的特殊符号list
        abnormal_chars = broadcast.value
        if data in abnormal_chars:
            # 表示这个是 特殊字符
            acmlt += 1
            return False
        else:
            return True

    normal_words_rdd = words_rdd.filter(filter_func)
    # 8. 正常单词的单词计数逻辑
    result_rdd = normal_words_rdd.map(lambda x: (x, 1)).\
        reduceByKey(lambda a, b: a + b)

    print("正常单词计数结果: ", result_rdd.collect())
    print("特殊字符数量: ", acmlt)---从本地运行改成hadoop集群，

```

可以。你的代码现在是：

```python
conf = SparkConf().setAppName("test").setMaster("local[*]")
```

这表示 **本地模式**。
如果要改成 **Hadoop 集群 / YARN 模式**，核心改 3 件事：

---

# 1. 不要写死 `local[*]`

把这行：

```python
conf = SparkConf().setAppName("test").setMaster("local[*]")
```

改成：

```python
conf = SparkConf().setAppName("test")
```

原因：

* `master` 交给 `spark-submit` 指定
* 这样同一份代码既能本地跑，也能集群跑

---

# 2. 输入路径改成 HDFS 路径

你现在读的是本地文件：

```python
file_rdd = sc.textFile("../../data/input/accumulator_broadcast_data.txt")
```

改成 HDFS：

```python
file_rdd = sc.textFile("hdfs://localhost:9000/input/accumulator_broadcast_data.txt")
```

如果你的 NameNode 不是 `localhost:9000`，就换成你真实的 HDFS 地址。

---

# 3. 用 `spark-submit --master yarn` 提交

不要再这样跑：

```bash
python 你的文件.py
```

改成：

```bash
spark-submit --master yarn 你的文件.py
```

---

# 改好的代码

```python
# coding:utf8
import re

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test")
    sc = SparkContext(conf=conf)

    # 1. 从 HDFS 读取数据
    file_rdd = sc.textFile("hdfs://localhost:9000/input/accumulator_broadcast_data.txt")

    # 2. 特殊字符列表
    abnormal_char = [",", ".", "!", "#", "$", "%"]

    # 3. 广播变量
    broadcast = sc.broadcast(abnormal_char)

    # 4. 累加器
    acmlt = sc.accumulator(0)

    # 5. 过滤空行
    lines_rdd = file_rdd.filter(lambda line: line.strip())

    # 6. 去除首尾空格
    data_rdd = lines_rdd.map(lambda line: line.strip())

    # 7. 按空白符切分
    words_rdd = data_rdd.flatMap(lambda line: re.split(r"\s+", line))

    # 8. 过滤特殊字符，并累计特殊字符数量
    def filter_func(data):
        abnormal_chars = broadcast.value
        if data in abnormal_chars:
            acmlt.add(1)
            return False
        else:
            return True

    normal_words_rdd = words_rdd.filter(filter_func)

    # 9. 正常单词计数
    result_rdd = normal_words_rdd.map(lambda x: (x, 1)).reduceByKey(lambda a, b: a + b)

    print("正常单词计数结果:", result_rdd.collect())
    print("特殊字符数量:", acmlt.value)

    sc.stop()
```

---

# 你还要先把文件放到 HDFS

先上传：

```bash
hdfs dfs -mkdir -p /input
hdfs dfs -put accumulator_broadcast_data.txt /input/
```

检查：

```bash
hdfs dfs -ls /input
```

---

# 运行命令

如果你本地已经配置好 YARN：

```bash
spark-submit \
  --master yarn \
  33_RDD_accumulator_broadcast.py
```

如果你要指定 deploy mode，也可以：

```bash
spark-submit \
  --master yarn \
  --deploy-mode client \
  33_RDD_accumulator_broadcast.py
```

---

# 你要注意的几个点

## 1. 不要再写 `local[*]`

否则还是本地跑，不会进 YARN。

## 2. `print("特殊字符数量: ", acmlt)` 最好改成

```python
print("特殊字符数量:", acmlt.value)
```

更标准。

## 3. `acmlt += 1` 最好改成

```python
acmlt.add(1)
```

更规范，也更清楚。

## 4. `broadcast` 变量名可以用，但最好别和概念重名

例如：

```python
abnormal_bc = sc.broadcast(abnormal_char)
```

更容易读。

---

# 最短改法总结

## 原来

```python
setMaster("local[*]")
textFile("../../data/input/xxx.txt")
python xxx.py
```

## 改成

```python
setMaster 删掉
textFile("hdfs://localhost:9000/input/xxx.txt")
spark-submit --master yarn xxx.py
```

---

# 如果你的 HDFS 是 `node1:8020`

那前提是你的机器真能解析 `node1`。
你前面已经报过：

```text
UnknownHostException: node1
```

所以你现在更适合先用：

```python
hdfs://localhost:9000
```

---

如果你愿意，我可以直接把这份代码再改成一版 **“本地模式 / YARN 模式可切换版”**。

```
(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % spark-submit --master yarn 35_RDD_broadcast_and_accumulator_demo.py

WARNING: An illegal reflective access operation has occurred
WARNING: Illegal reflective access by org.apache.spark.unsafe.Platform (file:/Users/yonggan/opt/spark-3.2.0-bin-hadoop3.2/jars/spark-unsafe_2.12-3.2.0.jar) to constructor java.nio.DirectByteBuffer(long,int)
WARNING: Please consider reporting this to the maintainers of org.apache.spark.unsafe.Platform
WARNING: Use --illegal-access=warn to enable warnings of further illegal reflective access operations
WARNING: All illegal access operations will be denied in a future release
Exception in thread "main" org.apache.spark.SparkException: When running with master 'yarn' either HADOOP_CONF_DIR or YARN_CONF_DIR must be set in the environment.
        at org.apache.spark.deploy.SparkSubmitArguments.error(SparkSubmitArguments.scala:634)
        at org.apache.spark.deploy.SparkSubmitArguments.validateSubmitArguments(SparkSubmitArguments.scala:274)
        at org.apache.spark.deploy.SparkSubmitArguments.validateArguments(SparkSubmitArguments.scala:234)
        at org.apache.spark.deploy.SparkSubmitArguments.<init>(SparkSubmitArguments.scala:119)
        at org.apache.spark.deploy.SparkSubmit$$anon$2$$anon$3.<init>(SparkSubmit.scala:1026)
        at org.apache.spark.deploy.SparkSubmit$$anon$2.parseArguments(SparkSubmit.scala:1026)
        at org.apache.spark.deploy.SparkSubmit.doSubmit(SparkSubmit.scala:85)
        at org.apache.spark.deploy.SparkSubmit$$anon$2.doSubmit(SparkSubmit.scala:1043)
        at org.apache.spark.deploy.SparkSubmit$.main(SparkSubmit.scala:1052)
        at org.apache.spark.deploy.SparkSubmit.main(SparkSubmit.scala)
(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % spark-submit --master yarn 35_RDD_broadcast_and_accumulator_demo.py---# coding:utf8
import time

from pyspark import SparkConf, SparkContext
from pyspark.storagelevel import StorageLevel
import re

if __name__ == '__main__':
    # conf = SparkConf().setAppName("test").setMaster("local[*]")
    conf = SparkConf().setAppName("test")
    sc = SparkContext(conf=conf)

    # 1. 读取数据文件
    # file_rdd = sc.textFile("../../data/input/accumulator_broadcast_data.txt")
    file_rdd = sc.textFile("hdfs://localhost:9000/input/accumulator_broadcast_data.txt")

    # 特殊字符的list定义
    abnormal_char = [",", ".", "!", "#", "$", "%"]

    # 2. 将特殊字符list 包装成广播变量
    broadcast = sc.broadcast(abnormal_char)

    # 3. 对特殊字符出现次数做累加, 累加使用累加器最好
    acmlt = sc.accumulator(0)

    # 4. 数据处理, 先处理数据的空行, 在Python中有内容就是True None就是False
    lines_rdd = file_rdd.filter(lambda line: line.strip())

    # 5. 去除前后的空格
    data_rdd = lines_rdd.map(lambda line: line.strip())

    # 6. 对数据进行切分, 按照正则表达式切分, 因为空格分隔符某些单词之间是两个或多个空格
    # 正则表达式 \s+ 表示 不确定多少个空格, 最少一个空格
    words_rdd = data_rdd.flatMap(lambda line: re.split("\s+", line))

    # 7. 当前words_rdd中有正常单词 也有特殊符号.
    # 现在需要过滤数据, 保留正常单词用于做单词计数, 在过滤 的过程中 对特殊符号做计数
    def filter_func(data):
        """过滤数据, 保留正常单词用于做单词计数, 在过滤 的过程中 对特殊符号做计数"""
        global acmlt
        # 取出广播变量中存储的特殊符号list
        abnormal_chars = broadcast.value
        if data in abnormal_chars:
            # 表示这个是 特殊字符
            acmlt += 1
            return False
        else:
            return True

    normal_words_rdd = words_rdd.filter(filter_func)
    # 8. 正常单词的单词计数逻辑
    result_rdd = normal_words_rdd.map(lambda x: (x, 1)).\
        reduceByKey(lambda a, b: a + b)

    print("正常单词计数结果: ", result_rdd.collect())
    print("特殊字符数量: ", acmlt)
  ```
    
这次**还没进入你的 Python 代码逻辑**，就先被 `spark-submit --master yarn` 挡住了。

# 一句话结论

报错核心是：

```text
When running with master 'yarn' either HADOOP_CONF_DIR or YARN_CONF_DIR must be set in the environment.
```

意思是：

> 你要用 **YARN 模式** 提交 Spark 作业，但 Spark **不知道去哪里找 Hadoop/YARN 配置文件**。

---

# 为什么会这样

当你运行：

```bash
spark-submit --master yarn 35_RDD_broadcast_and_accumulator_demo.py
```

Spark 需要知道：

* YARN ResourceManager 在哪
* NameNode / HDFS 默认配置是什么
* 相关 Hadoop XML 配置在哪

这些通常来自：

* `core-site.xml`
* `hdfs-site.xml`
* `yarn-site.xml`
* `mapred-site.xml`

Spark 通过环境变量去找这些配置目录：

* `HADOOP_CONF_DIR`
* 或 `YARN_CONF_DIR`

你现在没设置，所以它直接退出了。

---

# 先说最直接的解决方法

你之前已经折腾过 Hadoop 本地配置，所以现在大概率只要把配置目录导出来就行。

## 先试这个

```bash
export HADOOP_CONF_DIR=/opt/homebrew/Cellar/hadoop/3.4.3/libexec/etc/hadoop
export YARN_CONF_DIR=$HADOOP_CONF_DIR
```

然后再跑：

```bash
spark-submit --master yarn 35_RDD_broadcast_and_accumulator_demo.py
```

---

# 先验证配置目录对不对

先执行：

```bash
ls /opt/homebrew/Cellar/hadoop/3.4.3/libexec/etc/hadoop
```

正常应该能看到类似：

```text
core-site.xml
hdfs-site.xml
mapred-site.xml
yarn-site.xml
```

如果这个路径不存在，就不能用它。

---

# 更稳的排查方法

执行：

```bash
echo $HADOOP_CONF_DIR
echo $YARN_CONF_DIR
```

如果为空，说明没设置成功。

然后找你的 Hadoop 配置目录：

```bash
find /opt/homebrew -name core-site.xml 2>/dev/null
find /opt/homebrew -name yarn-site.xml 2>/dev/null
```

找到后，把那个目录设成：

```bash
export HADOOP_CONF_DIR=那个目录
export YARN_CONF_DIR=$HADOOP_CONF_DIR
```

---

# 你的代码本身还要再改两处

即使你把 `HADOOP_CONF_DIR` 设好了，你这份代码后面**还可能再出两个问题**。

---

## 问题 1：累加器打印方式不标准

你现在写的是：

```python
print("特殊字符数量: ", acmlt)
```

应该改成：

```python
print("特殊字符数量: ", acmlt.value)
```

因为真正的值在 `.value` 里。

---

## 问题 2：累加器更新方式最好改

你现在写：

```python
acmlt += 1
```

最好改成：

```python
acmlt.add(1)
```

更规范，也更清楚。

---

# 建议你改成这版

```python
# coding:utf8
import re

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test")
    sc = SparkContext(conf=conf)

    # 从 HDFS 读取数据
    file_rdd = sc.textFile("hdfs://localhost:9000/input/accumulator_broadcast_data.txt")

    abnormal_char = [",", ".", "!", "#", "$", "%"]

    # 广播变量
    abnormal_bc = sc.broadcast(abnormal_char)

    # 累加器
    acmlt = sc.accumulator(0)

    # 过滤空行
    lines_rdd = file_rdd.filter(lambda line: line.strip())

    # 去除首尾空格
    data_rdd = lines_rdd.map(lambda line: line.strip())

    # 按空白符切分
    words_rdd = data_rdd.flatMap(lambda line: re.split(r"\s+", line))

    def filter_func(data):
        abnormal_chars = abnormal_bc.value
        if data in abnormal_chars:
            acmlt.add(1)
            return False
        else:
            return True

    normal_words_rdd = words_rdd.filter(filter_func)

    result_rdd = normal_words_rdd.map(lambda x: (x, 1)).reduceByKey(lambda a, b: a + b)

    print("正常单词计数结果:", result_rdd.collect())
    print("特殊字符数量:", acmlt.value)

    sc.stop()
```

---

# 你现在的运行顺序应该是

## 第一步：设置环境变量

```bash
export HADOOP_CONF_DIR=/opt/homebrew/Cellar/hadoop/3.4.3/libexec/etc/hadoop
export YARN_CONF_DIR=$HADOOP_CONF_DIR
```

## 第二步：确认 HDFS 文件存在

```bash
hdfs dfs -ls /input/accumulator_broadcast_data.txt
```

## 第三步：提交到 YARN

```bash
spark-submit --master yarn 35_RDD_broadcast_and_accumulator_demo.py
```

---

# 为什么之前 8088 没更新，这次如果成功就会更新

因为这次你是：

```bash
spark-submit --master yarn ...
```

只要环境变量设好，Spark 就能提交到 YARN，
然后你就会在：

```text
localhost:8088
```

看到新的 application。

---

# 最短记忆版

```text
local[*] 模式：直接 python 跑，看 4040
yarn 模式：spark-submit --master yarn
还必须先设置 HADOOP_CONF_DIR / YARN_CONF_DIR
```

你现在先执行这三条：

```bash
export HADOOP_CONF_DIR=/opt/homebrew/Cellar/hadoop/3.4.3/libexec/etc/hadoop
export YARN_CONF_DIR=$HADOOP_CONF_DIR
spark-submit --master yarn 35_RDD_broadcast_and_accumulator_demo.py
```

把新输出贴给我，我继续帮你往下拆。


很好，这一步其实已经**成功进入 YARN 了🔥**，只是现在卡在**数据路径问题**。

---

# ✅ 先给你结论

现在报错是：

```text
Input path does not exist: hdfs://localhost:9000/input/accumulator_broadcast_data.txt
```

👉 意思：

> **HDFS 上没有这个文件**

📌 原始报错：


---

# 🚀 先说好消息（非常重要）

你已经做到：

```text
Application application_... state: RUNNING
```

👉 说明：

* ✔ YARN 配置成功了
* ✔ spark-submit 成功提交
* ✔ Executor 也启动了
* ✔ 8088 页面一定能看到新任务

👉 你现在已经从“本地模式”升级到“集群模式”了

---

# ❗现在真正的问题

你代码里：

```python
file_rdd = sc.textFile("hdfs://localhost:9000/input/accumulator_broadcast_data.txt")
```

但 HDFS 里根本没有这个文件。

---

# 🧠 为什么之前本地能跑，现在不行

之前你用的是：

```python
../../data/input/xxx.txt
```

👉 读的是**本地文件系统**

现在你改成：

```python
hdfs://localhost:9000/input/xxx.txt
```

👉 读的是 **HDFS**

👉 两个完全不同的地方！！

---

# ✅ 正确解决步骤（一步一步来）

## 1️⃣ 先检查 HDFS 里有没有文件

```bash
hdfs dfs -ls /input
```

如果报：

```text
No such file or directory
```

👉 说明目录都没有

---

## 2️⃣ 创建目录

```bash
hdfs dfs -mkdir -p /input
```

---

## 3️⃣ 上传文件到 HDFS

假设你本地文件在：

```bash
../../data/input/accumulator_broadcast_data.txt
```

执行：

```bash
hdfs dfs -put ../../data/input/accumulator_broadcast_data.txt /input/
```

---

## 4️⃣ 再确认一遍

```bash
hdfs dfs -ls /input
```

你应该看到：

```text
accumulator_broadcast_data.txt
```

---

## 5️⃣ 再跑一次 Spark

```bash
spark-submit --master yarn 35_RDD_broadcast_and_accumulator_demo.py
```

---

# 🧠 你现在要建立的核心认知

## 本地模式 vs 集群模式

| 模式       | 读文件位置  |
| -------- | ------ |
| local[*] | 本地文件系统 |
| yarn     | HDFS   |

---

# ⚠️ 你的代码现在是“集群思维”

```python
sc.textFile("hdfs://...")
```

👉 所有 worker 节点都要能访问

👉 所以必须用 HDFS

---

# 🎯 再帮你总结整个流程（面试级别）

## Spark on YARN 执行流程

1. spark-submit 提交 job
2. ResourceManager 分配资源
3. 启动 ApplicationMaster
4. 启动 Executors
5. Executors 从 HDFS 读取数据
6. 执行计算

👉 所以：

```text
数据必须在 HDFS
```

---

# 🔥 你现在已经完成的阶段

✔ local 模式
✔ HDFS 写数据
✔ Spark UI 4040
✔ YARN UI 8088
✔ spark-submit
✔ Executor 启动

👉 现在只差一个点：

```text
HDFS 数据准备
```

---

# 🧪 你现在只需要执行这3行

```bash
hdfs dfs -mkdir -p /input
hdfs dfs -put ../../data/input/accumulator_broadcast_data.txt /input/
spark-submit --master yarn 35_RDD_broadcast_and_accumulator_demo.py
```

---

# 🚀 下一步（如果你想继续进阶）

你已经到了可以学：

👉 Spark 面试核心 4 件套：

1. Broadcast vs Accumulator（你正在做）
2. Shuffle 原理
3. reduceByKey vs groupByKey
4. cache vs checkpoint

---

如果你愿意，我可以下一步帮你做：

👉 **“Spark on YARN 一张图 + 一套面试答案（非常加分🔥）”**


```
2026-04-03 06:53:06,929 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Found 1 items
-rw-r--r--   1 yonggan supergroup       2906 2026-04-02 08:22 /input/order.text
(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD %
```

问题找到了：**HDFS 里没有 `accumulator_broadcast_data.txt`，只有 `order.text`**。

你现在的 HDFS `/input` 目录内容是：

```text
/input/order.text
```

所以这行代码一定会报错：

```python
file_rdd = sc.textFile("hdfs://localhost:9000/input/accumulator_broadcast_data.txt")
```

因为那个文件根本不存在。

---

# 两种修法

## 方案 1：把代码改成现有文件名

如果你就是想先跑通，改成：

```python
file_rdd = sc.textFile("hdfs://localhost:9000/input/order.text")
```

然后再执行：

```bash
spark-submit --master yarn 35_RDD_broadcast_and_accumulator_demo.py
```

---

## 方案 2：把真正需要的文件上传到 HDFS

如果你就是要跑 `accumulator_broadcast_data.txt`，那先上传：

```bash
hdfs dfs -put ../../data/input/accumulator_broadcast_data.txt /input/
```

然后确认：

```bash
hdfs dfs -ls /input
```

再跑。

---

# 你现在最适合做什么

为了先验证 **broadcast + accumulator + YARN** 这一套通了，建议你先用现有文件：

```python
file_rdd = sc.textFile("hdfs://localhost:9000/input/order.text")
```

这样最快。

---

# 还要顺手改两行代码

你现在代码里还有两处建议一起改：

## 1. 累加器加法

把：

```python
acmlt += 1
```

改成：

```python
acmlt.add(1)
```

## 2. 打印累加器

把：

```python
print("特殊字符数量: ", acmlt)
```

改成：

```python
print("特殊字符数量: ", acmlt.value)
```

---

# 改好后的关键部分

```python
file_rdd = sc.textFile("hdfs://localhost:9000/input/order.text")

def filter_func(data):
    abnormal_chars = broadcast.value
    if data in abnormal_chars:
        acmlt.add(1)
        return False
    else:
        return True

print("特殊字符数量: ", acmlt.value)
```

---

# 一句话总结

你不是 YARN 没跑起来。
你是 **YARN 已经跑起来了，但代码读了一个 HDFS 中不存在的文件名**。

现在只差把文件名对上。


这个现象其实是**正常的，不是错误**👇

---

# 一句话结论

```text
localhost:4040 打不开 = Spark 应用已经结束了
```

👉 所以端口被释放了 → 浏览器连不上

---

# 🧠 为什么会这样

你这次运行流程是：

1. `spark-submit --master yarn ...`
2. 程序执行（读取 HDFS + 计算）
3. 出错（找不到文件）
4. Spark 自动 `stop()`
5. 4040 UI 被关闭

👉 所以你现在访问：

```text
http://localhost:4040
```

就会：

```text
connection refused ❌
```

---

# 📌 关键证据（你日志里已经说明了）

最后几行：

```text
SparkContext: Successfully stopped SparkContext
SparkUI: Stopped Spark web UI at http://localhost:4040
```

👉 UI 已经关闭了

---

# 🧠 什么时候 4040 能打开？

只有在 **Spark 程序还在运行的时候**

---

# ✅ 让 4040 一直能打开的方法

你之前已经写了这一行：

```python
time.sleep(100000)
```

👉 这个就是为了：

> 程序跑完后不退出，让 UI 还活着

---

# 🚨 但你这次为什么还是打不开？

因为你程序 **还没跑到 sleep 就挂了**

原因是：

```text
Input path does not exist ❌
```

👉 在这里就 crash 了：

```python
file_rdd = sc.textFile("hdfs://localhost:9000/input/accumulator_broadcast_data.txt")
```

👉 所以：

* 没进入正常执行
* 没进入 sleep
* UI 直接被关闭

---

# 🧪 正确打开 4040 的步骤

## 第一步：修复文件路径（关键）

你现在 HDFS 里是：

```text
/input/order.text
```

所以改成：

```python
file_rdd = sc.textFile("hdfs://localhost:9000/input/order.text")
```

---

## 第二步：保留 sleep

```python
time.sleep(100000)
```

---

## 第三步：重新运行

```bash
spark-submit --master yarn 35_RDD_broadcast_and_accumulator_demo.py
```

---

## 第四步：立刻打开

```text
http://localhost:4040
```

---

# 🧠 4040 vs 8088 再帮你彻底理清

## 🔵 4040（Spark UI）

* 当前这个 job 的内部执行情况
* stages / tasks / storage / shuffle
* ❗ 只在 job 运行期间存在

---

## 🟡 8088（YARN UI）

* 所有提交到 YARN 的任务
* job 历史记录
* ❗ 一直存在

---

# 🎯 你现在这个状态

| 项目            | 状态        |
| ------------- | --------- |
| YARN (8088)   | ✅ 正常      |
| Spark 提交      | ✅ 成功      |
| Executor 启动   | ✅ 成功      |
| Spark UI 4040 | ❌ 程序结束后消失 |

---

# 🔥 面试级一句话总结

```text
Spark UI (4040) is only available while the application is running.
Once the SparkContext stops, the UI is shut down and the port is released.
```

---

# 🚀 你现在只差最后一步

👉 修这个：

```python
file_rdd = sc.textFile("hdfs://localhost:9000/input/order.text")
```

👉 然后再跑

👉 再打开 4040

---

如果你愿意，我可以帮你下一步：

👉 **带你逐页讲 4040 UI（Jobs / Stages / Storage），面试直接加分🔥**


这个页面说明：**4040 端口上的 Spark UI 进程还在，但应用信息还没准备好，或者刚好已经结束/异常了**。

# 一句话结论

```text
HTTP ERROR 500 + Failed to get the application information
```

意思是：

> Spark UI 网页服务起来了，但它拿不到当前 Spark Application 的信息，所以 `/jobs/` 页面渲染失败了。

---

# 你这个情况最可能的原因

结合你前面的日志，最可能是这两种：

## 1. 程序刚启动，UI比应用信息更早起来

Spark UI 先绑定了 `4040`，但 Job / App 信息还没完全注册好。
所以这时访问 `/jobs/`，会临时看到这个 500。

这也是页面自己写的提示：

```text
If you are starting up Spark, please wait a while until it's ready.
```

---

## 2. 程序已经报错或退出了

你前面已经遇到过：

```text
Input path does not exist
```

如果应用很快失败：

* Spark UI 可能短暂还在
* 但内部应用状态已经没了
* 再访问 `/jobs/` 就可能报这个 500

这个也很常见。

---

# 这和“connection refused”有什么区别

## `connection refused`

说明：

> 4040 上根本没有服务在监听了

也就是 UI 已经彻底关了。

## 你现在这个 `HTTP 500`

说明：

> 4040 上还有服务
> 但服务内部拿不到 app 信息

所以：

* **500 比 refused 更前一步**
* 它表示“服务还活着，但内容拿不出来”

---

# 为什么会出现这个错误页

页面里核心报错是：

```text
java.util.NoSuchElementException: Failed to get the application information
```

这个意思就是：

> Spark UI 去取 applicationInfo 时没取到值。

说白了就是：

* Jobs 页想展示当前 app 的 job/stage 信息
* 但当前 app 对象不存在、未初始化完成、或者已经消失
* 所以页面报 500

---

# 你现在该怎么判断是哪一种

看终端最有效。

## 如果终端还在持续输出日志

说明应用还在启动或运行中。
这时：

* 等 3 到 10 秒
* 刷新 `localhost:4040/jobs/`

可能就好了。

## 如果终端已经出现报错并退出

那说明应用已经挂了。
这种情况下 4040 不会稳定可用，500 很正常。

---

# 结合你前面的情况，我更倾向于这个原因

你之前已经有明确报错：

```text
Input path does not exist: hdfs://localhost:9000/input/accumulator_broadcast_data.txt
```

而且应用会很快 stop。
所以你现在这个 500，大概率是：

> Spark UI 还没完全关掉，但应用已经失败了，导致 Jobs 页面拿不到应用信息。

---

# 正确做法

先把程序跑成功，再去看 4040。

你现在最该先修的是输入路径。你 HDFS 里实际有的是：

```text
/input/order.text
```

所以先改代码：

```python
file_rdd = sc.textFile("hdfs://localhost:9000/input/order.text")
```

同时把累加器也顺手改一下：

```python
acmlt.add(1)
print("特殊字符数量:", acmlt.value)
```

---

# 想稳定看到 4040，建议这样做

让程序成功跑完后别立刻退出，可以在最后加：

```python
import time
time.sleep(100000)
```

比如：

```python
print("正常单词计数结果:", result_rdd.collect())
print("特殊字符数量:", acmlt.value)

time.sleep(100000)
sc.stop()
```

这样：

* 应用成功
* SparkContext 还活着
* 4040 页面会稳定很多

---

# 你现在可以这样理解

```text
4040 能打开但报 500
= Spark UI server 在
= 但 Spark application info 不在/没准备好
```

---

# 最短记忆版

## 4040 报 500

* UI 在
* App 信息没拿到

## 4040 connection refused

* UI 都没了

---

你这张图不是新问题，本质上还是前面那个应用没有稳定跑起来。先把输入文件路径改对，4040 就会正常很多。


很好，这次你这段日志其实是 **完全成功的运行（而且很关键的一点）** 👇

---

# ✅ 一句话结论

```text
你的程序已经成功执行完了，只是执行太快 → 4040 UI 一闪而过
```

📌 关键输出：

```text
[1, 2, 3, 4, 5]
```

👉 说明 job 成功执行
📌 原始日志：

---

# 🧠 为什么你又看不到 4040

看最后几行：

```text
SparkContext: Successfully stopped SparkContext
SparkUI: Stopped Spark web UI at http://localhost:4040
```

👉 意思：

> 程序执行完 → 自动 stop → UI 关闭

---

# ⚠️ 核心原因（你现在遇到的所有 UI 问题本质）

```text
你的 job 执行太快（不到 1 秒）
```

看这里：

```text
Job 0 finished ... took 0.28 s
```

👉 0.28 秒就结束了

所以：

* 4040 开起来
* 任务跑完
* UI 立刻关闭

👉 你根本来不及打开浏览器

---

# 🧪 怎么稳定看到 4040（关键技巧）

## 方法 1（最推荐🔥）

在代码最后加：

```python
import time
time.sleep(100000)
```

例如：

```python
print([1, 2, 3, 4, 5])

import time
time.sleep(100000)
```

---

## 方法 2（更真实一点）

加一个耗时操作：

```python
import time

rdd = sc.parallelize(range(100000000))
rdd.map(lambda x: x * 2).count()

time.sleep(100000)
```

---

# 🔍 你这次运行模式很关键

虽然你写的是：

```bash
spark-submit --master yarn ...
```

但看日志：

```text
Starting executor ID driver on host localhost
Running task ... executor driver
```

👉 实际是：

```text
YARN client mode + 本地 executor
```

👉 也就是说：

* Driver 在你本机
* Executor 也在本机

👉 所以你看到：

```text
localhost:4040
```

---

# 🧠 为什么你看到 executor 还是 localhost

因为你现在：

* 是伪分布式 / 单机 YARN
* NodeManager 就在本机

所以：

```text
executor = localhost（正常）
```

---

# 🎯 你现在的进度（非常关键）

你已经完成：

| 阶段           | 状态 |
| ------------ | -- |
| local[*]     | ✅  |
| HDFS 读写      | ✅  |
| spark-submit | ✅  |
| YARN 提交      | ✅  |
| executor 启动  | ✅  |
| job 执行       | ✅  |

👉 你现在已经进入：

```text
Spark on YARN 正常运行阶段🔥
```

---

# 🧠 为什么之前 4040 出问题，现在正常

之前：

❌ 路径错
❌ 程序 crash
❌ UI 不稳定

现在：

✔ job 成功
✔ executor 执行
✔ UI 正常启动

👉 只是太快结束了

---

# 🔥 面试级总结（一定要记）

```text
Spark UI (4040) only exists while the application is running.
For short jobs, the UI may disappear immediately after execution.
```

---

# 🚀 下一步建议（非常重要）

你现在可以开始看：

👉 4040 页面里的 4 个核心模块：

1. Jobs
2. Stages
3. Storage
4. Executors

---

# 如果你想下一步更强

我可以带你：

👉 用你这段代码，在 4040 里讲清楚：

* DAG 是怎么生成的
* 为什么有 stage
* shuffle 在哪一步发生
* reduceByKey vs groupByKey 差别

👉 这是 **面试高频 + 实战最重要部分🔥**

你现在已经到了可以学这个的阶段了。


很好，这个问题非常关键（面试也常问）👇

---

# ✅ 一句话结论

```python
不要在代码里写 setMaster("local[*]")
```

👉 改成：

```python
conf = SparkConf().setAppName("test")
```

👉 然后用命令控制：

```bash
spark-submit --master yarn xxx.py
```

---

# ❌ 你现在的写法（错误用法）

```python
conf = SparkConf().setAppName("test").setMaster("local[*]")
```

👉 问题：

* 强制写死本地模式
* 即使你用 `--master yarn` 也可能冲突
* 面试官会觉得你不懂部署方式

---

# ✅ 正确写法（标准生产写法）

```python
conf = SparkConf().setAppName("test")
sc = SparkContext(conf=conf)
```

---

# 🚀 真正控制运行模式的地方

👉 在命令行：

## 本地模式

```bash
spark-submit --master local[*] xxx.py
```

## YARN 模式

```bash
spark-submit --master yarn xxx.py
```

---

# 🧠 为什么要这样设计（重点）

Spark 设计原则：

```text
代码 = 业务逻辑
运行方式 = 部署配置
```

👉 解耦！！

---

# 🔥 面试回答模板（直接用）

**Q: How do you switch between local and YARN mode in Spark?**

👉 标准回答：

```text
We should not hardcode the master in the application code.
Instead, we define only the application name in SparkConf,
and control the execution mode using spark-submit.

For example:
- local mode: --master local[*]
- YARN mode: --master yarn

This makes the application portable and environment-independent.
```

---

# ⚠️ 你现在还要注意一件事

你已经改成：

```python
conf = SparkConf().setAppName("test")
```

但如果你还看到：

```text
executor driver on localhost
```

👉 说明你还是：

```text
YARN client mode（默认）
```

---

# 🚀 如果你想更“像集群”

可以这样跑：

```bash
spark-submit \
  --master yarn \
  --deploy-mode cluster \
  xxx.py
```

区别：

| 模式         | driver 在哪 |
| ---------- | --------- |
| client（默认） | 本机        |
| cluster    | YARN 节点   |

---

# 🎯 最终正确版本

## 代码

```python
conf = SparkConf().setAppName("test")
sc = SparkContext(conf=conf)
```

---

## 运行

```bash
spark-submit --master yarn xxx.py
```

---

# 🔥 最短记忆版

```text
代码里不要写 master
运行模式用 spark-submit 控制
```

---

# 🚀 你现在已经到一个很高阶段了

你已经能：

✔ local
✔ HDFS
✔ YARN
✔ spark-submit

👉 下一步就是：

```text
Spark DAG / Stage / Shuffle 原理（面试核心🔥）
```

---

如果你愿意，我可以下一步：

👉 用你刚才那个程序，带你在 4040 UI 里“看懂一次 Spark 执行流程”（面试直接加分）


```
# coding:utf8
import os
# os.environ["JAVA_HOME"] = "/Users/yonggan/Library/Java/JavaVirtualMachines/corretto-1.8.0_442/Contents/Home"
# os.environ["PYSPARK_PYTHON"] = "/Users/yonggan/anaconda3/envs/spark38/bin/python"
# os.environ["SPARK_HOME"] = "/Users/yonggan/opt/spark-3.2.0-bin-hadoop3.2"
# os.environ["PATH"] = os.environ["JAVA_HOME"] + "/bin:" + os.environ.get("PATH", "")

import subprocess

print("JAVA_HOME =", os.environ.get("JAVA_HOME"))
print("SPARK_HOME =", os.environ.get("SPARK_HOME"))
print("PYSPARK_PYTHON =", os.environ.get("PYSPARK_PYTHON"))

try:
    print(subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT).decode())
except Exception as e:
    print("java -version failed:", e)

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    local_words_path = os.path.join(base_dir, "data", "input", "words.txt")

    file_rdd1 = sc.textFile(local_words_path)
    print("默认读取分区数: ", file_rdd1.getNumPartitions())
    print("file_rdd1 内容:", file_rdd1.collect())

    file_rdd2 = sc.textFile(local_words_path, 3)
    file_rdd3 = sc.textFile(local_words_path, 100)
    print("file_rdd2 分区数:", file_rdd2.getNumPartitions())
    print("file_rdd3 分区数:", file_rdd3.getNumPartitions())

    # hdfs_rdd = sc.textFile("hdfs://node1:8020/input/words.txt")
    # print("hdfs_rdd 内容:", hdfs_rdd.collect())给我讲讲，怎么能学会
```

你现在这段代码其实已经在做一件**非常对的事情**：
👉 同时在理解 **环境 + Spark API + 分区机制**

但你问的是更本质的问题：

> **“怎么才能真正学会，而不是只是会跑？”**

我给你一个**最有效的学习路径（结合你当前阶段）**👇

---

# 🧠 一句话核心

```text
学会 Spark = 代码跑通 + 知道为什么 + 能用 UI 解释
```

---

# 🔥 你这段代码在学什么（拆开看）

## 1️⃣ 环境检查（你写得很好）

```python
print("JAVA_HOME =", ...)
print("SPARK_HOME =", ...)
print("PYSPARK_PYTHON =", ...)
```

👉 这是在解决：

```text
Spark 为啥跑不起来？
```

👉 你现在已经掌握：

* Java
* Python
* Spark 环境依赖

✔ 这是第 1 层（基础）

---

## 2️⃣ textFile + 分区机制（核心）

```python
file_rdd1 = sc.textFile(local_words_path)
file_rdd2 = sc.textFile(local_words_path, 3)
file_rdd3 = sc.textFile(local_words_path, 100)
```

👉 你在学：

```text
Spark 数据是如何分布的（partition）
```

输出：

```python
getNumPartitions()
```

👉 这是：

```text
Spark 性能的核心
```

✔ 第 2 层（数据分布）

---

## 3️⃣ collect()

```python
file_rdd1.collect()
```

👉 你在学：

```text
Spark 什么时候真正执行（lazy evaluation）
```

✔ 第 3 层（执行模型）

---

# ❗但你现在卡在哪

你现在是：

```text
会写代码 ✅
会跑代码 ✅
```

但还没完全到：

```text
理解 Spark 在干什么 ❌
```

---

# 🚀 正确学习方法（非常关键🔥）

我给你一个**4步闭环法**（你照这个走一定会进步）

---

# 🥇 Step 1：写代码（你已经会了）

例如：

```python
rdd = sc.textFile(...)
```

---

# 🥈 Step 2：问自己 3 个问题（关键🔥）

每写一行，都问：

## Q1：数据长什么样？

👉 list？tuple？分区？

## Q2：在哪执行？

👉 driver？executor？

## Q3：什么时候执行？

👉 transformation？action？

---

# 🥉 Step 3：用 4040 验证（你现在缺这个）

你必须打开：

```text
http://localhost:4040
```

看：

* Jobs
* Stages
* Tasks

👉 这是你从“会写代码”→“理解系统”的关键

---

# 🏆 Step 4：解释给别人（面试能力）

比如这段代码：

```python
sc.textFile(path, 100)
```

你要能说：

```text
This creates an RDD with up to 100 partitions.
But the actual number depends on file size and HDFS block size.
```

---

# 🧠 你这段代码的“正确理解”

我帮你用面试级解释👇

---

## 🔹 textFile 默认分区

```python
file_rdd1 = sc.textFile(path)
```

👉 分区数 ≈

```text
max(文件block数, defaultParallelism)
```

---

## 🔹 textFile(path, 3)

```python
file_rdd2 = sc.textFile(path, 3)
```

👉 表示：

```text
最少 3 个分区（不是一定 3 个）
```

---

## 🔹 textFile(path, 100)

```python
file_rdd3 = sc.textFile(path, 100)
```

👉 表示：

```text
尝试创建更多分区（提高并行度）
```

但：

```text
如果文件很小 → 不会真的有 100 个
```

---

# 🔥 真正学会 Spark 的关键

你要做到这 3 件事：

---

## 1️⃣ 能预测结果

看到：

```python
sc.textFile(path, 100)
```

你能说：

```text
不会真的 100 个分区，因为数据太小
```

---

## 2️⃣ 能解释执行流程

```text
Driver:
  创建 RDD

Executor:
  读取数据
  分区处理

Action:
  collect → 触发执行
```

---

## 3️⃣ 能画 DAG（最重要🔥）

你要能画：

```text
textFile → map → filter → reduceByKey
```

👉 哪一步会 shuffle？

👉 哪一步是 stage 切分点？

---

# 🚀 给你一个练习（非常重要）

把你这段代码改成：

```python
rdd = sc.textFile(local_words_path, 3)

rdd2 = rdd.map(lambda x: x.upper())
rdd3 = rdd2.filter(lambda x: "A" in x)

print(rdd3.collect())

import time
time.sleep(100000)
```

然后：

👉 打开 4040
👉 看：

* 有几个 stage？
* 哪一步是 transformation？
* 哪一步是 action？

---

# 🎯 最短学习路线（你照这个走）

```text
1. 会写代码
2. 看 4040 UI
3. 解释执行流程
4. 讲给别人听
```

---

# 🔥 面试级总结（一定记住）

```text
Learning Spark is not about memorizing APIs.
It's about understanding how data flows and how computation is executed.
```

---

# 🚀 下一步我可以帮你

如果你愿意，我可以带你做这个👇：

👉 用你这段代码，在 4040 里：

* 一步一步看 DAG
* 标出 stage
* 解释 shuffle
* 讲 reduceByKey vs groupByKey

👉 这是 **Spark 面试最核心的能力🔥**

你现在已经到这个阶段了。



























