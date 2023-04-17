from config import *
import telebot
from telebot.types import ReplyKeyboardMarkup #para crear botones
from telebot.types import ForceReply #para responder el mensaje
from telebot.types import ReplyKeyboardRemove #para eliminar botonera
import xgboost as xgb
import threading
import requests
import pickle

#instancia del bot
bot = telebot.TeleBot(BOT_TOKEN)

usuarios = {}

#responde al comando start
@bot.message_handler(commands=["start", "ok", "help"])
def cmd_start(message):
    "Show available commands"
    markup = ReplyKeyboardRemove()

    intro = "This model makes it possible to predict the probability of suffering from cardiovascular disease, with an accuracy of 80%, trained from a database of more than 68,000 data, with the aim of alerting people about this risk."
    aviso = "Consult with your doctor any medical decision. This is an academic exercise only and the results should not be relied upon for any medical decisions."
    
    bot.send_message(message.chat.id, intro, reply_markup=markup)
    bot.send_message(message.chat.id, aviso, reply_markup=markup)
    bot.send_message(message.chat.id, "Use the /sign command to enter your data.", reply_markup=markup)

#responde al comando alta
@bot.message_handler(commands=["sign"])
def cmd_alta(message):
    "Ask the username."
    markup = ForceReply()
    msg = bot.send_message(message.chat.id, "What's your name?", reply_markup=markup)
    bot.register_next_step_handler(msg, preguntar_edad)

def preguntar_edad(message):
    "Ask the age of the usero"
    usuarios[message.chat.id] = {}
    usuarios[message.chat.id]["name"] = message.text
    markup = ForceReply()
    msg = bot.send_message(message.chat.id, "How old are you?", reply_markup=markup)
    bot.register_next_step_handler(msg, preguntar_sexo)

def preguntar_sexo(message):
    "Asks the user's gender and verifies the age"
    #si la edad introducida no es un numero
    if not message.text.isdigit():
        #informamos el error y volemos a preguntar
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "ERROR: You must enter a number. \nHow old are you?", reply_markup=markup)
        #Volvemos a ejecutar la funcion
        bot.register_next_step_handler(msg, preguntar_sexo)
    else:   #si la edad es un numero
        usuarios[message.chat.id]["age"] = int(message.text)
        #definimos 2 botones para el sexo
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            input_field_placeholder="Press a button",
            resize_keyboard=True
            )
        markup.add("Men", "Woman")
        #Preguntar por el sexo
        msg =  bot.send_message(message.chat.id, "What's your gender?", reply_markup=markup)
        bot.register_next_step_handler(msg, preguntar_altura)

def preguntar_altura(message):
    "Ask the height of the user and verify the gender"
    #si el genero no es valido
    if message.text != "Men" and message.text != "Woman":
        #informamos el error y volemos a preguntar
        msg = bot.send_message(message.chat.id, "ERROR: Invalid gender. \nPress a button")
        #Volvemos a ejecutar la funcion
        bot.register_next_step_handler(msg, preguntar_altura)
    else: #si el genero es valido
        usuarios[message.chat.id]["sex"] = message.text
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "Please enter your height in cm", reply_markup=markup)
        bot.register_next_step_handler(msg, preguntar_peso)

def preguntar_peso(message):
    "Ask the user's weight and check the height"
    #si la altura introducida no es un numero
    if not message.text.isdigit():
        #informamos el error y volemos a preguntar
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "ERROR: You must indicate a number. \nPlease enter your height in cm", reply_markup=markup)
        #Volvemos a ejecutar la funcion
        bot.register_next_step_handler(msg, preguntar_peso)
    else:   #si es un numero
        usuarios[message.chat.id]["height"] = int(message.text)
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "Please enter your weight in kg", reply_markup=markup)
        bot.register_next_step_handler(msg, preguntar_alta)

def preguntar_alta(message):
    "Ask for high blood pressure and check weight"
    #si el peso introducido no es un numero
    if not message.text.isdigit():
        #informamos el error y volemos a preguntar
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "ERROR: You must indicate a number. \nPlease enter your weight in kg", reply_markup=markup)
        #Volvemos a ejecutar la funcion
        bot.register_next_step_handler(msg, preguntar_alta)
    else:   #si es un numero
        usuarios[message.chat.id]["weight"] = int(message.text)
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "Please enter your systolic (high) pressure.", reply_markup=markup)
        bot.register_next_step_handler(msg, preguntar_baja)

def preguntar_baja(message):
    "Ask the low pressure and verify high"
    #si la presion introducido no es un numero
    if not message.text.isdigit():
        #informamos el error y volemos a preguntar
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "ERROR: You must indicate a number. \nPlease enter your systolic (high) pressure.", reply_markup=markup)
        #Volvemos a ejecutar la funcion
        bot.register_next_step_handler(msg, preguntar_baja)
    else:   #si es un numero
        usuarios[message.chat.id]["high"] = int(message.text)
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "Please enter your diastolic (low) pressure.", reply_markup=markup)
        bot.register_next_step_handler(msg, preguntar_colesterol)

def preguntar_colesterol(message):
    "Ask about cholesterol and verify low"
    #si la presion introducido no es un numero
    if not message.text.isdigit():
        #informamos el error y volemos a preguntar
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "ERROR: You must indicate a number. \nPlease enter your diastolic (low) pressure.", reply_markup=markup)
        #Volvemos a ejecutar la funcion
        bot.register_next_step_handler(msg, preguntar_colesterol)
    else:   #si es un numero
        usuarios[message.chat.id]["low"] = int(message.text)
        #definimos 3 botones para el colesterol
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            input_field_placeholder="Press a button",
            resize_keyboard=True
            )
        markup.add("Normal", "Above normal", "Well above normal")
        #1: normal, 2: above normal, 3: Well above normal
        #Preguntar
        msg =  bot.send_message(message.chat.id, "How is your cholesterol?", reply_markup=markup)
        bot.register_next_step_handler(msg, preguntar_glucosa)

def preguntar_glucosa(message):
    "Ask about glucose and check cholesterol"
    #si la opcion no es valido
    if message.text != "Normal" and message.text != "Above normal" and message.text != "Well above normal":
        #informamos el error y volemos a preguntar
        msg = bot.send_message(message.chat.id, "ERROR: Invalid colesterol. \nPress a button")
        #Volvemos a ejecutar la funcion
        bot.register_next_step_handler(msg, preguntar_glucosa)
    else: #si el colesterol es valido
        usuarios[message.chat.id]["colesterol"] = message.text
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            input_field_placeholder="Press a button",
            resize_keyboard=True
            )
        markup.add("Normal", "Above normal", "Well above normal")
        #1: normal, 2: por Above normal, 3: Well above normal
        #Preguntar
        msg =  bot.send_message(message.chat.id, "How is your glucose?", reply_markup=markup)
        bot.register_next_step_handler(msg, preguntar_smoke)

def preguntar_smoke(message):
    "Ask if he smokes and check his glucose"
    #si la opcion no es valido
    if message.text != "Normal" and message.text != "Above normal" and message.text != "Well above normal":
        #informamos el error y volemos a preguntar
        msg = bot.send_message(message.chat.id, "ERROR: Invalid glucose. \nPress a button")
        #Volvemos a ejecutar la funcion
        bot.register_next_step_handler(msg, preguntar_smoke)
    else: #si glucosa es valido
        usuarios[message.chat.id]["glucose"] = message.text
        #definimos 2 botones para fumadores
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            input_field_placeholder="Press a button",
            resize_keyboard=True
            )
        markup.add("Yes", "No")
        #Preguntar si fuma
        msg =  bot.send_message(message.chat.id, "Do you smoke?", reply_markup=markup)
        bot.register_next_step_handler(msg, preguntar_alcohol)

def preguntar_alcohol(message):
    "Ask if drinks alcohol and check if smokes."
    #si la opcion no es valido
    if message.text != "Yes" and message.text != "No":
        #informamos el error y volemos a preguntar
        msg = bot.send_message(message.chat.id, "ERROR: Invalid answer. \nPress a button")
        #Volvemos a ejecutar la funcion
        bot.register_next_step_handler(msg, preguntar_alcohol)
    else: #si fuma es valido
        usuarios[message.chat.id]["smoke"] = message.text
        #definimos 2 botones para alcohol
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            input_field_placeholder="Press a button",
            resize_keyboard=True
            )
        markup.add("Yes", "No")
        #Preguntar si toma alcohol
        msg =  bot.send_message(message.chat.id, "Drink alcohol?", reply_markup=markup)
        bot.register_next_step_handler(msg, preguntar_actividad)

def preguntar_actividad(message):
    "Ask if he is active and check if he drinks alcohol"
    #si la opcion no es valida
    if message.text != "Yes" and message.text != "No":
        #informamos el error y volemos a preguntar
        msg = bot.send_message(message.chat.id, "ERROR: Invalid answer. \nPress a button")
        #Volvemos a ejecutar la funcion
        bot.register_next_step_handler(msg, preguntar_actividad)
    else: #si alcohol es valido
        usuarios[message.chat.id]["alcohol"] = message.text
        #definimos 2 botones para actividad
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            input_field_placeholder="Press a button",
            resize_keyboard=True
            )
        markup.add("Yes", "No")
        #Preguntar si toma hace actividad
        msg =  bot.send_message(message.chat.id, "Do you do physical activity?", reply_markup=markup)
        bot.register_next_step_handler(msg, guardar_datos_usuario)


def guardar_datos_usuario(message):
    "Guarda los datos ingresados por el usuario"
    #si la actividad no es valido
    if message.text != "Yes" and message.text != "No":
        #informamos el error y volemos a preguntar
        msg = bot.send_message(message.chat.id, "ERROR: Invalid answer. \nPress a button")
        #Volvemos a ejecutar la funcion
        bot.register_next_step_handler(msg, guardar_datos_usuario)
    else: #si la respuesta es valida
        usuarios[message.chat.id]["actividad"] = message.text
        texto = 'Datos introducidos: \n'
        texto += f'<code>Name:</code> {usuarios[message.chat.id]["name"]}\n'
        texto += f'<code>Age:</code> {usuarios[message.chat.id]["age"]}\n'
        texto += f'<code>Gender:</code> {usuarios[message.chat.id]["sex"]}\n'
        texto += f'<code>Height:</code> {usuarios[message.chat.id]["height"]}\n'
        texto += f'<code>Weight:</code> {usuarios[message.chat.id]["weight"]}\n'
        texto += f'<code>Systolic (high) pressure:</code> {usuarios[message.chat.id]["high"]}\n'
        texto += f'<code>Diastolic (low) pressure:</code> {usuarios[message.chat.id]["low"]}\n'
        texto += f'<code>Cholesterol:</code> {usuarios[message.chat.id]["colesterol"]}\n'
        texto += f'<code>Glucose:</code> {usuarios[message.chat.id]["glucose"]}\n'
        texto += f'<code>Smoke:</code> {usuarios[message.chat.id]["smoke"]}\n'
        texto += f'<code>Drink alcohol:</code> {usuarios[message.chat.id]["alcohol"]}\n'
        texto += f'<code>Physical activity:</code> {usuarios[message.chat.id]["actividad"]}\n'

        #print(usuarios)

        markup = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, texto, parse_mode="html", reply_markup=markup)
        #definimos 2 botones para confirmar
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            input_field_placeholder="Press a button",
            resize_keyboard=True
            )
        markup.add("Yes", "No")
        #Preguntar si confirma los datos ingresados
        msg =  bot.send_message(message.chat.id, "Confirm the data entered?", reply_markup=markup)
        bot.register_next_step_handler(msg, confirmar_datos_usuario)


def confirmar_datos_usuario(message):
    "Processes the data entered by the user"
    #si la respuesta es valida
    if message.text != "Yes" and message.text != "No":
        #informamos el error y volemos a preguntar
        msg = bot.send_message(message.chat.id, "ERROR: Invalid answer. \nPress a button")
        #Volvemos a ejecutar la funcion
        bot.register_next_step_handler(msg, confirmar_datos_usuario)
    else: #si la respuesta es valido
        if message.text == "No":
            #para borrar los datos
            del usuarios[message.chat.id]
            markup = ReplyKeyboardRemove()
            bot.send_message(message.chat.id, "Deleted information. Use the /sign command to enter your data", reply_markup=markup)
        else:
            msg = bot.send_message(message.chat.id, "Data is processed await.")
            probabilidad = procesar_datos(msg)
            texto= 'The probability of developing cardiovascular disease is: '
            texto+= f'<code>{round(probabilidad[0]*100,3)} % </code>' 
            markup = ReplyKeyboardRemove()
            bot.send_message(message.chat.id, texto, parse_mode="html", reply_markup=markup)
            

def procesar_datos(message):
    "Passes the data to a format that the model accepts and returns the probability"
    
    gender = 2
    if usuarios[message.chat.id]["sex"] == "Woman":
       gender = 1

    cholesterol = 3
    if usuarios[message.chat.id]["colesterol"] == "Normal":
        cholesterol = 1
    elif usuarios[message.chat.id]["colesterol"] == "Above normal":
        cholesterol = 2
   
    glucosa = 3
    if usuarios[message.chat.id]["glucose"] == "Normal":
        glucosa = 1
    elif usuarios[message.chat.id]["glucose"] == "Above normal":
        glucosa = 2
    smoke = 0
    if usuarios[message.chat.id]["smoke"] == "Si":
        smoke = 1    
    alcohol = 0
    if usuarios[message.chat.id]["alcohol"] == "Si":
        alcohol = 1
    physical_activity = 0
    if usuarios[message.chat.id]["actividad"] == "Si":
        physical_activity = 1

    patient = {
    'age': usuarios[message.chat.id]["age"],
    'gender': gender,
    'height': usuarios[message.chat.id]["height"],
    'weight': usuarios[message.chat.id]["weight"],
    'ap_high': usuarios[message.chat.id]["high"],
    'ap_low': usuarios[message.chat.id]["low"],
    'cholesterol': cholesterol,
    'glucose': glucosa,
    'smoke': smoke,
    'alcohol': alcohol,
    'physical_activity': physical_activity
    }

    ## Load the model
    input_file = 'model_xgb_new.bin'

    with open(input_file, 'rb') as f_in: 
        dv, model = pickle.load(f_in)

    X = dv.transform([patient])
    d_test = xgb.DMatrix(X, feature_names = dv.get_feature_names_out())
    y_pred = model.predict(d_test)

    return y_pred
    #print(usuario)
    #msg = bot.send_message(message.chat.id, y_pred)
    #bot.register_next_step_handler(msg, consultar_modelo)


def recibir_mensajes():
    "Bucle infinito que comprueba si hay nuevos mensajes"
    bot.infinity_polling() #repite infinitamente


### MAIN ###
if __name__ == '__main__':
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "give the welcome"),
        telebot.types.BotCommand("/sign", "enter your data"),
        ])      #Aca los agregamos para que aparezcan en el menu

    print('Initializing the bot')
    hilo_bot = threading.Thread(name="hilo_bot", target=recibir_mensajes) #hilo que recibe mensajes y continua la ejecucion
    hilo_bot.start()
    print("Bot started")
