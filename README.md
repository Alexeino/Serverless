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
