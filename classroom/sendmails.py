import smtplib, ssl
import json

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pytz import timezone
from datetime import datetime

"""
Method to send emails.
"""

def sendMails(HTML, receiver_email):
	# Setting configuration values
	port = 465
	smtp_server = "smtp.gmail.com"
	sender_email = 'oathtocode@gmail.com'
	pwd = 'hackathon@12#21'

	message = MIMEMultipart("alternative", None, [MIMEText(HTML, 'html')])
	message['Subject'] = 'Classroom'
	message['From'] = sender_email

	# Create a secure SSL context
	context = ssl.create_default_context()
	server = smtplib.SMTP_SSL(smtp_server, port, context=context)
	try:
		server.login(sender_email, pwd)
	except Exception as e:
		print("Invalid password.")
		print(e)
		return False

	try:
		server.sendmail(sender_email, receiver_email, message.as_string())
		print("Emails sent successfully.")
	except Exception as e:
		server.quit()
		return False

	server.quit()
	return True



"""
def sendVerificationMail(receiver_email, msg):

	# Setting configuration values
	port = 465
	smtp_server = "smtp.gmail.com"
	sender_email = 'o1devmail@gmail.com'

	# pwd = os.environ['PWD'].encode('utf-8')

	# Not suitable for production
	pwd = "gAAAAABfYfJ0RKc2ME-juklP9IlzLjPkpQ_2OJ1H5nNFLTbpd2ii-h6xuIwR5K866IcBuru9owhfKUVolITFdug7v4fPF6IE0Q==".encode('utf-8')
	key = SecretKey.objects.get(name = "master").key
	try:
		sender_pwd = Fernet(key).decrypt(pwd).decode()
	except:
		logging.exception("Exception occurred.")
		print("Invalid password.")
		return False

	message = ""Subject: Verification email



""
	message += msg

	# Create a secure SSL context
	context = ssl.create_default_context()
	server = smtplib.SMTP_SSL(smtp_server, port, context=context)

	try:
		server.login(sender_email, sender_pwd)
	except Exception as e:
		logging.exception("Exception occurred.")
		print("Invalid password.")
		return False

	try:
		server.sendmail(sender_email, receiver_email, message)
		print("Verification email sent successfully.")
	except Exception as e:
		logging.exception("Exception occurred.")
		server.quit()
		return False

	server.quit()
	return True
"""