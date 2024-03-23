import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By

# Initialize the WebDriver
driver = webdriver.Chrome()

# Open the webpage
URL = "https://chaldal.com"
driver.get(URL)

sidebars = []
url_list = []

def scroll_page():
    # Scroll down the page multiple times to load more content
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


ul = driver.find_elements(By.CSS_SELECTOR,"ul[class*='level-']")
for a_tags in ul:
    links = a_tags.find_elements(By.TAG_NAME,"a")   # finds the <a> tags
    for link in links:
        url = link.get_attribute("href")  # finds the href from the <a> tags
        url_list.append(url)
        sidebars.append(link.text)   # finds the texts shown associated with the links (options in the menus)

data = {'menu' : sidebars, 'url' : url_list}
df = pd.DataFrame(data)
df.set_index('url', inplace=True)
df.to_excel("F:\Scrapping\Chaldaal_dynamic.xlsx",sheet_name="urls")

for url in url_list:
    driver.get(url)
    scroll_page()
    html_content = driver.page_source
    soup = BeautifulSoup(html_content,"lxml")

    try:
        productPane = soup.find("div",class_="productPane")
        products = productPane.findAll("div",class_="product")
        items = []
        quantities = []
        prices = []
        for product in products:
            item = product.find("div",class_="name").text
            quantity = product.find("div",class_="subText").text
            price = product.find("div",class_="price").text
            items.append(item)
            quantities.append(quantity)
            prices.append(price)
    except:
        print("Exception occurred")

    df2 = pd.DataFrame(columns=['item','quantity','price'],data={"item":items,"quantity":quantities,"price":prices})
    menu = df.loc[url, 'menu']
    print(f"URL: {url}, Menu: {menu}")
    sheetname = df.loc[url, 'menu']
    with pd.ExcelWriter("F:\Scrapping\Chaldaal_dynamic.xlsx", mode='a') as writer:
        df2.to_excel(writer, sheet_name=sheetname)

driver.close()