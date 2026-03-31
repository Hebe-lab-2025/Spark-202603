下面直接给你 **PySpark 10 个最常见实验**，每个都带：

* 目的
* 完整命令
* 完整代码
* 预期现象
* 你该观察什么

我默认你现在已经有：

* Docker 三节点
* Spark Standalone 集群
* `node1` 是 Master
* `node2` / `node3` 是 Worker
* 可以进入 `node1`
* 可以运行：

```bash
docker exec -it node1 bash
source /root/.bashrc
cd /root/spark
bin/pyspark --master spark://node1:7077
```

---

# 实验 0：先进入 PySpark

每次做实验前，先执行：

```bash
docker exec -it node1 bash
source /root/.bashrc
cd /root/spark
bin/pyspark --master spark://node1:7077
```

进入后你会看到：

```python
>>>
```

后面的 Python 代码都在这里执行。

退出时：

```python
exit()
```

然后：

```bash
exit
```

---

# 实验 1：parallelize 创建 RDD

## 目的

理解：

* 本地集合怎么变成 RDD
* RDD 是分布式对象

## 代码

```python
rdd = sc.parallelize([1, 2, 3, 4, 5])
print(rdd)
print(rdd.collect())
```

## 预期现象

你会看到类似：

```python
ParallelCollectionRDD[0] at readRDDFromFile at PythonRDD.scala:...
[1, 2, 3, 4, 5]
```

## 你该理解什么

* `parallelize()`：本地集合 -> RDD
* `collect()`：RDD -> 本地 Python list

---

# 实验 2：看默认分区数

## 目的

理解：

* RDD 有分区
* 分区影响并行度

## 代码

```python
rdd = sc.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9])
print(rdd.getNumPartitions())
```

## 预期现象

你会得到一个数字，比如：

```python
2
```

或者别的数字。

## 你该理解什么

* `getNumPartitions()` = 当前 RDD 的分区数
* 分区数通常和默认并行度有关

---

# 实验 3：手动指定分区数

## 目的

理解：

* 可以自己指定分区数
* Task 数量通常和分区有关

## 代码

```python
rdd = sc.parallelize([1, 2, 3, 4, 5, 6], 3)
print(rdd.getNumPartitions())
print(rdd.collect())
```

## 预期现象

```python
3
[1, 2, 3, 4, 5, 6]
```

## 你该理解什么

* 第二个参数 `3` 表示 3 个分区
* 后续执行时通常会对应多个 Task

---

# 实验 4：用 glom 看每个分区里有什么

## 目的

理解：

* 分区不是抽象概念
* 每个分区里真有一部分数据

## 代码

```python
rdd = sc.parallelize([1, 2, 3, 4, 5, 6], 3)
print(rdd.glom().collect())
```

## 预期现象

类似：

```python
[[1, 2], [3, 4], [5, 6]]
```

也可能分布略有不同。

## 你该理解什么

* `glom()`：把每个分区里的元素收成一个列表
* 结果是“按分区查看数据”

---

# 实验 5：map 转换

## 目的

理解：

* `map` 是一对一转换
* transformation 是惰性执行

## 代码

```python
rdd = sc.parallelize([1, 2, 3, 4, 5], 2)
rdd2 = rdd.map(lambda x: x * 10)

print(rdd2)
print(rdd2.collect())
```

## 预期现象

```python
PythonRDD...
[10, 20, 30, 40, 50]
```

## 你该理解什么

* `map()` 不会立刻执行真正计算
* 只有 `collect()` 这种 action 出现时，才触发执行

---

# 实验 6：filter 过滤

## 目的

理解：

* 过滤操作怎么做
* transformation + action 的配合

## 代码

```python
rdd = sc.parallelize([1, 2, 3, 4, 5, 6], 2)
rdd2 = rdd.filter(lambda x: x % 2 == 0)
print(rdd2.collect())
```

## 预期现象

```python
[2, 4, 6]
```

## 你该理解什么

* `filter()` 保留满足条件的数据
* 这是 transformation

---

# 实验 7：flatMap 和 map 的区别

## 目的

理解：

* `map`：一条进去，一条出来
* `flatMap`：一条进去，多条出来，再打平

## 代码 1：map

```python
rdd = sc.parallelize(["hello spark", "hello docker"], 2)
result = rdd.map(lambda line: line.split(" "))
print(result.collect())
```

## 预期现象

```python
[['hello', 'spark'], ['hello', 'docker']]
```

## 代码 2：flatMap

```python
rdd = sc.parallelize(["hello spark", "hello docker"], 2)
result = rdd.flatMap(lambda line: line.split(" "))
print(result.collect())
```

## 预期现象

```python
['hello', 'spark', 'hello', 'docker']
```

## 你该理解什么

* `map` 保留嵌套结构
* `flatMap` 会打平

---

# 实验 8：reduceByKey 做 WordCount

## 目的

理解：

* WordCount 最经典
* `reduceByKey` 会引入 Shuffle
* 会产生多个 Stage

## 代码

```python
rdd = sc.parallelize(
    ["hello spark", "hello docker", "spark docker", "hello hello"],
    4
)

result = (
    rdd.flatMap(lambda line: line.split(" "))
       .map(lambda word: (word, 1))
       .reduceByKey(lambda a, b: a + b)
)

print(result.collect())
```

## 预期现象

类似：

```python
[('hello', 4), ('spark', 2), ('docker', 2)]
```

顺序可能不一样。

## 你该观察什么

* Master UI 上会出现一个应用
* 这个 Job 通常不止一个 Stage
* 因为 `reduceByKey` 发生了 Shuffle

## 你该理解什么

* `reduceByKey` 是面试高频
* 比 `groupByKey` 更推荐

---

# 实验 9：groupByKey 和 reduceByKey 对比

## 目的

理解：

* 两者都能做聚合
* `reduceByKey` 更高效

## 代码 1：groupByKey

```python
rdd = sc.parallelize(
    [("a", 1), ("a", 2), ("b", 1), ("b", 3)],
    2
)

result = rdd.groupByKey().mapValues(lambda values: list(values))
print(result.collect())
```

## 预期现象

```python
[('a', [1, 2]), ('b', [1, 3])]
```

## 代码 2：reduceByKey

```python
rdd = sc.parallelize(
    [("a", 1), ("a", 2), ("b", 1), ("b", 3)],
    2
)

result = rdd.reduceByKey(lambda a, b: a + b)
print(result.collect())
```

## 预期现象

```python
[('a', 3), ('b', 4)]
```

## 你该理解什么

* `groupByKey`：先把所有值聚一起
* `reduceByKey`：先本地聚合，再全局聚合
* 所以通常 `reduceByKey` 更省网络、更高效

---

# 实验 10：cache 缓存

## 目的

理解：

* RDD 默认不缓存
* 重复 action 会重复算
* `cache()` 可以减少重复计算

## 代码

```python
rdd = sc.parallelize([1, 2, 3, 4, 5], 2).map(lambda x: x * 10)

rdd.cache()

print(rdd.collect())
print(rdd.collect())
```

## 预期现象

两次都输出：

```python
[10, 20, 30, 40, 50]
```

## 你该观察什么

如果你后面能看 4040 / Storage 页面，会看到缓存信息。

## 你该理解什么

* 不加 cache：每次 action 都可能重新算
* 加 cache：第一次算完后缓存，后面复用

---

# 实验 11：distinct 去重

## 目的

理解：

* 去重也是常用操作
* 去重通常涉及 Shuffle

## 代码

```python
rdd = sc.parallelize([1, 2, 2, 3, 3, 3, 4, 4], 3)
print(rdd.distinct().collect())
```

## 预期现象

```python
[1, 2, 3, 4]
```

顺序可能不同。

## 你该理解什么

* `distinct()` 经常伴随重新分布数据
* 可能产生 Shuffle

---

# 实验 12：union 合并两个 RDD

## 目的

理解：

* 怎么把两个 RDD 合并
* union 不是去重

## 代码

```python
rdd1 = sc.parallelize([1, 2, 3], 2)
rdd2 = sc.parallelize([3, 4, 5], 2)

rdd3 = rdd1.union(rdd2)
print(rdd3.collect())
```

## 预期现象

```python
[1, 2, 3, 3, 4, 5]
```

## 你该理解什么

* `union()` 只是拼接
* 不会自动去重

---

# 实验 13：intersection 交集

## 目的

理解：

* 两个 RDD 的交集
* 常见集合操作

## 代码

```python
rdd1 = sc.parallelize([1, 2, 3, 4], 2)
rdd2 = sc.parallelize([3, 4, 5, 6], 2)

print(rdd1.intersection(rdd2).collect())
```

## 预期现象

```python
[3, 4]
```

## 你该理解什么

* 这是集合交集
* 一般也会涉及数据重分布

---

# 实验 14：sortBy 排序

## 目的

理解：

* 排序怎么做
* 排序通常涉及全局重分布

## 代码

```python
rdd = sc.parallelize([5, 1, 3, 2, 4], 2)
print(rdd.sortBy(lambda x: x).collect())
print(rdd.sortBy(lambda x: x, ascending=False).collect())
```

## 预期现象

```python
[1, 2, 3, 4, 5]
[5, 4, 3, 2, 1]
```

## 你该理解什么

* 排序通常成本较高
* 面试里常问是不是宽依赖 / 会不会 Shuffle

---

# 实验 15：repartition 重新分区

## 目的

理解：

* 可以增加或减少分区
* `repartition` 通常会 Shuffle

## 代码

```python
rdd = sc.parallelize([1, 2, 3, 4, 5, 6], 2)
print(rdd.getNumPartitions())

rdd2 = rdd.repartition(4)
print(rdd2.getNumPartitions())
print(rdd2.glom().collect())
```

## 预期现象

```python
2
4
...
```

每个分区的数据分布可能不固定。

## 你该理解什么

* `repartition()` 会重新洗牌分区
* 用来调整并行度

---

# 实验 16：coalesce 减少分区

## 目的

理解：

* `coalesce` 更适合减少分区
* 比 `repartition` 更轻一些

## 代码

```python
rdd = sc.parallelize([1, 2, 3, 4, 5, 6], 4)
print(rdd.getNumPartitions())

rdd2 = rdd.coalesce(2)
print(rdd2.getNumPartitions())
print(rdd2.glom().collect())
```

## 预期现象

```python
4
2
...
```

## 你该理解什么

* `coalesce()` 常用于减少分区
* 通常比 `repartition()` 更省

---

# 实验 17：多个 action 触发多个 Job

## 目的

理解：

* 一个 action 常常触发一个 Job
* 多个 action 通常对应多个 Job

## 代码

```python
rdd = sc.parallelize([1, 2, 3, 4, 5], 3)

print(rdd.map(lambda x: x + 1).collect())
print(rdd.map(lambda x: x * 2).collect())
print(rdd.filter(lambda x: x % 2 == 0).collect())
```

## 预期现象

```python
[2, 3, 4, 5, 6]
[2, 4, 6, 8, 10]
[2, 4]
```

## 你该观察什么

如果能看 4040 / Jobs 页面，会看到 3 个 Job。

## 你该理解什么

* `collect()` 是 action
* 每次 action 都可能形成一个新 Job

---

# 实验 18：用文本文件做 textFile

## 目的

理解：

* 真实场景更常见的是读文件
* 不是只用 `parallelize`

先退出 PySpark：

```python
exit()
```

然后在 node1 容器中执行：

```bash
mkdir -p /root/data
cat > /root/data/test.txt <<'EOF'
apple banana
banana orange
apple orange banana
EOF
```

再重新进入 PySpark：

```bash
cd /root/spark
bin/pyspark --master spark://node1:7077
```

执行：

```python
rdd = sc.textFile("file:///root/data/test.txt")
print(rdd.collect())
```

## 预期现象

```python
['apple banana', 'banana orange', 'apple orange banana']
```

---

# 实验 19：完整文件版 WordCount

## 目的

把前面的知识串起来。

## 代码

```python
rdd = sc.textFile("file:///root/data/test.txt", 4)

result = (
    rdd.flatMap(lambda line: line.split(" "))
       .map(lambda word: (word, 1))
       .reduceByKey(lambda a, b: a + b)
       .sortBy(lambda x: x[0])
)

print(result.collect())
```

## 预期现象

```python
[('apple', 2), ('banana', 3), ('orange', 2)]
```

## 你该理解什么

这就是最经典的 Spark 面试和教学案例。

---

# 实验 20：保存结果

## 目的

理解：

* Spark 不只是 collect 回 Driver
* 也可以把结果输出到文件系统

在 PySpark 里执行：

```python
result = sc.parallelize([("a", 1), ("b", 2), ("c", 3)], 2)
result.saveAsTextFile("file:///root/output_test")
```

然后退出 PySpark：

```python
exit()
```

在 node1 shell 里执行：

```bash
ls -R /root/output_test
cat /root/output_test/part-*
```

## 预期现象

你会看到：

```text
('a', 1)
('b', 2)
('c', 3)
```

## 你该理解什么

* Spark 输出通常是目录，不是单文件
* 每个分区可能对应一个 `part-*` 文件

---

# 一套最推荐的学习顺序

如果你不想一次做太多，最建议按这个顺序练：

## 第 1 组：基础

先做这 5 个：

```python
# 1
rdd = sc.parallelize([1,2,3,4,5])
rdd.collect()

# 2
rdd.getNumPartitions()

# 3
rdd = sc.parallelize([1,2,3,4,5,6], 3)
rdd.glom().collect()

# 4
rdd.map(lambda x: x * 10).collect()

# 5
rdd.filter(lambda x: x % 2 == 0).collect()
```

---

## 第 2 组：字符串和 WordCount

再做这 4 个：

```python
rdd = sc.parallelize(["hello spark", "hello docker"], 2)
rdd.map(lambda line: line.split(" ")).collect()

rdd.flatMap(lambda line: line.split(" ")).collect()

rdd = sc.parallelize(["hello spark", "hello docker", "spark hello"], 4)
rdd.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b).collect()

rdd.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).groupByKey().mapValues(lambda values: list(values)).collect()
```

---

## 第 3 组：性能和分区

最后做这 4 个：

```python
rdd = sc.parallelize([1,2,3,4,5], 2).map(lambda x: x * 10)
rdd.cache()
rdd.collect()
rdd.collect()

rdd = sc.parallelize([1,2,3,4,5,6], 2)
rdd.repartition(4).glom().collect()

rdd = sc.parallelize([1,2,3,4,5,6], 4)
rdd.coalesce(2).glom().collect()

sc.parallelize([5,1,3,2,4], 2).sortBy(lambda x: x).collect()
```

---

# 你最该背下来的结论

## 1

`parallelize`：本地集合 -> RDD

## 2

`collect`：RDD -> Driver，本地 list

## 3

`map`：一对一转换

## 4

`flatMap`：一对多并打平

## 5

`filter`：过滤

## 6

`reduceByKey`：聚合，更高效

## 7

`groupByKey`：能用，但通常不如 `reduceByKey`

## 8

`cache`：避免重复计算

## 9

`repartition`：重新分区，常伴随 Shuffle

## 10

`coalesce`：通常用来减少分区

---

# 最后一套“面试演示版”

如果面试官让你快速展示几个常见 API，你可以直接跑这一套：

```python
rdd = sc.parallelize(["hello spark", "hello docker", "spark cluster", "hello hello"], 4)

print(rdd.getNumPartitions())
print(rdd.glom().collect())

words = rdd.flatMap(lambda line: line.split(" "))
print(words.collect())

pairs = words.map(lambda word: (word, 1))
print(pairs.collect())

counts = pairs.reduceByKey(lambda a, b: a + b)
print(counts.collect())

counts.cache()
print(counts.collect())
print(counts.collect())
```

---

如果你愿意，我下一条直接给你：

**“这 20 个实验整理成一份 A4 速记版”** 或者
**“每个实验对应的 Job / Stage / Task 应该怎么看”**
