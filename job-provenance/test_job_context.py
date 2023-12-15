import pytest
from unittest.mock import MagicMock, patch
import json

@pytest.fixture
def spark(mocker):
    spark = MagicMock()
    def mock_get(key, default=None)->str:
        return {"spark.databricks.clusterUsageTags.sparkVersion":"10.4.x"}.get(key,default)
    
    spark.conf.get = mock_get
    return spark


def get_dbutils(file_name:str):
    # dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson()
	dbutils = MagicMock()
	getContext = MagicMock()
	def mock_toJson()->str:
		return str(open(file_name,'r').read())

	dbutils.notebook.entry_point.getDbutils.return_value.notebook.return_value.getContext.return_value.toJson.return_value = mock_toJson()
	return dbutils

def test_spark_conf(spark):
    assert "10.4.x" == spark.conf.get("spark.databricks.clusterUsageTags.sparkVersion")
    assert spark.conf.get("zed") is None

def test_dbutils():
	dbutils = get_dbutils('10.4.json')
	js = dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson()
	assert str == type(js), js
	assert len(js) > 1000, js

	ctx = json.loads(js)
	assert ctx is not None, ctx
	assert type(ctx) == dict
	tags = ctx.get("tags")
	assert "orgId" in tags.keys()
	assert tags.get("orgId", None) == "1444828305810485"

def test_get_context_10_4_parent(spark):
	from job_context import get_job_context
	dbutils = get_dbutils('10.4.json')
	r_ctx = get_job_context(spark, dbutils)
	assert r_ctx is not None
	assert r_ctx['org_id'] == '1444828305810485'
	assert r_ctx['user'] == "douglas.moore@databricks.com"
	assert r_ctx['job_id'] == "98731591823372"
	assert r_ctx['job_run_id'] == "1080228838514376"
	assert r_ctx['task_run_id'] == "982886890498460"
 
def test_get_context_10_4_child(spark):
	from job_context import get_job_context
	dbutils = get_dbutils('10.4.child.json')
	r_ctx = get_job_context(spark, dbutils)
	assert r_ctx is not None
	assert r_ctx['org_id'] == '1444828305810485'
	assert r_ctx['user'] == "douglas.moore@databricks.com"
	assert r_ctx['job_id'] == "822028419959927"
	assert r_ctx['job_run_id'] == None
	assert r_ctx['task_run_id'] == "448220989536269"
