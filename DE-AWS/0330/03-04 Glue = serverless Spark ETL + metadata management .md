<img width="653" height="210" alt="image" src="https://github.com/user-attachments/assets/c64c5121-ea73-4d94-a8c5-cdd4b9314e1a" />

很好🔥 现在进入 **Section 4：AWS Glue Deep Dive（深度剖析）**
👉 这一部分是 **面试拉开差距的关键🔥**

---

# 🧠 一句话核心（面试必背）

> AWS Glue = serverless Spark ETL + metadata management

---

# 🧭 一、Glue 深度理解（本质🔥）

![Image](https://docs.aws.amazon.com/images/glue/latest/dg/images/HowItWorks-overview.png)

![Image](https://miro.medium.com/0%2Adz-LGWbS8vSOZC9s.png)

![Image](https://docs.aws.amazon.com/images/glue/latest/dg/images/PopulateCatalog-overview.png)

![Image](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2022/08/26/revekkak-new-withborder.png)

---

👉 Glue = 3 层结构：

```text
Data Source → Glue → Target
```

👉 细化：

```text
S3 / RDS → Crawler → Catalog → Job → S3 / Redshift
```

---

# ⚡ 二、Glue 内部是怎么工作的？（面试重点🔥）

---

## 🔥 1️⃣ Glue Job 本质 = Spark

👉 关键点：

* 本质是 Spark job
* 用 PySpark 写

👉 面试一句话：

> Glue runs ETL jobs on Spark under the hood.

---

## 🔥 2️⃣ Serverless（核心优势）

👉 不用：

* 配 cluster
* 管资源

👉 AWS 自动分配

---

## 🔥 3️⃣ 动态资源（DPU🔥）

👉 Glue 用：

👉 **DPU（Data Processing Unit）**

---

👉 你要记住：

> 更多 DPU → 更快 → 更贵

---

# 🎯 三、Glue 核心组件（深度版🔥）

---

## 🔥 1️⃣ Crawler（自动建表）

👉 做什么：

* 扫 S3
* 推断 schema

👉 输出：
👉 Data Catalog

---

## 🔥 2️⃣ Data Catalog（元数据）

👉 本质：

* 表结构
* 分区信息

👉 类似：
👉 Hive Metastore

---

## 🔥 3️⃣ Job（执行 ETL）

👉 功能：

* 清洗数据
* 转格式（JSON → Parquet🔥）
* 聚合

---

# ⚔️ 四、Glue vs EMR（深度对比🔥）

| 项目   | Glue | EMR   |
| ---- | ---- | ----- |
| 管理   | 全托管  | 自己管   |
| 灵活性  | 低    | 高     |
| 使用场景 | ETL  | 大规模计算 |

---

👉 面试一句话：

> Glue is easier, EMR is more flexible.

---

# 🚨 五、面试高频深度问题（关键🔥）

---

## ❓ Q1：How does Glue handle schema evolution?

👉 答：

> Glue can automatically update schema using crawlers.

---

## ❓ Q2：How to optimize Glue jobs?

👉 答：

* increase DPU
* use partition
* convert to Parquet

---

## ❓ Q3：Glue job slow怎么办？

👉 答：

* 调高 DPU
* 优化数据格式
* 减少小文件

---

## ❓ Q4：Glue vs Lambda？

👉 答：

| Glue    | Lambda |
| ------- | ------ |
| 大数据 ETL | 小任务    |
| 长时间     | 短时间    |

---

# 🚀 六、实战（面试加分🔥）

---

👉 标准 pipeline：

```text
Kinesis → S3 → Glue → Athena
```

---

👉 你要这样说：

> I used Glue jobs to transform raw data into partitioned Parquet format, improving query performance in Athena.

---

# 🔥 七、最重要总结（秒杀面试）

---

👉 三句话：

> Glue = Spark ETL
> Crawler = schema
> DPU = compute

---

# 🚀 下一步（非常关键🔥）

你现在已经进入：

👉 **高级 Data Engineer 面试区🔥**

接下来建议👇

---

## 🔥 必练：

👉 **Design a scalable data pipeline（系统设计）**
👉 或 **Mock 面试**

---

直接说👇
👉 **“设计题” 或 “mock interview”**



<img width="472" height="243" alt="image" src="https://github.com/user-attachments/assets/ef6f5490-4a2f-41a3-b0e1-35803a869916" />


这页是 **Glue Costs（成本模型）🔥**
👉 考试很爱问“哪个更便宜 / 如何省钱”

---

# 🧠 一、核心一句话（必须背🔥）

👉
**Glue = 按使用付费（Pay-as-you-go）**

---

# 🧠 二、Glue 怎么收费？

---

## 🔥 1️⃣ 按计算资源（最重要）

👉 单位：

👉 **DPU（Data Processing Unit）**

---

### 📌 DPU 是什么？

👉 可以理解成：

```text
CPU + Memory + Compute
```

---

### 📌 收费方式

👉

```text
费用 = DPU × 时间
```

👉 举例：

* 2 DPU × 10分钟
  = 收费

---

---

## 🔥 2️⃣ Glue Job（ETL任务）

👉 每次跑 Job 才收费：

* 不运行 → 不花钱 ✔️

---

## 🔥 3️⃣ Glue Crawler（也收费）

👉 扫描数据时收费

---

## 🔥 4️⃣ Data Catalog（有免费额度）

👉 存 metadata：

* 少量免费
* 超过才收费

---

# 🧠 三、考试最重要理解（核心🔥）

---

## 🔥 Glue vs EMR（必考）

---

| Glue       | EMR    |
| ---------- | ------ |
| 按使用付费 ✔️   | 一直收费 ❌ |
| Serverless | 要开集群   |
| 简单         | 复杂     |

---

👉 👉 默认结论：

```text
想省钱 + 简单 → Glue
```

---

# 🧠 四、如何优化 Glue 成本？（考试加分🔥）

---

## 🔥 1️⃣ 减少运行时间

👉 优化 ETL：

* 用 Parquet
* 用 Partition

---

## 🔥 2️⃣ 减少 DPU 使用

👉 小任务 → 少 DPU

---

## 🔥 3️⃣ 避免不必要 Job

👉 不要频繁触发

---

## 🔥 4️⃣ 用 Trigger / Schedule

👉 控制运行频率

---

# 🧠 五、考试秒选场景（最重要🔥）

---

## ✅ 场景1

👉 “cost-effective ETL”

✔️ Glue

---

## ✅ 场景2

👉 “不用一直运行资源”

✔️ Glue（Serverless）

---

## ❌ 场景3（陷阱）

👉 “长时间运行大规模计算”

✔️ EMR 更合适

---

# 🧠 六、经典陷阱（必错🔥）

---

## ❌ 错误1

👉 Glue 一直收费 ❌

👉 正确：
✔️ 只有运行时收费

---

## ❌ 错误2

👉 忽略 DPU

👉 👉 成本核心就是：

✔️ DPU × 时间

---

# 🧠 七、面试标准回答（直接背🔥）

👉

> “AWS Glue pricing is based on DPU usage and job duration, making it cost-effective since you only pay when the job runs.”

---

# 🎯 八、终极速记（考前🔥）

```text
Glue收费 = DPU × 时间
不运行 = 不收费
省钱 = Glue（vs EMR）
```

---

# 🚀 下一步（最后核心🔥）

你现在已经掌握：

* S3 ✅
* Glue（含成本） ✅
* Athena（含优化） ✅

👉 最后一块👇

👉 **Redshift（数据仓库 + BI + 高频考点🔥）**

👉 学完这个，你这门基本稳了 🚀

<img width="805" height="388" alt="image" src="https://github.com/user-attachments/assets/9f4646fa-c319-42da-99e4-fdcaeeb9d498" />

这页是 **Glue 成本“细节版（考试会考数字 + 默认值🔥）”**
👉 我帮你整理成：**能做题 + 能算钱 + 能记住**

---

# 🧠 一、核心一句话（必须背🔥）

```text
Glue成本 = DPU × 时间（按秒计费，有最低时间）
```

---

# 🧠 二、ETL Job 收费规则（考试重点🔥）

---

## 🔥 1️⃣ 按 DPU × 时间

👉 举例：

```text
10 DPU × 10分钟 = 收费
```

---

## 🔥 2️⃣ 按秒计费（但有最低时间）

👉 重点来了：

* 老版本：最少 10分钟 ❌
* 新版本（Glue 2.0+）：最少 **1分钟 ✔️**

👉 👉 考试点：

```text
Glue 2.0+ = 更省钱
```

---

# 🧠 三、不同 Job 的 DPU（高频考点🔥）

---

## 🔵 1️⃣ Spark Job（最常见🔥）

👉 默认：

```text
Default: 10 DPU
Minimum: 2 DPU
```

👉 👉 ⚠️ 重点：

👉 默认很贵！！

---

## 🔵 2️⃣ Spark Streaming

```text
Default: 2 DPU
```

---

## 🔵 3️⃣ Ray Job（AI/ML）

```text
Default: 6 M-DPU（高内存）
```

---

## 🔵 4️⃣ Python Shell（最便宜🔥）

```text
Default: 0.0625 DPU
```

👉 👉 超级关键：

👉 小任务首选！

---

# 🧠 四、价格（考试知道大概就行）

---

```text
≈ $0.44 / DPU-hour
```

👉 不需要死记
👉 只要知道：

👉 **DPU 越多 → 越贵**

---

# 🧠 五、考试最重要理解（核心🔥）

---

## 🔥 默认很坑！

👉 Spark Job 默认：

```text
10 DPU ❗
```

👉 👉 很容易浪费钱

---

## 🔥 小任务不要用 Spark

👉 应该用：

✔️ Python Shell（0.0625 DPU）

---

# 🧠 六、考试秒选场景（最重要🔥）

---

## ✅ 场景1

👉 “cost optimization”

✔️ 减少 DPU
✔️ 用 Python Shell

---

## ✅ 场景2

👉 “小数据 ETL”

✔️ Python Shell

---

## ✅ 场景3

👉 “Glue 太贵”

✔️ 减少 DPU / 优化 job

---

## ❌ 场景4（陷阱）

👉 默认配置最优 ❌

👉 错：

👉 默认 10 DPU 很贵

---

# 🧠 七、经典陷阱（必错🔥）

---

## ❌ 错误1

👉 不知道默认 10 DPU

👉 👉 很多人忽略！

---

## ❌ 错误2

👉 小任务用 Spark

👉 👉 浪费钱！

---

## ❌ 错误3

👉 忽略最低计费时间

👉 👉 即使很短也要收费

---

# 🧠 八、面试标准回答（直接背🔥）

👉

> “Glue pricing is based on DPU usage and duration. To optimize cost, we can reduce DPU allocation or use lightweight jobs like Python Shell for smaller workloads.”

---

# 🎯 九、终极速记（考前🔥）

```text
默认 10 DPU（贵❗）
小任务 → Python Shell
收费 = DPU × 时间
```

---

# 🚀 你现在已经接近通关🔥

你已经掌握：

* S3 ✅
* Glue（含成本） ✅
* Athena（含优化） ✅
* ORC / Parquet ✅

👉 最后一块👇

👉 **Redshift（数据仓库 + BI + 高频压轴🔥）**

👉 学完这个，你这门基本稳了 🚀



<img width="814" height="411" alt="image" src="https://github.com/user-attachments/assets/bd6f4b08-04f1-4017-90eb-b649004ce0f2" />


这页是 **Glue 成本（Glue Costs）**，面试很喜欢问👉“钱怎么算、怎么优化”🔥
我给你做成 **中英文双语 + 能上场回答版**

---

# 💰 一句话核心（先记住）

👉 **EN：** Glue is billed based on compute (DPUs) and metadata storage (Data Catalog).
👉 **中：** Glue 的费用主要来自：计算资源（DPU）+ 元数据存储（Catalog）

---

# 1️⃣ Crawlers 成本（中英文🔥）

---

## ❓ Q1: How are Glue Crawlers priced?

👉 **EN：**
Glue Crawlers are billed based on the number of DPUs used and execution time. Billing is per second with a 10-minute minimum.

👉 **中：**
Glue Crawler 按 DPU 数量和运行时间收费，按秒计费，但**最少按 10 分钟算**。

---

## 🧠 怎么理解？

```text
运行 3 分钟 → 按 10 分钟收费 ❗
运行 20 分钟 → 按 20 分钟收费
```

---

## ⚠️ 面试加分点

👉
**EN：** Even short jobs incur a minimum cost due to the 10-minute billing window.
👉
**中：** 即使任务很短，也会有最低 10 分钟的费用。

---

# 2️⃣ DPU 是什么（重点🔥）

---

## ❓ Q2: What is a DPU?

👉 **EN：**
A DPU (Data Processing Unit) is a unit of compute in AWS Glue. One DPU provides 4 vCPUs and 16 GB of memory.

👉 **中：**
DPU 是 Glue 的计算单位，一个 DPU 提供 **4 个 CPU + 16GB 内存**。

---

## 🧠 类比理解

👉 就像：

```text
EC2 instance size
```

👉 DPU = Glue 的“机器规格”

---

## ❗ 面试关键点

👉
**EN：** More DPUs = faster execution but higher cost.
👉
**中：** DPU 越多 → 跑得越快，但也越贵

---

# 3️⃣ Data Catalog 成本（中英文🔥）

---

## ❓ Q3: How is Glue Data Catalog priced?

👉 **EN：**
The first 1 million metadata objects are free. After that, it costs $1 per 100,000 objects per month.

👉 **中：**
前 100 万个元数据对象免费，超过后每 10 万个收费 $1 / 月。

---

## 🧠 什么是 “object”？

👉 指的是：

* 表（table）
* 分区（partition）
* 数据库（database）

---

## 举例：

```text
1,200,000 objects
```

👉 超出：

```text
200,000
```

👉 费用：

```text
$2 / 月
```

---

# 4️⃣ 面试最爱问（优化成本🔥）

---

## ❓ Q4: How do you reduce Glue cost?

---

### 👉 答案（中英文双语🔥）

---

### ✅ 1. 减少 DPU

👉 **EN：** Use fewer DPUs when possible.
👉 **中：** 合理减少 DPU 数量

---

### ✅ 2. 控制运行时间

👉 **EN：** Optimize job execution time.
👉 **中：** 优化任务执行时间（避免长时间运行）

---

### ✅ 3. 避免频繁 crawler

👉 **EN：** Avoid running crawlers too frequently.
👉 **中：** 不要频繁跑 Crawler（很浪费钱）

---

### ✅ 4. 用 partition

👉 **EN：** Use partitioning to reduce data scanned.
👉 **中：** 使用分区减少处理数据量

---

### ✅ 5. 用 Parquet

👉 **EN：** Use columnar formats like Parquet.
👉 **中：** 使用列式存储（Parquet）减少计算量

---

# 5️⃣ 实战场景（非常加分🔥）

---

## 🎯 场景：你设计一个 pipeline

```text
每天跑 crawler ❌（贵）
```

👉 优化：

```text
每周跑一次 crawler ✅
```

---

## 🎯 场景：ETL job

```text
10 DPU 跑 2 分钟
```

👉 其实：

```text
可以 2 DPU 跑 5 分钟（更便宜🔥）
```

---

# 6️⃣ 面试完整回答（直接背🔥）

---

## ❓ Q: How is AWS Glue priced?

👉

**EN：**
AWS Glue is priced based on compute resources (DPUs) and metadata storage. Crawlers and jobs are billed per second with a 10-minute minimum, and the Data Catalog is free up to 1 million objects.

👉

**中：**
Glue 的费用包括计算资源（DPU）和元数据存储。Crawler 和 Job 按秒计费，但有 10 分钟最低费用，Data Catalog 前 100 万对象免费。

---

# 7️⃣ 一句话记忆

👉 **Glue = DPU（算力钱） + Catalog（元数据钱）**

---

# 🚀 下一步（你现在已经进入“面试强区🔥”）

你已经覆盖：

* S3 ✅
* Glue ✅
* Athena ✅
* Cost ✅

👉 下一步建议：

### 🔥 高频问题

👉 **Athena 成本 vs Glue 成本 vs Redshift 成本**

或者：

### 🔥 系统设计

👉 设计一个：

* TB级日志分析系统（Amazon常考）

---

直接说👇
👉 **「成本对比」 或 「系统设计」** 我带你继续冲🔥

<img width="802" height="313" alt="image" src="https://github.com/user-attachments/assets/8e114f86-8566-465f-b63e-4bc990c959c2" />

很好🔥 这一页是 **Glue 成本（Glue Costs）— 面试中高级考点**

---

# 🧠 一句话核心（面试必背）

> AWS Glue cost = 按 DPU × 时间收费

---

# 💰 一、Glue 是怎么收费的？（本质🔥）

👉 核心公式：

```text
成本 = 使用的 DPU 数量 × 运行时间
```

---

👉 你要记住：

* DPU 越多 → 越快 → 💰 越贵
* 运行时间越长 → 💰 越贵

---

👉 面试一句话：

> Glue pricing is based on DPU usage and job duration.

---

# ⚡ 二、这一页重点：Notebook / Interactive Session

---

## 🧠 是什么？

👉 Glue 不只是跑 job，还可以：

* 写 Notebook（类似 Jupyter）
* 实时开发 ETL

👉 类似：
👉 Data Engineer 的“开发环境”

---

# ⚙️ 三、收费细节（逐条讲清楚🔥）

---

## 🔥 1️⃣ 按 session 时间收费

👉 只要 session 开着：

👉 就在计费 💰

---

👉 即使你不运行代码 ❗

---

## 🔥 2️⃣ 按 DPU 数量收费

👉 默认：

```text
5 DPUs（默认）
最少 2 DPUs
```

---

👉 面试点：

> More DPUs = faster execution but higher cost.

---

## 🔥 3️⃣ 最小计费单位

👉 1 分钟起算

👉 即使你只用 10 秒：

👉 也按 1 分钟算

---

## 🔥 4️⃣ Idle Timeout（很关键🔥）

👉 可以设置：

```text
如果不用 → 自动关闭
```

👉 否则：

👉 💥 白白烧钱

---

# 🚨 四、面试常见坑（必须会🔥）

---

## ❌ 忘记关 session

👉 结果：

* 一直计费 💰💰💰

---

## ❌ DPU 设置过高

👉 结果：

* 成本爆炸

---

## ❌ 长时间 idle

👉 结果：

* 浪费钱

---

# 🎯 五、面试高频问题

---

## ❓ Q1：How does Glue pricing work?

👉 答：

> It is based on DPU usage and execution time.

---

## ❓ Q2：How do you reduce Glue cost?

👉 标准答案🔥：

* reduce DPU
* optimize job
* avoid idle sessions

---

## ❓ Q3：What is DPU?

👉 答：

> A unit of compute capacity in Glue.

---

## ❓ Q4：How to avoid unnecessary cost?

👉 答：

* set idle timeout
* stop sessions
* optimize code

---

# 🚀 六、实战怎么说（面试加分🔥）

---

👉 英文：

> I optimized Glue cost by reducing DPU usage, optimizing job execution time, and configuring idle timeouts for interactive sessions.

---

👉 中文：

> 我通过降低 DPU、优化任务时间，以及设置空闲超时来降低 Glue 成本。

---

# 🔥 七、最重要总结（秒杀面试）

---

👉 三句话：

> Pay per DPU
> Pay per time
> Avoid idle

---

# 🚀 下一步（关键🔥）

你现在已经掌握：

👉 S3 + Glue + Athena + 成本优化（完整体系🔥）

---

## 🔥 建议你下一步：

👉 **Design Data Pipeline（Amazon最爱）**
👉 或 **Mock 面试（真实问答）**

---

直接说👇
👉 **“设计题” 或 “mock interview”**



<img width="813" height="437" alt="image" src="https://github.com/user-attachments/assets/f709473f-37b5-4f68-8011-13e3baf29f38" />

很好，这个问题**非常关键🔥（面试必问）**

---

# 🧠 一句话核心（面试必背）

> DPU = Data Processing Unit，是 AWS Glue 的计算资源单位

---

# ⚡ 一、DPU 是什么？（通俗理解🔥）

👉 你可以把 DPU 理解成：

> 👉 “一台小计算机器（CPU + 内存）”

---

👉 官方定义（简单版）：

* 1 DPU ≈

  * 4 vCPU
  * 16 GB 内存

---

👉 面试一句话：

> A DPU is a unit of compute capacity used by Glue jobs.

---

# 🧭 二、为什么需要 DPU？（本质🔥）

👉 Glue 本质是跑 **Spark 作业**

👉 Spark 需要计算资源：

* CPU（算数据）
* 内存（存数据）

👉 DPU = AWS 帮你打包好的计算资源

---

# ⚙️ 三、DPU 在实际中怎么用？

---

## 👉 例子：

```text
你设置：
10 DPU
```

👉 意味着：

* 更多 CPU
* 更多内存
* 更快处理数据 🚀
* 💰 更贵

---

# 💰 四、DPU 和成本关系（重点🔥）

---

👉 公式：

```text
成本 = DPU × 时间
```

---

👉 举例：

| DPU    | 时间   | 成本         |
| ------ | ---- | ---------- |
| 2 DPU  | 10分钟 | 💰         |
| 10 DPU | 10分钟 | 💰💰💰💰💰 |

---

👉 面试一句话：

> More DPUs improve performance but increase cost.

---

# ⚔️ 五、什么时候加 DPU？（面试会问🔥）

---

## ✅ 数据量大

👉 比如：

* TB 级数据

---

## ✅ Job 很慢

👉 提高 DPU 可以加速

---

## ❌ 小数据不需要

👉 否则浪费钱

---

# 🚨 六、面试常见坑

---

## ❌ 盲目加 DPU

👉 问题：

* 成本爆炸

---

## ❌ 不优化代码

👉 即使加 DPU：

* 也可能慢

---

# 🎯 七、面试高频问法

---

## ❓ Q1：What is DPU?

👉 答：

> A unit of compute resource in Glue consisting of CPU and memory.

---

## ❓ Q2：How to optimize Glue performance?

👉 答：

* increase DPU
* optimize Spark job
* reduce data size

---

## ❓ Q3：How to reduce cost?

👉 答：

* reduce DPU
* reduce execution time

---

# 🚀 八、面试加分表达（直接用🔥）

---

👉 英文：

> I tuned the number of DPUs to balance performance and cost.

---

👉 中文：

> 我通过调整 DPU 数量，在性能和成本之间做平衡。

---

# 🔥 九、最重要总结（记住这3句）

---

> DPU = 计算资源
> 多 DPU = 更快
> 多 DPU = 更贵

---

# 🚀 下一步（关键🔥）

你现在已经理解：

👉 Glue 的底层计算模型（非常加分）

---

如果你想更强👇

👉 我可以帮你讲：

* **Spark 在 Glue 里怎么跑（深度🔥）**
* 或来一轮 **Mock 面试**

---

直接说👇
👉 **“Spark” 或 “mock interview”**

很好，这页是在教你 **“如何算 Glue 成本”（考试会直接考计算🔥）**
👉 我帮你拆成：**公式 + 例子 + 秒算技巧**

---

# 🧠 一、核心公式（必须背🔥）

```text
Glue Cost = DPU × 时间（小时） × 单价
```

👉 单价：

```text
≈ $0.44 / DPU-hour
```

---

# 🧠 二、第一个例子（ETL Job）

---

## 📌 题目条件

* Spark Job
* 运行 15 分钟
* 使用 6 DPU
* 单价 $0.44

---

## 🔥 步骤拆解

---

### 1️⃣ 时间转小时

```text
15 分钟 = 1/4 小时
```

---

### 2️⃣ 套公式

```text
6 × 1/4 × 0.44
```

---

### 3️⃣ 计算

```text
6 × 0.25 = 1.5
1.5 × 0.44 = 0.66
```

---

## ✅ 最终答案

```text
$0.66
```

---

# 🧠 三、第二个例子（Interactive Session）

---

## 📌 条件

* 5 DPU
* 运行 24 分钟
* 单价 $0.44

---

## 🔥 步骤

---

### 1️⃣ 转时间

```text
24 分钟 = 2/5 小时
```

---

### 2️⃣ 套公式

```text
5 × 2/5 × 0.44
```

---

### 3️⃣ 计算

```text
5 × 0.4 = 2
2 × 0.44 = 0.88
```

---

## ✅ 最终答案

```text
$0.88
```

---

# 🧠 四、考试秒算技巧（非常重要🔥）

---

## 🔥 技巧1：分钟 → 小时

| 分钟 | 小时   |
| -- | ---- |
| 15 | 0.25 |
| 30 | 0.5  |
| 45 | 0.75 |
| 24 | 0.4  |

---

## 🔥 技巧2：先乘 DPU × 时间

👉 再乘价格

---

## 🔥 技巧3：看到 0.44

👉 心里直接：

```text
≈ 0.5（快速估算）
```

---

# 🧠 五、考试套路（必考🔥）

---

## ❓常见题型

👉 给你：

* DPU
* 时间
* 单价

👉 问：

👉 cost = ?

---

## ❓隐藏考点

👉 时间单位转换（最容易错❗）

---

# 🧠 六、经典陷阱（必错🔥）

---

## ❌ 错误1

👉 不换算时间

👉 直接用分钟 ❌

---

## ❌ 错误2

👉 忘记 DPU

👉 只算时间 ❌

---

## ❌ 错误3

👉 忽略最低计费时间

👉 很短也要收费

---

# 🧠 七、面试一句话（直接背🔥）

👉

> “Glue cost is calculated based on DPU usage and job duration, typically using the formula DPU × time × price per DPU-hour.”

---

# 🎯 八、终极速记（考前🔥）

```text
成本 = DPU × 时间 × 单价
关键 = 分钟 → 小时
```

---

# 🚀 你已经到最后一关🔥

你现在掌握：

* S3 ✅
* Glue（含成本计算） ✅
* Athena（含优化） ✅
* ORC / Parquet ✅

👉 最后一块👇

👉 **Redshift（数据仓库 + BI + 高频压轴🔥）**

👉 学完这个 = AWS Data Engineer 全通 🚀

