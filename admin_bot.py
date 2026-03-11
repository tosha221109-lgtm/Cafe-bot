#!/usr/bin/env python3
import telebot
from telebot import types
import json
import os
from datetime import datetime, timedelta

ADMIN_BOT_TOKEN = "8633895201:AAH1cVXc7GynUBml9uy1Smwj83RnG70cOlI"
MAIN_BOT_TOKEN = "8705139639:AAHtMsc4yeK3BKY4oRj-3_juxxioUCaNZMI"
ADMIN_ID = 430974371

USERS_FILE = "users.json"
MENU_FILE = "menu.json"
CAFE_INFO_FILE = "cafe_info.json"

admin_bot = telebot.TeleBot(ADMIN_BOT_TOKEN)

# Состояния админа
admin_state = {}

# ─────────────────────────────────────────────
#  ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ─────────────────────────────────────────────

def is_admin(uid):
    return uid == ADMIN_ID

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def load_menu():
    if not os.path.exists(MENU_FILE):
        return {}
    try:
        with open(MENU_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_menu(menu):
    with open(MENU_FILE, "w", encoding="utf-8") as f:
        json.dump(menu, f, ensure_ascii=False, indent=2)

def load_cafe_info():
    if not os.path.exists(CAFE_INFO_FILE):
        return {}
    try:
        with open(CAFE_INFO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_cafe_info(info):
    with open(CAFE_INFO_FILE, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

def send_to_main_bot(chat_id, text=None, photo=None, caption=None):
    import requests
    if photo:
        requests.post(
            f"https://api.telegram.org/bot{MAIN_BOT_TOKEN}/sendPhoto",
            json={"chat_id": chat_id, "photo": photo, "caption": caption or "", "parse_mode": "Markdown"}
        )
    else:
        requests.post(
            f"https://api.telegram.org/bot{MAIN_BOT_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
        )

# ─────────────────────────────────────────────
#  КЛАВИАТУРЫ
# ─────────────────────────────────────────────

def admin_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("📊 Статистика"),
        types.KeyboardButton("👥 Пользователи"),
    )
    markup.add(
        types.KeyboardButton("📢 Рассылка"),
        types.KeyboardButton("🍽 Управление меню"),
    )
    markup.add(
        types.KeyboardButton("⚙️ Настройки заведения"),
    )
    return markup

def menu_manage_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("➕ Добавить блюдо"),
        types.KeyboardButton("✏️ Редактировать блюдо"),
    )
    markup.add(
        types.KeyboardButton("❌ Удалить блюдо"),
        types.KeyboardButton("📸 Добавить фото"),
    )
    markup.add(types.KeyboardButton("⬅️ Назад"))
    return markup

def settings_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(
        types.KeyboardButton("🕐 Изменить часы работы"),
        types.KeyboardButton("📣 Изменить текст акции"),
        types.KeyboardButton("📍 Изменить адрес"),
    )
    markup.add(types.KeyboardButton("⬅️ Назад"))
    return markup

def categories_inline(action):
    menu = load_menu()
    markup = types.InlineKeyboardMarkup(row_width=1)
    for cat in menu.keys():
        markup.add(types.InlineKeyboardButton(cat, callback_data=f"{action}|{cat}"))
    markup.add(types.InlineKeyboardButton("❌ Отмена", callback_data="cancel"))
    return markup

def dishes_inline(category, action):
    menu = load_menu()
    markup = types.InlineKeyboardMarkup(row_width=1)
    for i, dish in enumerate(menu.get(category, [])):
        markup.add(types.InlineKeyboardButton(
            f"{dish['name']} — {dish['price']} ₽",
            callback_data=f"{action}|{category}|{i}"
        ))
    markup.add(types.InlineKeyboardButton("⬅️ Назад", callback_data=f"back_cats|{action}"))
    return markup

def dish_edit_keyboard(category, idx):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("✏️ Название", callback_data=f"edit_field|{category}|{idx}|name"),
        types.InlineKeyboardButton("💰 Цена", callback_data=f"edit_field|{category}|{idx}|price"),
    )
    markup.add(
        types.InlineKeyboardButton("⚖️ Выход", callback_data=f"edit_field|{category}|{idx}|weight"),
        types.InlineKeyboardButton("📝 Описание", callback_data=f"edit_field|{category}|{idx}|description"),
    )
    markup.add(
        types.InlineKeyboardButton("📊 КБЖУ", callback_data=f"edit_field|{category}|{idx}|kbju"),
        types.InlineKeyboardButton("📸 Фото", callback_data=f"edit_field|{category}|{idx}|photo"),
    )
    markup.add(types.InlineKeyboardButton("✅ Готово", callback_data="cancel"))
    return markup

# ─────────────────────────────────────────────
#  СТАРТ
# ─────────────────────────────────────────────

@admin_bot.message_handler(commands=["start"])
def cmd_start(message):
    if not is_admin(message.from_user.id):
        admin_bot.send_message(message.chat.id, "❌ Нет доступа.")
        return
    admin_bot.send_message(
        message.chat.id,
        "👋 Привет, администратор!\n\n🌶 *Панель управления Sweet Pepper*\n\nВыберите действие:",
        parse_mode="Markdown",
        reply_markup=admin_keyboard()
    )

@admin_bot.message_handler(func=lambda m: m.text == "⬅️ Назад" and is_admin(m.from_user.id))
def go_back(message):
    admin_state.pop(message.from_user.id, None)
    admin_bot.send_message(message.chat.id, "Главное меню:", reply_markup=admin_keyboard())

# ─────────────────────────────────────────────
#  СТАТИСТИКА
# ─────────────────────────────────────────────

@admin_bot.message_handler(func=lambda m: m.text == "📊 Статистика" and is_admin(m.from_user.id))
def show_stats(message):
    users = load_users()
    total = len(users)
    if total == 0:
        admin_bot.send_message(message.chat.id, "📊 Пока нет пользователей.", reply_markup=admin_keyboard())
        return
    today = datetime.now().strftime("%Y-%m-%d")
    today_count = sum(1 for u in users.values() if u.get("last_visit", "").startswith(today))
    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    week_count = sum(1 for u in users.values() if u.get("first_visit", "") >= week_ago)
    text = (f"📊 *Статистика Sweet Pepper*\n\n"
            f"👥 Всего пользователей: *{total}*\n"
            f"📅 Заходили сегодня: *{today_count}*\n"
            f"🆕 Новых за 7 дней: *{week_count}*\n\n"
            f"🕐 {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    admin_bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=admin_keyboard())

# ─────────────────────────────────────────────
#  ПОЛЬЗОВАТЕЛИ
# ─────────────────────────────────────────────

@admin_bot.message_handler(func=lambda m: m.text == "👥 Пользователи" and is_admin(m.from_user.id))
def show_users(message):
    users = load_users()
    if not users:
        admin_bot.send_message(message.chat.id, "👥 Пока нет пользователей.", reply_markup=admin_keyboard())
        return
    text = "👥 *Список пользователей:*\n\n"
    for uid, info in list(users.items())[:30]:
        name = info.get("name", "Без имени")
        username = f"@{info['username']}" if info.get("username") else "—"
        last = info.get("last_visit", "—")[:10]
        visits = info.get("visits", 1)
        text += f"• {name} ({username})\n  📅 {last} | 👁 {visits} визитов\n\n"
    if len(users) > 30:
        text += f"... и ещё {len(users) - 30} пользователей"
    admin_bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=admin_keyboard())

# ─────────────────────────────────────────────
#  РАССЫЛКА
# ─────────────────────────────────────────────

@admin_bot.message_handler(func=lambda m: m.text == "📢 Рассылка" and is_admin(m.from_user.id))
def start_broadcast(message):
    users = load_users()
    if not users:
        admin_bot.send_message(message.chat.id, "👥 Нет пользователей для рассылки.", reply_markup=admin_keyboard())
        return
    admin_state[message.from_user.id] = {"action": "broadcast"}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("⬅️ Назад"))
    admin_bot.send_message(
        message.chat.id,
        f"📢 *Рассылка*\n\nПолучателей: *{len(users)}*\n\nОтправьте текст, фото или видео:",
        parse_mode="Markdown",
        reply_markup=markup
    )

@admin_bot.message_handler(
    func=lambda m: is_admin(m.from_user.id) and admin_state.get(m.from_user.id, {}).get("action") == "broadcast",
    content_types=["text", "photo", "video"]
)
def do_broadcast(message):
    if message.text == "⬅️ Назад":
        admin_state.pop(message.from_user.id, None)
        admin_bot.send_message(message.chat.id, "Главное меню:", reply_markup=admin_keyboard())
        return
    admin_state.pop(message.from_user.id, None)
    users = load_users()
    admin_bot.send_message(message.chat.id, f"📤 Отправляю {len(users)} пользователям...", reply_markup=admin_keyboard())
    success = 0
    failed = 0
    for uid in users.keys():
        try:
            if message.content_type == "text":
                send_to_main_bot(int(uid), text=f"🌶 *Sweet Pepper*\n\n{message.text}")
            elif message.content_type == "photo":
                send_to_main_bot(int(uid), photo=message.photo[-1].file_id, caption=f"🌶 *Sweet Pepper*\n\n{message.caption or ''}")
            elif message.content_type == "video":
                import requests
                requests.post(
                    f"https://api.telegram.org/bot{MAIN_BOT_TOKEN}/sendVideo",
                    json={"chat_id": int(uid), "video": message.video.file_id, "caption": f"🌶 *Sweet Pepper*\n\n{message.caption or ''}", "parse_mode": "Markdown"}
                )
            success += 1
        except Exception:
            failed += 1
    admin_bot.send_message(
        message.chat.id,
        f"✅ *Рассылка завершена!*\n\n📨 Отправлено: *{success}*\n❌ Не доставлено: *{failed}*",
        parse_mode="Markdown",
        reply_markup=admin_keyboard()
    )

# ─────────────────────────────────────────────
#  УПРАВЛЕНИЕ МЕНЮ
# ─────────────────────────────────────────────

@admin_bot.message_handler(func=lambda m: m.text == "🍽 Управление меню" and is_admin(m.from_user.id))
def menu_manage(message):
    admin_bot.send_message(message.chat.id, "🍽 *Управление меню*\n\nВыберите действие:", parse_mode="Markdown", reply_markup=menu_manage_keyboard())

# ── ДОБАВИТЬ БЛЮДО ──

@admin_bot.message_handler(func=lambda m: m.text == "➕ Добавить блюдо" and is_admin(m.from_user.id))
def add_dish_start(message):
    admin_bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=categories_inline("add_dish"))

@admin_bot.callback_query_handler(func=lambda c: c.data.startswith("add_dish|"))
def add_dish_category(call):
    admin_bot.answer_callback_query(call.id)
    category = call.data.split("|", 1)[1]
    admin_state[call.from_user.id] = {"action": "add_dish", "category": category, "step": "name"}
    admin_bot.send_message(call.message.chat.id, f"Категория: *{category}*\n\nВведите название блюда:", parse_mode="Markdown")

# ── РЕДАКТИРОВАТЬ БЛЮДО ──

@admin_bot.message_handler(func=lambda m: m.text == "✏️ Редактировать блюдо" and is_admin(m.from_user.id))
def edit_dish_start(message):
    admin_bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=categories_inline("edit_cat"))

@admin_bot.callback_query_handler(func=lambda c: c.data.startswith("edit_cat|"))
def edit_dish_category(call):
    admin_bot.answer_callback_query(call.id)
    category = call.data.split("|", 1)[1]
    admin_bot.send_message(call.message.chat.id, f"*{category}*\nВыберите блюдо:", parse_mode="Markdown", reply_markup=dishes_inline(category, "edit_dish"))

@admin_bot.callback_query_handler(func=lambda c: c.data.startswith("edit_dish|"))
def edit_dish_select(call):
    admin_bot.answer_callback_query(call.id)
    _, category, idx = call.data.split("|")
    idx = int(idx)
    menu = load_menu()
    dish = menu[category][idx]
    text = (f"✏️ *{dish['name']}*\n\n"
            f"💰 Цена: {dish['price']} ₽\n"
            f"⚖️ Выход: {dish.get('weight', '—')}\n"
            f"📝 Описание: {dish.get('description', '—')}\n"
            f"📊 КБЖУ: {dish.get('kbju', '—')}\n"
            f"📸 Фото: {'есть' if dish.get('photo') else 'нет'}\n\n"
            f"Что редактируем?")
    admin_bot.send_message(call.message.chat.id, text, parse_mode="Markdown", reply_markup=dish_edit_keyboard(category, idx))

@admin_bot.callback_query_handler(func=lambda c: c.data.startswith("edit_field|"))
def edit_field_start(call):
    admin_bot.answer_callback_query(call.id)
    _, category, idx, field = call.data.split("|")
    field_names = {"name": "название", "price": "цену", "weight": "выход (граммы/мл)", "description": "описание", "kbju": "КБЖУ (например: 250 ккал | Б:12 Ж:8 У:30)", "photo": "фото (отправьте фото)"}
    admin_state[call.from_user.id] = {"action": "edit_field", "category": category, "idx": int(idx), "field": field}
    admin_bot.send_message(call.message.chat.id, f"Введите {field_names.get(field, field)}:")

# ── УДАЛИТЬ БЛЮДО ──

@admin_bot.message_handler(func=lambda m: m.text == "❌ Удалить блюдо" and is_admin(m.from_user.id))
def delete_dish_start(message):
    admin_bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=categories_inline("del_cat"))

@admin_bot.callback_query_handler(func=lambda c: c.data.startswith("del_cat|"))
def delete_dish_category(call):
    admin_bot.answer_callback_query(call.id)
    category = call.data.split("|", 1)[1]
    admin_bot.send_message(call.message.chat.id, f"*{category}*\nВыберите блюдо для удаления:", parse_mode="Markdown", reply_markup=dishes_inline(category, "del_dish"))

@admin_bot.callback_query_handler(func=lambda c: c.data.startswith("del_dish|"))
def delete_dish_confirm(call):
    admin_bot.answer_callback_query(call.id)
    _, category, idx = call.data.split("|")
    idx = int(idx)
    menu = load_menu()
    dish = menu[category][idx]
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Да, удалить", callback_data=f"del_confirm|{category}|{idx}"),
        types.InlineKeyboardButton("❌ Отмена", callback_data="cancel")
    )
    admin_bot.send_message(call.message.chat.id, f"Удалить *{dish['name']}* из {category}?", parse_mode="Markdown", reply_markup=markup)

@admin_bot.callback_query_handler(func=lambda c: c.data.startswith("del_confirm|"))
def delete_dish_do(call):
    admin_bot.answer_callback_query(call.id)
    _, category, idx = call.data.split("|")
    idx = int(idx)
    menu = load_menu()
    dish_name = menu[category][idx]["name"]
    del menu[category][idx]
    save_menu(menu)
    admin_bot.send_message(call.message.chat.id, f"✅ Блюдо *{dish_name}* удалено!", parse_mode="Markdown", reply_markup=menu_manage_keyboard())

# ── ДОБАВИТЬ ФОТО ──

@admin_bot.message_handler(func=lambda m: m.text == "📸 Добавить фото" and is_admin(m.from_user.id))
def add_photo_start(message):
    admin_bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=categories_inline("photo_cat"))

@admin_bot.callback_query_handler(func=lambda c: c.data.startswith("photo_cat|"))
def add_photo_category(call):
    admin_bot.answer_callback_query(call.id)
    category = call.data.split("|", 1)[1]
    admin_bot.send_message(call.message.chat.id, f"*{category}*\nВыберите блюдо:", parse_mode="Markdown", reply_markup=dishes_inline(category, "photo_dish"))

@admin_bot.callback_query_handler(func=lambda c: c.data.startswith("photo_dish|"))
def add_photo_dish(call):
    admin_bot.answer_callback_query(call.id)
    _, category, idx = call.data.split("|")
    admin_state[call.from_user.id] = {"action": "edit_field", "category": category, "idx": int(idx), "field": "photo"}
    admin_bot.send_message(call.message.chat.id, "📸 Отправьте фото блюда:")

# ── НАЗАД К КАТЕГОРИЯМ ──

@admin_bot.callback_query_handler(func=lambda c: c.data.startswith("back_cats|"))
def back_to_categories(call):
    admin_bot.answer_callback_query(call.id)
    action = call.data.split("|")[1]
    # Map action to category selector
    action_map = {"edit_dish": "edit_cat", "del_dish": "del_cat", "photo_dish": "photo_cat"}
    new_action = action_map.get(action, action)
    admin_bot.send_message(call.message.chat.id, "Выберите категорию:", reply_markup=categories_inline(new_action))

@admin_bot.callback_query_handler(func=lambda c: c.data == "cancel")
def cancel_action(call):
    admin_bot.answer_callback_query(call.id)
    admin_state.pop(call.from_user.id, None)
    admin_bot.send_message(call.message.chat.id, "Отменено.", reply_markup=menu_manage_keyboard())

# ── ОБРАБОТКА ТЕКСТОВОГО ВВОДА ──

@admin_bot.message_handler(
    func=lambda m: is_admin(m.from_user.id) and admin_state.get(m.from_user.id, {}).get("action") in ["add_dish", "edit_field"],
    content_types=["text", "photo"]
)
def handle_input(message):
    uid = message.from_user.id
    state = admin_state.get(uid, {})
    action = state.get("action")

    if action == "add_dish":
        step = state.get("step")
        category = state.get("category")
        menu = load_menu()

        if step == "name":
            state["dish_name"] = message.text
            state["step"] = "price"
            admin_state[uid] = state
            admin_bot.send_message(message.chat.id, f"Название: *{message.text}*\n\nВведите цену (только цифры):", parse_mode="Markdown")

        elif step == "price":
            try:
                price = int(message.text)
            except ValueError:
                admin_bot.send_message(message.chat.id, "❌ Введите цену цифрами, например: 350")
                return
            state["dish_price"] = price
            state["step"] = "weight"
            admin_state[uid] = state
            admin_bot.send_message(message.chat.id, f"Цена: *{price} ₽*\n\nВведите выход блюда (например: 250 г или 300 мл):\nИли напишите *-* чтобы пропустить", parse_mode="Markdown")

        elif step == "weight":
            weight = "" if message.text == "-" else message.text
            state["dish_weight"] = weight
            state["step"] = "description"
            admin_state[uid] = state
            admin_bot.send_message(message.chat.id, "Введите описание блюда:\nИли напишите *-* чтобы пропустить", parse_mode="Markdown")

        elif step == "description":
            description = "" if message.text == "-" else message.text
            state["dish_description"] = description
            state["step"] = "kbju"
            admin_state[uid] = state
            admin_bot.send_message(message.chat.id, "Введите КБЖУ (например: 320 ккал | Б:15 Ж:10 У:35):\nИли напишите *-* чтобы пропустить", parse_mode="Markdown")

        elif step == "kbju":
            kbju = "" if message.text == "-" else message.text
            # Сохраняем блюдо
            new_dish = {
                "name": state["dish_name"],
                "price": state["dish_price"],
                "weight": state.get("dish_weight", ""),
                "description": state.get("dish_description", ""),
                "kbju": kbju,
                "photo": "",
            }
            menu[category].append(new_dish)
            save_menu(menu)
            admin_state.pop(uid, None)
            admin_bot.send_message(
                message.chat.id,
                f"✅ Блюдо *{new_dish['name']}* добавлено в *{category}*!\n\nФото можно добавить через 📸 Добавить фото",
                parse_mode="Markdown",
                reply_markup=menu_manage_keyboard()
            )

    elif action == "edit_field":
        category = state.get("category")
        idx = state.get("idx")
        field = state.get("field")
        menu = load_menu()

        if field == "photo":
            if message.content_type == "photo":
                file_id = message.photo[-1].file_id
                menu[category][idx]["photo"] = file_id
                save_menu(menu)
                admin_state.pop(uid, None)
                admin_bot.send_message(message.chat.id, f"✅ Фото для *{menu[category][idx]['name']}* сохранено!", parse_mode="Markdown", reply_markup=menu_manage_keyboard())
            else:
                admin_bot.send_message(message.chat.id, "❌ Отправьте фото, не текст!")
            return

        value = message.text
        if field == "price":
            try:
                value = int(value)
            except ValueError:
                admin_bot.send_message(message.chat.id, "❌ Введите цену цифрами!")
                return

        dish_name = menu[category][idx]["name"]
        menu[category][idx][field] = value
        save_menu(menu)
        admin_state.pop(uid, None)

        field_names = {"name": "Название", "price": "Цена", "weight": "Выход", "description": "Описание", "kbju": "КБЖУ"}
        admin_bot.send_message(
            message.chat.id,
            f"✅ *{field_names.get(field, field)}* для *{dish_name}* обновлено!",
            parse_mode="Markdown",
            reply_markup=menu_manage_keyboard()
        )

# ─────────────────────────────────────────────
#  НАСТРОЙКИ ЗАВЕДЕНИЯ
# ─────────────────────────────────────────────

@admin_bot.message_handler(func=lambda m: m.text == "⚙️ Настройки заведения" and is_admin(m.from_user.id))
def settings(message):
    info = load_cafe_info()
    text = (f"⚙️ *Настройки заведения*\n\n"
            f"🕐 Часы: {info.get('hours', '—')}\n"
            f"📍 Адрес: {info.get('address', '—')}\n"
            f"📣 Акция: {info.get('promo', '—')}")
    admin_bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=settings_keyboard())

@admin_bot.message_handler(func=lambda m: m.text in ["🕐 Изменить часы работы", "📣 Изменить текст акции", "📍 Изменить адрес"] and is_admin(m.from_user.id))
def settings_edit(message):
    field_map = {
        "🕐 Изменить часы работы": ("hours", "часы работы (например: Пн-Сб: 8:30-2:00 | Вс: 10:30-2:00)"),
        "📣 Изменить текст акции": ("promo", "текст акции"),
        "📍 Изменить адрес": ("address", "адрес"),
    }
    field, hint = field_map[message.text]
    admin_state[message.from_user.id] = {"action": "edit_setting", "field": field}
    admin_bot.send_message(message.chat.id, f"Введите {hint}:")

@admin_bot.message_handler(
    func=lambda m: is_admin(m.from_user.id) and admin_state.get(m.from_user.id, {}).get("action") == "edit_setting"
)
def save_setting(message):
    uid = message.from_user.id
    field = admin_state[uid]["field"]
    info = load_cafe_info()
    info[field] = message.text
    save_cafe_info(info)
    admin_state.pop(uid, None)
    field_names = {"hours": "Часы работы", "promo": "Текст акции", "address": "Адрес"}
    admin_bot.send_message(
        message.chat.id,
        f"✅ *{field_names.get(field, field)}* обновлено!",
        parse_mode="Markdown",
        reply_markup=settings_keyboard()
    )

# ─────────────────────────────────────────────
#  ЗАПУСК
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("✅ Админ-бот Sweet Pepper запущен!")
    admin_bot.infinity_polling(timeout=10, long_polling_timeout=5)
