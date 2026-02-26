from aiogram import Router
from . import (
    auth_register,
    process_first_name,
    base,
    last_name,
    enter_phone,
    enter_email,
    enter_photo,
    process_password_and_show_summary,
    edit_field,
    finish_registration,
    back,
)

router = Router()
router.include_routers(
    base.router,
    back.router,
    auth_register.router,
    process_first_name.router,
    last_name.router,
    enter_phone.router,
    enter_email.router,
    enter_photo.router,
    process_password_and_show_summary.router,
    edit_field.router,
    finish_registration.router,
)
