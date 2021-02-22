#!/usr/bin/env python3
"""Module that defines the Person class"""

import unidecode

class Person:
    def __init__(self, first_name: str, last_name: str, email: dict, phone: dict, birthday: str):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.birthday = birthday

    def get_name(self):
        return self.first_name + " " + self.last_name

    def get_unaccented_name(self):
        return unidecode.unidecode(self.get_name())
