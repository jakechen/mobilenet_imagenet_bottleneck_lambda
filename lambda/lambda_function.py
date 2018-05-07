import numpy as np
import boto3
from keras.preprocessing import image
from keras.applications.mobilenet import MobileNet, preprocess_input

s3 = boto3.client('s3')
model = MobileNet(input_shape=(224,224,3), include_top=False, weights='imagenet')

def lambda_hander(event, context):
    
    for record in event['Records']:
        s3_bucket = record['s3']['bucket']['name']
        s3_key = record['s3']['object']['key']
        
        # download file to /tmp/[s3_key]
        s3.download_file(Bucket=s3_bucket,
                         Key=s3_key,
                         Filename='/tmp/{}'.format(s3_key))
        
        # load and preprocess image
        img_path = '/tmp/{}'.format(s3_key)
        img = image.load_img(img_path, target_size=(224,224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        
        # get bottleneck features
        features = model.predict(x)
        
        # save features to /tmp/[s3_key].npy
        np.save(open('/tmp/{}.npy'.format(s3_key), 'w'), features)
        
        # upload features to s3://[s3_bucket]/[s3_key].npy
        s3.upload_file(Filename='/tmp/{}.npy'.format(s3_key),
                       Bucket=s3_bucket,
                       Key=s3_key+'.npy')