import logging
from fake_useragent import UserAgent
import os
from urllib.parse import urlencode

def get_search_url(keywords):
    if not keywords:
        logging.warning("Danh sách từ khóa rỗng! Không thể tạo URL.")
        return None
    query = urlencode({"keywords": ",".join(keywords)})
    return f'https://cafebiz.vn/search.chn?{query}'

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawler.log'),
        logging.StreamHandler()
    ]
)

# Cấu hình User-Agent ngẫu nhiên
ua = UserAgent()
HEADER = {
    'User-Agent': ua.random,
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

# Cấu hình thư mục lưu dữ liệu
folder_path = 'contents'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
