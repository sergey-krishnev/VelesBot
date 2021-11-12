from aiogram.types import CallbackQuery

from keyboards.inline.callback_data import open_menu_callback
from keyboards.inline.suggest_question import finish_suggest
from loader import dp
from utils.db_api.user_dao import get_user_by_id, register_user


@dp.callback_query_handler(open_menu_callback.filter(menu="my_profile"))
async def open_my_profile(call: CallbackQuery):
    user = get_user_by_id(call.from_user.id)
    if user is None:
        register_user(call.from_user.id)
        user = get_user_by_id(call.from_user.id)
    coin = user.get("coin")
    energy = user.get("energy")
    rank = user.get("rank")
    await call.message.edit_text(f"Мой профиль:\nИмя: {call.from_user.full_name}\n"
                                 f"Количество монет: {coin}\nКоличество энергии: {energy} из 200\n"
                                 f"Ранг: {rank}",
                                 reply_markup=finish_suggest)
