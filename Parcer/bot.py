from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.utils import executor
import time
import logging
from config import TOKEN, CHANNEL_ID, ALINA_ID, ADMIN_ID, DOMAIN
from expectant import Form
from parcer import Parcer
from stylist import Stylist


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
parcer = Parcer()
stylist = Stylist()

logging.basicConfig(
    level=logging.WARNING,
    filename = "logs/mylog.log",
    format = "%(asctime)s - %(levelname)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
    )
logging.info('bot is running, objects are created')


async def on_startup(_):
    while True:
        try:
            news = parcer.get_awesome_news()
            #await bot.send_message(ADMIN_ID, DOMAIN + parcer.get_last_link() + '\n\nverify this link. May I drop it?', parce_mode='HTML')
            logging.info('news was scrapping.', news)
            news_text = stylist.style(news)
            logging.info('news was stylish.')
            await bot.send_message(CHANNEL_ID, news_text, parse_mode='HTML')
            logging.info('message was sent. Wait 14400 sec')
            await bot.send_message(ADMIN_ID, 'Сообщение отправлено без ошибок.')
            time.sleep(14400)
        except TypeError:
            logging.exception('Message wasn\'t sent. Wait 3600 sec')
            await bot.send_message(ADMIN_ID, "Сообщение не отправлено. Возникла ошибка TypeError в модуле bot.py")
            time.sleep(3600)


'''
@dp.message_handler(state=Form.answer) # Принимаем состояние
async def start(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy: # Устанавливаем состояние ожидания
        Form.answer['expect_answer'] = message.text

        await state.finish() # Выключаем состояние
'''

@dp.message_handler(commands=['help'])
async def process_helper_command(message: types.Message):
    await message.reply("Интересно, что умеет бот?)\n Пока ничего, только здороваться)")

@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def send_to_admin(message: types.Message):
    await message.reply("Мммммм, надеюсь, это нюдсы...")

@dp.message_handler(commands=['get_logs'])
async def get_logs(message: types.Message):
    await message.reply("What log file?")

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
