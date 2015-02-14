import os

from app import Message

from twilio.rest import TwilioRestClient
import sendgrid

client = TwilioRestClient(account=os.getenv('TWILIO_SID'), token=os.getenv('TWILIO_TOKEN'))
sg = sendgrid.SendGridClient(os.getenv('SG_USER'), os.getenv('SG_PASSWORD'))

messages = Message.query.all()

for m in messages:
  msgText = """ Hi, %s. Your valentine %s has left you a love message. Find it here: http://bit.ly/aecc-love2 with your password: %s. Have fun <3 """ % (m.receiver, m.sender, m.password)
  client.messages.create(to=m.phone, from_=os.getenv('TWILIO_NUMBER'), body=msgText)
  if m.email:
    email = sendgrid.Mail()
    email.add_to(m.email)
    email.set_subject('Love Message from %s' % (m.sender))
    email.set_text(msgText)
    email.set_html(msgText)
    email.set_from('aecc.upr@gmail.com')
    sg.send(email)

