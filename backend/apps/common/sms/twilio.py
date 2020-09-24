# -*- coding: utf-8 -*-
import logging

from common.exceptions import SMSServiceDown
from django.conf import settings
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

logger = logging.getLogger(__name__)


class TwilioHelper:

    client = None
    is_active = False

    def __init__(self):
        self.is_active = settings.TWILIO_ACTIVE
        if not self.is_active:
            return
        try:
            self.client = Client(
                settings.TWILIO_ACCOUNT_SID,
                settings.TWILIO_AUTH_TOKEN
            )
        except TwilioRestException as error:
            logger.error(error)
            raise SMSServiceDown('SMS Service Provider failed')

    def send_sms(self, to, body):
        if self.is_active:
            message = None
            try:
                message = self.client.messages.create(
                    to=to,
                    from_=settings.TWILIO_NUMBER,
                    body=body
                )
            except TwilioRestException as error:
                logger.error(error)
            finally:
                if not message:
                    message = self.client.messages.create(
                        to=to,
                        from_=settings.TWILIO_NUMBER,
                        body=body
                    )
                return message

        logger.warning('TWILIO is disabled')
        return None
