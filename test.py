from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(model='qwen3:30b', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
    'stream': True,
  },
])
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)