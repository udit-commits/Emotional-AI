import boto3
from datetime import datetime
import os
from typing import List, Tuple

def fetch_chats():
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user-chats')

    # Scan the entire table
    response = table.scan()
    items = response['Items']

    # Continue scanning if we have more items (pagination)
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])

    # Create output directory if it doesn't exist
    os.makedirs('chat_exports', exist_ok=True)

    # Group chats by user_id
    for item in items:
        user_id = item['user-id']
        chat_history: List[Tuple[str, str, str]] = item['chat_history']
        
        # Sort chat history by timestamp (convert to datetime for comparison)
        chat_history.sort(key=lambda x: datetime.strptime(x[2], '%Y-%m-%dT%H:%M:%S.%f'))
        
        # Calculate total time spent (difference between first and last message)
        first_time = datetime.strptime(chat_history[0][2], '%Y-%m-%dT%H:%M:%S.%f')
        last_time = datetime.strptime(chat_history[-1][2], '%Y-%m-%dT%H:%M:%S.%f')
        total_time = last_time - first_time
        total_messages = len(chat_history)
        
        # Write to individual file for each user
        filename = f'chat_exports/chat_{user_id}.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Chat Export for User {user_id} - Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Messages: {total_messages}\n")
            f.write(f"Total Time Spent: {total_time}\n")
            f.write("-" * 80 + "\n\n")
            
            for message, user_type, timestamp in chat_history:
                timestamp_dt = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')
                f.write(f"[{timestamp_dt.strftime('%Y-%m-%d %H:%M:%S')}] {user_type}:\n")
                f.write(f"{message}\n")
                f.write("-" * 40 + "\n\n")

    print(f"Successfully exported {len(items)} chat conversations to chat_exports directory")

if __name__ == "__main__":
    fetch_chats()
