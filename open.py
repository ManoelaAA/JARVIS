import webbrowser as web
import subprocess
import time



# ----- CONFIGURA O ENDEREÇO DA WEB ----- #
path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"



#Programas que poderão ser abertos
def programs(open_prog):
    
    none_prog = False

    if "google" in open_prog:
        
        subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe ')
        time.sleep(0.5)

    if "vs code" in open_prog:

        subprocess.Popen(r"caminho/completo/para/o/programa")
        time.sleep(0.5)

    if "teams" in open_prog:

        subprocess.Popen(r"caminho/completo/para/o/programa")
        time.sleep(0.5)

    if "powerpoint" in open_prog:
        subprocess.Popen(r"caminho/completo/para/o/programa")
        time.sleep(0.5)

    if "word" in open_prog:

        subprocess.Popen(r"caminho/completo/para/o/programa")
        time.sleep(0.5)
    
    if "discord" in open_prog:

        subprocess.Popen(r"caminho/completo/para/o/programa")
        time.sleep(0.5)
    
    if "spotify" in open_prog:

        subprocess.Popen(r"caminho/completo/para/o/programa")
        time.sleep(0.5)

    else:
        none_prog = True
    
    return none_prog


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------- #



#Sites que poderão ser abertos através do comando acesse
def site(site_path):

    none_site = False

    if "youtube" in site_path:

        web.get(path).open("https://www.youtube.com/")

    elif "e-mail" in site_path:

        web.get(path).open("https://mail.google.com/mail/u/0/?ogbl#inbox")

    elif "drive" in site_path:

        web.get(path).open("https://drive.google.com/drive/my-drive")

    elif "netflix" in site_path:

        web.get(path).open("https://www.netflix.com/browse")
    
    elif "disney" in site_path:

        web.get(path).open("https://www.disneyplus.com/pt-br/home")

    else:
        none_site = True

    return none_site
