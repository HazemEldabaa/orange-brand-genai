from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import cv2
import numpy as np
import urllib
import ssl
from bs4 import BeautifulSoup
import pandas as pd
import requests

def get_json(div_id, url):

    URL = url
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    # Locate the div by ID and extract table data
    div = soup.find('div', {'id': div_id})
    if not div:
        print(f"No div with id {div_id} found.")
        return None

    # Assuming the table is inside this div
    table = div.find('table')
    if not table:
        print(f"No table found inside div with id {div_id}.")
        return None
        
    # Prepare to collect data
    data = []

    # Iterate through rows of the main table
    for row in table.find_all('tr'):
        # Each row has a main cell with an image and another table with metadata
        cells = row.find_all('td')
        if len(cells) < 2:
            continue  # Skip rows that don't have at least two cells (image and metadata)

        image_info = cells[0].text.strip()
        metadata_table = cells[1].find('table')
        
        if metadata_table:
            metadata = {}
            for meta_row in metadata_table.find_all('tr'):
                label_cell, value_cell = meta_row.find_all('td')
                label = label_cell.text.strip()
                value = value_cell.text.strip()
                metadata[label] = value

            # Add image info as part of metadata
            metadata['Image Info'] = image_info
            
            # Append to the data list
            data.append(metadata)
    
    # Convert the collected data into a DataFrame
    if data:
        df = pd.DataFrame(data)
        return df
    else:
        print("No data extracted.")
        return None

def send_prompt(link, prompt_text, json_link, headless = True):
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--incognito")
    if headless:
        options.add_argument("--headless")

    options.add_argument("--window-size=1920,1080")  # Set a reasonable window size
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    try:
        driver = webdriver.Chrome(options=options)
        driver.get(link)
        driver.implicitly_wait(30)
        
        # Locate and interact with elements
        advanced = driver.find_element(By.XPATH, '//*[@id="component-21"]/label/input')
        
        # Click on the advanced checkbox
        advanced.click()
        
        # Wait for a brief moment
        time.sleep(2)
        preset_dropdown = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="component-99"]/label/div/div[1]/div/input'))
        )
        preset_dropdown.click()  # Click to open the dropdown
        preset_dropdown.clear()
        preset_dropdown.send_keys("realistic")
        preset_dropdown.send_keys(Keys.ENTER)
        
        time.sleep(2)

        # Wait for the performance checkbox to be clickable
        performance = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="component-100"]/div[2]/label[1]/input'))
        )
        
        # Click the performance checkbox if not already selected
        if not performance.is_selected():
            performance.click()
        
        # Clear and set quantity to 1
        quantity = driver.find_element(By.XPATH, '//*[@id="component-104"]/div[2]/div/input')
        quantity.clear()
        quantity.send_keys("1")

        model = driver.find_element(By.XPATH, '//*[@id="component-216"]/div[1]/button[3]')
        model.click()

        refiner_dropdown = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="component-121"]/label/div/div[1]/div/input'))
        )
        refiner_dropdown.click()  # Click to open the dropdown
        refiner_dropdown.clear()
        refiner_dropdown.send_keys("realistic") #realisticVisionV60B1
        refiner_dropdown.send_keys(Keys.ENTER)

        model_dropdown = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="component-120"]/label/div/div[1]/div/input'))
        )
        model_dropdown.click()  # Click to open the dropdown
        model_dropdown.clear()
        model_dropdown.send_keys("mobius") #mobius
        model_dropdown.send_keys(Keys.ENTER)
        
        lora2_drop_down = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="component-133"]/label/div/div[1]/div/input'))
        )
        lora2_drop_down.click()  # Click to open the dropdown
        lora2_drop_down.clear()
        lora2_drop_down.send_keys("perfect_eyes") #add-detail-xl
        lora2_drop_down.send_keys(Keys.ENTER)

        # Find the prompt textarea and send the prompt text
        prompt_textarea = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="positive_prompt"]/label/textarea'))
        )
        prompt_textarea.clear()  # Clear any existing text
        prompt_textarea.send_keys(prompt_text)  # Send the provided prompt text
        prompt_textarea.send_keys(Keys.ENTER)  # Press Enter to confirm the prompt text

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
        img = cv2.imdecode(arr, -1)  # 'Load it as it is'
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        time.sleep(3)

        settings = driver.find_element(By.XPATH, '//*[@id="component-216"]/div[1]/button[1]')
        settings.click()

        logs = driver.find_element(By.XPATH, '//*[@id="component-109"]/a')
        logs.click()

        df = get_json(image_id, json_link)

        time.sleep(3)

        # Save the image
        return {"image": img, "data": df}

    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage