from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    choosing_role = State()
    
    # Student states
    student_menu = State()
    student_tutor = State()
    student_hw_check = State()
    student_training = State()
    student_exam_prep = State()
    student_study_plan = State()
    student_cheat_sheet = State()
    
    # Teacher states
    teacher_menu = State()
    teacher_schedule = State()
    teacher_hw_check = State()
    teacher_material_gen = State()
    teacher_analytics = State()
    teacher_plagiarism = State()
    teacher_presentation = State()
