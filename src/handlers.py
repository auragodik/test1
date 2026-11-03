from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from src.keyboard import confirm_buttons
from src.state import Register
router = Router()

users_data = {}


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"привет, {message.from_user.first_name}!")
    print(f"пользователь {message.from_user.full_name} написал команду /start!")


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "/start - команда для запуска\n"
        "/help - список команд\n"
        "/register - зарегистрироваться\n"
        "/profile - мои данные"
    )


@router.message(Command("register"))
async def cmd_register(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer("введите имя:")


@router.message(Register.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.age)
    await message.answer("введите ваш возраст:")


@router.message(Register.age)
async def get_age(message: Message, state: FSMContext):

    if not message.text.isdigit():
        await message.answer("это не число, пж, введите возраст цифрами:")
        return

    age = int(message.text)

    if age <= 0:
        await message.answer("возраст должен быть больше нуля, введите еще раз:")
        return

    await state.update_data(age=age)
    await state.set_state(Register.confirm)

    data = await state.get_data()
    await message.answer(
        f"проверьте данные\n"
        f"имя — {data['name']}\n"
        f"возраст — {data['age']}",
        reply_markup=confirm_buttons
    )


@router.callback_query(F.data == "confirm_reg")
async def confirm_reg(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id

    users_data[user_id] = {
        "name": data["name"],
        "age": data["age"]
    }

    await callback.answer()
    await callback.message.answer("регистрация завершена!")
    await state.clear()
    print(f"зарегистрирован пользователь {user_id}: {users_data[user_id]}")


@router.callback_query(F.data == "restart_reg")
async def restart_reg(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Register.name)
    await callback.message.answer("начнем заново. введите ваше имя:")


@router.message(Command("profile"))
async def cmd_profile(message: Message):
    user_id = message.from_user.id

    if user_id in users_data:
        user = users_data[user_id]
        await message.answer(
            f"ваши данные:\n"
            f"имя — {user['name']}\n"
            f"возраст — {user['age']}"
        )
    else:
        await message.answer(
            "вы не зарегистрированы. напишите /register, чтобы пройти регистрацию."
        )


@router.message()
async def echo(message: Message):
    await message.answer(f"ты написал: {message.text}")