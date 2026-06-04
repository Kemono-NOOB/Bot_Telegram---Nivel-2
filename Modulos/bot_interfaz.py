import re
import telebot
from telebot.types import Message
import logging
from dotenv import load_dotenv
import os
from Modulos.motor_datos import rd_CI, rd_csv
from motor_documentos import session_data, rch_final, log




class TelegramBot:
    
    def __init__(self):

        self.TELEGRAM_BOT_KEY=os.getenv('TELEGRAM_BOT_KEY', 'NO BOT KEY')
        self.ADMIN_PASSWORD=os.getenv('ADMIN_PASSWORD', 'NO PASSWORD')
        self.bot = telebot.TeleBot(self.TELEGRAM_BOT_KEY)

        

        #!MENSAJES DISPONIBLES

        self.bot.register_message_handler(self.mh_inicio, commands=['Inicio'])

        
        self.bot.register_message_handler(self.mh_obtenerinfo, commands=['Registrarse'])

        
        self.bot.register_message_handler(self.mh_ver_notas, commands=['Ver_notas'])

        
        self.bot.register_message_handler(self.mh_general, func = lambda message: True)


    def inicio(self):
        self.bot.infinity_polling(logger_level=logging.CRITICAL,
        timeout=60,
        long_polling_timeout=60)

    def mh_inicio(self,message:Message):

        session_data(message.from_user.username ,'Inició el Bot')
        self.bot.send_message(message.from_user.id,
        'Clave de acceso')

        self.bot.register_next_step_handler(message, self.control_acceso)

    def mh_obtenerinfo(self, message: Message):
        info: str = ''
        info += f'ID: {message.from_user.id}\n'
        info += f'Username: {message.from_user.username}\n'
        info += f'Name: {message.from_user.first_name}\n'

        self.bot.send_message(message.from_user.id, info)


	

    def ver_notas(self, message: Message):

        cedula=self.procesar_ingreso(message)

        if cedula:
            self.bot.send_message(message.chat.id, 'Validado')
            archivo, msg = rch_final(cedula)
            if archivo:
                self.bot.send_message(message.chat.id, msg)
                try:
                    self.bot.send_document(message.chat.id, open(archivo, 'rb'))
                    os.remove(archivo)
                    session_data(message.from_user.username ,'Notas entregadas')
                except Exception as e:
                    err_msg='ERROR AL ENVIAR NOTAS'
                    print(log(err_msg, 'ver_notas', 'telegram_bot.py', e))
                    self.bot.send_message(message.chat.id, err_msg)
            else:
                self.bot.send_message(message.chat.id, msg)
        else:
            self.bot.send_message(message.chat.id, 'Cédula inválida, intente nuevamente.')
            self.bot.register_next_step_handler(message, self.ver_notas)	



    def mh_general(self, message: Message):
        self.bot.send_message(message.from_user.id,'Comando inválido')

    def control_acceso(self, message: Message):
        clave_input = message.text
        permitido = False

        if clave_input == self.ADMIN_PASSWORD:
            mensaje = 'Bienvenido'
            permitido = True
            session_data(message.from_user.username ,'Inició sesión')
        else:
            mensaje = 'Incorrecto'
            session_data(message.from_user.username,'INGRESO DE CONTRASENA INCORRECTA')

        self.bot.send_message(message.chat.id, mensaje)

        if not permitido:
            self.bot.register_next_step_handler(message,
            self.control_acceso)

    def mh_ver_notas(self, message: Message):

        self.bot.send_message(message.chat.id, 'Cédula')

        self.bot.register_next_step_handler(message, self.ver_notas)
        
    @staticmethod

    def procesar_ingreso(self, message:Message):
        
        ingreso : str = message.text
        if ingreso:
            ingreso=ingreso.strip()
            ingreso=re.sub(r'\D','',ingreso)
            if ingreso:
                return ingreso
        
        return None	