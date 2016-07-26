# -*- coding:utf8 -*-
from flask import render_template,json,request
from . import main

from pyspark import SparkContext,SparkConf
print ("Successfully imported Spark Modules")

from pyspark.mllib.classification import LogisticRegressionWithLBFGS, LogisticRegressionModel
print ("Successfully imported Mlib")

sc = SparkContext("local[2]", "data analyse")

# conf = SparkConf().setAppName("data analyse").setMaster('spark://10.0.2.15:7077')  
# sc = SparkContext(conf=conf)

ROOTDIR = '/home/gugugujiawei/projects/data'

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/cls/logistic')
def logistic():
    return render_template('reactjs/index.html')


# Load and parse the data
def parsePoint(line):
    values = [float(x) for x in line.split(' ')]
    return LabeledPoint(values[0], values[1:])

def logistic_model():

    global sc
    data = sc.textFile(ROOTDIR + "/sample_svm_data.txt")
    parsedData = data.map(parsePoint)
    # Build the model
    model = LogisticRegressionWithLBFGS.train(parsedData)

    # Evaluating the model on training data
    labelsAndPreds = parsedData.map(lambda p: (p.label, model.predict(p.features)))
    trainErr = labelsAndPreds.filter(lambda (v, p): v != p).count() / float(parsedData.count())
    print("Training Error = " + str(trainErr))    

@main.route('/cls/logistic/post',methods=['POST'])
def logistic_post():
    global sc
    print request.form['userName']
    print request.form['userEmail']

    data = sc.textFile(ROOTDIR + "/UserPurchaseHistory.csv").map(lambda line:
    line.split(",")).map(lambda record: (record[0], record[1], record[2]))
    numPurchases = data.count()
    print numPurchases

    # logistic_model()

    return json.dumps({'msg': 'test','success': True})