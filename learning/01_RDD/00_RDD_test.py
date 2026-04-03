from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("test").getOrCreate()

data = [1, 2, 3, 4]
rdd = spark.sparkContext.parallelize(data)
print(rdd.collect())

input("Press Enter to exit...")