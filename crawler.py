from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import config
import logging
import time
import os

def get_driver():
    """Khởi tạo trình duyệt Selenium"""
    options = Options()
    options.add_argument("--headless")  # Chạy ở chế độ ẩn
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("start-maximized")

    service = Service("chromedriver")  # Đảm bảo bạn có chromedriver trong PATH hoặc đặt đường dẫn tại đây
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def get_urls(search_url, keywords):
    """Dùng Selenium để lấy tất cả bài viết từ trang tìm kiếm"""
    driver = get_driver()
    driver.get(search_url)

    wait = WebDriverWait(driver, 10)

    urls = set()
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Cuộn xuống cuối trang
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2)  # Chờ nội dung tải thêm

        # Lấy tất cả bài viết sau khi cuộn
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for item in soup.find_all('li', class_='item'):
            link_tag = item.find('a', href=True)
            if link_tag:
                article_url = link_tag['href']
                if any(keyword.lower() in article_url.lower() for keyword in keywords):
                    urls.add(article_url)

        # Kiểm tra nếu không còn nội dung mới để tải
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    driver.quit()
    logging.info(f"Tìm thấy {len(urls)} bài viết.")
    return list(urls)

def get_contents(url):
    """Dùng Selenium để lấy nội dung bài viết"""
    driver = get_driver()
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 10)

        # Chờ tiêu đề bài viết xuất hiện
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Lấy tiêu đề bài viết
        title_tag = soup.select_one('h1.title, h1, h2')
        title = title_tag.text.strip() if title_tag else "Không có tiêu đề"

        # Lấy nội dung bài viết
        content_div = soup.select_one('div.detail-content')
        content = " ".join(p.get_text(strip=True) for p in content_div.find_all('p')) if content_div else "Không có nội dung"

        # Lấy ngày đăng bài
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
        driver.quit()
        return None
