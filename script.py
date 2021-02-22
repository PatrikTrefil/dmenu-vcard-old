#!/usr/bin/env python3
"""Dmenu script for getting information about contacts from vcard files"""

import os
import subprocess
import person
from vcards import *
from utils import *

PATH = f"{os.getenv('HOME')}/.contacts/contacts/"

# user chooses what he wants to know
query = subprocess.run(["dmenu", "-i", "-p", "Query:"], input=b"phone\nemail\nbirthday",
                       stdout=subprocess.PIPE, check=True).stdout.decode("UTF-8")[:-1]
if query == "":
    exit(1)


# get the list of files
files = [f"{PATH}{item}" for item in os.listdir(PATH)]

# list of all people using the Person class
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
