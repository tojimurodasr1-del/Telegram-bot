import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import google.generativeai as genai

# Sizning token va API kalitlaringiz
TELEGRAM_BOT_TOKEN = "8955600106:AAElDg3kR0R_teh4kHEDdBl5qjJttXu53kk"
GEMINI_API_KEY = "AQ.Ab8RN6L-nRXr4OfJZaKRZfGO-h-kqGVLBCFJaRDet-VAmV0q0w"

# Konsolda xatoliklarni kuzatish uchun
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Gemini AI modelini sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_message = update.message.text.lower().strip()

    # 1. Aniq shablonli salomlashuvlar
    greetings = [
        "salom", "salom alaykum", "assalomu alaykum", "assalom", 
        "salomalaykum", "vaalaykum assalom", "va alaykum assalom"
    ]
    
    if user_message in greetings:
        await update.message.reply_text("Alaykum assalom! Sizga qanday yordam bera olaman?")
        return

    # 2. Qolgan barcha savollar uchun AI (Gemini) javobi
    try:
        response = model.generate_content(update.message.text)
        ai_reply = response.text if response.text else "Javob hosil qilishda xatolik bo'ldi."
        await update.message.reply_text(ai_reply)
    except Exception as e:
        logging.error(f"AI javob berishda xatolik: {e}")
        await update.message.reply_text("Uzr, hozirda so'rovingizga javob berishda xatolik yuz berdi.")

def main():
    # Telegram botni ishga tushirish
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Matnli xabarlarga ishlov berish
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot muvaffaqiyatli ishga tushdi...")
    app.run_polling()

if __name__ == '__main__':
    main()
