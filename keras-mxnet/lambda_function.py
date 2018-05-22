import numpy as np
from keras.preprocessing import image
import boto3
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
        
        # load selected MobileNet model
        from keras.applications.mobilenet import MobileNet, preprocess_input
        model = MobileNet(input_shape=(224,224,3), include_top=False, weights='imagenet')
        
        img_path = '/tmp/{}'.format(s3_key) # where to download image
        feat_path = '/tmp/{}.npy'.format(s3_key) # where to save features
        
        # download file to /tmp/[s3_key]
        s3.download_file(Bucket=s3_bucket,
                         Key=s3_key,
                         Filename=img_path)
        
        # load and preprocess image
        img = image.load_img(img_path, target_size=(224,224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        
        # get bottleneck features
        features = model.predict(x)
        
        # save features to /tmp/[s3_key].npy
        np.save(open(feat_path, 'wb'), features)
        
        # upload features to s3://[s3_bucket]/[s3_key].npy
        s3.upload_file(Filename=feat_path,
                      Bucket=s3_bucket,
                      Key=s3_key+'.npy')
        
        print(response)

        return