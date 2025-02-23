import config
import logging
import os
import pandas as pd
import csv

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

        # Xử lý dữ liệu
        escaped_content = {key: escape_csv_value(value) for key, value in content.items()}
        df = pd.DataFrame([escaped_content])

        summary_file = os.path.join(config.folder_path, "summary.csv")

        file_exists = os.path.exists(summary_file) and os.stat(summary_file).st_size > 0

        if file_exists:
            try:
                existing_df = pd.read_csv(summary_file, dtype=str, on_bad_lines="skip")
            except Exception as e:
                logging.error(f"Lỗi khi đọc file summary.csv: {e}")
                return

            if content['url'] in existing_df.get("url", []):
                logging.info(f"Bài viết {content['url']} đã tồn tại trong summary.csv, bỏ qua.")
                return

            combined_df = pd.concat([existing_df, df], ignore_index=True)
        else:
            combined_df = df

        combined_df.to_csv(summary_file, index=False, sep=",", quoting=csv.QUOTE_ALL, encoding="utf-8")

        logging.info(f"Đã lưu bài viết vào {summary_file}")

    except Exception as e:
        logging.error(f"Lỗi khi tải bài viết từ {content.get('url', 'Không rõ URL')}: {e}")
