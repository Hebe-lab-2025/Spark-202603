```
/Users/yonggan/anaconda3/envs/spark38/bin/python /Users/yonggan/Downloads/Spark-202603/learning/01_RDD/07_RDD_wordcount_example.py  Error processing line 1 of /Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/distutils-precedence.pth:    Traceback (most recent call last):     File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site.py", line 177, in addpackage       exec(line)     File "<string>", line 1, in <module>   ModuleNotFoundError: No module named '_distutils_hack'  Remainder of file ignored 26/04/02 04:23:03 WARN Utils: Your hostname, Yonggans-MacBook-Pro.local resolves to a loopback address: 127.0.0.1; using 10.0.0.21 instead (on interface en0) 26/04/02 04:23:03 WARN Utils: Set SPARK_LOCAL_IP if you need to bind to another address Exception in thread "main" java.lang.ExceptionInInitializerError 	at org.apache.spark.unsafe.array.ByteArrayMethods.<clinit>(ByteArrayMethods.java:54) 	at org.apache.spark.internal.config.package$.<init>(package.scala:1149) 	at org.apache.spark.internal.config.package$.<clinit>(package.scala) 	at org.apache.spark.deploy.SparkSubmitArguments.$anonfun$loadEnvironmentArguments$3(SparkSubmitArguments.scala:157) 	at scala.Option.orElse(Option.scala:447) 	at org.apache.spark.deploy.SparkSubmitArguments.loadEnvironmentArguments(SparkSubmitArguments.scala:157) 	at org.apache.spark.deploy.SparkSubmitArguments.<init>(SparkSubmitArguments.scala:115) 	at org.apache.spark.deploy.SparkSubmit$$anon$2$$anon$3.<init>(SparkSubmit.scala:1026) 	at org.apache.spark.deploy.SparkSubmit$$anon$2.parseArguments(SparkSubmit.scala:1026) 	at org.apache.spark.deploy.SparkSubmit.doSubmit(SparkSubmit.scala:85) 	at org.apache.spark.deploy.SparkSubmit$$anon$2.doSubmit(SparkSubmit.scala:1043) 	at org.apache.spark.deploy.SparkSubmit$.main(SparkSubmit.scala:1052) 	at org.apache.spark.deploy.SparkSubmit.main(SparkSubmit.scala) Caused by: java.lang.IllegalStateException: java.lang.NoSuchMethodException: java.nio.DirectByteBuffer.<init>(long,int) 	at org.apache.spark.unsafe.Platform.<clinit>(Platform.java:113) 	... 13 more Caused by: java.lang.NoSuchMethodException: java.nio.DirectByteBuffer.<init>(long,int) 	at java.base/java.lang.Class.getConstructor0(Class.java:3218) 	at java.base/java.lang.Class.getDeclaredConstructor(Class.java:2493) 	at org.apache.spark.unsafe.Platform.<clinit>(Platform.java:71) 	... 13 more Traceback (most recent call last):   File "/Users/yonggan/Downloads/Spark-202603/learning/01_RDD/07_RDD_wordcount_example.py", line 7, in <module>     sc = SparkContext(conf=conf)   File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/pyspark/context.py", line 144, in __init__     SparkContext._ensure_initialized(self, gateway=gateway, conf=conf)   File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/pyspark/context.py", line 339, in _ensure_initialized     SparkContext._gateway = gateway or launch_gateway(conf)   File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/pyspark/java_gateway.py", line 108, in launch_gateway     raise RuntimeError("Java gateway process exited before sending its port number") RuntimeError: Java gateway process exited before sending its port number  Process finished with exit code 1 ---中文解决
```
你这个报错 **不是一处问题**，而是 **两个独立问题叠加**：

---

# 先说结论

## 真正导致 Spark 起不来的核心原因

是这个：

```text
Caused by: java.lang.NoSuchMethodException: java.nio.DirectByteBuffer.<init>(long,int)
...
RuntimeError: Java gateway process exited before sending its port number
```

这通常说明：

**你的 Spark 版本 和 当前 Java 版本不兼容。**

最常见情况是：

* 你装的是 **Spark 3.2.x / 3.3.x**
* 但你现在跑的是 **Java 17 / 21 / 24**
* 这时 PySpark 经常直接炸掉

---

## 另一个问题

这个：

```text
ModuleNotFoundError: No module named '_distutils_hack'
```

说明你的 `spark38` 这个 conda 环境里：

**setuptools / distutils 相关包坏了或者不完整**

这个问题会先报 warning/error，但 **不是最致命的主因**。
真正让 Spark 启动失败的，还是 **Java 版本不匹配**。

---

# 你现在应该怎么修

按这个顺序做，最快。

---

# 第一步：先检查 Java 版本

在终端执行：

```bash
java -version
echo $JAVA_HOME
```

如果你看到类似：

* `17`
* `21`
* `24`

那基本就是根因了。

---

# 第二步：把 Java 切到 8 或 11

对于 Spark 3.2 / 3.3，最稳的是：

* **Java 8**
* 或 **Java 11**

Mac 上先看你有没有装过这些版本：

```bash
/usr/libexec/java_home -V
```

如果有 Java 11，比如输出里有：

```text
11.0.x
```

那就临时切过去：

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH=$JAVA_HOME/bin:$PATH
java -version
```

如果你有 Java 8，也可以：

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 1.8)
export PATH=$JAVA_HOME/bin:$PATH
java -version
```

---

# 第三步：再跑你的 PySpark 程序

```bash
/Users/yonggan/anaconda3/envs/spark38/bin/python /Users/yonggan/Downloads/Spark-202603/learning/01_RDD/07_RDD_wordcount_example.py
```

很多时候，**切到 Java 8/11 后就直接好了**。

---

# 第四步：修复 `_distutils_hack` 问题

激活你的 conda 环境：

```bash
conda activate spark38
```

然后重新装一遍 setuptools：

```bash
pip uninstall -y setuptools
pip install setuptools
```

如果还不行，再补一遍：

```bash
pip install --upgrade pip setuptools wheel
```

然后测试：

```bash
python -c "import setuptools; import _distutils_hack; print('ok')"
```

如果输出 `ok`，说明这个问题修好了。

---

# 更稳的完整修法

我建议你直接这样做：

## 1）激活环境

```bash
conda activate spark38
```

## 2）修 Python 包

```bash
pip uninstall -y setuptools
pip install --upgrade pip setuptools wheel
```

## 3）切 Java 11

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH=$JAVA_HOME/bin:$PATH
java -version
```

## 4）可选：加本机 IP，去掉 Spark warning

```bash
export SPARK_LOCAL_IP=127.0.0.1
```

## 5）再运行

```bash
python /Users/yonggan/Downloads/Spark-202603/learning/01_RDD/07_RDD_wordcount_example.py
```

---

# 如果你没有 Java 11

可以安装。

如果你用 Homebrew：

```bash
brew install openjdk@11
```

然后可能要加：

```bash
sudo ln -sfn /opt/homebrew/opt/openjdk@11/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-11.jdk
```

再检查：

```bash
/usr/libexec/java_home -V
```

然后切换：

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH=$JAVA_HOME/bin:$PATH
```

---

# 为什么会报这个 DirectByteBuffer 错误

你看到的是：

```text
NoSuchMethodException: java.nio.DirectByteBuffer.<init>(long,int)
```

这类错误本质上是：

**Spark 内部用了某些低层 Java API，旧 Spark 版本和新 JDK 不兼容。**

所以不是你 Python 代码写错了，
而是：

**Spark 启动阶段就挂了。**

于是 Python 侧只能看到：

```text
RuntimeError: Java gateway process exited before sending its port number
```

意思就是：

**JVM 还没起来，PySpark 就连不上 Java gateway。**

---

# 那个 hostname warning 要不要管

这个：

```text
WARN Utils: Your hostname ... resolves to a loopback address
WARN Utils: Set SPARK_LOCAL_IP if you need to bind to another address
```

通常 **不是致命问题**。

你本地学习环境里可以直接加：

```bash
export SPARK_LOCAL_IP=127.0.0.1
```

就行。

---

# 我建议你最终固定到 `.zshrc`

如果你以后都用 Spark 3.2/3.3，本地可以固定：

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH=$JAVA_HOME/bin:$PATH
export SPARK_LOCAL_IP=127.0.0.1
```

然后：

```bash
source ~/.zshrc
```

---

# 一套最直接可复制命令

你直接按这个跑：

```bash
conda activate spark38

pip uninstall -y setuptools
pip install --upgrade pip setuptools wheel

export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH=$JAVA_HOME/bin:$PATH
export SPARK_LOCAL_IP=127.0.0.1

java -version
python -c "import setuptools; import _distutils_hack; print('python ok')"

python /Users/yonggan/Downloads/Spark-202603/learning/01_RDD/07_RDD_wordcount_example.py
```

---

# 预期结果

如果修对了：

1. `_distutils_hack` 不再报错
2. `Java gateway process exited before sending its port number` 消失
3. SparkContext 能正常创建
4. wordcount 程序开始执行

---

# 你这个问题一句话总结

**主因是 Java 版本过高导致 Spark 启动失败，次因是 conda 环境里的 setuptools 坏了；先切到 Java 8/11，再重装 setuptools，基本就能解决。**

把这几个命令的输出发我，我可以直接帮你定位到哪一步还没对：

```bash
java -version
echo $JAVA_HOME
/usr/libexec/java_home -V
conda list | grep setuptools
python -c "import _distutils_hack; print('ok')"
```


```
/Users/yonggan/anaconda3/envs/spark38/bin/python /Users/yonggan/Downloads/Spark-202603/learning/01_RDD/07_RDD_wordcount_example.py 
Error processing line 1 of /Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site-packages/distutils-precedence.pth:

  Traceback (most recent call last):
    File "/Users/yonggan/anaconda3/envs/spark38/lib/python3.8/site.py", line 177, in addpackage
      exec(line)
    File "<string>", line 1, in <module>
  ModuleNotFoundError: No module named '_distutils_hack'

Remainder of file ignored
26/04/02 04:24:36 WARN Utils: Your hostname, Yonggans-MacBook-Pro.local resolves to a loopback address: 127.0.0.1; using 10.0.0.21 instead (on interface en0)
26/04/02 04:24:36 WARN Utils: Set SPARK_LOCAL_IP if you need to bind to another address
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
  File "/Users/yonggan/Downloads/Spark-202603/learning/01_RDD/07_RDD_wordcount_example.py", line 7, in <module>
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

你这个报错还是同一个结论：

## 核心根因

**Spark 和 Java 版本不兼容**，这才是导致程序直接起不来的主因。
你这个关键报错是：

```text
Caused by: java.lang.NoSuchMethodException: java.nio.DirectByteBuffer.<init>(long,int)
```

这类错误通常出现在 **旧版 Spark 搭配较新的 Java** 时。Spark 官方现在的最新文档里说明，**Spark 4.x 需要 Java 17+**，而 Spark 3.5 还明确写了 **Java 8/11 支持将在下个大版本移除**，反过来也说明 Spark 3.x 时代和 Java 版本的搭配很敏感。([Apache Spark][1])

你日志里的栈看起来更像是：
**你现在本地不是 Spark 4.x，而是较老的 Spark 3.2/3.3 一类版本，却跑在过高的 Java 上**，所以 JVM 在 Spark 启动阶段就挂了，最终 PySpark 才报：

```text
RuntimeError: Java gateway process exited before sending its port number
```

这是结果，不是根因。([Apache Spark][2])

---

# 另一个问题

这个：

```text
ModuleNotFoundError: No module named '_distutils_hack'
```

说明你当前 `spark38` 环境里的 **setuptools/distutils 也坏了**。
它不是最底层主因，但也应该一起修，不然后面还会继续出别的问题。

---

# 最直接解决方案

## 方案 A：不升级 Spark，直接把 Java 切到 11

这通常是最快的。

### 1）先查你现在的 Java

在终端运行：

```bash
java -version
echo $JAVA_HOME
/usr/libexec/java_home -V
```

---

### 2）如果你机器里有 Java 11，切过去

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH=$JAVA_HOME/bin:$PATH
export SPARK_LOCAL_IP=127.0.0.1
java -version
```

---

### 3）修 Python 环境里的 setuptools

先激活环境：

```bash
conda activate spark38
```

然后执行：

```bash
pip uninstall -y setuptools
pip install --upgrade pip setuptools wheel
```

再验证：

```bash
python -c "import setuptools; import _distutils_hack; print('ok')"
```

如果打印 `ok`，说明这部分修好了。

---

### 4）重新运行

```bash
python /Users/yonggan/Downloads/Spark-202603/learning/01_RDD/07_RDD_wordcount_example.py
```

---

# 一套你可以直接复制的命令

```bash
conda activate spark38

pip uninstall -y setuptools
pip install --upgrade pip setuptools wheel

export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH=$JAVA_HOME/bin:$PATH
export SPARK_LOCAL_IP=127.0.0.1

java -version
python -c "import setuptools; import _distutils_hack; print('python ok')"

python /Users/yonggan/Downloads/Spark-202603/learning/01_RDD/07_RDD_wordcount_example.py
```

---

# 如果你没有 Java 11

可以装：

```bash
brew install openjdk@11
sudo ln -sfn /opt/homebrew/opt/openjdk@11/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-11.jdk
```

然后再：

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH=$JAVA_HOME/bin:$PATH
```

---

# 这几个 warning 怎么看

## 1）`_distutils_hack`

要修，但不是 Spark 崩掉的最核心原因。

## 2）`hostname resolves to a loopback address`

这个一般不是致命问题，本地学习环境直接：

```bash
export SPARK_LOCAL_IP=127.0.0.1
```

就够了。

## 3）`Java gateway process exited before sending its port number`

这只是说明：
**Java 进程先死了，PySpark 连不上。**
真正要看上面那个 Java 栈。

---

# 你现在最可能的真实情况

大概率是：

* Python 环境：`spark38`
* PySpark/Spark：老版本
* Java：17/21/更高
* 所以 Spark 初始化失败
* 同时 conda 环境里 `setuptools` 也坏了

---

# 你现在先不要改代码

**这不是你 `07_RDD_wordcount_example.py` 代码写错。**
是环境问题。

---

# 你下一步就做 3 件事

按顺序：

### 1.

```bash
java -version
```

### 2.

```bash
/usr/libexec/java_home -V
```

### 3.

```bash
conda activate spark38
python -c "import _distutils_hack; print('ok')"
```

把这三段输出发我，我可以直接告诉你该用 Java 11 还是要不要顺手重建这个 `spark38` 环境。

[1]: https://spark.apache.org/docs/latest/api/python/getting_started/install.html?utm_source=chatgpt.com "Installation — PySpark 4.1.0 documentation - Apache Spark"
[2]: https://spark.apache.org/releases/spark-release-3-2-0.html?utm_source=chatgpt.com "Spark Release 3.2.0"


这是 **PyCharm 和你终端环境不一致** 的典型问题（很常见 👍）。
你在 terminal 里 `conda activate spark38` 了，但 **PyCharm 不会自动用这个环境**。

---

# 一句话结论

👉 **PyCharm 用的是它自己配置的 interpreter，不是你 terminal 的 conda 环境**

---

# 正确做法（最关键）

## 方法1（推荐）：在 PyCharm 里绑定你的 conda 环境

### 步骤：

1. 打开 PyCharm
2. 进入：

   ```
   Preferences (Mac: ⌘ + ,)
   ```
3. 找到：

   ```
   Project → Python Interpreter
   ```
4. 点击右上角 ⚙️ → `Add Interpreter`
5. 选择：

   ```
   Conda Environment
   ```
6. 选择：

   ```
   Existing environment
   ```
7. 指向你的环境路径：

```bash
/Users/yonggan/anaconda3/envs/spark38/bin/python
```

8. 点击 OK

---

# 验证是否成功

在 PyCharm terminal 里运行：

```bash
which python
```

如果输出：

```bash
/Users/yonggan/anaconda3/envs/spark38/bin/python
```

说明成功 ✅

---

# 方法2：让 PyCharm Terminal 自动激活 conda（可选）

如果你想 PyCharm 里的 terminal 自动 `conda activate`：

### 设置路径：

```
Preferences → Tools → Terminal
```

把 Shell path 改成：

```bash
/bin/zsh -l
```

（`-l` = login shell，会加载你的 `.zshrc`）

---

然后在 `.zshrc` 里加：

```bash
conda activate spark38
```

⚠️ 注意：
不建议长期这样（会影响其他项目），但学习 Spark 可以先用。

---

# 为什么会这样（面试可以说）

👉 PyCharm 有自己的 Python interpreter 管理机制：

* terminal：你自己控制（conda activate）
* PyCharm run/debug：走 IDE 配置的 interpreter

所以会出现：

| 场景          | Python             |
| ----------- | ------------------ |
| terminal    | spark38 ✅          |
| PyCharm run | base / 系统 Python ❌ |

---

# 你的这个错误为什么一直没好

因为：

👉 你虽然在 terminal 修了环境
👉 但 PyCharm 运行代码 **没用那个环境**

所以：

* `_distutils_hack` 还是报错
* Java gateway 还是炸

---

# 最重要检查（马上做）

在 PyCharm 里运行：

```python
import sys
print(sys.executable)
```

如果不是：

```bash
/Users/yonggan/anaconda3/envs/spark38/bin/python
```

说明你还没切成功 ❌

---

# 最稳做法（推荐）

你现在直接：

### 1️⃣ PyCharm绑定 interpreter

### 2️⃣ 再执行：

```bash
pip install --upgrade setuptools
```

### 3️⃣ 再切 Java 11（很关键）

---

# 一句话总结

👉 **你现在不是环境没配好，而是 PyCharm 没用你配好的环境**

---

如果你愿意，我可以帮你做一套：

👉 **PyCharm + PySpark + Java 11 一次性无坑配置（面试级环境）**

包括：

* interpreter
* JAVA_HOME
* SPARK_HOME
* pyspark run config

直接一套跑通，不再踩坑 🔥


很好，这张图已经说明一件关键事情👇

# ✅ 当前状态（你做对了）

👉 PyCharm 已经 **正确绑定了你的 conda 环境**

```text
/anaconda3/envs/spark38/bin/python
```

✔ interpreter 没问题
✔ pyspark 3.2.0 已安装
✔ 不是 PyCharm 配置问题了

---

# ❗现在的问题只剩一个（核心）

👉 **Java 版本不对**

你报错里最关键的是：

```text
NoSuchMethodException: java.nio.DirectByteBuffer.<init>(long,int)
```

这个 100% 是：

> ❌ Spark 3.2.0 + 高版本 Java（17/21/24） → 直接崩

---

# 🚨 你现在卡住的真正原因

👉 PyCharm 虽然用对 Python 了
👉 但 **没有用你 terminal 里的 JAVA_HOME**

---

# ✅ 正确修法（关键）

## 方法1（最推荐）：在 PyCharm 里设置 Java

### 步骤：

1️⃣ 打开 Run Configuration
（右上角 ▶️旁边）

2️⃣ 找到你的 script：

```
07_RDD_wordcount_example.py
```

3️⃣ 找到：

```
Environment variables
```

4️⃣ 加上：

```bash
JAVA_HOME=/Library/Java/JavaVirtualMachines/openjdk-11.jdk/Contents/Home
SPARK_LOCAL_IP=127.0.0.1
```

👉 如果你不知道路径，先终端跑：

```bash
/usr/libexec/java_home -v 11
```

复制输出

---

## 方法2（更简单）：让 PyCharm 继承 terminal 环境

在 PyCharm Terminal 里运行：

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export SPARK_LOCAL_IP=127.0.0.1
```

然后用 PyCharm Run（有时候不稳定）

---

## 方法3（最稳，推荐面试环境）

直接写进 `.zshrc`：

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH=$JAVA_HOME/bin:$PATH
export SPARK_LOCAL_IP=127.0.0.1
```

然后：

```bash
source ~/.zshrc
```

---

# 🔧 你还有一个小问题（顺手修）

你现在：

```text
setuptools = 44.1.1 ❌ 太旧
```

这就是 `_distutils_hack` 报错原因

---

## 升级它：

在 PyCharm terminal 里：

```bash
pip install --upgrade setuptools
```

---

# ✅ 最终你应该达到的状态

## Java：

```bash
java -version
# → 11.x
```

## Python：

```python
import sys
print(sys.executable)
# → spark38
```

## setuptools：

```bash
pip show setuptools
# → >= 60+
```

---

# 🧠 一句话总结（面试级）

👉 **PySpark 启动失败通常是 JVM 层问题，而不是 Python 代码问题，尤其是 Spark 与 Java 版本不兼容时，Java gateway 会直接退出。**

---

# 🚀 下一步（我建议）

如果你想彻底不踩坑，我可以帮你一键配好：

👉 PyCharm + Spark + Java + 环境变量
👉 能跑 local / standalone / yarn
👉 面试直接讲架构

你现在只差最后一步（Java）就通了 🔥


可以，那就**不要硬改 Java 17**。
你现在最稳的路是：

# 直接结论

**保留 Java 17，把 Spark 从 3.2.0 升到 3.5.x。**

原因是：

* 你现在装的是 **pyspark 3.2.0**，而 Spark 社区在做 Java 17 支持时明确说了：**Java 17 支持是 3.3.0 的新特性，不能回补到 3.2 分支**。([Apache Issues][1])
* Spark 3.5 文档明确写着：**Spark 3.5.x 支持 Java 8/11/17，且支持 Python 3.8+**。这正好匹配你当前的 Python 3.8 环境。([Apache Spark][2])
* 你现在的报错 `DirectByteBuffer.<init>(long,int)` 本质上就是 **Spark 3.2.0 跑在 Java 17 上不兼容** 的表现。结合上面的官方兼容信息，继续死磕 3.2.0 没意义。([Apache Issues][1])

# 你现在该怎么做

在 **spark38** 环境里执行：

```bash
conda activate spark38

pip uninstall -y pyspark py4j spark
pip install --upgrade pip setuptools wheel
pip install pyspark==3.5.2
```

说明：

* `spark` 这个包你环境里还有一个 `spark 0.2.1`，它不是 Apache Spark 主包，容易添乱，建议一起卸掉。
* `pyspark==3.5.2` 是 3.5 系列稳定维护版本之一；Spark 官方也建议 3.5 用户升级到稳定维护版。([Apache Spark][3])

# 然后验证

先看包版本：

```bash
python -c "import pyspark; print(pyspark.__version__)"
```

你应该看到：

```bash
3.5.2
```

再跑你的脚本：

```bash
python /Users/yonggan/Downloads/Spark-202603/learning/01_RDD/07_RDD_wordcount_example.py
```

# 还要顺手修一个小坑

你之前还有这个错误：

```text
ModuleNotFoundError: No module named '_distutils_hack'
```

这通常是 `setuptools` 有问题。你刚才那条命令里已经顺手升级了：

```bash
pip install --upgrade pip setuptools wheel
```

这一步一般能一起修掉。若还报错，再补一遍：

```bash
pip uninstall -y setuptools
pip install setuptools
```

# PyCharm 里也要同步

因为你是从 PyCharm 跑的，所以升级完包后，确认 PyCharm 仍然指向这个解释器：

```text
/Users/yonggan/anaconda3/envs/spark38/bin/python
```

然后在 PyCharm terminal 里执行一次：

```bash
python -c "import pyspark; print(pyspark.__version__)"
```

确认它看到的是 3.5.2，不是旧的 3.2.0。

# 不推荐的路

## 1. 继续用 Spark 3.2.0 + Java 17

不推荐。
因为官方已经说明 Java 17 支持是 **从 3.3.0 开始的新特性**，不会回补到 3.2。([Apache Issues][1])

## 2. 直接升到 Spark 4.x

现在也不推荐。
因为 Spark 最新文档写的是 **Spark 4.x 需要 Java 17/21，Python 3.10+**，而你当前环境是 Python 3.8。([Apache Spark][4])

# 最适合你的组合

你现在最顺的组合就是：

* **Java 17**
* **Python 3.8**
* **PySpark 3.5.x**

这套是官方兼容的。([Apache Spark][2])

# 一套最省事命令

直接复制：

```bash
conda activate spark38
pip uninstall -y pyspark py4j spark
pip install --upgrade pip setuptools wheel
pip install pyspark==3.5.2
python -c "import pyspark; print(pyspark.__version__)"
python /Users/yonggan/Downloads/Spark-202603/learning/01_RDD/07_RDD_wordcount_example.py
```

如果你跑完后把这两段输出发我，我可以继续帮你看下一步：

```bash
python -c "import pyspark; print(pyspark.__version__)"
java -version
```

[1]: https://issues.apache.org/jira/browse/SPARK-33772 "[SPARK-33772] Build and Run Spark on Java 17 - ASF Jira"
[2]: https://spark.apache.org/docs/3.5.8/?utm_source=chatgpt.com "Overview - Spark 3.5.8 Documentation"
[3]: https://spark.apache.org/releases/spark-release-3-5-2.html?utm_source=chatgpt.com "Spark Release 3.5.2"
[4]: https://spark.apache.org/docs/latest/ "Overview - Spark 4.1.1 Documentation"


```
(spark38) yonggan@Yonggans-MacBook-Pro Spark-202603 % history                                                                                                          
 1408  git rm -r --cached .idea 2>/dev/null\ngit rm -r --cached spark-warehouse 2>/dev/null\ngit rm -r --cached metastore_db 2>/dev/null\ngit rm -r --cached data/output 2>/dev/null
 1409  git rm -r --cached .\ngit add .
 1410  git commit -m "chore: apply gitignore and remove generated files"
 1411  git push
 1412  git status
 1413  git status
 1414  git add .
 1415  git commit -m "update"
 1416  git push
 1417  git status
 1418  git commit -m "update-v"
 1419  git push
 1420  git status
 1421  git add .
 1422  git commit -m "update-v"
 1423  git push
(spark38) yonggan@Yonggans-MacBook-Pro Spark-202603 % ls
CDK-kejian                                              learning
README.md                                               spark_programming
SDE-Student                                             test.txt
course-master-big-data-with-pyspark-and-aws-main        算法
data
(spark38) yonggan@Yonggans-MacBook-Pro Spark-202603 % ls -lh
total 24
drwxr-xr-x@  6 yonggan  staff   192B Mar 31 04:02 CDK-kejian
-rw-r--r--@  1 yonggan  staff   4.4K Oct  6  2021 README.md
drwxr-xr-x@  3 yonggan  staff    96B Mar 30 07:10 SDE-Student
drwxrwxr-x@  5 yonggan  staff   160B Mar 29 12:07 course-master-big-data-with-pyspark-and-aws-main
drwxrwxr-x@  5 yonggan  staff   160B Mar 29 08:06 data
drwxr-xr-x@ 11 yonggan  staff   352B Mar 31 07:42 learning
drwx------@ 12 yonggan  staff   384B Mar 31 07:49 spark_programming
-rw-r--r--@  1 yonggan  staff   272B Mar 31 03:05 test.txt
drwxr-xr-x@  3 yonggan  staff    96B Mar 30 00:18 算法
(spark38) yonggan@Yonggans-MacBook-Pro Spark-202603 % ls learning/
00_example                      DE-AWS                          __init__.py
01_RDD                          Pdf                             pyspark-basics
02_SQL                          Practice-PySpark                spark-3.2.0-bin-hadoop3.2
(spark38) yonggan@Yonggans-MacBook-Pro Spark-202603 % export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export SPARK_LOCAL_IP=127.0.0.1
(spark38) yonggan@Yonggans-MacBook-Pro Spark-202603 % export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH=$JAVA_HOME/bin:$PATH
export SPARK_LOCAL_IP=127.0.0.1
(spark38) yonggan@Yonggans-MacBook-Pro Spark-202603 % source ~/.zshrc
(base) yonggan@Yonggans-MacBook-Pro Spark-202603 % java --version
openjdk 17.0.14 2025-01-21
OpenJDK Runtime Environment JBR-17.0.14+1-1367.22-nomod (build 17.0.14+1-b1367.22)
OpenJDK 64-Bit Server VM JBR-17.0.14+1-1367.22-nomod (build 17.0.14+1-b1367.22, mixed mode, sharing)
(base) yonggan@Yonggans-MacBook-Pro Spark-202603 % cd learning/
(base) yonggan@Yonggans-MacBook-Pro learning % ls         
00_example                      DE-AWS                          __init__.py
01_RDD                          Pdf                             pyspark-basics
02_SQL                          Practice-PySpark                spark-3.2.0-bin-hadoop3.2
(base) yonggan@Yonggans-MacBook-Pro learning % cd 01_RDD/
(base) yonggan@Yonggans-MacBook-Pro 01_RDD % spark 01_RDD_create_parallelize.py 
zsh: command not found: spark
(base) yonggan@Yonggans-MacBook-Pro 01_RDD % pyspark 01_RDD_create_parallelize.py 
Running python applications through 'pyspark' is not supported as of Spark 2.0.
Use ./bin/spark-submit <python file>
/Users/yonggan/opt/spark-3.2.0-bin-hadoop3.2/bin/spark-class: line 96: CMD: bad array subscript
head: illegal line count -- -1
(base) yonggan@Yonggans-MacBook-Pro 01_RDD %
```

你现在的问题已经很清楚了：

# 结论

你机器上 **没有 Java 11**，所以这句根本没有成功：

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
```

因为如果本机没有 11，`/usr/libexec/java_home -v 11` 不会给你一个有效路径。
后面你又 `source ~/.zshrc`，并且回到了 `(base)`，说明：

1. `.zshrc` 里又自动激活了 conda base
2. Java 还是 **17**
3. 你本地 Spark 还是 **3.2.0**
4. 所以 **Spark 3.2.0 + Java 17** 继续炸

---

# 你刚才输出里最关键的证据

## 1）Java 还是 17

你执行后看到：

```bash
java --version
openjdk 17.0.14
```

这就说明你根本没切到 Java 11。

---

## 2）你现在在用的还是 Spark 3.2.0

这里很明显：

```bash
/Users/yonggan/opt/spark-3.2.0-bin-hadoop3.2/bin/spark-class
```

说明系统里的 `pyspark` / `spark-submit` 还是指向 **旧 Spark 3.2.0**。

---

## 3）你用了错误运行方式

你执行了：

```bash
pyspark 01_RDD_create_parallelize.py
```

这个用法不对。
`pyspark` 是进交互式 shell 的，不是拿来直接跑 `.py` 文件的。

正确方式是：

```bash
spark-submit 01_RDD_create_parallelize.py
```

或者直接：

```bash
python 01_RDD_create_parallelize.py
```

前提是你的 PySpark 环境已经配好。

---

# 你现在最稳的解决路线

因为你说 **Java 不能改，只能是 17**，那就不要再折腾 Java 11 了。

## 正确路线：

**升级 PySpark / Spark 到 3.5.x**

---

# 你现在要做的事

## 第一步：确认当前 conda 环境

先别在 `(base)` 里搞，回到你的环境：

```bash
conda activate spark38
```

然后确认：

```bash
which python
python -V
```

你应该看到：

```bash
/Users/yonggan/anaconda3/envs/spark38/bin/python
Python 3.8.x
```

---

## 第二步：卸掉旧的 pyspark

在 `spark38` 里执行：

```bash
pip uninstall -y pyspark py4j spark
```

---

## 第三步：安装适配 Java 17 的版本

直接装：

```bash
pip install --upgrade pip setuptools wheel
pip install pyspark==3.5.2
```

---

## 第四步：验证 PySpark 版本

执行：

```bash
python -c "import pyspark; print(pyspark.__version__)"
```

你应该看到：

```bash
3.5.2
```

---

## 第五步：不要再用系统旧 Spark 3.2.0 命令

你现在机器里有这个旧目录：

```bash
/Users/yonggan/opt/spark-3.2.0-bin-hadoop3.2
```

这会干扰你。

先检查当前命令指向哪里：

```bash
which pyspark
which spark-submit
```

如果输出指向：

```bash
/Users/yonggan/opt/spark-3.2.0-bin-hadoop3.2/...
```

那说明你当前走的是 **系统旧 Spark**，不是 conda 里的新 PySpark。

---

# 最简单做法：直接用 Python 跑，不走外部 spark-submit

你这个脚本里已经是这种形式：

```python
from pyspark import SparkContext, SparkConf
sc = SparkContext(conf=conf)
```

那你直接用：

```bash
python 07_RDD_wordcount_example.py
```

就行。

这样优先使用的是 **当前 conda 环境里的 pyspark 包**，而不是外部 `/opt/spark-3.2.0...`。

---

# 如果还想用 spark-submit

那也要用 **当前环境里的**，不是系统旧的。

先查：

```bash
which spark-submit
```

如果不是 conda 环境里的，先别用它。

---

# 你现在 `.zshrc` 还有一个问题

你执行 `source ~/.zshrc` 后，提示符从：

```bash
(spark38)
```

变成了：

```bash
(base)
```

说明你的 `.zshrc` 里有自动激活 base。
这会把你刚才手动激活的 `spark38` 覆盖掉。

---

## 临时不要 `source ~/.zshrc`

现在先这样操作：

```bash
conda activate spark38
python -c "import sys; print(sys.executable)"
python -c "import pyspark; print(pyspark.__version__)"
java --version
```

重点看这三个：

1. Python 是否是 `spark38`
2. pyspark 是否已经是 `3.5.2`
3. Java 是否还是 `17`

只要结果是：

* Python = `spark38`
* pyspark = `3.5.2`
* Java = `17`

这套就是能跑的目标组合。

---

# 你刚才那个 `spark` 命令为什么报错

你执行了：

```bash
spark 01_RDD_create_parallelize.py
```

报：

```bash
zsh: command not found: spark
```

因为根本没有叫 `spark` 的标准命令。
常见的是：

* `pyspark`
* `spark-submit`
* `spark-shell`

没有直接 `spark`。

---

# 你刚才那个 `pyspark xxx.py` 为什么报错

你执行：

```bash
pyspark 01_RDD_create_parallelize.py
```

报：

```bash
Running python applications through 'pyspark' is not supported
Use ./bin/spark-submit <python file>
```

因为：

* `pyspark` = 交互式 shell
* 跑脚本要用 `spark-submit`
* 或者直接 `python your_script.py`

---

# 你现在最推荐的操作顺序

直接复制这一套：

```bash
conda activate spark38

pip uninstall -y pyspark py4j spark
pip install --upgrade pip setuptools wheel
pip install pyspark==3.5.2

python -c "import sys; print(sys.executable)"
python -c "import pyspark; print(pyspark.__version__)"
java --version

cd /Users/yonggan/Downloads/Spark-202603/learning/01_RDD
python 07_RDD_wordcount_example.py
```

---

# 如果你担心旧 Spark 3.2.0 干扰

再执行：

```bash
which python
which pyspark
which spark-submit
echo $PATH
```

如果 `pyspark` 和 `spark-submit` 还指向 `/Users/yonggan/opt/spark-3.2.0-bin-hadoop3.2`，那就说明 PATH 里旧 Spark 还在前面。

这时有两个选择：

## 方案 A：先不用 `pyspark/spark-submit`

直接用：

```bash
python 07_RDD_wordcount_example.py
```

最省事。

## 方案 B：把旧 Spark PATH 去掉

把 `.zshrc` 里类似这种删掉或注释掉：

```bash
export SPARK_HOME=/Users/yonggan/opt/spark-3.2.0-bin-hadoop3.2
export PATH=$SPARK_HOME/bin:$PATH
```

然后重新开 terminal。

---

# 一句话总结

你现在不是代码问题，而是：

**本机只有 Java 17，但你还在用旧 Spark 3.2.0；正确做法是保留 Java 17，升级到 PySpark 3.5.x，并且不要再调用系统里的旧 Spark 3.2.0 命令。**

把下面四个输出发我，我能直接告诉你下一步还差哪里：

```bash
which python
python -c "import pyspark; print(pyspark.__version__)"
which pyspark
which spark-submit
```


```
(base) yonggan@Yonggans-MacBook-Pro 01_RDD % python 01_RDD_create_parallelize.py
PYTHON: /Users/yonggan/anaconda3/bin/python
JAVA_HOME from env: /Users/yonggan/Library/Java/JavaVirtualMachines/corretto-1.8.0_442/Contents/Home
SPARK_HOME from env: /Users/yonggan/opt/spark-3.2.0-bin-hadoop3.2
PYSPARK_PYTHON from env: /Users/yonggan/anaconda3/envs/spark38/bin/python
java -version:
 openjdk version "1.8.0_442"
OpenJDK Runtime Environment Corretto-8.442.06.1 (build 1.8.0_442-b06)
OpenJDK 64-Bit Server VM Corretto-8.442.06.1 (build 25.442-b06, mixed mode)

Traceback (most recent call last):
  File "/Users/yonggan/Downloads/Spark-202603/learning/01_RDD/01_RDD_create_parallelize.py", line 23, in <module>
    from pyspark import SparkConf, SparkContext
ModuleNotFoundError: No module named 'pyspark'
(base) yonggan@Yonggans-MacBook-Pro 01_RDD %
```

现在问题已经很明确了，**好消息是核心 Spark/Java 兼容性这次不是主问题**。

# 你当前真实状态

你运行时打印出来的是：

```bash
PYTHON: /Users/yonggan/anaconda3/bin/python
```

这说明你现在用的是 **base 环境的 python**，不是 `spark38`。

但你环境变量里又有：

```bash
PYSPARK_PYTHON=/Users/yonggan/anaconda3/envs/spark38/bin/python
```

这就变成了：

* 主 Python：`base`
* PySpark Python：`spark38`

结果主解释器里根本没装 `pyspark`，所以报：

```bash
ModuleNotFoundError: No module named 'pyspark'
```

---

# 一句话结论

**你不是 Spark 起不来，而是你当前跑脚本时根本没进入 spark38 环境。**

---

# 现在怎么修

## 最直接做法

先切回 `spark38`：

```bash
conda activate spark38
```

然后确认：

```bash
which python
```

你应该看到：

```bash
/Users/yonggan/anaconda3/envs/spark38/bin/python
```

再检查：

```bash
python -c "import pyspark; print(pyspark.__version__)"
```

如果能输出版本号，说明环境对了。

然后再跑：

```bash
python 01_RDD_create_parallelize.py
```

---

# 如果 `conda activate spark38` 后还是回到 base

说明你的 shell 配置有问题。
先临时不用管 `conda activate`，直接强制用这个解释器跑：

```bash
/Users/yonggan/anaconda3/envs/spark38/bin/python 01_RDD_create_parallelize.py
```

这个最稳。

---

# 你现在的环境其实是这样

从你的输出看：

## 对的部分

* `JAVA_HOME` = Java 8
* `SPARK_HOME` = Spark 3.2.0

这套其实是兼容的。

## 错的部分

* 运行脚本的 Python 是 `base`
* 但 `pyspark` 安装在 `spark38` 里
* 所以导入失败

---

# 你现在先做这三步

## 1

```bash
conda activate spark38
```

## 2

```bash
which python
python -c "import pyspark; print(pyspark.__version__)"
```

## 3

```bash
python 01_RDD_create_parallelize.py
```

---

# 如果第二步还报 `No module named pyspark`

那就在 `spark38` 里装一下：

```bash
pip install pyspark==3.2.0
```

因为你当前：

* Java 8
* Spark 3.2.0
* SPARK_HOME 也是 3.2.0

那装 `pyspark 3.2.0` 最一致。

---

# 最稳的一套命令

你直接复制这个：

```bash
conda activate spark38
which python
python -c "import sys; print(sys.executable)"
python -c "import pyspark; print(pyspark.__version__)" || pip install pyspark==3.2.0
python 01_RDD_create_parallelize.py
```

---

# 最关键的理解

你刚才看到：

```bash
java -version: 1.8
```

这说明 Java 已经不是之前那个 17 问题了。
**现在唯一问题就是：你在 base 里跑，而不是在 spark38 里跑。**

把这两个输出发我，我就能直接告诉你下一步：

```bash
conda activate spark38
which python
python -c "import pyspark; print(pyspark.__version__)"
```


下面给你做成 **一眼秒懂版**。

---

# HDFS 读流程图（一眼秒懂版）

```text
        用户 / Spark / Hadoop Client
                  |
                  | 1. open("/data/a.txt")
                  v
             +-----------+
             | NameNode  |
             +-----------+
                  |
                  | 2. 返回 block 元数据
                  |    比如：
                  |    block1 -> DN1, DN3
                  |    block2 -> DN2, DN4
                  v
        客户端拿到每个 block 的位置列表
                  |
                  | 3. 按“就近原则”选 DataNode
                  v
      +-----------+        +-----------+        +-----------+
      | DataNode1 |        | DataNode2 |  ...   | DataNode3 |
      +-----------+        +-----------+        +-----------+
            |                    |                    |
            | 4. 直接读取 block    |                    |
            +--------------------> 客户端 <------------+
                                 |
                                 | 5. 客户端按顺序拼接 block
                                 v
                              最终文件内容
```

---

# HDFS 读流程，按步骤讲

## 1. 客户端先问 NameNode

用户要读文件：

```text
hdfs dfs -cat /data/a.txt
```

客户端不会直接找 DataNode，
而是先找 **NameNode** 问：

> 这个文件被切成了哪些 block？
> 每个 block 在哪些 DataNode 上？

---

## 2. NameNode 只返回“位置”，不传数据

NameNode 不负责真正传文件内容。
它只告诉客户端：

* block1 在 DN1、DN3
* block2 在 DN2、DN4

所以 NameNode 更像：

> **元数据管理员 / 路由表管理者**

---

## 3. 客户端自己选最近的 DataNode

客户端拿到 block 位置后，会按 **网络距离最近** 原则读。

优先级一般是：

1. 本机
2. 同机架
3. 跨机架

所以 HDFS 读性能高的一个原因就是：

> **数据尽量本地读 / 就近读**

---

## 4. 客户端直接从 DataNode 读 block

注意：

**后续数据流不经过 NameNode**

而是：

```text
Client <---- DataNode
```

这样避免 NameNode 成为大瓶颈。

---

## 5. 客户端把多个 block 拼起来

一个大文件会被切成很多 block。
客户端按 block 顺序读完，再拼接成完整文件内容。

---

# HDFS 读流程核心面试点

## 一句话记忆

**读数据时：先问 NameNode 要地址，再直接去 DataNode 拉数据。**

---

## NameNode 做什么？

* 管元数据
* 记录文件 → block → DataNode 的映射
* 不参与真正的数据传输

---

## DataNode 做什么？

* 真正存 block
* 把 block 内容返回给客户端

---

## 为什么这样设计？

因为这样：

* NameNode 压力小
* 数据读写更快
* 系统扩展性更好

---

---

# HDFS 写流程图（一眼秒懂版）

```text
         用户 / Spark / Hadoop Client
                   |
                   | 1. create("/data/a.txt")
                   v
              +-----------+
              | NameNode  |
              +-----------+
                   |
                   | 2. 检查权限 / 文件名 / 是否可创建
                   | 3. 选择每个 block 的副本放置位置
                   v
      例：block1 副本放到 DN1 -> DN2 -> DN3

客户端开始写数据
                   |
                   | 4. 数据切成 packet
                   v
             +-----------+
             | DataNode1 |
             +-----------+
                   |
                   | 5. pipeline 转发
                   v
             +-----------+
             | DataNode2 |
             +-----------+
                   |
                   | 6. 再转发
                   v
             +-----------+
             | DataNode3 |
             +-----------+

ACK 返回方向：
DataNode3 -> DataNode2 -> DataNode1 -> Client
```

---

# HDFS 写流程，按步骤讲

## 1. 客户端先请求创建文件

比如：

```text
hdfs dfs -put local.txt /data/a.txt
```

客户端先找 NameNode 说：

> 我要创建这个文件

---

## 2. NameNode 检查并分配副本位置

NameNode 会检查：

* 文件是否已存在
* 权限是否正确
* 父目录是否存在

然后它决定：

> 这个 block 的 3 个副本放在哪些 DataNode 上

比如：

```text
block1 -> DN1, DN2, DN3
```

---

## 3. 客户端不是同时写 3 份，而是写 pipeline

客户端先把数据发给第一个节点：

```text
Client -> DN1
```

然后：

```text
DN1 -> DN2
DN2 -> DN3
```

这叫 **pipeline 写入**

---

## 4. 数据不是整块发，而是切成 packet

block 很大，比如 128MB。
写的时候不是一下写完整个 block，
而是拆成很多小 packet 连续发送。

这样效率更高。

---

## 5. 每个 DataNode 落盘后返回 ACK

确认链路是反方向的：

```text
DN3 -> DN2 -> DN1 -> Client
```

客户端只有在整条链都确认成功后，
才认为这批数据写成功。

---

## 6. 一个 block 写满后，再向 NameNode 申请下一个 block

如果文件很大，block1 写满后：

客户端再次找 NameNode：

> 给我下一个 block 的存储位置

然后继续 block2、block3...

---

# HDFS 写流程核心面试点

## 一句话记忆

**写数据时：先问 NameNode 分配副本位置，再通过 DataNode pipeline 写入。**

---

## 为什么要 pipeline？

因为不用客户端同时发三份：

* 降低客户端压力
* 减少网络开销
* 提高吞吐量

---

## ACK 为什么反向返回？

因为要确认整条副本链都写成功了。

只有最后一个 DN 成功、一路返回 ACK，客户端才放心。

---

---

# HDFS 副本机制图（一眼秒懂版）

假设副本数 = 3

```text
一个文件 -> 被切成多个 block

file_A
  |
  +---- block1 --> DN1, DN2, DN5
  +---- block2 --> DN3, DN4, DN6
  +---- block3 --> DN2, DN5, DN7
```

---

# 更直观点：副本放置示意图

```text
                Rack1                          Rack2
        +-------------------+         +-------------------+
        | DN1   DN2   DN3   |         | DN4   DN5   DN6   |
        +-------------------+         +-------------------+

例如 block1 的三个副本：
    副本1 -> DN1   (本地 / 同机架优先)
    副本2 -> DN4   (跨机架，容灾)
    副本3 -> DN5   (同副本2所在机架中的另一台机器)
```

---

# 为什么副本要跨机架？

如果 3 份全放一个机架：

* 这个机架交换机挂了
* 整个 block 就都不可读了

所以 HDFS 常见策略是：

* 一份在本机架
* 两份在另一个机架

这样兼顾：

* 读性能
* 容灾
* 网络成本

---

# 副本机制核心作用

## 1. 容错

某个 DataNode 挂了，
还有其他副本可读。

---

## 2. 提高可用性

一个副本坏了，系统还能继续工作。

---

## 3. 提高读取性能

客户端可选最近的副本读取。

---

# 面试高频问法

## 问：HDFS 默认副本数是多少？

通常是：

```text
3
```

---

## 问：副本由谁决定？

**NameNode**

---

## 问：客户端写几次？

不是自己写 3 次，
而是 **写一次到 pipeline 头节点**，后面节点自动转发。

---

## 问：如果某个 DataNode 写失败怎么办？

pipeline 会重组，跳过坏节点，必要时 NameNode 会重新分配新的 DataNode。

---

# 一张对比表，直接秒答

| 项目              | 读流程               | 写流程                        |
| --------------- | ----------------- | -------------------------- |
| 先找谁             | NameNode          | NameNode                   |
| NameNode作用      | 返回 block 位置       | 分配 block 和副本位置             |
| 真正传数据的是谁        | DataNode → Client | Client → DataNode pipeline |
| 数据是否经过 NameNode | 不经过               | 不经过                        |
| 性能关键点           | 就近读               | pipeline 写                 |
| 容错方式            | 读其他副本             | 副本重建 / pipeline 重组         |

---

# 你背诵时就记这三句

## HDFS 读

**先问 NameNode 要 block 地址，再直接从 DataNode 就近读取。**

## HDFS 写

**先问 NameNode 分配副本位置，再通过 DataNode pipeline 写入。**

## HDFS 副本

**副本由 NameNode 管理，默认 3 份，既保证容错，也提升可用性和读取性能。**

---

如果你要，我下一条可以继续给你做：

**`HDFS 读写流程 + NameNode / DataNode 职责` 一页面试速记表**。


下面给你做成 **面试一页速记版（直接背🔥）**，重点是：
👉 字段含义 + 一句话解释 + 面试怎么说

---

# 🚀 YARN UI 一页速记（ResourceManager）

![Image](https://docs.arenadata.io/en/ADH/current/how-to/_images/yarn/resourcemanager-ui2_dark.png)

![Image](https://cdn.buttercms.com/4MiFgj5WQhGTqMTHTrlw)

![Image](https://www.adaltas.cloud/static/9165f2d69150edd9144891c361eed32e/a2b91/yarn-ui-applications-diagnostic.png)

![Image](https://community.cloudera.com/t5/image/serverpage/image-id/17743i110680105D9ADD2C/image-size/medium?px=400\&v=v2)

---

## 🧠 一句话总结（先背这个）

👉 **YARN 是资源调度中心，ResourceManager 负责分配 CPU / Memory 给应用（Spark / MapReduce）。**

---

# 🧾 Cluster Metrics（集群指标）

| 字段                   | 含义      | 面试一句话  |
| -------------------- | ------- | ------ |
| Apps Submitted       | 提交的任务总数 | 系统历史负载 |
| Apps Running         | 当前运行任务  | 当前压力   |
| Apps Pending         | 等待资源的任务 | 资源不够   |
| Apps Completed       | 已完成任务   | 系统吞吐   |
| Containers Allocated | 已分配容器数  | 当前资源使用 |
| Containers Pending   | 等待分配    | 资源紧张   |
| Memory Used          | 已用内存    | 资源利用率  |
| Memory Total         | 总内存     | 集群规模   |

---

# 🧾 Applications（任务列表）

| 字段             | 含义                      |
| -------------- | ----------------------- |
| Application ID | 每个任务唯一ID                |
| Name           | Spark / MapReduce job 名 |
| User           | 提交用户                    |
| Queue          | 队列（调度策略）                |
| State          | RUNNING / FINISHED      |
| Final Status   | SUCCEEDED / FAILED      |
| Tracking UI    | 跳到 Spark UI             |

👉 面试点：

👉 **YARN 只管资源，不管具体计算逻辑（Spark UI 看细节）**

---

# 🧾 Nodes（节点信息）

| 字段              | 含义           |
| --------------- | ------------ |
| Active Nodes    | 正常节点         |
| Lost Nodes      | 掉线节点         |
| Unhealthy Nodes | 异常节点         |
| NodeManager     | 每台机器上的 agent |
| Memory / CPU    | 节点资源         |

👉 面试一句话：

👉 **NodeManager = 每台机器的资源执行者**

---

# 🧾 Schedulers（调度器）

常见：

* FIFO（先进先出）
* Capacity（容量调度）
* Fair（公平调度）

👉 面试高频：

👉 **生产一般用 Capacity / Fair，避免一个任务独占资源**

---

# 🧠 YARN 架构一句话（超高频🔥）

👉 **ResourceManager 分配资源，NodeManager 执行任务，ApplicationMaster 负责单个任务调度。**

---

---

# ⚡ Spark UI 一页速记（Jobs / Stages / DAG）

![Image](https://www.filepicker.io/api/file/aazCeBgkQzuEv0TEPBQs)

![Image](https://downloads.apache.org/spark/docs/3.0.0/img/AllStagesPageDetail6.png)

![Image](https://miro.medium.com/v2/resize%3Afit%3A1400/1%2A2_m_Cxps2UzA7R87zfvciw.png)

![Image](https://untitled-life.github.io/images/post/visual_dag_resolved.png)

---

## 🧠 一句话总结（先背这个）

👉 **Spark UI 是执行细节，YARN UI 是资源分配。**

---

# 🧾 Jobs（任务层）

| 字段          | 含义                  |
| ----------- | ------------------- |
| Job ID      | 一个 action 触发一个 job  |
| Description | 任务描述                |
| Status      | Running / Succeeded |
| Stages      | 包含多个 stage          |
| Duration    | 执行时间                |

👉 面试点：

👉 **一个 action（collect / count） = 一个 job**

---

# 🧾 Stages（阶段层）

| 字段             | 含义    |
| -------------- | ----- |
| Stage ID       | 阶段编号  |
| Tasks          | 并行任务数 |
| Input / Output | 数据量   |
| Shuffle Read   | 跨节点读  |
| Shuffle Write  | 跨节点写  |

---

## 🧠 核心理解（超重要🔥）

👉 Stage 的划分 = **是否发生 Shuffle**

---

## 🔥 两种依赖

### Narrow Dependency（窄依赖）

```text
map / filter
```

👉 不跨节点 → 同一个 stage

---

### Wide Dependency（宽依赖）

```text
reduceByKey / groupByKey
```

👉 需要 shuffle → 新 stage

---

# 🧾 DAG（核心）

```text
RDD1 --map--> RDD2 --reduceByKey--> RDD3
                 (shuffle)
```

👉 DAG = 计算逻辑图（不是执行）

---

## 面试一句话

👉 **DAG 描述计算逻辑，Stage 是执行边界，Task 是并行单元。**

---

# 🧾 Tasks（任务层）

| 字段             | 含义     |
| -------------- | ------ |
| Task           | 最小执行单位 |
| Executor       | 执行机器   |
| Duration       | 执行时间   |
| Locality Level | 数据是否本地 |

👉 面试点：

👉 **一个 partition = 一个 task**

---

# 🧾 Executors（执行器）

| 字段             | 含义        |
| -------------- | --------- |
| Executor ID    | worker 进程 |
| Storage Memory | 缓存        |
| Task Time      | 执行时间      |
| Failed Tasks   | 失败数       |

👉 面试一句话：

👉 **Executor 是真正执行 Spark 代码的进程**

---

---

# 🧠 Spark 执行流程（必须会🔥）

```text
代码 → DAG → Stage → Task → Executor
```

---

# 🧠 YARN vs Spark UI（面试必问）

| 对比  | YARN UI      | Spark UI    |
| --- | ------------ | ----------- |
| 作用  | 资源管理         | 计算执行        |
| 看什么 | CPU / Memory | DAG / Stage |
| 关注点 | 集群负载         | 性能瓶颈        |
| 用户  | 运维 / 平台      | 开发          |

---

# 🧠 高频面试题总结

## Q1：为什么会有 Stage？

👉 因为 **shuffle 会切断 pipeline**

---

## Q2：为什么 shuffle 慢？

👉 跨节点：

* 磁盘 IO
* 网络 IO

---

## Q3：Task 数量由什么决定？

👉 **partition 数**

---

## Q4：Spark 为什么快？

👉

* 内存计算
* DAG 优化
* 减少 IO

---

# 🧠 最后给你 5 句“面试秒杀话术”

1️⃣
👉 **YARN 负责资源调度，Spark 负责计算执行。**

2️⃣
👉 **一个 action 触发一个 job。**

3️⃣
👉 **Stage 的边界由 shuffle 决定。**

4️⃣
👉 **一个 partition 对应一个 task。**

5️⃣
👉 **Executor 是真正执行任务的进程。**

---

如果你要，我可以继续帮你做：

👉 **Spark + HDFS + YARN 全链路一张图（面试王炸🔥）**
