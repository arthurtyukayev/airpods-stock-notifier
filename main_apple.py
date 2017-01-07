from requests import get
from pprint import pprint, pformat
from telebot import TeleBot
from datetime import datetime
from time import sleep
from sys import exc_info

token = "321322376:AAErzsopGAH9wwkzCg3dVsBfnbmhVMctOD8"
user_id = 51985891

bot = TeleBot(token=token)

desired_store_address = '1151 Galleria Boulevard'
airpods_part_number = 'MMEF2AM/A'

url = "http://www.apple.com/shop/retail/pickup-message"
params = {'parts.0': airpods_part_number, 'location': '95747'}
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}

while True:
    try:
        r = get(url=url, params=params, headers=headers)
        response_dict = dict(r.json())

        if r.status_code == 200:
            found_store = False
            for store in response_dict['body']['stores']:
                if store['address']['address2'] == desired_store_address:
                    if store['partsAvailability'][airpods_part_number]['pickupDisplay'].lower() == 'available':
                        if store['partsAvailability'][airpods_part_number][
                            'storePickupQuote'].split(" ")[0].lower() == 'tomorrow':
                            # Print message for the log.
                            store_location = "{}, {}, {}".format(store['address']['address2'], store['city'],
                                                                 store['address']['postalCode'])
                            print("There is stock in the Apple Store on {} tomorrow.".format(desired_store_address))
                            # Send telegram message.
                            current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                            formatted = pformat(store['partsAvailability'][airpods_part_number])
                            product = store['partsAvailability'][airpods_part_number]['storePickupProductTitle']
                            message = "<b>{} are in stock at the Apple Store tomorrow at:\n</b> <pre>{}</pre>\n<b>Order them for pickup now.</b>" \
                                      "\nChecked at {}" \
                                      "\n\n<code>{}</code>".format(product, store_location, current_time,
                                                                   formatted.replace("<br/>", " "))
                            bot.send_message(chat_id=user_id, text=message, parse_mode='HTML')
                        elif store['partsAvailability'][airpods_part_number][
                            'storePickupQuote'].split(" ")[0].lower() == 'today':
                            # Print message for the log.
                            store_location = "{}, {}, {}".format(store['address']['address2'], store['city'],
                                                                 store['address']['postalCode'])
                            print("There is stock in the Apple Store on {} right now.".format(desired_store_address))
                            # Send telegram message.
                            current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                            formatted = pformat(store['partsAvailability'][airpods_part_number])
                            product = store['partsAvailability'][airpods_part_number]['storePickupProductTitle']
                            message = "<b>{} are in stock at the Apple Store right now at:\n</b> <pre>{}</pre>\n<b>GO TO THE APPLE STORE NOW!</b>" \
                                      "\n" \
                                      "\nChecked at {}" \
                                      "\n<code>{}</code>".format(product, store_location, current_time,
                                                                 formatted.replace("<br/>", " "))
                            bot.send_message(chat_id=user_id, text=message, parse_mode='HTML')
                    else:
                        print("Ran a check, there is no stock.")
                found_store = True
            if not found_store:
                message = "<b>Apple Store Stock Notifier</b>\nI couldn't match the proper store address, check the script."
                bot.send_message(chat_id=user_id, text=message, parse_mode='HTML')

        else:
            print("Request came back with an error.")
    except:
        print("Unexpected error: {}".format(exc_info()[0]))
    print("Sleeping for 30 seconds.")
    sleep(30)
