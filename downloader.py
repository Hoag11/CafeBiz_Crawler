import config
import logging
import os
import pandas as pd
import re
from datetime import datetime

def download(content):
    try:
        # Lấy ngày và kiểm tra định dạng
        raw_date = content['date'] or "No_Date"
        clean_date = re.sub(r'[\/*?:"<>|]', "", raw_date)  # Loại bỏ ký tự đặc biệt

        # Chuyển đổi ngày thành định dạng datetime (nếu có thể)
        try:
            parsed_date = datetime.strptime(clean_date, '%d/%m/%Y')
            month_year = parsed_date.strftime('%Y-%m')
        except ValueError:
            logging.warning(f"Không thể phân tích ngày: {raw_date}")
            month_year = "Unknown_Month"

        # Đường dẫn file theo tháng
        file_name = f"{month_year}.csv"
        file_path = os.path.join(config.folder_path, file_name)


        df = pd.DataFrame([content])

        if os.path.exists(file_path):
            existing_df = pd.read_csv(file_path)
            combined_df = pd.concat([existing_df, df], ignore_index=True)
            combined_df.to_csv(file_path, index=False)
        else:
            df.to_csv(file_path, index=False)

        logging.info(f"Đã lưu bài viết vào {file_path}")

    except Exception as e:
        logging.error(f"Lỗi khi tải bài viết từ {content['url']}: {e}")
