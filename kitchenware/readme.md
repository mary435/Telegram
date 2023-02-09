# Telegram Bot for Kitchenware Classification Model

This project starts with the model that was trained for the competition organized in Kaggle by [DataTalks.Club](https://www.kaggle.com/competitions/kitchenware-classification/overview).

You can see the development of my solution [here](https://github.com/mary435/kitchenware_classification.git). 

And this is the invitation link to the telegram app to test the model: [Telegram Kitchenware Classification](https://t.me/MaryPython_bot)

But if you want to develop your own bot, I'll explain the steps I followed in mine.

First consider that we already have a config.py file with the API Token of your telegram bot. If not, you can follow the steps [here](../README.md).

Now we install the necessary libraries in the environment that you prefer conda or pipenv, from request.txt.

```
pip install -r request.txt
```

Next step, save your model.h5 in a lighter format, for that you can use my save.py file replacing the name of your model. On this line: 
```
model = tf.keras.models.load_model('xception_v4_larger.h5')
```
This will create a /model folder that will contain your model.

Next we create our main.py and add these imports:
```
from config import * #for API Token
import telebot
from telebot.types import ReplyKeyboardRemove #to remove keypad
import threading
import requests
from PIL import Image
import tensorflow as tf
import numpy as np
from tensorflow.keras.applications.xception import preprocess_input
```

To follow we load the model and create an instance of the bot:
```
#Load model
MODEL = tf.keras.models.load_model('model/')

#bot instance
bot = telebot.TeleBot(BOT_TOKEN)
```

And in our main function we are going to use that instance of the bot and set the commands, like this: ```telebot.types.BotCommand("/command", "Text")```

We also create a thread with the threading library to control the threads. Additionally this thread object calls the receive_messages function which makes the bot wait infinitely for messages.
```threading.Thread(name="hilo_bot", target=receive_messages)```

Add to the function some print to see on the server if the bot is running. And here is the code block to clarify:

``` 
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

```

Move on we need functions with decorators @bot to handle the messages.

So for example we create this function to handle the responses to the start and help commands.

Here we define in a variable the text to send to the user in response to the start command and send a message using the instance of the bot.

Always use to reply the chat id with 'message.chat.id' to make sure we reply in the same chat.

Also with ```markup = ReplyKeyboardRemove()``` indicate that the keyboard is deleted, to make sure that no previous configurations remain.

```
@bot.message_handler(commands=["start", "help"])
def cmd_start(message):
    "Show available commands"
    markup = ReplyKeyboardRemove() #to remove keypad

    intro = "This model classifies images of different kitchen utensils into 6 classes:\n"
    intro+= "*Cups \n*Glasses \n*Plates \n*Spoons \n*Forks \n*Knives"
    
    bot.send_message(message.chat.id, intro, reply_markup=markup)
    bot.send_message(message.chat.id, "Upload an image to classify it.", reply_markup=markup
```

To finish the most important function that receives the image and responds with the prediction. Here we use the decorator too, but this time we receibe a "photo".

Photos received in telegram are temporarily saved with an id. We can access that id like so: ```file_id = message.photo[-1].file_id``` and get the path to the url where it is stored like this: ```file_path = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}').json()['result']['file_path']```

That allows us to read it using pillow like this: ```img = Image.open(requests.get(f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}', stream=True).raw)```

Now all that remains is to convert the image into an array, obtain the prediction and respond. Here is the full function code for clarification:

```
@bot.message_handler(content_types=["photo"])
def bot_mensajes_texto(message):
    "Manage received picture messages"
    file_id = message.photo[-1].file_id

    # get URL by id
    file_path = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}').json()['result']['file_path']

    # open URL with Pillow
    img = Image.open(requests.get(f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}', stream=True).raw)

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

    bot.send_message(message.chat.id, response, reply_markup=markup)
```

If you got here, now all that remains is to run your file with ```python main.py``` and use your telegram to test it!

