import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import filters
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from typing import List
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage


API_TOKEN = 'ропа'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands=['date'])
async def return_date(message: types.Message):
    await message.reply(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))


@dp.message_handler(filters.Text(contains=['weather'], ignore_case=True))
async def command_weather(message: types.Message):
    await message.reply("Weather is good, dont worry!")


class FSMEvent(StatesGroup):
    username = State()
    password = State()


@dp.message_handler(filters.Text(contains=['register'], ignore_case=True))
async def update_start(message: types.Message):
    await FSMEvent.username.set()
    await message.reply('Please write your username (only alphabet)')


@dp.message_handler(state=FSMEvent.username)
async def choose_username(message: types.Message, state: FSMContext):
    if message.text.isalpha():
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMEvent.next()
        await message.reply('Choose correct password, please write only digit')
    else:
        await message.reply('Please write correct username')


@dp.message_handler(state=FSMEvent.password)
async def choose_password(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.finish()
        await message.reply('Готово!')
    else:
        await message.reply('Please write correct password')




@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


