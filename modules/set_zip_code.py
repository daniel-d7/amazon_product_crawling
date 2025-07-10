import os
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def set_zip_code(driver, zip_code_p1, zip_code_p2, max_attempts):
    for attempt in range(max_attempts):
        try:
            zip_code_link = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "nav-global-location-slot"))
            )
            zip_code_link.click()
            time.sleep(1)
            zip_code_legend_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "GLUXZipUpdateInput_0"))
            )
            zip_code_legend_input.clear()
            zip_code_legend_input.send_keys(zip_code_p1)
            zip_code_legend_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "GLUXZipUpdateInput_1"))
            )
            zip_code_legend_input.clear()
            zip_code_legend_input.send_keys(zip_code_p2)
            zip_code_legend_input.send_keys(Keys.ENTER)
            time.sleep(3)
            return True
        except Exception:
            time.sleep(1)
    return False