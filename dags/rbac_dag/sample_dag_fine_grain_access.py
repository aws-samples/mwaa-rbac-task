"""
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: MIT-0

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from airflow import DAG
from custom_operators.rbac_python_operator import RBACPythonOperator
from airflow.utils.dates import days_ago

import rbac_dag.dag_config as cf

from datetime import datetime
from time import sleep
from io import BytesIO
import json


def task_process(*args, **kwargs):
    bucket = kwargs["bucket"]
    boto_session = kwargs["task_session"]

    # Sleep mocks a time taking process
    sleep(cf.MOCK_TRANSFORMATION_IN_SECONDS)

    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    if bucket == cf.PROCESSED_S3_BUCKET:
        s3_obj = {"processed_dt": now}
        obj_name = "processed"
    else:
        s3_obj = {"published_dt": now}
        obj_name = "published"

    s3 = boto_session.resource("s3")
    s3.Object(bucket_name=bucket, key=f"control_file/{obj_name}.json").put(
        Body=BytesIO(json.dumps(s3_obj).encode("utf-8")).getvalue()
    )


dag_default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 0,
}

dag = DAG(
    dag_id="sample_rbac_dag",
    description="Sample DAG with fine grain access for tasks",
    default_args=dag_default_args,
    start_date=days_ago(0),
    schedule_interval="@once",
    catchup=False,
)

process_task = RBACPythonOperator(
    task_id="process_task",
    python_callable=task_process,
    provide_context=True,
    op_kwargs={"bucket": cf.PROCESSED_S3_BUCKET},
    task_iam_role_arn=cf.PROCESSED_IAM_ROLE,
    dag=dag,
)

publish_task = RBACPythonOperator(
    task_id="publish_task",
    python_callable=task_process,
    provide_context=True,
    op_kwargs={"bucket": cf.PUBLISHED_S3_BUCKET},
    task_iam_role_arn=cf.PUBLISHED_IAM_ROLE,
    dag=dag,
)

process_task >> publish_task
