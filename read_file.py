
import pandas as pd
from functions.products import products, update_product_for_db, delete_product, check_product, add_product


def read_file_func(file_name,branch_id):

    df_excel = pd.read_csv(f'{file_name}.csv', skiprows=4, encoding='cp1251', delimiter=';', on_bad_lines='skip')
    codes_list = df_excel['Code'].tolist()

    for code in set(codes_list):
         if not check_product((str(code),), branch_id=branch_id) and str(code) !='nan' :
            matching_rows = df_excel[df_excel['Code'] == f'{code}']
            df_code = matching_rows['Code'].values[0]
            df_name = matching_rows['Name'].values[0]
            df_price100 = (matching_rows['Price Type: При 100% Оплате (перечисление)'].values[0])
            df_price25 = (matching_rows['Price Type: Цена договорная (перечисление)'].values[0])
            df_id_number = matching_rows['Barcode'].values[0]
            df_number = matching_rows['Balance'].values[0]
            df_deadline = matching_rows['Expiry Date'].values[0]
            df_company_name = matching_rows['Producer'].values[0]
            add_product(code=df_code,id_number=df_id_number, name=df_name, number=df_number, is_ordered='',price25=df_price25,price100=df_price100,percentage='',deadline=df_deadline,company_name=df_company_name,branch_id=branch_id)

    products_table = products(branch_id=branch_id)

    for product in products_table:
        code = product.code
        name = product.name
        price100 = product.price100
        price25 = product.price25
        id = product.id
        if code in df_excel['Code'].values:
            matching_rows = df_excel[df_excel['Code'] == f'{code}']

            df_code = matching_rows['Code'].values[0]
            df_name = matching_rows['Name'].values[0]
            df_price100 = float(matching_rows['Price Type: При 100% Оплате (перечисление)'].values[0])
            df_price25 = float(matching_rows['Price Type: Цена договорная (перечисление)'].values[0])
            df_id_number = matching_rows['Barcode'].values[0]
            df_number = matching_rows['Balance'].values[0]
            df_is_ordered = ''
            df_deadline = matching_rows['Expiry Date'].values[0]
            df_company_name = matching_rows['Producer'].values[0]

            if (code != df_code or
                    name != df_name or
                    price25 != df_price25 or
                    price100 != df_price100):

                 update_product_for_db(
                    id=id,
                    code=df_code,
                    id_number=df_id_number,
                    name=df_name,
                    number=df_number,
                    is_ordered=df_is_ordered,
                    price25=df_price25,
                    price100=df_price100,
                    percentage=0,
                    deadline=df_deadline,
                    company_name=df_company_name
                )
        else:
            delete_product(code=code)

