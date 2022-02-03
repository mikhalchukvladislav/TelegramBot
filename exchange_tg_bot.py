import telebot
from telebot import types
from bot_info import keys, TOKEN
from extensions import APIException, GetPrice
import time


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('📋 Список валют')
    item2 = types.KeyboardButton('🔍 Пример запроса')
 
    markup.add(item1, item2)
 
    text_for_start = '\
Привет! Я - {0.first_name}, перевожу валюты между собой.\n\
Нажмите на кнопку "🔍 Пример запроса", чтобы увидеть пример запроса,\
 или для начала работы сразу введите команду боту в следующем формате:\n\
<имя валюты> <в какую валюту перевести>\
 <количество переводимой валюты>\n\
Нажав кнопку "📋 Список валют", Вы ознакомитесь с доступными валютами.'.format(bot.get_me())
    
    bot.reply_to(message, text_for_start, reply_markup=markup)

@bot.message_handler(content_types=['text'])
def exchange(message: telebot.types.Message):

    if message.text == '📋 Список валют':
        text = 'Доступные валюты:'
        for key in keys.keys():
            text = '\n'.join((text, key))
        bot.reply_to(message, text)
    
    elif message.text == '🔍 Пример запроса':
        bot.reply_to(message, 'рубль евро 20.45')

    elif message.text != '🔍 Пример запроса' and message.text != '📋 Список валют':

        try:
            values = message.text.split(' ')

            if len(values) != 3:
                raise APIException('Неверный ввод параметров.')

            quote, base, amount = values
            total_base = GetPrice.exch(quote, base, amount)
        
        except APIException as e:
            bot.reply_to(message, f'Ошибка пользователя.\n{e}')
        
        except Exception as e:
            bot.reply_to(message, f'Не удалось обработать команду\n{e}')
        
        else:
            sti = open('C:/Users/Oblre/Desktop/Личное/PYTHON/SkillFactory/tg_bot/AnimatedSticker.tgs', 'rb')
            text = f'Цена {amount} {keys[quote]} в {keys[base]} : {total_base}'
            bot.send_sticker(message.chat.id, sti)
            bot.send_message(message.chat.id, text)

while True:
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        print(e)  # или import traceback; traceback.print_exc() для печати полной инфы
        time.sleep(15)