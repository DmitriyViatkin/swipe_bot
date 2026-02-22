from aiogram import Router, types
from aiogram.filters import Command
from src.bot.authorization.keyboards.choise_language import get_language_keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    text = (
        "🇺🇦 Будь ласка, оберіть мову:\n"
        "🇷🇺 Пожалуйста, выберите язык:\n"
        "🇺🇸 Please, choose a language:"
    )
    await message.answer(text, reply_markup=get_language_keyboard())
