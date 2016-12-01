#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from bot_functions import BotFunctions


data = None


class ExternalData(object):
    def __init__(self):
        cd = os.path.join(os.getcwd(), os.path.dirname(__file__))
        __location__ = os.path.realpath(cd)

        self.credentials = BotFunctions.get_local_json_contents(os.path.join(__location__, "credentials.json"))


def init():
    global data
    data = ExternalData()
