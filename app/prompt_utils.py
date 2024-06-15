from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import numpy as np
import urllib
import ssl
from bs4 import BeautifulSoup
import pandas as pd
import requests
import io

def get_json(div_id, url):
    URL = url
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    div = soup.find('div', {'id': div_id})
    if not div:
        print(f"No div with id {div_id} found.")
        return None

    table = div.find('table')
    if not table:
        print(f"No table found inside div with id {div_id}.")
        return None

    data = []

    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) < 2:
            continue

        image_info = cells[0].text.strip()
        metadata_table = cells[1].find('table')

        if metadata_table:
            metadata = {}
            for meta_row in metadata_table.find_all('tr'):
                label_cell, value_cell = meta_row.find_all('td')
                label = label_cell.text.strip()
                value = value_cell.text.strip()
                metadata[label] = value

            metadata['Image Info'] = image_info
            data.append(metadata)

    return pd.DataFrame(data)

def send_prompt(url, prompt_text, json_link, headless=False):
    driver = None
    try:
        options = Options()

        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)

        driver.get(url)

        lora1_drop_down = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="component-133"]/label/div/div[1]/div/input'))
        )
        lora1_drop_down.click()
        lora1_drop_down.clear()
        lora1_drop_down.send_keys("perfect_eyes")
        lora1_drop_down.send_keys(Keys.ENTER)

        prompt_textarea = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="positive_prompt"]/label/textarea'))
        )
        prompt_textarea.clear()
        prompt_textarea.send_keys(prompt_text)
        prompt_textarea.send_keys(Keys.ENTER)

        btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="generate_button"]'))
        )
        btn.click()

        generated_image = WebDriverWait(driver, 160).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="final_gallery"]/div[2]/div/button/img'))
        )

        ssl_context = ssl._create_unverified_context()
        image_src = generated_image.get_attribute("src")
        print(image_src)
        image_id = image_src.split("/")[-1].split(".")[0] + "_png"

        req = urllib.request.urlopen(image_src, context=ssl_context)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = io.BytesIO(arr)

        time.sleep(3)

        settings = driver.find_element(By.XPATH, '//*[@id="component-216"]/div[1]/button[1]')
        settings.click()

        logs = driver.find_element(By.XPATH, '//*[@id="component-109"]/a')
        logs.click()

        df = get_json(image_id, json_link)

        time.sleep(3)
        return {"image": img, "data": df}

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        if driver:
            driver.quit()

