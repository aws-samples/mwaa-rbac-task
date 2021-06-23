# Overview

## Description
The code provided with repository is a reference [Apache Airflow](https://airflow.apache.org/) Directed Acyclic Graph(DAG) to support task level access control. 
The implementation has the following,
1. A custom Airflow Operator ( [PythonOperator](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/python.html) ) to provide fine grain access
2. Sample DAG that can be executed in [Amazon Managed Workflows for Apache Airflow (MWAA)](https://docs.aws.amazon.com/mwaa/index.html) 
    - Compatible in 1.10.12 and 2.0.2 version 

## How to use this code base

Prerequisite:

1. [MWAA](https://us-west-2.console.aws.amazon.com/mwaa/home) Environment ( Version 1.10.12 or 2.0.2)
2. Create following buckets 
   - Processed bucket name : `s3-<AWS-ACCOUNT_ID>-<REGION>-mwaa-processed` 
   - Published bucket name : `s3-<AWS-ACCOUNT_ID>-<REGION>-mwaa-published`
   - Replace `<AWS-ACCOUNT_ID>` with your AWS Account ID and `<REGION>` to the region where the MWAA is available
3. Create [IAM Roles](https://console.aws.amazon.com/iam/home?region=us-west-2#/roles$new?step=type)
    - Write access for the processed bucket 
        - Role Name : write_access_processed_bucket
        - Policy Document:
           ```{
               "Version": "2012-10-17",
               "Statement": [
                   {
                       "Sid": "VisualEditor0",
                       "Effect": "Allow",
                       "Action": [
                           "s3:PutObject",
                           "s3:DeleteObject"
                       ],
                       "Resource": "arn:aws:s3:::<AWS-ACCOUNT_ID>-<REGION>-mwaa-processed/*"
                   }
               ]
           }```
        - Role Name : write_access_published_bucket 
        - Policy Document:
            ```
            {
               "Version": "2012-10-17",
               "Statement": [
                   {
                       "Sid": "VisualEditor0",
                       "Effect": "Allow",
                       "Action": [
                           "s3:PutObject",
                           "s3:DeleteObject"
                       ],
                       "Resource": "arn:aws:s3:::<AWS-ACCOUNT_ID>-<REGION>-mwaa-published/*"
                   }
               ]
            }
            ```
4. Establish trust relationship with [MWAA](https://us-west-2.console.aws.amazon.com/mwaa/home) execution role (Found in the MWAA environment page)
   ```
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "AWS": [
             "arn:aws:iam::ACCOUNT-ID-WITHOUT-HYPHENS:assumed-role/<MWAA-EXECUTION_ROLE>/AmazonMWAA-airflow"
           ],
           "Service": "s3.amazonaws.com"
         },
         "Action": "sts:AssumeRole"
       }
     ]
   }
   ```
    
5. Code Deployment to [MWAA](https://us-west-2.console.aws.amazon.com/mwaa/home) :
    - DAG Deployment
        - Code base is present in the `dags/rbac_dag` directory
        - Update the following variables in `dag_config.py` file
          - REGION ( e.g. us-west-2)
          - ACCOUNT_ID 
        - Deploy to MWAA by copying the DAG files to the appropriate MWAA S3 buckets
    - Custom Operator
        - Code base is present in the `custom_operator` directory
        - Deploy to MWAA by copying the custom operator files to the appropriate MWAA S3 buckets
   
6. DAG Execution
    - DAG `sample_rbac_dag` should show up in the [MWAA](https://us-west-2.console.aws.amazon.com/mwaa/home) Web UI ( can be accessed from MWAA service page) after few seconds.
    - Click the `Play` button to run the DAG
    - Notice that, since the roles are established at the task level the DAG completes the execution. Now try to restrict access via the roles and we will notice the DAG failing.

