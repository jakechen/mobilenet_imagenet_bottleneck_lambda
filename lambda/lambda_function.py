import boto3
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

batch = boto3.client('batch')

def lambda_handler(event, context):
    logger.debug(event)
    
    for record in event['Records']:
        s3_bucket = record['s3']['bucket']['name']
        s3_key = record['s3']['object']['key']
        logger.debug(s3_bucket)
        logger.debug(s3_key)
        
        response = batch.submit_job(
            jobName='serverless-imagenet-bottleneck',
            jobQueue='first-run-job-queue',
            jobDefinition='serverless-imagenet-bottleneck:1',
            containerOverrides={
                'command': [
                    'python3',
                    'record_bottleneck.py',
                    s3_bucket,
                    s3_key
                ]
            }
        )
        
        print(response)