# Databricks notebook source
from pyspark.context import SparkContext
sc = SparkContext(appName='a')
sc.emptyRDD().count()

# COMMAND ----------


