很好，你已经**100%成功完成第一步：3节点Docker集群已经跑起来了 ✅**

下面我帮你**系统整理 + 下一步完整操作（不省略）**，你直接照做即可👇

---

# ✅ 当前状态总结（你已经完成）

📄 来自你的日志：

### 已完成：

* Docker 安装 ✔️
* Docker Compose ✔️
* 创建目录：

  ```
  ~/docker-spark-3nodes
  ```
* 写好：

  * `Dockerfile` ✔️
  * `docker-compose.yml` ✔️
* 成功执行：

  ```
  docker compose up -d --build
  ```
* 结果：

  ```
  node1 / node2 / node3 已全部启动 ✔️
  ```

👉 **结论：你已经有“3台虚拟机”了（用Docker模拟）**

---

# ⚠️ 下一步核心目标（非常重要）

👉 现在只是“3台空机器”

你接下来要做的是：

### 🔥 目标：

1. 配置 SSH 免密
2. 三节点互通
3. 安装 Spark
4. 搭建 Standalone 集群

---

# 🚀 Step 1：进入 node1（主节点）

```bash
docker exec -it node1 bash
```

---

# 🚀 Step 2：生成 SSH key（node1执行）

```bash
ssh-keygen -t rsa
```

👉 一直回车（不要密码）

---

# 🚀 Step 3：复制公钥到所有节点

```bash
ssh-copy-id root@node1
ssh-copy-id root@node2
ssh-copy-id root@node3
```

👉 密码都是：

```
123456
```

---

# 🚀 Step 4：测试免密登录

```bash
ssh node2
ssh node3
```

👉 如果不需要密码 = 成功 ✅

---

# 🚀 Step 5：配置 hosts（3个节点都要做）

进入每个节点：

```bash
docker exec -it node1 bash
docker exec -it node2 bash
docker exec -it node3 bash
```

编辑：

```bash
nano /etc/hosts
```

添加👇：

```
172.28.0.11 node1
172.28.0.12 node2
172.28.0.13 node3
```

---

# 🚀 Step 6：安装 Spark（在 node1）

```bash
cd /opt
wget https://dlcdn.apache.org/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz
tar -zxvf spark-3.2.0-bin-hadoop3.2.tgz
mv spark-3.2.0-bin-hadoop3.2 spark
```

---

# 🚀 Step 7：配置环境变量

```bash
nano /etc/profile
```

追加：

```bash
export SPARK_HOME=/opt/spark
export PATH=$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH
```

生效：

```bash
source /etc/profile
```

---

# 🚀 Step 8：配置 Spark

```bash
cd /opt/spark/conf
cp spark-env.sh.template spark-env.sh
cp workers.template workers
```

---

## 编辑 spark-env.sh

```bash
nano spark-env.sh
```

添加：

```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export SPARK_MASTER_HOST=node1
export SPARK_WORKER_MEMORY=1g
```

---

## 编辑 workers

```bash
nano workers
```

写入：

```
node1
node2
node3
```

---

# 🚀 Step 9：分发 Spark 到 node2 / node3

```bash
scp -r /opt/spark root@node2:/opt/
scp -r /opt/spark root@node3:/opt/
```

---

# 🚀 Step 10：启动集群（node1）

```bash
cd /opt/spark
sbin/start-all.sh
```

---

# 🚀 Step 11：验证

在 node1 执行：

```bash
jps
```

应该看到：

```
Master
Worker
```

---

# 🌐 打开 Web UI（关键）

浏览器打开：

```
http://localhost:8080
```

👉 如果打不开，执行：

```bash
docker ps
```

然后把 8080 映射出来（我可以帮你改 compose）

---

# 🎯 一句话总结你现在的位置

👉 你现在已经完成：

> “用 Docker 在 Mac 上模拟 3 台 Linux 服务器”

👉 下一步：

> “把这 3 台机器变成 Spark 集群”

---

# 🚨 常见坑（你很可能会遇到）

### ❌ ssh-copy-id 不存在

解决：

```bash
apt install openssh-client -y
```

---

### ❌ scp 失败

👉 一般是 SSH 没配置好

---

### ❌ 8080打不开

👉 需要 port 映射（我可以帮你改 compose）

---

# 🚀 如果你想更快（推荐）

我可以直接帮你：

✅ 给你一份：

* 完整 docker-compose（带 Spark 已装好）
* 一键启动集群版本

👉 你只需要：

```
docker compose up
```

---

# 👉 下一步你做什么？

你现在只需要回我一句：

👉 **“继续”**

我会带你：

✔️ 修复端口
✔️ 打开Spark UI
✔️ 跑第一个分布式任务
✔️ + 面试讲解（Spark架构一套）



对，**现在 3 个容器都起来了，但没有映射任何端口到你 Mac 本机**。

所以结论很简单：

## 你现在的状态

* `node1` / `node2` / `node3` 都在运行 ✅
* 但 `PORTS` 这一列是空的
* 所以你现在**不能直接在宿主机浏览器打开 Spark UI**
* 也不能直接 `ssh localhost -p xxx` 这种方式访问它们

---

# 为什么？

因为你现在的 `docker-compose.yml` 里没有写 `ports:`。

你现在只是：

* 容器之间内部互通
* 宿主机没有暴露端口

---

# 这意味着什么？

### 现在可以做的

你仍然可以继续：

```bash
docker exec -it node1 bash
```

然后在容器内部完成：

* SSH 免密
* 安装 Spark
* 配置集群
* 启动 `start-all.sh`

这些都**不受影响**。

### 现在不方便的

你暂时不能直接在 Mac 浏览器访问：

* Spark Master UI `8080`
* Spark Worker UI `8081`
* Jupyter / 其他服务端口

---

# 你现在最该做的事

先继续进 `node1` 配 SSH 和 Spark，等 Spark 真启动后，再决定要不要映射端口。

---

# 如果你想现在就映射端口

你把 `docker-compose.yml` 改成下面这样。

## 改好的 `docker-compose.yml`

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
      - "8081:8081"
      - "4040:4040"
      - "2221:22"
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
      - "2222:22"
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
      - "2223:22"
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

# 改完后执行

```bash
docker compose down
docker compose up -d --build
docker ps
```

然后你会看到类似：

```bash
0.0.0.0:8080->8080/tcp
0.0.0.0:8081->8081/tcp
0.0.0.0:4040->4040/tcp
0.0.0.0:2221->22/tcp
```

---

# 之后你就可以

在浏览器打开：

```text
http://localhost:8080
```

如果 Spark Master 启动成功，就能看到 UI。

---

# 我建议你现在这样走

## 方案A：先不改端口，继续配集群

先执行：

```bash
docker exec -it node1 bash
```

然后做：

* ssh-keygen
* ssh-copy-id
* 装 Spark
* 配 workers
* start-all.sh

## 方案B：先改端口，再继续

优点：

* 后面能直接看 UI
* 更直观

---

# 你这个 `docker ps` 输出最关键的信息

就是这一点：

> **容器运行正常，但没有端口映射**

所以不是坏了，只是**还没暴露给宿主机**。

你下一步直接先执行这个就行：

```bash
docker exec -it node1 bash
```

如果你愿意，我下一条可以直接给你一套 **从 node1 开始到 Spark 集群启动成功的完整命令清单**。


对，结果还是一样，说明判断没错：

## 现在确认的事实

你的 3 个 Spark 节点容器：

* `node1`
* `node2`
* `node3`

都已经成功运行了，**没有挂掉**。
但它们的 `PORTS` 还是空的，说明：

### 当前 compose 配置没有做端口映射

所以现在：

* 宿主机 Mac **看不到容器里的 22 / 8080 / 8081**
* 浏览器打不开 Spark UI
* 但 **容器内部网络是可用的**

---

# 你现在可以继续，不用卡在这里

这一步不是报错，只是“还没开放端口”。

直接进入 `node1` 继续配置就行：

```bash
docker exec -it node1 bash
```

---

# 你现在最推荐走法

我建议你先**不改 compose**，先把集群配起来。
因为现在最重要的是确认这 3 个节点内部能不能：

* ssh 互通
* 安装 Spark
* 启动 Master / Worker

等 Spark 真跑起来后，再映射 UI 端口。

---

# 下一步完整命令

下面你直接照着做。

## 1）进入 node1

```bash
docker exec -it node1 bash
```

---

## 2）先看 3 个节点能不能互 ping

在 `node1` 里执行：

```bash
ping -c 2 node2
ping -c 2 node3
```

如果通，说明容器网络正常。

---

## 3）生成 SSH key

在 `node1` 里执行：

```bash
ssh-keygen -t rsa
```

一直回车。

---

## 4）把公钥复制到自己和另外两个节点

```bash
ssh-copy-id root@node1
ssh-copy-id root@node2
ssh-copy-id root@node3
```

密码都是：

```bash
123456
```

---

## 5）测试免密登录

```bash
ssh node1
ssh node2
ssh node3
```

如果不再要密码，就成功了。

---

## 6）安装 Spark

还在 `node1`：

```bash
cd /opt
wget https://dlcdn.apache.org/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz
tar -zxvf spark-3.2.0-bin-hadoop3.2.tgz
mv spark-3.2.0-bin-hadoop3.2 spark
```

---

## 7）配置 Spark

```bash
cd /opt/spark/conf
cp spark-env.sh.template spark-env.sh
cp workers.template workers
```

编辑 `spark-env.sh`：

```bash
nano /opt/spark/conf/spark-env.sh
```

加上：

```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export SPARK_MASTER_HOST=node1
export SPARK_WORKER_MEMORY=1g
```

编辑 `workers`：

```bash
nano /opt/spark/conf/workers
```

改成：

```bash
node1
node2
node3
```

---

## 8）分发 Spark 到 node2 / node3

```bash
scp -r /opt/spark root@node2:/opt/
scp -r /opt/spark root@node3:/opt/
```

---

## 9）启动 Spark 集群

在 `node1`：

```bash
cd /opt/spark
sbin/start-all.sh
```

---

## 10）验证

```bash
jps
```

`node1` 上应该看到：

```bash
Master
Worker
```

再分别检查：

```bash
ssh node2 jps
ssh node3 jps
```

应该看到：

```bash
Worker
```

---

# 到这里你已经完成了什么

你就真的完成了：

### “在 Mac 上用 Docker 模拟 3 台机器，并跑起 Spark Standalone 集群”

这已经够课程练习和理解架构了。

---

# 什么时候再改端口

等你确认 `start-all.sh` 成功后，再改 `docker-compose.yml` 加：

```yaml
ports:
  - "8080:8080"
  - "8081:8081"
```

这样才有意义，因为那时 Spark UI 才真的存在。

---

# 你这个阶段最关键的一句

**现在不是失败，也不是卡住，只是还没做端口暴露。**

你先执行这句：

```bash
docker exec -it node1 bash
```

然后把里面的输出贴给我。


正常，你已经**进入容器里面了**。

问题是：

## 为什么报错？

你现在提示符是：

```bash
root@node1:/#
```

这表示你已经在 **node1 容器内部** 了。

所以你再输入：

```bash
docker exec -it node2 bash
```

会报：

```bash
bash: docker: command not found
```

因为 **容器里面没有 Docker 命令**，Docker 只能在你 Mac 宿主机终端里执行。

---

# 你现在怎么退出容器

你刚才写的：

```bash
exit()
quit()
q
```

都不是 bash 命令。

正确退出是：

```bash
exit
```

或者直接按：

```bash
Ctrl + D
```

---

# 现在你要做的，不是退出也不是再进 node2

你现在已经在 `node1` 里了，正好继续下面步骤。

---

# 现在就在 `node1` 里执行这些命令

## 1）测试网络

```bash
ping -c 2 node2
ping -c 2 node3
```

---

## 2）生成 ssh key

```bash
ssh-keygen -t rsa
```

一路回车。

---

## 3）复制公钥

```bash
ssh-copy-id root@node1
ssh-copy-id root@node2
ssh-copy-id root@node3
```

密码都是：

```bash
123456
```

---

## 4）测试免密

```bash
ssh node2
```

如果跳进去了，再执行：

```bash
exit
```

回到 `node1`。

然后：

```bash
ssh node3
```

---

# 你现在最重要的认知

## 宿主机命令 vs 容器内命令

### 在 Mac 终端里才能运行：

```bash
docker ps
docker exec -it node1 bash
docker exec -it node2 bash
docker exec -it node3 bash
```

### 在容器里运行：

```bash
ping
ssh
ssh-copy-id
apt
wget
tar
jps
```

---

# 你现在不要乱了

你此刻已经在最该在的位置：

```bash
root@node1:/#
```

所以现在**继续在这里执行**：

```bash
ping -c 2 node2
ping -c 2 node3
```

把输出贴给我。


这张图其实在教你 **Linux / Mac 终端最基础的目录切换命令（cd）**，核心就3点👇

---

# 🧠 这张图在教什么（重点）

## 1️⃣ `cd ~/Documents`

👉 含义：进入 Documents 文件夹

* `~` = 当前用户的 home 目录
* 所以：

  ```bash
  cd ~/Documents
  ```

  = 进入：

  ```
  /Users/你的用户名/Documents
  ```

---

## 2️⃣ `ls`

👉 查看当前目录内容

图里执行了：

```bash
ls
```

显示：

* zip 文件
* png
* docx
* test 文件夹

👉 就是“列出文件列表”

---

## 3️⃣ `cd ..`

👉 回到上一级目录

```bash
cd ..
```

比如：

```
/Users/xxx/Documents
⬆ 回到
/Users/xxx
```

---

## 4️⃣ `cd -`

👉 返回刚刚的目录（来回跳）

```bash
cd -
```

这个很重要 👇

例子：

```bash
cd ~/Documents
cd ..
cd -
```

👉 会回到：

```
~/Documents
```

---

# 🎯 一句话总结

这张图就是在教你：

> **如何在终端里进入目录、返回上一级、以及快速来回切换目录**

---

# 🔥 和你现在 Docker 有啥关系？

你刚刚在用：

```bash
docker exec -it node1 bash
```

进入容器后，其实就是在 Linux 终端里操作。

所以这些命令你马上就会用到：

```bash
cd /opt
cd /opt/spark
cd ..
cd -
ls
```

---

# 🚀 给你一个超实用速记（直接背）

```bash
cd ~        # 回家目录
cd ..       # 上一级
cd -        # 回到刚刚的位置
ls          # 看文件
pwd         # 看当前路径
```

---

# 👍 你现在该做啥

你现在已经在：

```bash
root@node1:/#
```

直接执行：

```bash
pwd
ls
```

然后继续：

```bash
ping -c 2 node2
```

我帮你下一步一步带你把 Spark 集群跑起来。


这张图在教你一个非常基础但**你马上就会用到的命令：`mkdir`（创建目录）**

---

# 🧠 核心知识（这张图想表达的）

## 1️⃣ `mkdir foo`

```bash
mkdir foo
```

👉 含义：

> 创建一个叫 `foo` 的文件夹

执行后：

```bash
ls
```

会看到：

```bash
foo
```

---

## 2️⃣ 一次创建多个目录（重点）

```bash
mkdir dir1 dir2 dir3 dir_4
```

👉 含义：

> 一次创建多个文件夹

执行后：

```bash
ls -l
```

会看到：

```bash
dir1
dir2
dir3
dir_4
```

---

## 3️⃣ `ls -l`（长格式）

```bash
ls -l
```

👉 显示详细信息：

例如：

```bash
drwxr-xr-x 2 user user 4096 Aug 7 dir1
```

含义：

* `d` → 是目录（folder）
* `rwx` → 权限
* 时间 / 大小 / 用户

---

# 🎯 一句话总结

这张图在教：

> **如何用 `mkdir` 创建一个或多个文件夹 + 用 `ls` 查看**

---

# 🔥 和你现在 Spark 有什么关系（重点）

你接下来马上会用到类似操作👇

在容器里：

```bash
cd /opt
mkdir spark
```

或者：

```bash
mkdir -p /export/server
```

👉（课程很多会用 `/export/server` 这种目录）

---

# 🚀 给你一个实战组合（你马上会用）

在 node1 里可以试一下：

```bash
mkdir test1 test2
ls
```

---

# 💡 高频命令速记（直接背）

```bash
mkdir dir        # 创建一个目录
mkdir a b c      # 一次创建多个
mkdir -p a/b/c   # 递归创建（最常用🔥）
ls               # 查看文件
ls -l            # 详细查看
```

---

# 👍 你现在下一步

你现在在：

```bash
root@node1:/#
```

可以先随便练一下：

```bash
mkdir test
ls
```

然后继续：

```bash
ping -c 2 node2
```

我帮你把 Spark 集群一步一步带起来。


很好，这三个是 **Linux 文本处理三剑客（必须会）**，但注意👇
👉 **它们不是“谁的名字缩写”，而是工具名 + 含义来源不同**

我帮你用**最简单记忆方式**讲清楚👇

---

# 🧠 一句话记忆（你直接背）

```
grep = 找
awk  = 取
sed  = 改
```

---

# 📌 1️⃣ grep（找）

## 来源

👉 来自早期 Unix 编辑器命令：

```
g/re/p
```

含义：

* g → global（全局）
* re → regular expression（正则）
* p → print（打印）

👉 所以 grep =
**“全局匹配正则并打印”**

---

## 作用

👉 找关键词

```bash
grep "error" log.txt
```

---

# 📌 2️⃣ awk（取）

## 来源

👉 三个作者名字首字母：

```
Aho + Weinberger + Kernighan
```

👉 awk = 人名缩写（唯一一个是人名）

---

## 作用

👉 按列处理数据（最强）

```bash
awk '{print $1}' file.txt
```

👉 打印第一列

---

# 📌 3️⃣ sed（改）

## 来源

👉 **Stream Editor（流编辑器）**

👉 sed =
**Stream EDitor**

---

## 作用

👉 批量替换 / 修改文本

```bash
sed 's/old/new/g' file.txt
```

👉 把 old 全部换成 new

---

# 🎯 总结（面试版一句话）

| 工具   | 来源            | 核心能力 |
| ---- | ------------- | ---- |
| grep | g/re/p        | 查找文本 |
| awk  | 三位作者名字        | 按列处理 |
| sed  | Stream Editor | 文本替换 |

---

# 🔥 面试/实战黄金组合（你以后会用）

```bash
cat log.txt | grep ERROR | awk '{print $2}' | sed 's/:/ /g'
```

👉 流程：

* grep → 找错误行
* awk → 取第2列
* sed → 替换格式

---

# 👍 你只要记住这个就够了

👉 **grep找，awk取，sed改**

---

如果你要，我可以给你一页：

👉「grep + awk + sed 高频面试题 + 10个实战例子（直接背）」


这张图在教你一个新命令：👉 **`tail`（看文件“尾部”）**

---

# 🧠 核心一句话

```bash
tail = 看文件最后几行
```

---

# 📌 图里在做什么？

命令是：

```bash
tail -v asian_countries.txt
```

---

## 🔍 分解理解

### 1️⃣ `tail`

👉 查看文件**最后内容**

默认：

```bash
tail file.txt
```

👉 显示最后 **10行**

---

### 2️⃣ `-v`

👉 显示文件名（verbose）

所以输出变成：

```text
==> asian_countries.txt <==
```

👉 这个就是图中红圈部分

---

# 📌 输出内容解释

```text
==> asian_countries.txt <==
Armenia
Saudi Arabia
Syria
...
```

👉 含义：

* 上面一行 → 文件名
* 下面 → 文件最后几行内容

---

# 🎯 一句话总结

这张图在教：

> **用 `tail` 查看文件结尾，用 `-v` 显示文件名**

---

# 🔥 常用 tail 命令（你必须会）

## 1️⃣ 看最后 10 行（默认）

```bash
tail file.txt
```

---

## 2️⃣ 指定行数

```bash
tail -n 5 file.txt
```

👉 最后 5 行

---

## 3️⃣ 实时查看日志（🔥最重要）

```bash
tail -f log.txt
```

👉 实时滚动（类似监控）

---

## 4️⃣ 多文件 + 显示文件名

```bash
tail -v file1 file2
```

---

# 🚀 和你 Spark / 后端的关系（重点）

你以后会大量用：

```bash
tail -f logs/spark.log
```

👉 用来看：

* Spark 执行情况
* 报错
* Worker / Executor 日志

---

# 💡 高频组合（面试 + 实战）

```bash
tail -f app.log | grep ERROR
```

👉 实时看错误日志

---

# 👍 最重要一句

👉 **tail = 看结尾 + 看日志（实时）**

---

# 👉 你现在可以练一下

在 node1 里：

```bash
echo "hello" > test.txt
echo "world" >> test.txt
tail test.txt
```

---

如果你要，我可以给你一页：

👉「Linux 文件查看命令大全（cat / less / head / tail 对比）」


很好，这个词你以后会经常看到，必须理解👇

---

# 🧠 一句话理解

```text
verbose = 输出更多详细信息
```

👉 中文：**详细模式 / 啰嗦模式**

---

# 📌 在你这张图里的意思

```bash
tail -v asian_countries.txt
```

👉 `-v`（verbose）作用：

```text
==> asian_countries.txt <==
```

👉 多打印一行：**文件名**

---

# 🔥 对比一下（秒懂）

## ❌ 不加 -v

```bash
tail asian_countries.txt
```

输出：

```text
Armenia
Saudi Arabia
...
```

👉 你不知道这是哪个文件

---

## ✅ 加 -v

```bash
tail -v asian_countries.txt
```

输出：

```text
==> asian_countries.txt <==
Armenia
Saudi Arabia
...
```

👉 更清晰

---

# 📌 为什么叫 verbose？

👉 来自英语：

* verbose = **话多的 / 详细的**

👉 在程序里意思就是：

> “多说点信息给你看”

---

# 🚀 你以后会看到的常见写法

## 1️⃣ 单个 -v

```bash
cp -v file1 file2
```

👉 会告诉你：

```text
file1 -> file2
```

---

## 2️⃣ 双 -vv（更详细）

```bash
ssh -vv user@host
```

👉 debug 用

---

## 3️⃣ 三个 -vvv（极详细）

👉 网络 / SSH 排查常用

---

# 🎯 一句话总结（直接背）

```text
-v = 显示更多信息
-vv = 更详细
-vvv = debug级别
```

---

# 👍 结合你现在学的命令

```bash
grep -v error   # 这里不是 verbose！是“排除”
```

⚠️ 注意：

* 在 grep 里：

  ```bash
  -v = 取反（不包含）
  ```
* 在 tail / cp / ssh 里：

  ```bash
  -v = verbose（详细）
  ```

👉 **同一个 -v，不同命令含义可能不同（很重要🔥）**

---

# 🚀 你现在记住这句话就够了

👉 **verbose = 多输出信息，方便你看发生了什么**

---

如果你要，我可以帮你整理一页：

👉「Linux 命令参数 -v / -f / -n / -r 高频面试总结（直接背）」


很好，这个我给你整理成**面试可背 + 实战可用的一页速记表**👇

---

# 🚀 Linux 高频参数总结（直接背）

## 🧠 一句话核心

```text
-v 看过程
-f 跟踪/强制
-n 数量
-r 递归/反向
```

---

# 📌 1️⃣ -v（verbose：详细输出）

👉 含义：**显示过程 / 多输出信息**

### 常见用法

```bash
cp -v a.txt b.txt      # 显示复制过程
rm -v file.txt         # 显示删除
tail -v file.txt       # 显示文件名
```

### 面试点

👉 用于**debug / 观察执行过程**

---

# 📌 2️⃣ -f（follow / force）

👉 两种常见含义（重点⚠️）

---

## 🔥 含义1：跟踪（follow）

```bash
tail -f log.txt
```

👉 实时看日志（最常考🔥）

---

## 🔥 含义2：强制（force）

```bash
rm -f file.txt
```

👉 不提示直接删除

---

### 面试一句话

```text
-f = 跟踪日志 或 强制执行
```

---

# 📌 3️⃣ -n（number：数量）

👉 含义：**指定数量**

### 常见用法

```bash
head -n 5 file.txt   # 前5行
tail -n 10 file.txt  # 后10行
```

---

### 面试点

👉 控制输出规模（日志分析常用）

---

# 📌 4️⃣ -r（recursive / reverse）

👉 两种含义（⚠️常考）

---

## 🔥 含义1：递归（recursive）

```bash
cp -r dir1 dir2
rm -r folder
```

👉 操作整个目录

---

## 🔥 含义2：反向（reverse）

```bash
sort -r file.txt
```

👉 倒序排序

---

### 面试一句话

```text
-r = 递归（文件夹） 或 反向（排序）
```

---

# 🎯 高频组合（必须会🔥）

## 1️⃣ 删除目录（危险）

```bash
rm -rf folder
```

👉 面试解释：

* r = 递归
* f = 强制

---

## 2️⃣ 实时看错误日志

```bash
tail -f app.log | grep ERROR
```

---

## 3️⃣ 查看前/后几行

```bash
head -n 5 file.txt
tail -n 5 file.txt
```

---

## 4️⃣ 复制整个目录

```bash
cp -r src/ dest/
```

---

# 💡 面试高频陷阱（你必须知道）

## ⚠️ 同一个参数，不同命令含义不同

### 举例：

```bash
grep -v error
```

👉 这里：

```text
-v = 取反（不包含）
```

❌ 不是 verbose！

---

# 🧠 最终速记版（超短）

```text
-v → 详细输出
-f → 跟踪/强制
-n → 数量
-r → 递归/反向
```

---

# 👍 面试一句话回答模板

> “-v is for verbose output, -f is used for follow or force, -n controls number of lines, and -r is for recursive operations or reverse sorting depending on the command.”

---

如果你要下一步，我可以给你：

👉「Linux 20个高频命令 + 参数 + 面试问法（grep/awk/sed/ps/top 全覆盖）」


很好，这张图是 **`top` 命令（系统监控）**，这个在面试和排查问题里非常重要🔥

我帮你用**最简单+面试级理解**拆开👇

---

# 🧠 一句话总结

```text
top = 实时查看系统资源（CPU / 内存 / 进程）
```

---

# 📊 上半部分（系统整体状态）

## 1️⃣ 进程信息

```text
Processes: 621 total, 2 running, 619 sleeping
```

👉 含义：

* total → 总进程数
* running → 正在运行
* sleeping → 休眠（大部分进程都是这个）

---

## 2️⃣ Load Average（🔥面试重点）

```text
Load Avg: 3.82, 4.15, 4.01
```

👉 含义：

* 最近 1 / 5 / 15 分钟的负载

### 💡 怎么判断？

👉 和 CPU 核心数对比！

* 4核CPU：

  * load ≈ 4 → 正常
  * load > 4 → 有压力
  * load >> 4 → 过载

---

## 3️⃣ CPU 使用率

```text
CPU usage: 7.75% user, 10.27% sys, 81.97% idle
```

👉 含义：

* user → 用户程序
* sys → 系统
* idle → 空闲

👉 你这个：

> CPU 很闲（80% 空闲）✅

---

## 4️⃣ 内存（🔥重点）

```text
PhysMem: 16G used, 481M unused
```

👉 表面看很满，但：

👉 macOS 会缓存内存（正常）

---

# 📋 下半部分（进程列表）

表头：

```text
PID  COMMAND   %CPU   MEM
```

---

## 重点字段

### 🔥 PID

👉 进程ID

---

### 🔥 COMMAND

👉 程序名

比如：

* `Google Chrome`
* `WindowServer`
* `kernel_task`

---

### 🔥 %CPU

👉 CPU占用

```text
top → 22%
```

👉 当前最耗CPU

---

### 🔥 MEM

👉 内存占用

```text
WindowServer → 1468M
```

👉 UI系统占用很多

---

# 🎯 面试标准回答（直接背）

> “top is used to monitor system performance in real time, including CPU usage, memory consumption, load average, and active processes.”

---

# 🔥 实战你要会这几个操作

## 1️⃣ 按 CPU 排序

```text
按 P
```

---

## 2️⃣ 按内存排序

```text
按 M
```

---

## 3️⃣ 退出

```text
q
```

---

## 4️⃣ 杀进程（结合）

```bash
kill -9 PID
```

---

# 🚨 你这个截图说明什么？

👉 你的电脑其实：

* CPU 很空闲 ✅
* 内存使用正常（mac机制）✅
* 没有异常进程 ❌

👉 所以“卡”大概率是：

* Chrome
* Docker
* IDE

---

# 💡 和你现在 Docker + Spark 的关系

你之后会用：

```bash
top
```

看：

* Spark Executor 是否吃CPU
* Docker 是否占资源
* 是否卡死

---

# 👍 最重要记住这3点

```text
Load Avg = 系统压力
%CPU     = 谁在占用
MEM      = 谁在吃内存
```

---

如果你要，我可以给你一页：

👉「top / htop / ps / kill 一整套排查性能问题流程（面试级）」

下一步很简单：**不要在 Mac 终端直接输入 `node1`**，因为 `node1` 不是命令。
你要么**进入容器**，要么**在容器里 ssh 到别的节点**。

---

# 你刚才哪里错了

你在宿主机执行了：

```bash
node1
```

所以报：

```bash
zsh: command not found: node1
```

因为：

* `node1` 是容器名 / 主机名
* 不是 shell 命令

---

# 正确思路

## 在 Mac 宿主机里

只能这样进容器：

```bash
docker exec -it node1 bash
docker exec -it node2 bash
docker exec -it node3 bash
```

## 在容器里面

才能这样：

```bash
ssh node2
ssh node3
ping node2
ping node3
```

---

# 你现在就照这个做

## 第1步：进入 node1

在 **Mac 终端** 执行：

```bash
docker exec -it node1 bash
```

---

## 第2步：在 node1 里测试网络

进去后执行：

```bash
ping -c 2 node2
ping -c 2 node3
```

如果都通，继续下一步。

---

## 第3步：生成 SSH key

还在 `node1` 里执行：

```bash
ssh-keygen -t rsa
```

一直按回车。

---

## 第4步：复制公钥到 3 个节点

```bash
ssh-copy-id root@node1
ssh-copy-id root@node2
ssh-copy-id root@node3
```

密码都是：

```bash
123456
```

---

## 第5步：验证免密

```bash
ssh node2
```

进去了就说明成功。然后：

```bash
exit
```

回到 `node1`。

再试：

```bash
ssh node3
```

---

# 你现在只需要记住

## 宿主机

```bash
docker exec -it node1 bash
```

## 容器里

```bash
ssh node2
```

---

# 你这一步的唯一目标

先把 **node1 能 ssh 到 node2 / node3** 做通。

你现在直接执行这句：

```bash
docker exec -it node1 bash
```

进去后马上执行：

```bash
ping -c 2 node2
ping -c 2 node3
```

把结果贴我。


不用纠结，我给你一个**非常清晰的判断规则👇**

---

# 🧠 你现在该不该退出？

👉 **看你当前在哪**

---

## ✅ 情况1：你现在在 Mac（宿主机）

提示符是这种：

```bash
(base) yonggan@Yonggans-MacBook-Pro %
```

👉 **不用退出，直接执行：**

```bash
docker exec -it node1 bash
```

---

## ❗情况2：你在容器里

提示符是这种：

```bash
root@node1:/#
```

👉 **不用退出！直接继续干活**

---

# 🎯 你刚刚的状态

你已经：

```bash
exit
```

回到了 Mac：

```bash
(base) yonggan@Yonggans-MacBook-Pro %
```

👉 所以现在应该：

---

# 🚀 正确下一步（直接复制）

```bash
docker exec -it node1 bash
```

进去后会变成：

```bash
root@node1:/#
```

---

# 🚀 然后立刻执行👇

```bash
ping -c 2 node2
ping -c 2 node3
```

---

# 🧠 超简单记忆（以后不会乱）

```text
看到 root@node1  → 已经在容器里
看到 MacBook-Pro → 在宿主机
```

---

# 👍 一句话结论

👉 **你现在不用退出，直接进 node1 再继续**

---

你现在就执行：

```bash
docker exec -it node1 bash
```

然后把 ping 结果发我。


对，你这个 `exit` 是把 **Terminal 这个 shell 会话关掉了**，不是“回到上一级”。

所以现在看到：

```text
[Process completed]
```

说明：

* 这个终端标签页里的 shell 已经结束了
* 不是卡住
* 也不是报错
* 只是这个窗口现在不能继续输入了

## 下一步

你现在要做的是**重新开一个终端会话**：

### 方法1：最简单

按：

```text
Command + T
```

开一个新的 Terminal 标签页

### 方法2

在 Terminal 顶部菜单点：

```text
Shell > New Tab
```

或者：

```text
Shell > New Window
```

## 新开后你会看到类似

```bash
(base) yonggan@Yonggans-MacBook-Pro ~ %
```

这才是新的可输入终端。

## 然后直接执行

```bash
docker exec -it node1 bash
```

进去后再执行：

```bash
ping -c 2 node2
ping -c 2 node3
```

## 以后别在 Mac 宿主机随便 `exit`

因为：

* 在容器里 `exit` = 退出容器，回到 Mac
* 在 Mac 终端里 `exit` = 关闭当前 shell

你现在开个新 tab 就行。


不是的，你现在这个👇

```bash
(base) yonggan@Yonggans-MacBook-Pro docker-spark-3nodes %
```

👉 **这是你的 Mac（宿主机）终端，不是 node3 ❗**

---

# 🧠 怎么判断在哪？

## 🖥️ 宿主机（Mac）

```bash
(base) yonggan@Yonggans-MacBook-Pro %
```

👉 特征：

* 有你的用户名 `yonggan`
* 有 `MacBook-Pro`
* 有 `(base)`（conda环境）

---

## 🐳 容器里（node1 / node2 / node3）

```bash
root@node1:/#
root@node2:/#
root@node3:/#
```

👉 特征：

* `root@xxx`
* 没有 MacBook-Pro
* 没有 (base)

---

# 🎯 你现在的位置

👉 **你现在在 Mac 上（正确）**

---

# 🚀 下一步（关键一步）

直接执行👇：

```bash
docker exec -it node1 bash
```

---

# 进去后你会看到👇

```bash
root@node1:/#
```

---

# 然后马上执行👇

```bash
ping -c 2 node2
ping -c 2 node3
```

---

# 🧠 记住一句话

```text
docker exec = 进入容器
```

---

# 👍 你现在只需要做一件事

👉 复制这行执行：

```bash
docker exec -it node1 bash
```

然后把 ping 结果发我，我帮你下一步（SSH + Spark）。


很好，**网络已经通了 ✅**

这说明：

* `node1 -> node2` 通
* `node1 -> node3` 通
* Docker 三节点内部网络没问题

---

# 下一步：做 SSH 免密

你现在就在 `root@node1:/#` 里，继续执行下面这些。

## 1）生成 SSH key

```bash
ssh-keygen -t rsa
```

看到提示后，一路按回车就行。

---

## 2）把公钥复制到 3 个节点

依次执行：

```bash
ssh-copy-id root@node1
ssh-copy-id root@node2
ssh-copy-id root@node3
```

密码都是：

```bash
123456
```

如果第一次提示：

```text
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

输入：

```bash
yes
```

---

## 3）测试免密是否成功

先试：

```bash
ssh node2
```

如果直接进去，不要密码，就成功了。

进去后你会看到类似：

```bash
root@node2:/#
```

然后执行：

```bash
exit
```

回到 `node1`。

再试：

```bash
ssh node3
```

---

# 你现在的目标

只做一件事：

> 让 `node1` 能无密码 ssh 到 `node1 / node2 / node3`

---

# 如果 `ssh-copy-id` 不存在

先装一下：

```bash
apt update && apt install -y openssh-client
```

不过按你 Dockerfile，大概率已经有了。

---

# 你现在直接执行第一句

```bash
ssh-keygen -t rsa
```

然后把输出贴给我。


很好，**SSH 免密已经成功了 ✅**

因为你执行：

```bash
ssh node2
```

直接进去了，而且**没有再输入密码**，这就说明成功。

---

# 你现在在哪？

你现在提示符是：

```bash
root@node2:~#
```

👉 说明你现在已经从 `node1` ssh 到了 `node2`

---

# 下一步

先退回 `node1`：

```bash
exit
```

你会回到：

```bash
root@node1:/#
```

---

# 然后再验证 node3

回到 `node1` 后执行：

```bash
ssh node3
```

如果也直接进去，不用密码，说明 `node3` 也好了。

进去后再：

```bash
exit
```

回到 `node1`

---

# 如果 node3 也成功

那你下一步就可以开始装 Spark 了。

在 `node1` 里执行下面这组：

## 1）去 /opt

```bash
cd /opt
```

## 2）下载 Spark

```bash
wget https://dlcdn.apache.org/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz
```

## 3）解压

```bash
tar -zxvf spark-3.2.0-bin-hadoop3.2.tgz
```

## 4）改名

```bash
mv spark-3.2.0-bin-hadoop3.2 spark
```

---

# 你现在只差一步确认

先在 `node2` 里执行：

```bash
exit
```

回到 `node1` 后执行：

```bash
ssh node3
```

把结果贴我。


很好，这几条说明你现在环境是正常的：

## 当前状态

```bash
java -version
```

说明 **Java 11 已安装成功**，这正适合 Spark 3.2。

```bash
echo $JAVA_HOME
```

说明 **JAVA_HOME 也配好了**：

```bash
/usr/lib/jvm/java-11-openjdk-amd64
```

```bash
hostname -I
```

说明 `node1` 的容器 IP 是：

```bash
172.28.0.11
```

---

## 为什么 `ip addr` 不行

```bash
bash: ip: command not found
```

这不是大问题，只是你的镜像里**没装 `ip` 命令**，它通常来自：

```bash
iproute2
```

如果你想装，可以执行：

```bash
apt update && apt install -y iproute2
```

但你现在**不用装也可以继续**，因为：

```bash
hostname -I
```

已经够用了。

---

## 现在结论

你已经确认了：

* Java 正常
* `JAVA_HOME` 正常
* node1 网络正常
* 容器互通正常
* SSH 免密基本成功

---

## 下一步

现在直接去验证 `node3` 免密，然后开始装 Spark。

先执行：

```bash
ssh node3
```

如果能直接进去，说明 3 个节点 SSH 都通了。

进去后再退回：

```bash
exit
```

回到 `node1` 后，开始装 Spark：

```bash
cd /opt
wget https://dlcdn.apache.org/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz
tar -zxvf spark-3.2.0-bin-hadoop3.2.tgz
mv spark-3.2.0-bin-hadoop3.2 spark
```

你现在先执行：

```bash
ssh node3
```


对，这个报错是正常的。

## 为什么？

你现在提示符是：

```bash
root@node1:/#
```

这说明你**已经在 node1 容器里面了**。

所以你再执行：

```bash
docker exec -it node1 bash
```

会报：

```bash
bash: docker: command not found
```

因为：

* `docker` 命令只在你的 **Mac 宿主机** 上有
* 容器内部没有 Docker

---

## 你现在已经不用再 `docker exec` 了

因为你已经在 `node1` 里面了。

你现在该继续做的是：

### 先验证 node3 免密

```bash
ssh node3
```

如果直接进去，说明成功。

进去后退出：

```bash
exit
```

回到 `node1`

---

## 然后开始安装 Spark

回到 `node1` 后执行：

```bash
cd /opt
wget https://dlcdn.apache.org/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz
tar -zxvf spark-3.2.0-bin-hadoop3.2.tgz
mv spark-3.2.0-bin-hadoop3.2 spark
```

---

## 你现在的位置关系，记住这句就够了

### 宿主机 Mac 里才能执行

```bash
docker ps
docker exec -it node1 bash
```

### 容器里执行

```bash
ssh node2
ssh node3
wget
tar
jps
```

---

你现在直接执行这句：

```bash
ssh node3
```

把结果贴我。


很好，**node3 也免密成功了 ✅**

现在说明你已经完成了最关键的基础环境：

* `node1 -> node2` SSH 免密成功
* `node1 -> node3` SSH 免密成功
* 3 个节点网络互通
* Java 11 正常

---

# 下一步

## 先退回 node1

你现在在：

```bash
root@node3:~#
```

执行：

```bash
exit
```

回到：

```bash
root@node1:/#
```

---

# 然后开始安装 Spark

在 `node1` 执行下面这几句：

```bash
cd /opt
wget https://archive.apache.org/dist/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz
tar -zxvf spark-3.2.0-bin-hadoop3.2.tgz
mv spark-3.2.0-bin-hadoop3.2 spark
```

我这里把下载地址换成了 `archive.apache.org`，更适合下旧版本 Spark 3.2.0。

---

# 安装完后继续配置

执行：

```bash
cd /opt/spark/conf
cp spark-env.sh.template spark-env.sh
cp workers.template workers
```

编辑 `spark-env.sh`：

```bash
nano /opt/spark/conf/spark-env.sh
```

在文件最后加：

```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export SPARK_MASTER_HOST=node1
export SPARK_WORKER_MEMORY=1g
```

保存退出。

---

# 配 workers

执行：

```bash
nano /opt/spark/conf/workers
```

改成：

```text
node1
node2
node3
```

保存退出。

---

# 然后把 Spark 分发到另外两个节点

在 `node1` 执行：

```bash
scp -r /opt/spark root@node2:/opt/
scp -r /opt/spark root@node3:/opt/
```

---

# 最后启动集群

```bash
cd /opt/spark
sbin/start-all.sh
```

再检查：

```bash
jps
ssh node2 jps
ssh node3 jps
```

正常应该看到：

* `node1`：`Master` + `Worker`
* `node2`：`Worker`
* `node3`：`Worker`

---

你现在先执行第一步：

```bash
exit
cd /opt
wget https://archive.apache.org/dist/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz
```

把下载结果发我。


对，问题已经定位了：

## 为什么 404

你用的是：

```bash
wget https://dlcdn.apache.org/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz
```

这个地址现在没有这个旧版本了，所以返回 `404 Not Found`。
Apache Archive 里仍然有 `spark-3.2.0-bin-hadoop3.2.tgz` 这个文件。([archive.apache.org][1])

---

## 为什么 `tar` 也失败

因为压缩包根本没下载下来，所以当前目录里没有：

```bash
spark-3.2.0-bin-hadoop3.2.tgz
```

所以 `tar` 找不到文件。

---

# 你现在直接执行这组

还在 `root@node1:/opt#` 的话，直接：

```bash
wget https://archive.apache.org/dist/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz
tar -zxvf spark-3.2.0-bin-hadoop3.2.tgz
mv spark-3.2.0-bin-hadoop3.2 spark
ls /opt
```

---

# 正常的话你会看到

最后 `ls /opt` 应该出现：

```bash
spark
spark-3.2.0-bin-hadoop3.2.tgz
```

---

# 然后下一步

如果上面成功，再继续：

```bash
cd /opt/spark/conf
cp spark-env.sh.template spark-env.sh
cp workers.template workers
```

然后编辑：

```bash
nano spark-env.sh
```

加上：

```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export SPARK_MASTER_HOST=node1
export SPARK_WORKER_MEMORY=1g
```

再编辑：

```bash
nano workers
```

改成：

```bash
node1
node2
node3
```

---
```
你先把这四句跑完，把 `ls /opt` 结果发我。

[1]: https://archive.apache.org/dist/spark/spark-3.2.0/ "Index of /dist/spark/spark-3.2.0"

为什么 404

你用的是：

wget https://dlcdn.apache.org/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz

这个地址现在没有这个旧版本了，所以返回 404 Not Found。
Apache Archive 里仍然有 spark-3.2.0-bin-hadoop3.2.tgz 这个文件。  

为什么 tar 也失败

因为压缩包根本没下载下来，所以当前目录里没有：

spark-3.2.0-bin-hadoop3.2.tgz

所以 tar 找不到文件。

你现在直接执行这组

还在 root@node1:/opt# 的话，直接：

wget https://archive.apache.org/dist/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz
tar -zxvf spark-3.2.0-bin-hadoop3.2.tgz
mv spark-3.2.0-bin-hadoop3.2 spark
ls /opt
正常的话你会看到

最后 ls /opt 应该出现：

spark
spark-3.2.0-bin-hadoop3.2.tgz
然后下一步

如果上面成功，再继续：

cd /opt/spark/conf
cp spark-env.sh.template spark-env.sh
cp workers.template workers

然后编辑：

nano spark-env.sh

加上：

export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export SPARK_MASTER_HOST=node1
export SPARK_WORKER_MEMORY=1g

再编辑：

nano workers

改成：

node1
node2
node3

你先把这四句跑完，把 ls /opt 结果发我。

```

很好，这一步**完全正确，而且你已经走在正确路径上了 ✅**

我帮你总结当前状态（基于你的日志）：

---

# 🎯 当前状态（非常关键）

你已经完成：

### ✅ 集群基础

* node1 / node2 / node3 网络互通
* SSH 免密全部成功
* Java 11 正常

### ✅ Spark 下载已修复

你已经切换到正确地址：

```bash
wget https://archive.apache.org/dist/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz
```

👉 并且已经开始下载（287MB）

---

# ⚠️ 你现在只需要做一件事

👉 **等下载完成，不要中断**

---

# 🚀 下载完成后（直接执行这三句）

```bash
tar -zxvf spark-3.2.0-bin-hadoop3.2.tgz
mv spark-3.2.0-bin-hadoop3.2 spark
ls /opt
```

---

# ✅ 成功标志

`ls /opt` 应该看到：

```bash
spark
spark-3.2.0-bin-hadoop3.2.tgz
```

---

# 🚀 下一步（马上要做）

解压成功后继续：

```bash
cd /opt/spark/conf
cp spark-env.sh.template spark-env.sh
cp workers.template workers
```

---

## 编辑 spark-env.sh

```bash
nano spark-env.sh
```

在最后加：

```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export SPARK_MASTER_HOST=node1
export SPARK_WORKER_MEMORY=1g
```

---

## 编辑 workers

```bash
nano workers
```

改成：

```bash
node1
node2
node3
```

---

# 🔥 接下来大步骤（提前给你心理预期）

你马上要做：

1. 分发 Spark 到 node2 / node3
2. 启动集群
3. 看 jps
4. 打开 UI（如果你映射端口）

---

# 💡 小提醒（你现在的下载速度）

```text
97.5 KB/s → 287MB
```

👉 大概要 30~40 分钟（正常）

---

# 🚀 如果你想加速（可选）

可以换更快源：

```bash
wget https://mirrors.tuna.tsinghua.edu.cn/apache/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz
```

---

# 👍 你现在不用做任何复杂操作

👉 **等下载完成 → 解压 → 配置**

---

# 下一步你做这个就行

等下载结束后执行：

```bash
tar -zxvf spark-3.2.0-bin-hadoop3.2.tgz
```

把结果发我，我带你下一步（配置 + 启动集群 🚀）


很好，这个问题问得很关键，我直接给你结论👇

---

# 🎯 要不要重新下载？

## ❌ 不需要重新下载（大多数情况）

你现在已经在下载：

```bash
archive.apache.org
```

👉 这个是官方历史仓库，**稳定但慢**

---

# 🧠 为什么会慢？

你现在速度：

```text
97 KB/s
```

👉 原因：

* archive.apache.org 在欧洲
* 不是 CDN
* 专门存旧版本 → 不优化速度

---

# 🚀 最优建议（美国环境）

## ✅ 方案1（推荐）：换 CDN 官方源（更快）

```bash
Ctrl + C   # 停掉当前下载
```

然后执行：

```bash
wget https://downloads.apache.org/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz
```

👉 这个是 Apache CDN，通常在美国会更快

---

## ❗如果还是 404

说明这个版本不在主 CDN，只能用 archive。

---

## ✅ 方案2（如果 archive 很慢）

👉 直接换清华源（其实美国也能用）

```bash
wget https://mirrors.tuna.tsinghua.edu.cn/apache/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz
```

👉 很多时候比 archive 快很多

---

# 🧠 怎么判断要不要重下？

## 看进度

如果你看到：

```text
ETA 40 min+
```

👉 建议重下

如果：

```text
ETA 5~10 min
```

👉 可以继续等

---

# 🎯 给你最简单决策

👉 现在这个情况：

```text
97 KB/s → 太慢
```

✔️ 建议：

```bash
Ctrl + C
```

然后执行👇（优先试这个）

```bash
wget https://mirrors.tuna.tsinghua.edu.cn/apache/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz
```

---

# 👍 一句话总结

```text
archive = 稳但慢
downloads = 官方CDN（快）
镜像源 = 最快（一般）
```

---

# 🚀 下一步

你现在：

👉 停掉下载
👉 换这个执行：

```bash
wget https://mirrors.tuna.tsinghua.edu.cn/apache/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz
```

然后把下载速度发我，我帮你判断。


很好，你现在这个情况我帮你**一次性讲清楚（避免你反复踩坑）👇**

---

# ❗为什么又 404？

你试了：

```bash
https://downloads.apache.org/spark/spark-3.2.0/...
```

👉 还是 404，因为：

### 🧠 关键原因

```text
downloads.apache.org = 只放“最新版本”
```

👉 Spark 3.2.0 是旧版本
👉 已经被移走 → 只能在 archive

---

# 🎯 结论（非常重要）

| 地址                   | 能不能用     |
| -------------------- | -------- |
| downloads.apache.org | ❌（没有旧版本） |
| dlcdn.apache.org     | ❌（没有旧版本） |
| archive.apache.org   | ✅（但慢）    |
| 清华镜像                 | ✅（推荐🔥）  |

---

# 🚀 你现在最优解（直接执行）

👉 停掉慢下载（如果还在跑）：

```bash
Ctrl + C
```

👉 然后执行这个👇（最快方案）

```bash
wget https://mirrors.tuna.tsinghua.edu.cn/apache/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz
```

---

# 🧠 为什么这个最快？

* 清华是全球镜像（CDN）
* 美国访问也很快
* 比 archive 快很多

---

# 🚀 下载完成后继续（不用再问）

```bash
tar -zxvf spark-3.2.0-bin-hadoop3.2.tgz
mv spark-3.2.0-bin-hadoop3.2 spark
```

---

# 🔥 你刚才这一步其实已经很接近成功了

你已经看到：

```bash
spark  spark-3.2.0-bin-hadoop3.2.tgz
```

👉 说明你之前下载可能已经成功了一部分甚至完整了！

---

# ⚠️ 先检查一下（很关键）

执行：

```bash
ls -lh /opt
```

---

## 如果看到：

```bash
spark-3.2.0-bin-hadoop3.2.tgz  287M
```

👉 ✔️ 已经下载完成 → **不用重新下！直接解压**

---

## 如果是：

```bash
spark-3.2.0-bin-hadoop3.2.tgz  10M / 50M
```

👉 ❌ 不完整 → 重新下载（用清华源）

---

# 👍 一句话总结

```text
Spark 3.2.0 必须用 archive 或镜像源，CDN已经没有
```

---

# 🚀 你现在做这个

```bash
ls -lh /opt
```

把结果发我，我帮你判断：

👉 **是继续解压，还是重新下载（一步到位）**


很好，你现在踩到的是**最后一个常见坑**👇我帮你一次性解决。

---

# ❗问题本质

你访问的路径：

```bash
spark-3.2.0
```

👉 在很多镜像里 **已经被清理/移动了**
所以：

* downloads ❌
* dlcdn ❌
* 清华 ❌
* 只有 archive ✅（但慢）

---

# 🎯 最稳解决方案（不再折腾）

👉 **用 archive + 断点续传（最快实际方案）**

---

# 🚀 直接执行（关键）

```bash
wget -c https://archive.apache.org/dist/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz
```

---

## 🧠 为什么加 `-c`？

```text
-c = 断点续传（continue）
```

👉 如果你之前已经下载了一部分：

* 不会重新下载
* 直接接着下
* 速度更稳定

---

# 🚨 重要检查（现在就做）

执行：

```bash
ls -lh
```

---

## 情况1（最理想）

```bash
spark-3.2.0-bin-hadoop3.2.tgz  287M
```

👉 ✔️ 已下载完成 → **直接解压**

```bash
tar -zxvf spark-3.2.0-bin-hadoop3.2.tgz
```

---

## 情况2（部分下载）

```bash
spark-3.2.0-bin-hadoop3.2.tgz  20M / 100M
```

👉 ✔️ 用 `-c` 继续下载

---

## 情况3（没有文件）

👉 直接用上面的 wget

---

# 🚀 下载完成后（一步到位）

```bash
tar -zxvf spark-3.2.0-bin-hadoop3.2.tgz
mv spark-3.2.0-bin-hadoop3.2 spark
```

---

# 💡 为什么你刚才所有镜像都404

👉 很关键一句：

```text
Spark 3.2 太旧 → 很多镜像站已经删掉
```

---

# 👍 一句话总结

```text
旧版本 Spark = 只能 archive + -c 续传
```

---

# 🚀 你现在只做这一步

```bash
ls -lh
```

把结果发我，我帮你判断：

👉 **能不能直接解压，还是继续下载（一步到位）**


很好，这一步**完全正确，而且是最优解 ✅**

---

# 🎯 当前状态（关键判断）

你现在看到：

```text
206 Partial Content
```

👉 说明：

```text
断点续传成功了（-c 起作用）
```

并且：

```text
24% → 71.65MB
速度 311KB/s
ETA 11分钟
```

👉 结论：

* ✔️ 下载在继续（不是重新开始）
* ✔️ 速度已经比刚才快了
* ✔️ 10分钟内能完成（完全可以等）

---

# 🚀 你现在唯一要做的

👉 **不要动，等它下载完**

---

# ⏳ 下载完成后（下一步）

你直接执行这三句：

```bash
tar -zxvf spark-3.2.0-bin-hadoop3.2.tgz
mv spark-3.2.0-bin-hadoop3.2 spark
ls /opt
```

---

# ✅ 正常结果

```bash
spark
spark-3.2.0-bin-hadoop3.2.tgz
```

---

# 🚀 然后继续（非常关键）

```bash
cd /opt/spark/conf
cp spark-env.sh.template spark-env.sh
cp workers.template workers
```

---

## 编辑 spark-env.sh

```bash
nano spark-env.sh
```

加：

```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export SPARK_MASTER_HOST=node1
export SPARK_WORKER_MEMORY=1g
```

---

## 编辑 workers

```bash
nano workers
```

改成：

```text
node1
node2
node3
```

---

# 🔥 接下来马上要做（提前告诉你）

等你这一步完成：

👉 分发 Spark 到 node2/node3
👉 启动集群
👉 jps 验证

---

# 💡 你现在其实已经进入“成功阶段”

你已经完成：

* Docker 3节点 ✔️
* 网络 ✔️
* SSH免密 ✔️
* Java ✔️

👉 现在只差：

```text
Spark安装 + 启动
```

---

# 👍 一句话总结

```text
你现在只需要等下载完成，后面 5 步就能跑起 Spark 集群
```

---

等下载完成后，把：

```bash
ls /opt
```

发我，我带你**直接启动集群 🚀**


很好，这一段我帮你整理成**一步一步执行版（直接照抄）🚀**

等你 **解压完成后，从这里开始👇**

---

# 🚀 Step 1：配置 Spark（在 node1）

```bash
cd /opt/spark/conf
cp spark-env.sh.template spark-env.sh
cp workers.template workers
```

---

## ✏️ 编辑 spark-env.sh

```bash
nano spark-env.sh
```

👉 在最后加：

```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export SPARK_MASTER_HOST=node1
export SPARK_WORKER_MEMORY=1g
```

保存退出（Ctrl + X → Y → Enter）

---

## ✏️ 编辑 workers

```bash
nano workers
```

改成：

```text
node1
node2
node3
```

保存退出

---

# 🚀 Step 2：分发 Spark 到 node2 / node3

👉 在 node1 执行：

```bash
scp -r /opt/spark root@node2:/opt/
scp -r /opt/spark root@node3:/opt/
```

👉 不会再问密码（因为你已经免密了）

---

# 🚀 Step 3：启动 Spark 集群（在 node1）

```bash
cd /opt/spark
sbin/start-all.sh
```

---

# 🚀 Step 4：验证集群

## ✔️ node1

```bash
jps
```

应该看到：

```text
Master
Worker
```

---

## ✔️ node2

```bash
ssh node2 jps
```

应该看到：

```text
Worker
```

---

## ✔️ node3

```bash
ssh node3 jps
```

应该看到：

```text
Worker
```

---

# 🎯 最终结果（你应该看到）

| 节点    | 进程              |
| ----- | --------------- |
| node1 | Master + Worker |
| node2 | Worker          |
| node3 | Worker          |

---

# 🔥 面试级一句话（你可以背）

```text
Spark Standalone cluster consists of one Master and multiple Workers, where Master schedules tasks and Workers execute them.
```

---

# 🚨 常见坑（提前帮你避）

### ❌ jps 没反应

```bash
apt install openjdk-11-jdk -y
```

---

### ❌ start-all.sh 报错

👉 99% 是：

* SSH 没通（你已经解决）
* JAVA_HOME 没配（你已配）

---

# 👍 你现在只差最后3步

```text
配置 → 分发 → 启动
```

---

# 🚀 下一步你做这个

等你解压完成后直接执行：

```bash
cd /opt/spark/conf
```

把输出发我，我帮你检查配置是否OK，然后带你启动🔥


很好，这一步你已经**关键成功了 ✅（Spark下载完成）**

```bash
287MB saved ✔️
```

👉 接下来就是**最后 3 步：解压 → 配置 → 启动**

我给你**一步一步命令版（照抄即可）👇**

---

# 🚀 Step 1：解压 + 重命名

```bash
tar -zxvf spark-3.2.0-bin-hadoop3.2.tgz
mv spark-3.2.0-bin-hadoop3.2 spark
ls /opt
```

---

# 🚀 Step 2：配置 Spark

```bash
cd /opt/spark/conf
cp spark-env.sh.template spark-env.sh
cp workers.template workers
```

---

## ✏️ 编辑 spark-env.sh

```bash
nano spark-env.sh
```

👉 在最后加：

```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export SPARK_MASTER_HOST=node1
export SPARK_WORKER_MEMORY=1g
```

👉 保存：

```
Ctrl + X → Y → Enter
```

---

## ✏️ 编辑 workers

```bash
nano workers
```

改成：

```text
node1
node2
node3
```

保存退出

---

# 🚀 Step 3：分发 Spark（非常关键）

```bash
scp -r /opt/spark root@node2:/opt/
scp -r /opt/spark root@node3:/opt/
```

👉 不会要密码（你已经免密）

---

# 🚀 Step 4：启动集群

```bash
cd /opt/spark
sbin/start-all.sh
```

---

# 🚀 Step 5：验证

## node1

```bash
jps
```

👉 应该看到：

```text
Master
Worker
```

---

## node2

```bash
ssh node2 jps
```

👉 应该看到：

```text
Worker
```

---

## node3

```bash
ssh node3 jps
```

👉 应该看到：

```text
Worker
```

---

# 🎯 成功标志

```text
node1: Master + Worker
node2: Worker
node3: Worker
```

---

# 💡 你现在已经进入最后阶段

你已经完成：

* Docker三节点 ✔️
* 网络 ✔️
* SSH免密 ✔️
* Java ✔️
* Spark下载 ✔️

👉 现在就是**启动集群（最后一步）**

---

# 🚀 你现在做这个

直接执行：

```bash
tar -zxvf spark-3.2.0-bin-hadoop3.2.tgz
```

然后把输出发我，我帮你继续下一步（配置检查 + 启动）

说明你现在这个 `/opt/spark` **不是解压出来的 Spark 目录**。

最可能是你之前手动建过一个空的 `spark` 目录，所以：

```bash
ls /opt
```

能看到 `spark`，但里面没有 `conf`。

---

# 直接修复

你现在在 `root@node1:/opt#`，直接执行下面这组：

```bash
rm -rf /opt/spark
tar -zxvf /opt/spark-3.2.0-bin-hadoop3.2.tgz -C /opt
mv /opt/spark-3.2.0-bin-hadoop3.2 /opt/spark
ls /opt
ls /opt/spark
```

---

# 正常的话你会看到

```bash
/opt/spark
```

里面有这些目录之一：

```bash
bin
conf
sbin
jars
python
```

---

# 然后继续

如果 `ls /opt/spark` 正常，再执行：

```bash
cd /opt/spark/conf
cp spark-env.sh.template spark-env.sh
cp workers.template workers
```

编辑 `spark-env.sh`：

```bash
nano spark-env.sh
```

追加：

```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export SPARK_MASTER_HOST=node1
export SPARK_WORKER_MEMORY=1g
```

编辑 `workers`：

```bash
nano workers
```

改成：

```text
node1
node2
node3
```

---

# 后面三步

配置完后直接：

```bash
scp -r /opt/spark root@node2:/opt/
scp -r /opt/spark root@node3:/opt/
cd /opt/spark
sbin/start-all.sh
```

再验证：

```bash
jps
ssh node2 jps
ssh node3 jps
```

---

你现在先执行这组修复命令：

```bash
rm -rf /opt/spark
tar -zxvf /opt/spark-3.2.0-bin-hadoop3.2.tgz -C /opt
mv /opt/spark-3.2.0-bin-hadoop3.2 /opt/spark
ls /opt/spark
```

把结果发我。


完美 ✅ 这一步说明：

```text
Spark 已正确安装 ✔️
```

你现在 `/opt/spark` 结构是完整的（有 `conf / sbin / bin`），可以继续了。

---

# 🚀 下一步：配置 Spark（关键一步）

你现在就在：

```bash
root@node1:/opt#
```

直接执行👇

---

## Step 1：进入配置目录

```bash
cd /opt/spark/conf
```

---

## Step 2：创建配置文件

```bash
cp spark-env.sh.template spark-env.sh
cp workers.template workers
```

---

## Step 3：编辑 spark-env.sh

```bash
nano spark-env.sh
```

👉 在文件最后加👇

```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export SPARK_MASTER_HOST=node1
export SPARK_WORKER_MEMORY=1g
```

👉 保存：

```
Ctrl + X → Y → Enter
```

---

## Step 4：编辑 workers

```bash
nano workers
```

👉 改成👇

```text
node1
node2
node3
```

👉 保存退出

---

# 🚀 下一步（马上）

配置完成后继续：

## Step 5：分发 Spark

```bash
scp -r /opt/spark root@node2:/opt/
scp -r /opt/spark root@node3:/opt/
```

---

## Step 6：启动集群

```bash
cd /opt/spark
sbin/start-all.sh
```

---

## Step 7：验证

```bash
jps
```

👉 应该看到：

```text
Master
Worker
```

再：

```bash
ssh node2 jps
ssh node3 jps
```

---

# 🎯 成功标志

| 节点    | 结果              |
| ----- | --------------- |
| node1 | Master + Worker |
| node2 | Worker          |
| node3 | Worker          |

---

# 🧠 你现在处于什么阶段

```text
你已经完成 90% ✔️
只差：配置 + 启动
```

---

# 🚀 你现在做这个

```bash
cd /opt/spark/conf
```

然后执行：

```bash
cp spark-env.sh.template spark-env.sh
```

把下一步输出发我，我帮你确认配置是否OK，然后带你启动🔥


很好，你现在这一步是**关键配置点 🔥**

---

# ❗你现在看到的内容

```text
localhost
```

👉 这代表：

```text
只在本机启动 Worker ❌
```

---

# 🚀 正确做法（必须改）

## 在 nano 里直接这样改👇

把：

```text
localhost
```

删掉，改成：

```text
node1
node2
node3
```

---

# ✏️ 完整结果应该是

```text
node1
node2
node3
```

👉 不要多空格，不要写 localhost

---

# 💾 保存退出（你现在这一步）

按：

```text
Ctrl + X
Y
Enter
```

---

# 🚀 下一步（继续执行）

现在继续👇

## 分发 Spark

```bash
scp -r /opt/spark root@node2:/opt/
scp -r /opt/spark root@node3:/opt/
```

---

## 启动集群

```bash
cd /opt/spark
sbin/start-all.sh
```

---

## 验证

```bash
jps
```

👉 应该看到：

```text
Master
Worker
```

然后：

```bash
ssh node2 jps
ssh node3 jps
```

---

# 🎯 你这一步的意义（面试点）

```text
workers 文件 = 定义 Worker 节点列表
```

👉 Spark Master 会：

* SSH 到这些机器
* 启动 Worker

---

# 👍 一句话总结

```text
workers = 集群机器清单（谁跑 Worker）
```

---

# 🚀 你现在只做两件事

1️⃣ 改成：

```text
node1
node2
node3
```

2️⃣ 保存退出

---

然后直接执行：

```bash
scp -r /opt/spark root@node2:/opt/
```

把结果发我，我带你最后启动 🚀


很好，这个结果非常关键👇

```bash
344 Jps
```

👉 说明：

```text
Spark 还没启动 ❗（正常）
```

---

# 🧠 为什么只有 Jps？

`jps` 只看到：

* 自己（Jps）

👉 没有看到：

```text
Master
Worker
```

说明：

```text
你还没执行 start-all.sh
```

---

# 🚀 下一步（真正启动集群）

你现在就在：

```bash
root@node1:/opt/spark#
```

直接执行👇：

```bash
sbin/start-all.sh
```

---

# ⏳ 执行后你会看到类似

```text
starting org.apache.spark.deploy.master.Master
starting org.apache.spark.deploy.worker.Worker
...
```

---

# 🚀 然后立刻验证

## node1

```bash
jps
```

应该看到：

```text
Master
Worker
```

---

## node2

```bash
ssh node2 jps
```

---

## node3

```bash
ssh node3 jps
```

---

# 🎯 成功标志

| 节点    | 应该看到            |
| ----- | --------------- |
| node1 | Master + Worker |
| node2 | Worker          |
| node3 | Worker          |

---

# 🚨 如果启动失败（提前帮你判断）

常见原因：

1. ❌ workers 没改（你刚改了）
2. ❌ spark-env.sh 没配 JAVA_HOME
3. ❌ SSH 不通（你已解决）

👉 所以你大概率会一次成功

---

# 👍 一句话总结

```text
现在只是没启动，不是坏了
```

---

# 🚀 你现在就做这个

```bash
sbin/start-all.sh
```

把输出发我，我帮你确认是否完全成功 🔥



问题已经很清楚了，一共 **2 个错误**：

---

# 1. `spark-env.sh` 第一行坏了

你这里报：

```bash
/opt/spark/conf/spark-env.sh: line 1: ÷#!/usr/bin/env: No such file or directory
```

说明你的 `spark-env.sh` 第一行前面多了一个乱码字符：

```bash
÷#!/usr/bin/env bash
```

正确应该是：

```bash
#!/usr/bin/env bash
```

---

# 2. `JAVA_HOME` 路径写错了

你报：

```bash
/usr/lib/jvm/java-11-openjdk-amd64/bin/java: No such file or directory
```

因为你这个容器是 **aarch64/ARM**，不是 amd64。

你前面虽然 `echo $JAVA_HOME` 看起来是这个值，但实际 Java 在别的目录。

---

# 现在直接修

你现在在 `root@node1:/opt/spark#`，按下面做。

## 第一步：找真正的 Java 路径

执行：

```bash
readlink -f $(which java)
```

把结果记下来。大概率会像这样：

```bash
/usr/lib/jvm/java-11-openjdk-arm64/bin/java
```

---

## 第二步：重写 `spark-env.sh`

直接执行：

```bash
cat > /opt/spark/conf/spark-env.sh <<'EOF'
#!/usr/bin/env bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
export SPARK_MASTER_HOST=node1
export SPARK_WORKER_MEMORY=1g
EOF
```

如果你上一步查出来不是 `arm64`，就把这里改成你实际查到的目录，去掉最后的 `/bin/java`，只留 Java Home。

例如如果上一步是：

```bash
/usr/lib/jvm/java-11-openjdk-arm64/bin/java
```

那这里就写：

```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
```

---

## 第三步：确认 workers

执行：

```bash
cat /opt/spark/conf/workers
```

应该是：

```bash
node1
node2
node3
```

如果不是，就改：

```bash
cat > /opt/spark/conf/workers <<'EOF'
node1
node2
node3
EOF
```

---

## 第四步：重新分发到 node2 / node3

执行：

```bash
scp /opt/spark/conf/spark-env.sh root@node2:/opt/spark/conf/
scp /opt/spark/conf/spark-env.sh root@node3:/opt/spark/conf/
scp /opt/spark/conf/workers root@node2:/opt/spark/conf/
scp /opt/spark/conf/workers root@node3:/opt/spark/conf/
```

---

## 第五步：重新启动

先清一下旧进程：

```bash
sbin/stop-all.sh
```

再启动：

```bash
sbin/start-all.sh
```

---

## 第六步：验证

执行：

```bash
jps
ssh node2 jps
ssh node3 jps
```

正确结果应该是：

* node1: `Master` 和 `Worker`
* node2: `Worker`
* node3: `Worker`

---

你现在先执行这句：

```bash
readlink -f $(which java)
```

把输出发我。



成功了 ✅

### 当前结果

* `node1`: `Master` + `Worker`
* `node2`: `Worker`
* `node3`: `Worker`

这说明你的 **Spark Standalone 3-node cluster 已经跑起来了**。

### 你已经完成

* Docker 模拟 3 台机器
* 节点互 ping
* SSH 免密
* Spark 安装
* Master/Worker 启动
* `jps` 验证通过

### 现在可以怎么验证

在 `node1` 里跑：

```bash
/opt/spark/bin/spark-submit \
  --master spark://node1:7077 \
  /opt/spark/examples/src/main/python/pi.py 10
```

如果正常，会输出类似 `Pi is roughly ...`

### 关于 Web UI

你现在还没做端口映射，所以宿主机浏览器暂时打不开 `8080`。
如果想在 Mac 上看 UI，需要给 `node1` 映射端口，比如 `8080:8080`。

### 面试里可以怎么说

> I set up a Spark Standalone cluster with one Master and three Workers using Docker containers to simulate multi-node deployment on a Mac.

如果你愿意，下一步我可以直接给你：
**1) 跑一个 Spark 测试任务**
或
**2) 改 docker-compose，打开 8080 UI**


先做 **1) 跑一个 Spark 测试任务**，最快验证集群真的在算。

在 `node1` 里直接执行：

```bash
/opt/spark/bin/spark-submit \
  --master spark://node1:7077 \
  /opt/spark/examples/src/main/python/pi.py 10
```

如果成功，你会看到类似：

```text
Pi is roughly 3.14...
```

再做一个更直观的：

```bash
/opt/spark/bin/spark-submit \
  --master spark://node1:7077 \
  /opt/spark/examples/src/main/python/wordcount.py \
  /opt/spark/README.md
```

---

如果你要 **2) 打开 8080 UI**，改 `docker-compose.yml` 里 `node1` 这一段，加上 `ports`：

```yaml
  node1:
    build: .
    container_name: node1
    hostname: node1
    tty: true
    stdin_open: true
    privileged: true
    ports:
      - "8080:8080"
      - "8081:8081"
      - "4040:4040"
      - "2221:22"
    networks:
      spark-net:
        ipv4_address: 172.28.0.11
```

`node2` 和 `node3` 可以这样：

```yaml
  node2:
    build: .
    container_name: node2
    hostname: node2
    tty: true
    stdin_open: true
    privileged: true
    ports:
      - "2222:22"
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
      - "2223:22"
    networks:
      spark-net:
        ipv4_address: 172.28.0.13
```

然后在 Mac 宿主机执行：

```bash
docker compose down
docker compose up -d --build
```

再重新进 `node1`，启动 Spark：

```bash
docker exec -it node1 bash
cd /opt/spark
sbin/start-all.sh
```

之后浏览器打开：

```text
http://localhost:8080
```

你现在先跑这个最重要的验证命令：

```bash
/opt/spark/bin/spark-submit \
  --master spark://node1:7077 \
  /opt/spark/examples/src/main/python/pi.py 10
```


这是正常现象里的“异常分支”：

你现在这句

```bash
ssh -o StrictHostKeyChecking=no root@node2
```

**不需要这样写**。
你前面已经验证过免密是通的，直接用：

```bash
ssh node2
```

更简单。

---

# 为什么现在又要密码

最可能是这几个原因之一：

## 1. 你没必要加 `-o StrictHostKeyChecking=no`

它只是跳过 host key 确认，**不负责免密**。

## 2. `root@node2` 和你之前测试的方式不一致

你之前成功的是：

```bash
ssh node2
```

所以先继续用这个。

## 3. 如果容器重建过，authorized_keys 可能变了

但你现在 Spark 已经跑起来，说明节点间 SSH 基本是通的。

---

# 你现在该做什么

## 先别管这个 SSH

你现在的目标不是再测 SSH，而是**跑 Spark 测试任务**。

你已经在 `node1` 里了，直接执行：

```bash
/opt/spark/bin/spark-submit \
  --master spark://node1:7077 \
  /opt/spark/examples/src/main/python/pi.py 10
```

---

# 如果你就是想测试 SSH

先按：

```bash
Ctrl + C
```

取消当前密码输入。

然后试：

```bash
ssh node2
```

如果还想彻底检查免密，再执行：

```bash
ssh -v node2
```

---

# 现在最推荐的下一步

直接跑这个：

```bash
/opt/spark/bin/spark-submit \
  --master spark://node1:7077 \
  /opt/spark/examples/src/main/python/pi.py 10
```

把输出贴给我。


你**大概率已经通过过免密了**，因为你之前成功执行过：

* `ssh node2` 直接进去
* `ssh node3` 直接进去
* `start-all.sh` 也把 `node2` 和 `node3` 的 Worker 拉起来了

如果**没有免密**，`start-all.sh` 一般很难把远端 Worker 正常拉起来。

---

# 你现在为什么又像没免密？

因为你这次用了：

```bash
ssh -o StrictHostKeyChecking=no root@node2
```

这和你前面成功的方式不一样。
先不要用这个，先用你之前成功过的最简单方式：

```bash
ssh node2
```

---

# 现在怎么确认，最准确？

你在 `node1` 里直接执行这两个命令：

```bash
ssh node2 hostname
ssh node3 hostname
```

## 如果免密成功

会直接输出：

```bash
node2
node3
```

**不会问密码。**

## 如果失败

会提示你输入密码。

---

# 如果真的失败，重新做一遍免密

在 `node1` 里执行：

```bash
ssh-copy-id root@node2
ssh-copy-id root@node3
```

密码输入：

```bash
123456
```

然后再测试：

```bash
ssh node2 hostname
ssh node3 hostname
```

---

# 再检查一下公钥文件

在 `node1` 里看：

```bash
ls -l /root/.ssh
cat /root/.ssh/id_rsa.pub
```

然后在 `node2` 里看：

```bash
ssh node2
cat /root/.ssh/authorized_keys
exit
```

如果 `authorized_keys` 里有 `node1` 的公钥，就说明配置是对的。

---

# 最关键的一句

你现在先不要猜，直接测这个最清楚：

```bash
ssh node2 hostname
ssh node3 hostname
```

把输出发我。


对，这次看起来是 **免密失效了**，因为：

```bash
ssh node2 hostname
```

已经开始要密码了。

不过别慌，**Spark 能跑起来说明之前至少通过一次**，现在重新补一下最稳。

# 现在这样做

你当前在 `node1`，先按：

```bash
Ctrl + C
```

取消当前密码输入。

---

# Step 1：重新把公钥写到 node2 / node3

在 `node1` 执行：

```bash
ssh-copy-id root@node2
ssh-copy-id root@node3
```

密码都输入：

```bash
123456
```

---

# Step 2：立即测试

执行：

```bash
ssh node2 hostname
ssh node3 hostname
```

## 正确结果应该是

直接输出：

```bash
node2
node3
```

而且**不问密码**。

---

# 如果还问密码，再做这个检查

## 先看 node1 公钥

```bash
cat /root/.ssh/id_rsa.pub
```

## 再登录 node2 检查 authorized_keys

```bash
ssh root@node2
cat /root/.ssh/authorized_keys
exit
```

看里面有没有和 `id_rsa.pub` 一样的内容。

---

# 最省事的修复方式

如果你想直接强制重建 authorized_keys，可以在 `node1` 执行：

```bash
cat /root/.ssh/id_rsa.pub | ssh root@node2 "mkdir -p /root/.ssh && cat >> /root/.ssh/authorized_keys"
cat /root/.ssh/id_rsa.pub | ssh root@node3 "mkdir -p /root/.ssh && cat >> /root/.ssh/authorized_keys"
```

然后再测：

```bash
ssh node2 hostname
ssh node3 hostname
```

---

# 你现在先做这两句

```bash
ssh-copy-id root@node2
ssh-copy-id root@node3
```

把结果发我。



对，**现在这次重启/重建后，免密确实没保持住**。

而且你这里其实有 **两个问题**：

# 1）`node2` 在要密码

说明 `node1 -> node2` 的公钥登录没生效。

# 2）`node3` 在问 authenticity

说明 `node3` 的 host key 变了，通常是**容器重建后指纹变了**。

---

# 现在别一起输两条命令了

你刚才输入了：

```bash
ssh node2 hostname
ssh node3 hostname
```

以后一次只输一条。

---

# 现在这样修，最稳

## 第一步：按 `Ctrl + C`

先退出当前卡住状态。

---

## 第二步：清掉旧的 known_hosts 记录

在 `node1` 里执行：

```bash
ssh-keygen -R node2
ssh-keygen -R node3
```

---

## 第三步：重新复制公钥

执行：

```bash
ssh-copy-id root@node2
ssh-copy-id root@node3
```

过程中如果看到：

```bash
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

输入：

```bash
yes
```

密码还是：

```bash
123456
```

---

## 第四步：重新测试

一条一条执行：

```bash
ssh node2 hostname
```

再执行：

```bash
ssh node3 hostname
```

---

# 正确结果应该是

直接输出：

```bash
node2
node3
```

并且**不再问密码**。

---

# 为什么会这样

因为你前面很可能重新起过容器，容器里的：

* `/root/.ssh/authorized_keys`
* SSH host key

都可能变了。

所以：

* 以前的免密失效
* known_hosts 也可能不匹配

---

# 你现在就按这个顺序执行

```bash
Ctrl + C
ssh-keygen -R node2
ssh-keygen -R node3
ssh-copy-id root@node2
ssh-copy-id root@node3
ssh node2 hostname
ssh node3 hostname
```

先把 `ssh-copy-id root@node2` 的输出发我。


很好，第一步完成了。

结果说明：

* `node2` 的旧 host key 已经删掉了 ✅
* `node3` 当前 `known_hosts` 里没有记录，也没关系 ✅

---

# 下一步直接做

在 `node1` 里一条一条执行：

```bash
ssh-copy-id root@node2
```

如果提示：

```text
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

输入：

```bash
yes
```

密码输入：

```bash
123456
```

然后再执行：

```bash
ssh-copy-id root@node3
```

同样输入：

```bash
yes
```

和密码：

```bash
123456
```

---

# 然后测试

还是在 `node1`：

```bash
ssh node2 hostname
```

再执行：

```bash
ssh node3 hostname
```

正确的话会直接输出：

```bash
node2
node3
```

不会再问密码。

把 `ssh-copy-id root@node2` 的结果发我。


很好，这个错误已经**定位根因了 👇**

```bash
ERROR: No identities found
```

👉 含义：

```text
node1 上没有 SSH 公钥（id_rsa.pub 不存在）
```

也就是说：

👉 **你的 key 丢了 / 容器重建后没了**

---

# 🚀 直接修（一步到位）

## 第一步：重新生成 key

在 `node1` 执行：

```bash
ssh-keygen -t rsa
```

👉 一路按回车（不要密码）

---

## 第二步：确认生成成功

执行：

```bash
ls /root/.ssh
```

应该看到：

```bash
id_rsa
id_rsa.pub
```

---

## 第三步：重新分发公钥

```bash
ssh-copy-id root@node2
ssh-copy-id root@node3
```

👉 输入：

```bash
yes
123456
```

---

## 第四步：验证免密

```bash
ssh node2 hostname
ssh node3 hostname
```

---

# 🎯 正确结果

```bash
node2
node3
```

👉 不再问密码 = 成功

---

# 🧠 为什么会这样（你要知道）

因为：

```text
Docker 容器 = 临时系统
```

👉 你重建过容器：

* `/root/.ssh/id_rsa` 被清掉
* 所以 ssh-copy-id 找不到 key

---

# 👍 一句话总结

```text
ERROR: No identities found = 没有 SSH key → 重新 ssh-keygen
```

---

# 🚀 你现在只做这个

```bash
ssh-keygen -t rsa
```

然后把输出发我，我帮你继续下一步（确保免密彻底稳定 🔥）


对，就按这个做。

你现在在 `node1` 里直接输入：

```bash
ssh-keygen -t rsa
```

一路回车后，再执行：

```bash
ls /root/.ssh
```

如果看到：

```bash
id_rsa
id_rsa.pub
```

继续执行：

```bash
ssh-copy-id root@node2
ssh-copy-id root@node3
```

最后验证：

```bash
ssh node2 hostname
ssh node3 hostname
```

把这四步的输出贴给我。



