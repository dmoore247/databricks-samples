# Databricks notebook source
# MAGIC %md # Test Job Context
# MAGIC Child notebook

# COMMAND ----------

# MAGIC %pip install --quiet databricks-sdk==0.13.0 mlflow
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

from job_context import get_job_context
context = get_job_context(spark, dbutils)
context

# COMMAND ----------

import mlflow

with mlflow.start_run(experiment_id="23900c21a2054ab3982fb13dc326122e"):
    mlflow.log_param('notebook','child')
    mlflow.log_param('sparkVersion', spark.conf.get('spark.databricks.clusterUsageTags.sparkVersion', None))
    mlflow.log_param('clusterSource',spark.conf.get('spark.databricks.clusterSource',None))
    mlflow.log_metric('context_length',len(context))
    mlflow.log_dict(context, "context.json")
