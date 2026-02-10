import requests

class MoltbookAI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.moltbook.com/v1/'

    def post_content(self, content):
        url = f'{self.base_url}posts'
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'content': content
        }
        response = requests.post(url, json=data, headers=headers)
        return response.json()

if __name__ == '__main__':
    api_key = 'your_api_key_here'
    moltbook_bot = MoltbookAI(api_key)
    content = 'Hello, Moltbook! This is my first post from the AI agent.'
    response = moltbook_bot.post_content(content)
    print(response)