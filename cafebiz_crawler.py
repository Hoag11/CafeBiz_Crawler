from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import logging
import re
import config

def get_all_urls(driver, keywords):
    all_urls = set()
    scroll_pause_time = 8
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

        try:
            more_button = driver.find_element(By.CSS_SELECTOR, "div.list__viewmore a.more")
            if more_button.is_displayed():
                ActionChains(driver).move_to_element(more_button).click().perform()
                time.sleep(scroll_pause_time)
        except Exception:

            pass

        page_urls = extract_urls(driver, keywords)
        all_urls.update(page_urls)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    return list(all_urls)

def extract_urls(driver, keywords):
    urls = set()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    for link in soup.find_all('a', href=True):
        article_url = link['href']
        if any(keyword.lower() in article_url.lower() for keyword in keywords):
            urls.add(article_url)

    return list(urls)

def get_urls(search_url, keywords):
    urls = []

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument(f'user-agent={config.HEADER["User-Agent"]}')

    try:
        driver = webdriver.Chrome(options=options)
        driver.get(search_url)

        # Gọi hàm get_all_urls để lấy tất cả URL trên trang
        all_urls = get_all_urls(driver, keywords)
        logging.info(f"Tìm thấy {len(all_urls)} URL trong {search_url}")

        driver.quit()
        return all_urls

    except Exception as e:
        logging.error(f"Lỗi khi crawl {search_url}: {e}")
        if 'driver' in locals():
            driver.quit()
        return []


def get_contents(url):
    try:
        if not url.startswith("http"):
            url = "https://cafebiz.vn" + url
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument(f'user-agent={config.HEADER["User-Agent"]}')
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
        date = re.sub(r'[/]', '-', date)
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


