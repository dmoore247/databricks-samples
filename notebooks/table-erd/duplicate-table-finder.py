# Databricks notebook source
# MAGIC %md # Is dataset duplication costing your organization millions?
# MAGIC
# MAGIC Duplicate datasets cost enterprises millions in excessive licensing fees, duplicate data pipelines and enterprise scale data quality issues and data discovery fumbles. The current process is manually, word-of-mouth and tedious. As a data governance function you have almost no tracking. In this session you’ll learn how to use Databricks Data Intelligence Platform components (Vector Search, System Tables, Delta Live Tables, Lake View) to quickly solve these problems.
# MAGIC
# MAGIC People concerned with purchasing expensive data sets and managing effective use of the data real estate will be most interested in this discussion. Participants will get a demo and access to the solution code will be shared.
# MAGIC
# MAGIC If duplicate data set detection isn't your thing, you might accidently to get insights into how Databricks can help you solve other near real-time data deduplication tasks, does any one have duplicate customers or patients or products or claims?

# COMMAND ----------

%pip install --quiet databricks-vectorsearch
dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %md # Collect the table metadata

# COMMAND ----------

# MAGIC %sql
# MAGIC USE catalog douglas_moore;
# MAGIC USE schema vector;

# COMMAND ----------

# MAGIC %sql
# MAGIC --
# MAGIC -- This builds the view pulling all the column metadata into column_json
# MAGIC --
# MAGIC CREATE OR REPLACE VIEW table_metadata_vw
# MAGIC AS 
# MAGIC WITH cols as (
# MAGIC   SELECT 
# MAGIC     c.table_catalog, c.table_schema, c.table_name, c.ordinal_position,
# MAGIC     c.column_name, c.full_data_type, c.comment as column_comment
# MAGIC   FROM system.information_schema.columns c
# MAGIC   ORDER BY c.table_catalog, c.table_schema, c.table_name, c.ordinal_position
# MAGIC ),
# MAGIC full_table_index AS (
# MAGIC SELECT
# MAGIC table_catalog || '.' || table_schema || '.' || table_name as full_table_name, 
# MAGIC to_json(named_struct(
# MAGIC   'columns', collect_list(named_struct(
# MAGIC     'column_name', column_name,
# MAGIC     'ordinal_position', ordinal_position,
# MAGIC     'full_data_type', full_data_type,
# MAGIC     'comment', column_comment
# MAGIC   ))
# MAGIC )) AS column_json
# MAGIC FROM  cols
# MAGIC GROUP BY full_table_name
# MAGIC ORDER BY full_table_name
# MAGIC )
# MAGIC SELECT * from full_table_index;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM table_metadata_vw limit 5

# COMMAND ----------

# MAGIC %md ## Create source table for vector search index
# MAGIC - Requires a primary key column
# MAGIC - Requires a column to compute an embedding on (the vector)
# MAGIC - Optional filter columns
# MAGIC - Requires Change Data Feed (CDF) to be enabled (auto update the vector index)

# COMMAND ----------

# MAGIC %sql
# MAGIC --
# MAGIC -- Create source table for vector index
# MAGIC --
# MAGIC CREATE TABLE IF NOT EXISTS table_metadata (
# MAGIC   full_table_name STRING PRIMARY KEY,
# MAGIC   column_json STRING
# MAGIC )
# MAGIC TBLPROPERTIES (delta.enableChangeDataFeed = true)
# MAGIC ;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- add new records to be indexed
# MAGIC INSERT INTO table_metadata
# MAGIC SELECT * FROM table_metadata_vw

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from table_metadata

# COMMAND ----------

# MAGIC %md # Setup Vector search
# MAGIC (use UI)

# COMMAND ----------

# MAGIC %md # Search the index

# COMMAND ----------

from databricks.vector_search.client import VectorSearchClient

# Connect to the vector search index
client = VectorSearchClient(disable_notice=True)
index = client.get_index(
    endpoint_name="one-env-shared-endpoint-3", 
    index_name="douglas_moore.vector.table_metadata_vector_index")

# COMMAND ----------

# index.describe()

# COMMAND ----------

full_table_name = "dbdemos.uc_lineage.dinner"
df = spark.sql(f"select column_json from table_metadata where full_table_name = '{full_table_name}'")
column_json = df.collect()[0][0]

# COMMAND ----------

# search index
results = index.similarity_search(
    query_text=column_json, 
    columns=["full_table_name", "column_json"],
    num_results=10)

print(f"score:  \tTable")
for _ in results['result']['data_array']:
    print(f"{_[2]} \t{_[0]}")
