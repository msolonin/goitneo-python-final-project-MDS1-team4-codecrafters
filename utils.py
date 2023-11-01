# -*- coding: utf-8 -*-
"""
Utils, functions, classes for use it in main.py
"""
import pickle
from datetime import datetime
from collections import UserDict


def input_error(func):
    """Common wrapper for intercept all exceptions
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError:
            return "Please use correct number of arguments"
        except KeyError:
            return "Name is not present in address book"
        except AttributeError:
            return "Could not show, list of birthdays empty"
        except ValueError:
            return "Please add command"
        except Exception:
            print(f"Unexpected action: in def {func.__name__}()")
    return wrapper


class Pickle:

    NOTES = 'notes.pickle'
    CONTACTS = 'contacts.pickle'

    @staticmethod
    def save_to_file(file_name, data):
        with open(file_name, "wb") as _file:
            pickle.dump(data, _file)

    @staticmethod
    def read_from_file(file_name):
        with open(file_name, "rb") as _file:
            content = pickle.load(_file)
        return content

    def save_notes(self, data):
        self.save_to_file(self.NOTES, data)

    def read_notes(self):
        try:
            return self.read_from_file(self.NOTES)
        except FileNotFoundError:
            return Notes()  # TODO: Class not exist, change name if it will be different name

    def save_contacts(self, data):
        self.save_to_file(self.CONTACTS, data)

    def read_contacts(self):
        try:
            return self.read_from_file(self.CONTACTS)
        except FileNotFoundError:
            return AddressBook()


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    pass


class AddressBook(UserDict):
    pass


class Address(Field):
    pass


class Birthday(Field):

    date_format = "%d.%m.%Y"

    @property
    def date_object(self):
        return self.convert_date(self.value)

    @staticmethod
    def convert_date(date: str):
        try:
            return datetime.strptime(date, Birthday.date_format).date()
        except Exception:
            return None
        

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phone = None
        self.birthday = None
        self.address = None

    def add_phone(self, phone: str):
        """ Method for add phone
        :param phone: phone in format +3***, or 323***
        """
        self.phone = Phone(phone)

    def add_birthday(self, birthday: str):
        """ Automatically convert it in datetime format
        :param birthday: Birthday date of user
        :type birthday: format str DD.MM.YYYY
        """
        self.birthday = Birthday(birthday)

    def add_address(self, address: str):
        self.address = Address(address)

    def edit_phone(self, phone: str):
        """ Method for edit phone number
        :param phone: phone in format +3***, or 323***
        """
        self.add_phone(phone)

    def edit_address(self, address: str):
        self.add_address(address)

    def get_phone(self):
        """ getter for phone number
        :return: phone number
        :rtype: str
        """
        return self.phone.value

    def get_birthday(self):
        """ getter for birthday
        :return: birthday in format %d.%m.%Y
        :rtype: str
        """
        return self.birthday.value
    
    def get_address(self):
        return self.address.value

    def __str__(self):
        birthday = ''
        if self.birthday:
            birthday = f" birthday: {str(self.birthday)}, "
        return f"Contact name: {self.name.value},{birthday} phone: {self.phone}"
