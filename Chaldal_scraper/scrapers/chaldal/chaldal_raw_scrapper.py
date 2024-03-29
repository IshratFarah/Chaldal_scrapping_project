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
submenu_list = []   # list of dataframes. Each df contain subcategories and associated links
all_item = []   # contains the list of all item information
path = "E:\\Projects\\Chaldal_scrapping_project\\Chaldal_scraper\\scrapped_data\\"
file_name = "Chaldaal_rawdata_v1.1.xlsx"
full_filepath = path + file_name


def find_links(link_container):
    container = link_container
    url_list = []
    url_title = []
    for a_tags in container:
        links = a_tags.find_elements(By.TAG_NAME, "a")
        for link in links:
            url_list.append(link.get_attribute("href"))    # finds the href from the <a> tags
            url_title.append(link.text)   # finds the link titles
    data = {'menu': url_title, 'url': url_list}
    df = pd.DataFrame(data)
    return df


def initialize(url):
    driver.get(url)
    scroll_page()
    html_content = driver.page_source
    soup = BeautifulSoup(html_content,"lxml")
    return soup


def find_product_description(product_link):
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


def get_product_info(soup,menubar):
    items = []
    quantities = []
    prices = []
    product_links = []
    descriptions = []
    category = []
    try:
        productPane = soup.find("div", class_="productPane")
        products = productPane.findAll("div", class_="product")  # prod_elements == products
        for product in products:
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
            description = find_product_description(product_link)
            descriptions.append(description)
            category.append(menubar)
        df_item_by_cat = pd.DataFrame(columns=['item', 'quantity', 'price', 'description', 'category'],
                                      data={"item": items, "quantity": quantities, "price": prices,
                                            "description": descriptions, "category": category})
        all_item.append(df_item_by_cat)
    except AttributeError:
        sub_link_container = driver.find_elements(By.CLASS_NAME, "category-links-wrapper")
        df_sub = get_categories(sub_link_container)
        submenu_list.append(df_sub)


def get_categories(container):
    df = find_links(container)
    for index, row in df.iterrows():
        soup = initialize(row['url'])
        get_product_info(soup, row['menu'])
    return df


def main():
    menu_link_container = driver.find_elements(By.CSS_SELECTOR, "ul[class*='level-']")
    df_menu = get_categories(menu_link_container)
    df_menu.to_excel(full_filepath, sheet_name="menu_urls", index=False)

    # Save the subcategories and the associated links
    df_submenu_links = pd.concat(submenu_list, ignore_index=True)
    with pd.ExcelWriter(full_filepath, engine='openpyxl', mode='a') as writer:
        df_submenu_links.to_excel(writer, sheet_name="submenu_urls", index=False)

    # Save information of all items in a single dataframe
    df_all_item = pd.concat(all_item, ignore_index= True)
    with pd.ExcelWriter(full_filepath, engine='openpyxl', mode='a') as writer:
        df_all_item.to_excel(writer, sheet_name="item_info", index=False)

    driver.close()


main()
