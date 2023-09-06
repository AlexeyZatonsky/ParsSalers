#Web Scarping
from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

from selenium.webdriver.common.by import By

#Data manipulation
import sqlite3




class Parser_interface():
    
    'Parser_intrface'

    def __init__(self):
        self.con = sqlite3.connect(r'Database\items.db')
        self.cur = self.con.cursor()

    def search_on_item(self, search_item:str) -> str:
        self.search_query = search_item
        self.search_item = search_item.replace(' ', '%20')
        self.url = ''
        self.url = (self.__doc__) + self.search_item

        self.browser.get(self.url)


    def start_browser(self): 
        self.browser = webdriver.Chrome(executable_path = r'Additional_files\chromedriver.exe', options = self.web_options())


    def web_options(self) -> object:
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('disable-infobars')
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument('start-maximized') 
        self.options.add_argument("--disable-blink-features")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        return self.options


    def pars(self): pass


    def create_list(self) -> list: pass


    def add_sqlite(self) -> None:
        self.data_product: list

        self.shop_name = str(self.__class__.__name__)

        for title, price in self.data_product:

            title = str(title)
            price = float(price)

            self.cur.execute('''INSERT INTO items(item_name, item_price, shop_name, search_query)
                                VALUES(?, ?, ?, ?);''',
                                (title, price, self.shop_name, self.search_query))

        self.con.commit()


    def remove_database(self) -> None:
        self.cur.execute('DELETE FROM items')
        self.con.commit()





class Lenta(Parser_interface): 

    'https://lenta.com/search/?searchText=' 
    
    def pars(self):
        try:
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'sku-card-small-header__title')))
            
        finally:
            self.item_titles = self.browser.find_elements(By.CLASS_NAME, 'sku-card-small-header__title')
            self.item_prices_int = self.browser.find_elements(By.CLASS_NAME, 'price-label__integer')
            self.item_prices_fraction = self.browser.find_elements(By.CLASS_NAME, 'price-label__fraction')
        

    def create_list(self) -> list:
        self.titles_list = []
        self.prices_list = []

        for title in self.item_titles:
            self.titles_list.append(title.text.lower())

        for priceint, pricefl in zip(self.item_prices_int, self.item_prices_fraction): 
            price = priceint.text +'.'+ pricefl.text 
            price = price.replace(' ', '')
            self.prices_list.append(price)

        self.browser.quit()

        self.data_product = list(zip(self.titles_list, self.prices_list))
        return self.data_product




class Metro(Parser_interface): 

    'https://online.metro-cc.ru/search?q='

    def pars(self):
        try:
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.base-product-name.reset-link')))
        
        finally:
            self.item_titles = self.browser.find_elements(By.CSS_SELECTOR, 'a.base-product-name.reset-link')
            self.item_prices = self.browser.find_elements(By.CSS_SELECTOR ,'span.base-product-prices__actual-sum')


    def create_list(self) -> list:
        self.titles_list = []
        self.prices_list = []

        for title in self.item_titles:
            if title.text != '':
                self.titles_list.append(title.text.lower())

        for price in self.item_prices:
            price = price.text
            price = price.replace(' ', '')

            if price != '':
                self.prices_list.append(price)

        self.browser.quit()

        self.data_product = list(zip(self.titles_list, self.prices_list))
        return self.data_product




def start_to_pars(shop: Lenta | Metro, search_item:str):
    shop.start_browser()
    shop.search_on_item(search_item)
    shop.pars()
    shop.create_list()
    print(shop.data_product)
    shop.add_sqlite()

parser = Parser_interface()
lenta = Lenta()
metro = Metro()


if __name__ == '__main__':
    start_to_pars(lenta, 'Шоколад бабаевский')
    start_to_pars(metro, 'Шоколад бабаевский')
    