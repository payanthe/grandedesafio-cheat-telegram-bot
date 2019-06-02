#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple Bot to fetch correct responses from https://grandedesafio.com/.
"""
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import requests
from bs4 import BeautifulSoup

update_id = None
def main():
    global update_id
    bot = telegram.Bot('820244574:AAE6xxpyfSPrTmQUNI2wHaHZve_XjnOO5xE')

    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            reply_to_user(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            update_id += 1


def reply_to_user(bot):
    global update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:

            if update.message.text == "/start":
                update.message.reply_text(
                    "*How To USE* \n *This Bot Is Super EASY * \n Just Send Me Quiz Number : \n https://grandedesafio.com/quiz/1234567 \n Just Send Me *1234567* ",
                    parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                res = get_correct(str(update.message.text))
                update.message.reply_text(res, parse_mode=telegram.ParseMode.MARKDOWN)


def get_correct(id):
    if not id.isdigit():
        return "*This Bot Is Super EASY * \n Just Send Me * Quiz Number*  : \n https://grandedesafio.com/quiz/1234567 \n Just Send Me *1234567* "
    url = "https://grandedesafio.com/quiz/" + id

    headers = {
        'cache-control': "no-cache",
        'postman-token': "1facc381-1b49-09b9-9ece-521dc956b012",
        'User-Agent': 'Mozilla/5'
    }

    response = requests.get(url, headers=headers, allow_redirects=False)

    if response.status_code != 200:
        return "* There is Problem We Fix It Soon *"
    result = []

    c = response.content

    try:
        soup = BeautifulSoup(c, features="html.parser")
        samples = soup.find_all("td", class_="correct")
        name = soup.select("#name_div > h3.fivepxtop.tenpxbottom.center")
        if len(name) > 0:
            name = name[0].get_text()
        result.append(name)
        for i in samples:
            f = i.get_text()
            result.append(str(f).strip())
        text = ""
        text = "*" + result[0] + "*"
        text += "\n"
        for i in range(1, len(result)):
            num = "*" + str(i) + "*"
            text += num
            text += "  "
            text += result[i]
            text += "\n"
        text += "\n *CREATOR* @paydarap"
        return text
    except Exception as e:
        print(e)
        return "*Wrong Quiz Number* \nJust Send Me Quiz Number : \n https://grandedesafio.com/quiz/1234567 \n Just Send Me *1234567* "


if __name__ == '__main__':
    main()
