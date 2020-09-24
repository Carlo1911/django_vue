# -*- coding: utf-8 -*-
from django.conf import settings

from .tasks import send_mailgun_email as email
from .tasks import send_mailgun_html_email as html_email


def send_email(from_email, to_email, subject, body):
    if not settings.SEND_EMAILS:
        print('Activate SEND_EMAILS var in settings to send transactional emails')
        return
    email.delay(from_email, to_email, subject, body)


def send_html_email(from_email, to_email, subject, body, template, data):
    if not settings.SEND_EMAILS:
        print('Activate SEND_EMAILS var in settings to send transactional emails')
        return
    html_email.delay(from_email, to_email, subject, body, template, data)
