from telebot import TeleBot
from requests import get, post
from pprint import pprint, pformat
from datetime import datetime
from time import sleep

token = "321322376:AAErzsopGAH9wwkzCg3dVsBfnbmhVMctOD8"
user_id = 51985891

bot = TeleBot(token=token)

product_sku = 52106337  # Change this to find a different product.
search_location_zip = 95747  # Change this to search a different area.

product_availabity_url = "https://api.target.com/available_to_promise/v2/{}/search".format(product_sku)
product_info_url = "http://redsky.target.com/v1/pdp/tcin/{}".format(product_sku)

while True:
    # Building the request.
    params = {
        "key": "eb2551e4accc14f38cc42d32fbc2b2ea",
        "nearby": search_location_zip,
        "inventory_type": "stores",
        "multichannel_option": "none",
        "field_groups": "location_summary",
        "requested_quantity": 1,
        "radius": 15
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
    }
    r = get(product_availabity_url, params=params, headers=headers)
    p = get(product_info_url, headers)

    # Getting info about the product
    product_info = p.json()['product']['item']

    if r.status_code != 200:
        print("Request came back with an error. Status Code: {}".format(r.status_code))
        continue

    availability_stores = r.json()['products'][0]['locations']
    for store in availability_stores:
        if store['availability_status'] == 'IN_STOCK':
            product_name = product_info['product_description']['title'].replace('&#174;', "")
            product_name = product_info['product_description']['title'].replace('&#153;', "")
            current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            store_location = store['formatted_store_address']
            formatted = pformat(store)
            print('There is stock at the {} Target on {}.'.format(store['store_name'], store_location))
            message = "<b>{} in stock at the {} Target on:\n</b> <pre>{}</pre>" \
                      "\n" \
                      "\nChecked at {}" \
                      "\n<code>{}</code>".format(product_name, store['store_name'], store_location, current_time,
                                                 formatted.replace("<br/>", " "))
            bot.send_message(chat_id=user_id, text=message, parse_mode='HTML')

    # Sleep
    print("Sleeping for 30 seconds.")
    sleep(30)
