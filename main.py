import asyncio
import time
from aiogram import Bot
import schedule
from src.config import CATEGORY, CHAT_ID, PERIOD, TOKEN
from src.kwork_parser import NEW_OFFER_URL, Kworks, get_new_kworks
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


MESSAGE_TEXT = """
{title}
Желаемый бюджет: {price} Рублей

{description}
"""


async def send_kowrks(bot: Bot, kworks: Kworks):
    for id, kwork in kworks.items():
        await bot.send_message(CHAT_ID, MESSAGE_TEXT.format(
            title=kwork.title,
            price=kwork.price,
            description=kwork.description
        ), reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="Откликнуться",
                url=NEW_OFFER_URL.format(id=id)
            )]
        ]))
        await asyncio.sleep(1/3)


bot = Bot(token=TOKEN)


def main():
    kworks = get_new_kworks(CATEGORY)
    asyncio.run(send_kowrks(bot, kworks))


if __name__ == "__main__":
    main()

    schedule.every(PERIOD).minutes.do(main)
    while True:
        schedule.run_pending()
        time.sleep(10/1000)
