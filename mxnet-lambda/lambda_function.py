import boto3
import numpy as np
import mxnet as mx
from mxnet.gluon.model_zoo import vision
from io import BytesIO
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')
batch = boto3.client('batch')

# load selected MobileNet model
model = vision.get_model(name='mobilenet1.0', pretrained=True, root='/tmp/.mxnet/models')


def lambda_handler(event, context):
    """
    Input: Lambda s3 trigger events
    """
    logger.debug(event)
    
    for record in event['Records']:
        s3_bucket = record['s3']['bucket']['name']
        s3_key = record['s3']['object']['key']
        logger.info("S3 bucket: {}".format(s3_bucket))
        logger.info("S3 key: {}".format(s3_key))
        
        # download file to memory
        response = s3.get_object(
            Bucket=s3_bucket,
            Key=s3_key
        )
        
        # decode and preprocess image
        image = mx.image.imdecode(response['Body'].read())
        image = image.astype('float32')/255
        image = mx.image.color_normalize(image,
                                         mean=mx.nd.array([0.485, 0.456, 0.406]),
                                         std=mx.nd.array([0.229, 0.224, 0.225]))
        image = image.reshape([1, -1, image.shape[0], image.shape[1]])
        
        # get bottleneck features
        features = model.features(image)
        
        # save features to buffer and upload
        with BytesIO() as b:
            np.save(b, features.asnumpy())
            
            b.seek(0)
            response = s3.put_object(
                Body = b,
                Bucket=s3_bucket,
                Key="{}.npy".format(s3_key)
            )
        
            logging.info(response)

    return
