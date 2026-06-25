from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

bot = Bot(token="Вставьте сюда ваш токен")
dp = Dispatcher()

# FSM
class Form(StatesGroup):
    choice = State()
    details = State()

# Кнопки
menu_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Услуга 1"), KeyboardButton(text="Услуга 2")]
], resize_keyboard=True)

@dp.message(F.text == "/start")
async def start(msg: Message, state: FSMContext):
    await msg.answer("Привет! Что вас интересует?", reply_markup=menu_kb)
    await state.set_state(Form.choice)

@dp.message(Form.choice)
async def get_choice(msg: Message, state: FSMContext):
    await state.update_data(user_choice=msg.text)
    await msg.answer("Напишите кратко ваши пожелания или детали:", reply_markup=None)
    await state.set_state(Form.details)

@dp.message(Form.details)
async def get_details(msg: Message, state: FSMContext):
    data = await state.get_data()
    await msg.answer(f"Готово! Ваша заявка:\n\nВыбрано: {data['user_choice']}\nДетали: {msg.text}\n\nСкоро свяжусь.")
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
