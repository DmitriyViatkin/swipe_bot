# src/bot/adverts/handlers/__init__.py
from aiogram import Router
from . import (
    start_handler,
    start_create_adverts,
    location_handler,
    appointment,
    layout_handler,
    state_handler,
    heating_handler,
    payment_handler,
    communications_handlers,
    rooms_handler,
    area_handler,
    kitchen_area_handler,
    balcony_handler,
    commission_handler,
    description_handler,
    price_handler,
    add_image_handler,
    skip_photo,
    finish_image,
    back_a,
    cancel_a,
    # show_summary,
    edit_advert_field,
    finish_create_advert,
)
from .list_advert import cmd_show_adverts
from .list_advert import navigate_adverts

router = Router()

router.include_router(start_handler.router)
router.include_router(start_create_adverts.router)
router.include_router(location_handler.router)
router.include_router(appointment.router)
router.include_router(layout_handler.router)
router.include_router(state_handler.router)
router.include_router(heating_handler.router)
router.include_router(payment_handler.router)
router.include_router(communications_handlers.router)
router.include_router(rooms_handler.router)
router.include_router(area_handler.router)
router.include_router(kitchen_area_handler.router)
router.include_router(balcony_handler.router)
router.include_router(commission_handler.router)
router.include_router(description_handler.router)
router.include_router(price_handler.router)
router.include_router(add_image_handler.router)
router.include_router(skip_photo.router)
router.include_router(finish_image.router)

# router.include_router(show_summary.router)
router.include_router(edit_advert_field.router)
router.include_router(finish_create_advert.router)
router.include_router(cmd_show_adverts.router)
router.include_router(navigate_adverts.router)
router.include_router(back_a.router)
router.include_router(cancel_a.router)
