# Databricks notebook source
# MAGIC %md ## Interactive Duplicate Table Search

# COMMAND ----------

# MAGIC %md ## Setup

# COMMAND ----------

%pip install --quiet databricks-vectorsearch
dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %sql
# MAGIC use catalog douglas_moore;
# MAGIC use schema vector;

# COMMAND ----------

from databricks.vector_search.client import VectorSearchClient

# Connect to the vector search index
client = VectorSearchClient(disable_notice=True)
index = client.get_index(
    endpoint_name="one-env-shared-endpoint-3", 
    index_name="douglas_moore.vector.table_metadata_vector_index")

# COMMAND ----------

def do_search(full_table_name:str):
    if len(full_table_name.split('.')) != 3:
        print("use full tablename, in the form of <catalog>.<schema>.<table>")
        return
    
    df = spark.sql(f"select column_json from table_metadata where full_table_name = '{full_table_name}'")
    if df.isEmpty():
        print(f"'{full_table_name}' has not been indexed")
        print(df.collect())
        return
    column_json = df.collect()[0][0]
    
    # search the vector index
    results = index.similarity_search(
        query_text=column_json, 
        columns=["full_table_name", "column_json"],
        num_results=10)

    print(f"Score:  \tTable")
    for _ in results['result']['data_array']:
        _score, _name = _[2],_[0]
        if _score > 0.9:
            print(f"{_score} \t{_name}")

# COMMAND ----------

import ipywidgets as widgets
def show_search_ui():
    layout = widgets.Layout(width='auto', height='40px') #set width and height
    # Create button widget. 
    button = widgets.Button(
        description="Search for similar",
        disabled=False,
        display='flex',
        flex_flow='column',
        align_items='stretch',
        layout=layout
        )
    table_name_widget = widgets.Text(
        value='douglas_moore.information_schema.tables',
        placeholder='Type something',
        description='table name:',
        disabled=False,
        display='flex',
        flex_flow='column',
        align_items='stretch',
        layout=layout
    )
    # Output widget to display the loaded dataframe
    output = widgets.Output()


    def on_button_clicked(_):
        with output:
            output.clear_output()
            name = table_name_widget.value
            do_search(name)

    # Register the button's callback function to query UC and display results to the output widget
    button.on_click(on_button_clicked)

    display(table_name_widget, button, output)

# COMMAND ----------

# MAGIC %md ## Search

# COMMAND ----------

show_search_ui()
