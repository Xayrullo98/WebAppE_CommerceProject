import os
from datetime import datetime
import requests
def download_file_func(warehouse_id,file_name):
    login = ''
    password = ''
    login_url = 'https://smartup.merospharm.uz/b/core/s$log_in'

    headers = {
        "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        "host": "smartup.merospharm.uz",
        "origin": "https://smartup.merospharm.uz",
        "referer": "https://smartup.merospharm.uz/login.html"
    }

    session = requests.Session()
    response = session.post(url=login_url, data={'login': login, 'password': password, 'lang_code': 'en'}, headers=headers)

    if response.status_code == 200:

        today = datetime.today().strftime("%d.%m.%Y")
        price_list_url = f"https://smartup.merospharm.uz/b/anor/rep/product_price_list:run?rt=csv&date={today}&margin=&detail=&with_balance=Y&warehouse_id={warehouse_id}&product_group_id=102&-project_code=trade&-project_hash=01&-filial_id=28939&-user_id=28664&-lang_code=en"

        price_response = session.get(price_list_url, headers={"accept": "application/json, text/plain, */*",
                                                              "referer": "https://smartup.merospharm.uz/"})

        if price_response.status_code == 200:
            # Save the response content to a file
            file_path = f"{file_name}.csv"
            with open(file_path, 'wb') as file:
                file.write(price_response.content)
            print("File downloaded successfully.")
        else:
            print("Failed to fetch the price list:", price_response.text)
    else:
        print("Login failed. Please check your credentials.")


