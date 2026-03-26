下面是帮你整理好的**Markdown版本（可直接复制到GitHub/Notion）**👇
已结构化 + 面试友好 + 可打印

---

# 🧠 Bash & Linux 命令速查表

> 一句话理解
> **Bash = Linux / Mac 终端里用来“和系统说话”的命令语言**

---

# 📂 1. 文件 / 目录操作

## 🔍 `ls -l` 输出结构

```bash
-rwxr-xr-x 1 root root 4703728 Dec 17 07:01 file.txt
```

| 位置 | 含义   | 解释        |
| -- | ---- | --------- |
| 1  | 权限   | rwx       |
| 2  | 链接数  | 通常忽略      |
| 3  | 所有者  | user      |
| 4  | 所属组  | group     |
| 5  | 文件大小 | bytes     |
| 6  | 修改时间 | timestamp |
| 7  | 文件名  | name      |

---

## 🔐 权限解释

| 符号 | 含义      |
| -- | ------- |
| r  | read    |
| w  | write   |
| x  | execute |

```
-rwxr-xr-x
```

| 部分  | 含义     |
| --- | ------ |
| -   | 文件     |
| d   | 目录     |
| rwx | owner  |
| r-x | group  |
| r-x | others |

---

## 📁 常用命令

```bash
ls
ls -l
ls -a

cd folder
cd ..
cd ~

pwd

mkdir test
mkdir -p a/b/c

rm file.txt
rm -r folder

cp a.txt b.txt
mv a.txt b.txt
```

---

# 📄 2. 文件查看

## 📊 对比表

| 命令      | 作用   | 特点    |
| ------- | ---- | ----- |
| cat     | 查看全部 | 小文件   |
| less    | 滚动查看 | 大文件🔥 |
| head    | 前几行  | 默认10  |
| tail    | 后几行  |       |
| tail -f | 实时日志 | 🔥    |

---

## 🔧 示例

```bash
cat file.txt
head -n 20 file.txt
tail -n 50 file.txt
tail -f log.txt
less file.txt
```

---

# 🔍 3. 文本处理三剑客

## 🧠 总览

| 工具   | 作用 |
| ---- | -- |
| grep | 查找 |
| awk  | 取列 |
| sed  | 替换 |

---

## grep

```bash
grep "error" log.txt
grep -i error log.txt
grep -v info log.txt
```

---

## awk

```bash
awk '{print $1}'
awk -F "," '{print $1}'
```

---

## sed

```bash
sed 's/a/b/g'
sed -i 's/old/new/g' file.txt
```

---

# ⚙️ 4. 系统 & 进程

```bash
ps aux
top
kill -9 PID
```

| 命令   | 作用   |
| ---- | ---- |
| ps   | 进程列表 |
| top  | 实时监控 |
| kill | 杀进程  |

---

# 💾 5. 磁盘

```bash
df -h
du -sh folder
```

| 命令 | 作用   |
| -- | ---- |
| df | 磁盘空间 |
| du | 文件大小 |

---

# 🌐 6. 网络

```bash
ping google.com
curl http://api.com
wget file
```

| 命令   | 作用    |
| ---- | ----- |
| ping | 连通性   |
| curl | API请求 |
| wget | 下载    |

---

# 🔗 7. 管道 & 重定向（🔥重点）

```bash
ls | grep txt
echo "hello" > a.txt
echo "world" >> a.txt
cat file.txt | wc -l
```

| 符号 | 作用 |
| -- | -- |
| |  | 管道 |
| >  | 覆盖 |
| >> | 追加 |

👉 面试关键词：**pipeline / data flow**

---

# 🧩 8. 权限

```bash
chmod 755 file.sh
chown user file
```

| 命令    | 作用  |
| ----- | --- |
| chmod | 权限  |
| chown | 所有者 |

---

## 🔐 755解释

| 数字 | 权限  |
| -- | --- |
| 7  | rwx |
| 5  | r-x |
| 5  | r-x |

---

# 🚀 9. 环境变量

```bash
echo $PATH
echo $JAVA_HOME

export JAVA_HOME=/usr/lib/jvm
```

| 命令              | 作用   |
| --------------- | ---- |
| echo $PATH      | 查看路径 |
| echo $JAVA_HOME | 查看变量 |
| export          | 设置变量 |

---

## ⚠️ 注意

| 问题    | 原因       |
| ----- | -------- |
| 不生效   | 没 source |
| 新窗口失效 | export临时 |

---

# 🧠 10. Top 命令（性能监控）

```bash
top
```

| 指标           | 含义    |
| ------------ | ----- |
| load average | 系统负载  |
| us           | 用户CPU |
| sy           | 系统CPU |
| id           | 空闲    |
| wa           | IO等待  |

---

## 🔥 快捷键

| 键 | 作用    |
| - | ----- |
| P | CPU排序 |
| M | 内存排序  |
| q | 退出    |

---

# 🐳 11. Docker（实战）

```bash
docker ps
docker exec -it container bash
docker logs container
```

---

# ☁️ 12. 服务器 / AWS

```bash
ssh user@ip
scp file user@ip:/
nohup java -jar app.jar &
```

---

# 🔥 面试黄金组合

```bash
ps aux | grep java
tail -f log.txt | grep error
cat file.txt | wc -l
```

---

# 🎯 面试一句话总结

> **Bash is a shell used to interact with the OS, manage files, monitor processes, and process data using pipelines.**

---

# ⚡ 最重要20个（必须熟）

```bash
ls cd pwd mkdir rm cp mv
cat less tail grep
ps top kill
df du
curl ping
export source
docker ps exec logs
ssh scp
```

---

如果你要，我可以再给你👇
👉 一页 **“Linux 面试速记卡（A4打印版）”**
👉 或 **“真实面试题 + 标准答案”**

直接说：**要速记卡版** 🚀
