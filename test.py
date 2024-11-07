import pandas as pd
from numpy import number
from functions.products import add_product

df = pd.read_csv('downloaded_file.csv', skiprows=4, delimiter=';', encoding='cp1251', on_bad_lines='skip')

for index, row in df.iterrows():
    product = row.to_dict()
    if not str(product.get("Code"))=="nan"  and  not str(product.get("Price Type: При 100% Оплате (перечисление)"))=="nan"  :

        try:
            add_product(
                code=product['Code'],
                id_number=product['Barcode'],
                name=product['Name'],
                number=product['Balance'],
                is_ordered='',
                price100=product['Price Type: При 100% Оплате (перечисление)'],
                price25=product['Price Type: Цена договорная (перечисление)'],
                percentage= f"0",
                deadline=product['Expiry Date'],
                company_name=product['Producer'],
                branch_id=1
            )
        except Exception as x:
            print(x)
        print(product['Price Type: При 100% Оплате (перечисление)'],'d')
        print(product['Price Type: Цена договорная (перечисление)'],'g')