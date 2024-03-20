import time

import schedule
from telebot import TeleBot
from telebot.util import quick_markup

from src.config import get_config
from src.kwork_parser import NEW_OFFER_URL, Kworks, get_new_kworks

MESSAGE_TEXT = """
{title}
Желаемый бюджет: {price} Рублей

{description}
"""


def send_kworks(bot: TeleBot, kworks: Kworks):
    for id, kwork in kworks.items():
        bot.send_message(
            get_config().chat_id,
            MESSAGE_TEXT.format(
                title=kwork.title, price=kwork.price, description=kwork.description
            ),
            reply_markup=quick_markup(
                {"Откликнуться": {"url": NEW_OFFER_URL.format(id=id)}}
            ),
        )
        time.sleep(1 / 2)


bot = TeleBot(token=get_config().token)


def main():
    kworks = get_new_kworks(get_config().category)
    send_kworks(bot, kworks)


if __name__ == "__main__":
    main()

    schedule.every(get_config().period).minutes.do(main)
    while True:
        schedule.run_pending()
        time.sleep(10 / 1000)
