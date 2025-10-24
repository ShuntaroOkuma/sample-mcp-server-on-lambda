import json

def handler(event, context):
    """
    A simple Lambda function that processes an event and returns a message.
    """
    print(f"Received event: {json.dumps(event)}")
    
    # If event is a string, parse it as JSON
    if isinstance(event, str):
        try:
            event = json.loads(event)
        except json.JSONDecodeError:
            # If parsing fails, treat as empty dict
            event = {}
    
    # Ensure event is a dict-like object
    if not hasattr(event, 'get'):
        event = {}

    name = event.get("name", "World")
    
    response_payload = {
        "message": f"Hello, {name}!"
    }
    
    return {
        "statusCode": 200,
        "body": json.dumps(response_payload)
    }
