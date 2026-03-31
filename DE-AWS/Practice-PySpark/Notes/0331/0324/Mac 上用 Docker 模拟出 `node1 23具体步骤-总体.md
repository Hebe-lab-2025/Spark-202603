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
