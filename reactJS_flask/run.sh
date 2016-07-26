#!/bin/bash
ROOT=$(dirname $0)
export SPARK_HOME="/usr/local/src/spark-1.6.1-bin-hadoop2.6/"
export PYTHONPATH="$ROOT/project/site-packages:$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.9-src.zip:$ROOT/python/lib/pyspark.zip"
python ./project/manage.py runserver -t 0.0.0.0
