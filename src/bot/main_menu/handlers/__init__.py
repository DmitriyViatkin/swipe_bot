from aiogram import Router
from . import profile, profile_menu

router = Router()

router.include_router(profile.router)
router.include_router(profile_menu.router)
