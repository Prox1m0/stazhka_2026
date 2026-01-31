from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from config import ADMIN_ID

from services.settings_service import get_greeting, set_greeting, get_buttons, save_settings, add_button, remove_button
from services.menu_service import get_main_menu
from states import AdminForm

router = Router()

@router.message(Command("panel"))
async def admin_panel(message: types.Message, state: FSMContext):
    await state.clear()
    if message.from_user.id != ADMIN_ID:
        return
    kb = [
        [types.KeyboardButton(text="🔧 Изменить приветствие")],
        [types.KeyboardButton(text="🔘 Управление кнопками")],
        [types.KeyboardButton(text="📊 Статистика")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("⚙️ Панель управления", reply_markup=keyboard)


@router.message(F.text == "⚙️ Админ-панель")
async def admin_panel_by_button(message: types.Message, state: FSMContext):
    await state.clear()
    if message.from_user.id != ADMIN_ID:
        return
    kb = [
        [types.KeyboardButton(text="🔧 Изменить приветствие")],
        [types.KeyboardButton(text="🔘 Управление кнопками")],
        [types.KeyboardButton(text="📊 Статистика")],
        [types.KeyboardButton(text="🛠 Тест бота")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("⚙️ Панель управления", reply_markup=keyboard)


@router.message(F.text == "🔧 Изменить приветствие")
async def prompt_new_greeting(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer(f"Текущий текст:\n\n{get_greeting()}\n\nВведите новый текст:")
    await state.set_state(AdminForm.editing_greeting)


@router.message(AdminForm.editing_greeting)
async def process_greeting_input(message: types.Message, state: FSMContext):
    set_greeting(message.text)
    save_settings()
    await message.answer("✅ Приветствие обновлено!", reply_markup=get_main_menu())
    await state.clear()


@router.message(F.text == "🔘 Управление кнопками")
async def manage_buttons(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    await state.clear()

    kb = [
        [types.KeyboardButton(text="➕ Добавить кнопку")],
        [types.KeyboardButton(text="🗑 Удалить кнопку")],
        [types.KeyboardButton(text="↩️ Назад в панель")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    buttons_list = "\n".join([f"{i+1}. {btn['text']}" for i, btn in enumerate(get_buttons())])
    await message.answer(f"📋 Текущие кнопки:\n\n{buttons_list}\n\nВыберите действие:", reply_markup=keyboard)


@router.message(F.text == "↩️ Назад в панель")
async def back_to_panel(message: types.Message, state: FSMContext):
    await state.clear()
    kb = [
        [types.KeyboardButton(text="🔧 Изменить приветствие")],
        [types.KeyboardButton(text="🔘 Управление кнопками")],
        [types.KeyboardButton(text="📊 Статистика")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("⚙️ Панель управления", reply_markup=keyboard)


@router.message(F.text == "➕ Добавить кнопку")
async def add_button_prompt(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer("Введите текст новой кнопки:")
    await state.set_state(AdminForm.adding_button_text)


@router.message(AdminForm.adding_button_text)
async def process_button_text(message: types.Message, state: FSMContext):
    await state.update_data(button_text=message.text)
    kb = [
        [types.KeyboardButton(text="📝 Текст")],
        [types.KeyboardButton(text="🔗 Ссылка")],
        [types.KeyboardButton(text="❌ Отмена")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Выберите тип действия:", reply_markup=keyboard)
    await state.set_state(AdminForm.adding_button_action)


@router.message(AdminForm.adding_button_action)
async def process_button_action(message: types.Message, state: FSMContext):
    action = message.text
    data = await state.get_data()

    if action == "📝 Текст":
        await message.answer("Введите текст, который будет отправлен при нажатии:")
        await state.set_state(AdminForm.adding_button_content)

    elif action == "🔗 Ссылка":
        await message.answer("Введите ссылку:")
        await state.set_state(AdminForm.adding_button_url)

    elif action == "❌ Отмена":
        await message.answer("Добавление отменено.", reply_markup=get_main_menu())
        await state.clear()
    else:
        await message.answer("Выберите действие из меню.")


@router.message(AdminForm.adding_button_content)
async def process_button_content(message: types.Message, state: FSMContext):
    data = await state.get_data()
    new_button = {
        "text": data["button_text"],
        "action": "text",
        "content": message.text
    }
    add_button(new_button)
    await message.answer(f"✅ Кнопка «{data['button_text']}» добавлена!", reply_markup=get_main_menu())
    await state.clear()


@router.message(AdminForm.adding_button_url)
async def process_button_url(message: types.Message, state: FSMContext):
    data = await state.get_data()
    new_button = {
        "text": data["button_text"],
        "action": "url",
        "url": message.text
    }
    add_button(new_button)
    await message.answer(f"✅ Кнопка «{data['button_text']}» добавлена как ссылка!", reply_markup=get_main_menu())
    await state.clear()


@router.message(F.text == "🗑 Удалить кнопку")
async def delete_button_prompt(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    buttons = get_buttons()
    if not buttons:
        await message.answer("📭 Нет кнопок для удаления.", reply_markup=get_main_menu())
        await state.clear()
        return

    buttons_list = "\n".join([f"{i+1}. {btn['text']}" for i, btn in enumerate(buttons)])
    await message.answer(f"📋 Введите номер кнопки для удаления:\n\n{buttons_list}")
    await state.set_state(AdminForm.deleting_button)


@router.message(AdminForm.deleting_button)
async def process_delete_button(message: types.Message, state: FSMContext):
    try:
        index = int(message.text) - 1
        buttons = get_buttons()
        if 0 <= index < len(buttons):
            removed = buttons[index]["text"]
            remove_button(index)
            await message.answer(f"✅ Кнопка «{removed}» удалена!", reply_markup=get_main_menu())
        else:
            await message.answer("❌ Неверный номер. Попробуйте снова.")
    except ValueError:
        await message.answer("❌ Введите число.")
    await state.clear()


@router.message(F.text == "📊 Статистика")
async def show_stats(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    await state.clear()
    buttons_count = len(get_buttons())
    await message.answer(f"📊 Статистика:\nКнопок в меню: {buttons_count}")


@router.message(F.text == "⬅️ Назад")
async def go_back(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы вернулись в главное меню.", reply_markup=get_main_menu())
