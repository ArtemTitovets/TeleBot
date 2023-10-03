import telebot
from config import keys, TOKEN
from extensions import APIException, MoneyConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту через пробел в следующем формате: <имя валюты, ' \
           'цену которой вы хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> ' \
           '<количество переводимой валюты>.\n\nДля ввода количества переводимой валюты используйте цифры.\n' \
           'Если переводится дробноге количества валюты используйте точку.' \
           '\n\nЧтобы увидеть список всех доступных валют введите команду /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Введено некорректное число параметров.')

        quote, base, amount = values
        total_base = MoneyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        all_total_base = float(total_base) * float(amount)
        text = f'Цена {amount} {quote} в {base} = {all_total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()