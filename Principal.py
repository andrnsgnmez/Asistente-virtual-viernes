import speech_recognition as sr  #nos ayudara a que reconozca lo que le digamos
import pyttsx3  #servira para que la computadora nos hable, toma las voces intaladas
import pywhatkit  #servira para que nuestro asistente realice cosas o siga ordenes
import wikipedia #poder uscar en wiki
import datetime #maneja el tiempo
import keyboard # nos ayuda a controlar el teclado con python y leer la tecla
import os #ayuda a manipular archivos con python
import subprocess as sub #para llamar programas externos a python
#from pygame import mixer #una libreria de videojuegos importamos su mixer para musica
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

#Bautizamos nuestro asistente
name = 'viernes'
#variable para que sr empiece a reconocer la voz
listener = sr.Recognizer()

#variale para iniciar esta libreria
engine = pyttsx3.init()

#creamos variable voices para escoger la voz sino tendra una de defecto
voices = engine.getProperty('voices')
engine.setProperty('rate', 140)  #con esta propiedad ajustamos velocidad
engine.setProperty('voice', voices[3].id) #aqui escogemos la voz por medio de su id

#para ejecutar nuestro engine debemos crear el sub proceso
engine.say("¿Hola? Soy viernes, tu asistente virtual, bienvenido de vuelta,  ¿como puedo ayudarlo?")
engine.runAndWait()

def talk(text):
    engine.say(text) #con estas dos lineas es suficiente, engine.decir y dentro la variable que va pasar como parametro
    engine.runAndWait() #que ejecute y espere

#creamos una nueva funcion
def listen():
        try: #usamos un try catch sirve para verificar que el codigo sea correcto
            with sr.Microphone() as source: #es decir que nuestro sr tome nuestro microfono como una fuente para escuchar
                print("Escuchando...")
                voice = listener.listen(source) #esta nueva variable permitira que el pc escuche lo hablado
                rec = listener.recognize_google(voice, language="es") #osea que el pc tome los servicios de reconocimiento de google de la fuente voice
                rec = rec.lower() #todo lo que digamos pyhton lo reconocera y lo convertira en texto osea un string y lower lo pasa a minuscula 
                if name in rec: #con esto el programa solo funcionara si hago el llamado a viernes
                    rec = rec.replace(name, '') #el metodo replace sirve para reemplazar strings
                    print(rec)
        except:
            pass    
        return rec

#creamos funcion run, aqui harems que tolo lo que digimos en el liten, lo haga en run
def run():
    while True: #para que se ejecute hasta que le pidamos lo contrario
        rec = listen()
        if 'reproduce' in rec: # como se hizo anteriormente usamos if en rec para que realice lo solicitado solosi cumple esa condicion
            music = rec.replace('reproduce', '') #usamos una nueva variable para el replace para que no repita el rec
            talk('reproduciendo ' + music) #usamos la funcion talk
            pywhatkit.playonyt(music) #con esta linea hara todo un proceso para abrir Yt y reproducir


        elif 'busca' in rec:
            order = rec.replace('busca', '') 
            wikipedia.set_lang("es") #este  metodo nos ayuda a que viernes busque en español colocando el es cmo esttring
            info = wikipedia.summary(order, 1) #el metodo summary nos va resumir la informacion, el numero es la longuitud
            print(order +": " + info)
            talk(info)

        elif 'alarma' in rec:
            num = rec.replace('alarma', '')
            num = num.strip() #lo que hara es cortar el string vacio, para que no hayan conflictos
            talk("Alarma activada a las" + num + "horas")
            while True:
                if datetime.datetime.now().strftime('%H:%M') == num:  #la libreria ayuda con fechas y horas, con el metodo now utilizaremos la hora actual con el srt.. convertimos en texto
                    print("DESPIERTA!!!")
                    mixer.init() #iniciamos libreria
                    mixer.music.load("alarma-auronplay.mp3") #usamos para que reproduxca el audio o musica
                    mixer.music.play() # para que se reprodusca
                    if keyboard.read_key() == "s": #para que se detenga la musica
                        mixer.music.stop()
                        break


#utilizaremos un diccionario llamado sites, donde tenemos un significado y una definicion, una clave y un valor
        elif 'abre' in rec or 'abrir' in rec:
            sites={
                'google':'google.com',
                'youtube':'youtube.com',
                'materiales':'https://ingemecanica.com/tutoriales/materiales.html',
                'mecánica':'https://www.todomecanica.com/',
                'robótica':'https://realidadaumentadayotras.jimdofree.com/rob%C3%B3tica-educativa-y-programaci%C3%B3n/',
                'canva':'canva.com/folder/all-designs',
                'salud':'https://www.who.int/es',
                'Programación':'https://www.muyinteresante.es/tecnologia/articulo/cuanto-tipos-de-lenguaje-de-programacion-existen-511584540297'
            }

            programs={
                'word': r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
                'excel': r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
                'power poin': r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
                'calculadora': r"C:\Program Files\scilab-6.1.0\bin\Scilex.exe",
                'recortes': r"%windir%\system32\SnippingTool.exe",
                'zoom': r"C:\Users\harol\AppData\Roaming\Zoom\bin\Zoom.exe",
            }

            for i in list(sites.keys()):
                if i in rec:
                    sub.call(f'start chrome.exe {sites[i]}', shell=True) #usamos sub para poder abrir gogle luego las direeciones y shell ayudara como si fuera cmd
                    talk(f'Abriendo {i}')
            for app in programs:
                if app in rec:
                    talk(f'Abriendo {app}')
                    os.starfile(programs[app])


        elif 'qué puedes hacer' in rec:
            lista = rec.replace('qué puedes hacer', '')
            li_commands = {
                "abrir websites": "Ejemplo: 'abrir youtube.com'",
                "Reproducir video o musica": "Ejemplo: 'Reproduce Desde cero Drew Back'",
                "Buscar informacion": "Ejemplo: 'Busca el teorema del trabajo y la energia'",
                "Poner Alarma": "Ejemplo: 'Activa alarma 13:20'",
                "tell me": "Example: 'tell me about India'",
                "weather": "Example: 'what weather/temperature in Mumbai?'",
                "news": "Example: 'news for today' ",
            }
            
            ans = "Puedo hacer muchas cosas, por ejemplo, puedes preguntarme sobre algo que necesites, Puedo abrir sitios web para ti, Activar alarmas y más. Ver la lista de comandos-"
            print(ans)
            print(li_commands)
            talk(ans)

        elif 'escribe' in rec:
            try:
                with open("nota.txt", 'a') as f: 
                    write(f) #la funcion esta abajo

            except FileNotFoundError as e:
                file = open("nota.txt", 'w')
                write(file)
                



        elif 'termina' in rec or 'terminar' in rec or 'termino' in rec:
            talk('Como usted ordene. Estare aqui esperando a sus ordenes. Que tenga buen día, jéfe.') 
            break    

def write(f): #argumento llamado f osea un archivo
    talk("¿Qué quieres que escriba?")
    rec_write = listen() #variable para que reconozca la voz
    f.write(rec_write + os.linesep) # escribira el texto que reconozca con nuestra voz y el os hara un salto de linea
    f.close()
    talk("Listo, puedes revisarlo")
    sub.Popen("nota.txt", shell=True) # abrira nuestro archivo para mostrar

run()

