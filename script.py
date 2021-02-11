#!/usr/bin/env python3

import re
import os
import subprocess
import argparse
import person

PATH = f"{os.getenv('HOME')}/.contacts/contacts/"

# user chooses what he wants to know
query = subprocess.run(["dmenu", "-i", "-p", "Query:"], input=b"phone\nemail\nbirthday",
                       stdout=subprocess.PIPE, check=True).stdout.decode("UTF-8")[:-1]
if query == "":
    exit(1)


def notify(text: str, time="8000") -> str:
    subprocess.run(["notify-send", "-t", time, text])


def get_field(field: str, text: str) -> str:
    """get information after last semicolon"""
    REGEX = re.compile(field + ".*:(.*)", re.MULTILINE)
    res = re.search(REGEX, text)
    try:
        return res.group(0)
    except AttributeError:
        return ""


def copy_to_clipboard(text: str) -> None:
    subprocess.run(["xclip", "-selection", "clipboard"],
                   input=text.encode("UTF-8"))


def get_formatted_name(text: str) -> str:
    return get_field("FN", text)


def get_name(text: str) -> str:
    return get_field(r"^N", text)


def parse_name(unformatted_name: str) -> dict:
    l = unformatted_name[2:].split(";")
    return {"first name": l[1], "last name": l[0]}


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


files = [f"{PATH}{item}" for item in os.listdir(PATH)]

people = []

for file in files:
    with open(file, "r") as curr:
        content = curr.read()
        name = parse_name(get_name(content))
        phone = get_phone(content)
        email = get_email(content)
        birthday = get_birthday(content)
    people += [person.Person(name["first name"],
                             name["last name"], email, phone, birthday)]

names = [person.get_unaccented_name() for person in people]
selected = subprocess.run(
    ["dmenu", "-i", "-p", "Choose person: "], input="\n".join(names).encode("UTF-8"), stdout=subprocess.PIPE, check=True)

selected = selected.stdout.decode("UTF-8")[:-1]


for person in people:
    if person.get_unaccented_name() == selected:
        if query == "email":
            if person.email != "":
                print(person.email)
                copy_to_clipboard(person.email)
            else:
                print("No information about this contact")
                notify("No information about this contact")

        elif query == "phone":
            if person.phone != "":
                print(person.phone)
                copy_to_clipboard(person.phone)
            else:
                print("No information about this contact")
                notify("No information about this contact")
        elif query == "birthday":
            if person.birthday != "":
                print(person.birthday)
                text = f"{person.get_name()} has birthday on {person.birthday}."
                notify(text)
            else:
                print("No information about this contact")
                notify("No information about this contact")
        break
