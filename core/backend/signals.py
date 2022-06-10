from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Account
from core.settings import EMAIL_HOST_USER, EMAIL_RECIEVER, SMS_RECIEVER, ARKESEL_KEY, ARKESEL_SENDER_ID
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import requests


#         msg.send()
# @receiver(post_save, sender=Account)
def send_email(sender, instance, created, **kwargs):
    '''Notify admin if a new account is created'''
    if created:
        subject = 'JAMILAHOME NOTIFICATION'
        html_template = 'backend/notification/notification_mail.html'
        to_mail = EMAIL_RECIEVER
        from_mail = EMAIL_HOST_USER
        context = {
            'Email': instance.email,
            'Name': instance.name,
            'Date': instance.date_created,
        }
        html_text = render_to_string(html_template, context)
        msg = EmailMultiAlternatives(
            subject, html_text, from_mail, [to_mail])
        msg.attach_alternative(html_text, "text/html")
        try:
            msg.send()
        except Exception as e:
            print(e)


# @receiver(post_save, sender=Account)
def send_sms(sender, instance, created, **kwargs):
    '''Notify admin if a new account is created'''
    if created:
        url = 'http://api.arkesel.com/sms/send'
        # PAYLOAD FOR USER
        data = {
            'key': ARKESEL_KEY,
            'sender': ARKESEL_SENDER_ID,
            'recipient': instance.phone,
            'message': 'Welcome to JAMILAHOME, {}'.format(instance.name),
            'dlr': '1',
        }
        # PAYLOAD FOR ADMIN
        data_2 = {
            'key': ARKESEL_KEY,
            'sender': ARKESEL_SENDER_ID,
            'recipient': SMS_RECIEVER,
            'message': f'Hi, a new user has registered on Jamilahome. Username: {instance.name}',
            'dlr': '1',
        }
        try:
            response = requests.post(url, data=data)
        except Exception as err:
            print(err)  # to user
        try:
            response = requests.post(url, data=data_2)  # to admin
        except Exception as err:
            print(err)
