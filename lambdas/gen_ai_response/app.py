import json
import requests

API_KEY = "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"
from telegram_helper import send_message


def invoke_llm(query):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
        },
        data=json.dumps(
            {
                "model": "openai/gpt-4o-mini",
                "messages": [{"role": "user", "content": query}],
                "max_tokens": 30,  # Limit response length to 30 tokens
            }
        ),
    )
    return response.json()


def lambda_handler(event, context):
    print("Event ", event)
    print("Context ", context)
    telegram_message = event["message"]

    query = telegram_message["text"]
    user_id = telegram_message["from"]["id"]

    print("Query ", query)
    print("User id ", user_id)
    llm_response = invoke_llm(query)
    send_message(
        telegram_message["chat"]["id"], llm_response["choices"][0]["message"]["content"]
    )
    return {"statusCode": 200, "body": llm_response["choices"][0]["message"]["content"]}
