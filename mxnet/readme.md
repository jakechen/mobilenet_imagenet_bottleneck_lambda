Spin up EC2 instance with Public Amazon Linux AMI, defined [here](https://docs.aws.amazon.com/lambda/latest/dg/current-supported-versions.html)

Instructions:
```Shell
	virtualenv -p python27 env

	# Install OS and Python libraries/packages
	pip install mxnet
	sudo yum install libgomp

	# Copy files out of virtualenv
	cp -r env/lib/python2.7/site-packages/* .
	cp -r env/lib64/python2.7/site-packages/* .

	# Zip up deployment package
	zip -r -9 --exclude="*.pyc" ../lambda.zip ./*
```
