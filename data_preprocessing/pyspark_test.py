from pyspark import SparkContext
import json

sc = SparkContext()

terms = json.load(open('terms.json','r'))

dd = [ {model:terms[model]} for model in terms.keys()]

rdd = sc.parallelize(dd)

mapped = rdd.map(lambda x: (x.keys())[0].upper())

print mapped