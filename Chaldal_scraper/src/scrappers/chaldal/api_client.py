import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By

url_home = "https://chaldal.com"
submenu_list = []   # list of dataframes. Each df contain subcategories and associated links
all_item = []   # contains the list of all item information
path = "E:\\Projects\\Chaldal_scrapping_project\\Chaldal_scraper\\scrapped_data\\"
file_name = "Chaldaal_rawdata_v1.3.xlsx"
full_filepath = path + file_name
print(full_filepath)


class PageHandler:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get(url_home)

    def scroll_page(self):
        # Scroll down the page multiple times to load more content
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def loader(self, url):
        self.driver.get(url)
        self.scroll_page()
        html_content = self.driver.page_source
        soup = BeautifulSoup(html_content, "lxml")
        return soup


def get_url(link_container):
    container = link_container
    url_list = []
    url_title = []
    for a_tags in container:
        links = a_tags.find_elements(By.TAG_NAME, "a")
        for link in links:
            url_list.append(link.get_attribute("href"))  # finds the href from the <a> tags
            url_title.append(link.text)  # finds the link titles
    data = {'menu': url_title, 'url': url_list}
    df = pd.DataFrame(data)
    return df


class UrlManager:
    def __init__(self):
        pass

    def get_url(self, link_container):
        container = link_container
        url_list = []
        url_title = []
        for a_tags in container:
            links = a_tags.find_elements(By.TAG_NAME, "a")
            for link in links:
                url_list.append(link.get_attribute("href"))  # finds the href from the <a> tags
                url_title.append(link.text)  # finds the link titles
        data = {'menu': url_title, 'url': url_list}
        df = pd.DataFrame(data)
        return df


class DataRetriever:
    def __init__(self, handler: PageHandler, get_url: UrlManager):
        self._handler = handler
        self._get_url = get_url

    def find_product_description(self, product_link):
        detail_link = url_home + product_link
        soup = self._handler.loader(detail_link)
        description = soup.find("div", class_="details").text
        return description

    def get_product_info(self, soup, menubar):
        items = []
        quantities = []
        prices = []
        product_links = []
        descriptions = []
        category = []
        i = 0
        try:
            productPane = soup.find("div", class_="productPane")
            products = productPane.findAll("div", class_="product")  # prod_elements == products
            for product in products:
                if i == 2:
                    i=0
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
                description = self.find_product_description(product_link)
                descriptions.append(description)
                category.append(menubar)
                i = i + 1
            df_item_by_cat = pd.DataFrame(columns=['item', 'quantity', 'price', 'description', 'category'],
                                          data={"item": items, "quantity": quantities, "price": prices,
                                                "description": descriptions, "category": category})
            all_item.append(df_item_by_cat)
        except AttributeError:
            sub_link_container = self._handler.driver.find_elements(By.CLASS_NAME, "category-links-wrapper")
            df_sub = self._get_url.get_url(sub_link_container)
            submenu_list.append(df_sub)

    def get_data(self, df):
        for index, row in df.iterrows():
            soup = self._handler.loader(row['url'])
            self.get_product_info(soup, row['menu'])


class Main:

    def __init__(self, handler: PageHandler, get_url: UrlManager, get_data: DataRetriever):
        self._handler = handler
        self._get_url = get_url
        self._get_data = get_data

    def executor(self):
        menu_link_container = self._handler.driver.find_elements(By.CSS_SELECTOR, "ul[class*='level-']")
        df_menu = self._get_url.get_url(menu_link_container)
        print(df_menu.shape)
        df_menu.to_excel(full_filepath, sheet_name="menu_urls", index=False)
        self._get_data.get_data(df_menu)

        # Save the subcategories and the associated links
        df_submenu_links = pd.concat(submenu_list, ignore_index=True)
        print(df_submenu_links.shape)
        with pd.ExcelWriter(full_filepath, engine='openpyxl', mode='a') as writer:
            df_submenu_links.to_excel(writer, sheet_name="submenu_urls", index=False)
        self._get_data.get_data(df_submenu_links)

        # Save information of all items in a single dataframe
        df_all_item = pd.concat(all_item, ignore_index=True)
        print(df_all_item.shape)
        with pd.ExcelWriter(full_filepath, engine='openpyxl', mode='a') as writer:
            df_all_item.to_excel(writer, sheet_name="item_info", index=False)

        self._handler.driver.close()


class ChaldalAPIClient:
    def __init__(self):
        pass

    def get_data_from_web_site(self):
        handler = PageHandler()
        get_url = UrlManager()
        get_data = DataRetriever(handler=handler, get_url=get_url)
        main = Main(handler=handler, get_url=get_url, get_data=get_data)
        main.executor()




