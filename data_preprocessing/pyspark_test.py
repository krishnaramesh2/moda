from pyspark import SparkContext
import json
import data_extractor_spark as dext

sc = SparkContext()

terms = json.load(open('../templates/terms.json','r'))

print "Successfully loaded json file into memory!!"

dd = [ {model:terms[model]} for model in terms.keys()]

rdd = sc.parallelize(dd)

mapped = rdd.map(lambda x: dext.extract_data(x))

print mapped.take(10)