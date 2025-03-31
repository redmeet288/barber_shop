from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.all_keyboards import main_keyboard
from states import UserStates
import aiohttp
from data import weather_api_token
from datetime import datetime
import time
from data import get_countries_data
import random


router = Router()
countries_data =  get_countries_data()
print(countries_data)

@router.message(F.text.lower() == "страны", UserStates.user_main_kb)
async def countries(message: Message, state: FSMContext):
    country = random.choice(countries_data)
    country_name = country["name"]["common"]
    capital = country["capital"][0]
    area = country["area"]
    flag = country["flag"]
    population = country["population"]
    await message.answer(
        f"Угадай что за страна: "
        f"Столица: {capital}"
        f"Население(Чел.): {population}"
        f"Площадь км²: {area}"
    )
    await state.set_state(UserStates.user_choice_country)
    await state.update_data(country=country_name)
    await state.update_data(flag=flag)

@router.message(F.text, UserStates.user_choice_country)
async def check_country_answer(message: Message, state: FSMContext):
    user_country = message.text
    print(user_country)
    current_country_data = await state.get_data()
    print(current_country_data)
    current_country = current_country_data["country"]
    result = "Правильно!" if user_country.lower() == current_country.lower() else f"Неправильно({current_country})"
    await message.reply(
        "ПРАВИЛЬНО ИЛИ НЕПРАВИЛЬНО",
        reply_markup=main_keyboard()
    )
    await state.set_state(UserStates.user_main_kb)