# coding:utf8
import os
from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, "data", "input", "tiny_files")

    # 读取小文件文件夹
    rdd = sc.wholeTextFiles(input_path)
    print(rdd.map(lambda x: x[1]).collect())
