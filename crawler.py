from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import config


def get_all_urls(driver, keywords):
    all_urls = set()
    scroll_pause_time = 1
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

        new_urls = get_urls(driver.current_url, keywords)
        all_urls.update(new_urls)

    return list(all_urls)

def get_urls(search_url, keywords, visited=None):
    if visited is None:
        visited = set()
    urls = []

    try:
        if search_url in visited:
            return []
        visited.add(search_url)

        # Sử dụng get_all_urls để lấy tất cả các URL từ trang tìm kiếm
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(search_url)

        # Lấy tất cả các URL bằng cách cuộn trang xuống
        all_urls = get_all_urls(driver, keywords)

        time.sleep(config.RATE_LIMIT_DELAY)
        logging.info(f"Tìm thấy {len(all_urls)} URL trong {search_url}")

        driver.quit()
        return all_urls

    except Exception as e:
        logging.error(f"Lỗi khi crawl {search_url}: {e}")
        if 'driver' in locals():
            driver.quit()
        return []


    except Exception as e:
        logging.error(f"Lỗi khi crawl {search_url}: {e}")
        if 'driver' in locals():
            driver.quit()
        return []


def get_contents(url):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Không cần cuộn trang nên có thể chạy headless
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.detail-content"))
            )
        except:
            logging.warning(f"Timeout waiting for content to load on {url}")

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        title_tag = soup.select_one('h1.title, h1, h2')
        title = title_tag.text.strip() if title_tag else "Không có tiêu đề"

        content_div = soup.select_one('div.detail-content')
        content = " ".join(
            p.get_text(strip=True) for p in content_div.find_all('p')) if content_div else "Không có nội dung"

        date_tag = soup.select_one('div.timeandcatdetail span.time, time, span.date')
        date = date_tag.text.strip() if date_tag else "Không rõ ngày"

        driver.quit()
        return {
            'url': url,
            'title': title,
            'content': content,
            'date': date
        }

    except Exception as e:
        logging.error(f"Lỗi khi xử lý URL {url}: {e}")
        if 'driver' in locals():
            driver.quit()
        return None
