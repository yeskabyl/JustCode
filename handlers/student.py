from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states import UserStates
from services.ai_service import get_ai_response, analyze_image

router = Router()

# AI Tutor
@router.message(UserStates.student_menu, F.text == "AI-Репетитор")
async def start_tutor(message: types.Message, state: FSMContext):
    await state.set_state(UserStates.student_tutor)
    await message.answer("Я твой AI-репетитор. Напиши тему или вопрос, который хочешь разобрать.")

@router.message(UserStates.student_tutor)
async def tutor_chat(message: types.Message, state: FSMContext):
    prompt = f"Ты опытный репетитор. Объясни ученику тему: {message.text}. Используй пошаговый подход, примеры и задавай вопросы для проверки понимания."
    response = await get_ai_response([{"role": "user", "content": prompt}])
    await message.answer(response)

# HW Check
@router.message(UserStates.student_menu, F.text == "Проверка ДЗ")
async def start_hw_check(message: types.Message, state: FSMContext):
    await state.set_state(UserStates.student_hw_check)
    await message.answer("Пришли фото или текст своего домашнего задания, и я проверю его на ошибки.")

@router.message(UserStates.student_hw_check, F.photo)
async def hw_check_photo(message: types.Message, state: FSMContext, bot):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{bot.token}/{file.file_path}"
    
    prompt = "Проанализируй это домашнее задание. Найди ошибки, объясни их и предложи правильное решение."
    response = await analyze_image(file_url, prompt)
    await message.answer(response)

# Training (Simplified)
@router.message(UserStates.student_menu, F.text == "Тренажер")
async def start_training(message: types.Message, state: FSMContext):
    await state.set_state(UserStates.student_training)
    await message.answer("На какую тему хочешь потренироваться? Я подготовлю 5 задач.")

@router.message(UserStates.student_training)
async def generate_training(message: types.Message, state: FSMContext):
    prompt = f"Сгенерируй 5 задач по теме '{message.text}' разного уровня сложности для тренировки."
    response = await get_ai_response([{"role": "user", "content": prompt}])
    await message.answer(response)
    await state.set_state(UserStates.student_menu) # Return to menu for simplicity in this version

# Cheat Sheets
@router.message(UserStates.student_menu, F.text == "Шпаргалки")
async def start_cheat_sheet(message: types.Message, state: FSMContext):
    await state.set_state(UserStates.student_cheat_sheet)
    await message.answer("По какой теме тебе нужна умная шпаргалка? Я соберу самое важное.")

@router.message(UserStates.student_cheat_sheet)
async def generate_cheat_sheet(message: types.Message, state: FSMContext):
    prompt = f"Создай компактную умную шпаргалку по теме '{message.text}'. Включи основные определения, формулы и правила."
    response = await get_ai_response([{"role": "user", "content": prompt}])
    await message.answer(response)
    await state.set_state(UserStates.student_menu)

# Other features can be added similarly
