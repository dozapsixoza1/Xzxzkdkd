import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = "8202264301:AAGUjk8fleqjJs1P1gBS5-3cqzPenWT-8Sk"
ADMIN_ID = 6979133757
MAX_PLAYERS = 30

dp = Dispatcher()
bot = Bot(token=TOKEN)

players = []  # Список участников
form_data = {}  # Временное хранилище ответов пользователей


def keyboard_register():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Регистрация", callback_data="register")]
    ])


@dp.message(Command("start"))
async def start(msg: types.Message):
    await msg.answer(
        "🔥 Турнир на **Butterfly Legacy**!\n"
        "🏆 1 место — Butterfly Legacy\n"
        "🥈 2 место — 4000 голды\n"
        "🥉 3 место — 2000 голды\n\n"
        f"Свободных мест: {MAX_PLAYERS - len(players)}/{MAX_PLAYERS}\n\n"
        "Чтобы вступить — нажми кнопку 👇",
        reply_markup=keyboard_register()
    )


@dp.callback_query(F.data == "register")
async def register(call: types.CallbackQuery):
    if len(players) >= MAX_PLAYERS:
        await call.message.answer("❌ Мест больше нет! Лимит — 30 игроков.")
        return

    form_data[call.from_user.id] = {}
    await call.message.answer("1️⃣ Введите ваш ник-нейм:")
    await call.answer()


@dp.message(F.text)
async def form_handler(msg: types.Message):
    user_id = msg.from_user.id
    if user_id not in form_data:
        return
    
    data = form_data[user_id]

    if "nick" not in data:
        data["nick"] = msg.text
        await msg.answer("2️⃣ Введите ваш ID в игре:")
        return

    if "game_id" not in data:
        data["game_id"] = msg.text
        await msg.answer("3️⃣ Ваш возраст:")
        return

    if "age" not in data:
        data["age"] = msg.text
        await msg.answer("4️⃣ Ваша роль? (Снайпер / Рифлер / Раскид / Капитан):")
        return

    if "role" not in data:
        data["role"] = msg.text
        await msg.answer("5️⃣ Ваш ранг:")
        return

    if "rank" not in data:
        data["rank"] = msg.text
        await msg.answer("6️⃣ Готов к праку в 12:30? (Да/Нет):")
        return

    if "ready" not in data:
        data["ready"] = msg.text
        players.append(data)
        del form_data[user_id]

        place = len(players)

        await msg.answer(
            f"✅ Вы зарегистрированы!\n"
            f"Ваш номер: **{place}/{MAX_PLAYERS}**"
        )

        await bot.send_message(
            ADMIN_ID,
            f"🎯 Новый игрок #{place}\n\n"
            f"👤 Ник: {data['nick']}\n"
            f"🆔 ID: {data['game_id']}\n"
            f"🎂 Возраст: {data['age']}\n"
            f"🎯 Роль: {data['role']}\n"
            f"🏅 Ранг: {data['rank']}\n"
            f"✅ Готов? {data['ready']}"
        )


@dp.message(Command("list"))
async def list_players(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return
    
    if not players:
        await msg.answer("Список пуст!")
        return
    
    text = "📋 Список участников:\n\n"
    for i, p in enumerate(players, start=1):
        text += f"{i}. {p['nick']} — {p['role']}\n"
    
    await msg.answer(text)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
