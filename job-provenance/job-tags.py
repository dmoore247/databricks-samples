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
import pprint

# COMMAND ----------

# MAGIC %md ## `.toJson()`

# COMMAND ----------

try:
    ctx_tojson = dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson()
    pprint.pprint(ctx_tojson)
except Exception as e:
    print(e)

# COMMAND ----------

# MAGIC %md ## `.safeToJson()`

# COMMAND ----------

import json
try:
    safe_tags = json.loads(dbutils.notebook.entry_point.getDbutils().notebook().getContext().safeToJson())
    pprint.pprint(safe_tags)
except Exception as e:
    print(e)

# COMMAND ----------

# MAGIC %md ## databricks-sdk

# COMMAND ----------

import json
try:
    from databricks.sdk import WorkspaceClient
    ws = WorkspaceClient()
    sdk_safe_tojson = json.loads(ws.dbutils.notebook.entry_point.getDbutils().notebook().getContext().safeToJson())
    pprint.pprint(sdk_safe_tojson)
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
    pprint.pprint(f"{ctx.__dict__}")

# COMMAND ----------

# MAGIC %md ## run sub-notebook

# COMMAND ----------

try:
    dbutils.notebook.run("./job-tags-sub", timeout_seconds=60)
except Exception as e:
    print(e)

# COMMAND ----------

# MAGIC %md ## unified

# COMMAND ----------

import json


def get_context() -> dict:
    version = 0
    ctx = None
    _ = spark.conf.get('spark.databricks.clusterUsageTags.sparkVersion', None)
    assert 'custom' not in _ and 'dlt' not in _

    major, minor = int(_.split('.')[0]), int(_.split('.')[1])
    version = (major, minor)

    if version <= (10,4):
        try:
            print('toJson')
            ctx = json.loads(dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson())
        except Exception as e:
            print('toJson fails', e)

    elif version <= (13,3):
        try:
            print('safeToJson')
            ctx = json.loads(dbutils.notebook.entry_point.getDbutils().notebook().getContext().safeToJson())
        except Exception as e:
            print('safeToJson fails', e)
    else:    
        try:
            print('databricks_repl_context')
            from dbruntime.databricks_repl_context import get_context
            _ = get_context()
            if _:
                ctx = get_context().__dict__
        except Exception as e:
            print('databricks_repl_context fails', e)
    
    r_ctx = {}
    for x in ['commandRunId','notebookPath','notebook_path',
              'notebookId','notebook_id',
              'workspaceId',
              'clusterId','clusterName','cluster_name',
              'jobName','jobGroupId','jobGroup',
              'idInJob',
              'rootRunId', 'currentRunId', 'jobRunId', 
              'jobId']:
        if x in ctx.keys():
            r_ctx[x] = ctx[x]
        if 'tags' in ctx.keys():
            for t in ctx['tags'].keys():
                if t == x:
                    r_ctx[t] = ctx['tags'][t]
        if 'attributes' in ctx.keys():
            for t in ctx['attributes'].keys():
                if t == x:
                    r_ctx[t] = ctx['attributes'][t]

    return dict(sorted(r_ctx.items()))

get_context()


# COMMAND ----------


