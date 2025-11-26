import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# --- CONFIGURACIÓN (LOGGING) ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- LÓGICA DE BINANCE (API) ---
def get_binance_price(symbol):
    """
    Consulta la API pública de Binance para obtener el precio de un par.
    Documentación: https://developers.binance.com/docs/binance-spot-api-docs/rest-api/general-api-information
    """
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url, timeout=5)
        response.raise_for_status() # Lanza error si la petición falla
        data = response.json()
        
        if 'price' in data:
            price = float(data['price'])
            # Formateo condicional: Si es muy pequeño (como PEPE), mostramos más decimales
            if price < 0.01:
                return f"${price:.8f} USDT"
            else:
                return f"${price:,.2f} USDT"
        else:
            return "No disponible"
    except Exception as e:
        logging.error(f"Error conectando a Binance: {e}")
        return "Error de conexión ⚠️"

# --- INTERFAZ GRÁFICA (TECLADOS) ---

def get_main_keyboard():
    """Genera los botones del menú principal."""
    keyboard = [
        [InlineKeyboardButton("₿ Bitcoin (BTC)", callback_data='calc_BTCUSDT')],
        [InlineKeyboardButton("Ξ Ethereum (ETH)", callback_data='calc_ETHUSDT')],
        [InlineKeyboardButton("🐸 Pepe (PEPE)", callback_data='calc_PEPEUSDT')],
        [InlineKeyboardButton("🔄 Actualizar Todo", callback_data='refresh_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

# --- HANDLERS (MANEJADORES) ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envía el menú inicial."""
    welcome_text = (
        "📊 **Star Platanos Crypto**\n\n"
        "Bienvenido al monitor de mercado en tiempo real.\n"
        "Los datos son obtenidos directamente de Binance.\n\n"
        "Selecciona una moneda para ver su precio actual:"
    )
    
    # Si viene de un botón (callback), editamos el mensaje anterior
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=welcome_text,
            reply_markup=get_main_keyboard(),
            parse_mode='Markdown'
        )
    # Si es un comando nuevo /start
    else:
        await update.message.reply_text(
            text=welcome_text,
            reply_markup=get_main_keyboard(),
            parse_mode='Markdown'
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja las interacciones con los botones."""
    query = update.callback_query
    await query.answer() # Feedback visual de que el botón fue presionado
    data = query.data

    if data == 'refresh_menu':
        # Simplemente recargamos el menú (útil si quisiéramos poner precios en el menú mismo)
        await start(update, context)

    elif data.startswith('calc_'):
        # Extraemos el símbolo (ej: calc_BTCUSDT -> BTCUSDT)
        symbol = data.split('_')[1]
        
        # Mapeo para mostrar nombres bonitos
        coin_names = {
            'BTCUSDT': 'Bitcoin',
            'ETHUSDT': 'Ethereum',
            'PEPEUSDT': 'Pepe Coin'
        }
        coin_name = coin_names.get(symbol, symbol)
        
        # Obtenemos el precio
        price_text = get_binance_price(symbol)
        
        # Menú de detalle
        keyboard = [
            [InlineKeyboardButton("🔄 Actualizar Precio", callback_data=data)],
            [InlineKeyboardButton("⬅️ Volver a la Lista", callback_data='refresh_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=f"📈 **Cotización Actual: {coin_name}**\n\n"
                 f"💰 Precio: `{price_text}`\n\n"
                 f"_Datos en tiempo real de Binance API_",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def unknown_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Respuesta a texto no reconocido."""
    await update.message.reply_text("⛔ Comando no reconocido.\nUsa /start para ver los precios.")

# --- MAIN ---

if __name__ == '__main__':
    # RECUERDA: Tu Token real va aquí
    TOKEN = "8318357352:AAFft552B2hFLT1hR9lbMCVzSXnw6iQ_Y5w" 
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), unknown_text))
    
    print("Star Platanos Crypto V5.0 iniciado...")
    application.run_polling()