import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# --- CONFIGURACIÓN (LOGGING) ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- BANCO DE STANDS ---
STANDS = [
    "Star Platinum", "Magician's Red", "Hermit Purple", "Hierophant Green", 
    "Silver Chariot", "The Fool", "The World", "Tower of Gray", "Dark Blue Moon", 
    "Strength", "Ebony Devil", "Yellow Temperance", "Hanged Man", "Emperor", 
    "Empress", "Wheel of Fortune", "Justice", "Lovers", "Sun", "Death Thirteen", 
    "Judgement", "High Priestess", "Geb", "Khnum", "Tohth", "Anubis", "Bastet", 
    "Sethan", "Osiris", "Horus", "Atum", "Tenore Sax", "Cream",
    "Crazy Diamond", "The Hand", "Heaven's Door", "Killer Queen", "Aqua Necklace", 
    "Bad Company", "Red Hot Chili Pepper", "The Lock", "Surface", "Love Deluxe", 
    "Pearl Jam", "Achtung Baby", "Ratt", "Harvest", "Cinderella", "Atom Heart Father", 
    "Boy II Man", "Earth Wind and Fire", "Highway Star", "Stray Cat", "Super Fly", "Enigma",
    "Gold Experience", "Sticky Fingers", "Moody Blues", "Sex Pistols", "Aerosmith", 
    "Purple Haze", "Spice Girl", "Chariot Requiem", "Gold Experience Requiem", 
    "King Crimson", "Echoes", "Black Sabbath", "Soft Machine", "Kraft Work", 
    "Little Feet", "Man in the Mirror", "Mr. President", "Beach Boy", "The Grateful Dead", 
    "Baby Face", "White Album", "Clash", "Talking Head", "Notorious B.I.G.", 
    "Metallica", "Green Day", "Oasis", "Rolling Stones",
    "Stone Free", "Kiss", "Burning Down the House", "Foo Fighters", "Weather Report", 
    "Diver Down", "Whitesnake", "C-Moon", "Made in Heaven", "Goo Goo Dolls", 
    "Manhattan Transfer", "Highway to Hell", "Marilyn Manson", "Jumpin' Jack Flash", 
    "Limp Bizkit", "Survivor", "Planet Waves", "Dragon's Dream", "Yo-Yo Ma", 
    "Green, Green Grass of Home", "Jail House Lock", "Bohemian Rhapsody", 
    "Sky High", "Under World"
]

# --- FUNCIONES DEL BOT ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia la interacción."""
    keyboard = [
        [InlineKeyboardButton("🏹 ¡Quiero un Stand!", callback_data='get_stand')],
        [InlineKeyboardButton("No, soy una persona normal", callback_data='cancel')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "¡Hola! Soy Star Platanos. 🍌⭐\n\n"
        "La flecha ha aparecido ante ti. ¿Tienes la fuerza espiritual para despertar tu Stand?",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja los botones."""
    query = update.callback_query
    await query.answer() 

    if query.data == 'get_stand':
        stand = random.choice(STANDS)
        
        # MEJORA DE UX: Botón para reintentar
        keyboard = [[InlineKeyboardButton("🔄 Reintentar", callback_data='get_stand')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text=f"✨ **¡STAND DESPERTADO!** ✨\n\n"
                 f"Tu Stand es: **「 {stand} 」**\n\n",
            reply_markup=reply_markup # Agregamos el botón aquí
        )
        
    elif query.data == 'cancel':
        await query.edit_message_text(text="F (Usa /start si cambias de opinión)")

async def unknown_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """MEJORA DE UX: Responde a texto que no es comando."""
    await update.message.reply_text(
        "No entiendo tus palabras... 🍌\n"
        "Usa el comando /start para iniciar el ritual."
    )

# --- EJECUCIÓN PRINCIPAL ---

if __name__ == '__main__':
    # RECUERDA: Reemplaza con tu TOKEN real
    TOKEN = "8318357352:AAFft552B2hFLT1hR9lbMCVzSXnw6iQ_Y5w" 
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Handler para texto desconocido (debe ir al final)
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), unknown_text))
    
    print("Star Platanos V3 (UX Mejorada) listo...")
    application.run_polling()