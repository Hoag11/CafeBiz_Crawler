import os
import pandas as pd

def merge_csv_files(output_file="summary.csv"):
    folder_path = 'FLC'
    all_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

    if not all_files:
        print("Không tìm thấy file CSV nào trong thư mục.")
        return

    merged_df = pd.concat(
        [pd.read_csv(os.path.join(folder_path, f), dtype=str) for f in all_files],
        ignore_index=True
    )

    output_path = os.path.join(folder_path, output_file)
    merged_df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Đã tạo file tổng hợp: {output_path}")

merge_csv_files()
