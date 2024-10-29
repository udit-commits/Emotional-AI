import json
import requests

API_KEY = "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"


def invoke_llm():
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
        },
        data=json.dumps(
            {
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {"role": "user", "content": "What is the meaning of life?"}
                ],
                "max_tokens": 10,  # Limit response length to 300 tokens
            }
        ),
    )
    return response.json()


def lambda_handler(event, context):
    llm_response = invoke_llm()
    return {"statusCode": 200, "body": llm_response["choices"][0]["message"]["content"]}
