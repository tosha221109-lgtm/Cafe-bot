#!/usr/bin/env python3
import telebot
from telebot import types
import json
import os
from datetime import datetime

BOT_TOKEN = "8705139639:AAHtMsc4yeK3BKY4oRj-3_juxxioUCaNZMI"
ADMIN_ID = 430974371
ADMIN_BOT_TOKEN = "8633895201:AAH1cVXc7GynUBml9uy1Smwj83RnG70cOlI"
USERS_FILE = "users.json"
MENU_FILE = "menu.json"

bot = telebot.TeleBot(BOT_TOKEN)
users_db = {}
review_state = {}
subscribers = set()

# ─────────────────────────────────────────────
#  МЕНЮ ПО УМОЛЧАНИЮ
# ─────────────────────────────────────────────
DEFAULT_MENU = {
    "🍳 Завтраки": [
        {"name": "Овсянка с топпингом", "description": "280 г", "price": 205, "weight": "280 г", "kbju": "", "photo": ""},
        {"name": "Овсянка с фруктами", "description": "320 г", "price": 265, "weight": "320 г", "kbju": "", "photo": ""},
        {"name": "Сырники фри (2 шт)", "description": "145 г, с топпингом или вареньем", "price": 265, "weight": "145 г", "kbju": "", "photo": ""},
        {"name": "Сырники фри (3 шт)", "description": "210 г, с топпингом или вареньем", "price": 345, "weight": "210 г", "kbju": "", "photo": ""},
        {"name": "Блины с вареньем", "description": "150 г", "price": 170, "weight": "150 г", "kbju": "", "photo": ""},
        {"name": "Блины с творогом", "description": "180 г", "price": 195, "weight": "180 г", "kbju": "", "photo": ""},
        {"name": "Блины с клубникой", "description": "180 г, со сливочным сыром", "price": 275, "weight": "180 г", "kbju": "", "photo": ""},
        {"name": "Блины с лососем", "description": "180 г, со сливочным сыром", "price": 425, "weight": "180 г", "kbju": "", "photo": ""},
        {"name": "Утренний ролл с беконом", "description": "280 г, с омлетом, томатом", "price": 305, "weight": "280 г", "kbju": "", "photo": ""},
        {"name": "Утренний ролл с цыплёнком", "description": "280 г, с омлетом, томатом", "price": 325, "weight": "280 г", "kbju": "", "photo": ""},
        {"name": "Утренний бейгл с яйцом", "description": "220 г", "price": 325, "weight": "220 г", "kbju": "", "photo": ""},
        {"name": "Завтрак от Перцев", "description": "280 г, глазунья с овощами и котлетой", "price": 345, "weight": "280 г", "kbju": "", "photo": ""},
        {"name": "Глазунья с томатами", "description": "180 г", "price": 245, "weight": "180 г", "kbju": "", "photo": ""},
        {"name": "Глазунья с беконом (2 яйца)", "description": "190 г", "price": 295, "weight": "190 г", "kbju": "", "photo": ""},
        {"name": "Омлет с сыром и грибами", "description": "230 г", "price": 315, "weight": "230 г", "kbju": "", "photo": ""},
        {"name": "Омлет с лососем", "description": "250 г", "price": 425, "weight": "250 г", "kbju": "", "photo": ""},
    ],
    "🥗 Закуски и салаты": [
        {"name": "Камамбер фри", "description": "130 г, с ягодным соусом", "price": 335, "weight": "130 г", "kbju": "", "photo": ""},
        {"name": "Луковые кольца", "description": "180 г", "price": 325, "weight": "180 г", "kbju": "", "photo": ""},
        {"name": "Бородинские гренки", "description": "150 г", "price": 180, "weight": "150 г", "kbju": "", "photo": ""},
        {"name": "Кесадилья с цыплёнком и сыром", "description": "130 г", "price": 295, "weight": "130 г", "kbju": "", "photo": ""},
        {"name": "Цветная капуста с чили и мёдом", "description": "250 г", "price": 245, "weight": "250 г", "kbju": "", "photo": ""},
        {"name": "Крылышки-гриль (5 шт)", "description": "270 г, в медовой глазури", "price": 455, "weight": "270 г", "kbju": "", "photo": ""},
        {"name": "Мясной сет 2025", "description": "540 г", "price": 595, "weight": "540 г", "kbju": "", "photo": ""},
        {"name": "Кобб-салат с цыплёнком", "description": "270 г", "price": 355, "weight": "270 г", "kbju": "", "photo": ""},
        {"name": "Сицилийский салат", "description": "210 г, с цыплёнком и апельсинами", "price": 335, "weight": "210 г", "kbju": "", "photo": ""},
        {"name": "Цезарь с курицей", "description": "210 г", "price": 325, "weight": "210 г", "kbju": "", "photo": ""},
        {"name": "Цезарь с креветками", "description": "210 г", "price": 475, "weight": "210 г", "kbju": "", "photo": ""},
        {"name": "Грузинский салат", "description": "250 г, с моцареллой", "price": 265, "weight": "250 г", "kbju": "", "photo": ""},
        {"name": "Тёплый паста-салат", "description": "250 г, с фарфалле и ветчиной", "price": 315, "weight": "250 г", "kbju": "", "photo": ""},
    ],
    "🍲 Супы и горячее": [
        {"name": "Лёгкий куриный бульон", "description": "300 г, с яйцом", "price": 185, "weight": "300 г", "kbju": "", "photo": ""},
        {"name": "Фирменный борщ", "description": "350 г, с говядиной", "price": 260, "weight": "350 г", "kbju": "", "photo": ""},
        {"name": "Тыквенный суп сливочный", "description": "220 г, с цыплёнком", "price": 255, "weight": "220 г", "kbju": "", "photo": ""},
        {"name": "Грибная кружка на сливках", "description": "220 г", "price": 295, "weight": "220 г", "kbju": "", "photo": ""},
        {"name": "Жаркое по-ярославски", "description": "300 г, свинина в остром сливочном соусе", "price": 365, "weight": "300 г", "kbju": "", "photo": ""},
        {"name": "Жаркое с треской", "description": "300 г, в сливочно-устричном соусе", "price": 365, "weight": "300 г", "kbju": "", "photo": ""},
        {"name": "Пельмешки запечённые с сыром", "description": "180 г", "price": 305, "weight": "180 г", "kbju": "", "photo": ""},
        {"name": "Запечённая треска", "description": "350 г, с вялеными томатами", "price": 555, "weight": "350 г", "kbju": "", "photo": ""},
        {"name": "Стейк из цыплёнка", "description": "350 г, с картофельным пюре", "price": 435, "weight": "350 г", "kbju": "", "photo": ""},
        {"name": "Стейк из индейки", "description": "320 г, с картофельными дольками", "price": 585, "weight": "320 г", "kbju": "", "photo": ""},
        {"name": "Стейк из свинины", "description": "450 г, с картофелем по-деревенски", "price": 695, "weight": "450 г", "kbju": "", "photo": ""},
    ],
    "🍝 Пасты": [
        {"name": "Спагетти Карбонара", "description": "250 г, с беконом", "price": 365, "weight": "250 г", "kbju": "", "photo": ""},
        {"name": "Фарфалле с курицей и грибами", "description": "300 г", "price": 345, "weight": "300 г", "kbju": "", "photo": ""},
        {"name": "Неаполитана с фрикадельками", "description": "300 г, в томатном соусе", "price": 395, "weight": "300 г", "kbju": "", "photo": ""},
        {"name": "Неаполитана с креветками", "description": "300 г", "price": 445, "weight": "300 г", "kbju": "", "photo": ""},
        {"name": "Ризотто с грибами", "description": "250 г, с цыплёнком", "price": 355, "weight": "250 г", "kbju": "", "photo": ""},
    ],
    "🥐 Бейглы и сэндвичи": [
        {"name": "Цезарь-бейгл", "description": "240 г, с цыплёнком", "price": 325, "weight": "240 г", "kbju": "", "photo": ""},
        {"name": "Pepper-бейгл", "description": "240 г, с говядиной", "price": 335, "weight": "240 г", "kbju": "", "photo": ""},
        {"name": "Fish-бейгл", "description": "240 г, с лососем", "price": 395, "weight": "240 г", "kbju": "", "photo": ""},
        {"name": "Chiken-бейгл", "description": "240 г, с цыплёнком барбекю", "price": 325, "weight": "240 г", "kbju": "", "photo": ""},
        {"name": "Клаб-сэндвич с цыплёнком", "description": "280 г", "price": 345, "weight": "280 г", "kbju": "", "photo": ""},
        {"name": "Клаб-сэндвич с говядиной", "description": "280 г", "price": 365, "weight": "280 г", "kbju": "", "photo": ""},
    ],
    "🍰 Десерты": [
        {"name": "Фирменный яблочный штрудель", "description": "со сливочным мороженым", "price": 255, "weight": "", "kbju": "", "photo": ""},
        {"name": "Малиновый Наполеон", "description": "", "price": 215, "weight": "", "kbju": "", "photo": ""},
        {"name": "Чизкейк Сан Себастьян", "description": "", "price": 335, "weight": "", "kbju": "", "photo": ""},
        {"name": "Черничный чизкейк", "description": "", "price": 215, "weight": "", "kbju": "", "photo": ""},
        {"name": "Панна-котта", "description": "", "price": 245, "weight": "", "kbju": "", "photo": ""},
        {"name": "Мороженое", "description": "", "price": 95, "weight": "", "kbju": "", "photo": ""},
    ],
    "☕ Кофе и чай": [
        {"name": "Эспрессо", "description": "30 мл", "price": 105, "weight": "30 мл", "kbju": "", "photo": ""},
        {"name": "Американо", "description": "150 мл", "price": 125, "weight": "150 мл", "kbju": "", "photo": ""},
        {"name": "Капучино", "description": "150 мл", "price": 175, "weight": "150 мл", "kbju": "", "photo": ""},
        {"name": "Латте", "description": "250 мл", "price": 195, "weight": "250 мл", "kbju": "", "photo": ""},
        {"name": "Флэт Уайт", "description": "150 мл", "price": 185, "weight": "150 мл", "kbju": "", "photo": ""},
        {"name": "Раф кофе", "description": "200 мл", "price": 235, "weight": "200 мл", "kbju": "", "photo": ""},
        {"name": "Матча Латте", "description": "250 мл", "price": 235, "weight": "250 мл", "kbju": "", "photo": ""},
        {"name": "Чай (чайник)", "description": "400 мл", "price": 185, "weight": "400 мл", "kbju": "", "photo": ""},
        {"name": "Облепиховый чай", "description": "400 мл", "price": 225, "weight": "400 мл", "kbju": "", "photo": ""},
    ],
    "🍹 Безалкогольные напитки": [
        {"name": "Морс клюквенный", "description": "300 мл", "price": 145, "weight": "300 мл", "kbju": "", "photo": ""},
        {"name": "Лимонад домашний", "description": "300 мл", "price": 185, "weight": "300 мл", "kbju": "", "photo": ""},
        {"name": "Свежевыжатый сок", "description": "200 мл", "price": 225, "weight": "200 мл", "kbju": "", "photo": ""},
        {"name": "Coca-Cola / Fanta / Sprite", "description": "330 мл", "price": 145, "weight": "330 мл", "kbju": "", "photo": ""},
        {"name": "Вода минеральная", "description": "500 мл", "price": 95, "weight": "500 мл", "kbju": "", "photo": ""},
    ],
    "🍸 Коктейли авторские": [
        {"name": "Эйприл", "description": "250 мл, Whitley Neill Rhubarb Gin", "price": 355, "weight": "250 мл", "kbju": "", "photo": ""},
        {"name": "Малиновый Твист", "description": "190 мл, малина на джине", "price": 355, "weight": "190 мл", "kbju": "", "photo": ""},
        {"name": "Глубина", "description": "300 мл, Blue Curacao", "price": 355, "weight": "300 мл", "kbju": "", "photo": ""},
        {"name": "Сарти Мартини", "description": "150 мл, Sarti Aperitivo", "price": 355, "weight": "150 мл", "kbju": "", "photo": ""},
        {"name": "Тиффани", "description": "200 мл, настойка солёная карамель", "price": 355, "weight": "200 мл", "kbju": "", "photo": ""},
        {"name": "Воин Дракона", "description": "350 мл, водка, персиковый ликёр", "price": 425, "weight": "350 мл", "kbju": "", "photo": ""},
        {"name": "Бабушкин Лонг", "description": "350 мл, малина на джине, вишня на коньяке", "price": 425, "weight": "350 мл", "kbju": "", "photo": ""},
        {"name": "Ронго", "description": "350 мл, ром, сироп маракуйя", "price": 425, "weight": "350 мл", "kbju": "", "photo": ""},
        {"name": "Мартин (сезонный)", "description": "250 мл, Whitley Neill Quince", "price": 355, "weight": "250 мл", "kbju": "", "photo": ""},
        {"name": "Майя (сезонный)", "description": "250 мл, Sarti Aperitivo", "price": 355, "weight": "250 мл", "kbju": "", "photo": ""},
        {"name": "Аврил (сезонный)", "description": "250 мл, Pogues Irish Whiskey", "price": 355, "weight": "250 мл", "kbju": "", "photo": ""},
    ],
    "🍹 Коктейли классика": [
        {"name": "Кайпиринья", "description": "150 мл, Cachaca, лайм", "price": 425, "weight": "150 мл", "kbju": "", "photo": ""},
        {"name": "Пина Колада", "description": "300 мл, ром, ананас", "price": 425, "weight": "300 мл", "kbju": "", "photo": ""},
        {"name": "Аристей", "description": "150 мл, Berkshire Dandelion Gin", "price": 425, "weight": "150 мл", "kbju": "", "photo": ""},
        {"name": "Ла-Манш", "description": "150 мл, Pogues Irish Whiskey", "price": 425, "weight": "150 мл", "kbju": "", "photo": ""},
        {"name": "Нью-Йорк Сауэр", "description": "200 мл, Bankhall Sweet Mash", "price": 425, "weight": "200 мл", "kbju": "", "photo": ""},
        {"name": "Irish Coffee", "description": "190 мл, Pogues Irish Whiskey, эспрессо", "price": 425, "weight": "190 мл", "kbju": "", "photo": ""},
        {"name": "Негрони Сбальято", "description": "150 мл, Campari Bitter", "price": 425, "weight": "150 мл", "kbju": "", "photo": ""},
        {"name": "Пенициллин", "description": "150 мл, Pogues Irish Whiskey, Laphroaig", "price": 475, "weight": "150 мл", "kbju": "", "photo": ""},
        {"name": "Aperol/Campari/Sarti Spritz", "description": "из ассортимента", "price": 375, "weight": "", "kbju": "", "photo": ""},
    ],
    "🥃 Виски": [
        {"name": "Johnnie Walker Red Label", "description": "40 мл, шотландский", "price": 285, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Ballantines Finest", "description": "40 мл, шотландский", "price": 325, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Loch Lomond", "description": "40 мл, шотландский", "price": 595, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Laphroaig", "description": "40 мл, шотландский", "price": 675, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Glenmorangie", "description": "40 мл, шотландский", "price": 675, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Jack Daniels", "description": "40 мл, американский", "price": 365, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Makers Mark", "description": "40 мл, американский", "price": 375, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "The Pogues", "description": "40 мл, ирландский", "price": 305, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Proper Twelve", "description": "40 мл, ирландский", "price": 425, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Bankhall Sweet Mash", "description": "40 мл", "price": 325, "weight": "40 мл", "kbju": "", "photo": ""},
    ],
    "🍷 Вино": [
        {"name": "Cielo Bio Bio Bubbles", "description": "125 мл / 750 мл, Италия", "price": 345, "weight": "125 мл", "kbju": "", "photo": ""},
        {"name": "Cape Original Moscato", "description": "125 мл / 750 мл, ЮАР, сладкое", "price": 325, "weight": "125 мл", "kbju": "", "photo": ""},
        {"name": "Рислинг Sturmwolken", "description": "125 мл / 750 мл, Германия", "price": 325, "weight": "125 мл", "kbju": "", "photo": ""},
        {"name": "Совиньон Блан Arco Bay", "description": "125 мл / 750 мл, Новая Зеландия", "price": 475, "weight": "125 мл", "kbju": "", "photo": ""},
        {"name": "Tarapaca Merlo", "description": "125 мл / 750 мл, Чили", "price": 315, "weight": "125 мл", "kbju": "", "photo": ""},
        {"name": "Гарнача Celebrities", "description": "125 мл / 750 мл, Испания", "price": 315, "weight": "125 мл", "kbju": "", "photo": ""},
        {"name": "Lakky Shiraz", "description": "125 мл / 750 мл, Австралия", "price": 315, "weight": "125 мл", "kbju": "", "photo": ""},
        {"name": "Порто (крепл.)", "description": "100 мл", "price": 365, "weight": "100 мл", "kbju": "", "photo": ""},
    ],
    "🍺 Пиво": [
        {"name": "Крушовице (в стекле)", "description": "450 мл, 4.8%", "price": 225, "weight": "450 мл", "kbju": "", "photo": ""},
        {"name": "Крушовице Безалкогольное", "description": "330 мл", "price": 195, "weight": "330 мл", "kbju": "", "photo": ""},
        {"name": "Крафт (банка или бутылка)", "description": "450 мл", "price": 450, "weight": "450 мл", "kbju": "", "photo": ""},
        {"name": "Oklers Weizen разлив 250 мл", "description": "4.5%", "price": 235, "weight": "250 мл", "kbju": "", "photo": ""},
        {"name": "Oklers Weizen разлив 400 мл", "description": "4.5%", "price": 365, "weight": "400 мл", "kbju": "", "photo": ""},
        {"name": "Pilsner Murquell разлив 250 мл", "description": "4.8%", "price": 235, "weight": "250 мл", "kbju": "", "photo": ""},
        {"name": "Pilsner Murquell разлив 400 мл", "description": "4.8%", "price": 365, "weight": "400 мл", "kbju": "", "photo": ""},
    ],
    "🥃 Водка": [
        {"name": "Whitley Artisanal Vodka Gold", "description": "40 мл", "price": 155, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Чайковский", "description": "40 мл", "price": 190, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Белуга Нобл", "description": "40 мл", "price": 230, "weight": "40 мл", "kbju": "", "photo": ""},
    ],
    "🍸 Джин": [
        {"name": "Whitley Neill Dry Gin", "description": "40 мл", "price": 265, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Whitley Neill Rhubarb&Ginger", "description": "40 мл", "price": 265, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Bulldog", "description": "40 мл", "price": 315, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Drumshanbo Gunpowder Irish Gin", "description": "40 мл", "price": 365, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Mare Gin", "description": "40 мл", "price": 475, "weight": "40 мл", "kbju": "", "photo": ""},
    ],
    "🥃 Ром и кашаса": [
        {"name": "Dead Mans Finger Black", "description": "40 мл", "price": 295, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Nusa Cana Tropical Island", "description": "40 мл", "price": 355, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Matusalem Solera 7", "description": "40 мл", "price": 395, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Diplomatico Mantuano", "description": "40 мл", "price": 395, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Takamaka Extra Noir", "description": "40 мл", "price": 395, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Cachaca", "description": "40 мл", "price": 325, "weight": "40 мл", "kbju": "", "photo": ""},
    ],
    "🥃 Коньяк и бренди": [
        {"name": "Кизляр 3*", "description": "40 мл", "price": 230, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Арарат 3*", "description": "40 мл", "price": 245, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Vecchia Romagna", "description": "40 мл", "price": 285, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Calvados VSOP", "description": "40 мл", "price": 465, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Camus VS", "description": "40 мл", "price": 490, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Camus VSOP", "description": "40 мл", "price": 645, "weight": "40 мл", "kbju": "", "photo": ""},
    ],
    "🌵 Текила и мескаль": [
        {"name": "Dead Mans Fingers Reposado", "description": "40 мл", "price": 295, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Cuerno de Toro Blanco", "description": "40 мл", "price": 355, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Cuerno de Toro Reposado", "description": "40 мл", "price": 375, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Raicilla Estancia", "description": "40 мл, мескаль", "price": 655, "weight": "40 мл", "kbju": "", "photo": ""},
    ],
    "🍶 Ликёры и вермуты": [
        {"name": "Jagermeister", "description": "40 мл", "price": 285, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Sambuca", "description": "40 мл", "price": 265, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Bols (в ассортименте)", "description": "40 мл", "price": 285, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Atxa Vermouth", "description": "40 мл", "price": 150, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Aperol Aperitivo", "description": "40 мл", "price": 245, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Campari Bitter", "description": "40 мл", "price": 265, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Fernet Branca", "description": "40 мл", "price": 275, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Amaro Montenegro", "description": "40 мл", "price": 295, "weight": "40 мл", "kbju": "", "photo": ""},
    ],
    "🥂 Шоты и лонги": [
        {"name": "Шот (40 мл)", "description": "из нашего ассортимента", "price": 150, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Лонг (200 мл)", "description": "микс на выбор", "price": 295, "weight": "200 мл", "kbju": "", "photo": ""},
    ],
    "🌶 Настойки Sweet Pepper": [
        {"name": "Ярославская Черника", "description": "40 мл / 500 мл", "price": 150, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Солёная Карамель", "description": "40 мл / 500 мл", "price": 150, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Малина на Джине", "description": "40 мл / 500 мл", "price": 190, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Вишня на коньяке", "description": "40 мл / 500 мл", "price": 190, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Хреновуха", "description": "40 мл / 500 мл", "price": 150, "weight": "40 мл", "kbju": "", "photo": ""},
        {"name": "Наш Адвокат", "description": "40 мл", "price": 150, "weight": "40 мл", "kbju": "", "photo": ""},
    ],
}

CAFE_INFO_FILE = "cafe_info.json"
DEFAULT_CAFE_INFO = {
    "name": "Sweet Pepper",
    "address": "г. Ярославль, ул. Кирова, 10-25",
    "phone": "Уточните у персонала",
    "hours": "Пн-Сб: 8:30-2:00 | Вс: 10:30-2:00",
    "welcome": "Добро пожаловать в Sweet Pepper! 🌶\nВыберите раздел меню",
    "promo": "🎉 Акция: закажи 3 настойки — получи 4-ю в подарок!",
}

def load_menu():
    if os.path.exists(MENU_FILE):
        try:
            with open(MENU_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return DEFAULT_MENU

def save_menu(menu):
    with open(MENU_FILE, "w", encoding="utf-8") as f:
        json.dump(menu, f, ensure_ascii=False, indent=2)

def load_cafe_info():
    if os.path.exists(CAFE_INFO_FILE):
        try:
            with open(CAFE_INFO_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return DEFAULT_CAFE_INFO.copy()

def save_cafe_info(info):
    with open(CAFE_INFO_FILE, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

MENU = load_menu()
CAFE_INFO = load_cafe_info()

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
        username = f"@{user.username}" if user.username else "без username"
        name = users_db[uid]["name"] or "Без имени"
        notify_admin(f"🆕 *Новый пользователь!*\n\nИмя: {name}\nUsername: {username}\nID: {uid}\nВсего: {len(users_db)}")
    else:
        users_db[uid]["last_visit"] = now
        users_db[uid]["visits"] = users_db[uid].get("visits", 1) + 1
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users_db, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def main_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[types.KeyboardButton(cat) for cat in MENU.keys()])
    markup.add(types.KeyboardButton("⭐️ Оставить отзыв"))
    markup.add(types.KeyboardButton("🔔 Акции и новости"))
    markup.add(types.KeyboardButton("📍 Как нас найти"))
    markup.add(types.KeyboardButton("ℹ️ О нас"))
    return markup

def dishes_keyboard(category):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for i, dish in enumerate(MENU.get(category, [])):
        markup.add(types.InlineKeyboardButton(
            f"{dish['name']} — {dish['price']} ₽",
            callback_data=f"dish|{category}|{i}"
        ))
    markup.add(types.InlineKeyboardButton("⬅️ Главное меню", callback_data="main_menu"))
    return markup

def dish_detail_keyboard(category, index):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f"⬅️ Назад к {category}", callback_data=f"cat|{category}"))
    return markup

@bot.message_handler(commands=["start", "menu"])
def cmd_start(message):
    save_user(message.from_user)
    bot.send_message(
        message.chat.id,
        f"👋 Привет! Я бот {CAFE_INFO['name']}.\n\n{CAFE_INFO['welcome']}",
        reply_markup=main_menu_keyboard()
    )

@bot.message_handler(func=lambda m: m.text == "ℹ️ О нас")
def about(message):
    info = load_cafe_info()
    text = (f"🌶 *{info['name']}*\n\n"
            f"📍 {info['address']}\n"
            f"🕐 Часы работы: {info['hours']}\n\n"
            f"{info.get('promo', '')}")
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=main_menu_keyboard())

@bot.message_handler(func=lambda m: m.text == "📍 Как нас найти")
def show_map(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(
        "🗺️ Открыть в Яндекс Картах",
        url="https://yandex.ru/maps/?text=%D0%AF%D1%80%D0%BE%D1%81%D0%BB%D0%B0%D0%B2%D0%BB%D1%8C+%D1%83%D0%BB+%D0%9A%D0%B8%D1%80%D0%BE%D0%B2%D0%B0+10"
    ))
    markup.add(types.InlineKeyboardButton(
        "🌍 Открыть в Google Maps",
        url="https://www.google.com/maps/search/Sweet+Pepper+%D0%AF%D1%80%D0%BE%D1%81%D0%BB%D0%B0%D0%B2%D0%BB%D1%8C"
    ))
    info = load_cafe_info()
    bot.send_message(
        message.chat.id,
        f"📍 *{info['name']}*\n\n🏙 {info['address']}\n\nВыберите приложение для навигации:",
        parse_mode="Markdown",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text == "⭐️ Оставить отзыв")
def ask_review(message):
    review_state[message.chat.id] = True
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("❌ Отмена"))
    bot.send_message(
        message.chat.id,
        "⭐️ *Оставьте ваш отзыв*\n\nНапишите что думаете о нас. Нам важно ваше мнение! 🙏",
        parse_mode="Markdown",
        reply_markup=markup
    )

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
    notify_admin(f"⭐️ *Новый отзыв!*\n\nИмя: {name} ({username})\nID: {user.id}\n\nТекст: {message.text}")
    bot.send_message(
        message.chat.id,
        "✅ Спасибо за отзыв! Мы ценим вашу обратную связь 🙏",
        reply_markup=main_menu_keyboard()
    )

@bot.message_handler(func=lambda m: m.text == "🔔 Акции и новости")
def subscribe(message):
    uid = message.chat.id
    if uid in subscribers:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("❌ Отписаться", callback_data="unsubscribe"))
        bot.send_message(uid, "🔔 Вы уже подписаны на новости Sweet Pepper!\n\nХотите отписаться?", reply_markup=markup)
    else:
        subscribers.add(uid)
        user = message.from_user
        username = f"@{user.username}" if user.username else "без username"
        name = f"{user.first_name or ''} {user.last_name or ''}".strip() or "Аноним"
        notify_admin(f"🔔 *Новый подписчик!*\n\n{name} ({username})\nВсего: {len(subscribers)}")
        bot.send_message(uid, "✅ Вы подписались на акции Sweet Pepper! 🌶", reply_markup=main_menu_keyboard())

@bot.callback_query_handler(func=lambda c: c.data == "unsubscribe")
def unsubscribe(call):
    bot.answer_callback_query(call.id)
    subscribers.discard(call.message.chat.id)
    bot.send_message(call.message.chat.id, "🔕 Вы отписались от новостей.", reply_markup=main_menu_keyboard())

@bot.message_handler(func=lambda m: m.text in MENU.keys())
def show_category(message):
    bot.send_message(
        message.chat.id,
        f"*{message.text}*\nВыберите блюдо:",
        parse_mode="Markdown",
        reply_markup=dishes_keyboard(message.text)
    )

@bot.callback_query_handler(func=lambda c: c.data == "main_menu")
def cb_main_menu(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, CAFE_INFO["welcome"], reply_markup=main_menu_keyboard())

@bot.callback_query_handler(func=lambda c: c.data.startswith("cat|"))
def cb_category(call):
    bot.answer_callback_query(call.id)
    _, category = call.data.split("|", 1)
    bot.send_message(
        call.message.chat.id,
        f"*{category}*\nВыберите блюдо:",
        parse_mode="Markdown",
        reply_markup=dishes_keyboard(category)
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("dish|"))
def cb_dish(call):
    bot.answer_callback_query(call.id)
    _, category, idx = call.data.split("|")
    dish = MENU[category][int(idx)]
    lines = [f"🍽 *{dish['name']}*"]
    if dish.get("weight"):
        lines.append(f"⚖️ Выход: {dish['weight']}")
    if dish.get("description"):
        lines.append(f"📝 {dish['description']}")
    if dish.get("kbju"):
        lines.append(f"📊 КБЖУ: {dish['kbju']}")
    lines.append(f"\n💰 Цена: *{dish['price']} ₽*")
    caption = "\n".join(lines)
    try:
        if dish.get("photo"):
            bot.send_photo(
                call.message.chat.id,
                photo=dish["photo"],
                caption=caption,
                parse_mode="Markdown",
                reply_markup=dish_detail_keyboard(category, int(idx))
            )
        else:
            bot.send_message(
                call.message.chat.id,
                caption,
                parse_mode="Markdown",
                reply_markup=dish_detail_keyboard(category, int(idx))
            )
    except Exception:
        bot.send_message(
            call.message.chat.id,
            caption,
            parse_mode="Markdown",
            reply_markup=dish_detail_keyboard(category, int(idx))
        )

if __name__ == "__main__":
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
