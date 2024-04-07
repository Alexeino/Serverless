# Serverless

* Serverless config
``` sls config credentials --provider aws --key YOUR_ACCESS_KEY --secret YOUR_SECRET_KEY --profile PROFILE_NAME ```<br>

* Creating a Serverless Application <br>
``` serverless ```
* Deploying the Serverless Application (Complete Stack) <br>
``` serverless deploy ```
* Deploying the Serverless Application (Function Only) <br>
``` serverless deploy function -f <function_name> ```
* Invoking a Lambda Function Locally <br>
``` serverless invoke local --function <function_name> ``` or<br>
``` serverless invoke --function <function_name> ```
* Invoking a Lambda function locally with log message <br>
``` serverless invoke --function <function_name> --log ```
* Seeing CloudWatch Logs of a function <br>
``` serverless logs --function <function_name> ```
* Removing Serverless Project and Stack <br>
``` serverless remove ```
<br>

<br>
* Creating Serverless Project from a template <br>
``` serverless create --template <template_name> --path <project_folder> ```

## Timeout & Memory

* Since Lambda functions are billed on execution time and memory utilized, It's important to specify the timeout and memory size for each lambda function.

```
functions:
  hello-short-timeout:
    handler: handler.hello
    timeout: 3 
    memorySize: 128
    description: Short timeout function
```

* It makes sure that if something goes wrong with lambda function and it's stuck somewhere in the code such as slow response from an external api, timeout would make sure that cost would be controlled.

* In Production environment it's good to use description to state the purpose of the function.

## Using Provider for common settings

* For Common settings for multiple functions or resources we can specify attributes in the provider section.

```
provider:
  name: aws
  runtime: python3.9
  timeout: 2
  memorySize: 128
  ```

* This will apply to all the function unless attributes are defined explicitly.

## IAM Authorization for Lambda project-3

* By default, Lambda functions are not authorized to access any AWS resources or services such as S3, DynamoDB etc.
* For this we need to provide IAM policy to allow the access to specific AWS resources.

```
provider:
  name: aws
  runtime: python3.9

  # IAM Policy
  iam:
    role:
      statements:
        - Effect: "Allow"
          Action:
            - "lambda:*" # Allow all actions such as list_functions() etc.
          Resource:
            - "*" # Allow to all Lambda Functions in the account
```

* This IAM policy will allow our lambda function to allow all actions on the lambda functions in same account.

## Environment Variables in Serverless project-4

* Using environment variables.

```
provider:
  name: aws
  runtime: python3.9
  environment:
    PROJECT_NAME: 'DE_WHS_TOOLS' # Common to all functions

functions:
  hello-env-de:
    handler: handler.hello
  hello-env-tie:
    handler: handler.hello
    environment:
      PROJECT_NAME: 'TIE_TOOLS' # Specific to this function
```

# AWS SAM

* Creating a SAM application<br>
``` sam init ```
* Creating artifactory through SAM build<br>
``` sam build ```
* Deploying App to the AWS Cloudformation Stack<br>
``` sam deploy --guided ``` (first time)<br> 
``` sam deploy ```
* Deploying Serverless API locally<br>
``` sam local start-api ```
> **Note** During Local development after making changes to the code re-build the App and restart the local server for changes to be reflected locally
* Invoking a SAM lambda funtion locally with event.json<br>
``` sam local invoke -e event.json ```


> List Items in AWS bucket<br>
``` aws s3 ls <bucket-name>/ ``` <br>
Emptying a bucket<br>
``` aws s3 rm "s3://<bucket-name>/" --recursive ```

# Thumbnail Generator App (Serverless)
This small app lisntes on the ObjectCreated event on S3 bucket and then creates a thumbnail PNG out of the uploaded image.
It uses Pillow for Image resizing and returns a Presigned URL which can be used for downloading the thumbnail which is valid for 3600 seconds.

### STEPS
1. Create a Serverless App using Starter Template (Python)
``` serverless ```
2. Add the following components one by one to ther **serverless.yamls**
```
provider:
  name: aws
  runtime: python3.10
  timeout: 20                           # Timeout and Memory
  memorySize: 256
  region: eu-north-1
  profile: dev                          # Serverless Profile Name
  stage: dev                            # Stage Dev
  environment:                          # ENV vars
    THUMBNAIL_SIZE: 128
    REGION_NAME: ${self:provider.region}
```
3. IAM Roles to allow access the S3 bucket contents under provider
```
provider:
...
  iam:
    role:
      statements:
        - Effect: 'Allow'
          Resource: '*'
          Action: 's3:*' 
```
4. custom section to define custom variables to be used in serverless.yaml
```
custom:
  bucket: alexeino-thumbnails
  pythonRequirements:
    dockerizePip: true
```
5. Add s3 event to the handler function which adds s3:ObjectCreated as trigger
```
functions:
  generator:
    handler: handler.thumbnail_generator
    events:
      - s3:
          bucket: ${self:custom.bucket}
          event: s3:ObjectCreated:*
          rules:
            - suffix: .png
```
6. Add serverless-python-requirements plugin for making requirements.txt to work.
```
plugins:
  - serverless-python-requirements
```
7. Define your handler method as you want, add requirements.txt and deploy it.
``` sls deploy ```

> **Note** In order to invoke the function locally which uses requirements.txt we will need to install serverless-python-requirements inside the project root dir otherwise we can't invoke this function locally. So Use ``` sls install -g serverless-python-requirements ``` inside project dir before using ``` sls invoke -f <function-name> ```