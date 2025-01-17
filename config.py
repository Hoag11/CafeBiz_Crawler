import logging
from fake_useragent import UserAgent
import os

url = 'https://cafebiz.vn/sitemap.xml'

#logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawler.log'),
        logging.StreamHandler()
    ]
)

#random User-Agent configuration
ua = UserAgent()
HEADER = {
    'User-Agent': ua.random,
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

#file path configuration
folder_path = 'contents'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)