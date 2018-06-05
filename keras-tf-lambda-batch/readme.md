### Build Docker Image
First, we build a Docker Image that returns the bottleneck features for an input image.

See the [batch](./batch) directory for the completed [Dockerfile](./batch/Dockerfile) and the completed [python script](./batch/src/record_bottleneck.py).

`docker build -t serverless_imagenet_bottleneck`

### Register Docker Image to AWS ECR
1. Navigate to the [ECS Console](https://console.aws.amazon.com/ecs)
2. Click "Repositories" on the left.
3. Click "Create Repositories".
4. Follow the directions.

### Create AWS Batch Job Definition
1. Navigate to the [AWS Batch Console](https://console.aws.amazon.com/batch/)
1. Create GPU-Compute Environment
	1. Select p2 family
	2. Use custom AMI created above
	3. Use all other defaults
2. Create Job Queue
	1. Set 1 as priority
	2. Select compute env from above
3. Create Job Definition
	1. In "Container Image", input the ECS Repository URI from above
	2. Leave everything else as default
4. Submit a job
	1. Use the Job Definition from above
	2. Use the Job Queue from above
	3. Submit!

### Create AWS Lambda Function
