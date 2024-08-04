from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as Firefox_Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time as t
import pandas as pd
from tqdm import tqdm

firefox_options = Firefox_Options()

# firefox_options.add_argument("--width=1500")
# firefox_options.add_argument("--height=500")
# firefox_options.headless = True

driverpath = "C:\\GIT_PROJECTS\\GITHUB_TEST\\driver\\geckodriver.exe"
path='D:/nse_download/ftse_sp_download/'
#driverService = Service('chromedriver/geckodriver')
#driverService = Service('C:\\AmarTool')
driverService = Service(executable_path=driverpath)

browser = webdriver.Firefox(service=driverService, options=firefox_options)

big_df = pd.DataFrame()

browser.get('https://www.londonstockexchange.com/indices/ftse-250/constituents/table')     
try:
    WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.ID, "ccc-notify-accept"))).click()
    print('accepted cookies')
except Exception as e:
    print('no cookie button!')
t.sleep(2)

for i in tqdm(range(1, 14)):
    browser.get(f'https://www.londonstockexchange.com/indices/ftse-250/constituents/table?page={i}') 
    t.sleep(1)
    df = pd.read_html(WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "table[class='full-width ftse-index-table-table']"))).get_attribute('outerHTML'))[0]
    #print(df)
    big_df = pd.concat([big_df, df], axis=0, ignore_index=True)

#print(big_df)

#updated to capture the index and index rename
big_df.to_csv(path+"LSE_250_companies.csv", index=False, encoding='utf-8-sig')

print('all done')
browser.quit()

