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
@bot.message_handler(commands=["start", "ayuda", "help"])
def cmd_start(message):
    "Muestra los comandos disponibles"
    markup = ReplyKeyboardRemove()

    intro = "Este modelo permite predecir la probabilidad de padecer una enfermedad cardiovascular, con una precisión del 80%, entrenados a partir de una base de datos de más de 68.000 datos, con el objetivo de alertar a las personas sobre este riesgo."
    aviso = "Consulte con su médico cualquier decisión médica. Este es solo un ejercicio académico y no se debe confiar en los resultados para ninguna decisión médica."
    
    bot.send_message(message.chat.id, intro, reply_markup=markup)
    bot.send_message(message.chat.id, aviso, reply_markup=markup)
    bot.send_message(message.chat.id, "Usa el comando /alta para ingresar tus datos.", reply_markup=markup)

#responde al comando alta
@bot.message_handler(commands=["alta"])
def cmd_alta(message):
    "Pregunta el nombre de usuario"
    markup = ForceReply()
    msg = bot.send_message(message.chat.id, "¿Como te llamas?", reply_markup=markup)
    bot.register_next_step_handler(msg, preguntar_edad)

def preguntar_edad(message):
    "Pregunta la edad del usuario"
    usuarios[message.chat.id] = {}
    usuarios[message.chat.id]["nombre"] = message.text
    markup = ForceReply()
    msg = bot.send_message(message.chat.id, "¿Cuantos años tienes?", reply_markup=markup)
    bot.register_next_step_handler(msg, preguntar_sexo)

def preguntar_sexo(message):
    "Pregunta el sexo del usuario y verifica la edad"
    #si la edad introducida no es un numero
    if not message.text.isdigit():
        #informamos el error y volemos a preguntar
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "ERROR: Debes indicar un numero. \n¿Cuantos años tienes?", reply_markup=markup)
        #Volvemos a ejecutar la funcion
        bot.register_next_step_handler(msg, preguntar_sexo)
    else:   #si la edad es un numero
        usuarios[message.chat.id]["edad"] = int(message.text)
        #definimos 2 botones para el sexo
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            input_field_placeholder="Pulsa un boton",
            resize_keyboard=True
            )
        markup.add("Hombre", "Mujer")
        #Preguntar por el sexo
        msg =  bot.send_message(message.chat.id, "¿Cual es tu genero?", reply_markup=markup)
        bot.register_next_step_handler(msg, preguntar_altura)

def preguntar_altura(message):
    "Pregunta la altura del usuario y verifica el genero"
    #si el genero no es valido
    if message.text != "Hombre" and message.text != "Mujer":
        #informamos el error y volemos a preguntar
        msg = bot.send_message(message.chat.id, "ERROR: Genero no valido. \nPulsa un botón")
        #Volvemos a ejecutar la funcion
        bot.register_next_step_handler(msg, preguntar_altura)
    else: #si el genero es valido
        usuarios[message.chat.id]["sexo"] = message.text
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "Por favor ingresa tu altura en cm", reply_markup=markup)
        bot.register_next_step_handler(msg, preguntar_peso)

def preguntar_peso(message):
    "Pregunta el peso del usuario y verifica la altura"
    #si la altura introducida no es un numero
    if not message.text.isdigit():
        #informamos el error y volemos a preguntar
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "ERROR: Debes indicar un numero. \nPor favor ingresa tu altura en cm", reply_markup=markup)
        #Volvemos a ejecutar la funcion
        bot.register_next_step_handler(msg, preguntar_peso)
    else:   #si es un numero
        usuarios[message.chat.id]["altura"] = int(message.text)
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "Por favor ingresa tu peso en kg", reply_markup=markup)
        bot.register_next_step_handler(msg, preguntar_alta)

def preguntar_alta(message):
    "Pregunta la presion alta y verifica peso"
    #si el peso introducido no es un numero
    if not message.text.isdigit():
        #informamos el error y volemos a preguntar
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "ERROR: Debes indicar un numero. \nPor favor ingresa tu peso en kg", reply_markup=markup)
        #Volvemos a ejecutar la funcion
        bot.register_next_step_handler(msg, preguntar_alta)
    else:   #si es un numero
        usuarios[message.chat.id]["peso"] = int(message.text)
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "Por favor ingresa tu presión sistolica (alta)", reply_markup=markup)
        bot.register_next_step_handler(msg, preguntar_baja)

def preguntar_baja(message):
    "Pregunta la presion baja y verifica alta"
    #si la presion introducido no es un numero
    if not message.text.isdigit():
        #informamos el error y volemos a preguntar
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "ERROR: Debes indicar un numero. \nPor favor ingresa tu presión sistolica (alta)", reply_markup=markup)
        #Volvemos a ejecutar la funcion
        bot.register_next_step_handler(msg, preguntar_baja)
    else:   #si es un numero
        usuarios[message.chat.id]["alta"] = int(message.text)
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "Por favor ingresa tu presión diastolica (baja)", reply_markup=markup)
        bot.register_next_step_handler(msg, preguntar_colesterol)

def preguntar_colesterol(message):
    "Pregunta por el colesterol y verifica baja"
    #si la presion introducido no es un numero
    if not message.text.isdigit():
        #informamos el error y volemos a preguntar
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "ERROR: Debes indicar un numero. \nPor favor ingresa tu presión diastolica (baja)", reply_markup=markup)
        #Volvemos a ejecutar la funcion
        bot.register_next_step_handler(msg, preguntar_colesterol)
    else:   #si es un numero
        usuarios[message.chat.id]["baja"] = int(message.text)
        #definimos 3 botones para el colesterol
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            input_field_placeholder="Pulsa un boton",
            resize_keyboard=True
            )
        markup.add("Normal", "Encima de lo normal", "Muy por encima de lo normal")
        #1: normal, 2: por encima de lo normal, 3: muy por encima de lo normal
        #Preguntar
        msg =  bot.send_message(message.chat.id, "¿Como esta su colesterol?", reply_markup=markup)
        bot.register_next_step_handler(msg, preguntar_glucosa)

def preguntar_glucosa(message):
    "Pregunta por la glucosa y verifica colesterol"
    #si la opcion no es valido
    if message.text != "Normal" and message.text != "Encima de lo normal" and message.text != "Muy por encima de lo normal":
        #informamos el error y volemos a preguntar
        msg = bot.send_message(message.chat.id, "ERROR: Colesterol no valido. \nPulsa un botón")
        #Volvemos a ejecutar la funcion
        bot.register_next_step_handler(msg, preguntar_glucosa)
    else: #si el colesterol es valido
        usuarios[message.chat.id]["colesterol"] = message.text
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            input_field_placeholder="Pulsa un boton",
            resize_keyboard=True
            )
        markup.add("Normal", "Encima de lo normal", "Muy por encima de lo normal")
        #1: normal, 2: por encima de lo normal, 3: muy por encima de lo normal
        #Preguntar
        msg =  bot.send_message(message.chat.id, "¿Como esta su glucosa?", reply_markup=markup)
        bot.register_next_step_handler(msg, preguntar_smoke)

def preguntar_smoke(message):
    "Pregunta si fuma y verifica la glucosa"
    #si la opcion no es valido
    if message.text != "Normal" and message.text != "Encima de lo normal" and message.text != "Muy por encima de lo normal":
        #informamos el error y volemos a preguntar
        msg = bot.send_message(message.chat.id, "ERROR: Glucosa no valido. \nPulsa un botón")
        #Volvemos a ejecutar la funcion
        bot.register_next_step_handler(msg, preguntar_smoke)
    else: #si glucosa es valido
        usuarios[message.chat.id]["glucosa"] = message.text
        #definimos 2 botones para fumadores
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            input_field_placeholder="Pulsa un boton",
            resize_keyboard=True
            )
        markup.add("Si", "No")
        #Preguntar si fuma
        msg =  bot.send_message(message.chat.id, "¿Fuma?", reply_markup=markup)
        bot.register_next_step_handler(msg, preguntar_alcohol)

def preguntar_alcohol(message):
    "Pregunta si toma alcohol y verifica si fuma"
    #si la opcion no es valido
    if message.text != "Si" and message.text != "No":
        #informamos el error y volemos a preguntar
        msg = bot.send_message(message.chat.id, "ERROR: Respuesta no valido. \nPulsa un botón")
        #Volvemos a ejecutar la funcion
        bot.register_next_step_handler(msg, preguntar_alcohol)
    else: #si fuma es valido
        usuarios[message.chat.id]["fuma"] = message.text
        #definimos 2 botones para alcohol
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            input_field_placeholder="Pulsa un boton",
            resize_keyboard=True
            )
        markup.add("Si", "No")
        #Preguntar si toma alcohol
        msg =  bot.send_message(message.chat.id, "Toma alcohol?", reply_markup=markup)
        bot.register_next_step_handler(msg, preguntar_actividad)

def preguntar_actividad(message):
    "Pregunta si hace actividad y verifica si toma alcohol"
    #si la opcion no es valida
    if message.text != "Si" and message.text != "No":
        #informamos el error y volemos a preguntar
        msg = bot.send_message(message.chat.id, "ERROR: Respuesta no valida. \nPulsa un botón")
        #Volvemos a ejecutar la funcion
        bot.register_next_step_handler(msg, preguntar_actividad)
    else: #si alcohol es valido
        usuarios[message.chat.id]["alcohol"] = message.text
        #definimos 2 botones para actividad
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            input_field_placeholder="Pulsa un boton",
            resize_keyboard=True
            )
        markup.add("Si", "No")
        #Preguntar si toma hace actividad
        msg =  bot.send_message(message.chat.id, "Hace actividad fisica?", reply_markup=markup)
        bot.register_next_step_handler(msg, guardar_datos_usuario)


def guardar_datos_usuario(message):
    "Guarda los datos ingresados por el usuario"
    #si la actividad no es valido
    if message.text != "Si" and message.text != "No":
        #informamos el error y volemos a preguntar
        msg = bot.send_message(message.chat.id, "ERROR: Respuesta no valido. \nPulsa un botón")
        #Volvemos a ejecutar la funcion
        bot.register_next_step_handler(msg, guardar_datos_usuario)
    else: #si la respuesta es valida
        usuarios[message.chat.id]["actividad"] = message.text
        texto = 'Datos introducidos: \n'
        texto += f'<code>Nombre:</code> {usuarios[message.chat.id]["nombre"]}\n'
        texto += f'<code>Edad:</code> {usuarios[message.chat.id]["edad"]}\n'
        texto += f'<code>Genero:</code> {usuarios[message.chat.id]["sexo"]}\n'
        texto += f'<code>Altura:</code> {usuarios[message.chat.id]["altura"]}\n'
        texto += f'<code>Peso:</code> {usuarios[message.chat.id]["peso"]}\n'
        texto += f'<code>Presión sistolica (alta):</code> {usuarios[message.chat.id]["alta"]}\n'
        texto += f'<code>Presión diastolica (baja):</code> {usuarios[message.chat.id]["baja"]}\n'
        texto += f'<code>Colesterol:</code> {usuarios[message.chat.id]["colesterol"]}\n'
        texto += f'<code>Glucosa:</code> {usuarios[message.chat.id]["glucosa"]}\n'
        texto += f'<code>Fuma:</code> {usuarios[message.chat.id]["fuma"]}\n'
        texto += f'<code>Toma alcohol:</code> {usuarios[message.chat.id]["alcohol"]}\n'
        texto += f'<code>Realiza actividad fisica:</code> {usuarios[message.chat.id]["actividad"]}\n'

        #print(usuarios)

        markup = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, texto, parse_mode="html", reply_markup=markup)
        #definimos 2 botones para confirmar
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            input_field_placeholder="Pulsa un boton",
            resize_keyboard=True
            )
        markup.add("Si", "No")
        #Preguntar si confirma los datos ingresados
        msg =  bot.send_message(message.chat.id, "Confirma los datos ingresados?", reply_markup=markup)
        bot.register_next_step_handler(msg, confirmar_datos_usuario)


def confirmar_datos_usuario(message):
    "Procesa los datos ingresados por el usuario"
    #si la respuesta es valida
    if message.text != "Si" and message.text != "No":
        #informamos el error y volemos a preguntar
        msg = bot.send_message(message.chat.id, "ERROR: Respuesta no valido. \nPulsa un botón")
        #Volvemos a ejecutar la funcion
        bot.register_next_step_handler(msg, confirmar_datos_usuario)
    else: #si la respuesta es valido
        if message.text == "No":
            #para borrar los datos
            del usuarios[message.chat.id]
            markup = ReplyKeyboardRemove()
            bot.send_message(message.chat.id, "Informacion borrada. Usa el comando /alta para ingresar tus datos", reply_markup=markup)
        else:
            msg = bot.send_message(message.chat.id, "Se procesan los datos aguarde.")
            probabilidad = procesar_datos(msg)
            texto= 'La probabilidad de desarrollar una enfermedad cardiovascular es: '
            texto+= f'<code>{round(probabilidad[0]*100,3)} % </code>' 
            markup = ReplyKeyboardRemove()
            bot.send_message(message.chat.id, texto, parse_mode="html", reply_markup=markup)
            

def procesar_datos(message):
    "Pasa los datos a formato que acepta el modelo y devulve la probabilidad"
    
    gender = 2
    if usuarios[message.chat.id]["sexo"] == "Mujer":
       gender = 1

    cholesterol = 3
    if usuarios[message.chat.id]["colesterol"] == "Normal":
        cholesterol = 1
    elif usuarios[message.chat.id]["colesterol"] == "Encima de lo normal":
        cholesterol = 2
   
    glucosa = 3
    if usuarios[message.chat.id]["glucosa"] == "Normal":
        glucosa = 1
    elif usuarios[message.chat.id]["glucosa"] == "Encima de lo normal":
        glucosa = 2
    smoke = 0
    if usuarios[message.chat.id]["fuma"] == "Si":
        smoke = 1    
    alcohol = 0
    if usuarios[message.chat.id]["alcohol"] == "Si":
        alcohol = 1
    physical_activity = 0
    if usuarios[message.chat.id]["actividad"] == "Si":
        physical_activity = 1

    patient = {
    'age': usuarios[message.chat.id]["edad"],
    'gender': gender,
    'height': usuarios[message.chat.id]["altura"],
    'weight': usuarios[message.chat.id]["peso"],
    'ap_high': usuarios[message.chat.id]["alta"],
    'ap_low': usuarios[message.chat.id]["baja"],
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
        telebot.types.BotCommand("/start", "da la bienvenida"),
        telebot.types.BotCommand("/alta", "ingrese sus datos"),
        ])      #Aca los agregamos para que aparezcan en el menu

    print('Inicialdo el bot')
    hilo_bot = threading.Thread(name="hilo_bot", target=recibir_mensajes) #hilo que recibe mensajes y continua la ejecucion
    hilo_bot.start()
    print("Bot iniciado")
