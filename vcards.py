#!/usr/bin/env python3
"""Simple module for working with vcard files"""

import re


def get_field(field: str, text: str) -> str:
    """get information after last semicolon"""
    REGEX = re.compile(field + ".*:(.*)", re.MULTILINE)
    res = re.search(REGEX, text)
    try:
        return res.group(0)
    except AttributeError:
        return ""


def get_formatted_name(text: str) -> str:
    return get_field(r"^FN", text)


def get_name(text: str) -> str:
    return get_field(r"^N", text)


def parse_name(unformatted_name: str) -> dict:
    l = unformatted_name[2:].split(";")
    return {"first name": l[1], "last name": l[0]}


def get_email(text: str) -> str:
    line = get_field("^EMAIL", text)
    res = re.search(r":(.*?$)", line)
    try:
        return res.group(1)
    except AttributeError:
        return ""


def get_phone(text: str) -> str:
    line = get_field("^TEL", text)
    res = re.search(r":(.*?$)", line)
    try:
        return res.group(1).replace(" ", "")
    except AttributeError:
        return ""


def get_birthday(text: str) -> str:
    line = get_field("^BDAY", text)
    res = re.search(r":(.*?$)", line)
    try:
        month = res.group(1)[4:6]
        day = res.group(1)[6:8]
        year = res.group(1)[:4]
        return f"{day}.{month}.{year}"
    except AttributeError:
        return ""
