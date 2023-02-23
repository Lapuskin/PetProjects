from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import datetime
import asyncio

from config import TOKEN


time = datetime.datetime.now()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message, bot: Bot):
    await message.reply("Привет!\nЭто JobBot - машина, которая поможет найти тебе вакансию по-вкусу)"
                        "Бот осуществляет поиск вакансий на таких площадках, как: Rabota.by, hh.ru и другие.")
    await asyncio.sleep(1)
    await bot.send_message("Давай немного сузим круг поиска.\nУкажи страну.")

@dp.message_handler(commands=['help'])
async def process_helper_command(message: types.Message):
    await message.reply("Интересно, что умеет бот?)\n Пока ничего, только здороваться)")

@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def send_to_admin(message: types.Message):
    await message.reply("Мммммм, надеюсь, это нюдсы...")

if __name__ == '__main__':
    executor.start_polling(dp)
