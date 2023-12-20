import json
from unittest.mock import MagicMock

import pytest

from job_provenance.job_context import get_job_context, is_job

MIN_CONTEXT_LENGTH = 1000

@pytest.fixture
def spark():
    spark = MagicMock()

    def mock_get(key, default=None) -> str:
        job_all_tags = """[{"key":"Vendor","value":"Databricks"},{"key":"Creator","value":"douglas.moore@databricks.com"},{"key":"ClusterName","value":"job-208642262573410-run-946414708728403"},{"key":"ClusterId","value":"1218-164003-oleantft"},{"key":"DatabricksInstancePoolCreatorId","value":"7644138420879474"},{"key":"DatabricksInstancePoolId","value":"0727-104344-hauls13-pool-uftxk0r6"},{"key":"DatabricksInstanceGroupId","value":"-8117034103866820710"},{"key":"JobId","value":"208642262573410"},{"key":"RunName","value":"scratch"},{"key":"Name","value":"workerenv-1444828305810485-d9ffacea-609b-45bd-9ce1-0aea7d300120-worker"}]"""
        return {"spark.databricks.clusterUsageTags.sparkVersion": "10.4.x",
                "spark.databricks.clusterUsageTags.clusterAllTags": job_all_tags}.get(key, default)

    spark.conf.get = mock_get
    return spark

@pytest.fixture
def iteractive_10_4_spark():
    spark = MagicMock()

    def mock_get(key, default=None) -> str:
        all_tags = """[{"key":"Vendor","value":"Databricks"},{"key":"Creator","value":"douglas.moore@databricks.com"},{"key":"ClusterName","value":"Cody Davis's Shared 14.2 Cluster"},{"key":"ClusterId","value":"1215-153339-cmts67ky"},{"key":"Name","value":"workerenv-1444828305810485-d9ffacea-609b-45bd-9ce1-0aea7d300120-worker"}]"""
        return {"spark.databricks.clusterUsageTags.sparkVersion": "10.4.x",
                "spark.databricks.clusterUsageTags.clusterAllTags": all_tags}.get(key, default)

    spark.conf.get = mock_get
    return spark

def get_dbutils(file_name: str):
    # dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson()
    dbutils = MagicMock()

    def mock_tojson() -> str:
        return str(open(file_name).read())

    dbutils.notebook.entry_point.getDbutils.return_value.notebook.return_value.getContext.return_value.toJson.return_value = (
        mock_tojson()
    )
    return dbutils


def test_spark_conf(spark):
    assert "10.4.x" == spark.conf.get("spark.databricks.clusterUsageTags.sparkVersion")
    assert spark.conf.get("zed") is None


def test_is_job(spark):
    assert True == is_job(spark)


def test_dbutils():
    dbutils = get_dbutils("resources/10.4.json")
    js = dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson()
    assert str == type(js), js
    assert len(js) > MIN_CONTEXT_LENGTH, js

    ctx = json.loads(js)
    assert ctx is not None, ctx
    assert isinstance(ctx, dict)
    tags = ctx.get("tags")
    assert "orgId" in tags.keys()
    assert tags.get("orgId", None) == "1444828305810485"


def test_get_context_10_4_parent(spark):
    dbutils = get_dbutils("resources/10.4.json")
    r_ctx = get_job_context(dbutils=dbutils, spark=spark)
    assert r_ctx is not None
    assert r_ctx["org_id"] == "1444828305810485"
    assert r_ctx["user"] == "douglas.moore@databricks.com"
    assert r_ctx["job_id"] == "98731591823372"
    assert r_ctx["job_run_id"] == "1080228838514376"
    assert r_ctx["task_run_id"] == "982886890498460"


def test_get_context_10_4_child(spark):
    dbutils = get_dbutils("resources/10.4.child.json")
    r_ctx = get_job_context(dbutils=dbutils, spark=spark)
    assert r_ctx is not None
    assert r_ctx["org_id"] == "1444828305810485"
    assert r_ctx["user"] == "douglas.moore@databricks.com"
    assert r_ctx["job_id"] == "822028419959927"
    assert r_ctx["job_run_id"] is None
    assert r_ctx["task_run_id"] == "448220989536269"
    
def test_get_context_10_4_interactive(iteractive_10_4_spark):
    dbutils = get_dbutils("resources/10.4.interactive.json")
    r_ctx = get_job_context(dbutils=dbutils, spark=iteractive_10_4_spark)
    assert r_ctx is not None
    assert r_ctx["org_id"] == "1444828305810485"
    assert r_ctx["user"] == "douglas.moore@databricks.com"
    assert r_ctx["job_id"] is None
    assert r_ctx["job_run_id"] is None
    assert r_ctx["task_run_id"] is None