
## Job identifiers
Explore the many ways to get job identifiers across compute types. The solution coalesces these solutions into one drop in module and method.

## Solution
The solution consists of `job_context.py` which contains method `get_job_context(...)`

Using the solution:
```python
from job_context import get_job_context
context = get_job_context(spark, dbutils)
context
```

## Setup and run tests

1. Create Interactive clusters for:
    - DBR 10.4 LTS Non-assigned
    - DBR 13.3 LTS Shared
    - DBR 14.2 Shared

2. Edit job.json
    - Setup notification emails
    - Set repo location
    - Set run-as id

3. Create job definition in Databricks
```shell
databricks jobs create --json @job.json
```

4. Run the workflow