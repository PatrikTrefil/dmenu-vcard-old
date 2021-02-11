#!/usr/bin/env python3

import re
import os
import subprocess
import argparse


# user chooses what he wants to know
query = subprocess.run(["dmenu", "-i", "-p", "Query:"], input=b"phone\nemail\nbirthday",
                       stdout=subprocess.PIPE).stdout.decode("UTF-8")[:-1]
if query == "":
    exit(1)


class Person:
    def __init__(self, first_name, last_name, email, phone, birthday):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.birthday = birthday

    def get_name(self):
        return self.first_name + " " + self.last_name


def get_field(field: str, text: str) -> str:
    REGEX = re.compile(field + ".*:(.*)", re.MULTILINE)
    res = re.search(REGEX, text)
    try:
        return res.group(0)
    except AttributeError:
        return ""


def get_formatted_name(text: str) -> str:
    return get_field("FN", text)


def get_name(text: str) -> str:
    return get_field(r"^N", text)


def parse_name(unformatted_name: str) -> list:
    l = unformatted_name[2:].split(";")
    return l


def get_email(text: str) -> str:
    line = get_field("EMAIL", text)
    res = re.search(r":(.*?$)", line)
    try:
        return res.group(1)
    except AttributeError:
        return ""


def get_phone(text: str) -> str:
    line = get_field("TEL", text)
    res = re.search(r":(.*?$)", line)
    try:
        return res.group(1).replace(" ", "")
    except AttributeError:
        return ""


def get_birthday(text: str) -> str:
    line = get_field("BDAY", text)
    res = re.search(r":(.*?$)", line)
    try:
        month = res.group(1)[4:6]
        day = res.group(1)[6:8]
        year = res.group(1)[:4]
        return f"{day}.{month}.{year}"
    except AttributeError:
        return ""


files = os.listdir(f"{os.getenv('HOME')}/.contacts/contacts/")
files = [f"{os.getenv('HOME')}/.contacts/contacts/{item}" for item in files]

people = []
for file in files:
    with open(file, "r") as curr:
        content = curr.read()
        name = parse_name(get_name(content))
        phone = get_phone(content)
        email = get_email(content)
        birthday = get_birthday(content)
    people += [Person(name[1], name[0], email, phone, birthday)]

names = [person.first_name + " " + person.last_name for person in people]
selected = subprocess.run(
    ["dmenu", "-i"], input="\n".join(names).encode("UTF-8"), stdout=subprocess.PIPE)

selected = selected.stdout.decode("UTF-8")[:-1]


for person in people:
    if person.get_name() == selected:
        if query == "email":
            print(person.email)
            subprocess.run(["xclip", "-selection", "clipboard"],
                           input=person.email.encode("UTF-8"))
        elif query == "phone":
            print(person.phone)
            subprocess.run(["xclip", "-selection", "clipboard"],
                           input=person.phone.encode("UTF-8"))
        elif query == "birthday":
            text = f"{person.get_name()} has birthday on {person.birthday}."
            subprocess.run(["notify-send", "-t", "8000", text])
        break
