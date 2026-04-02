你现在这个问题，其实是**3个核心问题叠加在一起**，我帮你一次性拆清楚（面试级理解 + 实操修复）👇

---

# 🔥 一句话总结（最关键）

👉 **Spark 3.2 不支持 Java 17，你现在环境混乱（JDK 8 / 11 / 17 混用）导致 crash**

---

# 🧠 1. 你现在的真实问题（从日志反推）

你这段报错是关键：

```
IllegalAccessError: cannot access sun.nio.ch.DirectBuffer
```

👉 这在 Spark 里 = **Java 版本不兼容**

---

# 🔍 你的环境实际情况（很乱）

从日志里可以看到：

### ❌ JAVA版本混乱

* 一会儿：

  ```
  JAVA_HOME → Java 8
  ```
* 一会儿：

  ```
  java --version → Java 17
  ```

👉 说明：
👉 **你的 shell / conda / spark-env 没统一**

---

### ❌ pyspark 也没装（你前面报错）

```
ModuleNotFoundError: No module named 'pyspark'
```

---

### ❌ 错误运行方式

```
pyspark xxx.py ❌（不支持）
```

---

# 🚨 2. 为什么会炸（核心原理）

### Spark 3.2 支持：

| Java版本  | 支持情况  |
| ------- | ----- |
| Java 8  | ✅ 推荐  |
| Java 11 | ✅     |
| Java 17 | ❌ 不支持 |

👉 你现在：
👉 **实际运行走的是 Java 17（炸）**

---

# ✅ 3. 正确解决方案（一步到位）

## ✅ Step 1：强制统一 Java 版本（必须）

👉 推荐用 Java 11（最稳）

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH=$JAVA_HOME/bin:$PATH
```

然后验证：

```bash
java -version
```

👉 必须看到：

```
openjdk version "11.x"
```

---

## ✅ Step 2：彻底固定 Spark 用的 Java（关键）

在：

```bash
$SPARK_HOME/conf/spark-env.sh
```

加：

```bash
export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-11.../Contents/Home
```

👉 这样 Spark 不会乱用 Java17

---

## ✅ Step 3：修复 pyspark 环境

你之前报错：

```
No module named pyspark
```

👉 安装：

```bash
conda activate spark38
pip install pyspark==3.2.0
```

---

## ✅ Step 4：正确运行方式（必须）

❌ 错误：

```bash
python xxx.py
pyspark xxx.py
```

✅ 正确：

```bash
spark-submit 01_RDD_create_parallelize.py
```

---

# ⚠️ 4. 你刚才的另一个坑（conda activate失败）

你写了：

```bash
conda activate spark38
```

但报错：

```
invalid choice: 'activate'
```

👉 原因：
👉 你直接在 shell script 里执行

---

## ✅ 正确方式：

### 方式1（推荐）：

```bash
conda init zsh
source ~/.zshrc
conda activate spark38
```

---

### 方式2（脚本里）：

```bash
source ~/anaconda3/etc/profile.d/conda.sh
conda activate spark38
```

---

# 📌 5. 你的完整问题链（总结）

结合你日志 ：

👉 实际是：

1. Java版本乱（8 / 17 混）
2. Spark 3.2 不支持 Java 17 → crash
3. pyspark 没装 → import 报错
4. conda activate 用错方式
5. pyspark 运行方式错误

---

# 🚀 6. 一步到位终极修复（直接照抄）

```bash
# 1. fix java
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH=$JAVA_HOME/bin:$PATH

# 2. fix conda
source ~/anaconda3/etc/profile.d/conda.sh
conda activate spark38

# 3. install pyspark
pip install pyspark==3.2.0

# 4. run
spark-submit 01_RDD_create_parallelize.py
```

---

# 🧠 面试级总结（你可以这样讲）

👉 一句话版本：

> The issue was caused by Java version mismatch — Spark 3.2 is not compatible with Java 17, so I fixed it by standardizing the environment to Java 11 and ensuring Spark uses the correct JAVA_HOME.

---

# 👍 如果你下一步想进阶

我可以帮你做一个：

👉 **Spark 环境终极一键配置（Mac M1 + Conda + Java + Spark）**
👉 或者：**面试：Spark运行原理 + Driver/Executor启动流程**

直接说一句：继续 👍

```
(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % echo  "conda activate spark38" > spark-evn.sh
(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % echo $SHELL 
/bin/zsh
(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % vim spark-env.sh
(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % mv spark-evn.sh spark-env.sh
(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % vim spark-env.sh 
(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % chomod +x spark-env.sh
zsh: command not found: chomod
(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % chmod +x spark-env.sh
(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % ./spark-env.sh
usage: conda [-h] [--no-plugins] [-V] COMMAND ...
conda: error: argument COMMAND: invalid choice: 'activate' (choose from 'clean', 'compare', 'config', 'create', 'info', 'init', 'install', 'list', 'notices', 'package', 'remove', 'uninstall', 'rename', 'run', 'search', 'update', 'upgrade', 'build', 'content-trust', 'convert', 'debug', 'develop', 'doctor', 'index', 'inspect', 'metapackage', 'render', 'skeleton', 'pack', 'env', 'repo', 'token', 'server', 'verify')
(
```

你这个报错很正常。

# 原因

你在脚本里写了：

```bash
conda activate spark38
```

然后用：

```bash
./spark-env.sh
```

执行。

这样会报错，是因为 **`conda activate` 不是普通命令**，它需要先加载 conda 的 shell 初始化脚本。
直接执行 `.sh` 文件时，shell 并不知道 `activate` 这套功能。

---

# 你这里还有两个小问题

## 1. 文件名一开始写错了

你先写的是：

```bash
spark-evn.sh
```

后来才改成：

```bash
spark-env.sh
```

这个没关系，后来改对了。

## 2. `chomod` 拼错了

你输入的是：

```bash
chomod +x spark-env.sh
```

正确是：

```bash
chmod +x spark-env.sh
```

---

# 正确写法

## 方案1：脚本里先 source conda.sh

把 `spark-env.sh` 改成：

```bash
#!/bin/zsh
source ~/anaconda3/etc/profile.d/conda.sh
conda activate spark38
python --version
which python
```

然后执行：

```bash
chmod +x spark-env.sh
./spark-env.sh
```

---

## 方案2：不用 activate，直接用 conda run

这个更简单：

```bash
conda run -n spark38 python --version
conda run -n spark38 which python
```

如果你只是想运行某个 Python 文件，可以直接：

```bash
conda run -n spark38 python 01_RDD_create_parallelize.py
```

---

# 但你这里更重要的一点

你这个 `spark-env.sh` **不是给当前目录随便建一个脚本就行**。

Spark 真正读取的 `spark-env.sh` 应该放在：

```bash
$SPARK_HOME/conf/spark-env.sh
```

比如你的路径大概率是：

```bash
/Users/yonggan/opt/spark-3.2.0-bin-hadoop3.2/conf/spark-env.sh
```

---

# 你现在真正该配置的是这个

进入 Spark 配置目录：

```bash
cd /Users/yonggan/opt/spark-3.2.0-bin-hadoop3.2/conf
```

如果没有模板，就复制一个：

```bash
cp spark-env.sh.template spark-env.sh
```

然后编辑：

```bash
vim spark-env.sh
```

写成这样：

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PYSPARK_PYTHON=/Users/yonggan/anaconda3/envs/spark38/bin/python
export PYSPARK_DRIVER_PYTHON=/Users/yonggan/anaconda3/envs/spark38/bin/python
export SPARK_LOCAL_IP=127.0.0.1
```

---

# 然后验证

先看 Java：

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH=$JAVA_HOME/bin:$PATH
java -version
```

要看到 Java 11。

再运行：

```bash
spark-submit 01_RDD_create_parallelize.py
```

---

# 最后一句总结

你现在这个报错不是 Spark 本身坏了，而是：

**你把 `conda activate` 放进普通脚本直接执行了，但没有先 source conda 的初始化脚本。**

你可以直接用下面这个最稳版本：

```bash
#!/bin/zsh
source ~/anaconda3/etc/profile.d/conda.sh
conda activate spark38
python --version
which python
```

如果你愿意，我下一条可以直接给你一份 **可复制的最终版 `spark-env.sh`**。


在 `vim` 里，全选删除很简单👇

---

# ✅ 最常用（推荐）

```bash
ggdG
```

### 含义：

* `gg` → 跳到文件开头
* `dG` → 删除到文件结尾

👉 **= 全部删除**

---

# ✅ 另一种写法（等价）

```bash
:%d
```

👉 删除整个文件所有内容

---

# ✅ 面试/记忆一句话

👉 `ggdG = go top + delete to bottom`

---

# ⚠️ 小提醒

如果你删错了：

```bash
u
```

👉 撤销（undo）

---

需要我顺便给你一份 **vim 高频命令 cheat sheet（面试+实战）** 可以直接背 👍
```

(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % python 08_RDD_operators_groupBy.py 
Error processing line 1 of /Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/distutils-precedence.pth:

  Traceback (most recent call last):
    File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site.py", line 177, in addpackage
      exec(line)
    File "<string>", line 1, in <module>
  ModuleNotFoundError: No module named '_distutils_hack'

Remainder of file ignored
Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/04/02 04:54:09 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Traceback (most recent call last):
  File "08_RDD_operators_groupBy.py", line 7, in <module>
    sc = SparkContext(conf=conf)
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/pyspark/context.py", line 146, in __init__
    self._do_init(master, appName, sparkHome, pyFiles, environment, batchSize, serializer,
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/pyspark/context.py", line 209, in _do_init
    self._jsc = jsc or self._initialize_context(self._conf._jconf)
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/pyspark/context.py", line 329, in _initialize_context
    return self._jvm.JavaSparkContext(jconf)
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/py4j/java_gateway.py", line 1573, in __call__
    return_value = get_return_value(
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/py4j/protocol.py", line 326, in get_return_value
    raise Py4JJavaError(
py4j.protocol.Py4JJavaError: An error occurred while calling None.org.apache.spark.api.java.JavaSparkContext.
: java.lang.IllegalAccessError: class org.apache.spark.storage.StorageUtils$ (in unnamed module @0x2913da72) cannot access class sun.nio.ch.DirectBuffer (in module java.base) because module java.base does not export sun.nio.ch to unnamed module @0x2913da72
        at org.apache.spark.storage.StorageUtils$.<init>(StorageUtils.scala:213)
        at org.apache.spark.storage.StorageUtils$.<clinit>(StorageUtils.scala)
        at org.apache.spark.storage.BlockManagerMasterEndpoint.<init>(BlockManagerMasterEndpoint.scala:110)
        at org.apache.spark.SparkEnv$.$anonfun$create$9(SparkEnv.scala:348)
        at org.apache.spark.SparkEnv$.registerOrLookupEndpoint$1(SparkEnv.scala:287)
        at org.apache.spark.SparkEnv$.create(SparkEnv.scala:336)
        at org.apache.spark.SparkEnv$.createDriverEnv(SparkEnv.scala:191)
        at org.apache.spark.SparkContext.createSparkEnv(SparkContext.scala:277)
        at org.apache.spark.SparkContext.<init>(SparkContext.scala:460)
        at org.apache.spark.api.java.JavaSparkContext.<init>(JavaSparkContext.scala:58)
        at java.base/jdk.internal.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)
        at java.base/jdk.internal.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:77)
        at java.base/jdk.internal.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)
        at java.base/java.lang.reflect.Constructor.newInstanceWithCaller(Constructor.java:500)
        at java.base/java.lang.reflect.Constructor.newInstance(Constructor.java:481)
        at py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:247)
        at py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:357)
        at py4j.Gateway.invoke(Gateway.java:238)
        at py4j.commands.ConstructorCommand.invokeConstructor(ConstructorCommand.java:80)
        at py4j.commands.ConstructorCommand.execute(ConstructorCommand.java:69)
        at py4j.ClientServerConnection.waitForCommands(ClientServerConnection.java:182)
        at py4j.ClientServerConnection.run(ClientServerConnection.java:106)
        at java.base/java.lang.Thread.run(Thread.java:840)

(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % 

```
这次核心报错还是**同一个根因**：

# 结论

你的 `08_RDD_operators_groupBy.py` 失败，**不是 groupBy 代码逻辑问题**，而是：

1. **Spark 3.2 / PySpark 3.2 正在用 Java 17**
2. **Spark 3.2 不兼容 Java 17**
3. 另外还有一个次要问题：**conda 环境里 setuptools/distutils 有点坏了**

---

# 先看最关键报错

这句最重要：

```text
java.lang.IllegalAccessError: ... cannot access class sun.nio.ch.DirectBuffer
```

这基本就是：

> **Spark 3.2 + Java 17/更高版本 = 不兼容**

所以你现在要修的不是 Python 代码，而是**运行环境**。

---

# 你的问题分成两层

## 第一层：主问题

```text
IllegalAccessError
```

这个导致 SparkContext 起不来，所以程序直接挂了。

---

## 第二层：次要问题

```text
ModuleNotFoundError: No module named '_distutils_hack'
```

这个说明你的 `spark38` 环境里，`setuptools` / `distutils` 有点异常。
它会报 warning，但**当前真正让程序死掉的还是 Java 问题**。

---

# 先修主问题：强制改成 Java 11

## 第1步：检查你当前到底用的是哪个 Java

在终端运行：

```bash
echo $JAVA_HOME
java -version
which java
```

如果看到 `17`，那就是问题所在。

---

## 第2步：临时切到 Java 11

运行：

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH=$JAVA_HOME/bin:$PATH
java -version
```

你应该看到类似：

```text
openjdk version "11.x"
```

---

## 第3步：再跑你的程序

建议这样跑：

```bash
python 08_RDD_operators_groupBy.py
```

或者更稳一点：

```bash
spark-submit 08_RDD_operators_groupBy.py
```

---

# 更稳的长期方案：改 Spark 的配置文件

去你真正的 Spark 配置目录，不是当前这个 `01_RDD` 目录。

大概率是：

```bash
cd /Users/yonggan/opt/spark-3.2.0-bin-hadoop3.2/conf
```

如果没有配置文件：

```bash
cp spark-env.sh.template spark-env.sh
```

然后编辑 `spark-env.sh`：

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PYSPARK_PYTHON=/Users/yonggan/anaconda3/envs/spark38/bin/python
export PYSPARK_DRIVER_PYTHON=/Users/yonggan/anaconda3/envs/spark38/bin/python
export SPARK_LOCAL_IP=127.0.0.1
```

这样 Spark 每次都会固定用 Java 11。

---

# 再修次要问题：`_distutils_hack`

这个一般是 `setuptools` 装坏了。

在 `spark38` 里运行：

```bash
conda activate spark38
python -m pip install --upgrade pip setuptools
```

如果还不行，再补一个：

```bash
python -m pip install distlib
```

或者直接重装 setuptools：

```bash
python -m pip uninstall setuptools -y
python -m pip install setuptools
```

---

# 最推荐你现在直接执行这一组

按顺序来：

```bash
conda activate spark38

export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH=$JAVA_HOME/bin:$PATH

java -version
echo $JAVA_HOME

python -m pip install --upgrade pip setuptools

spark-submit 08_RDD_operators_groupBy.py
```

---

# 你这个报错怎么快速识别

以后看到这种：

```text
IllegalAccessError
cannot access sun.nio.ch.DirectBuffer
```

直接判断：

> **Spark 版本老，Java 版本太新**

这是典型环境兼容问题，不是业务代码问题。

---

# 最后一句

你现在先不要继续改 `groupBy.py` 代码。
先把 **Java 固定到 11**，这个报错大概率就没了；`_distutils_hack` 再顺手修掉。

把下面三条命令的输出发我，我可以直接帮你判断现在有没有切成功：

```bash
echo $JAVA_HOME
java -version
which java
```


在 **vim** 里，“下一行插入”的快捷键是：

---

# ✅ 最常用

```bash
o
```

👉 含义：

* 在**当前行的下一行**新开一行
* 并自动进入 **insert 模式**

---

# ✅ 对比（很重要）

| 操作    | 快捷键 | 含义           |
| ----- | --- | ------------ |
| 下一行插入 | `o` | 在当前行**下面**插入 |
| 上一行插入 | `O` | 在当前行**上面**插入 |

---

# ✅ 使用流程（面试/实战）

```bash
按 ESC → 按 o → 开始输入
```

---

# 🧠 一句话记忆

👉 `o = open below`
👉 `O = open above`

---

# ⚡ 小技巧

如果你想在**行尾继续写**：

```bash
A
```

如果想在**行首插入**：

```bash
I
```

---

需要的话我可以给你一份
👉 **vim 高频命令（面试 + 实战一页纸）** 👍

```
(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % ./spark-env.sh 
Python 3.8.20
/Users/yonggan/anaconda3/envs/spark38/bin/python
(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % python 08_RDD_operators_groupBy.py
Error processing line 1 of /Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/distutils-precedence.pth:

  Traceback (most recent call last):
    File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site.py", line 177, in addpackage
      exec(line)
    File "<string>", line 1, in <module>
  ModuleNotFoundError: No module named '_distutils_hack'

Remainder of file ignored
Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/04/02 04:57:28 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Traceback (most recent call last):
  File "08_RDD_operators_groupBy.py", line 7, in <module>
    sc = SparkContext(conf=conf)
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/pyspark/context.py", line 146, in __init__
    self._do_init(master, appName, sparkHome, pyFiles, environment, batchSize, serializer,
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/pyspark/context.py", line 209, in _do_init
    self._jsc = jsc or self._initialize_context(self._conf._jconf)
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/pyspark/context.py", line 329, in _initialize_context
    return self._jvm.JavaSparkContext(jconf)
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/py4j/java_gateway.py", line 1573, in __call__
    return_value = get_return_value(
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/py4j/protocol.py", line 326, in get_return_value
    raise Py4JJavaError(
py4j.protocol.Py4JJavaError: An error occurred while calling None.org.apache.spark.api.java.JavaSparkContext.
: java.lang.IllegalAccessError: class org.apache.spark.storage.StorageUtils$ (in unnamed module @0x2913da72) cannot access class sun.nio.ch.DirectBuffer (in module java.base) because module java.base does not export sun.nio.ch to unnamed module @0x2913da72
        at org.apache.spark.storage.StorageUtils$.<init>(StorageUtils.scala:213)
        at org.apache.spark.storage.StorageUtils$.<clinit>(StorageUtils.scala)
        at org.apache.spark.storage.BlockManagerMasterEndpoint.<init>(BlockManagerMasterEndpoint.scala:110)
        at org.apache.spark.SparkEnv$.$anonfun$create$9(SparkEnv.scala:348)
        at org.apache.spark.SparkEnv$.registerOrLookupEndpoint$1(SparkEnv.scala:287)
        at org.apache.spark.SparkEnv$.create(SparkEnv.scala:336)
        at org.apache.spark.SparkEnv$.createDriverEnv(SparkEnv.scala:191)
        at org.apache.spark.SparkContext.createSparkEnv(SparkContext.scala:277)
        at org.apache.spark.SparkContext.<init>(SparkContext.scala:460)
        at org.apache.spark.api.java.JavaSparkContext.<init>(JavaSparkContext.scala:58)
        at java.base/jdk.internal.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)
        at java.base/jdk.internal.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:77)
        at java.base/jdk.internal.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)
        at java.base/java.lang.reflect.Constructor.newInstanceWithCaller(Constructor.java:500)
        at java.base/java.lang.reflect.Constructor.newInstance(Constructor.java:481)
        at py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:247)
        at py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:357)
        at py4j.Gateway.invoke(Gateway.java:238)
        at py4j.commands.ConstructorCommand.invokeConstructor(ConstructorCommand.java:80)
        at py4j.commands.ConstructorCommand.execute(ConstructorCommand.java:69)
        at py4j.ClientServerConnection.waitForCommands(ClientServerConnection.java:182)
        at py4j.ClientServerConnection.run(ClientServerConnection.java:106)
        at java.base/java.lang.Thread.run(Thread.java:840)

```

对，你现在这个结果说明：

# 结论

`./spark-env.sh` **只证明了 Python 环境对了**，**没有证明 Java 对了**。

你看到的是：

```bash
Python 3.8.20
/Users/yonggan/anaconda3/envs/spark38/bin/python
```

但后面的 Spark 还是报：

```text
IllegalAccessError ... cannot access sun.nio.ch.DirectBuffer
```

这还是典型的：

> **Spark 3.2 正在跑到 Java 17 上了**

---

# 为什么你这个 `spark-env.sh` 没解决问题

因为你现在执行的是：

```bash
./spark-env.sh
```

这只是在**当前子 shell**里运行了一个脚本。
脚本结束后，它设置的环境变量**不会保留到你后面的 `python ...` 命令**。

所以你虽然看到了 Python 对了，但后面运行 `python 08_RDD_operators_groupBy.py` 时，Spark 还是可能拿到了错误的 Java。

---

# 你现在最该做的事

先直接在**当前终端**里执行下面这几行，不要通过 `./spark-env.sh`：

```bash
source ~/anaconda3/etc/profile.d/conda.sh
conda activate spark38

export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH=$JAVA_HOME/bin:$PATH
export PYSPARK_PYTHON=/Users/yonggan/anaconda3/envs/spark38/bin/python
export PYSPARK_DRIVER_PYTHON=/Users/yonggan/anaconda3/envs/spark38/bin/python
export SPARK_LOCAL_IP=127.0.0.1
```

然后马上检查：

```bash
echo $JAVA_HOME
java -version
which java
```

你必须看到 **Java 11**。

---

# 然后再运行

```bash
python 08_RDD_operators_groupBy.py
```

或者更推荐：

```bash
spark-submit 08_RDD_operators_groupBy.py
```

---

# 如果你想用脚本，正确方式不是 `./spark-env.sh`

而是：

```bash
source ./spark-env.sh
```

或者简写：

```bash
. ./spark-env.sh
```

因为：

* `./spark-env.sh` → 开一个子 shell 执行，变量不保留
* `source ./spark-env.sh` → 在当前 shell 执行，变量会保留

---

# 你的脚本应该写成这样

```bash
#!/bin/zsh
source ~/anaconda3/etc/profile.d/conda.sh
conda activate spark38
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH=$JAVA_HOME/bin:$PATH
export PYSPARK_PYTHON=/Users/yonggan/anaconda3/envs/spark38/bin/python
export PYSPARK_DRIVER_PYTHON=/Users/yonggan/anaconda3/envs/spark38/bin/python
export SPARK_LOCAL_IP=127.0.0.1
```

然后这样用：

```bash
source ./spark-env.sh
```

再检查：

```bash
java -version
echo $JAVA_HOME
which java
```

---

# 另外一个小问题：`_distutils_hack`

这个是次要问题，不是当前主因。先修 Java。

修法：

```bash
python -m pip install --upgrade pip setuptools
```

如果还报，再执行：

```bash
python -m pip uninstall setuptools -y
python -m pip install setuptools
```

---

# 你现在卡住的本质

不是 groupBy，不是 Python 代码。
是这两个点：

1. **Spark 3.2 + Java 17 不兼容**
2. **你用 `./spark-env.sh`，环境变量没留在当前 shell**

---

# 最短修复步骤

直接复制跑：

```bash
source ~/anaconda3/etc/profile.d/conda.sh
conda activate spark38
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH=$JAVA_HOME/bin:$PATH
java -version
python -m pip install --upgrade pip setuptools
spark-submit 08_RDD_operators_groupBy.py
```

---

把这三个命令的输出贴我，我可以直接帮你确认是不是已经切对了：

```bash
echo $JAVA_HOME
java -version
which java
```


在 **Terminal（命令行）里整行删除**，最常用的是👇

---

# ✅ 一键删除整行

```bash
Ctrl + U
```

👉 含义：

* 从**光标位置删除到行首**
* 如果光标在行尾 → 相当于**删整行**

---

# ✅ 常用组合（一起记）

| 快捷键        | 作用              |
| ---------- | --------------- |
| `Ctrl + U` | 删除到行首（常用 = 整行删） |
| `Ctrl + K` | 删除到行尾           |
| `Ctrl + A` | 跳到行首            |
| `Ctrl + E` | 跳到行尾            |

---

# 🧠 一句话记忆

👉 `U = up（往前删）`
👉 `K = kill（往后删）`

---

# ⚡ 小技巧

如果你想**删除整行（无论光标在哪）**：

```bash
Ctrl + A → Ctrl + K
```

---
```
需要我给你整理一份
👉 **Terminal / Linux 高频快捷键（面试 + 实战）一页纸** 👍

```
(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH=$JAVA_HOME/bin:$PATH
(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % python 09_RDD_operators_filter.py 
Error processing line 1 of /Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/distutils-precedence.pth:

  Traceback (most recent call last):
    File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site.py", line 177, in addpackage
      exec(line)
    File "<string>", line 1, in <module>
  ModuleNotFoundError: No module named '_distutils_hack'

Remainder of file ignored
26/04/02 05:03:07 WARN Utils: Your hostname, Yonggans-MacBook-Pro.local resolves to a loopback address: 127.0.0.1; using 10.0.0.21 instead (on interface en0)
26/04/02 05:03:07 WARN Utils: Set SPARK_LOCAL_IP if you need to bind to another address
WARNING: An illegal reflective access operation has occurred
WARNING: Illegal reflective access by org.apache.spark.unsafe.Platform (file:/Users/yonggan/opt/spark-3.2.0-bin-hadoop3.2/jars/spark-unsafe_2.12-3.2.0.jar) to constructor java.nio.DirectByteBuffer(long,int)
WARNING: Please consider reporting this to the maintainers of org.apache.spark.unsafe.Platform
WARNING: Use --illegal-access=warn to enable warnings of further illegal reflective access operations
WARNING: All illegal access operations will be denied in a future release
Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/04/02 05:03:08 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Error processing line 1 of /Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/distutils-precedence.pth:

  Traceback (most recent call last):
    File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site.py", line 177, in addpackage
      exec(line)
    File "<string>", line 1, in <module>
  ModuleNotFoundError: No module named '_distutils_hack'

Remainder of file ignored
[1, 3, 5]                                                                       
(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % 
  ```

(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH=$JAVA_HOME/bin:$PATH
(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % python 09_RDD_operators_filter.py 
Error processing line 1 of /Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/distutils-precedence.pth:

  Traceback (most recent call last):
    File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site.py", line 177, in addpackage
      exec(line)
    File "<string>", line 1, in <module>
  ModuleNotFoundError: No module named '_distutils_hack'

Remainder of file ignored
26/04/02 05:03:07 WARN Utils: Your hostname, Yonggans-MacBook-Pro.local resolves to a loopback address: 127.0.0.1; using 10.0.0.21 instead (on interface en0)
26/04/02 05:03:07 WARN Utils: Set SPARK_LOCAL_IP if you need to bind to another address
WARNING: An illegal reflective access operation has occurred
WARNING: Illegal reflective access by org.apache.spark.unsafe.Platform (file:/Users/yonggan/opt/spark-3.2.0-bin-hadoop3.2/jars/spark-unsafe_2.12-3.2.0.jar) to constructor java.nio.DirectByteBuffer(long,int)
WARNING: Please consider reporting this to the maintainers of org.apache.spark.unsafe.Platform
WARNING: Use --illegal-access=warn to enable warnings of further illegal reflective access operations
WARNING: All illegal access operations will be denied in a future release
Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/04/02 05:03:08 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Error processing line 1 of /Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/distutils-precedence.pth:

  Traceback (most recent call last):
    File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site.py", line 177, in addpackage
      exec(line)
    File "<string>", line 1, in <module>
  ModuleNotFoundError: No module named '_distutils_hack'

Remainder of file ignored
[1, 3, 5]                                                                       
(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % 
```

好了，**这次已经跑通了** ✅

你最后输出了：

```python
[1, 3, 5]
```

说明：

* `SparkContext` 已经成功启动
* `filter` 算子正常执行
* **Java 11 切换生效了**
* 主问题已经解决了

---

# 现在怎么看这些信息

## 1. 成功信号

最关键的是最后有结果：

```python
[1, 3, 5]
```

这表示程序已经正常跑完。

---

## 2. 现在剩下的是“警告”，不是致命错误

### 这个警告：

```text
WARN Utils: hostname resolves to a loopback address
```

不是大问题。
是 Spark 在本机启动时发现 hostname 先解析到 `127.0.0.1`。

你可以加这个避免它：

```bash
export SPARK_LOCAL_IP=127.0.0.1
```

---

### 这个警告：

```text
Illegal reflective access
```

也不是当前 blocker。
这是 **Spark 3.2 + Java 11** 常见兼容告警之一。

重点是：

* **Java 17** 时会直接炸
* **Java 11** 时通常只是 warning，可以跑

所以你现在是正常状态。

---

## 3. 这个还是环境小问题

```text
ModuleNotFoundError: No module named '_distutils_hack'
```

这说明你当前 conda 环境里的 `setuptools` 有点不完整。
但因为程序已经跑出来了，所以它现在只是“脏 warning”。

---

# 下一步建议

## 先修一下 `_distutils_hack`

在 `spark38` 环境里执行：

```bash
python -m pip install --upgrade pip setuptools
```

如果还有，再执行：

```bash
python -m pip uninstall setuptools -y
python -m pip install setuptools
```

---

## 再固定本地 Spark 环境

你每次都手动 export 很麻烦，可以放到真正的 Spark 配置里：

```bash
/Users/yonggan/opt/spark-3.2.0-bin-hadoop3.2/conf/spark-env.sh
```

内容建议写成：

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PYSPARK_PYTHON=/Users/yonggan/anaconda3/envs/spark38/bin/python
export PYSPARK_DRIVER_PYTHON=/Users/yonggan/anaconda3/envs/spark38/bin/python
export SPARK_LOCAL_IP=127.0.0.1
```

---

# 一句话总结

你现在已经从“**跑不起来**”变成“**能跑，只剩环境告警**”。

---

# 面试式表达

你可以这样说：

> I identified that the root cause was a Java compatibility issue. Spark 3.2 failed under a newer JDK, so I standardized the runtime to Java 11. After that, the Spark job ran successfully, and the remaining messages were only non-blocking environment warnings.

如果你愿意，我下一条直接给你一份 **最终版 Mac M1 Spark 本地环境配置清单**。


```
(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD % python 11_RDD_operators_union.py 
WARNING: An illegal reflective access operation has occurred
WARNING: Illegal reflective access by org.apache.spark.unsafe.Platform (file:/Users/yonggan/opt/spark-3.2.0-bin-hadoop3.2/jars/spark-unsafe_2.12-3.2.0.jar) to constructor java.nio.DirectByteBuffer(long,int)
WARNING: Please consider reporting this to the maintainers of org.apache.spark.unsafe.Platform
WARNING: Use --illegal-access=warn to enable warnings of further illegal reflective access operations
WARNING: All illegal access operations will be denied in a future release
Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/04/02 05:22:28 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
[1, 1, 3, 3, 'a', 'b', 'a']
(spark38) yonggan@Yonggans-MacBook-Pro 01_RDD %
```

这次是**正常运行**，没问题。

你已经看到结果了：

```python
[1, 1, 3, 3, 'a', 'b', 'a']
```

说明 `union` 成功执行了。

---

# 你现在看到的这些是什么

## 1. 这是 warning，不是 error

比如：

```text
WARNING: An illegal reflective access operation has occurred
```

这个在 **Spark 3.2 + Java 11** 下很常见。
重点是：

* 程序**能跑**
* 有输出
* 没崩

所以现在不用慌。

---

## 2. 你的 `union` 结果也合理

如果你的代码大概是把两个 RDD 合并，比如：

* 第一个 RDD: `[1, 1, 3, 3]`
* 第二个 RDD: `['a', 'b', 'a']`

那么：

```python
rdd1.union(rdd2).collect()
```

结果就是：

```python
[1, 1, 3, 3, 'a', 'b', 'a']
```

---

# `union` 的核心理解

## Spark RDD `union`

* 只是把两个 RDD **拼接**
* **不会去重**
* 顺序通常表现为：前一个 RDD 的数据 + 后一个 RDD 的数据

---

# 和 `distinct()` 区别

如果你想去重，要再接：

```python
rdd1.union(rdd2).distinct().collect()
```

---

# 一句话记忆

> `union = combine, not deduplicate`

---

# 你现在的状态

你本地 Spark 环境已经基本能用了：

* `filter` 跑通了
* `union` 跑通了
* Java 主问题已经解决了

现在剩下的只是一些非阻塞 warning。

---

# 你可以继续这样做

每次开新 terminal 后先执行：

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH=$JAVA_HOME/bin:$PATH
export SPARK_LOCAL_IP=127.0.0.1
```

然后再跑：

```bash
python 11_RDD_operators_union.py
```

---

# 面试里怎么说

> `union` combines two RDDs into one and keeps all elements, including duplicates.

如果你要，我下一条可以把 **RDD 高频 operators：map / flatMap / filter / distinct / union / groupByKey / reduceByKey** 给你做成一个超清晰对比表。

```
/Users/yonggan/anaconda3/envs/spark38/bin/python /Users/yonggan/Downloads/Spark-202603/learning/01_RDD/15_RDD_operators_gorupByKey.py 
26/04/02 05:23:43 WARN Utils: Your hostname, Yonggans-MacBook-Pro.local resolves to a loopback address: 127.0.0.1; using 10.0.0.21 instead (on interface en0)
26/04/02 05:23:43 WARN Utils: Set SPARK_LOCAL_IP if you need to bind to another address
Exception in thread "main" java.lang.ExceptionInInitializerError
	at org.apache.spark.unsafe.array.ByteArrayMethods.<clinit>(ByteArrayMethods.java:54)
	at org.apache.spark.internal.config.package$.<init>(package.scala:1149)
	at org.apache.spark.internal.config.package$.<clinit>(package.scala)
	at org.apache.spark.deploy.SparkSubmitArguments.$anonfun$loadEnvironmentArguments$3(SparkSubmitArguments.scala:157)
	at scala.Option.orElse(Option.scala:447)
	at org.apache.spark.deploy.SparkSubmitArguments.loadEnvironmentArguments(SparkSubmitArguments.scala:157)
	at org.apache.spark.deploy.SparkSubmitArguments.<init>(SparkSubmitArguments.scala:115)
	at org.apache.spark.deploy.SparkSubmit$$anon$2$$anon$3.<init>(SparkSubmit.scala:1026)
	at org.apache.spark.deploy.SparkSubmit$$anon$2.parseArguments(SparkSubmit.scala:1026)
	at org.apache.spark.deploy.SparkSubmit.doSubmit(SparkSubmit.scala:85)
	at org.apache.spark.deploy.SparkSubmit$$anon$2.doSubmit(SparkSubmit.scala:1043)
	at org.apache.spark.deploy.SparkSubmit$.main(SparkSubmit.scala:1052)
	at org.apache.spark.deploy.SparkSubmit.main(SparkSubmit.scala)
Caused by: java.lang.IllegalStateException: java.lang.NoSuchMethodException: java.nio.DirectByteBuffer.<init>(long,int)
	at org.apache.spark.unsafe.Platform.<clinit>(Platform.java:113)
	... 13 more
Caused by: java.lang.NoSuchMethodException: java.nio.DirectByteBuffer.<init>(long,int)
	at java.base/java.lang.Class.getConstructor0(Class.java:3218)
	at java.base/java.lang.Class.getDeclaredConstructor(Class.java:2493)
	at org.apache.spark.unsafe.Platform.<clinit>(Platform.java:71)
	... 13 more
Traceback (most recent call last):
  File "/Users/yonggan/Downloads/Spark-202603/learning/01_RDD/15_RDD_operators_gorupByKey.py", line 7, in <module>
    sc = SparkContext(conf=conf)
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/pyspark/context.py", line 144, in __init__
    SparkContext._ensure_initialized(self, gateway=gateway, conf=conf)
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/pyspark/context.py", line 339, in _ensure_initialized
    SparkContext._gateway = gateway or launch_gateway(conf)
  File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/pyspark/java_gateway.py", line 108, in launch_gateway
    raise RuntimeError("Java gateway process exited before sending its port number")
RuntimeError: Java gateway process exited before sending its port number

Process finished with exit code 1
```





