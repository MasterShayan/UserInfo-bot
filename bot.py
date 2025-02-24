import telebot
import random
from datetime import datetime
import pytz


timezone = pytz.timezone('Asia/Tehran')


API_KEY = "YOUR_BOT_TOKEN"  # Token
bot = telebot.TeleBot(API_KEY)


def get_menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        telebot.types.KeyboardButton(
            "🌟 Premium",
            request_users=telebot.types.KeyboardButtonRequestUsers(
                request_id=random.randint(1, 99),
                user_is_premium=True,
                request_photo=True,
                request_name=True,
                request_username=True
            )
        ),
        telebot.types.KeyboardButton(
            "👤 User",
            request_users=telebot.types.KeyboardButtonRequestUsers(
                request_id=random.randint(1, 99),
                request_photo=True,
                user_is_bot=False,
                request_name=True,
                request_username=True
            )
        ),
        telebot.types.KeyboardButton(
            "🤖 Bot",
            request_users=telebot.types.KeyboardButtonRequestUsers(
                request_id=random.randint(1, 99),
                user_is_bot=True,
                request_photo=True,
                request_name=True,
                request_username=True
            )
        ),
        telebot.types.KeyboardButton(
            "👥 Group",
            request_chat=telebot.types.KeyboardButtonRequestChat(
                request_id=random.randint(1, 99),
                chat_is_channel=False,
                chat_has_username=False,
                request_photo=True,
                request_title=True
            )
        ),
        telebot.types.KeyboardButton(
            "👥 Super Group",
            request_chat=telebot.types.KeyboardButtonRequestChat(
                request_id=random.randint(1, 99),
                chat_is_channel=False,
                chat_has_username=True,
                request_photo=True,
                request_title=True,
                request_username=True
            )
        ),
        telebot.types.KeyboardButton(
            "🔊 Private Channel",
            request_chat=telebot.types.KeyboardButtonRequestChat(
                request_id=random.randint(1, 99),
                chat_is_channel=True,
                chat_has_username=False,
                request_photo=True,
                request_title=True
            )
        ),
        telebot.types.KeyboardButton(
            "🔊 Channel",
            request_chat=telebot.types.KeyboardButtonRequestChat(
                request_id=random.randint(1, 99),
                chat_is_channel=True,
                chat_has_username=True,
                request_photo=True,
                request_title=True,
                request_username=True
            )
        )
    )
    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    message_id = message.message_id
    try:
        bot.send_message(
            chat_id=chat_id,
            text="Hi, welcome to the Username Info Bot!\nChoose from the menu below!",
            reply_to_message_id=message_id,
            reply_markup=get_menu()
        )
    except Exception as e:
        print(f"Error in send_welcome: {e}")


@bot.message_handler(content_types=['users_shared'])
def handle_users_shared(message):
    chat_id = message.chat.id
    message_id = message.message_id
    
    try:
        if hasattr(message, 'users_shared') and message.users_shared.users:
            shared_user = message.users_shared.users[0]
            shared_user_id = shared_user.user_id
            shared_first_name = str(shared_user.first_name or '').replace('<', '').replace('>', '').replace('/', '')
            shared_username = f"@{shared_user.username}" if shared_user.username else "No"
            
            response = (
                f"🆔 ID: <code>{shared_user_id}</code>\n"
                f"👤 Name: <b>{shared_first_name}</b>\n"
                f"🔗 Username: {shared_username}"
            )
            bot.send_message(
                chat_id=chat_id,
                text=response,
                reply_to_message_id=message_id,
                parse_mode='HTML'
            )
    except Exception as e:
        print(f"Error in handle_users_shared: {e}")
        bot.send_message(chat_id=chat_id, text="Something went wrong, please try again.")


@bot.message_handler(content_types=['chat_shared'])
def handle_chat_shared(message):
    chat_id = message.chat.id
    message_id = message.message_id
    
    try:
        if hasattr(message, 'chat_shared') and message.chat_shared:
            shared_chat_id = message.chat_shared.chat_id
            shared_title = str(message.chat_shared.title or '').replace('<', '').replace('>', '').replace('/', '')
            shared_username = f"@{message.chat_shared.username}" if message.chat_shared.username else "No"
            
            response = (
                f"🆔 ID: <code>{shared_chat_id}</code>\n"
                f"👥 Title: <b>{shared_title}</b>\n"
                f"🔗 Username: {shared_username}"
            )
            bot.send_message(
                chat_id=chat_id,
                text=response,
                reply_to_message_id=message_id,
                parse_mode='HTML'
            )
    except Exception as e:
        print(f"Error in handle_chat_shared: {e}")
        bot.send_message(chat_id=chat_id, text="Something went wrong, please try again.")


@bot.message_handler(func=lambda message: True)
def handle_all(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text="Please use the menu or press /start")


if __name__ == "__main__":
    try:
        print("Bot is starting...")
        bot.polling(non_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"Polling error: {e}")
