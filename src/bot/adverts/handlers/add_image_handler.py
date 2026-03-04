import base64
from io import BytesIO
from aiogram import Bot, Router, types, F
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from ..adverts_state import AdvertsState
from aiogram.fsm.context import FSMContext
from ..keyboard.image_kb import finish_images_kb

router = Router()


@router.message(
    AdvertsState.waiting_for_images,
    F.photo,
    ~F.text.in_([__("btn_cancel_r"), __("btn_back")]),
)
async def process_image(message: types.Message, state: FSMContext, bot: Bot):

    data = await state.get_data()
    images = data.get("image", [])

    photo = message.photo[-1]
    file_in_memory = BytesIO()
    file_info = await bot.get_file(photo.file_id)
    await bot.download(file_info, destination=file_in_memory)
    image_bytes = file_in_memory.getvalue()
    image_base_64 = base64.b64encode(image_bytes).decode("utf-8")
    new_image_obj = {
        "image_id": 0,
        "base64": image_base_64,
        "position": len(images),
        "is_delete": False,
    }
    images.append(new_image_obj)
    await state.update_data(images=images)

    await message.answer(
        _("photo_added_success").format(count=len(images))
        + "\n"
        + _("send_more_or_finish"),
        reply_markup=finish_images_kb(),
    )
