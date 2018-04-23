import subprocess
import os
import pandas as pd

df = pd.read_csv('data/links_cnn.csv')

# ctr = 0
# for link in df.link:
#     ctr += 1
#     try:
#         file_path = "data/screenshot/" + str(ctr)
#         subprocess.check_output(["webkit2png","-o", file_path, "-", link])
#     except:
#         pass
    
from selenium import webdriver
DRIVER = '/usr/local/bin/chromedriver'

from time import time

ctr = 0
for link in df.link:
    ctr += 1
    time0 = time.now()
    driver = webdriver.Chrome(DRIVER)
    driver.get(link)
    file_path = "data/screenshot/" + str(ctr) + '.png'
    screenshot = driver.save_screenshot(file_path)
    driver.close()
    

