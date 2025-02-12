import logging
import config
import downloader
import concurrent.futures
import cafebiz_crawler
import vneconomy_crawler

keywords = []


def main(choice):
    logging.info("Bắt đầu quy trình crawl.")

    if choice == 1:
        search_url = config.get_search_url(keywords)
        crawler_module = cafebiz_crawler
    elif choice == 2:
        search_url = config.get_vneconomy_url(keywords)
        crawler_module = vneconomy_crawler
    else:
        logging.error("Lựa chọn không hợp lệ.")
        return

    if not search_url:
        logging.error("Không có URL hợp lệ để crawl. Dừng chương trình.")
        return

    urls = crawler_module.get_urls(search_url, keywords=keywords)

    if not urls:
        logging.info("Không tìm thấy bài viết nào.")
        return

    all_contents = []

    for url in urls:
        logging.info(f"Đang xử lý URL: {url}")
        content = crawler_module.get_contents(url)
        if content:
            all_contents.append(content)

    if not all_contents:
        logging.info("Không có nội dung nào để tải xuống.")
        return

    max_workers = 30
    logging.info(f"Bắt đầu tải xuống {len(all_contents)} bài viết với {max_workers} workers.")

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(lambda content: downloader.download(content), all_contents)

    logging.info("Quy trình crawl hoàn tất.")


if __name__ == "__main__":
    keyword = input("Nhập từ khóa cần tìm: ")
    choice = int(input("Chọn trang web cần tìm kiếm (1: CafeBiz, 2: VnEconomy): "))

    keywords = [key.strip() for key in keyword.split(",")]

    main(choice)
