import json
import time

def hello(event, context):
    print("hello world")
    time.sleep(4)
    return "Another Hello World"

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
