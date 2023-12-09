import json
import pprint

def get_job_context(spark, dbutils) -> dict:
    """Return job context for current notebook"""
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

        task_run_id = ctx.get('rootRunId',None).get('id',None) if ctx.get('rootRunId',None) else None
        job_run_id = ctx.get('tags',None).get('jobRunId',None) if ctx.get('tags',None) else None 
        job_id = ctx.get('tags',None).get('jobId',None) if ctx.get('tags',None) else None

    elif version <= (13,3):
        try:
            print('safeToJson')
            ctx = json.loads(dbutils.notebook.entry_point.getDbutils().notebook().getContext().safeToJson())
            pprint.pprint(ctx)
        except Exception as e:
            print('safeToJson fails', e)
        task_run_id = ctx.get('attributes',None).get('rootRunId',None)
        job_run_id = ctx.get('attributes',None).get('multitaskParentRunId',None) or ctx.get('attributes',None).get('jobRunId',None)
        job_id = ctx.get('attributes',None).get('jobId',None)
    else:    
        try:
            print('databricks_repl_context')
            from dbruntime.databricks_repl_context import get_context
            _ = get_context()
            if _:
                ctx = get_context().__dict__
        except Exception as e:
            print('databricks_repl_context fails', e)
        task_run_id = ctx.get('rootRunId', None)
        job_run_id = ctx.get('multitaskParentRunId', None)
        job_id = ctx.get('jobId', None)
    
    r_ctx = {
        'job_id': job_id if job_id != '' else None,
        'job_run_id': job_run_id if job_run_id != '' else None,
        'task_run_id': task_run_id if task_run_id != '' else None
    }
    return r_ctx