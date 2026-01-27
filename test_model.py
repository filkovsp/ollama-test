from ollama import chat
from ollama import ChatResponse

from dotenv import load_dotenv
load_dotenv()  # Loads from .env file


if __name__ == "__main__":
    response: ChatResponse = chat(
            model='gpt-oss:20b',
            messages=[
                {
                    'role': 'user',
                    'content': "Hi, who are you?",
                },
            ]
        )
    
    print(response.message.content)