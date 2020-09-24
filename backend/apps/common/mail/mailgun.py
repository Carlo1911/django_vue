# -*- coding: utf-8 -*-
import requests
from django.conf import settings
from django.template.loader import get_template


class MailGunHelper(object):
    base_url = settings.MAILGUN_DOMAIN
    api_key = settings.MAILGUN_KEY

    def _render_destination(self, to_email):
        if isinstance(to_email, str):
            to_addresses = [to_email]
        else:
            to_addresses = to_email
        return to_addresses

    def send_simple_email(self, *args, **kwargs):
        return requests.post(
            f'{self.base_url}/messages',
            auth=('api', self.api_key),
            data={'from': kwargs.get('from_email'),
                  'to': self._render_destination(kwargs.get('to_email')),
                  'subject': kwargs.get('subject'),
                  'text': kwargs.get('body')})

    def send_html_email(self, *args, **kwargs):
        return requests.post(
            f'{self.base_url}/messages',
            auth=('api', self.api_key),
            data={'from': kwargs.get('from_email'),
                  'to': self._render_destination(kwargs.get('to_email')),
                  'subject': kwargs.get('subject'),
                  'text': kwargs.get('body'),
                  'html': get_template(kwargs.get('template')).render(kwargs.get('data'))}
        )

    def validate_email(self, email):
        return requests.get(
            'https://api.mailgun.net/v4/address/validate',
            auth=('api', self.api_key),
            params={'address': email}
        )
