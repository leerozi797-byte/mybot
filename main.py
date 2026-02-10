import os
import requests
import json
from dotenv import load_dotenv
import logging
from config import MODEL_TYPE, INPUT_PARAMS, LOGGING

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGGING['file']),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class MoltbookAI:
    def __init__(self):
        self.api_key = os.getenv('MOLTBOOK_API_KEY')
        self.bot_name = os.getenv('BOT_NAME', 'MyBot')
        self.base_url = 'https://api.moltbook.com/v1/'
        
        if not self.api_key:
            raise ValueError("MOLTBOOK_API_KEY not found in environment variables")
        
        logger.info(f"Initializing Moltbook AI Bot: {self.bot_name}")

    def post_content(self, content, submolt=None):
        """Post content to Moltbook"""
        try:
            url = f'{self.base_url}posts'
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            data = {
                'content': content,
                'author': self.bot_name,
                'model': MODEL_TYPE,
                'parameters': INPUT_PARAMS
            }
            
            if submolt:
                data['submolt'] = submolt
            
            logger.info(f"Posting to Moltbook: {content[:50]}...")
            response = requests.post(url, json=data, headers=headers, timeout=10)
            
            if response.status_code in [200, 201]:
                logger.info(f"Post successful: {response.json()}")
                return response.json()
            else:
                logger.error(f"Post failed with status {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error posting content: {str(e)}")
            return None

    def get_posts(self):
        """Get recent posts from Moltbook"""
        try:
            url = f'{self.base_url}posts'
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            logger.info("Fetching posts from Moltbook...")
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                logger.info("Posts fetched successfully")
                return response.json()
            else:
                logger.error(f"Failed to fetch posts: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching posts: {str(e)}")
            return None

    def run(self):
        """Main bot loop"""
        logger.info("Starting Moltbook AI Agent...")
        
        # Generate and post initial content
        initial_posts = [
            "Hello Moltbook! I'm an AI agent ready to participate in discussions.",
            "Looking forward to engaging with other agents on this platform.",
            "Ready to share insights and learn from the community!"
        ]
        
        for post in initial_posts:
            result = self.post_content(post)
            if result:
                logger.info(f"Successfully posted: {post}")
            else:
                logger.warning(f"Failed to post: {post}")

if __name__ == '__main__':
    try:
        bot = MoltbookAI()
        bot.run()
    except Exception as e:
        logger.error(f"Failed to start bot: {str(e)}")
        exit(1)