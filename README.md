# Telegram Bots for ML models

Artificial Intelligence has made huge strides in recent years, allowing us to train and use machine learning models for various applications. One platform that has been widely used for communication and messaging is Telegram. Here, we will explore how to develop Telegram bots using Python and implement machine learning models in them.

To develop Telegram bots, we will be using the telebot library. This library provides a simple way to interact with the Telegram Bot API, allowing us to build bots with ease.

Once our Telegram bot is functioning as desired, we can deploy it, so it can run in the cloud.

But first we need to get the API token for your bot on Telegram.
For that you must create a bot in BotFather. BotFather is a Telegram bot that helps create and manage bots. Here I show you the steps to create a bot with BotFather:

1. Open Telegram and search for BotFather in the chat search.
2. Click on BotFather and start a chat with it.
3. In the conversation with BotFather, type /newbot and press Enter.
3.Follow BotFather's instructions to choose a name and username for your bot.
4. Once you've created your bot, BotFather will provide you with a unique API token for your bot.

Keep this API token safe, as you won't be able to access it again. It's important not to share the API token with anyone, as it gives full access to your bot.

So as a first step, we are going to copy this API to a new config.py file where we are going to assign it to a new variable like this:

```
BOT_TOKEN =  "paste the api token in quotes"
```
Next we add this config.py file to .gitignore so we don't share it. 

Here's a basic example of code to make a bot that responds to commands: start and help.

```
from config import *
import telebot

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(chat_id=message.chat.id, text='Hola! Este es un bot de Telegram.')

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(chat_id=message.chat.id, text='Estos son los comandos disponibles: \n /start \n /help')

bot.polling()

```

We define two functions start_message and help_message that are activated when a message is received with the /start and /help commands, respectively. Both functions use the send_message method of the bot object to send a message back to the user.

Finally, we call the polling method so that the bot starts listening for messages.

Now we are going to see how to apply this example to Machine learning models: [Kitchenware Classification](/kitchenware) and [Cardiovascular Disease Risk](/cardio_model/).
