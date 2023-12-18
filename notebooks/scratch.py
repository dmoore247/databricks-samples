# Databricks notebook source
# dbutils.notebook.entry_point.getDbutils().notebook().getContext().safeToJson()

# COMMAND ----------

dbutils.notebook.entry_point.getDbutils().notebook()

# COMMAND ----------

import json

# COMMAND ----------


is_job(spark)

# COMMAND ----------


# COMMAND ----------

# MAGIC %sql set

# COMMAND ----------


def get_version(spark):
    _ = spark.conf.get('spark.databricks.clusterUsageTags.effectiveSparkVersion')
    return int(_.split('.')[0]), int(_.split('.')[1])


get_version(spark)

# COMMAND ----------


# COMMAND ----------


# COMMAND ----------

try:
    if "safeToJson" in dbutils.notebook.entry_point.getDbutils().notebook().getContext()._methods:
        dbutils.notebook.entry_point.getDbutils().notebook().getContext().safeToJson()
except Exception as e:
    print('caught ' + e)
finally:
    print('finally ')

# COMMAND ----------

dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson()

# COMMAND ----------

dbutils.notebook.entry_point.getDbutils().notebook().getContext().safeToJson

# COMMAND ----------
