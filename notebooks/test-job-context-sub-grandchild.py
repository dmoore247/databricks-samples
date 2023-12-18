# Databricks notebook source
# MAGIC %md # Test Job Context
# MAGIC Grand child notebook

# COMMAND ----------

# MAGIC %pip install --quiet databricks-sdk==0.13.0 mlflow==2.9.2
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

import json

j = json.loads(dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson())
json.dumps(j)

# COMMAND ----------

dbutils.widgets.text('job_id', '', label='job_id')
dbutils.widgets.text('job_run_id', '', label='job_run_id')
dbutils.widgets.text('task_run_id', '', label='task_run_id')
parent_job_id = dbutils.widgets.get("job_id")
parent_job_run_id = dbutils.widgets.get("job_run_id")
parent_task_run_id = dbutils.widgets.get("task_run_id")

parent_job_id, parent_job_run_id, parent_task_run_id

# COMMAND ----------

from src.job_provenance.job_context import get_job_context

context = get_job_context(dbutils)
context

# COMMAND ----------

import mlflow

mlflow.set_experiment("/Repos/douglas.moore@databricks.com/databricks-samples/notebooks/test-job-context")
with mlflow.start_run():
    mlflow.log_param('notebook', 'child')
    mlflow.log_param('sparkVersion', spark.conf.get('spark.databricks.clusterUsageTags.sparkVersion', None))
    mlflow.log_param('clusterSource', spark.conf.get('spark.databricks.clusterSource', None))
    mlflow.log_metric('context_length', len(context))
    mlflow.log_dict(context, "context.json")

# COMMAND ----------
