import requests
from pprint import pprint
from api import io

url = "https://api.intelligence.io.solutions/api/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": io}

data = {
    "model": "deepseek-ai/DeepSeek-R1-0528",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant"
        },
        {
            "role": "user",
            "content": "just say Hi."
        }
    ],
}

response = requests.post(url, headers=headers, json=data)
data = response.json()
pprint(data) 

text = data['choices'][0]['message']['content']
text = text.split('/think')[1][2:]