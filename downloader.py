import config
import logging
import os
import pandas as pd

def download(content):
    try:
        name = f"{content['date']}-{content['title']}".replace(' ', '_').replace('/', '-')
        content_name = f'{name}.txt'
        content_path = os.path.join(config.folder_path, content_name)

        df = pd.DataFrame([content])
        df.to_csv(content_path, index=False)
        logging.info(f"Đã tải xuống {content_path}")

    except Exception as e:
        logging.error(f"Lỗi khi tải xuống {content['url']}: {e}")