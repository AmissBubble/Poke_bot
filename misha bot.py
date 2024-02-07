import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.contrib.middlewares.logging import LoggingMiddleware

# Set up logging
logging.basicConfig(level=logging.INFO)

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = Bot(token='5629818025:AAE3CAZFs6uhMcWZodFUdpKhSJu5awmGK_o')
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

# States
class GameState(StatesGroup):
    SEARCHING = State()
    FOUND_POKEMON = State()
    TRY_CATCH = State()
    CAUGHT = State()

# Keyboard markup
keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Go'))

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Press the 'Go' button to start the adventure.", reply_markup=keyboard)
    await GameState.SEARCHING.set()



@dp.message_handler(state=GameState.SEARCHING, text='Go')
async def search_pokemon(message: types.Message, state: FSMContext):
    if random.choice([True, False]):  # Simulate finding a Pokemon
        await message.answer("You found a Pokemon! What do you want to do?", reply_markup=ReplyKeyboardMarkup(
            resize_keyboard=True).add(KeyboardButton('Drop and Go'), KeyboardButton('Try to Catch')))
        await GameState.FOUND_POKEMON.set()
    else:
        await message.answer("No Pokemon found. Press 'Go' to try again.")
        await GameState.SEARCHING.set()

@dp.message_handler(state=GameState.FOUND_POKEMON, text='Drop and Go')
async def drop_and_go(message: types.Message, state: FSMContext):
    await message.answer("You dropped the Pokemon and went on. Press 'Go' to try again.")
    await GameState.SEARCHING.set()

@dp.message_handler(state=GameState.FOUND_POKEMON, text='Try to Catch')
async def try_catch(message: types.Message, state: FSMContext):
    if random.choice([True, False]):  # Simulate catching the Pokemon
        await message.answer("Congratulations! You caught the Pokemon. Press 'Go' to try again.")
        await GameState.SEARCHING.set()
    else:
        await message.answer("Oops! The Pokemon escaped. Press 'Try Again' to attempt catching again.",
                             reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Try Again')))
        await GameState.TRY_CATCH.set()

@dp.message_handler(state=GameState.TRY_CATCH, text='Try Again')
async def try_again(message: types.Message, state: FSMContext):
    await message.answer("You tried again. Press 'Go' to start a new adventure.")
    await GameState.SEARCHING.set()

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)