from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import UserStates

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    kb = [
        [types.KeyboardButton(text="Я Студент"), types.KeyboardButton(text="Я Преподаватель")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Добро пожаловать в JustCode AI Agent! Выберите свою роль:", reply_markup=keyboard)
    await state.set_state(UserStates.choosing_role)

@router.message(UserStates.choosing_role, F.text == "Я Студент")
async def student_chosen(message: types.Message, state: FSMContext):
    await state.set_state(UserStates.student_menu)
    kb = [
        [types.KeyboardButton(text="AI-Репетитор"), types.KeyboardButton(text="Проверка ДЗ")],
        [types.KeyboardButton(text="Тренажер"), types.KeyboardButton(text="Подготовка к экзаменам")],
        [types.KeyboardButton(text="Учебный план"), types.KeyboardButton(text="Шпаргалки")],
        [types.KeyboardButton(text="Сменить роль")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Вы выбрали роль Студента. Чем я могу помочь?", reply_markup=keyboard)

@router.message(UserStates.choosing_role, F.text == "Я Преподаватель")
async def teacher_chosen(message: types.Message, state: FSMContext):
    await state.set_state(UserStates.teacher_menu)
    kb = [
        [types.KeyboardButton(text="Расписание"), types.KeyboardButton(text="Проверка работ")],
        [types.KeyboardButton(text="Генерация материалов"), types.KeyboardButton(text="Анализ успеваемости")],
        [types.KeyboardButton(text="Плагиат"), types.KeyboardButton(text="Дизайн презентаций")],
        [types.KeyboardButton(text="Сменить роль")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Вы выбрали роль Преподавателя. Какие задачи решим сегодня?", reply_markup=keyboard)

@router.message(F.text == "Сменить роль")
async def change_role(message: types.Message, state: FSMContext):
    await cmd_start(message, state)
