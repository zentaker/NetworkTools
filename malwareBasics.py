#!/usr/bin/env python

import subprocess, smtplib


def sendEmail(email, password, message):
    #crear una instancia de smtp server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    #iniciar conexion TLS
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


comand = "msg * you have been hack"
subprocess.popen(comand, shell=True)

