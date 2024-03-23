import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By

# Initialize the WebDriver
driver = webdriver.Chrome()

# Open the webpage
URL_home = "https://chaldal.com"
driver.get(URL_home)

# Define variables
sidebars = []   # contains the names of the sidebars
sidebar_url_list = []   # contains the links to the sidebars


def find_sidebar_links():
    ul = driver.find_elements(By.CSS_SELECTOR, "ul[class*='level-']")
    for a_tags in ul:
        links = a_tags.find_elements(By.TAG_NAME, "a")   # finds the <a> tags
        for link in links:
            url_sidebar = link.get_attribute("href")  # finds the href from the <a> tags
            sidebar_url_list.append(url_sidebar)
            sidebars.append(link.text)   # finds the texts shown associated with the links (options in the menus)
            # print('option: ' + link.text + ' url: ' + url_sidebar)
    return sidebar_url_list, sidebars


def initialize(url):
    driver.get(url)
    scroll_page()
    html_content = driver.page_source
    soup = BeautifulSoup(html_content,"lxml")
    return soup


def find_product_detail(product_link):
    detail_link = URL_home + product_link
    soup = initialize(detail_link)
    description = soup.find("div", class_="details").text
    return description



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


sidebar_url_list, sidebars = find_sidebar_links()

# Save the sidebars and associated links
data = {'menu': sidebars, 'url': sidebar_url_list}
df = pd.DataFrame(data)
df.set_index('url', inplace=True)
df.to_excel("E:\Projects\Chaldal_scrapping_project\Chaldal_scraper\scrapped_data\Chaldaal_dynamic_test.xlsx",
            sheet_name="urls")

items = []
quantities = []
prices = []
product_links = []
descriptions = []
category = []
i = 0

for url in sidebar_url_list:
    soup = initialize(url)
    menubar = df.loc[url, 'menu']
    print(menubar)
    if menubar == "Food":
        break
    try:
        productPane = soup.find("div", class_="productPane")
        products = productPane.findAll("div", class_="product")
        for product in products:
            if i == 3:
                i = 0
            break
            item = product.find("div", class_="name").text
            quantity = product.find("div", class_="subText").text
            if product.find("div", class_="discountedPrice"):
                price = product.find("div", class_="discountedPrice").text
            else:
                price = product.find("div", class_="price").text
            product_link = product.find("a", class_="btnShowDetails").get("href")
            items.append(item)
            quantities.append(quantity)
            prices.append(price)
            product_links.append(product_link)
            description = find_product_detail(product_link)
            descriptions.append(description)
            category.append(menubar)
            i = i + 1
            print(i)
    except Exception:
        print("Exception occurred")

df2 = pd.DataFrame(columns=['item', 'quantity', 'price', 'description', 'category'],
                   data={"item": items, "quantity": quantities, "price": prices,
                   "description": descriptions, "category": category})

with pd.ExcelWriter("E:\Projects\Chaldal_scrapping_project\Chaldal_scraper\scrapped_data\Chaldaal_dynamic_test.xlsx",
                    engine='openpyxl', mode='a') as writer:
    df2.to_excel(writer, sheet_name="raw_data")

print(df2)
driver.close()


#### skip this part for now #####

# food_sublinks = driver.find_elements(By.CSS_SELECTOR,"ul[class*='level-2']>li>div>a")
# print(food_sublinks)
# for sublink in food_sublinks:
#     print(sublink.text.strip())
# url_list.append(sublink.get_attribute("href"))

# # def find_all_links(element):
# #     child_elements = element.find_elements(By.XPATH,'//a')
# #     if child_elements:
# #         print('element has child')
# #         for child_element in child_elements:
# #             sub_links = child_element.find_elements(By.TAG_NAME,"a")
# #             url_list.append([link.get_attribute("href") for link in sub_links])


################################
