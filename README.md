# TohirMalik - Smartfon va Aksessuarlar Bot

Bu bot Telegram orqali smartfonlar va aksessuarlar sotuvini avtomatlashtirish uchun mo'ljallangan. Bot "TohirMalik" obrazida, samimiy ko'cha tilida javob beradi va Groq AI (Llama 3) bilan integratsiya qilingan.

## 🚀 Imkoniyatlar
- **Jonli suhbat**: Groq AI yordamida har qanday mavzuda TohirMalik obrazida suhbatlashish.
- **Mahsulot qidirish**: Do'kondagi mavjud mahsulotlarni narxi bilan ko'rsatish.
- **Buyurtma olish**: Mijozdan telefon raqamini so'rash va buyurtmani adminga yuborish.
- **Admin xabarnomasi**: Har bir yangi buyurtma haqida darhol xabar olish.

## 🛠 Texnologiyalar
- [Python 3.x](https://www.python.org/)
- [Aiogram 3.x](https://docs.aiogram.dev/) - Telegram Bot API
- [Groq SDK](https://groq.com/) - AI integratsiyasi
- [python-dotenv](https://pypi.org/project/python-dotenv/) - Maxfiy ma'lumotlarni boshqarish

## ⚙️ O'rnatish

1. Repozitoriyani yuklab oling:
   ```bash
   git clone https://github.com/USERNAME/REPO_NAME.git
   cd REPO_NAME
   ```

2. Kerakli kutubxonalarni o'rnating:
   ```bash
   pip install -r requirements.txt
   ```

3. `.env` faylini yarating va quyidagi ma'lumotlarni to'ldiring:
   ```env
   BOT_TOKEN=8636231807:AAFxEojcOL2ibwBOh1Gf4_KiTXtmXjNJVQs
   ADMIN_ID=897145046
   GROQ_API_KEY=gsk_...
   ```

4. Botni ishga tushiring:
   ```bash
   python main.py
   ```

## 📂 Fayllar tuzilmasi
- `main.py`: Botning asosiy mantiqi va AI integratsiyasi.
- `products.py`: Mahsulotlar ro'yxati (bazasi).
- `.env`: Maxfiy tokenlar (GitHub ga yuklanmaydi).
- `.gitignore`: GitHub ga yuklanmaydigan fayllar ro'yxati.

## 📝 Muallif
[Sizning Ismingiz]
