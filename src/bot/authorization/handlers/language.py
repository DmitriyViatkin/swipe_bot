from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, FSMI18nMiddleware, lazy_gettext as __

from src.bot.authorization.keyboards.auth_choise_keyboard import (
    get_auth_choice_keyboard,
)
from src.bot.authorization.keyboards.choise_language import get_language_keyboard

router = Router()


@router.message(F.text.in_([__("btn_lang_uk"), __("btn_lang_en"), __("btn_lang_ru")]))
async def process_language(
    message: types.Message, state: FSMContext, i18n_middleware: FSMI18nMiddleware
):
    lang_map = {
        str(_("btn_lang_uk")): "uk",
        str(_("btn_lang_en")): "en",
        str(_("btn_lang_ru")): "ru",
    }
    lang_code = lang_map.get(message.text, "en")
    await i18n_middleware.set_locale(state, lang_code)

    await message.answer(
        text=_("language_set_success"), reply_markup=get_auth_choice_keyboard()
    )


# --- 2. Повернення до мов через Inline кнопку ---
@router.callback_query(F.data == "back_to_lang")
async def inline_back_to_lang(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    text = (
        " Будь ласка, оберіть мову:\n"
        "Пожалуйста, выберите язык:\n"
        "Please, choose a language:"
    )
    await callback.message.edit_text(text=text, reply_markup=get_language_keyboard())
    await callback.answer()
