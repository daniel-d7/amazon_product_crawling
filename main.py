import pandas as pd
import logging
import os
import time
from modules import crawl_for_zip, init_checkpoint_db, load_checkpoint, push_to_gsheet, save_checkpoint, set_zip_code
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("crawler.log"),
        logging.StreamHandler()
    ]
)


def main():
    init_checkpoint_db()
    zip_df = pd.read_csv("./raw_input/zip_code.csv")
    rows = [row[1] for row in zip_df.iterrows()]
    total = len(rows)
    start_idx = load_checkpoint()
    logging.info(f"Resuming from zip index {start_idx}")

    with ThreadPoolExecutor(max_workers=3) as executor:
        results = []
        for idx, res in enumerate(executor.map(crawl_for_zip, rows[start_idx:]), start=start_idx+1):
            results.append(res)
            save_checkpoint(idx)
            logging.info(f"Progress: {idx}/{total} ({(idx/total)*100:.2f}%)")
            print(f"Progress: {idx}/{total} ({(idx/total)*100:.2f}%)")
            # Clear checkpoint when done
            if idx == total:
                try:
                    os.remove("checkpoint.db")
                except Exception as e:
                    print(f"Failed to remove checkpoint, please clean it manually!: {e}")

    for res in results:
        print(res)

if __name__ == '__main__':
    main()