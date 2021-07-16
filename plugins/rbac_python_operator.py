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

import boto3
from airflow.operators.python_operator import PythonOperator
from airflow.utils.decorators import apply_defaults

STS_TOKEN_VALIDITY = 900


class RBACPythonOperator(PythonOperator):
    """
    Operator creates a PythonOperator with role bases access control and returns the RBACPythonOperator
    :param / :type python_callable: Inherited, refer Airflow's PythonOperator Class
    :param / :type op_args: Inherited, refer Airflow's PythonOperator Class
    :param / :type op_kwargs: Inherited, efer Airflow's PythonOperator Class
    :param / :type provide_context: Inherited, refer Airflow's PythonOperator Class
    :param / :type templates_dict: Inherited, refer Airflow's PythonOperator Class
    :param / :type templates_exts: Inherited, refer Airflow's PythonOperator Class
    :param task_iam_role_arn: IAM role arn that will be associated during task execution
    :type task_iam_role_arn: str
    """

    @apply_defaults
    def __init__(
        self,
        task_iam_role_arn,
        python_callable,
        op_args=None,
        op_kwargs=None,
        provide_context=False,
        templates_dict=None,
        templates_exts=None,
        *args,
        **kwargs
    ):
        super().__init__(
            python_callable=python_callable,
            op_args=op_args,
            op_kwargs=op_kwargs,
            templates_dict=templates_dict,
            templates_exts=templates_exts,
            provide_context=provide_context,
            *args,
            **kwargs
        )
        self.task_iam_role_arn = task_iam_role_arn

    def execute(self, context):
        """Airflow PythonOperator Execute Method"""
        assumed_role_object = boto3.client("sts").assume_role(
            RoleArn=self.task_iam_role_arn,
            RoleSessionName="AssumeRoleSession",
            DurationSeconds=STS_TOKEN_VALIDITY,
        )
        task_session = boto3.session.Session(
            aws_access_key_id=assumed_role_object["Credentials"]["AccessKeyId"],
            aws_secret_access_key=assumed_role_object["Credentials"]["SecretAccessKey"],
            aws_session_token=assumed_role_object["Credentials"]["SessionToken"],
        )
        self.op_kwargs["task_session"] = task_session
        super(RBACPythonOperator, self).execute(context)
