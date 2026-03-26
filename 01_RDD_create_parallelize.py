conf = SparkConf().setAppName("test").setMaster("local[*]")
sc = SparkContext(conf=conf)