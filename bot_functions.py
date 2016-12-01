#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import string
import random

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


class BotFunctions(object):
    @staticmethod
    def id_generator(size=24, chars=string.ascii_uppercase + string.digits):
        """
        Generate a random string

        Source: http://stackoverflow.com/a/2257449
                and http://stackoverflow.com/a/23728630/2213647

        :param size:    the length of the random string (default: 24)
        :param chars:   the characters to we are using to generate the string
                        (default: all ASCII uppercase characters and all digits)
        :returns:       the randomly generated string
        """

        return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

    @staticmethod
    def get_local_json_contents(json_filename):
        """
        Return the contents of a (local) JSON file

        :param json_filename: the filename (as a string) of the local JSON file
        :returns: the data of the JSON file
        """

        try:
            with open(json_filename) as json_file:
                try:
                    data = json.load(json_file)
                except ValueError:
                    print("Contents of '" + json_filename + "' are not valid JSON")
                    raise
        except IOError:
            print("An error occurred while reading the '" + json_filename + "'")
            raise

        return data

    @staticmethod
    def get_remote_json_contents(json_url):
        """
        Return the contents of a (remote) JSON file

        :param json_url: the url (as a string) of the remote JSON file
        :returns: the data of the JSON file
        """

        data = None
        req = Request(json_url)

        try:
            response = urlopen(req).read()
        except HTTPError as e:
            print("HTTPError " + str(e.code))
        except URLError as e:
            print("URLError " + str(e.reason))
        else:
            try:
                data = json.loads(response.decode("utf-8"))
            except ValueError:
                print("Invalid JSON contents")

        return data
