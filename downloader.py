import config
import logging
import os
import pandas as pd
import csv
import glob

def escape_csv_value(value):
    if isinstance(value, str):
        value = value.replace('"', '""')  # Escape dấu `"`
        return f'"{value}"'
    return value

def download(content):
    try:
        if not content or 'url' not in content or not content['url']:
            logging.warning("Bỏ qua bài viết không hợp lệ.")
            return

        # Xác định ngày đăng bài
        article_date = content.get('date', 'Không rõ ngày').replace("/", "-")
        article_title = content.get('title', 'Không có tiêu đề')

        # Xây dựng đường dẫn file riêng lẻ
        file_name = f"{article_date}_{article_title[:150]}.csv"
        folder_path = config.folder_path
        file_path = os.path.join(folder_path, file_name)

        # Xử lý dữ liệu
        escaped_content = {key: escape_csv_value(value) for key, value in content.items()}
        df = pd.DataFrame([escaped_content])

        # Lưu vào file riêng lẻ
        df.to_csv(file_path, index=False, sep=",", quoting=csv.QUOTE_ALL, encoding="utf-8")
        logging.info(f"Đã lưu bài viết vào {file_path}")

    except Exception as e:
        logging.error(f"Lỗi khi tải bài viết từ {content.get('url', 'Không rõ URL')}: {e}")

def merge_and_cleanup():
    try:
        folder_path = config.folder_path
        summary_file = os.path.join(folder_path, "summary.csv")

        # Lấy danh sách tất cả các file CSV riêng lẻ
        all_files = glob.glob(os.path.join(folder_path, "*.csv"))
        all_files.remove(summary_file) if summary_file in all_files else None

        if not all_files:
            logging.info("Không có file nào để gộp.")
            return

        # Đọc tất cả các file CSV và gộp lại
        merged_df = pd.concat(
            [pd.read_csv(f, dtype=str, on_bad_lines="skip") for f in all_files],
            ignore_index=True
        )

        # Lưu file tổng hợp
        merged_df.to_csv(summary_file, index=False, sep=",", quoting=csv.QUOTE_ALL, encoding="utf-8")
        logging.info(f"Đã tạo file tổng hợp: {summary_file}")

        # Xóa các file riêng lẻ sau khi tổng hợp
        for f in all_files:
            os.remove(f)
            logging.info(f"Đã xóa file: {f}")

    except Exception as e:
        logging.error(f"Lỗi khi tổng hợp: {e}")
