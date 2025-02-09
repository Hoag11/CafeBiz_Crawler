from bs4 import BeautifulSoup
import config
import logging
import requests
from urllib.parse import urljoin

def get_urls(search_url, keywords, visited=None):
    if visited is None:
        visited = set()

    try:
        if search_url in visited:
            return []
        visited.add(search_url)

        response = requests.get(search_url, headers=config.HEADER)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        urls = []
        for item in soup.find_all('li', class_='item'):
            link_tag = item.find('a', href=True)
            if link_tag:
                article_url = urljoin(search_url, link_tag['href'])
                if any(keyword.lower() in article_url.lower() for keyword in keywords):
                    urls.append(article_url)

        logging.info(f"Tìm thấy {len(urls)} bài viết trong {search_url}")
        return urls

    except Exception as e:
        logging.error(f"Lỗi khi crawl {search_url}: {e}")
        return []

def get_contents(url):
    try:
        response = requests.get(url, headers=config.HEADER)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Lấy tiêu đề bài viết
        title_tag = soup.select_one('h1.title, h1, h2')
        title = title_tag.text.strip() if title_tag else "Không có tiêu đề"

        # Lấy nội dung bài viết
        content_div = soup.select_one('div.detail-content')
        content = " ".join(p.get_text(strip=True) for p in content_div.find_all('p')) if content_div else "Không có nội dung"

        # Lấy ngày đăng bài
        date_tag = soup.select_one('div.timeandcatdetail span.time, time, span.date')
        date = date_tag.text.strip() if date_tag else "Không rõ ngày"

        return {
            'url': url,
            'title': title,
            'content': content,
            'date': date
        }
    except Exception as e:
        logging.error(f"Lỗi khi xử lý URL {url}: {e}")
        return None
