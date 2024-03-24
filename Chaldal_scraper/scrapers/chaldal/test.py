import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By



# Initialize webdriver
driver = webdriver.Chrome()
url_home = "https://chaldal.com"
driver.get(url_home)

# Define global variables
items = []
quantities = []
prices = []
product_links = []
descriptions = []
category = []
category_url_list = []  # contains the links to the categories in sidebars
categories = []  # contains the titles of the categories in sidebars
subcategory_url_list = []   # contains the links to the subcategories
subcategory = []    # contains the titiles to the subcategories

def find_links(link_container):
    container = link_container
    url_list = []
    url_title = []
    # print("find_links function entered")
    # print(container)
    for a_tags in container:
        links = a_tags.find_elements(By.TAG_NAME, "a")
        print(links)# finds the <a> tags
        for link in links:
            url_list.append(link.get_attribute("href"))    # finds the href from the <a> tags
            url_title.append(link.text)   # finds the texts shown associated with the links (options in the menus)
            print(url_title)
    return url_list, url_title


def initialize(url):
    driver.get(url)
    scroll_page()
    html_content = driver.page_source
    soup = BeautifulSoup(html_content,"lxml")
    return soup


def find_product_detail(product_link):
    detail_link = url_home + product_link
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


def scrap_product_info(products, menubar):
    i = 0
    for product in products:
        if i == 2:
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


def main():
    link_container = driver.find_elements(By.CSS_SELECTOR, "ul[class*='level-']")
    category_url_list, categories = find_links(link_container)
    df_submenu = pd.DataFrame()

    # Save the sidebars and associated links
    data = {'menu': categories, 'url': category_url_list}
    df = pd.DataFrame(data)
    df.set_index('url', inplace=True)
    df.to_excel("E:\Projects\Chaldal_scrapping_project\Chaldal_scraper\scrapped_data\Chaldaal_dynamic_test.xlsx",
                sheet_name="urls")

    for url in category_url_list:
        soup = initialize(url)
        menubar = df.loc[url, 'menu']
        try:
            print(menubar)
            productPane = soup.find("div", class_="productPane")
            prod_elements = productPane.findAll("div", class_="product")
            scrap_product_info(prod_elements, menubar)
        except AttributeError:
            links = []
            titles = []
            sublink_container = driver.find_elements(By.CLASS_NAME, "category-links-wrapper")
            links, titles = find_links(sublink_container)
            data_s = {'menu': titles, 'url': links}
            df_s = pd.DataFrame(data_s)
            df_s.set_index('url', inplace=True)
            print(df_s)
            df_submenu = pd.concat([df_submenu, df_s], ignore_index=True)

    # with pd.ExcelWriter(
    #         "E:\Projects\Chaldal_scrapping_project\Chaldal_scraper\scrapped_data\Chaldaal_dynamic_test.xlsx",
    #         engine='openpyxl', mode='a') as writer:
    #     df_s.to_excel(writer, sheet_name="submenu_urls")
    print(df_submenu)

    # df2 = pd.DataFrame(columns=['item', 'quantity', 'price', 'description', 'category'],
    #                    data={"item": items, "quantity": quantities, "price": prices,
    #                    "description": descriptions, "category": category})
    #
    # with pd.ExcelWriter("E:\Projects\Chaldal_scrapping_project\Chaldal_scraper\scrapped_data\Chaldaal_dynamic_test.xlsx",
    #                     engine='openpyxl', mode='a') as writer:
    #     df2.to_excel(writer, sheet_name="raw_data")
    #
    # print(df2)
    driver.close()


main()
