# coding:utf8
import os
import sys
import subprocess

os.environ["JAVA_HOME"] = "/Users/yonggan/Library/Java/JavaVirtualMachines/corretto-1.8.0_442/Contents/Home"
os.environ["SPARK_HOME"] = "/Users/yonggan/opt/spark-3.2.0-bin-hadoop3.2"
os.environ["PYSPARK_PYTHON"] = "/Users/yonggan/anaconda3/envs/spark38/bin/python"
os.environ["PATH"] = (
    "/Users/yonggan/Library/Java/JavaVirtualMachines/corretto-1.8.0_442/Contents/Home/bin:"
    "/Users/yonggan/opt/spark-3.2.0-bin-hadoop3.2/bin:"
    "/usr/bin:/bin:/usr/sbin:/sbin"
)

print("PYTHON:", sys.executable)
print("JAVA_HOME from env:", os.environ.get("JAVA_HOME"))
print("SPARK_HOME from env:", os.environ.get("SPARK_HOME"))
print("PYSPARK_PYTHON from env:", os.environ.get("PYSPARK_PYTHON"))

out = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT)
print("java -version:\n", out.decode())

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    # conf = SparkConf().setAppName("test").setMaster("local[*]")
    conf = SparkConf().setAppName("test")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([1, 2, 3, 4, 5])
    print(rdd.collect())