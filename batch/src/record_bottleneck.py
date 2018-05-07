import numpy as np
from keras.preprocessing import image
import boto3
import argparse


def record_bottleneck(s3_bucket, s3_key, pretrained_model):
    # load selected pre-trained model
    if pretrained_model=='MobileNet':
        from keras.applications.mobilenet import MobileNet, preprocess_input
        model = MobileNet(input_shape=(224,224,3), include_top=False, weights='imagenet')
    
    img_path = '/tmp/{}'.format(s3_key) # where to download image
    feat_path = '/tmp/{}.npy'.format(s3_key) # where to save features
    
    # download file to /tmp/[s3_key]
    s3 = boto3.client('s3')
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
    np.save(open(feat_path, 'w'), features)
    
    # upload features to s3://[s3_bucket]/[s3_key].npy
    s3.upload_file(Filename=feat_path,
                  Bucket=s3_bucket,
                  Key=s3_key+'.npy')
                  

if __name__=='__main__':
    parser = argparse.ArgumentParser(
        description="""Takes an input image in S3 and outputs bottleneck \
        features back into S3."""
    )
    
    parser.add_argument('s3_bucket',
                        help='Amazon S3 bucket where the image is stored.')
    parser.add_argument('s3_key',
                        help='Amazon S3 Key for the the image.')
    parser.add_argument('--model', 
        help='Keras Application to use. Defaults to "MobileNet".',
        default='MobileNet'
    )
    
    args = parser.parse_args()
    
    s3_bucket = args.s3_bucket
    s3_key = args.s3_key
    pretrained_model = args.model
    
    record_bottleneck(s3_bucket, s3_key, pretrained_model)