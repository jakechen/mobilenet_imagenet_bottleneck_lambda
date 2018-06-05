# Serverless Imagenet Bottleneck Workflow

## Introduction
This set of tutorials create AWS Serverless workflows that return the bottleneck features for a network pretrained on ImageNet. There are multiple workflows depending on the Deep Learning framework used, which determines which AWS service used for inference. For example, MXNet is small enough to be deployed onto AWS Lambda, but Keras+Tensorflow will require Batch in addition to Lambda.

## Background
One of the primary use cases of this workflow is Transfer Learning for image classification. In Transfer Learning, pre-trained networks are used as a foundation for custom labels. In practice, model training only happens on the last layer, thus drastically speeding up training time. One further optimization is to first run the image through the pretrained network, record the n-1 layer (aka bottleneck features), and store the outputs to an offline file. In this case, we will store the features into Amazon S3. For more information on using bottleneck features to speed up transfer learning, see the 2nd half of [this blog](https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html)

The primary benefits of using a Serverless workflow is the ability to offload the compute resource management to an underlying fleet. This means no need to manage EC2 instances; we only pay when the workflow is run.

## TODO
- GPU inference instead of CPU

## Methods Shown
### 1. [Baseline MXNet on Sagemaker](./mxnet-sagemaker-endpoint/)
In this initial method, we will use a Sagemaker endpoint to run the inference and output the bottleneck features. While this does not have the benefits of Serverless, we can explore this method to establish a performance baseline.

### 2. [MXNet on Lambda](./mxnet-lambda)
This re-uses most of the code from the baseline, but will use Lambda for the Serverless compute.

### 3. [Keras+Tensorflow on Lambda+Batch](./keras-tf-lambda-batch)
Finally, we explore using Keras Applications for feature generation. However, this method is too large for AWS Lambda alone so it requires both AWS Lambda and AWS Batch.
