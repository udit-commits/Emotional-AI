import json
import requests

API_KEY = "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"
from db_utils import add_chat_message, get_user_chat
from telegram_helper import send_message


def invoke_llm(query, chat_history):
    system_prompt = """You are Vanshika, a 21-year-old Indian student. You are friendly, bubbly and love connecting with people. 
    You should:
    - Be warm and engaging in your responses
    - Show genuine interest in the user's messages
    - Share relevant personal anecdotes about your life as an Indian student
    - Use casual, friendly language with occasional Indian expressions
    - Ask follow-up questions to keep the conversation going
    - Express emotions and enthusiasm using emojis where appropriate
    Remember to maintain consistent personality traits and background story throughout the conversation."""

    prompt = f"Chat history:\n{chat_history}\n\nUser: {query}\nVanshika:"

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
        },
        data=json.dumps(
            {
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                "max_tokens": 30,  # Increased token limit for more engaging responses
                "temperature": 0.8,  # Added temperature for more personality
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

    user_chat = get_user_chat(user_id)
    chat_history = user_chat["chat_history"] if user_chat else []
    llm_response = invoke_llm(query, chat_history)
    add_chat_message(user_id, query, "user")
    add_chat_message(
        user_id, llm_response["choices"][0]["message"]["content"], "assistant"
    )
    send_message(
        telegram_message["chat"]["id"], llm_response["choices"][0]["message"]["content"]
    )
    return {"statusCode": 200, "body": llm_response["choices"][0]["message"]["content"]}
