#pip install wget
#pip install python-vlc
import telepot
import picamera
import RPi.GPIO as GPIO
import time
from time import sleep
import datetime
from telepot.loop import MessageLoop
import wget
import vlc
#declaracion del pin para el timbre
timbre_pin=18
#Declaraciones de los pines
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(timbre_pin,GPIO.IN)
print(GPIO.input(timbre_pin))

def portero_smart(msg):
    global chat_id
    global telegramText
    global telegramMessage
    #variables de mensaje enviado por telegram
    contenido,chat_type,chat_id=telepot.glance(msg)
    telegramText=msg[contenido]
    print('id: '+str(chat_id))
    print('Tipo de contenido:',contenido)
    print('Contenido del mensaje:',telegramText)
    if contenido=='text':
        print('Longitud del mensaje',len(telegramText))
        if len(telegramText)==1:
            captura()
            print('Foto Capturada de la Puerta')
    if contenido=='sticker':
        print('Han enviado un stiker')
        captura()
        print('Foto Capturada de la Puerta')
    if contenido=='voice':
        bot.sendMessage(chat_id,'Mensaje de voz enviado')
        print('Nota de Voz')
        file_id=telegramText['file_id']
        ruta_voice=bot.getFile(file_id)['file_path']
        file=ruta_voice[6:]
        print('archivo', ruta_voice[6:])
        url='https://api.telegram.org/file/bot1644864415:AAHloVoz6D-n_iWZWtIE9mI6bVIqggZt6Zk/{path}'.format(path=ruta_voice)
        wget.download(url,'/home/pi/Desktop')
        time.sleep(0.5)
        instance=vlc.Instance()
        player=instance.media_player_new()
        media=instance.media_new(file)
        player.set_media(media)
        player.play()  
            
bot=telepot.Bot('1644864415:AAHloVoz6D-n_iWZWtIE9mI6bVIqggZt6Zk')
print('Informacion del BotTelegram ')
print(bot.getMe())
bot.message_loop(portero_smart)
def timbre_activo():
    global chat_id
    bot.sendMessage(chat_id,'Tocaron la Puerta del Hogar'+time.strftime("%Y%B%d-%H:%M:%S"))
    camera=picamera.PiCamera()
    ruta='img_'+(time.strftime("%y%b%d_%H:%M:%S"))+'.jpg'
    print('imagen guardada ',ruta)
    camera.capture(ruta)
    camera.close()
    bot.sendPhoto(chat_id,photo=open(ruta,'rb'))
    bot.sendMessage(chat_id,'Foto Tomada'+time.strftime("%Y%B%d-%H:%M:%S"))
    print('imagen enviada')
def captura():
    global chat_id
    bot.sendMessage(chat_id,'Se capturo imagen de la puerta')
    camera=picamera.PiCamera()
    ruta='img_'+(time.strftime("%Y%B%d-%H:%M:%SS"))+'.jpg'
    print('imagen guarda',ruta)
    camera.capture(ruta)
    camera.close()
    bot.sendPhoto(chat_id,photo=open(ruta,'rb'))
    bot.sendMessage(chat_id,'Foto Capturada'+time.strftime("%Y%B%d-%H:%M:%S"))
while 1:
    timbre=GPIO.input(timbre_pin)
    if timbre ==0:
        print("Estado del timbre: Activo",timbre)
        timbre_activo()
    else:
        print('Estado del timbre: Inactivo',timbre)
        
    time.sleep(2)
    
GPIO.cleanup()
