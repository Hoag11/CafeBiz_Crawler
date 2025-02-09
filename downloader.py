import config
import logging
import os
import pandas as pd
import csv
from datetime import datetime

def escape_csv_value(value):
    if isinstance(value, str):
        if ',' in value or '\n' in value or '"' in value:
            value = value.replace('"', '""')  # Escape dấu `"`
            return f'"{value}"'
    return value

def download(content):
    try:
        if not content or 'url' not in content or not content['url']:
            logging.warning("Bỏ qua bài viết không hợp lệ.")
            return

        # Xác định ngày đăng bài
        article_date = content.get('date', 'Không rõ ngày').format('%Y-%m-%d')
        article_title = content.get('title', 'Không có tiêu đề')

        # Xây dựng đường dẫn file
        file_name = f"{article_date}_{article_title}.csv"
        folder_path = config.folder_path
        file_path = os.path.join(folder_path, file_name)

        # Xử lý dữ liệu
        escaped_content = {key: escape_csv_value(value) for key, value in content.items()}
        df = pd.DataFrame([escaped_content])

        file_exists = os.path.exists(file_path) and os.stat(file_path).st_size > 0

        if file_exists:
            existing_df = pd.read_csv(file_path, dtype=str)
            if content['url'] in existing_df['url'].values:
                logging.info(f"Bài viết {content['url']} đã tồn tại, bỏ qua.")
                return
            combined_df = pd.concat([existing_df, df], ignore_index=True)
            combined_df.to_csv(file_path, index=False, sep=",", quoting=csv.QUOTE_MINIMAL, escapechar="\\", encoding="utf-8")
        else:
            df.to_csv(file_path, index=False, sep=",", quoting=csv.QUOTE_MINIMAL, escapechar="\\", encoding="utf-8")

        logging.info(f"Đã lưu bài viết vào {file_path}")

    except Exception as e:
        logging.error(f"Lỗi khi tải bài viết từ {content.get('url', 'Không rõ URL')}: {e}")
