import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
from groq import Groq

from products import PRODUCTS

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GROQ_API_KEY:
    logging.info(f"GROQ_API_KEY yuklandi: {GROQ_API_KEY[:10]}...")
else:
    logging.warning("GROQ_API_KEY topilmadi!")

if not TOKEN:
    print("XATO: BOT_TOKEN topilmadi! .env faylni tekshiring.")
    exit()

# Initialize bot, dispatcher and groq
bot = Bot(token=TOKEN)
dp = Dispatcher()
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# States for the order flow
class OrderState(StatesGroup):
    waiting_for_product = State()
    waiting_for_contact = State()

# Keyboards
def get_contact_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Nomer yuborish", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

# 1. Start handler
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Assalomu alaykum! Tanishaylik, man TohirMalikman. 😎\n"
        "Sodda qilib aytganda, qo'limizdan kelgancha smartfon va aksessuarlar sotamiz.\n"
        "Xizmat, nima kerak uka/opa? Bemalol so'rayvering, begona emasmiz."
    )

# 2. Message handler (Search + AI)
@dp.message(F.text & ~F.text.startswith("/"))
async def handle_messages(message: types.Message, state: FSMContext):
    text = message.text.lower()
    
    # Check if user is saying "ha", "olaman", etc. to a previous suggestion
    current_state = await state.get_state()
    if current_state == OrderState.waiting_for_product:
        positive_words = ["ha", "olaman", "ma'qul", "yaxshi", "ok", "gap yo'q", "olamiz", "vobshe"]
        if any(word in text for word in positive_words):
            await state.set_state(OrderState.waiting_for_contact)
            await message.answer(
                "Baraka toping! Aloqaga chiqishimiz uchun pastdagi tugmani bosib nomeringizni yuboring, "
                "bolalar darrov telefon qilishadi.",
                reply_markup=get_contact_keyboard()
            )
            return

    # Flexible search logic
    found_product = None
    for name in PRODUCTS.keys():
        if name in text:
            found_product = name
            break
        
    if not found_product:
        for name in PRODUCTS.keys():
            words = name.split()
            if any(word in text for word in words if len(word) > 2):
                found_product = name
                break

    if found_product:
        info = PRODUCTS[found_product]
        await state.update_data(selected_product=found_product)
        await state.set_state(OrderState.waiting_for_product)
        await message.answer(
            f"Bor uka! {found_product.capitalize()} hozirda {info['price']} turibdi.\n"
            "Olmoqchimisiz? Ma'qul kelsa ayting, rasmiylashtiramiz."
        )
    else:
        # Groq AI handles everything else (including greetings)
        if groq_client:
            try:
                system_prompt = (
                    "Sizning ismingiz TohirMalik. Siz smartfon do'koni egasisiz. "
                    "Mijozlar bilan juda samimiy, sodda, ko'cha tilida (O'zbekcha street slang) gaplashasiz. "
                    "Mijozni 'uka' yoki 'opa' deb chaqirasiz. Javoblaringiz qisqa va qiziqarli bo'lsin. "
                    "Mijoz bilan do'stona suhbat quring. "
                    "Do'kondagi mahsulotlar: " + ", ".join(PRODUCTS.keys())
                )
                
                chat_completion = groq_client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message.text}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                response_text = chat_completion.choices[0].message.content
                await message.answer(response_text)
            except Exception as e:
                logging.error(f"Groq xatosi: {e}")
                await message.answer("Uka, uzr, ozgina kalla qo'yvordim. Qaytarib yuboring-chi?")
        else:
            await message.answer("Hozircha dam olyapman, uka. Keyinroq yozing.")

# 3. Contact handler
@dp.message(OrderState.waiting_for_contact, F.contact)
async def process_contact(message: types.Message, state: FSMContext):
    contact = message.contact
    data = await state.get_data()
    product = data.get("selected_product", "Noma'lum mahsulot")
    
    # Send confirmation to user
    await message.answer(
        "Bo'ldi gap yo'q! Nomerizni oldik. Hozir tez orada bolalar aloqaga chiqishadi. 🤝",
        reply_markup=types.ReplyKeyboardRemove()
    )
    
    # Send notification to Admin
    if ADMIN_ID:
        try:
            admin_msg = (
                f"🚀 YANGI BUYURTMA!\n\n"
                f"👤 Mijoz: {contact.first_name} (@{message.from_user.username or 'yoq'})\n"
                f"📱 Tel: {contact.phone_number}\n"
                f"📦 Mahsulot: {product.capitalize()}"
            )
            # ADMIN_ID ni int ga o'tkazishga harakat qilamiz
            await bot.send_message(int(ADMIN_ID), admin_msg)
        except Exception as e:
            logging.error(f"Adminga xabar yuborishda xato: {e}")
    
    await state.clear()

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
