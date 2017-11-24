from pyspark import SparkContext
import json
import data_extract_spark as extractor

sc = SparkContext(pyFiles = ["data_extract_spark.py" , "facebook_moda.py", "mongo_connector.py" ,"log.py", "conf.json", "pages.txt"])

terms = json.load(open("terms.json","r"))

dd = [ {model:terms[model]} for model in terms.keys()]

rdd = sc.parallelize(dd)

mapped = rdd.map(lambda x: extractor.extract_data(x))

print mapped.take(10)