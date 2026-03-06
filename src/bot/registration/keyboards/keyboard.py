from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from src.bot.authorization.states import AuthStates
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from src.bot.authorization.keyboards.control_keyboards import get_control_keyboard

router = Router()


# Кнопка "Назад"
@router.message(F.text == __("btn_back"))
async def go_back_auth(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == AuthStates.waiting_for_password:
        await state.set_state(AuthStates.waiting_for_email)
        await message.answer(_("enter_email"), reply_markup=get_control_keyboard())

    elif current_state == AuthStates.waiting_for_email:
        await state.clear()

        await message.answer(
            _("auth_choice_text"), reply_markup=types.ReplyKeyboardRemove()
        )


def get_language_keyboard():

    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text=str(__("btn_lang_uk"))))
    builder.add(KeyboardButton(text=str(__("btn_lang_en"))))
    builder.add(KeyboardButton(text=str(__("btn_lang_ru"))))

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_auth_choice_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text=str(__("btn_login"))))
    builder.add(KeyboardButton(text=str(__("btn_register"))))
    builder.add(KeyboardButton(text=str(__("btn_back_to_lang"))))

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_photo_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text=str(_("btn_skip")))
    builder.button(text=str(__("btn_back")))
    builder.button(text=str(_("btn_cancel")))
    builder.adjust(1, 2)
    return builder.as_markup(resize_keyboard=True)
