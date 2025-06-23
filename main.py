import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from ai_generator import generate_mcq

BOT_TOKEN = os.getenv("BOT_TOKEN")

user_scores = {}
user_language = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "नमस्ते! मैं एक Quiz Bot हूँ 🧠\n"
        "कोई भी subject भेजें जैसे: /quiz Transistor\n"
        "और मैं उस पर AI से सवाल बनाऊँगा।\n"
        "अपनी भाषा चुनने के लिए /language Hindi या English लिखें।"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 Commands:\n"
        "/start - Bot शुरू करें\n"
        "/quiz <subject> - किसी भी विषय पर सवाल\n"
        "/language Hindi/English - भाषा बदलें\n"
        "/help - मदद\n\n"
        "🔧 Coming Soon:\n✅ स्कोर\n✅ कठिनाई स्तर\n✅ लीडरबोर्ड"
    )

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text("कृपया भाषा बताइए: Hindi या English\nउदाहरण: /language English")
        return

    lang = context.args[0].strip().capitalize()
    if lang not in ["Hindi", "English"]:
        await update.message.reply_text("केवल Hindi या English चुन सकते हैं।")
        return

    user_language[user_id] = lang
    await update.message.reply_text(f"✅ आपकी भाषा '{lang}' सेट कर दी गई है।")

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = user_language.get(user_id, "Hindi")

    if not context.args:
        await update.message.reply_text("कृपया विषय बताइए। जैसे: /quiz Control System")
        return

    subject = " ".join(context.args)
    await update.message.reply_text(f"🔍 विषय: {subject}\n📚 भाषा: {lang}\nMCQ तैयार किया जा रहा है...")

    mcq = generate_mcq(subject, lang)
    if mcq:
        await update.message.reply_text(mcq)
    else:
        await update.message.reply_text("❌ सवाल लाने में दिक्कत हुई। बाद में प्रयास करें।")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("quiz", quiz))
app.add_handler(CommandHandler("language", set_language))

if __name__ == "__main__":
    app.run_polling()
