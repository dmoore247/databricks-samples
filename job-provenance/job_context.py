import json

def _get_safe_ctx(dbutils) -> dict:
    """Cycle through APIs to get context information"""
    ctx = None
    ctx_type = None
    try:
        ctx = dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson()
        ctx_type="toJson"
    except Exception as e1:
        print('toJson',e1)
        try:
            ctx = dbutils.notebook.entry_point.getDbutils().notebook().getContext().safeToJson()
            ctx_type="safeToJson"
        except Exception as e2:
            print('toSafeJson',e2)
            from dbruntime.databricks_repl_context import get_context
            _ = get_context()
            if _:
                ctx = get_context().__dict__
                ctx_type = "repl_context"
    #print(ctx_type, ctx)
    return json.loads(ctx), ctx_type

def get_job_context(spark, dbutils, parent:dict = None) -> dict:
    """
        Return job context for current notebook for use in auditing.
    """
    version = 0
    ctx = None
    _ = spark.conf.get('spark.databricks.clusterUsageTags.sparkVersion', None)
    assert 'custom' not in _ and 'dlt' not in _

    major, minor = int(_.split('.')[0]), int(_.split('.')[1])
    version = (major, minor)
    task_run_id = job_run_id = job_id = org_id = user = None
    
    ctx,ctx_type = _get_safe_ctx(dbutils)
    if ctx_type == 'toJson':
        tags = ctx.get("tags",None)
        task_run_id = str(ctx.get('currentRunId',None).get('id',None))
        job_run_id = tags.get('jobRunId',None) if task_run_id != tags.get('jobRunId',None) else None
        job_id = tags.get('jobId',None)
        org_id = tags.get('orgId',None)
        user = tags.get('user',None)
        
    elif ctx_type == 'safeToJson':
        attrs = ctx.get('attributes', None)
        task_run_id = attrs.get('currentRunId') or attrs.get('rootRunId',None)
        job_run_id = attrs.get('multitaskParentRunId',None) or attrs.get('jobRunId',None) or attrs.get('rootRunId',None)
        job_id = attrs.get('jobId',None)
        org_id = attrs.get('orgId',None)
        user = attrs.get('user',None)
    else:
        task_run_id = ctx.get('currentRunId',None) or ctx.get('rootRunId', None)
        job_run_id = ctx.get('multitaskParentRunId', None) or ctx.get('jobRunId',None) or ctx.get('rootRunId',None)
        job_id = ctx.get('jobId', None)
        org_id = ctx.get('orgId',None)
        user = ctx.get('user',None)

    r_ctx = {
        'org_id':org_id,
        'user':user,
        'job_id': job_id if job_id != '' else None,
        'job_run_id': job_run_id if job_run_id != '' else None,
        'task_run_id': task_run_id if task_run_id != '' else None
    }
    return r_ctx