import json
import boto3
from awslabs.mcp_lambda_handler import MCPLambdaHandler

# MCPLambdaHandlerのインスタンスを作成
mcp = MCPLambdaHandler(
    name="Lambda Invoker MCP Server",
    version="1.0.0"
)

# Boto3 Lambdaクライアントを初期化
lambda_client = boto3.client('lambda')

@mcp.tool()
def invoke_lambda_sync(function_name: str, payload: dict) -> dict:
    """
    Invokes an AWS Lambda function synchronously and returns its response.
    
    :param function_name: The name of the Lambda function to invoke.
    :param payload: A JSON serializable object to be sent as the payload.
    :return: The response from the Lambda function.
    """
    print(f"Invoking function '{function_name}' synchronously with payload: {payload}")
    try:
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',  # 同期呼び出し
            Payload=json.dumps(payload).encode('utf-8')
        )
        result_payload = response['Payload'].read().decode('utf-8')
        # 呼び出し先のLambdaが返すbodyもJSON文字列の場合、二重にパースが必要
        inner_result = json.loads(result_payload)
        if "body" in inner_result and isinstance(inner_result["body"], str):
             inner_result["body"] = json.loads(inner_result["body"])
        return inner_result
    except Exception as e:
        print(f"[ERROR] Failed to invoke function '{function_name}': {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error_type": type(e).__name__,
                "error_message": str(e)
            })
        }

@mcp.tool()
def invoke_lambda_async(function_name: str, payload: dict) -> dict:
    """
    Invokes an AWS Lambda function asynchronously.
    
    :param function_name: The name of the Lambda function to invoke.
    :param payload: A JSON serializable object to be sent as the payload.
    :return: A confirmation message.
    """
    print(f"Invoking function '{function_name}' asynchronously with payload: {payload}")
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='Event',  # 非同期呼び出し
        Payload=json.dumps(payload).encode('utf-8')
    )
    return {
        "status": "Request accepted for asynchronous execution.",
        "statusCode": response.get('StatusCode')
    }

def handler(event, context):
    """AWS Lambda handler function."""
    return mcp.handle_request(event, context)
