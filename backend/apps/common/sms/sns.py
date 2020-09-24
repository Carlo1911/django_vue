# -*- coding: utf-8 -*-
import logging

import boto3
from botocore.exceptions import ClientError
from common.exceptions import SMSServiceDown
from django.conf import settings

logger = logging.getLogger(__name__)


class SNSHelper:

    client = None
    is_active = False

    def __init__(self):
        self.is_active = settings.AWS_SNS_ACTIVE
        if not self.is_active:
            return
        try:
            self.client = boto3.client(
                'sns',
                aws_access_key_id=settings.AWS_SNS_ACCESS_KEY,
                aws_secret_access_key=settings.AWS_SNS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_SNS_REGION,
            )
        except ClientError as error:
            logger.error(error)
            raise SMSServiceDown('SMS Service Provider failed')

    def send_sms(self, to, body):
        if self.is_active:
            message = None
            try:
                message = self.client.publish(
                    PhoneNumber=to,
                    Message=body,
                )
                return message
            except ClientError as error:
                logger.error(error)
            finally:
                if not message:
                    message = self.client.publish(
                        PhoneNumber=to,
                        Message=body,
                    )
                return message

        logger.warning('AWS SNS is disabled')
        return None
