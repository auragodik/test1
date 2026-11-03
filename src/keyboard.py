from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

confirm_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="подтвердить", callback_data="confirm_reg"),
            InlineKeyboardButton(text="начать заново", callback_data="restart_reg"),
        ]
    ]
)