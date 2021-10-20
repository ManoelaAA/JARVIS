import sys
import os
from nltk.probability import FreqDist
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import pyttsx3
import datetime
import webbrowser as web
import wikipedia
from pydub import AudioSegment
from pydub.playback import play
import numpy as np
from numpy import asarray, object_, void
from numpy import savetxt

# Importa as bibliotecas do firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Importa os arquivos complementares
from En_2_Pt import *
from JARVIS_start import *
from open import *
from jokes import *



# ------------------------------------------------------------------------------------------------------------------------------------------------------------------- #



# ----- CONFIGURA A VOZ DO JARVIS ----- #
#Cria o objeto 
engine = pyttsx3.init('sapi5')

#Configura o ritmo/tempo
rate = engine.getProperty('rate')
engine.setProperty('rate', 175)

#Configura o volume
volume = engine.getProperty('volume')
engine.setProperty('volume',1.0)

#Configura a voz
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)



# ----- CONFIGURA O BANCO DE DADOS DO FIREBASE ----- #

# Define o caminho para a chave de segurança do banco de dados
database = os.path.dirname(__file__) + '\\database\\jarvis-personal-project.json'

# Buscar o conteúdo do arquivo JSON da chave da conta de serviço
cred = credentials.Certificate(database)

# Inicialize o aplicativo com uma conta de serviço, concedendo privilégios de administrador
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://jarvis-personal-project-default-rtdb.firebaseio.com/'
})



# ----- CONFIGURA O HORARIO ATUAL ----- #
# Define a variavel das datas
dt = datetime.datetime.now()

# Define as variavies com o horario
hr = dt.strftime("%H")
min = dt.strftime("%M")



# ----- CONFIGURA O HORARIO ATUAL ----- #
reminder_info = ['', '']



# ----- CONFIGURA OS CAMINHOS DOS ARQUIVOS QUE SERÃO USADOS ----- #
# Audios
joke_efect = os.path.dirname(__file__) + '\\audio\\joke_efect.wav'
open (joke_efect)
note = os.path.dirname(__file__) + '\\audio\\note.wav'
open (note)
alarm = os.path.dirname(__file__) + '\\audio\\alarm.wav'
open (alarm)



# ----- CONFIGURA OS ENDEREÇOS DA WEB ----- #
path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
url_search = "https://www.google.com/search?q="
wikipedia_search = "http://en.wikipedia.org/wiki/"



# Define as variaveis para configurações do console
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'



# ------------------------------------------------------------------------------------------------------------------------------------------------------------------- #



# Função para procurar alarme para o dia e horario atual
def search_alarm(day, hr):
    # Define o caminho do banco de dados para os dados do alarme
    ref_alarm = db.reference('alarmes')

    # Ordena os dados dos alarmes
    snapshot = ref_alarm.order_by_child('day').get()

    # Procura o alarme que tocará no dia e horario atual
    for key, val in snapshot.items():

        # Verifica se existe um alarme que deverá tocar nesse momento
        if day in '{0}'.format(val) and hr in '{0}'.format(val):
            print(f'alarmes que tocarão agora: {key}\n')

            # Toca o alarme
            JARVIS_answer(f'O alarme de {key} tocará')
            playsound(alarm)


# Função para verificar se existe um evento para o horario atual
def search_events(day, hour):
    # Define o caminho do banco de dados para os dados do alarme
    ref_event = db.reference('eventos')

    # Ordena os dados dos alarmes
    snapshot = ref_event.order_by_child('day').get()

    # Procura o alarme que tocará no dia e horario atual
    for key, val in snapshot.items():

        if day in '{0}'.format(val) and hour in '{0}'.format(val):
            print(f'\neventos que acontecerão agora: {key}')

            # Deleta o evento do banco de dados
            delete_event = ref_event.child(key)
            delete_event.delete()


# Função para adicionar uma anotação
def new_notes(new_note):
    # Define o caminho do banco de dados para os dados das anotações
    ref_notes = db.reference('anotações')

    notes_saves = []

    # Organiza anotações
    snapshot = ref_notes.order_by_child('day').get()

    # ----- Adiciona uma anotação ----- #
    ref_notes.update(new_note)

    # ----- Mostra todas as anotações salvas ----- #
    for key, val in snapshot.items():
        note = f'{0}'.format(key)

        notes_saves = [note] + notes_saves


# Função para mostrar as anotações salvas
def show_notes():
    # Define o caminho do banco de dados para os dados das anotações
    ref_notes = db.reference('anotações')

    # Organiza anotações
    snapshot = ref_notes.order_by_child('day').get()

    notes = []

    # ----- Mostra todas as anotações salvas ----- #
    for key, val in snapshot.items():
        note = '{0}'.format(key)

        print(note)

        # Armazena as anotações em uma variavel
        notes = [note] + notes

    return notes


# Função para deletar uma anotação
def delete_note(note):
    # Define o caminho do banco de dados para os dados das anotações
    ref_notes = db.reference('anotações')

    # Organiza anotações
    snapshot = ref_notes.order_by_child('day').get()

    # ----- Verifica se existe uma anotação ----- #
    if f'{note}' in '{0}'.format(snapshot.items()):

        # ----- Deleta uma anotação ----- #
        delete_note = ref_notes.child(note)

        delete_note.delete()
    
    else:
        JARVIS_answer('Nenhuma anotação encontrada')

        # break


# Função para adicionar alarme
def add_alarm(name, day, time):

    # Define o caminho do banco de dados para os dados do alarme
    ref_alarm = db.reference('alarmes')

    # Estrutura os dados para enviar para o banco de dados
    new_alarm = {
        name :{
            'day': day,
            'time': time
        }
    }

    # Envia o novo alarme para o banco de dados
    ref_alarm.update(new_alarm)


# Função para deletar um alarme
def delete_alarm(alarm):
    # Define o caminho do banco de dados para os dados dos alarmes
    ref_alarm = db.reference('alarmes')

    # Ordena os dados dos alarmes
    snapshot = ref_alarm.order_by_child('day').get()

    # ----- Verifica se existe um alarme ----- #
    if f'{alarm}' in '{0}'.format(snapshot.items()):
        # ----- Deleta um alarme ----- #
        delete_alarm = ref_alarm.child(alarm)

        delete_alarm.delete()

    else:
        JARVIS_answer('Nenhum alarme encontrado')


# Função para mostrar os alarmes salvos
def show_alarms():
    # Define o caminho do banco de dados para os dados dos alarmes
    ref_alarm = db.reference('alarmes')

    # Organiza os alarmes
    snapshot = ref_alarm.order_by_child('day').get()

    alarms = []

    # ----- Mostra todos os alarmes salvos ----- #
    for key, val in snapshot.items():
        alarm = '{0}'.format(key)

        print(alarm)

        # Armazena os alarmes em uma variavel
        alarms = [alarm] + alarms

    return alarms


# Função para adicionar evento
def add_event(name, day, time):

    # Define o caminho do banco de dados para os dados do evento
    ref_event = db.reference('eventos')

    # Estrutura os dados para enviar para o banco de dados
    new_event = {
        name :{
            'day': day,
            'time': time
        }
    }

    # Envia o novo evento para o banco de dados
    ref_event.update(new_event)


# Função para mostrar os eventos salvos
def show_events():
    # Define o caminho do banco de dados para os dados dos eventos
    ref_events = db.reference('eventos')

    # Organiza os eventos
    snapshot = ref_events.order_by_child('day').get()

    events = []

    # ----- Mostra todas os eventos salvos ----- #
    for key, val in snapshot.items():
        event = '{0}'.format(key)

        print(event)

        # Armazena os eventos em uma variavel
        events = [event] + events

    return events


# Função para deletar um evento
def delete_event(event):
    # Define o caminho do banco de dados para os dados dos eventos
    ref_event = db.reference('eventos')

    # Ordena os dados dos alarmes
    snapshot = ref_event.order_by_child('day').get()

    # ----- Verifica se existe um evento ----- #
    if f'{event}' in '{0}'.format(snapshot.items()):

        # ----- Deleta um evento ----- #
        delete_event = ref_event.child(event)

        delete_event.delete()

    else:
        JARVIS_answer('Nenhum evento encontrado')


# Função para verificar se o lembrete deverá ser avisado
def notification_reminder(reminder, reminder_time, hr, min):

    if f"{reminder_time}" == f"{hr}:{min}":
        JARVIS_answer(f"Você tinha me pedido para te lembrar de {reminder}")



# ------------------------------------------------------------------------------------------------------------------------------------------------------------------- #



# Função para o JARVIS falar
def JARVIS_answer(answer):
    engine.say(answer)
    engine.runAndWait()
    engine.stop()


#Função para captar o que foi falado do usuário
def spoken_recognition():

    sentence = ''

    #Habilita o microfone do usuário
    MIC = sr.Recognizer()
    
    #Usando o microfone
    with sr.Microphone() as source:
        
        #Chama um algoritmo de redução de ruidos no som
        MIC.adjust_for_ambient_noise(source)
        
        #Frase para o usuario dizer algo
        print("\nDiga alguma coisa: ")
        
        #Armazena o que foi dito numa variavel
        audio = MIC.listen(source)
    try:
        
        #Passa a variável para o algoritmo reconhecedor de padroes
        sentence = MIC.recognize_google(audio, language='pt-BR')
        sentence = sentence.lower()

        #Retorna a frase pronunciada
        print(f"\nVocê disse: {sentence}")
        
    #Se nao reconheceu o padrão de fala, exibe a mensagem
    except sr.UnknownValueError:
	    sentence = "não entendi..."

        
    return sentence.lower()


# Analisa o que foi dito pelo usuário
def spoken_analyzer(spoken, hr, min):

    # O que será respondido pelo JARVIS
    answer = ''

    # Variavel para verificar se foi pedido algo não programado
    err = ''

    # Cria a variavel para armazenar as informações do lembrete
    global reminder_info

    # --------------- Possibilidades de respostas do JARVIS --------------- #

    # --------------- BASICO --------------- #
    #Caso o usuario diga como você está
    if "como você está" in spoken:

        JARVIS_answer("estou bem, e você?")
    

    #Caso o usuario diga que horas são
    elif "horas são" in spoken:

        JARVIS_answer(f"Agora são {hr} horas e {min} minutos")


    #Caso o usuario diga que dia é hoje
    elif "dia é hoje" in spoken:

        # Atualiza a data atual do JARVIS
        dt = datetime.datetime.now()
        month = dt.strftime("%B")
        day = dt.strftime("%A")
        year = dt.strftime("%Y")

        # Traduz o dia e o mês
        day = days(day)
        month = months(month)

        JARVIS_answer(f'Hoje são {day} de {month}, do ano de {year}')


    #Caso o usuario diga quanto é 
    elif "quanto é " in spoken:

        # Separa do que foi dito a conta que foi pedida
        cal = spoken.split('quanto é ')[1]
        print(cal)

        # Substitui o sinal de multiplicação pelo que conseguirá fazer a conta
        if "x" in cal:
            cal = cal.replace("x", "*")

        calculated = ''.join(cal)

        # Calcula a conta pedida
        result = eval(calculated)

        print(f"\nresultado da conta: {result}")

        JARVIS_answer(f"O resultado é {result}")


    #Caso o usuario diga conte uma piada
    elif "conte uma piada" in spoken:
        
        # Define o array das piadas
        shuffle = np.array(piadas)

        # Sorteia uma piada
        np.random.shuffle(shuffle)

        # Separa em variaveis separadas a pergunta e a resposta da piada
        question = shuffle[0][0]
        answer = shuffle[0][1]

        print(f"\npergunta: {question}")

        # Conta a pergunta da piada
        JARVIS_answer(f"{question}")

        time.sleep(3)

        print(f"\nresposta: {answer}")

        # Conta a resposta da piada
        JARVIS_answer(f"{answer}")

        # Toca o efeito sonoro da piada
        playsound(joke_efect)


    # Caso o usuario diga obrigado/a
    elif "obrigad" in spoken:
        JARVIS_answer('merece, estou aqui para ajudar')

    
    # Caso o usuario diga me lembre de
    elif"me lembre de " in spoken:

        # Separa do que foi dito o que deverá ser lembrado
        reminder = spoken.split("de ")[1]

        print(reminder)

        # Verifica se o horario do lembrete será na proxima hora
        if int(min) + 5 >= 60:
            min_reminder = (int(min) + 1) - 60
            hour_reminder = int(hr) + 1

        else: 
            min_reminder = int(min) + 1
            hour_reminder = hr

        # Verifica se os minutos do lembrete é menor que 10 para acrescentar o 0 antes
        if min_reminder < 10:
            min_reminder = f"0{min_reminder}"

        # Define o horario do lembrete
        time_reminder = f"{hour_reminder}:{min_reminder}"

        print(time_reminder)

        # Armazena as informações do lembrete
        reminder_info = [reminder, time_reminder]



    # --------------- PESQUISAS --------------- #
    #Caso o usuario diga pesquise (pesquisa no Google Chrome)
    elif "pesquise " in spoken:

        # Separa do que foi dito o que será pesquisado
        key_word = spoken.split('pesquise ')[1]

        print(f"\nO que será pesquisado: {key_word}")

        # Define o endereço da web que será aberto os resultados da pesquisa
        search = url_search + key_word

        JARVIS_answer(f"Um momento, aqui são os resultados encontrados para {key_word}")

        # Abre a pagina da web com os resultados da pesquisa
        web.open_new_tab(search)


    #Caso o usuario diga o que é (abre uma página da wikipédia)
    elif "que é " in spoken:

        # Separa do que foi dito o que foi perguntado
        search = spoken.split('que é ')[1]

        # Define a linguagem da pesquisa
        wikipedia.set_lang("pt")

        # Define o resultado da pesquisa e o que será dito pelo JARVIS
        result = wikipedia.summary(search, sentences=1)
        searched = wikipedia.page(search)
        page = searched.url

        print(f"\nlink da página: {page}")
        print (f"resultado: {result}")

        # Abre a pagina da wikipedia do resultado
        web.open_new_tab(page)

        JARVIS_answer(f"{result}")



    # --------------- APLICATIVOS E SITES --------------- #
    #Caso o usuario diga abra (abre um arquivo de programa do computador)
    elif "abra " in spoken:

        # Separa do que foi dito o que deverá ser aberto
        program = spoken.split('abra ')[1]

        print(f"\nprograma que será aberto: {program}")

        JARVIS_answer(f'Um momento... {program} está sendo aberto')

        # Abre o programa desejado
        none_prog = programs(program)

        # Verifica se o programa desejado existe
        if none_prog == True:
            JARVIS_answer('nenhum programa foi encontrado')

    
    #Caso o usuario diga acesse (abre um site no chrome)
    elif "acesse " in spoken:

        # Separa do que foi dito o que deverá ser aberto
        site_path = spoken.split('acesse ')[1]

        print(f"\nsite que será aberto: {site_path}")

        JARVIS_answer(f'Um momento... {site_path} está sendo aberto')

        # Abre o site desejado
        none_site = site(site_path)

        # Verifica se o programa desejado está salvo no sistema
        if none_site == True:
            JARVIS_answer('Esse site não está salvo')
    


    # --------------- BANCO DE DADOS --------------- #

    # Anotações #
    # Caso o usuario diga crie uma anotação chamada
    elif "crie uma anotação " in spoken:
        
        # Separa do que foi dito a anotação
        note = spoken.split('anotação ')[1]

        # Atualiza a data atual do JARVIS
        dt = datetime.datetime.now()
        day = dt.strftime("%d")
        month = dt.strftime("%m")

        # Cria a anotação no formato para envio para o banco de dados
        new_note = {
            note:{
                'day' : f'{day}/{month}'
            }
        }

        # Envia, através da função, a anotação
        new_notes(new_note)

        JARVIS_answer(f'Entendido, {note} foi anotado')


    # Caso o usuario diga quais são minhas anotações
    elif "quais são minhas anotações" in spoken:

        JARVIS_answer('Um momento... estas são as anotações salvas: ')

        # Armazena as anotações
        notes = show_notes()

        # Diz toda as anotações salvas no banco de dados
        for x in notes:
            JARVIS_answer(f'{x}')


    # Caso o usuario diga delete minha anotação
    elif "delete minha anotação " in spoken:

        # Separa do que foi dito a anotação que será delatada
        note = spoken.split("anotação ")[1]

        JARVIS_answer(f'Entendido, sua anotação {note} será deletada')

        # Deleta a anotação pedida
        delete_note(f'{note}')



    # Alarmes #
    # Caso o usuario diga crie um alarme
    elif "crie um alarme " in spoken:

        # Verifica se todos os dados para criação do alarme foram ditos corretamente
        if ' para ' in spoken and ' de ' in spoken:

            # Configura o nome do alarme
            name_alarm = spoken.split("alarme ")[1]
            name_alarm = name_alarm.split(" para")[0]

            print(name_alarm)

            # Configura o horario do alarme
            time_alarm = spoken.split("para ")[1]
            time_alarm = time_alarm.split("de ")[0]

            #Caso o usuario tenha marcado para o meio-dia
            if "meio-dia" in time_alarm:
                time_alarm = "12:00"

            #Caso o usuario tenha marcado para a meia-noite
            elif "meia-noite" in time_alarm:
                time_alarm = "24:00"

            #Caso não tenha os minutos
            elif "horas" in time_alarm:
                hour = time_alarm.split(' horas')[0]

                time_alarm = f"{hour}:00"

            print(time_alarm)

            day_alarm = spoken.split("de ")[1]
            
            # Substitui o "e" dos dias por um espaço
            if " e " in day_alarm:
                day_alarm = day_alarm.replace(" e ", " ")

            # Configura os dias do alarme
            day_alarm = day_alarm.split()

            print(day_alarm)

            days_alarm = []

            # Transforma os dias para a abreviação
            for x in day_alarm:
                day = days_short(x)

                days_alarm = [day] + days_alarm

            print(days_alarm)

            comma = ', '

            # Transforma a lista de dias do alarme para string
            day_alarm = comma.join(days_alarm)

            print(day_alarm)

            JARVIS_answer(f'Entendido, seu alarme {name_alarm} foi criado')

            # Adiciona o alarme ao anco de dados
            add_alarm(name_alarm, day_alarm, time_alarm)

        else:
            JARVIS_answer('Dados para criação do alarme inválidos')


    # Caso o usuario diga quais são meus alarmes
    elif "quais são os meus alarmes" in spoken:
        JARVIS_answer('Um momento... estes são seus alarmes salvos: ')

        # Armazena os alarmes
        alarms = show_alarms()

        # Diz todos os alarmes do banco de dados
        for x in alarms:
            JARVIS_answer(f'{x}')


    # Caso o usuario diga delete meu evento
    elif "delete meu alarme " in spoken:

        # Separa do que foi dito a anotação que será delatada
        alarm = spoken.split("alarme ")[1]

        JARVIS_answer(f'Entendido, seu alarme {alarm} será deletado')

        # Deleta a anotação pedida
        delete_alarm(f'{alarm}')



    # Eventos #
    # Caso o usuario diga crie um evento
    elif "crie um evento " in spoken:

        # Verifica se todos os dados para criação do evento foram ditos corretamente
        if ' dia ' in spoken and ' às ' in spoken:

            # Configura o nome do evento
            name_event = spoken.split("evento ")[1]
            name_event = name_event.split(" para")[0]

            print(name_event)

            # Configura o dia do alarme
            day_event = spoken.split("para dia ")[1]
            day_event = day_event.split("às ")[0]

            # Substitui o "do" do dia por uma barra
            if " do " in day_event:
                day_event = day_event.replace(" do ", "/")
            
            # Substitui o "de" do dia por uma barra
            if " de " in day_event:
                day_event = day_event.replace(" de ", "/")

            # Verifica se o mês foi dito em forma de numero ou palavra
            month = day_event.split("/")[1]
            month = ''.join(month)

            day = day_event.split("/")[0]

            # Caso o mês informado esteja em forma de numero
            if month.isnumeric():
                print("mês numero")

            # Caso o mês informado esteja na forma de palavra
            else:
                month = month2num(month)
                print(month)

                day_event = f'{day}/{month}'     

            print(day_event)

            # Configura o horario do alarme
            time_event = spoken.split("às ")[1]

            #Caso o usuario tenha marcado para o meio-dia
            if "meio-dia" in time_event:
                time_event = "12:00"

            #Caso o usuario tenha marcado para a meia-noite
            elif "meia-noite" in time_event:
                time_event = "24:00"

            #Caso não tenha os minutos
            elif "horas" in time_event:
                hour = time_event.split(' horas')[0]

                time_event = f"{hour}:00"

            print(time_event)

            JARVIS_answer(f'Entendido, seu evento {name_event} foi criado')

            # Adiciona o evento ao banco de dados
            add_event(name_event, day_event, time_event)

        else:
            JARVIS_answer('Dados para criação de um evento inválidos')


    # Caso o usuario diga quais são meus eventos
    elif "quais são os meus eventos" in spoken:
        JARVIS_answer('Um momento... estes são seus eventos salvos: ')

        # Armazena os eventos
        events = show_events()

        # Diz todos os eventos do banco de dados
        for x in events:
            JARVIS_answer(f'{x}')


    # Caso o usuario diga delete meu evento
    elif "delete meu evento " in spoken:

        # Separa do que foi dito a anotação que será delatada
        event = spoken.split("evento ")[1]

        JARVIS_answer(f'Entendido, seu alarme {event} será deletado')

        # Deleta a anotação pedida
        delete_event(f'{event}')



    # --------------- NENHUM COMANDO ENCONTRADO --------------- #
    else:
        err = "err"

    return reminder_info, err



# ------------------------------------------------------------------------------------------------------------------------------------------------------------------- #



# Inicia a programação
while True:

    JARVIS_answer("Bem-vinda de volta")

    # Espera o comando inicial para iniciar o sistema
    while True:

        # Atualiza a data atual do JARVIS
        dt = datetime.datetime.now()    
        hr = dt.strftime("%H")
        min = dt.strftime("%M")
        month = dt.strftime("%m")
        day = dt.strftime("%A")

        # Transforma o dia de acordo com o desejado
        day = days(day)
        day = days_short(day)

        print(f'\n{day} às {hr}:{min}')

        # Define qual será a resposta inicial do JARVIS de acordo com a hora do dia
        JARVIS_init = JARVIS_start(int(hr))

        # Retorna o que foi dito pelo usuario
        sentence = spoken_recognition()

        # Verifica se o lembrete deverá ser falado
        notification_reminder(reminder_info[0], reminder_info[1], hr, min)

        # Caso o usuario tenha dito a palavra de comando
        if 'jarvis' in sentence:
            JARVIS_answer(f'{JARVIS_init}, em que posso ajudar?')

            break

        # Caso o usuario tenha dito até logo o JARVIS encerra
        if "até logo" in sentence:
            JARVIS_answer('até logo, foi bom conversar com você')

            sys.exit()
            
        # Verifica se uma palavra foi falada pelo usuario
        elif "não entendi..." != sentence:
            JARVIS_answer('palavra de comando incorreta')


    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------- #


    # Responderá aos comandos
    while True:

        # Atualiza a data atual do JARVIS
        dt = datetime.datetime.now()    
        hr = dt.strftime("%H")
        min = dt.strftime("%M")
        month = dt.strftime("%m")
        day = dt.strftime("%A")

        # Transforma o dia de acordo com o desejado
        day = days(day)
        day = days_short(day)

        print(f'\n{day} às {hr}:{min}')

        # Retorna o que foi dito pelo usuario
        sentence = spoken_recognition()
        
        # Envia o que foi dito pelo usuario para que o JARVIS responda
        reminder_info, err = spoken_analyzer(sentence, hr, min)

        # Atualiza a data atual do JARVIS
        dt = datetime.datetime.now()    
        hr = dt.strftime("%H")
        min = dt.strftime("%M")
        month = dt.strftime("%m")
        day = dt.strftime("%A")

        # Verifica se o lembrete deverá ser falado
        notification_reminder(reminder_info[0], reminder_info[1], hr, min)

        # Procura por alarmes que tocarão agora
        search_alarm(day, f'{hr}:{min}')

        # Procura por eventos que tocarão agora
        search_events(day, f'{hr}:{min}')

        # ------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

        # Caso não tenha identificado nada
        if "não entendi..." in sentence:
            JARVIS_answer('não entendi...')

        # Caso o usuario tenha dito descansar o JARVIS entra em modo descanso
        elif "descansar" in sentence:
            JARVIS_answer('Entendido, estarei aqui se precisar de algo')

            break

        # Caso o usuario tenha dito até logo o JARVIS encerra
        elif "até logo" in sentence:
            JARVIS_answer('até logo, foi bom conversar com você')

            sys.exit()
        
        # Caso o usuario diga um comando desconhecido
        elif err == "err":
            JARVIS_answer("Desculpe, não poderei ajudar com isso")
