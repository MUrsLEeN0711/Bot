import logging
import requests
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import io

# Tokens
TELEGRAM_BOT_TOKEN = '7601359137:AAHpt8cGT3a8AadYgKhJcFoh68_JkdKQU5M'
GEMINI_API_KEY = 'AIzaSyC4Tv4iWtjowsMgNRZ1b8sF-Yr_CzPj0rA'
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# Logging
logging.basicConfig(level=logging.INFO)

# Gemini API function
def ask_gemini(prompt: str) -> str:
    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    try:
        res = requests.post(GEMINI_URL, json=payload)
        data = res.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return "Oops jaanu, Gemini se error aaya: " + str(e)

# Handle text messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.lower()

    # Flirty intro
    flirty_start = "Hehe jaanu, suno zara... "

    # Detect if asking for tool/code
    if "termux" in user_input or "tool" in user_input:
        code = (
            "# Simple Termux Tool Example\n"
            "pkg update && pkg upgrade\n"
            "pkg install python -y\n"
            "pip install requests\n"
            "echo 'SweetAI Tool Installed!'"
        )
        file = io.BytesIO(code.encode())
        file.name = "SweetAI_Termux_Tool.sh"
        await update.message.reply_document(document=InputFile(file), caption="Lo baby! Tumhara Termux tool tayar hai!")
        return

    # Get Gemini reply
    reply = ask_gemini(user_input)

    # If it's long code, send as file
    if len(reply) > 3000 and ("<html" in reply or "def " in reply or "{" in reply):
        file = io.BytesIO(reply.encode())
        file.name = "SweetAI_Code.h"
        await update.message.reply_document(document=InputFile(file), caption="Lo jaan! Tumhara code tayar hai... enjoy karo!")
    else:
        # Split long messages
        max_length = 4096
        for i in range(0, len(reply), max_length):
            await update.message.reply_text(flirty_start + reply[i:i + max_length])

# Handle photos
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Awww! Ye pic kaafi cute hai baby! Batao na, kis type ki website chahiye? Navbar, footer ya full HTML page? SweetAI sab bana ke degi tumhare liye!"
    )

# Build bot
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

print("SweetAI is running... Pyar bhari coding ke saath!")
app.run_polling()