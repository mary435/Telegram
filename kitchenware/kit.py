from config import *
import telebot
#from telebot.types import ReplyKeyboardMarkup #to create buttons
#from telebot.types import ForceReply #to answer the message
from telebot.types import ReplyKeyboardRemove #to remove keypad
import threading
import requests
from PIL import Image
import tensorflow as tf
import numpy as np
from tensorflow.keras.applications.xception import preprocess_input

MODEL = tf.keras.models.load_model('model/')

#bot instance
bot = telebot.TeleBot(BOT_TOKEN)

usuarios = {}

#respond to start command
@bot.message_handler(commands=["start", "help"])
def cmd_start(message):
    "Show available commands"
    markup = ReplyKeyboardRemove()

    intro = "This model classifies images of different kitchen utensils into 6 classes:\n"
    intro+= "*Cups \n*Glasses \n*Plates \n*Spoons \n*Forks \n*Knives"
    
    bot.send_message(message.chat.id, intro, reply_markup=markup)
    bot.send_message(message.chat.id, "Upload an image to classify it.", reply_markup=markup)

#responds when not commands
@bot.message_handler(content_types=["photo"])
def bot_mensajes_texto(message):
    "Manage received picture messages"
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

    clases = ["Cup", "Fork", "Glass", "Knive", "Plate", "Spoon"]
    result = dict(zip(prediction[0], clases))
    pred = result[max(result)]
    response = f'In the photo there is a {pred}'
    markup = ReplyKeyboardRemove()
    #bot.send_message(message.chat.id, "Received", reply_markup=markup)

    bot.send_message(message.chat.id, response, reply_markup=markup)


def receive_messages():
    "Infinite loop checking for new messages"
    bot.infinity_polling() #repeat infinitely
    
### MAIN ###
if __name__ == '__main__':
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "give the welcome"),
        #telebot.types.BotCommand("/", ""),
        ])      #Here we add them so that they appear in the menu

    print('Initializing the bot')
    hilo_bot = threading.Thread(name="hilo_bot", target=receive_messages) #thread that receives messages and continues execution
    hilo_bot.start()
    print("Bot started")