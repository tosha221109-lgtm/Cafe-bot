#!/usr/bin/env python3
import telebot
from telebot import types

BOT_TOKEN = "8705139639:AAHtMsc4yeK3BKY4oRj-3_juxxioUCaNZMI"

bot = telebot.TeleBot(BOT_TOKEN)

MENU = {
    "🥗 Салаты": [
        {"name": "Цезарь с курицей", "description": "Листья романо, куриное филе, сухарики, пармезан, соус цезарь", "price": 390, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Caesar_salad_%281%29.jpg/1200px-Caesar_salad_%281%29.jpg"},
        {"name": "Греческий", "description": "Огурцы, помидоры, перец, маслины, сыр фета, оливковое масло", "price": 320, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Greek_salad.jpg/1200px-Greek_salad.jpg"},
        {"name": "Капрезе", "description": "Томаты, моцарелла, базилик, соус песто, бальзамик", "price": 350, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Caprese_salad_%28Najwa_photography%29.jpg/1200px-Caprese_salad_%28Najwa_photography%29.jpg"},
    ],
    "🍲 Горячие блюда": [
        {"name": "Стейк из говядины", "description": "Говяжья вырезка 250г, соус на выбор, картофель фри, овощи-гриль", "price": 890, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/New_york_strip_steak_1.jpg/1200px-New_york_strip_steak_1.jpg"},
        {"name": "Паста Карбонара", "description": "Спагетти, бекон, яйцо, пармезан, чёрный перец", "price": 450, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Fresh_made_Pasta_Carbonara.jpg/1200px-Fresh_made_Pasta_Carbonara.jpg"},
        {"name": "Куриное филе на гриле", "description": "Куриное филе 200г, соус терияки, рис басмати, свежие овощи", "price": 520, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Grilled_chicken_%28cut%29.jpg/1200px-Grilled_chicken_%28cut%29.jpg"},
    ],
    "🍕 Пицца": [
        {"name": "Маргарита", "description": "Томатный соус, моцарелла, свежий базилик (30 см)", "price": 420, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg/1200px-Eq_it-na_pizza-margherita_sep2005_sml.jpg"},
        {"name": "Пепперони", "description": "Томатный соус, моцарелла, колбаса пепперони (30 см)", "price": 490, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Supreme_pizza.jpg/1200px-Supreme_pizza.jpg"},
        {"name": "4 сыра", "description": "Сливочный соус, моцарелла, горгонзола, чеддер, пармезан (30 см)", "price": 540, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Pizza_de_queso.jpg/1200px-Pizza_de_queso.jpg"},
    ],
    "🍰 Десерты": [
        {"name": "Тирамису", "description": "Классический итальянский десерт, маскарпоне, савоярди, кофе", "price": 280, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Tiramisu_IMGP1488.jpg/1200px-Tiramisu_IMGP1488.jpg"},
        {"name": "Чизкейк Нью-Йорк", "description": "Сливочный сыр, печенье орео, ягодный соус", "price": 310, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Cheesecake_with_strawberries_%28Philadelphia%29.jpg/1200px-Cheesecake_with_strawberries_%28Philadelphia%29.jpg"},
    ],
    "☕ Напитки": [
        {"name": "Капучино", "description": "Двойной эспрессо, молоко, молочная пена (300 мл)", "price": 180, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg"},
        {"name": "Лимонад домашний", "description": "Свежевыжатый лимон, мята, сахарный сироп, газированная вода (500 мл)", "price": 220, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg"},
        {"name": "Апельсиновый сок", "description": "100% натуральный апельсиновый сок (400 мл)", "price": 250, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/2008-04-13_16-42_orange_juice.jpg/1200px-2008-04-13_16-42_orange_juice.jpg"},
    ],
}

CAFE_INFO = {"name": "Кафе «Уют»", "address": "ул. Пушкина, д. 10", "phone": "+7 (999) 123-45-67", "hours": "Пн–Пт: 09:00–22:00 | Сб–Вс: 10:00–23:00", "welcome": "Добро пожаловать! Выберите раздел меню 👇"}

def main_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[types.KeyboardButton(cat) for cat in MENU.keys()])
    markup.add(types.KeyboardButton("ℹ️ О нас"))
    return markup

def dishes_keyboard(category):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for i, dish in enumerate(MENU.get(category, [])):
        markup.add(types.InlineKeyboardButton(f"{dish['name']} — {dish['price']} ₽", callback_data=f"dish|{category}|{i}"))
    markup.add(types.InlineKeyboardButton("⬅️ Главное меню", callback_data="main_menu"))
    return markup

def dish_detail_keyboard(category, index):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f"⬅️ Назад к «{category}»", callback_data=f"cat|{category}"))
    return markup

@bot.message_handler(commands=["start", "menu"])
def cmd_start(message):
    bot.send_message(message.chat.id, f"👋 Привет! Я бот {CAFE_INFO['name']}.\n\n{CAFE_INFO['welcome']}", reply_markup=main_menu_keyboard())

@bot.message_handler(func=lambda m: m.text == "ℹ️ О нас")
def about(message):
    bot.send_message(message.chat.id, f"🏠 *{CAFE_INFO['name']}*\n\n📍 {CAFE_INFO['address']}\n📞 {CAFE_INFO['phone']}\n🕐 {CAFE_INFO['hours']}", parse_mode="Markdown", reply_markup=main_menu_keyboard())

@bot.message_handler(func=lambda m: m.text in MENU.keys())
def show_category(message):
    bot.send_message(message.chat.id, f"*{message.text}*\nВыберите блюдо:", parse_mode="Markdown", reply_markup=dishes_keyboard(message.text))

@bot.callback_query_handler(func=lambda c: c.data == "main_menu")
def cb_main_menu(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, CAFE_INFO["welcome"], reply_markup=main_menu_keyboard())

@bot.callback_query_handler(func=lambda c: c.data.startswith("cat|"))
def cb_category(call):
    bot.answer_callback_query(call.id)
    _, category = call.data.split("|", 1)
    bot.send_message(call.message.chat.id, f"*{category}*\nВыберите блюдо:", parse_mode="Markdown", reply_markup=dishes_keyboard(category))

@bot.callback_query_handler(func=lambda c: c.data.startswith("dish|"))
def cb_dish(call):
    bot.answer_callback_query(call.id)
    _, category, idx = call.data.split("|")
    dish = MENU[category][int(idx)]
    caption = f"🍽️ *{dish['name']}*\n\n📝 {dish['description']}\n\n💰 Цена: *{dish['price']} ₽*"
    try:
        bot.send_photo(call.message.chat.id, photo=dish["photo_url"], caption=caption, parse_mode="Markdown", reply_markup=dish_detail_keyboard(category, int(idx)))
    except Exception:
        bot.send_message(call.message.chat.id, caption, parse_mode="Markdown", reply_markup=dish_detail_keyboard(category, int(idx)))

if __name__ == "__main__":
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
