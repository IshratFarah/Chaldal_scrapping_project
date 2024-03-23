"""
1. extract from all link in one extractor file.
    1.1 try to extract all the link from web browser dynamically since
    the link will update later.
2. Make it in class and function wise implementation.
3. Try to go through the google stlye sheet doc.
4. xlsx,csv, and parquet file save

"""


class ChaldaExtractor:

    def __init__(self ):
        pass



    def save_to_supabase_bucket(self):
        pass

    def extract_chaldal_data(self):
        pass


chal_dal = ChaldaExtractor()
chal_dal.save_to_supabase_bucket()









import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

# Initialize the WebDriver
driver = webdriver.Chrome()

# Open the webpage
url = "https://chaldal.com/flash-sales"
driver.get(url)

# Scroll down the page multiple times to load more content
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


# Extract the HTML content of the scrolled page
html_content = driver.page_source

soup = BeautifulSoup(html_content,"lxml")
# print(soup)

productPane = soup.find("div",class_="productPane")
# print(result.text)

products = productPane.findAll("div",class_="product")
# for product in products:
#     print(product.text)
# print(len(products))

items = []
quantities = []
prices = []

for product in products:
    try:
        item = product.find("div",class_="name").text
        quantity = product.find("div",class_="subText").text
        price = product.find("div",class_="price").text
        items.append(item)
        quantities.append(quantity)
        prices.append(price)
    except:
        print("Exception occurred")

driver.close()

df = pd.DataFrame(columns=['item','quantity','price'],data={"item":items,"quantity":quantities,"price":prices})
print(df)
# df.to_csv("F:\Scrapping\Ramadan_items.csv",index=False)
# df.to_excel("F:\Scrapping\Chaldaal.xlsx",sheet_name="Flash_Sales")

with pd.ExcelWriter("F:\Scrapping\Chaldaal.xlsx", mode='a') as writer:
    df.to_excel(writer, sheet_name='Flash_Sales1')