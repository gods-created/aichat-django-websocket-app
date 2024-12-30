from random import choice
from string import (
    ascii_letters,
    digits
)
from cryptography.fernet import Fernet
from os import getenv
from openai import OpenAI
from json import loads

def row_to_json(row) -> dict:
    return loads(
        row.to_json()
    ) if row else {}

def generate_random_string() -> str:
    return ''.join(choice(ascii_letters + digits) for _ in range(400))

def generate_session() -> str:
    random_string = generate_random_string()
    key = Fernet.generate_key()
    f = Fernet(key)
    session = f.encrypt(random_string.encode()).decode()
    return session[:50]

def generate_ai_response(q: str) -> str:
    try:
        openai_api_key = getenv('OPENAI_API_KEY')
        if not openai_api_key:
            return 'The use of AI is not possible. Invalid API key'
        
        client = OpenAI(api_key=openai_api_key)
        completion = client.chat.completions.create(
            model='gpt-4o',
            messages=[
                {'role': 'assistant', 'content': 'You are a helpful assistant.'},
                {
                    'role': 'user',
                    'content': q
                }
            ]
        )

        return completion.choices[0].message.content
        
    except (Exception, ) as e:
        return str(e)