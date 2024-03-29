# Serverless

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
