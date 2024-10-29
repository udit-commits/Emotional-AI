import boto3
from datetime import datetime


def get_user_chat(user_id):
    """
    Fetches user chat record from DynamoDB table 'user-chats' using user_id

    Args:
        user_id (str): The user ID to look up

    Returns:
        dict: The user chat record if found, None if not found
    """
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("user-chats")

    try:
        response = table.get_item(Key={"user-id": str(user_id)})
        return response.get("Item")
    except Exception as e:
        print(f"Error fetching user chat: {e}")
        return None


def add_chat_message(user_id, message, user_type):
    """
    Adds a chat message to user's chat history. Creates new record if user doesn't exist.

    Args:
        user_id (str): The user ID
        message (str): The chat message
        user_type (str): Type of user (e.g. 'user', 'assistant')
    """
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("user-chats")

    current_time = datetime.now().isoformat()
    chat_entry = (message, user_type, current_time)

    try:
        # Update existing or create new record
        response = table.update_item(
            Key={"user-id": str(user_id)},
            UpdateExpression="SET chat_history = list_append(if_not_exists(chat_history, :empty_list), :chat)",
            ExpressionAttributeValues={":chat": [chat_entry], ":empty_list": []},
            ReturnValues="UPDATED_NEW",
        )
        return response
    except Exception as e:
        print(f"Error adding chat message: {e}")
        return None
