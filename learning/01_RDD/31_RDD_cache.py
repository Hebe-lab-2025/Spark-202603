# coding:utf8
import time

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd1 = sc.textFile("../../data/input/words.txt")
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