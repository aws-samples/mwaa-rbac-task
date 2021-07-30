# Bolster security with role-based access control in Amazon MWAA

## Overview
The code provided with the repository is a reference [Apache Airflow](https://airflow.apache.org/) Directed Acyclic Graph(DAG) to support task level access control. 
The implementation has the following,
1. A custom Airflow Operator ( [PythonOperator](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/python.html) ) to provide fine grain access
2. Sample DAG that can be executed in [Amazon Managed Workflows for Apache Airflow (MWAA)](https://docs.aws.amazon.com/mwaa/index.html) 
    - Compatible in 1.10.12 and 2.0.2 version 

## How to use this code base
Follow the instructions to enforce role based access to tasks. note that the below steps will incur cost. 

1. Create a [MWAA](https://us-west-2.console.aws.amazon.com/mwaa/home) Environment ( Version 1.10.12 or 2.0.2)
2. Create the following Amazon S3 buckets
   - Processed bucket name : `<AWS-ACCOUNT_ID>-<REGION>-mwaa-processed` 
   - Published bucket name : `<AWS-ACCOUNT_ID>-<REGION>-mwaa-published`
   - Replace `<AWS-ACCOUNT_ID>` with your AWS Account ID and `<REGION>` with the region where the above MWAA service was launched
   - Follow [best practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html) while creating buckets. Its is stongly recommended to enable version control, encryption (In this case Amazon S3 master-key i.e SSE-S3) and server access logging.
3. Create following [AWS Identity and Access Management](https://console.aws.amazon.com/iam/home?region=us-west-2#/roles$new?step=type) Roles
    - Write access for the processed bucket 
        - Role Name : write_access_processed_bucket
        - Policy Document: Refer `./policy-docs/write_access_processed_bucket.json`
    - Write access for the published bucket
        - Role Name : write_access_published_bucket 
        - Policy Document: Refer `./policy-docs/write_access_published_bucket.json`
           
4. Establish trust relationship with [MWAA](https://us-west-2.console.aws.amazon.com/mwaa/home) execution role (Found in the MWAA environment page)
   - Refer `./policy-docs/trust-policy.json`
    
5. Code deployment to [MWAA](https://us-west-2.console.aws.amazon.com/mwaa/home) :
    - DAG Deployment
        - Code base is present in the `./dags/rbac_dag` directory
        - Update the following variables in `./dags/rbac_dag/dag_config.py` file
          - REGION ( e.g. us-west-2)
          - ACCOUNT_ID 
        - Deploy to MWAA by copying the DAG files to the appropriate MWAA S3 buckets that was configured in step 1
    - Custom Operator
        - Code base is present in the `./plugins/`. Create a ZIP and copy to the MWAA's S3 bucket configured in step 1, example s3:/<mwaa-s3-bucket>/plugins/custom_operators.zip
        - Deploy to MWAA by editing the MWAA environment and configure `Plugins file - optional` with the above plugins path 
        - Update the MWAA environment for the above change to take effect
   
6. DAG Execution
    - DAG `sample_rbac_dag` should show up in the [MWAA](https://us-west-2.console.aws.amazon.com/mwaa/home) Web UI ( can be accessed from MWAA service page) after few seconds.
    - Click the `Play` button to run the DAG
    - Notice that, since the roles are established at the task level the DAG completes the execution. Now try to restrict access via the roles and we will notice the DAG failing.


## Clean up:
Bring down the services after implementing the above - as they will incur cost if left running, 
- MWAA environment
- Delete S3 Buckets
- Remove IAM Roles and Policies

