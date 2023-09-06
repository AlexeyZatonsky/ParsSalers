from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWidgets import QLineEdit, QPushButton, QListWidget, QLabel #natation classes
from PyQt6 import uic, QtGui, QtCore

from Parsers import Parser_interface, Lenta, Metro #classes
from Parsers import lenta, metro, parser #objects
from Parsers import start_to_pars #function

import sqlite3

import sys


class ParsSalers(QMainWindow):
    def __init__(self) -> None:
        super(ParsSalers, self).__init__() # Call the inherited classes __init__ method

        #natation 
        self.search_query_lineEdit: QLineEdit

        self.search_query_button: QPushButton
        self.add_cart_button: QPushButton
        self.lib_to_carts_button: QPushButton
        
        self.lenta_listWidget: QListWidget
        self.metro_listWidget: QListWidget
        self.cart_listWidget: QListWidget

        self.lenta_label: QLabel
        self.metro_label: QLabel
        

        # open qss(css) with app
        f = open(r'UI_files\interface.qss')
        self.StyleData = f.read()
        f.close()

        #load GUI interface, set qss and set window icon
        self.ui = uic.loadUi(r'UI_files\Interface.ui', self)
        self.ui.setStyleSheet(self.StyleData)
        self.setWindowIcon(QtGui.QIcon(r'Additional_files\ico.png'))

        self.show() # Show the GUI


        self.con = sqlite3.connect(r'Database\items.db')
        self.cur = self.con.cursor()

        self.add_to_list_widget()
        self.search_query_lineEdit.returnPressed.connect(self.query_start)
        self.search_query_button.clicked.connect(self.query_start)
        self.lib_to_carts_button.clicked.connect(self.calculate_cart)

    def query_start(self) -> None:

        try: 
            parser.remove_database()
            self.search_query = self.search_query_lineEdit.text()

            start_to_pars(metro, self.search_query)
            #start_to_pars(lenta, self.search_query)
        
        finally:
            self.add_to_list_widget()


    def draw_lenta_lst(self) -> list:
        self.lenta_list = list(self.cur.execute(('''SELECT item_id, item_name, item_price, shop_name
                                                    FROM items
                                                    WHERE shop_name = 'Lenta'
                                                    ORDER BY item_price ASC
                                                    LIMIT 20''')))

        return self.lenta_list


    def draw_metro_lst(self) -> list:
        self.metro_list = list(self.cur.execute(('''SELECT item_id, item_name, item_price, shop_name 
                                                    FROM items
                                                    WHERE shop_name = 'Metro'
                                                    ORDER BY item_price ASC
                                                    LIMIT 20''')))
        
        return self.metro_list


    def add_to_list_widget(self) -> None:
        
        for item in self.draw_lenta_lst():
            self.lenta_listWidget.addItem(self.clear_str(item))

        for item in self.draw_metro_lst():
            self.metro_listWidget.addItem(self.clear_str(item))


    def clear_str(self, item) -> str:
        self.symbols = ["(", "'", ")"]

        item = str(item)
        position = item.rfind(',')
        item = item[:position] + '₽' + item[position+1:]

        for simbol in self.symbols:
            item = item.replace(simbol, '')
        
        return item

    
    def calculate_cart(self): 
        metro_cart = 0
        lenta_cart = 0
        full_cart =  0
        
        if len(self.withdrawal_id_cart_list()) > 0:
            self.cart_calc = self.draw_sqlcart_lst(self.withdrawal_id_cart_list())
        else : pass

        for price, shop_name in self.cart_calc:
            
            if shop_name == 'Metro': metro_cart += price
            elif shop_name == 'Lenta': lenta_cart += price
            
        full_cart = lenta_cart + metro_cart
        
        self.lenta_label.setText('Лента: ' + str(round(lenta_cart, 2)))
        self.metro_label.setText('Метро: ' + str(round(metro_cart, 2)))
        

    def withdrawal_id_cart_list(self) -> list:
        self.cart_list_items = list()
        self.item_id_lst = list()

        alphabet = ['1','2','3','4','5','6','7','8','9']
        sqlNum = ''

        for i in range(self.cart_listWidget.count()):
            item = self.cart_listWidget.item(i).text()
            
            for simbol in item:
                if simbol  not in alphabet: break
                else: sqlNum += simbol

            self.item_id_lst.append(int(sqlNum))
            sqlNum = ''

        return self.item_id_lst

    
    def draw_sqlcart_lst(self, cart_list_items:list) -> list:
        self.cart_price_shop_lst = list()

        base_request ='''SELECT item_price, shop_name FROM items
                        WHERE item_id == '''
        
        for item_id in cart_list_items:
            recuest = base_request + str(item_id)

            item = self.cur.execute(recuest).fetchone()
            self.cart_price_shop_lst.append(item)
    
        return self.cart_price_shop_lst

    '''
    def sum_of_grams(self, cart_list_items) -> str:
        self.cart_name_lst = list()
        grams = ''

        self.grams_of_lenta = 0
        self.grams_of_metro = 0

        alphabet = ['1','2','3','4','5','6','7','8','9']
        base_request =  'SELECT item_name, shop_name FROM items WHERE item_id == '

        for item_id in  cart_list_items:
            recuest = base_request + str(item_id)

            item_name_recuest = self.cur.execute(recuest).fetchone()
            self.cart_name_lst.append(item_name_recuest)
        
        for item_name, shop_name in self.cart_name_lst:
            item_name:str
            index_grams = int(item_name.rfind('г'))

            

            for ind in grams:
                if ind not in alphabet: break
                else: pass
    '''


        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    window = ParsSalers()

    sys.exit(app.exec())
