#!/usr/bin/env python3
import telebot
from telebot import types
import json
import os
from datetime import datetime

BOT_TOKEN = "8705139639:AAHtMsc4yeK3BKY4oRj-3_juxxioUCaNZMI"

bot = telebot.TeleBot(BOT_TOKEN)

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

ADMIN_ID = 430974371
ADMIN_BOT_TOKEN = "8633895201:AAH1cVXc7GynUBml9uy1Smwj83RnG70cOlI"

# In-memory storage
users_db = {}

def notify_admin(text):
    try:
        import requests
        requests.post(
            f"https://api.telegram.org/bot{ADMIN_BOT_TOKEN}/sendMessage",
            json={"chat_id": ADMIN_ID, "text": text, "parse_mode": "Markdown"}
        )
    except Exception:
        pass

def save_user(user):
    uid = str(user.id)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    is_new = uid not in users_db
    if is_new:
        users_db[uid] = {
            "name": f"{user.first_name or ''} {user.last_name or ''}".strip(),
            "username": user.username or "",
            "first_visit": now,
            "last_visit": now,
            "visits": 1,
        }
        # Notify admin about new user
        username = f"@{user.username}" if user.username else "без username"
        name = users_db[uid]["name"] or "Без имени"
        notify_admin(
            f"🆕 *Новый пользователь!*\n\n"
            f"👤 {name}\n"
            f"📱 {username}\n"
            f"🆔 ID: {uid}\n"
            f"👥 Всего пользователей: {len(users_db)}"
        )
    else:
        users_db[uid]["last_visit"] = now
        users_db[uid]["visits"] = users_db[uid].get("visits", 1) + 1
    # Save to file for admin bot
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users_db, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

MENU = {
    "🍳 Завтраки": [
        {"name": "Овсянка с топпингом", "description": "280 г", "price": 205, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Oatmeal_with_dried_cranberries.jpg/1200px-Oatmeal_with_dried_cranberries.jpg"},
        {"name": "Овсянка с фруктами", "description": "320 г", "price": 265, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Oatmeal_with_dried_cranberries.jpg/1200px-Oatmeal_with_dried_cranberries.jpg"},
        {"name": "Сырники фри из творога (2 шт)", "description": "145 г, с топпингом или вареньем", "price": 265, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Syrniki.jpg/1200px-Syrniki.jpg"},
        {"name": "Сырники фри из творога (3 шт)", "description": "210 г, с топпингом или вареньем", "price": 345, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Syrniki.jpg/1200px-Syrniki.jpg"},
        {"name": "Блины с вареньем", "description": "3 шт / 150 г, или с топпингом", "price": 170, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Blinis.jpg/1200px-Blinis.jpg"},
        {"name": "Блины с творогом", "description": "2 шт / 180 г, с вареньем", "price": 195, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Blinis.jpg/1200px-Blinis.jpg"},
        {"name": "Блины с клубникой", "description": "2 шт / 180 г, со сливочным сыром", "price": 275, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Blinis.jpg/1200px-Blinis.jpg"},
        {"name": "Блины с лососем", "description": "2 шт / 180 г, со сливочным сыром", "price": 425, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Blinis.jpg/1200px-Blinis.jpg"},
        {"name": "Утренний ролл с беконом", "description": "280 г, с омлетом, томатом", "price": 305, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/1200px-Good_Food_Display_-_NCI_Visuals_Online.jpg"},
        {"name": "Утренний ролл с цыплёнком", "description": "280 г, с омлетом, томатом", "price": 325, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/1200px-Good_Food_Display_-_NCI_Visuals_Online.jpg"},
        {"name": "Утренний бейгл с яйцом", "description": "220 г", "price": 325, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Bagel-Plain-Alt.jpg/1200px-Bagel-Plain-Alt.jpg"},
        {"name": "Завтрак от Перцев", "description": "280 г, глазунья с овощами, тостами и котлетой", "price": 345, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/1200px-Good_Food_Display_-_NCI_Visuals_Online.jpg"},
        {"name": "Глазунья с томатами и зеленью", "description": "180 г", "price": 245, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/1200px-Good_Food_Display_-_NCI_Visuals_Online.jpg"},
        {"name": "Глазунья с беконом (2 яйца)", "description": "190 г", "price": 295, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/1200px-Good_Food_Display_-_NCI_Visuals_Online.jpg"},
        {"name": "Омлет с сыром и грибами", "description": "230 г", "price": 315, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/1200px-Good_Food_Display_-_NCI_Visuals_Online.jpg"},
        {"name": "Омлет с лососем", "description": "250 г", "price": 425, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/1200px-Good_Food_Display_-_NCI_Visuals_Online.jpg"},
    ],
    "🥗 Закуски и салаты": [
        {"name": "Камамбер фри", "description": "130 г, с ягодным соусом", "price": 335, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg/1200px-Eq_it-na_pizza-margherita_sep2005_sml.jpg"},
        {"name": "Луковые кольца", "description": "180 г", "price": 325, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg/1200px-Eq_it-na_pizza-margherita_sep2005_sml.jpg"},
        {"name": "Бородинские гренки", "description": "150 г", "price": 180, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg/1200px-Eq_it-na_pizza-margherita_sep2005_sml.jpg"},
        {"name": "Кесадилья с цыплёнком и сыром", "description": "130 г", "price": 295, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg/1200px-Eq_it-na_pizza-margherita_sep2005_sml.jpg"},
        {"name": "Цветная капуста с чили и мёдом", "description": "250 г", "price": 245, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg/1200px-Eq_it-na_pizza-margherita_sep2005_sml.jpg"},
        {"name": "Крылышки-гриль (5 шт)", "description": "270 г, в медовой глазури", "price": 455, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg/1200px-Eq_it-na_pizza-margherita_sep2005_sml.jpg"},
        {"name": "Мясной сет 2025", "description": "540 г", "price": 595, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg/1200px-Eq_it-na_pizza-margherita_sep2005_sml.jpg"},
        {"name": "Кобб-салат с цыплёнком", "description": "270 г", "price": 355, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Greek_salad.jpg/1200px-Greek_salad.jpg"},
        {"name": "Сицилийский салат", "description": "210 г, с цыплёнком, апельсинами и рукколой", "price": 335, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Greek_salad.jpg/1200px-Greek_salad.jpg"},
        {"name": "Классический цезарь с курицей", "description": "210 г", "price": 325, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Caesar_salad_%281%29.jpg/1200px-Caesar_salad_%281%29.jpg"},
        {"name": "Классический цезарь с креветками", "description": "210 г", "price": 475, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Caesar_salad_%281%29.jpg/1200px-Caesar_salad_%281%29.jpg"},
        {"name": "Грузинский салат", "description": "250 г, с моцареллой и свежими овощами", "price": 265, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Greek_salad.jpg/1200px-Greek_salad.jpg"},
        {"name": "Тёплый паста-салат", "description": "250 г, с фарфалле, ветчиной, шампиньонами и сыром", "price": 315, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Greek_salad.jpg/1200px-Greek_salad.jpg"},
    ],
    "🍲 Супы и горячее": [
        {"name": "Лёгкий куриный бульон", "description": "300 г, с яйцом", "price": 185, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Chicken_soup_with_noodles.jpg/1200px-Chicken_soup_with_noodles.jpg"},
        {"name": "Фирменный борщ", "description": "350 г, с говядиной и гренками с салом", "price": 260, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Chicken_soup_with_noodles.jpg/1200px-Chicken_soup_with_noodles.jpg"},
        {"name": "Тыквенный суп сливочный", "description": "220 г, с цыплёнком и песто", "price": 255, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Chicken_soup_with_noodles.jpg/1200px-Chicken_soup_with_noodles.jpg"},
        {"name": "Грибная кружка на сливках", "description": "220 г", "price": 295, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Chicken_soup_with_noodles.jpg/1200px-Chicken_soup_with_noodles.jpg"},
        {"name": "Жаркое по-ярославски", "description": "300 г, с картофельными дольками, свининой в остром сливочном соусе", "price": 365, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/New_york_strip_steak_1.jpg/1200px-New_york_strip_steak_1.jpg"},
        {"name": "Жаркое с треской", "description": "300 г, в сливочно-устричном соусе", "price": 365, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/New_york_strip_steak_1.jpg/1200px-New_york_strip_steak_1.jpg"},
        {"name": "Пельмешки запечённые с сыром", "description": "180 г", "price": 305, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/New_york_strip_steak_1.jpg/1200px-New_york_strip_steak_1.jpg"},
        {"name": "Запечённая треска", "description": "350 г, с вялеными томатами, пармезаном и цукини", "price": 555, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/New_york_strip_steak_1.jpg/1200px-New_york_strip_steak_1.jpg"},
        {"name": "Стейк из цыплёнка", "description": "350 г, с картофельным пюре и сицилийским соусом", "price": 435, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Grilled_chicken_%28cut%29.jpg/1200px-Grilled_chicken_%28cut%29.jpg"},
        {"name": "Стейк из индейки", "description": "320 г, с картофельными дольками, морковью и тыквой", "price": 585, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Grilled_chicken_%28cut%29.jpg/1200px-Grilled_chicken_%28cut%29.jpg"},
        {"name": "Стейк из свинины", "description": "450 г, с гарниром из картофеля по-деревенски", "price": 695, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/New_york_strip_steak_1.jpg/1200px-New_york_strip_steak_1.jpg"},
    ],
    "🍝 Пасты": [
        {"name": "Спагетти Карбонара", "description": "250 г, с беконом в сливочном соусе", "price": 365, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Fresh_made_Pasta_Carbonara.jpg/1200px-Fresh_made_Pasta_Carbonara.jpg"},
        {"name": "Фарфалле с курицей и грибами", "description": "300 г, в сливочном соусе", "price": 345, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Fresh_made_Pasta_Carbonara.jpg/1200px-Fresh_made_Pasta_Carbonara.jpg"},
        {"name": "Неаполитана с фрикадельками", "description": "300 г, спагетти в итальянском томатном соусе", "price": 395, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Fresh_made_Pasta_Carbonara.jpg/1200px-Fresh_made_Pasta_Carbonara.jpg"},
        {"name": "Неаполитана с креветками", "description": "300 г", "price": 445, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Fresh_made_Pasta_Carbonara.jpg/1200px-Fresh_made_Pasta_Carbonara.jpg"},
        {"name": "Ризотто с грибами", "description": "250 г, с цыплёнком и шампиньонами", "price": 355, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Fresh_made_Pasta_Carbonara.jpg/1200px-Fresh_made_Pasta_Carbonara.jpg"},
    ],
    "🥐 Бейглы и сэндвичи": [
        {"name": "Цезарь-бейгл", "description": "240 г, с цыплёнком, пармезаном и томатом", "price": 325, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Bagel-Plain-Alt.jpg/1200px-Bagel-Plain-Alt.jpg"},
        {"name": "Pepper-бейгл", "description": "240 г, с пряной говядиной, гаудой и томатом", "price": 335, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Bagel-Plain-Alt.jpg/1200px-Bagel-Plain-Alt.jpg"},
        {"name": "Fish-бейгл", "description": "240 г, с лососем, сливочным сыром, огурцом и каперсами", "price": 395, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Bagel-Plain-Alt.jpg/1200px-Bagel-Plain-Alt.jpg"},
        {"name": "Бейгл-сет с котлетой", "description": "350 г, с сочной котлетой, солёными огурцами и картофельными дольками", "price": 435, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Bagel-Plain-Alt.jpg/1200px-Bagel-Plain-Alt.jpg"},
        {"name": "Peppers Special с цыплёнком", "description": "210 г", "price": 305, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Bagel-Plain-Alt.jpg/1200px-Bagel-Plain-Alt.jpg"},
        {"name": "Peppers Special с лососем", "description": "210 г", "price": 385, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Bagel-Plain-Alt.jpg/1200px-Bagel-Plain-Alt.jpg"},
        {"name": "Сэндвич-сет с цыплёнком и фри", "description": "290 г", "price": 435, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Bagel-Plain-Alt.jpg/1200px-Bagel-Plain-Alt.jpg"},
    ],
    "🍰 Десерты": [
        {"name": "Фирменный яблочный штрудель", "description": "180 г, с шариком пломбира", "price": 255, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Tiramisu_IMGP1488.jpg/1200px-Tiramisu_IMGP1488.jpg"},
        {"name": "Малиновый Наполеон", "description": "150 г, с джемом и миндалём", "price": 215, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Tiramisu_IMGP1488.jpg/1200px-Tiramisu_IMGP1488.jpg"},
        {"name": "Чизкейк Сан Себастьян", "description": "240 г, сливочный с запечённой корочкой", "price": 335, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Cheesecake_with_strawberries_%28Philadelphia%29.jpg/1200px-Cheesecake_with_strawberries_%28Philadelphia%29.jpg"},
        {"name": "Черничный чизкейк", "description": "175 г, с натуральными ягодами без выпечки", "price": 215, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Cheesecake_with_strawberries_%28Philadelphia%29.jpg/1200px-Cheesecake_with_strawberries_%28Philadelphia%29.jpg"},
        {"name": "Панна-котта", "description": "200 г, с абрикосом, сливками, сахаром и ванилью", "price": 245, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Tiramisu_IMGP1488.jpg/1200px-Tiramisu_IMGP1488.jpg"},
        {"name": "Мороженое", "description": "50 г, сливочное / шоколадное / фисташковое", "price": 95, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Tiramisu_IMGP1488.jpg/1200px-Tiramisu_IMGP1488.jpg"},
    ],
    "☕ Кофе и чай": [
        {"name": "Эспрессо", "description": "30 мл", "price": 130, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg"},
        {"name": "Американо", "description": "200 мл", "price": 130, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg"},
        {"name": "Капучино", "description": "200 мл, или холодная версия", "price": 165, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg"},
        {"name": "Капучино XXL", "description": "300 мл", "price": 245, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg"},
        {"name": "Латте", "description": "300 мл", "price": 190, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg"},
        {"name": "Пряный Раф", "description": "250 мл", "price": 205, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg"},
        {"name": "Bumble Fresh", "description": "250 мл, апельсиновый фреш, эспрессо, карамельный топпинг", "price": 235, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg"},
        {"name": "Раф Пикник", "description": "200 мл", "price": 205, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg"},
        {"name": "Какао с маршмеллоу", "description": "200 мл", "price": 295, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg"},
        {"name": "Горячий шоколад", "description": "120 мл", "price": 295, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg"},
        {"name": "Фирменный чай Клюквенный", "description": "600 мл, с имбирём", "price": 290, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg"},
        {"name": "Фирменный чай Малиновый", "description": "600 мл, с анисом", "price": 290, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg"},
        {"name": "Фирменный чай Тропический", "description": "600 мл, с киви и базиликом", "price": 290, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg"},
        {"name": "Чай Чёрный", "description": "600 мл, Ассам / Эрл Грей / Дикая Вишня / Таёжный сбор", "price": 180, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg"},
        {"name": "Чай Зелёный", "description": "600 мл, с манго / жасмин / молочный улун", "price": 180, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg"},
    ],
    "🍹 Безалкогольные напитки": [
        {"name": "Смузи Ягодный Взрыв", "description": "250 мл, клюква, чёрная смородина, мёд, морс", "price": 245, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg"},
        {"name": "Смузи Завтрак Робинзона", "description": "250 мл, банан, ананас, пломбир, молоко", "price": 315, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg"},
        {"name": "Лимонад Фирменный (350 мл)", "description": "Малина с мятой / Яркая облепиха / Сочный апельсин", "price": 170, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg"},
        {"name": "Лимонад Фирменный (1000 мл)", "description": "Малина с мятой / Яркая облепиха / Сочный апельсин", "price": 455, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg"},
        {"name": "Молочный коктейль Пикник", "description": "250 мл, с грецким орехом и изюмом", "price": 255, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg"},
        {"name": "Молочный коктейль Классика", "description": "250 мл, шоколадный / банановый / ванильный", "price": 255, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg"},
        {"name": "Сок Классика", "description": "250 мл, ананас / апельсин / яблоко / персик / томат", "price": 95, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/2008-04-13_16-42_orange_juice.jpg/1200px-2008-04-13_16-42_orange_juice.jpg"},
        {"name": "Свежевыжатый сок", "description": "200 мл, апельсин или грейпфрут", "price": 265, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/2008-04-13_16-42_orange_juice.jpg/1200px-2008-04-13_16-42_orange_juice.jpg"},
        {"name": "Кола на разлив", "description": "250 мл", "price": 90, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg"},
        {"name": "Coca-Cola в стекле", "description": "330 мл", "price": 255, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg"},
    ],
    "🍸 Коктейли авторские": [
        {"name": "Эйприл", "description": "250 мл, Whitley Neill Rhubarb Gin, лимонный фреш, сироп бузина, пена клюква-апельсин-мёд", "price": 355},
        {"name": "Малиновый Твист", "description": "190 мл, малина на джине, лимонный фреш, сахарный сироп, яичный белок", "price": 355},
        {"name": "Глубина", "description": "300 мл, лимонная минту, ликёр Blue Curacao, лимонный фреш, лимонад лимон-лайм", "price": 355},
        {"name": "Сарти Мартини", "description": "150 мл, Sarti Aperitivo, лимонный фреш, сироп ваниль, игристое брют", "price": 355},
        {"name": "Тиффани", "description": "200 мл, настойка солёная карамель, наш адвокат, сливки, карамельно-апельсиновая пена", "price": 355},
        {"name": "Воин Дракона", "description": "350 мл, водка, персиковый ликёр, лимонный фреш, малиновый сироп, сок грейпфрут", "price": 425},
        {"name": "Бабушкин Лонг", "description": "350 мл, малина на джине, вишня на коньяке, клюковка, смородина, ликёр Cassis, лимонный фреш, морс", "price": 425},
        {"name": "Ронго", "description": "350 мл, ром, сироп маракуйя, лимонный фреш, сок персик, сок ананас", "price": 425},
        {"name": "Мартин (сезонный)", "description": "250 мл, Whitley Neill Quince, лимонный фреш, сироп манго, пена улун-мята-апельсин", "price": 355},
        {"name": "Майя (сезонный)", "description": "250 мл, Sarti Aperitivo, лимонный фреш, сироп кокос, содовая", "price": 355},
        {"name": "Аврил (сезонный)", "description": "250 мл, Pogues Irish Whiskey, лимонный фреш, пюре киви-базилик, парфюм ревень", "price": 355},
    ],
    "🍹 Коктейли классика": [
        {"name": "Кайпиринья", "description": "150 мл, Cachaca, тростниковый сахар, лайм", "price": 425},
        {"name": "Пина Колада", "description": "300 мл, ром, ананас, кокосовые сливки", "price": 425},
        {"name": "Аристей", "description": "150 мл, Berkshire Dandelion Gin, лимонный фреш, Nocino, мёд", "price": 425},
        {"name": "Ла-Манш", "description": "150 мл, Pogues Irish Whiskey, ликёр Cassis, Atxa Vermouth, биттер Peychauds", "price": 425},
        {"name": "Нью-Йорк Сауэр", "description": "200 мл, Bankhall Sweet Mash, лимонный фреш, сахарный сироп, яичный белок, Tarapaca Мерло", "price": 425},
        {"name": "Irish Coffee", "description": "190 мл, Pogues Irish Whiskey, двойной эспрессо, тростниковый сахар, сливки", "price": 425},
        {"name": "Негрони Сбальято", "description": "150 мл, Campari Bitter, Atha Vermouth, игристое брют", "price": 425},
        {"name": "Пенициллин", "description": "150 мл, Pogues Irish Whiskey, лимонный фреш, яичный белок, сахарный сироп, Laphroaig", "price": 475},
        {"name": "Aperol/Campari/Sarti Spritz", "description": "Любой коктейль из ассортимента", "price": 375},
    ],
    "🥃 Виски": [
        {"name": "Johnnie Walker Red Label", "description": "40 мл, шотландский", "price": 285},
        {"name": "James Crees", "description": "40 мл, шотландский", "price": 295},
        {"name": "Ballantines Finest", "description": "40 мл, шотландский", "price": 325},
        {"name": "Aber Falls Madeira Cask", "description": "40 мл, шотландский", "price": 325},
        {"name": "Haran 8", "description": "40 мл, шотландский", "price": 475},
        {"name": "Loch Lomond", "description": "40 мл, шотландский", "price": 595},
        {"name": "Laphroaig", "description": "40 мл, шотландский", "price": 675},
        {"name": "Glenmorangie", "description": "40 мл, шотландский", "price": 675},
        {"name": "Jim Beam White Label", "description": "40 мл, американский", "price": 345},
        {"name": "Jack Daniels", "description": "40 мл, американский", "price": 365},
        {"name": "Makers Mark", "description": "40 мл, американский", "price": 375},
        {"name": "Wild Turkey 101", "description": "40 мл, американский", "price": 675},
        {"name": "The Pogues", "description": "40 мл, ирландский", "price": 305},
        {"name": "Samuel Gelstons Pot Still", "description": "40 мл, ирландский", "price": 305},
        {"name": "Hinch Distillers Cut", "description": "40 мл, ирландский", "price": 305},
        {"name": "Peaky Blinder Irish Whiskey", "description": "40 мл, ирландский", "price": 305},
        {"name": "Proper Twelve", "description": "40 мл, ирландский", "price": 425},
        {"name": "Nestville", "description": "40 мл, из других стран", "price": 295},
        {"name": "Bankhall Sweet Mash", "description": "40 мл, из других стран", "price": 325},
        {"name": "Bellevoye Finition Grain Fin", "description": "40 мл, из других стран", "price": 495},
        {"name": "Xepec Tio Toto Cream", "description": "100 мл, херес", "price": 455},
        {"name": "Xepec Tio Toto Fino", "description": "100 мл, херес", "price": 455},
    ],
    "🍷 Вино": [
        {"name": "Cielo Bio Bio Bubbles, экстра драй", "description": "125 мл / 750 мл, Италия. Аромат цитрусов и зелёных фруктов с бодрящей свежестью", "price": 345},
        {"name": "Cape Original Moscato, сладкое", "description": "125 мл / 750 мл, ЮАР. Фруктовые и цветочные ноты, мандариновая сладость", "price": 325},
        {"name": "Рислинг Sturmwolken, п/сух", "description": "125 мл / 750 мл, Германия. Вкус спелого яблока с яркими фруктовыми оттенками", "price": 325},
        {"name": "Совиньон Блан Arco Bay, сухое", "description": "125 мл / 750 мл, Новая Зеландия. Свежий лист смородины с яркими тропиками", "price": 475},
        {"name": "Tarapaca Merlo, сухое", "description": "125 мл / 750 мл, Чили. Пряная вишня, аккорды спелой сливы", "price": 315},
        {"name": "Гарнача Celebrities, сухое", "description": "125 мл / 750 мл, Испания. Лесные ягоды и спелые тёмные фрукты", "price": 315},
        {"name": "Lakky Shiraz, полусухое", "description": "125 мл / 750 мл, Австралия. Сочный малиновый джем с табачным листом", "price": 315},
        {"name": "Порто (крепл.)", "description": "100 мл", "price": 365},
    ],
    "🍺 Пиво": [
        {"name": "Крушовице (в стекле)", "description": "450 мл, Пл. 11%, Алк. 4.8%", "price": 225},
        {"name": "Крушовице Безалкогольное", "description": "330 мл", "price": 195},
        {"name": "Крафт (банка или бутылка)", "description": "450 мл", "price": 450},
        {"name": "Oklers Weizen разлив 250 мл", "description": "Пл. 11%, Алк. 4.5%", "price": 235},
        {"name": "Oklers Weizen разлив 400 мл", "description": "Пл. 11%, Алк. 4.5%", "price": 365},
        {"name": "Pilsner Murquell разлив 250 мл", "description": "Пл. 12%, Алк. 4.8%", "price": 235},
        {"name": "Pilsner Murquell разлив 400 мл", "description": "Пл. 12%, Алк. 4.8%", "price": 365},
    ],
    "🥃 Водка": [
        {"name": "Whitley Artisanal Vodka Gold", "description": "40 мл", "price": 155},
        {"name": "Чайковский", "description": "40 мл", "price": 190},
        {"name": "Белуга Нобл", "description": "40 мл", "price": 230},
    ],
    "🍸 Джин": [
        {"name": "Whitley Neill Dry Gin", "description": "40 мл", "price": 265},
        {"name": "Whitley Neill Rhubarb&Ginger", "description": "40 мл", "price": 265},
        {"name": "Bulldog", "description": "40 мл", "price": 315},
        {"name": "Drumshanbo Gunpowder Irish Gin", "description": "40 мл", "price": 365},
        {"name": "Mare Gin", "description": "40 мл", "price": 475},
    ],
    "🥃 Ром и кашаса": [
        {"name": "Dead Mans Finger Black", "description": "40 мл", "price": 295},
        {"name": "Nusa Cana Tropical Island", "description": "40 мл", "price": 355},
        {"name": "Matusalem Solera 7", "description": "40 мл", "price": 395},
        {"name": "Diplomatico Mantuano", "description": "40 мл", "price": 395},
        {"name": "Takamaka Extra Noir", "description": "40 мл", "price": 395},
        {"name": "Cachaca", "description": "40 мл", "price": 325},
    ],
    "🥃 Коньяк и бренди": [
        {"name": "Кизляр 3*", "description": "40 мл", "price": 230},
        {"name": "Арарат 3*", "description": "40 мл", "price": 245},
        {"name": "Vecchia Romagna", "description": "40 мл", "price": 285},
        {"name": "Calvados VSOP", "description": "40 мл", "price": 465},
        {"name": "Camus VS", "description": "40 мл", "price": 490},
        {"name": "Camus VSOP", "description": "40 мл", "price": 645},
    ],
    "🌵 Текила и мескаль": [
        {"name": "Dead Mans Fingers Reposado", "description": "40 мл", "price": 295},
        {"name": "Cuerno de Toro Blanco", "description": "40 мл", "price": 355},
        {"name": "Cuerno de Toro Reposado", "description": "40 мл", "price": 375},
        {"name": "Raicilla Estancia", "description": "40 мл, мескаль", "price": 655},
    ],
    "🍶 Ликёры и вермуты": [
        {"name": "Jagermeister", "description": "40 мл", "price": 285},
        {"name": "Sambuca", "description": "40 мл", "price": 265},
        {"name": "Berkshire Sloe Gin", "description": "40 мл", "price": 265},
        {"name": "Bols (в ассортименте)", "description": "40 мл", "price": 285},
        {"name": "Atxa Vermouth", "description": "40 мл", "price": 150},
        {"name": "Carpano Dry", "description": "40 мл", "price": 160},
        {"name": "Aperol Aperitivo", "description": "40 мл", "price": 245},
        {"name": "Martini Riserva Bitter", "description": "40 мл", "price": 275},
        {"name": "Cynar Bitter", "description": "40 мл", "price": 245},
        {"name": "Campari Bitter", "description": "40 мл", "price": 265},
        {"name": "Fernet Branca", "description": "40 мл", "price": 275},
        {"name": "Branca Menta", "description": "40 мл", "price": 275},
        {"name": "Amaro Montenegro", "description": "40 мл", "price": 295},
    ],
    "🥂 Шоты и лонги": [
        {"name": "Медуза", "description": "50 мл, Самбука, Ликёр Triple Sec, Ром, Ликёр Blue Curacao, Baileys", "price": 345},
        {"name": "B-52", "description": "50 мл, Baileys, Кофейный ликёр, Ликёр Triple Sec", "price": 345},
        {"name": "Скользкий сосок", "description": "50 мл, Самбука, Baileys, Сироп гренадин", "price": 345},
        {"name": "Кровоизлияние в мозг", "description": "50 мл, Персиковый ликёр, Baileys, Сироп гренадин", "price": 325},
        {"name": "Боярский", "description": "50 мл, Водка, Сироп гренадин, Табаско", "price": 235},
        {"name": "Скорострел", "description": "50 мл, Кофейный ликёр, Настойка солёная карамель, Взбитые сливки", "price": 345},
        {"name": "Ангельские сиськи", "description": "50 мл, Наш адвокат, Самбука, Вишня мараскино", "price": 265},
        {"name": "Лонг Айленд Айс Ти", "description": "350 мл, Ром, Водка, Джин, Текила, Ликёр Triple Sec, Лимонный фреш, Кола", "price": 550},
        {"name": "Май Тай", "description": "350 мл, Белый ром, Тёмный ром, Ликёр Triple Sec, Сироп миндаль, Лимонный фреш, Сок апельсин, Сок ананас", "price": 550},
        {"name": "Аи-99", "description": "350 мл, Ром, Водка, Джин, Текила, Ликёр Triple Sec, Лимонный фреш, Сироп Blue Curacao, Лимонад лимон-лайм", "price": 550},
        {"name": "Джин-Тоник", "description": "250 мл, манго-папайя / ежевика / классика", "price": 245},
        {"name": "Ром-Кола", "description": "250 мл", "price": 265},
        {"name": "Виски-Кола", "description": "250 мл", "price": 265},
        {"name": "Aperol/Campari/Sarti Spritz", "description": "Любой коктейль из ассортимента", "price": 375},
    ],
    "🌶 Настойки Sweet Pepper": [
        {"name": "Абрикосовая", "description": "40 мл / 500 мл", "price": 150, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg"},
        {"name": "Легендарная Смородина", "description": "40 мл / 500 мл", "price": 150, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg"},
        {"name": "Облепиховая", "description": "40 мл / 500 мл", "price": 150, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg"},
        {"name": "Клюковка", "description": "40 мл / 500 мл", "price": 150, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg"},
        {"name": "Ярославская Черника", "description": "40 мл / 500 мл", "price": 150, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg"},
        {"name": "Солёная Карамель", "description": "40 мл / 500 мл", "price": 150, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg"},
        {"name": "Малина на Джине", "description": "40 мл / 500 мл", "price": 190, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg"},
        {"name": "Вишня на коньяке", "description": "40 мл / 500 мл", "price": 190, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg"},
        {"name": "Хреновуха", "description": "40 мл / 500 мл", "price": 150, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg"},
        {"name": "Наш Адвокат", "description": "40 мл", "price": 150, "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg"},
    ],
}

CAFE_INFO = {
    "name": "Sweet Pepper",
    "address": "г. Ярославль, ул. Кирова, 10-25",
    "phone": "Уточните у персонала",
    "hours": "Пн–Сб: 8:30–2:00 | Вс: 10:30–2:00",
    "welcome": "Добро пожаловать в Sweet Pepper! 🌶\nВыберите раздел меню 👇",
}



# In-memory state
review_state = {}
subscribers = set()

def main_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[types.KeyboardButton(cat) for cat in MENU.keys()])
    markup.add(types.KeyboardButton("⭐️ Оставить отзыв"))
    markup.add(types.KeyboardButton("🔔 Акции и новости"))
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
    save_user(message.from_user)
    bot.send_message(message.chat.id, f"👋 Привет! Я бот {CAFE_INFO['name']}.\n\n{CAFE_INFO['welcome']}", reply_markup=main_menu_keyboard())

@bot.message_handler(func=lambda m: m.text == "ℹ️ О нас")
def about(message):
    text = (f"🌶️ *{CAFE_INFO['name']}*\n\n"
            f"📍 {CAFE_INFO['address']}\n"
            f"📞 {CAFE_INFO['phone']}\n"
            f"🕐 Часы работы:\n{CAFE_INFO['hours']}\n\n"
            f"🎉 Акция: закажи 3 настойки — получи 4-ю в подарок!")
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=main_menu_keyboard())

@bot.message_handler(func=lambda m: m.text == "⭐️ Оставить отзыв")
def ask_review(message):
    review_state[message.chat.id] = True
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("❌ Отмена"))
    bot.send_message(message.chat.id, "⭐️ Оставьте отзыв\n\nНапишите что думаете о нас!", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "❌ Отмена")
def cancel_action(message):
    review_state.pop(message.chat.id, None)
    bot.send_message(message.chat.id, "Хорошо, возвращаемся в меню!", reply_markup=main_menu_keyboard())

@bot.message_handler(func=lambda m: review_state.get(m.chat.id))
def receive_review(message):
    review_state.pop(message.chat.id, None)
    user = message.from_user
    username = f"@{user.username}" if user.username else "без username"
    name = f"{user.first_name or ''} {user.last_name or ''}".strip() or "Аноним"
    notify_admin("⭐️ *Новый отзыв!*\n\n" + f"Имя: {name} ({username})\nТекст: {message.text}")
    bot.send_message(message.chat.id, "✅ Спасибо за отзыв! Мы ценим вашу обратную связь 🙏", reply_markup=main_menu_keyboard())

@bot.message_handler(func=lambda m: m.text == "🔔 Акции и новости")
def subscribe(message):
    uid = message.chat.id
    if uid in subscribers:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("❌ Отписаться", callback_data="unsubscribe"))
        bot.send_message(uid, "🔔 Вы уже подписаны на новости!", reply_markup=markup)
    else:
        subscribers.add(uid)
        user = message.from_user
        username = f"@{user.username}" if user.username else "без username"
        name = f"{user.first_name or ''} {user.last_name or ''}".strip() or "Аноним"
        notify_admin("🔔 *Новый подписчик!*\n\n" + f"{name} ({username})\nВсего: {len(subscribers)}")
        bot.send_message(uid, "✅ Вы подписались на акции Sweet Pepper! 🌶️", reply_markup=main_menu_keyboard())

@bot.callback_query_handler(func=lambda c: c.data == "unsubscribe")
def unsubscribe(call):
    bot.answer_callback_query(call.id)
    subscribers.discard(call.message.chat.id)
    bot.send_message(call.message.chat.id, "🔕 Вы отписались от новостей.", reply_markup=main_menu_keyboard())

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
