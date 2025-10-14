import json

def handler(event, context):
    """
    A simple Lambda function that processes an event and returns a message.
    """
    print(f"Received event: {json.dumps(event)}")

    name = event.get("name", "World")
    
    response_payload = {
        "message": f"Hello, {name}!"
    }
    
    return {
        "statusCode": 200,
        "body": json.dumps(response_payload)
    }
