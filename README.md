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


