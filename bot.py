import os, asyncio, threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "9259651602:AAE0QbA_ulvjHfVPmyXZfL-D3PIhb5hty9Y"

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()
def run_web():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), HealthHandler).serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "أهلاً بك في Notebook | 95 Quiz 📚✨\n\n"
        "أرسل أسئلتك كل سؤال في سطر بالصيغة التالية:\n"
        "السؤال | خيار1 | خيار2 | خيار3 | رقم_الإجابة\n\n"
        "مثال:\n"
        "Pharmaceutical suspensions are: | Homogeneous liquid systems | Disperse systems | Solid dosage forms | Gaseous systems | 2\n\n"
        "💡 اضغط على /pro للحصول على البرومبت الجاهز الذي يساعدك في استخراج الأسئلة واستخدام البوت بسهولة.\n\n"
        "📢 القناة الرئيسية: https://t.me/Notebok95\n"
        "👥 قناة القروب: https://t.me/notebook_95"
    )
    await update.message.reply_text(welcome_text)
async def prompt_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt_text = (
        "انسخ البرومبت التالي وأرسله لأي ذكاء اصطناعي مع ملفك أو محاضرتك:\n\n"
        "<pre>Generate multiple-choice questions (MCQs) from the text I provide.\n"
        "Format EVERY question on a single line strictly like this:\n"
        "Question | Option 1 | Option 2 | Option 3 | Option 4 | Correct Option Number\n\n"
        "Rules:\n"
        "- One question per line.\n"
        "- Use | to separate the question, options, and the correct answer number (1, 2, 3, or 4).\n"
        "- No numbering, no bullet points, and no extra text.\n"
        "- Keep questions under 300 characters and options under 100 characters.</pre>"
    )
    await update.message.reply_text(prompt_text, parse_mode="HTML")
async def handle_questions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    for line in [l.strip() for l in update.message.text.splitlines() if l.strip()]:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 4 and parts[-1].isdigit():
            q, opts, ans = parts[0], parts[1:-1], int(parts[-1]) - 1
            if 0 <= ans < len(opts):
                try:
                    await context.bot.send_poll(update.effective_chat.id, q[:300], [o[:100] for o in opts], type="quiz", correct_option_id=ans, is_anonymous=True)
                    await asyncio.sleep(0.5)
                except Exception:
                    pass

def main():
    threading.Thread(target=run_web, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler(["pro", "prompt"], prompt_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_questions))
    app.run_polling()

if __name__ == "__main__":
    main()
