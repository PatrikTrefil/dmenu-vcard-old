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


def get_all_fields(field: str, text: str) -> list:
    """parse information about a contact into dictionary where keys are types"""
    REGEX = re.compile(field + ".*:(.*)$", re.MULTILINE)
    res = re.finditer(REGEX, text)
    d = {}
    for item in res:
        match = re.search(r"TYPE=\"*(.*?)\"*(?=;)", item.group(0))
        try:
            item_type = match.group(1)
            d[item_type] = item.group(1)
        except:
            pass
    return d


def get_formatted_name(text: str) -> str:
    return get_field(r"^FN", text)


def get_name(text: str) -> str:
    return get_field(r"^N", text)


def parse_name(unformatted_name: str) -> dict:
    """get dict from an unformatted name"""
    l = unformatted_name[2:].split(";")
    return {"first name": l[1], "last name": l[0], "middle name": l[2], "honorific prefixes": l[3], "honorific suffixes": l[4]}


def get_email(text: str) -> dict:
    res = get_all_fields("^EMAIL", text)
    return res


def get_phone(text: str) -> str:
    res = get_all_fields("TEL", text)
    for key in res.keys():
        res[key] = res[key].replace(" ", "")
    return res


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
