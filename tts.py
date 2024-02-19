import requests
from seleniumwire import webdriver
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NaverWebTTS:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument('--log-level=3')
        options.add_argument("--mute-audio")
        driver = webdriver.Chrome(options=options)
        driver.get('https://papago.naver.com/')
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="btn-toolbar-source"]/span[1]/span/span/button')))
        self.driver, self.wait = driver, wait
        
    def save(self, text, path):
        if len(text)>1000:
            raise ValueError("Max length is 1000")
        
        context = self.driver.find_element(By.XPATH, '//*[@id="txtSource"]')
        context.clear()
        context.send_keys(text)
        
        self.wait.until(lambda d: d.find_element(By.XPATH, '//*[@id="btn-toolbar-source"]/span[1]/span/span/button').get_attribute("class") == 'btn_sound___2H-0Z')
        self.driver.find_element(By.XPATH, '//*[@id="btn-toolbar-source"]/span[1]/span/span/button').click()
        
        end_time = time.time() + 10
        url = None
        while url == None:
            for request in self.driver.requests:
                if "https://papago.naver.com/apis/tts/" in request.url and "audio" in request.response.headers.get('Content-Type', ''):
                    url = request.url
                    break
            if time.time() > end_time:
                raise TimeoutException("Requests Fail")
        res = requests.get(url=url)
        with open(path, "wb") as f:
            for chunk in res.iter_content(chunk_size=1024):
                f.write(chunk)
