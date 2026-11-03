from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext


router = Router()




@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет {message.from_user.full_name}",
        print("{message} napisal start")
    )
@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "/start - команда для запуска\n"
        "/help - список команд",
        # reply_markup=inline_buttons
    )   
@router.message(Command("register"))
async def register(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Как тебя зовут?')
