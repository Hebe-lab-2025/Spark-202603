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
