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

def run_web():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), HealthHandler).serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Notebook | 95 Quiz جاهز! أرسل الأسئلة (كل سؤال في سطر).")

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
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_questions))
    app.run_polling()

if __name__ == "__main__":
    main()
