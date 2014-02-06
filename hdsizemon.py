#!/usr/bin/env python
# -*- coding: utf-8 -*-
*******************************************
#        Ing. Kennedy Sanchez			        #
#    (Security + MGP + PS. Auditor)       #
#     @ksanchez_cld on twitter			      #
******************************************* 	

import paramiko
import os, smtplib, time
from sys import stdin
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

print "###########CR NET MONITOR###########"
print "   Disk Monitor Tool by Ksanchez    "
print "        05 Feb. 2014                "
print "####################################"
time.sleep(3)

horaRaw = time.time()
horaFormato = time.ctime(horaRaw)

SERVIDOR_SSH = ''
PUERTO_SSH   = PORT
USUARIO_SSH  = ''
CLAVE_SSH    = ''
CMD_HOST     = 'hostname'
PATH         = '/tmp/monitoreo'

def sshXfer():
	cnx = paramiko.Transport((SERVIDOR_SSH, PUERTO_SSH))
	cnx.connect(username = USUARIO_SSH, password = CLAVE_SSH)

	canal = cnx.open_session()
	canal.exec_command('rm -rf /tmp/monitoreo/ && mkdir -p /tmp/monitoreo && hostname >/tmp/monitoreo/size_servidores.log && df -h >>/tmp/monitoreo/size_servidores.log') 

	salida = canal.makefile('rb', -1).readlines()
	if salida:
		print salida
	else:
		print canal.makefile_stderr('rb', -1).readlines()
	cnx.close()
	print ('*'*50)
	print ('TRANSFIRIENDO ARCHIVOS....')
	print ('*'*50)

	cnx = paramiko.Transport((SERVIDOR_SSH, PUERTO_SSH))
	cnx.connect(username = USUARIO_SSH, password = CLAVE_SSH)

	sftp = paramiko.SFTPClient.from_transport(cnx)
	archivos = sftp.listdir('/tmp/monitoreo/')
	for f in archivos:
	  print "Recibiendo ",f
	  sftp.get(os.path.join('/tmp/monitoreo/',f),f)
	cnx.close()

def sendMail():
	msg = MIMEMultipart()
	msg['From'] = "k.sanchez@crcltd.com.do"
	#body = msg.attach( MIMEText(r))
	msg['Subject'] = "Reporte diario monitoreo espacio en disco" 
	macct = "ksanchez@micorreo.com"
	msg.attach( MIMEText("Adjunto, archivo de espacio en disco.\n\n" + "Realizado en fecha:" + horaFormato))
	files=["size_servidores.log"]
	for f in files:
	    part = MIMEBase('application', "octet-stream")
	    part.set_payload( open(f,"rb").read())
	    Encoders.encode_base64(part)
	    part.add_header('Content-Disposition', 'attachment; filename="size_servidores.log"')
	    msg.attach(part)
	s = smtplib.SMTP()
	s.connect(SERVER, PORT)
	s.sendmail("ksanchez@micorreo.com", macct , msg.as_string())
	s.quit()

sshXfer()
sendMail()
