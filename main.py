import time

import schedule
from telebot import TeleBot  # type: ignore
from telebot.util import quick_markup  # type: ignore

from src.config import MESSAGE_TEXT, NEW_OFFER_URL, SEND_KWORK_TIMEOUT, get_config
from src.kwork_parser import Kworks, get_new_kworks


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
        time.sleep(SEND_KWORK_TIMEOUT)


bot = TeleBot(token=get_config().token)


def main():
    kworks = get_new_kworks(get_config().category)
    send_kworks(bot, kworks)


if __name__ == "__main__":
    main()

    schedule.every(get_config().period).minutes.do(main)  # type: ignore
    while True:
        schedule.run_pending()
        time.sleep(10 / 1000)
