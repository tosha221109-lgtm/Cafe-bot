#!/usr/bin/env python3
import telebot
from telebot import types

BOT_TOKEN = “8705139639:AAHtMsc4yeK3BKY4oRj-3_juxxioUCaNZMI”

bot = telebot.TeleBot(BOT_TOKEN)

MENU = {
“🍳 Завтраки”: [
{“name”: “Овсянка с топпингом”, “description”: “280 г”, “price”: 205, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Oatmeal_with_dried_cranberries.jpg/1200px-Oatmeal_with_dried_cranberries.jpg”},
{“name”: “Овсянка с фруктами”, “description”: “320 г”, “price”: 265, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Oatmeal_with_dried_cranberries.jpg/1200px-Oatmeal_with_dried_cranberries.jpg”},
{“name”: “Сырники фри из творога (2 шт)”, “description”: “145 г, с топпингом или вареньем”, “price”: 265, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Syrniki.jpg/1200px-Syrniki.jpg”},
{“name”: “Сырники фри из творога (3 шт)”, “description”: “210 г, с топпингом или вареньем”, “price”: 345, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Syrniki.jpg/1200px-Syrniki.jpg”},
{“name”: “Блины с вареньем”, “description”: “3 шт / 150 г, или с топпингом”, “price”: 170, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Blinis.jpg/1200px-Blinis.jpg”},
{“name”: “Блины с творогом”, “description”: “2 шт / 180 г, с вареньем”, “price”: 195, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Blinis.jpg/1200px-Blinis.jpg”},
{“name”: “Блины с клубникой”, “description”: “2 шт / 180 г, со сливочным сыром”, “price”: 275, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Blinis.jpg/1200px-Blinis.jpg”},
{“name”: “Блины с лососем”, “description”: “2 шт / 180 г, со сливочным сыром”, “price”: 425, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Blinis.jpg/1200px-Blinis.jpg”},
{“name”: “Утренний ролл с беконом”, “description”: “280 г, с омлетом, томатом”, “price”: 305, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-*NCI_Visuals_Online.jpg/1200px-Good_Food_Display*-*NCI_Visuals_Online.jpg”},
{“name”: “Утренний ролл с цыплёнком”, “description”: “280 г, с омлетом, томатом”, “price”: 325, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display*-*NCI_Visuals_Online.jpg/1200px-Good_Food_Display*-*NCI_Visuals_Online.jpg”},
{“name”: “Утренний бейгл с яйцом”, “description”: “220 г”, “price”: 325, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Bagel-Plain-Alt.jpg/1200px-Bagel-Plain-Alt.jpg”},
{“name”: “Завтрак от Перцев”, “description”: “280 г, глазунья с овощами, тостами и котлетой”, “price”: 345, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display*-*NCI_Visuals_Online.jpg/1200px-Good_Food_Display*-*NCI_Visuals_Online.jpg”},
{“name”: “Глазунья с томатами и зеленью”, “description”: “180 г”, “price”: 245, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display*-*NCI_Visuals_Online.jpg/1200px-Good_Food_Display*-*NCI_Visuals_Online.jpg”},
{“name”: “Глазунья с беконом (2 яйца)”, “description”: “190 г”, “price”: 295, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display*-*NCI_Visuals_Online.jpg/1200px-Good_Food_Display*-*NCI_Visuals_Online.jpg”},
{“name”: “Омлет с сыром и грибами”, “description”: “230 г”, “price”: 315, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display*-*NCI_Visuals_Online.jpg/1200px-Good_Food_Display*-*NCI_Visuals_Online.jpg”},
{“name”: “Омлет с лососем”, “description”: “250 г”, “price”: 425, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display*-*NCI_Visuals_Online.jpg/1200px-Good_Food_Display*-*NCI_Visuals_Online.jpg”},
],
“🥗 Закуски и салаты”: [
{“name”: “Камамбер фри”, “description”: “130 г, с ягодным соусом”, “price”: 335, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg/1200px-Eq_it-na_pizza-margherita_sep2005_sml.jpg”},
{“name”: “Луковые кольца”, “description”: “180 г”, “price”: 325, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg/1200px-Eq_it-na_pizza-margherita_sep2005_sml.jpg”},
{“name”: “Бородинские гренки”, “description”: “150 г”, “price”: 180, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg/1200px-Eq_it-na_pizza-margherita_sep2005_sml.jpg”},
{“name”: “Кесадилья с цыплёнком и сыром”, “description”: “130 г”, “price”: 295, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg/1200px-Eq_it-na_pizza-margherita_sep2005_sml.jpg”},
{“name”: “Цветная капуста с чили и мёдом”, “description”: “250 г”, “price”: 245, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg/1200px-Eq_it-na_pizza-margherita_sep2005_sml.jpg”},
{“name”: “Крылышки-гриль (5 шт)”, “description”: “270 г, в медовой глазури”, “price”: 455, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg/1200px-Eq_it-na_pizza-margherita_sep2005_sml.jpg”},
{“name”: “Мясной сет 2025”, “description”: “540 г”, “price”: 595, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg/1200px-Eq_it-na_pizza-margherita_sep2005_sml.jpg”},
{“name”: “Кобб-салат с цыплёнком”, “description”: “270 г”, “price”: 355, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Greek_salad.jpg/1200px-Greek_salad.jpg”},
{“name”: “Сицилийский салат”, “description”: “210 г, с цыплёнком, апельсинами и рукколой”, “price”: 335, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Greek_salad.jpg/1200px-Greek_salad.jpg”},
{“name”: “Классический цезарь с курицей”, “description”: “210 г”, “price”: 325, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Caesar_salad*%281%29.jpg/1200px-Caesar_salad_%281%29.jpg”},
{“name”: “Классический цезарь с креветками”, “description”: “210 г”, “price”: 475, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Caesar_salad_%281%29.jpg/1200px-Caesar_salad_%281%29.jpg”},
{“name”: “Грузинский салат”, “description”: “250 г, с моцареллой и свежими овощами”, “price”: 265, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Greek_salad.jpg/1200px-Greek_salad.jpg”},
{“name”: “Тёплый паста-салат”, “description”: “250 г, с фарфалле, ветчиной, шампиньонами и сыром”, “price”: 315, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Greek_salad.jpg/1200px-Greek_salad.jpg”},
],
“🍲 Супы и горячее”: [
{“name”: “Лёгкий куриный бульон”, “description”: “300 г, с яйцом”, “price”: 185, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Chicken_soup_with_noodles.jpg/1200px-Chicken_soup_with_noodles.jpg”},
{“name”: “Фирменный борщ”, “description”: “350 г, с говядиной и гренками с салом”, “price”: 260, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Chicken_soup_with_noodles.jpg/1200px-Chicken_soup_with_noodles.jpg”},
{“name”: “Тыквенный суп сливочный”, “description”: “220 г, с цыплёнком и песто”, “price”: 255, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Chicken_soup_with_noodles.jpg/1200px-Chicken_soup_with_noodles.jpg”},
{“name”: “Грибная кружка на сливках”, “description”: “220 г”, “price”: 295, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Chicken_soup_with_noodles.jpg/1200px-Chicken_soup_with_noodles.jpg”},
{“name”: “Жаркое по-ярославски”, “description”: “300 г, с картофельными дольками, свининой в остром сливочном соусе”, “price”: 365, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/New_york_strip_steak_1.jpg/1200px-New_york_strip_steak_1.jpg”},
{“name”: “Жаркое с треской”, “description”: “300 г, в сливочно-устричном соусе”, “price”: 365, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/New_york_strip_steak_1.jpg/1200px-New_york_strip_steak_1.jpg”},
{“name”: “Пельмешки запечённые с сыром”, “description”: “180 г”, “price”: 305, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/New_york_strip_steak_1.jpg/1200px-New_york_strip_steak_1.jpg”},
{“name”: “Запечённая треска”, “description”: “350 г, с вялеными томатами, пармезаном и цукини”, “price”: 555, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/New_york_strip_steak_1.jpg/1200px-New_york_strip_steak_1.jpg”},
{“name”: “Стейк из цыплёнка”, “description”: “350 г, с картофельным пюре и сицилийским соусом”, “price”: 435, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Grilled_chicken_%28cut%29.jpg/1200px-Grilled_chicken_%28cut%29.jpg”},
{“name”: “Стейк из индейки”, “description”: “320 г, с картофельными дольками, морковью и тыквой”, “price”: 585, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Grilled_chicken_%28cut%29.jpg/1200px-Grilled_chicken_%28cut%29.jpg”},
{“name”: “Стейк из свинины”, “description”: “450 г, с гарниром из картофеля по-деревенски”, “price”: 695, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/New_york_strip_steak_1.jpg/1200px-New_york_strip_steak_1.jpg”},
],
“🍝 Пасты”: [
{“name”: “Спагетти Карбонара”, “description”: “250 г, с беконом в сливочном соусе”, “price”: 365, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Fresh_made_Pasta_Carbonara.jpg/1200px-Fresh_made_Pasta_Carbonara.jpg”},
{“name”: “Фарфалле с курицей и грибами”, “description”: “300 г, в сливочном соусе”, “price”: 345, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Fresh_made_Pasta_Carbonara.jpg/1200px-Fresh_made_Pasta_Carbonara.jpg”},
{“name”: “Неаполитана с фрикадельками”, “description”: “300 г, спагетти в итальянском томатном соусе”, “price”: 395, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Fresh_made_Pasta_Carbonara.jpg/1200px-Fresh_made_Pasta_Carbonara.jpg”},
{“name”: “Неаполитана с креветками”, “description”: “300 г”, “price”: 445, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Fresh_made_Pasta_Carbonara.jpg/1200px-Fresh_made_Pasta_Carbonara.jpg”},
{“name”: “Ризотто с грибами”, “description”: “250 г, с цыплёнком и шампиньонами”, “price”: 355, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Fresh_made_Pasta_Carbonara.jpg/1200px-Fresh_made_Pasta_Carbonara.jpg”},
],
“🥐 Бейглы и сэндвичи”: [
{“name”: “Цезарь-бейгл”, “description”: “240 г, с цыплёнком, пармезаном и томатом”, “price”: 325, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Bagel-Plain-Alt.jpg/1200px-Bagel-Plain-Alt.jpg”},
{“name”: “Pepper-бейгл”, “description”: “240 г, с пряной говядиной, гаудой и томатом”, “price”: 335, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Bagel-Plain-Alt.jpg/1200px-Bagel-Plain-Alt.jpg”},
{“name”: “Fish-бейгл”, “description”: “240 г, с лососем, сливочным сыром, огурцом и каперсами”, “price”: 395, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Bagel-Plain-Alt.jpg/1200px-Bagel-Plain-Alt.jpg”},
{“name”: “Бейгл-сет с котлетой”, “description”: “350 г, с сочной котлетой, солёными огурцами и картофельными дольками”, “price”: 435, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Bagel-Plain-Alt.jpg/1200px-Bagel-Plain-Alt.jpg”},
{“name”: “Peppers Special с цыплёнком”, “description”: “210 г”, “price”: 305, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Bagel-Plain-Alt.jpg/1200px-Bagel-Plain-Alt.jpg”},
{“name”: “Peppers Special с лососем”, “description”: “210 г”, “price”: 385, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Bagel-Plain-Alt.jpg/1200px-Bagel-Plain-Alt.jpg”},
{“name”: “Сэндвич-сет с цыплёнком и фри”, “description”: “290 г”, “price”: 435, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Bagel-Plain-Alt.jpg/1200px-Bagel-Plain-Alt.jpg”},
],
“🍰 Десерты”: [
{“name”: “Фирменный яблочный штрудель”, “description”: “180 г, с шариком пломбира”, “price”: 255, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Tiramisu_IMGP1488.jpg/1200px-Tiramisu_IMGP1488.jpg”},
{“name”: “Малиновый Наполеон”, “description”: “150 г, с джемом и миндалём”, “price”: 215, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Tiramisu_IMGP1488.jpg/1200px-Tiramisu_IMGP1488.jpg”},
{“name”: “Чизкейк Сан Себастьян”, “description”: “240 г, сливочный с запечённой корочкой”, “price”: 335, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Cheesecake_with_strawberries_%28Philadelphia%29.jpg/1200px-Cheesecake_with_strawberries_%28Philadelphia%29.jpg”},
{“name”: “Черничный чизкейк”, “description”: “175 г, с натуральными ягодами без выпечки”, “price”: 215, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Cheesecake_with_strawberries_%28Philadelphia%29.jpg/1200px-Cheesecake_with_strawberries_%28Philadelphia%29.jpg”},
{“name”: “Панна-котта”, “description”: “200 г, с абрикосом, сливками, сахаром и ванилью”, “price”: 245, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Tiramisu_IMGP1488.jpg/1200px-Tiramisu_IMGP1488.jpg”},
{“name”: “Мороженое”, “description”: “50 г, сливочное / шоколадное / фисташковое”, “price”: 95, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Tiramisu_IMGP1488.jpg/1200px-Tiramisu_IMGP1488.jpg”},
],
“☕ Кофе и чай”: [
{“name”: “Эспрессо”, “description”: “30 мл”, “price”: 130, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Американо”, “description”: “200 мл”, “price”: 130, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Капучино”, “description”: “200 мл, или холодная версия”, “price”: 165, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Капучино XXL”, “description”: “300 мл”, “price”: 245, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Латте”, “description”: “300 мл”, “price”: 190, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Пряный Раф”, “description”: “250 мл”, “price”: 205, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Bumble Fresh”, “description”: “250 мл, апельсиновый фреш, эспрессо, карамельный топпинг”, “price”: 235, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Раф Пикник”, “description”: “200 мл”, “price”: 205, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Какао с маршмеллоу”, “description”: “200 мл”, “price”: 295, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Горячий шоколад”, “description”: “120 мл”, “price”: 295, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Фирменный чай Клюквенный”, “description”: “600 мл, с имбирём”, “price”: 290, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg”},
{“name”: “Фирменный чай Малиновый”, “description”: “600 мл, с анисом”, “price”: 290, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg”},
{“name”: “Фирменный чай Тропический”, “description”: “600 мл, с киви и базиликом”, “price”: 290, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg”},
{“name”: “Чай Чёрный”, “description”: “600 мл, Ассам / Эрл Грей / Дикая Вишня / Таёжный сбор”, “price”: 180, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg”},
{“name”: “Чай Зелёный”, “description”: “600 мл, с манго / жасмин / молочный улун”, “price”: 180, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg”},
],
“🍹 Безалкогольные напитки”: [
{“name”: “Смузи Ягодный Взрыв”, “description”: “250 мл, клюква, чёрная смородина, мёд, морс”, “price”: 245, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg”},
{“name”: “Смузи Завтрак Робинзона”, “description”: “250 мл, банан, ананас, пломбир, молоко”, “price”: 315, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg”},
{“name”: “Лимонад Фирменный (350 мл)”, “description”: “Малина с мятой / Яркая облепиха / Сочный апельсин”, “price”: 170, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg”},
{“name”: “Лимонад Фирменный (1000 мл)”, “description”: “Малина с мятой / Яркая облепиха / Сочный апельсин”, “price”: 455, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg”},
{“name”: “Молочный коктейль Пикник”, “description”: “250 мл, с грецким орехом и изюмом”, “price”: 255, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg”},
{“name”: “Молочный коктейль Классика”, “description”: “250 мл, шоколадный / банановый / ванильный”, “price”: 255, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg”},
{“name”: “Сок Классика”, “description”: “250 мл, ананас / апельсин / яблоко / персик / томат”, “price”: 95, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/2008-04-13_16-42_orange_juice.jpg/1200px-2008-04-13_16-42_orange_juice.jpg”},
{“name”: “Свежевыжатый сок”, “description”: “200 мл, апельсин или грейпфрут”, “price”: 265, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/2008-04-13_16-42_orange_juice.jpg/1200px-2008-04-13_16-42_orange_juice.jpg”},
{“name”: “Кола на разлив”, “description”: “250 мл”, “price”: 90, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg”},
{“name”: “Coca-Cola в стекле”, “description”: “330 мл”, “price”: 255, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Citrus_Basil_Lemonade_%284739566741%29.jpg/1200px-Citrus_Basil_Lemonade_%284739566741%29.jpg”},
],
“🍸 Коктейли”: [
{“name”: “Эйприл”, “description”: “250 мл, Whitley Neill Rhubarb Gin, лимонный фреш, сироп бузина, пена клюква-апельсин-мёд”, “price”: 355, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Малиновый Твист”, “description”: “190 мл, малина на джине, лимонный фреш, сахарный сироп, яичный белок”, “price”: 355, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Глубина”, “description”: “300 мл, лимонная минту, ликёр Blue Curacao, лимонад лимон-лайм”, “price”: 355, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Тиффани”, “description”: “200 мл, настойка солёная карамель, наш адвокат, сливки, карамельно-апельсиновая пена”, “price”: 355, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Воин Дракона”, “description”: “350 мл, водка, персиковый ликёр, малиновый сироп, сок грейпфрут”, “price”: 425, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Ронго”, “description”: “350 мл, ром, сироп маракуйя, лимонный фреш, сок персик, сок ананас”, “price”: 425, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Лонг Айленд Айс Ти”, “description”: “350 мл, ром, водка, джин, текила, ликёр Triple Sec, лимонный фреш, кола”, “price”: 550, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Кайпиринья”, “description”: “150 мл, Cachaca, тростниковый сахар, лайм”, “price”: 425, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Негрони Сбальято”, “description”: “150 мл, Campari Bitter, Atha Vermouth, игристое брют”, “price”: 425, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Пенициллин”, “description”: “150 мл, Pogues Irish Whiskey, лимонный фреш, яичный белок, сахарный сироп, Laphroaig”, “price”: 475, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
],
“🌶 Настойки Sweet Pepper”: [
{“name”: “Абрикосовая”, “description”: “40 мл / 500 мл”, “price”: 150, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Легендарная Смородина”, “description”: “40 мл / 500 мл”, “price”: 150, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Облепиховая”, “description”: “40 мл / 500 мл”, “price”: 150, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Клюковка”, “description”: “40 мл / 500 мл”, “price”: 150, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Ярославская Черника”, “description”: “40 мл / 500 мл”, “price”: 150, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Солёная Карамель”, “description”: “40 мл / 500 мл”, “price”: 150, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Малина на Джине”, “description”: “40 мл / 500 мл”, “price”: 190, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Вишня на коньяке”, “description”: “40 мл / 500 мл”, “price”: 190, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Хреновуха”, “description”: “40 мл / 500 мл”, “price”: 150, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
{“name”: “Наш Адвокат”, “description”: “40 мл”, “price”: 150, “photo_url”: “https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Cappuccino_at_Sightglass_Coffee.jpg/1200px-Cappuccino_at_Sightglass_Coffee.jpg”},
],
}

CAFE_INFO = {
“name”: “Sweet Pepper”,
“address”: “г. Ярославль, ул. Кирова, 10-25”,
“phone”: “Уточните у персонала”,
“hours”: “Пн–Сб: 8:30–2:00 | Вс: 10:30–2:00”,
“welcome”: “Добро пожаловать в Sweet Pepper! 🌶\nВыберите раздел меню 👇”,
}

def main_menu_keyboard():
markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
markup.add(*[types.KeyboardButton(cat) for cat in MENU.keys()])
markup.add(types.KeyboardButton(“ℹ️ О нас”))
return markup

def dishes_keyboard(category):
markup = types.InlineKeyboardMarkup(row_width=1)
for i, dish in enumerate(MENU.get(category, [])):
markup.add(types.InlineKeyboardButton(f”{dish[‘name’]} — {dish[‘price’]} ₽”, callback_data=f”dish|{category}|{i}”))
markup.add(types.InlineKeyboardButton(“⬅️ Главное меню”, callback_data=“main_menu”))
return markup

def dish_detail_keyboard(category, index):
markup = types.InlineKeyboardMarkup()
markup.add(types.InlineKeyboardButton(f”⬅️ Назад к «{category}»”, callback_data=f”cat|{category}”))
return markup

@bot.message_handler(commands=[“start”, “menu”])
def cmd_start(message):
bot.send_message(message.chat.id, f”👋 Привет! Я бот {CAFE_INFO[‘name’]}.\n\n{CAFE_INFO[‘welcome’]}”, reply_markup=main_menu_keyboard())

@bot.message_handler(func=lambda m: m.text == “ℹ️ О нас”)
def about(message):
text = (f”🌶 *{CAFE_INFO[‘name’]}*\n\n”
f”📍 {CAFE_INFO[‘address’]}\n”
f”📞 {CAFE_INFO[‘phone’]}\n”
f”🕐 Часы работы:\n{CAFE_INFO[‘hours’]}\n\n”
f”🎉 Акция: закажи 3 настойки — получи 4-ю в подарок!”)
bot.send_message(message.chat.id, text, parse_mode=“Markdown”, reply_markup=main_menu_keyboard())

@bot.message_handler(func=lambda m: m.text in MENU.keys())
def show_category(message):
bot.send_message(message.chat.id, f”*{message.text}*\nВыберите блюдо:”, parse_mode=“Markdown”, reply_markup=dishes_keyboard(message.text))

@bot.callback_query_handler(func=lambda c: c.data == “main_menu”)
def cb_main_menu(call):
bot.answer_callback_query(call.id)
bot.send_message(call.message.chat.id, CAFE_INFO[“welcome”], reply_markup=main_menu_keyboard())

@bot.callback_query_handler(func=lambda c: c.data.startswith(“cat|”))
def cb_category(call):
bot.answer_callback_query(call.id)
_, category = call.data.split(”|”, 1)
bot.send_message(call.message.chat.id, f”*{category}*\nВыберите блюдо:”, parse_mode=“Markdown”, reply_markup=dishes_keyboard(category))

@bot.callback_query_handler(func=lambda c: c.data.startswith(“dish|”))
def cb_dish(call):
bot.answer_callback_query(call.id)
_, category, idx = call.data.split(”|”)
dish = MENU[category][int(idx)]
caption = f”🍽️ *{dish[‘name’]}*\n\n📝 {dish[‘description’]}\n\n💰 Цена: *{dish[‘price’]} ₽*”
try:
bot.send_photo(call.message.chat.id, photo=dish[“photo_url”], caption=caption, parse_mode=“Markdown”, reply_markup=dish_detail_keyboard(category, int(idx)))
except Exception:
bot.send_message(call.message.chat.id, caption, parse_mode=“Markdown”, reply_markup=dish_detail_keyboard(category, int(idx)))

if **name** == “**main**”:
bot.infinity_polling(timeout=10, long_polling_timeout=5)
