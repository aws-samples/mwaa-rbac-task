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

# DAG CONFIGURATIONS
REGION = "us-west-2"  # Update region
ACCOUNT_ID = "123456789012"  # Enter AWS Account Number here

PROCESSED_S3_BUCKET = f"{ACCOUNT_ID}-{REGION}-mwaa-processed"
PUBLISHED_S3_BUCKET = f"{ACCOUNT_ID}-{REGION}-mwaa-published"

PROCESSED_IAM_ROLE = f"arn:aws:iam::{ACCOUNT_ID}:role/write_access_processed_bucket"
PUBLISHED_IAM_ROLE = f"arn:aws:iam::{ACCOUNT_ID}:role/write_access_published_bucket"

MOCK_TRANSFORMATION_IN_SECONDS = 10
