# import logging
import gspread
import telebot
import openai
import cherrypy

# ТОКЕНЫ
bot = telebot.TeleBot("token")
openai.api_key = "open ai token"

# ПОДКЛЮЧЕНИЕ К ТАБЛИЦЕ
#ss = gspread.service_account(filename="fitnesschallengebot-d2625bfb6f58.json")
#sh = ss.open('Fitness_bot_GPT')
#wks = sh.worksheet('Лист1')

"""
# НАСТРОЙКА РАЗВЕРТЫВАНИЯ
WEBHOOK_HOST = 'IP-адрес сервера, на котором запущен бот'
WEBHOOK_PORT = 443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % ("6474649041:AAHd4EZSGiJLHPBPMdCmToVc8d-48kifCvo")
"""


"""
# Наш вебхук-сервер
class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                'content-type' in cherrypy.request.headers and \
                cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)
            """


# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG)


# ФУНКЦИОНАЛ БОТА
@bot.message_handler(func=lambda message: True)
def get_response(message):
    #body = [message.chat.id, message.chat.username]
    #wks.append_row(body, table_range="A1:I1")
    if message.text.startswith(">>>"):
        # Use Codex API for code completion
        response = openai.Completion.create(
            engine="code-davinci-002",
            prompt=f'```\n{message.text[3:]}\n```',
            temperature=0,
            max_tokens=4000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n", ">>>"],
        )
    else:
        # Use GPT API for text completion
        # Check if the question is about code or not
        if "code" in message.text.lower() or "python" in message.text.lower():
            # Use Codex API for code-related questions
            response = openai.Completion.create(
                engine="code-davinci-002",
                prompt=f'"""\n{message.text}\n"""',
                temperature=0,
                max_tokens=4000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=['"""'],
            )
        else:
            # Use GPT API for non-code-related questions
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f'"""\n{message.text}\n"""',
                temperature=0,
                max_tokens=2000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=['"""'],
            )

    bot.send_message(message.chat.id, f'{response["choices"][0]["text"]}', parse_mode="None")


bot.infinity_polling()

'''# Снимаем вебхук перед повторной установкой (избавляет от некоторых проблем)
bot.remove_webhook()

# Ставим заново вебхук
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Указываем настройки сервера CherryPy
cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

 # Собственно, запуск!
cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})'''
