import requests
from bs4 import BeautifulSoup
import config
import logging

#crawl url
def get_urls(url, keywords, visited=None):
    if visited is None:
        visited = set()

    try:
        if url in visited:
            return []
        visited.add(url)
        response = requests.get(url, headers=config.HEADER)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        urls = []

        for loc in soup.find_all('loc'):
            url = loc.text.strip()
            if any(keyword in loc.text for keyword in keywords):
                urls.append(loc.text)

            elif url.endswith('.xml'):
                urls.extend(get_urls(url, keywords, visited))

        logging.info(f'Tìm thấy {len(urls)} urls trong {url}')
        return urls

    except Exception as e:
        logging.error(f'Lỗi khi crawl {url}: {e}')
        return []

#crawl noi dung trang
def get_contents(url):
    try:
        response = requests.get(url, headers=config.HEADER)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Lấy tiêu đề bài viết
        title = soup.find('h1', class_='title').text.strip() if soup.find('h1', class_='title') else None

        # Lấy nội dung từ các thẻ <p> trong thẻ div class="content"
        content_div = soup.find('div', class_='detail-content')
        content = ' '.join(p.get_text(strip=True) for p in content_div.find_all('p')) if content_div else None

        # Lấy ngày đăng bài
        date_div = soup.find('div', class_='timeandcatdetail')
        date = None
        if date_div:
            date_span = date_div.find('span', class_='time')  # Tìm thẻ span trong div
            date = date_span.text.strip() if date_span else None
        return {
            'url': url,
            'title': title,
            'content': content,
            'date': date
        }
    except Exception as e:
        logging.error(f"Lỗi khi xử lý URL {url}: {e}")
        return None