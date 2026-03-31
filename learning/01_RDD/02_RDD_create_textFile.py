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
    # print("hdfs_rdd 内容:", hdfs_rdd.collect())