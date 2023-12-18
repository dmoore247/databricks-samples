# Databricks notebook source
# MAGIC %md # Test Job Context

# COMMAND ----------

# MAGIC %pip install --quiet databricks-sdk==0.13.0 mlflow==2.9.2
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

import json

j = json.loads(dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson())
json.dumps(j)

# COMMAND ----------

from src.job_provenance.job_context import get_job_context

context = get_job_context(dbutils)
context

# COMMAND ----------

import mlflow

print(mlflow.version.VERSION)

mlflow.set_experiment("/Repos/douglas.moore@databricks.com/databricks-samples/notebooks/test-job-context")
with mlflow.start_run():
    mlflow.log_param('notebook', 'parent')
    mlflow.log_param('sparkVersion', spark.conf.get('spark.databricks.clusterUsageTags.sparkVersion', None))
    mlflow.log_param('clusterSource', spark.conf.get('spark.databricks.clusterSource', None))
    mlflow.log_metric('context_length', len(context))
    mlflow.log_dict(context, "context.json")

# COMMAND ----------

dbutils.notebook.run('./test-job-context-sub', timeout_seconds=300, arguments=context)
