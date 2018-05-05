# mobilenet_imagenet_bottleneck_lambda

This AWS Lambda function returns the bottleneck features for an imagenet-pretrained mobilenet.

For more information on this topic, see the 2nd half of [this blog](https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html)

## Instructions
Below instructions are based on [this blog](https://ryan-cranfill.github.io/keras-aws-lambda/)

Load up EC2 or Cloud9

Run the following commands:

    sudo yum install -y python-devel python-nose python-setuptools gcc gcc-gfortran gcc-c++ blas-devel lapack-devel atlas-devel
    virtualenv env -p python3
    source env/bin/activate
    find env/ -name "*.so" | xargs strip
    cp -r ~/env/lib/python3.6/dist-packages/theano .
    cp -r ~/env/lib/python3.6/dist-packages/pkg_resources .
    cp -r ~/env/lib/python3.6/dist-packages/keras .
    cp -r ~/env/lib64/python3.6/dist-packages/* .
    