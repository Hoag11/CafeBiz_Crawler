import logging
import crawler
import config
import downloader
import concurrent.futures

keywords = []

def main():
    logging.info("Bắt đầu quy trình crawl.")

    urls = crawler.get_urls(config.url, keywords=keywords)

    all_contents = []

    for url in urls:
        logging.info(f"Đang xử lý URL: {url}")
        content = crawler.get_contents(url)
        if content:
            all_contents.append(content)

    max_workers = 60
    logging.info(f"Bắt đầu tải xuống {len(all_contents)} bài viết với {max_workers} workers.")
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(downloader.download, all_contents)

    logging.info("Quy trình crawl hoàn tất.")

if __name__ == "__main__":
    keyword = input("Nhập từ khóa cần tìm: ")
    for key in keyword.split(","):
        keyword = key.strip()
        keywords.append(keyword)
    main()
