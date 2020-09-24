# -*- coding: utf-8 -*-
try:
    from config.celery_worker import app
except:
    from config.celery_settings import app

from .mailgun import MailGunHelper
from .sgrip import SendGripHelper


@app.task(name='email_mg_task')
def send_mailgun_email(from_email, to_email, subject, body):
    mghelper = MailGunHelper()
    mghelper.send_simple_email(
        from_email=from_email,
        to_email=to_email,
        subject=subject,
        body=body,
    )


@app.task(name='email_sg_task')
def send_sendgrip_email(from_email, to_email, subject, body):
    sghelper = SendGripHelper()
    sghelper.send_simple_email(
        from_email=from_email,
        to_email=to_email,
        subject=subject,
        body=body,
    )


@app.task(name='html_email_mg_task')
def send_mailgun_html_email(from_email, to_email, subject, body, template, data):
    mghelper = MailGunHelper()
    mghelper.send_html_email(
        from_email=from_email,
        to_email=to_email,
        subject=subject,
        body=body,
        template=template,
        data=data,
    )
