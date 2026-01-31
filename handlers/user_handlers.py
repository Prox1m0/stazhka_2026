from aiogram import Router, types, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from services.menu_service import get_main_menu
from services.settings_service import get_greeting, get_buttons
from services.request_sender import send_request
from states import OrderForm

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(get_greeting(), reply_markup=get_main_menu())


@router.message(F.text == "Узнать цены")
async def show_prices(message: types.Message):
    try:
        await message.answer_document(
            document=types.FSInputFile("data/prices.pdf"),
            caption="📄 Вот наш прайс!"
        )
    except FileNotFoundError:
        await message.answer("Цены от 5000 руб. Подробнее на сайте: https://test_url/price")


@router.message(F.text == "Заказать")
async def start_order(message: types.Message, state: FSMContext):
    await state.set_state(OrderForm.name)
    await message.answer("Отлично! Как вас зовут?")


@router.message(OrderForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(OrderForm.task)
    await message.answer("Что нужно сделать?")


@router.message(OrderForm.task)
async def process_task(message: types.Message, state: FSMContext):
    await state.update_data(task=message.text)
    await state.set_state(OrderForm.contact)
    await message.answer("Оставьте контакт (телефон или email)")


@router.message(OrderForm.contact)
async def process_contact(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    name = data["name"]
    task = data["task"]
    contact = message.text
    
    await send_request(bot, name, task, contact, message.date)
    await message.answer("✅ Спасибо! Заявка передана, свяжемся в течение 2 часов.")
    await state.clear()

@router.message(F.text)
async def handle_user_text(message: types.Message, state: FSMContext):
    from config import ADMIN_ID
    buttons = get_buttons()
    user_text = message.text

    for btn in buttons:
        if btn["text"] == user_text:
            if btn["action"] == "text":
                if "content" in btn:
                    await message.answer(btn["content"])
                return
            
            elif btn["action"] == "faq":
                if "content" in btn:
                    await message.answer(
                        f"📘 <b>Часто задаваемые вопросы</b>\n\n{btn['content']}",
                        parse_mode="HTML"
                    )
                else:
                    await message.answer("Пока нет данных для FAQ.")
                return

            elif btn["action"] == "contact":
                if "content" in btn:
                    await message.answer(
                        f"📞 <b>Контакты</b>\n\n{btn['content']}",
                        parse_mode="HTML"
                    )
                else:
                    await message.answer("Пока нет контактной информации.")
                return

            elif btn["action"] == "price":
                try:
                    await message.answer_document(
                        document=types.FSInputFile("data/prices.pdf"),
                        caption="📄 Вот наш прайс!"
                    )
                except FileNotFoundError:
                    await message.answer("Цены от 5000 руб. Подробнее на сайте: https://test_url/price")
                return

            elif btn["action"] == "order":
                await state.set_state(OrderForm.name)
                await message.answer("Отлично! Как вас зовут?")
                return

            elif btn["action"] == "url":
                if "url" in btn:
                    await message.answer(
                        f'<a href="{btn["url"]}">🌐 Перейти: {btn["text"]}</a>',
                        parse_mode="HTML"
                    )
                return

            elif btn["action"] == "file":
                await message.answer("📎 Файл пока не поддерживается.")
                return

    if message.from_user.id == ADMIN_ID:
        await message.answer("Вы админ. Для настройки бота используйте /panel")
        return

    await message.answer("🤖 Я не понимаю эту команду. Воспользуйтесь кнопками ниже.", reply_markup=get_main_menu())


