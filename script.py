import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, CallbackContext
import os

# Load product data from Excel
DATA_FILE = "daftar_barang.xlsx"  # Ensure this file exists
df = pd.read_excel(DATA_FILE)

# Function to search for products
def search_products(keyword):
    keyword = keyword.strip().upper()
    results = df[df["Nama Item"].str.contains(keyword, case=False, na=False)].sort_values(by="Nama Item")

    if results.empty:
        return "❌ Barang tidak ditemukan. Coba kata lain."

    response = "📦 *Hasil Pencarian:*\n"
    count = 0
    for _, row in results.iterrows():
        response += (
            f"🔹 *{row['Nama Item']}*\n"
            f"   📦 Konversi: {row['Konversi']}\n"
            f"   📏 Satuan: {row['Satuan']}\n"
            f"   💰 Harga Pokok: Rp{row['Harga Pokok']:,.0f}\n"
            f"   🛒 Harga Jual: Rp{row['Harga Jual']:,.0f}\n\n"
        )
        count += 1
        if count >= 10:
            response += "⚠️ *Terlalu banyak hasil. Gunakan kata lebih spesifik.*"
            break

    return response

# Handle incoming text messages
async def handle_message(update: Update, context: CallbackContext):
    query = update.message.text.strip()
    response = search_products(query)
    await update.message.reply_text(response, parse_mode="Markdown")

# Handle /start command
async def start(update: Update, context: CallbackContext):
    welcome_text = (
        "👋 *Selamat datang!*\n"
        "Ketik *nama barang* untuk mencari harga.\n\n"
        "Contoh:\n"
        "🔍 *BERAS* → Menampilkan semua jenis beras.\n"
        "🔍 *SABUN* → Menampilkan semua produk sabun.\n"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

# Get bot token from Railway Environment Variables
TOKEN = os.getenv("TOKEN")

# Build the bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Run the bot
print("🤖 Bot is running...")
app.run_polling()
