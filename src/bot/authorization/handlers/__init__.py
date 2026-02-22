from aiogram import Router
from . import start, language, auth_login, auth_choice, auth_email, auth_password

router = Router()

router.include_router(start.router)
router.include_router(language.router)
router.include_router(auth_choice.router)
router.include_router(auth_login.router)
router.include_router(auth_email.router)
router.include_router(auth_password.router)
