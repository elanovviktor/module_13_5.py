from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



api = "7822078456:AAHvaw2ghYvc0MBErCXjhUqSHb_kc6o2fO0"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = KeyboardButton(text='Расчитать')#кнопка1
button_2 = KeyboardButton(text='Информация')#кнопка2
kb.row(button_1, button_2)# кнопки в ряд
# kb.add(button_1)
# kb.add(button_2)#можно добавить кнопки построчно

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start_(message):
    await message.answer(text='Привет, я бот помогающий твоему здоровью', reply_markup=kb)

@dp.message_handler(text = ["Информация"])
async def inform(message):
    await message.answer("Это информация о боте")

@dp.message_handler(text = ['Расчитать'])
async def set_age(message):
    await message.answer("Введите свой возраст:")
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    data = await state.get_data()
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def set_weight(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result = (10 * int(data['weight'])) + (6.25 * float(data['growth'])) - (5 * int(data['age'])) - 176
    await message.answer(f'Ваша норма каллорий {result}')
    await state.finish()

dp.message_handler()
async def start_any(message):
    await message.answer('Введите команду /start что бы начать общение')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

