import requests
import xlwt

from bs4 import BeautifulSoup as BS
book = xlwt.Workbook(encoding="utf-8") #initial new excel book
sheet1 = book.add_sheet("Sheet 1",cell_overwrite_ok=True) #initial sheet for write

f = open('E:\\scratches\\newart.txt',encoding='UTF8') #shop articles txt file
column_num = 1
for line in f:
    print('opened')
    span_list = []
    code = line.replace("\n", "")
    r = requests.get('https://tdme.ru/product/' + code)
    if r.status_code == 200:
        html = BS(r.content, 'html.parser')
        for el in html.select('h2.font-black.font-bold.text-2xl'):
            name = el.text
        print(name)
        for el in html.select('ul.my-4 li span'):
            span_list.append(el.text)
        price = span_list[1].replace(" ₽", "")
        print(price)
        span_list=[]
        for el in html.select('li.breadcrumb-item a'):
            span_list.append(el.text)
        category=span_list[2]
        sheet1.write(column_num, 0, code)
        sheet1.write(column_num, 1, name)
        sheet1.write(column_num, 2, price)
        sheet1.write(column_num, 3, category)
        sheet1.write(column_num, 4, f"https://tdme.ru/download/WebImage/TDM-{code}.jpg")
        column_num += 1
        book.save("items-tdme.xls")
    elif r.status_code == 404:
        print('Not Found.')