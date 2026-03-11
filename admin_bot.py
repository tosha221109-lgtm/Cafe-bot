#!/usr/bin/env python3
"""
=============================================================
  🔐  АДМИН-БОТ SWEET PEPPER
=============================================================
  Функции:
    • Статистика пользователей
    • Просмотр списка пользователей
    • Рассылка сообщений всем пользователям
    • Доступ только для администратора
=============================================================
"""

import telebot
from telebot import types
import json
import os
from datetime import datetime

# ───────────────────────────────────────────────
#  🔑  ТОКЕНЫ И ID
# ───────────────────────────────────────────────
ADMIN_BOT_TOKEN = "8633895201:AAH1cVXc7GynUBml9uy1Smwj83RnG70cOlI"  # Токен админ-бота
MAIN_BOT_TOKEN  = "8705139639:AAHtMsc4yeK3BKY4oRj-3_juxxioUCaNZMI"   # Токен основного бота
ADMIN_ID = 430974371  # Твой Telegram ID

# ───────────────────────────────────────────────
#  📁  ФАЙЛ С ПОЛЬЗОВАТЕЛЯМИ (общий с основным ботом)
# ───────────────────────────────────────────────
USERS_FILE = "users.json"

admin_bot = telebot.TeleBot(ADMIN_BOT_TOKEN)
main_bot  = telebot.TeleBot(MAIN_BOT_TOKEN)

# Состояние рассылки
broadcast_state = {}

# ───────────────────────────────────────────────
#  🛠️  ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ───────────────────────────────────────────────

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def is_admin(user_id):
    return user_id == ADMIN_ID

def admin_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("📊 Статистика"),
        types.KeyboardButton("👥 Пользователи"),
        types.KeyboardButton("📢 Рассылка"),
    )
    return markup

# ───────────────────────────────────────────────
#  📨  КОМАНДЫ
# ───────────────────────────────────────────────

@admin_bot.message_handler(commands=["start"])
def cmd_start(message):
    if not is_admin(message.from_user.id):
        admin_bot.send_message(message.chat.id, "❌ У вас нет доступа к этому боту.")
        return
    admin_bot.send_message(
        message.chat.id,
        "👋 Привет, администратор!\n\n"
        "🌶 *Панель управления Sweet Pepper*\n\n"
        "Выберите действие:",
        parse_mode="Markdown",
        reply_markup=admin_keyboard()
    )

@admin_bot.message_handler(func=lambda m: m.text == "📊 Статистика" and is_admin(m.from_user.id))
def show_stats(message):
    users = load_users()
    total = len(users)

    if total == 0:
        admin_bot.send_message(message.chat.id, "📊 Пока нет пользователей.", reply_markup=admin_keyboard())
        return

    # Статистика за сегодня
    today = datetime.now().strftime("%Y-%m-%d")
    today_count = sum(1 for u in users.values() if u.get("last_visit", "").startswith(today))

    # Новые за последние 7 дней
    from datetime import timedelta
    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    week_count = sum(1 for u in users.values() if u.get("first_visit", "") >= week_ago)

    text = (
        f"📊 *Статистика Sweet Pepper*\n\n"
        f"👥 Всего пользователей: *{total}*\n"
        f"📅 Заходили сегодня: *{today_count}*\n"
        f"🆕 Новых за 7 дней: *{week_count}*\n\n"
        f"🕐 Обновлено: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    )
    admin_bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=admin_keyboard())

@admin_bot.message_handler(func=lambda m: m.text == "👥 Пользователи" and is_admin(m.from_user.id))
def show_users(message):
    users = load_users()
    if not users:
        admin_bot.send_message(message.chat.id, "👥 Пока нет пользователей.", reply_markup=admin_keyboard())
        return

    text = "👥 *Список пользователей:*\n\n"
    for uid, info in list(users.items())[:30]:  # Показываем первые 30
        name = info.get("name", "Без имени")
        username = f"@{info['username']}" if info.get("username") else "—"
        last = info.get("last_visit", "—")[:10]
        visits = info.get("visits", 1)
        text += f"• {name} ({username})\n  📅 {last} | 👁 {visits} визитов\n\n"

    if len(users) > 30:
        text += f"... и ещё {len(users) - 30} пользователей"

    admin_bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=admin_keyboard())

@admin_bot.message_handler(func=lambda m: m.text == "📢 Рассылка" and is_admin(m.from_user.id))
def start_broadcast(message):
    users = load_users()
    if not users:
        admin_bot.send_message(message.chat.id, "👥 Нет пользователей для рассылки.", reply_markup=admin_keyboard())
        return

    broadcast_state[message.from_user.id] = True
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("❌ Отмена"))
    admin_bot.send_message(
        message.chat.id,
        f"📢 *Рассылка*\n\n"
        f"Получателей: *{len(users)}* пользователей\n\n"
        f"Напишите сообщение для рассылки.\n"
        f"Можно использовать текст, фото или видео:",
        parse_mode="Markdown",
        reply_markup=markup
    )

@admin_bot.message_handler(func=lambda m: m.text == "❌ Отмена" and is_admin(m.from_user.id))
def cancel_broadcast(message):
    broadcast_state.pop(message.from_user.id, None)
    admin_bot.send_message(message.chat.id, "❌ Рассылка отменена.", reply_markup=admin_keyboard())

@admin_bot.message_handler(
    func=lambda m: is_admin(m.from_user.id) and broadcast_state.get(m.from_user.id),
    content_types=["text", "photo", "video", "document"]
)
def do_broadcast(message):
    broadcast_state.pop(message.from_user.id, None)
    users = load_users()

    admin_bot.send_message(message.chat.id, f"📤 Отправляю рассылку {len(users)} пользователям...", reply_markup=admin_keyboard())

    success = 0
    failed = 0

    for uid in users.keys():
        try:
            if message.content_type == "text":
                main_bot.send_message(int(uid), f"🌶 *Sweet Pepper*\n\n{message.text}", parse_mode="Markdown")
            elif message.content_type == "photo":
                caption = f"🌶 *Sweet Pepper*\n\n{message.caption or ''}"
                main_bot.send_photo(int(uid), message.photo[-1].file_id, caption=caption, parse_mode="Markdown")
            elif message.content_type == "video":
                caption = f"🌶 *Sweet Pepper*\n\n{message.caption or ''}"
                main_bot.send_video(int(uid), message.video.file_id, caption=caption, parse_mode="Markdown")
            success += 1
        except Exception:
            failed += 1

    admin_bot.send_message(
        message.chat.id,
        f"✅ *Рассылка завершена!*\n\n"
        f"📨 Отправлено: *{success}*\n"
        f"❌ Не доставлено: *{failed}*",
        parse_mode="Markdown",
        reply_markup=admin_keyboard()
    )

# ───────────────────────────────────────────────
#  🚀  ЗАПУСК
# ───────────────────────────────────────────────
if __name__ == "__main__":
    print("✅ Админ-бот Sweet Pepper запущен!")
    admin_bot.infinity_polling(timeout=10, long_polling_timeout=5)
