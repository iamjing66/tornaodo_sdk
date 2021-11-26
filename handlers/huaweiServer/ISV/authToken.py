#!/usr/bin/env python
# coding=utf-8

import Global
import base64
import hmac


def generateResponseBodySignature(key, body):
    #return base_64(hmacSHA256(key, body))
    pass


def hmacSHA256(data, secret):

    secrets = secret.encode('utf-8')
    message = data.encode('utf-8')
    sign = base64.b64encode(hmac.new(secrets, message, digestmod="sha256").digest())

