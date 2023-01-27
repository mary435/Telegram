from config import *
import telebot
from telebot.types import ReplyKeyboardMarkup #para crear botones
from telebot.types import ForceReply #para responder el mensaje
from telebot.types import ReplyKeyboardRemove #para eliminar botonera
import threading
import requests
from PIL import Image
import tensorflow as tf
import numpy as np
from tensorflow.keras.applications.xception import preprocess_input

MODEL = tf.keras.models.load_model('model/')

#instancia del bot
bot = telebot.TeleBot(BOT_TOKEN)

usuarios = {}

#responde al comando start
@bot.message_handler(commands=["start", "ayuda", "help"])
def cmd_start(message):
    "Muestra los comandos disponibles"
    markup = ReplyKeyboardRemove()

    intro = "Este modelo clasifica imágenes de diferentes utensilios de cocina en 6 clases:\n"
    intro+= "*Tazas \n*Vasos \n*Platos \n*Cucharas \n*Tenedores \n*Cuchillos"
    
    bot.send_message(message.chat.id, intro, reply_markup=markup)
    bot.send_message(message.chat.id, "Envia una imagen para clasificar", reply_markup=markup)

#responde a texto que no son comandos 
@bot.message_handler(content_types=["photo"])
def bot_mensajes_texto(message):
    "Gestiona los mensajes de fotos recibidos"
    file_id = message.photo[-1].file_id
    # get URL by id
    file_path = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}').json()['result']['file_path']
    # open URL with Pillow
    img = Image.open(requests.get(f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}', stream=True).raw)
    # save on the disk if needed
    #img.save('photo.jpg')

    img = img.convert("RGB")
    img = img.resize((299,299))
    arr = np.array(img)
    arr = np.expand_dims(arr, axis=0)
    arr = preprocess_input(arr)
    prediction = MODEL.predict([arr])

    clases = ["Taza", "Tenedor", "Vaso", "Cuchillo", "Plato", "Cuchara"]
    result = dict(zip(prediction[0], clases))
    pred = result[max(result)]

    markup = ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Recibido", reply_markup=markup)

    bot.send_message(message.chat.id, pred, reply_markup=markup)


#### Main
def recibir_mensajes():
    "Bucle infinito que comprueba si hay nuevos mensajes"
    bot.infinity_polling() #repite infinitamente
    
### MAIN ###
if __name__ == '__main__':
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "da la bienvenida"),
        #telebot.types.BotCommand("/alta", "ingrese sus datos"),
        ])      #Aca los agregamos para que aparezcan en el menu

    print('Inicialdo el bot')
    hilo_bot = threading.Thread(name="hilo_bot", target=recibir_mensajes) #hilo que recibe mensajes y continua la ejecucion
    hilo_bot.start()
    print("Bot iniciado")