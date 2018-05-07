import boto3

batch = boto3.client('batch')

def lambda_handler(event, context):
    
    for record in event['Records']:
        s3_bucket = record['s3']['bucket']['name']
        s3_key = record['s3']['object']['key']
        
        response = batch.submit_job(
            jobName='serverless-imagenet-bottleneck-{}'.format(s3_key),
            jobQueue='first-run-job-queue',
            jobDefinition='serverless_imagenet_bottleneck:3 ',
            containerOverrides={
                'command': [
                    'python3',
                    'record_bottleneck.py',
                    s3_bucket,
                    s3_key
                ]
            },
            retryStrategy={
                'attempts': 123
            },
            timeout={
                'attemptDurationSeconds': 123
            }
        )
        
        print(response)