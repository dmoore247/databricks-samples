# Databricks notebook source
# MAGIC %md
# MAGIC We are using the below command to find the Job Run ID.
# MAGIC notebook_info = json.loads(dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson())
# MAGIC print(notebook_info)
# MAGIC
# MAGIC We identified sometime, we are seeing the all 3 tags for same job one run-
# MAGIC
# MAGIC * “multitaskParentRunId”
# MAGIC * “jobRunId”
# MAGIC * “runId”
# MAGIC When we run the job next time without job definition change we found only 2 tags–
# MAGIC
# MAGIC * “jobRunId”
# MAGIC * “runId”
# MAGIC When we run the job next time without job definition change we found only 1 tag–
# MAGIC
# MAGIC * “runId”
# MAGIC
# MAGIC Its very tricky, our goal is to find the parent job url. As job runs the framework code main notebook which interns call the child notebooks in thread pooling. We want to log the parent job url id in our custom logging table.

# COMMAND ----------

# MAGIC %pip install --quiet databricks-sdk==0.13.0
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

import json

# COMMAND ----------

# MAGIC %md ## `.toJson()`

# COMMAND ----------

try:
    dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson()
except Exception as e:
    print(e)

# COMMAND ----------

# MAGIC %md ## `.safeToJson()`

# COMMAND ----------

import json
try:
    safe_tags = json.loads(dbutils.notebook.entry_point.getDbutils().notebook().getContext().safeToJson())
    print(safe_tags)
except Exception as e:
    print(e)

# COMMAND ----------

# MAGIC %md ## databricks-sdk

# COMMAND ----------

from databricks.sdk import WorkspaceClient

ws = WorkspaceClient()
dbutils = ws.dbutils

# COMMAND ----------

import json
try:
    safe_tags = json.loads(dbutils.notebook.entry_point.getDbutils().notebook().getContext().safeToJson())
    print(safe_tags)
except Exception as e:
    print(e)

# COMMAND ----------

# MAGIC %md ## spark config

# COMMAND ----------

# MAGIC %sql set

# COMMAND ----------

tags = json.loads(spark.conf.get('spark.databricks.clusterUsageTags.clusterAllTags'))
tags

# COMMAND ----------

clusterName = spark.conf.get('spark.databricks.clusterUsageTags.clusterName', None)
job_id = None
run_id = None
if 'job' in clusterName and 'run' in clusterName:
    job_id = clusterName.split('-')[1]
    run_id = clusterName.split('-')[3]
print(clusterName, job_id, run_id)

# COMMAND ----------

# MAGIC %md ## python repl context

# COMMAND ----------

from dbruntime.databricks_repl_context import get_context
ctx = get_context()
if ctx:
    print(f"{ctx.__dict__}")

# COMMAND ----------


