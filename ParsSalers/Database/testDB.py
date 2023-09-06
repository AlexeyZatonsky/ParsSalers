import  sqlite3


lst = ("12", "21","22", "23")
ulst = list()

con = sqlite3.connect('Database\items.db')
cur = con.cursor()


for i in lst:
    zapros = '''SELECT item_price, shop_name FROM items
                    WHERE item_id == ''' + i
    
    ulst.append(cur.execute(zapros).fetchone())

print(ulst)
