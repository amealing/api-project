#!/bin/env python2.7

import imaplib
import email
import smtplib
import datetime
import logging
import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def check_email(user, password, subject):
	
	mail = imaplib.IMAP4_SSL("imap.gmail.com")
	mail.login(user, password)
	mail.select()

	typ, msgs = mail.search(None, 'subject', subject)

	if not msgs[0]:
		return 0

	emailid = msgs[0].split()[0]
	resp, data = mail.fetch(emailid, "(RFC822)")
	email_body = data[0][1] 
	m = email.message_from_string(email_body)

	return [m['From'],m['Subject']]

def check_email_return_attachments(user, password, target_dir):

	output_info = {}
	
	mail = imaplib.IMAP4_SSL("imap.gmail.com")
	mail.login(user, password)
	mail.select()

	typ, msgs = mail.search(None, 'UNSEEN')

	if not msgs[0]:
		return 0

	emailid = msgs[0].split()[-1]
	resp, data = mail.fetch(emailid, "(RFC822)")
	email_body = data[0][1] 
	m = email.message_from_string(email_body)
	
	output_info['From'] = m['From']
	output_info['attachments'] = []
	logging.info(m['From'])
	logging.info(datetime.datetime.today().strftime("%Y-%m-%d at %H:%M"))
	
	for part in m.walk():
		if part.get_content_maintype() == 'multipart':
			continue
		if part.get('Content-Disposition') is None:
			continue
		filename=part.get_filename()
		if filename is not None and is_txt_csv(filename):
			output_info['attachments'].append(filename)
			sv_path = os.path.join(target_dir, filename)
			fp = open(sv_path, 'wb')
			fp.write(part.get_payload(decode=True))
			fp.close()
			
	logging.info(output_info['attachments'])
	
	return output_info

def is_txt_csv(filename):
	extension = filename.split('.')[1]
	if extension in ["csv","txt"]:
		return 1
	else:
		return 0

def send_email(user, password, recipient, subject, text=None, files=None):

	gmail_user = user
	gmail_pwd = password
	FROM = user
	TO = recipient
	SUBJECT = subject

	msg = MIMEMultipart()
	msg['From'] = FROM
	msg['To'] = TO
	msg['Subject'] = subject
	msg.attach(MIMEText(text))

	for f in files or []:
		with open(f, "rb") as fil:
			part = MIMEApplication(
				fil.read(),
				Name=os.path.basename(f)
			)
			part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(f)
			msg.attach(part)
	

	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.ehlo()
	server.starttls()
	server.login(gmail_user, gmail_pwd)
	server.sendmail(FROM, TO, msg.as_string())
	server.close()
	print 'successfully sent the mail'


def get_email_from_string(email):
	# Turn into Regex
	email_address = email.split(" ")[-1]
	email_address = email_address.replace('<',"").replace('>',"")
	return email_address

def is_email_permitted(email, permitted):
	if email in permitted:
		return True
	else:
		return False

def send_email_safely(user, password, recipient, subject, text=None, files=None):
	counter = 0
	max_attempts = 4
	while counter < max_attempts:
		try:
			send_email(user, password, recipient, subject, text, files)
			break
		except:
			logging.exception('Sending output files') 
			counter += 1
	if counter == 4:
		today = datetime.datetime.today().strftime("%Y-%m-%d at %H:%M")
		logging.exception('Attempted to send message 4 times and failed {}-{}-{}-{}-{}'.format(recipient, subject, text, files, today))
		return counter

def delete_email(user, password, subject):
	mail = imaplib.IMAP4_SSL("imap.gmail.com")
	mail.login(user, password)
	mail.select()
	typ, msgs = mail.search(None,'subject', subject)
	emailid = msgs[0].split()[0]
	mail.store(emailid, '+FLAGS', '\\Deleted')
	mail.expunge()
	search = mail.search(None,'subject', subject)
	return search[1][0]

if __name__ == '__main__':
	delete_email(os.environ["USERNAME"]
							, os.environ["PASSWORD"]
							, "TEST_DELETE_EMAIL")