import pandas as pd
import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import time


def crawl_for_zip(row):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    results = []
    country = row["country"]

    logging.info(f"Starting crawl for country: {country}, zip: {row.get('part1', '')} {row.get('part2', '')}")

    if country == "can":
        driver.get("https://www.amazon.ca")
    elif country == "uk":
        driver.get("https://www.amazon.co.uk")
    else:
        driver.get("https://www.amazon.de")

    time.sleep(5)

    while True:
        try:
            element = driver.find_element(By.XPATH, "//button[contains(text(), 'Continue shopping')]")
            element.click()
            time.sleep(1)
        except NoSuchElementException:
            break

    if country in ["can", "uk"]:
        zip_code_p1 = row["part1"]
        zip_code_p2 = row["part2"]
        set_zip_code(driver, zip_code_p1, zip_code_p2, 2)
    else:
        zip_code = row["part1"]
        try:
            zip_code_legend_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "GLUXZipUpdateInput"))
            )
            zip_code_legend_input.clear()
            zip_code_legend_input.send_keys(zip_code)
            zip_code_legend_input.send_keys(Keys.ENTER)
            time.sleep(3)
        except Exception:
            pass

    asin_df = pd.read_csv("./raw_input/asin.csv")
    if country == "can":
        asin_df = asin_df[asin_df["COUNTRY"] == "CAN"]
    elif country == "uk":
        asin_df = asin_df[asin_df["COUNTRY"] == "GBR"]
    else:
        asin_df = asin_df[asin_df["COUNTRY"] == "DEU"]

    asin_list = asin_df['ASIN'].dropna().tolist()

    for asin in asin_list:
        url = f"https://www.amazon.ca/dp/{asin}?th=1"
        driver.get(url)
        time.sleep(3)
        try:
            product_title = driver.find_element(By.ID, "productTitle").text.strip()
        except:
            product_title = "Title not found"
        try:
            product_price = driver.find_element(By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[3]/span[2]/span[2]').text.strip()
        except:
            product_price = "Price not found"
        try:
            product_discount = driver.find_element(By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[2]').text.strip()
        except:
            product_discount = "Discount not found"
        try:
            product_rating = driver.find_element(By.XPATH, '//*[@id="acrPopover"]/span/a/span').text.strip()
        except:
            product_rating = "Rating not found"
        try:
            product_total_review = driver.find_element(By.XPATH, '//*[@id="acrPopover"]/span').text.strip()
        except:
            product_total_review = "Total review not found"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        results.append({
            'Timestamp': timestamp,
            'ASIN': asin,
            'Title': product_title,
            'Price': product_price,
            'Discount': product_discount,
            'Rating': product_rating,
            'Total review': product_total_review,
            'Country': country.upper(),
            'ZipCodeSet': f"{row.get('part1', '')} {row.get('part2', '')}" if country in ["can", "uk"] else row.get('part1', '')
        })

    output_df = pd.DataFrame(results)
    output_df.to_excel(f"output_{country}.xlsx", index=False, engine='openpyxl')
    driver.quit()

    logging.info(f"Finished crawling for country: {country}")
    return f"Completed crawling for country: {country}"