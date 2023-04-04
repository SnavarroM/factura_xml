import os
from imbox import Imbox
import traceback
import schedule
import time
from datetime import datetime
import subprocess

#! habilite aplicaciones menos seguras en su cuenta de Google
#! https://myaccount.google.com/lesssecureapps

def job():
    host = "imap.gmail.com"
    username = "copiafactura@cenabast.cl"
    password = 'Copia4040$$'
    download_folder = (r'C:\Users\snavarro\Desktop\toma de requerimientos\xml sii\script\scripts cenabast\decargas_gmail_python')

    if not os.path.isdir(download_folder):
        os.makedirs(download_folder, exist_ok=True)

    mail = Imbox(host, username=username, password=password,
                 ssl=True, ssl_context=None, starttls=False)
    messages = mail.messages(unread=True)  #! solo mensajes no leídos

    for (uid, message) in messages:
        mail.mark_seen(uid)  #! opcional, marcar el mensaje como leído

        for idx, attachment in enumerate(message.attachments):
            try:
                att_fn = attachment.get('filename')
                if att_fn.endswith('.xml'):
                    now = datetime.now()
                    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
                    new_att_fn = f"{dt_string}_{att_fn}"
                    download_path = f"{download_folder}/{new_att_fn}"
                    print(download_path)
                    with open(download_path, "wb") as fp:
                        fp.write(attachment.get('content').read())
                    subprocess.call(['python', 'insertion_2.3.4_no_repita_xml_cada_minuto.py', download_path])
            except:
                print(traceback.print_exc())

    mail.logout()

schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)