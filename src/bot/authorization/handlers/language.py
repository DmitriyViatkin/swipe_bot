from aiogram import Router, F, types


from src.bot.authorization.handlers.auth_choice import get_auth_choice_keyboard
from aiogram.utils.i18n import gettext as _, FSMI18nMiddleware
from aiogram.fsm.context import FSMContext

router = Router()


@router.callback_query(F.data.startswith("lang_"))
async def process_language(
    callback: types.CallbackQuery, state: FSMContext, i18n_middleware: FSMI18nMiddleware
):
    lang_code = callback.data.split("_")[1]

    await i18n_middleware.set_locale(state, lang_code)

    await callback.message.edit_text(
        text=_("language_set_success"), reply_markup=get_auth_choice_keyboard()
    )
    await callback.answer()
