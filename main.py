from requests import get
from pprint import pprint, pformat
from telebot import TeleBot
from datetime import datetime
from time import sleep
from sys import exc_info

token = "167272397:AAEmTnqpauTnZ5DcnXeXM2oDodcTsqHyKBU"
user_id = 51985891

bot = TeleBot(token=token)

url = "http://www.istocknow.com/live/live.php"
params = {'device.0': 'airpods', 'stores': 'retail', 'nostock': 'on'}
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}

while True:
    try:
        r = get(url=url, params=params, headers=headers)
        response_dict = dict(r.json())
        if r.status_code == 200:
            if '40' in response_dict['dataz']:
                # Send telegram message
                current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                product = 'AirPods'
                message = "<b>{} are in stock at the Apple Store right now at:\n</b> <pre>{}</pre>\n<b>GO TO THE APPLE STORE NOW!</b>" \
                          "\n" \
                          "\nChecked at {}" \
                          "\n<code>{}</code>".format(product, 'Apple Store Roseville', current_time,
                                                     pformat(response_dict['dataz']['40']))
                bot.send_message(chat_id=user_id, text=message, parse_mode='HTML')
            else:
                print("Checked but nothing was found.")
        else:
            print("Request came back with an error.")
    except:
        print("Unexpected error: {}".format(exc_info()[0]))
    print("Sleeping for 60 seconds.")
    sleep(120)
