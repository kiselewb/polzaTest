import os
import asyncio
from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

# ============================================
# КОНФИГУРАЦИЯ - ЗАПОЛНИТЕ СВОИ ДАННЫЕ
# ============================================

# Токен вашего бота (получить у @BotFather)
BOT_TOKEN = "BOT_TOKEN"

# ID чата (личный чат с ботом или группа)
# Узнать ID: отправьте боту /start и запустите get_chat_id()
CHAT_ID = "CHAT_ID"

# Путь к файлу с текстом
TEXT_FILE = "message.txt"


# ============================================


async def send_message_from_file(bot_token: str, chat_id: str, file_path: str):
    """
    Отправляет текст из файла в Telegram-чат
    """
    bot = Bot(token=bot_token)

    try:
        # Проверка существования файла
        if not os.path.exists(file_path):
            print(f"❌ Ошибка: Файл '{file_path}' не найден!")
            return False

        # Чтение текста из файла
        with open(file_path, 'r', encoding='utf-8') as f:
            message_text = f.read().strip()

        if not message_text:
            print("❌ Ошибка: Файл пустой!")
            return False

        print(f"📄 Текст из файла загружен ({len(message_text)} символов)")
        print(f"📤 Отправка сообщения в чат {chat_id}...")

        # Telegram ограничивает длину сообщения 4096 символов
        if len(message_text) > 4096:
            print("⚠️  Сообщение длинное, разбиваем на части...")
            # Разбиваем на части по 4000 символов
            chunks = [message_text[i:i + 4000] for i in range(0, len(message_text), 4000)]
            for i, chunk in enumerate(chunks, 1):
                await bot.send_message(chat_id=chat_id, text=chunk)
                print(f"   ✅ Отправлена часть {i}/{len(chunks)}")
                await asyncio.sleep(0.5)  # Небольшая задержка между сообщениями
        else:
            await bot.send_message(chat_id=chat_id, text=message_text)
            print("✅ Сообщение успешно отправлено!")

        return True

    except TelegramAPIError as e:
        print(f"❌ Ошибка Telegram API: {e}")
        if "Unauthorized" in str(e):
            print("   💡 Проверьте правильность BOT_TOKEN")
        elif "chat not found" in str(e).lower():
            print("   💡 Проверьте правильность CHAT_ID")
            print("   💡 Убедитесь, что отправили боту /start")
        return False
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return False
    finally:
        await bot.session.close()


async def get_chat_id(bot_token: str):
    """
    Вспомогательная функция для получения chat_id.
    Отправьте боту /start, затем запустите эту функцию
    """
    bot = Bot(token=bot_token)

    try:
        # Получаем информацию о боте
        bot_info = await bot.get_me()
        print(f"\n🤖 Информация о боте:")
        print(f"   Имя: {bot_info.first_name}")
        print(f"   Username: @{bot_info.username}")
        print(f"   ID: {bot_info.id}")

        # Получаем обновления
        updates = await bot.get_updates()

        if not updates:
            print("\n❌ Нет обновлений.")
            print("📝 Инструкция:")
            print(f"   1. Найдите бота @{bot_info.username} в Telegram")
            print("   2. Отправьте команду /start")
            print("   3. Запустите этот скрипт снова")
            return

        print("\n📋 Доступные чаты:")
        print("=" * 60)

        seen_chats = set()
        for update in updates:
            if update.message:
                chat = update.message.chat
                if chat.id not in seen_chats:
                    seen_chats.add(chat.id)
                    print(f"\n💬 Chat ID: {chat.id}")
                    print(f"   Тип: {chat.type}")
                    if chat.username:
                        print(f"   Username: @{chat.username}")
                    if chat.first_name:
                        print(f"   Имя: {chat.first_name}")
                    if chat.title:
                        print(f"   Название: {chat.title}")
                    print("-" * 60)

        print(f"\n✅ Найдено чатов: {len(seen_chats)}")
        print("📝 Скопируйте нужный Chat ID и вставьте в CHAT_ID")

    except TelegramAPIError as e:
        print(f"❌ Ошибка: {e}")
        if "Unauthorized" in str(e):
            print("   💡 Проверьте правильность BOT_TOKEN")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
    finally:
        await bot.session.close()


async def main():
    """Основная функция"""

    # Проверка конфигурации
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Ошибка: Не указан BOT_TOKEN!")
        print("\n📝 Инструкция:")
        print("1. Откройте @BotFather в Telegram")
        print("2. Создайте бота командой /newbot")
        print("3. Скопируйте токен")
        print("4. Вставьте токен в переменную BOT_TOKEN в начале скрипта")
        return

    if CHAT_ID == "YOUR_CHAT_ID_HERE":
        print("❌ Ошибка: Не указан CHAT_ID!")
        print("\n📝 Чтобы узнать chat_id, раскомментируйте строку:")
        print("   await get_chat_id(BOT_TOKEN)")
        print("\nИ закомментируйте строку:")
        print("   await send_message_from_file(...)")
        return

    # Отправка сообщения
    await send_message_from_file(BOT_TOKEN, CHAT_ID, TEXT_FILE)


if __name__ == "__main__":
    print("=" * 60)
    print("🤖 TELEGRAM MESSAGE SENDER (aiogram)")
    print("=" * 60)
    print()

    # ============================================
    # РЕЖИМ РАБОТЫ - выберите один вариант:
    # ============================================

    # ВАРИАНТ 1: Получить chat_id (раскомментируйте)
    # asyncio.run(get_chat_id(BOT_TOKEN))

    # ВАРИАНТ 2: Отправить сообщение (по умолчанию)
    asyncio.run(main())