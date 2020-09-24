# -*- coding: utf-8 -*-
import requests
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class SendGripHelper(object):
    api_key = settings.SENDGRID_KEY

    def send_simple_email(self, *args, **kwargs):
        if isinstance(kwargs.get('to_email'), str):
            to_addresses = []
            to_addresses.append(kwargs.get('to_email'))
        else:
            to_addresses = kwargs.get('to_email')
        for address in to_addresses:
            message = Mail(
                from_email=kwargs.get('from_email'),
                to_emails=address,
                subject=kwargs.get('subject'),
                html_content=kwargs.get('body'))
            try:
                sg = SendGridAPIClient(self.api_key)
                response = sg.send(message)
            except Exception as e:
                print(e)
