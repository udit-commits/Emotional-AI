import json


# import requests
# def invoke_llm():
#     response = requests.post(
#     url="https://openrouter.ai/api/v1/chat/completions",
#     headers={
#         "Authorization": f"Bearer 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",
#     },
#     data=json.dumps({
#         "model": "openai/gpt-4o-mini", # Optional
#         "messages": [
#         {
#             "role": "user",
#             "content": "What is the meaning of life?"
#         }
#         ]
#     })
#     )
#     return response
def lambda_handler(event, context):
    # print(invoke_llm())
    return {
        "statusCode": 200,
        "body": json.dumps("Hello Im emotional AI assistant local change "),
    }
