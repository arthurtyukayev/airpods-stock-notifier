from telebot import TeleBot
from requests import get, post
from pprint import pprint, pformat
from datetime import datetime
from time import sleep

token = "321322376:AAErzsopGAH9wwkzCg3dVsBfnbmhVMctOD8"
user_id = 51985891

bot = TeleBot(token=token)

# Product Info and Config
product_sku = '5577872'  # Change this to find a different product.
search_location_zip = 95747  # Change this to search a different area.

product_info_url = 'http://www.bestbuy.com/api/1.0/product/summaries'
product_availability_url = 'http://www.bestbuy.com/productfulfillment/c/api/1.0/fulfillments'

while True:
    search_json = {"skus": [
        {"quantity": 1, "skuId": "{}".format(product_sku)}],
        "zipCode": "{}".format(search_location_zip),
        "customerUuid": None
    }
    # Getting product info and availability
    #
    # Product Info
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
    }
    params = {'skus': product_sku, 'includeInactive': 'false'}
    info_response = get(product_info_url, params=params, headers=headers)
    if info_response.status_code != 200:
        print("Info Request came back with an error.")
        continue
    product_info = info_response.json()[0]
    # Product Availability
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
    }
    availability_response = post(product_availability_url, json=search_json, headers=headers)
    if availability_response.status_code != 200:
        print("Availability Request came back with an error.")
        continue

    product_availability = availability_response.json()

    availability_stores = product_availability['storePickup']['storeAvailabilities'][0:5]

    if len(availability_stores) > 0:
        for store in availability_stores:
            # Building the notification message
            product_name = product_info['meta']['title']
            current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            store_type = store['store']['locationSubType']
            store_location = "{}, {}, {} {}".format(store['store']['address']['street'],
                                                    store['store']['address']['city'],
                                                    store['store']['address']['state'],
                                                    store['store']['address']['zipcode'])
            store['store']['hours'] = []
            formatted = pformat(store)
            print('There is stock at the BestBuy store on {}.'.format(store_location))
            message = "<b>{} are in stock at the BestBuy {} right now at:\n</b> <pre>{}</pre>" \
                      "\n" \
                      "\nChecked at {}" \
                      "\n<code>{}</code>".format(product_name, store_type, store_location, current_time,
                                                 formatted.replace("<br/>", " "))
            bot.send_message(chat_id=user_id, text=message, parse_mode='HTML')
    else:
        print("Checked BestBuy, there is no stock.")

    print("Sleeping for 30 seconds.")
    sleep(30)
