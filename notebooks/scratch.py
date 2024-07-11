# Databricks notebook source
#dbutils.notebook.entry_point.getDbutils().notebook().getContext().safeToJson()

# COMMAND ----------

# MAGIC %md
# MAGIC | col1 | col2 |  col3   |
# MAGIC |------|------|---------|
# MAGIC | abc  | 123  |  12/4/5 |
# MAGIC | def  | 573  | 01/08/09|
# MAGIC

# COMMAND ----------

r = dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson()

# COMMAND ----------

try:
    r = {'toJson':dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson()}
except:
    r = {'toSafeJson':dbutils.notebook.entry_point.getDbutils().notebook().getContext().safeToJson()}
r

# COMMAND ----------

r1 = {'toJson': '{"rootRunId":null,"currentRunId":null,"jobGroup":"5301686147661020848_8872355671227396416_97f569cf85e8498981d66e131f57ef23","tags":{"opId":"ServerBackend-f0584fe4b1a506cb","shardName":"oregon-prod","opTarget":"com.databricks.backend.common.rpc.InternalDriverBackendMessages$StartRepl","clusterMemory":"249856","serverBackendName":"com.databricks.backend.daemon.driver.DriverCorral","notebookId":"502783634811541","projectName":"driver","tier":"tier-multitenant","eventWindowTime":"2819225.8000001907","httpTarget":"/notebook/502783634811541","commandRunId":"785db3f4-f76c-430b-9f5a-6aa509d87751","buildHash":"","workspaceRoutingTarget":"DESTINATION_DB","browserHash":"#notebook/502783634811541/command/69050624651077","browserPathName":"/","notebookLanguage":"python","workspaceRoutingBucket":"null","sparkVersion":"14.0.x-cpu-ml-scala2.12","hostName":"cons-webapp-15","httpMethod":"POST","browserIdleTime":"1154","jettyRpcJettyVersion":"9","browserLanguage":"en-US","browserTabId":"3df0aeaf-aff1-4680-8115-cb670f91d1c5","sourceIpAddress":"130.41.224.64","accountId":"e6e8162c-a42f-43a0-af86-312058795a14","loadedUiVersions":"Map(monolith -> 3e887c5ce6d690165028330522bc9ba746c29bf4)","browserUserAgent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36","orgId":"1444828305810485","userAgent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36","clusterId":"0329-145545-rugby794","workloadClass":"commandRunSelected","serverEventId":"CgsIn66RrQYQgtHBRjoQ3T0kvAjERDywRk3G/iJLVQ==","rootOpId":"ServiceMain-fa2c042c64d30002","requestIdWasMissing":"true","sessionId":"068e90867d445d116474fab95ca02dff84a51562ab97be27f5bb75939fb68a1f","clusterCreator":"afsana.afzal@databricks.com","originatedFromEnvoy":"true","clientBranchName":"webapp_2023-12-17_00.52.27Z_master_ce07d3f0_1042893885","workloadId":"502783634811541-4b373747-638d-4252-a14d-c2293ae0e536","clientTimestamp":"1705269076839","clusterType":"spot","requestId":"CgsIn66RrQYQssSyRjoQ3T0kvAjERDywRk3G/iJLVQ==","browserHasFocus":"true","queryParameters":"?o=1444828305810485","userId":"3967816683930536","browserIsHidden":"false","clientLocale":"en","branchName":"webapp_2023-12-17_00.52.27Z_master_ce07d3f0_1042893885","opType":"ServerBackend","sourcePortNumber":"0","user":"douglas.moore@databricks.com","browserHostName":"e2-demo-field-eng.cloud.databricks.com","parentOpId":"RPCClient-fa2c042c64d30425","jettyRpcType":"InternalDriverBackendMessages$DriverBackendRequest"},"extraContext":{"mlflowGitRelativePath":"notebooks/scratch","allowStdin":"true","non_uc_api_token":"","commandResultJsonMaxBytes":"20971520","enableDeltaLiveTablesAnalysis":"true","mlflowGitStatus":"unknown","mlflowGitReference":"main","mlflowGitUrl":"https://github.com/dmoore247/databricks-samples.git","notebook_path":"/Repos/douglas.moore@databricks.com/databricks-samples/notebooks/scratch","notebook_id":"502783634811541","thresholdForStoringInDbfs":"0","mlflowGitCommit":"605a2a975fd0ee6c054bfd31fffe35c64cbc73b0","enableStoringResultsInDbfs":"true","mlflowGitReferenceType":"branch","api_url":"https://oregon.cloud.databricks.com","aclPathOfAclRoot":"/workspace/1162555279775472/3945504874997326/1974893261152428/3239664139663167/502783634811541","mlflowGitProvider":"gitHub","api_token":"[REDACTED]"},"credentialKeys":["adls_aad_token","adls_gen2_aad_token","synapse_aad_token"]}'}
r2 = {'toSafeJson': '{"attributes":{"mlflowGitRelativePath":"notebooks/scratch","non_uc_api_token":"[REDACTED]","enableDeltaLiveTablesAnalysis":"true","mlflowGitStatus":"unknown","commandRunId":"a6a25709-3c2e-44d0-a528-e98ec6a6c34b","mlflowGitReference":"main","mlflowGitUrl":"https://github.com/dmoore247/databricks-samples.git","notebook_path":"/Repos/douglas.moore@databricks.com/databricks-samples/notebooks/scratch","notebook_id":"502783634811541","orgId":"1444828305810485","mlflowGitCommit":"605a2a975fd0ee6c054bfd31fffe35c64cbc73b0","mlflowGitReferenceType":"branch","clusterId":"0601-182128-dcbte59m","api_url":"https://oregon.cloud.databricks.com","aclPathOfAclRoot":"/workspace/1162555279775472/3945504874997326/1974893261152428/3239664139663167/502783634811541","mlflowGitProvider":"gitHub","api_token":"[REDACTED]","jobGroup":"5646897307052653121_6545871394206347938_348f1d544627471e8f55f687a5979015","user":"douglas.moore@databricks.com","currentRunId":"","browserHostName":"e2-demo-field-eng.cloud.databricks.com","rootRunId":""}}'}

# COMMAND ----------

r1, r2

# COMMAND ----------

import json

# COMMAND ----------



# COMMAND ----------

def get_config(r: dict) -> dict :
    if set(r.keys())== set(r1.keys()):
        return r
    else:
        common_key = set(r.keys()) & set(r1.keys())
        missing_key = set(r1.keys()) - set(r.keys())
        combined_dict = {k: r1[k] for k in common_key}
        combined_dict.update({k: r[k] for k in missing_key})
        return combined_dict

# COMMAND ----------

get_config(r1)

# COMMAND ----------

get_config(r2)

# COMMAND ----------

# MAGIC %sql set

# COMMAND ----------

try:
    if "safeToJson" in dbutils.notebook.entry_point.getDbutils().notebook().getContext()._methods:
        dbutils.notebook.entry_point.getDbutils().notebook().getContext().safeToJson()
except Exception as e:
    print('caught ' + e)
finally:
    print('finally ' )

# COMMAND ----------

dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson()

# COMMAND ----------

js = dbutils.notebook.entry_point.getDbutils().notebook().getContext().safeToJson()
js

# COMMAND ----------

from py4j.protocol import Py4JError

# COMMAND ----------


try:
    js = dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson()
    print(js)
except Py4JError as e:
    print('caught ' + e)


# COMMAND ----------

# MAGIC %pip install --quiet databricks-sdk==0.16.0
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

from databricks.sdk import WorkspaceClient
w = WorkspaceClient()
dbutils = w.dbutils
js = dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson()
print(js)

# COMMAND ----------


