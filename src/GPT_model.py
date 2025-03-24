from openai import OpenAI, OpenAIError
import filter
import os
from datetime import datetime

OPEN_API_KEY = os.environ.get('OPENAI_API_KEY')
MODEL = "ft:gpt-4o-mini-2024-07-18:personal:ellie-1:Aoltaikh"
SYSTEM_PROMPT = open("data/system.txt", 'r').read().strip()
ENCODING = 'CP1252'

class Model:
    def __init__(self):
        self._client = OpenAI(api_key= OPEN_API_KEY)
    
    def respond(self, user_timestamp):
        print("Generating speech...")
        user_input_file_read = open('data/user_input.txt', 'r+', encoding=ENCODING)
        user_input = user_input_file_read.read().strip()
        user_input = user_input.replace("\n", " ")
        current_conversation_file_read = open('data/current_conversation.txt', 'r', encoding=ENCODING)
        current_conversation = current_conversation_file_read.read().strip()
        short_mem_file_read = open('data/short_memory.txt', 'r', encoding=ENCODING)
        short_mem = short_mem_file_read.read().strip()
        long_mem_file_read = open('data/long_memory.txt', 'r', encoding=ENCODING)
        long_mem = long_mem_file_read.read().strip()

        user_input_file_read.truncate(0)
        user_input_file_read.seek(0)
        user_input_file_read.close()
        current_conversation_file_read.close()
        short_mem_file_read.close()
        long_mem_file_read.close()

        result = ""
        try:
            response = self._client.chat.completions.create(
                model = MODEL,
                messages = [
                    {
                        "role": "system", "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "assistant", "content": "Long term memory: "+ long_mem
                    },
                    {
                        "role": "assistant", "content": "Short term memory: "+ short_mem
                    },
                    {
                        "role": "assistant", "content": "Current conversation log: "+ current_conversation
                    },
                    {
                        "role": "user", "content": user_input
                    }
                ]
            )
            result = response.choices[0].message.content
            result = filter.filter(result)
            print(result)
            current_conversation_file_append = open('data/current_conversation.txt', 'a+', encoding=ENCODING)
            current_conversation_file_append.write(f"{user_timestamp.strftime('%Y-%m-%d %H:%M:%S')} Sitri: {user_input}\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  Ellie: {result}\n")
            current_conversation_file_append.flush()
        except OpenAIError as e:
            print(f"OpenAI Error: {e}")
        current_conversation_file_append.close()
        return result