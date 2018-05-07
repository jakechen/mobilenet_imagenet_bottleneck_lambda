# mobilenet_imagenet_bottleneck_lambda

This AWS Lambda function returns the bottleneck features for a network pretrained on ImageNet.

For more information on this topic, see the 2nd half of [this blog](https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html)

## Instructions
### Build and Register Docker Image to ECR
First, we build a Docker Image that returns the bottleneck features for an input image.

See [batch](./batch) for the Dockerfile and the [main python script](./src/record_bottleneck.py).