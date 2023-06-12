from aiogram.dispatcher.filters.state import StatesGroup, State

class Form(StatesGroup):
    expect_answer = State()