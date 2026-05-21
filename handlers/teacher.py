from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states import UserStates
from services.ai_service import get_ai_response, analyze_image
import pandas as pd
import io

router = Router()

# Schedule
@router.message(UserStates.teacher_menu, F.text == "Расписание")
async def start_schedule(message: types.Message, state: FSMContext):
    await state.set_state(UserStates.teacher_schedule)
    await message.answer("Пришли темы уроков и доступные временные слоты. Я составлю план и могу добавить его в Google Calendar.")

@router.message(UserStates.teacher_schedule)
async def process_schedule(message: types.Message, state: FSMContext):
    prompt = f"Составь учебное расписание на основе этих данных: {message.text}. Учти темы, контрольные и время на повторение."
    response = await get_ai_response([{"role": "user", "content": prompt}])
    await message.answer(f"Вот твое расписание:\n\n{response}")
    await message.answer("События были бы синхронизированы с Google Calendar в полной версии.")
    await state.set_state(UserStates.teacher_menu)

# Homework Check (Teacher version - bulk)
@router.message(UserStates.teacher_menu, F.text == "Проверка работ")
async def start_teacher_hw_check(message: types.Message, state: FSMContext):
    await state.set_state(UserStates.teacher_hw_check)
    await message.answer("Загрузи фото работы ученика или архив с работами для быстрой проверки.")

@router.message(UserStates.teacher_hw_check, F.photo)
async def teacher_hw_check_photo(message: types.Message, state: FSMContext, bot):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{bot.token}/{file.file_path}"
    
    prompt = "Ты ассистент преподавателя. Проверь эту работу, поставь оценку (1-10) и напиши краткий комментарий для ученика."
    response = await analyze_image(file_url, prompt)
    await message.answer(response)

# Material Generation
@router.message(UserStates.teacher_menu, F.text == "Генерация материалов")
async def start_material_gen(message: types.Message, state: FSMContext):
    await state.set_state(UserStates.teacher_material_gen)
    await message.answer("Для какого урока (предмет, класс, тема) подготовить материалы?")

@router.message(UserStates.teacher_material_gen)
async def process_material_gen(message: types.Message, state: FSMContext):
    prompt = f"Создай структуру урока, практические задания и тест по теме: {message.text}."
    response = await get_ai_response([{"role": "user", "content": prompt}])
    await message.answer(response)
    await state.set_state(UserStates.teacher_menu)

# Analytics (Excel generation stub)
@router.message(UserStates.teacher_menu, F.text == "Анализ успеваемости")
async def start_analytics(message: types.Message, state: FSMContext):
    await message.answer("Формирую сводную таблицу успеваемости на основе последних проверок...")
    
    # Mock data
    data = {
        'Ученик': ['Иван Иванов', 'Мария Петрова', 'Алексей Сидоров'],
        'Оценка': [8, 10, 7],
        'Рекомендация': ['Повторить логарифмы', 'Отлично!', 'Больше практики с тригонометрией']
    }
    df = pd.DataFrame(data)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Успеваемость')
    output.seek(0)
    
    file = types.BufferedInputFile(output.read(), filename="analytics.xlsx")
    await message.answer_document(file, caption="Сводная таблица успеваемости.")

# Design presentations
@router.message(UserStates.teacher_menu, F.text == "Дизайн презентаций")
async def start_presentation(message: types.Message, state: FSMContext):
    await state.set_state(UserStates.teacher_presentation)
    await message.answer("Напиши тему презентации, и я предложу структуру и дизайн-концепцию.")

@router.message(UserStates.teacher_presentation)
async def process_presentation(message: types.Message, state: FSMContext):
    prompt = f"Предложи детальную структуру презентации (8-10 слайдов) и рекомендации по дизайну для темы: {message.text}."
    response = await get_ai_response([{"role": "user", "content": prompt}])
    await message.answer(response)
    await state.set_state(UserStates.teacher_menu)
