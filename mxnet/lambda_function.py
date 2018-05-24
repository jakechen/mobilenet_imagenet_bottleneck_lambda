import boto3
import numpy as np
import mxnet as mx
from mxnet.gluon.model_zoo import vision
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')
batch = boto3.client('batch')


def lambda_handler(event, context):
    """
    Input: Lambda s3 trigger events
    """
    logger.debug(event)
    
    for record in event['Records']:
        s3_bucket = record['s3']['bucket']['name']
        s3_key = record['s3']['object']['key']
        logger.debug(s3_bucket)
        logger.debug(s3_key)
        
        img_path = '/tmp/{}'.format(s3_key) # where to download image
        feat_path = '/tmp/{}.npy'.format(s3_key) # where to save features
        
        # load selected MobileNet model
        model = vision.get_model(name='mobilenet1.0', pretrained=True)
        
        # download file to /tmp/[s3_key]
        s3.download_file(Bucket=s3_bucket,
                         Key=s3_key,
                         Filename=img_path)
        
        # load and preprocess image
        with open("./dog.0.jpg", 'rb') as fp:
            str_image = fp.read()
        image = mx.image.imdecode(str_image)
        image = image.astype('float32')/255
        image = mx.image.color_normalize(image,
                                         mean=mx.nd.array([0.485, 0.456, 0.406]),
                                         std=mx.nd.array([0.229, 0.224, 0.225]))
        image = image.reshape([1, -1, image.shape[0], image.shape[1]])
        
        # get bottleneck features
        features = model.features(image)
        
        # save features to /tmp/[s3_key].npy
        np.save(open(feat_path, 'wb'), features)
        
        # upload features to s3://[s3_bucket]/[s3_key].npy
        s3.upload_file(Filename=feat_path,
                      Bucket=s3_bucket,
                      Key=s3_key+'.npy')
        
        print(response)

        return