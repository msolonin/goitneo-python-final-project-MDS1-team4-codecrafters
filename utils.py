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


class Email(Field):
    pass


class Birthday(Field):

    date_format = "%d.%m.%Y"

    @property
    def date_object(self):
        """ Getter for date
        """
        return self.convert_date(self.value)

    @staticmethod
    def convert_date(date: str):
        """ Method for convert date in date object
        :param date: date in %d.%m.%Y format
        :type date: str
        :return: date object
        :rtype: datetime
        """
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
        self.email = None

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
        """ Add address
        :param address: Address in free format
        :type address: str
        """
        self.address = Address(address)

    def add_email(self, email: str):
        """ Add email
        :param email: Email in format xxx@xxx.xxx
        :type email: str

        """
        self.email = Email(email)

    def edit_phone(self, phone: str):
        """ Method for edit phone number
        :param phone: phone in format +3***, or 323***
        """
        self.add_phone(phone)

    def edit_address(self, address: str):
        """ Method for edit address
        :param address: Edit address in free format
        :type address: str
        """
        self.add_address(address)

    def edit_email(self, email: str):
        """ Method for edit email
        :param email:  Email in format xxx@xxx.xxx
        :type email: str
        """
        self.add_email(email)

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
        """ Method for get Record address
        :return: Current contact address
        :rtype: str
        """
        return self.address.value
    
    def get_email(self):
        """ Method for get current Record email
        :return: Current contact email
        :rtype: str
        """
        return self.email.value

    def __str__(self):
        """ Str representation of Record
        :return: Str representation
        :rtype: str
        """
        birthday = ''
        if self.birthday:
            birthday = f" birthday: {str(self.birthday)}, "
        return f"Contact name: {self.name.value},{birthday} phone: {self.phone}"


class Notes(UserDict):
    def add_note(self, name, text):
        self.data[name] = {"text": text, "tags": []}

    def add_tags(self, name, tags):
        self.data[name]["tags"] += tags.split(" ")

    def find_note(self, name):
        if name in self.data:
            return f"Note`s name: {name},\ntags: {' '.join(t for t in self.data[name]['tags'])};\ntext: {self.data[name]['text']}"

    def delete_note(self, name):
        if name in self.data:
            del self.data[name]
            return True
        else:
            return False

    def edit_note(self, name, new_text):
        if name in self.data:
            self.data[name]["text"] = new_text
            return True
        else:
            return False

    def find_notes_by_tag(self, tag):
        matching_notes = dict()
        for name, data in self.data.items():
            tags = data["tags"]
            if tag in tags:
                matching_notes[name] = data
        return matching_notes

    def sort_notes(self):
        sorted_notes = sorted(
            self.data.items(), key=lambda item: (-len(item[1]["tags"]), item[0])
        )
        return dict(sorted_notes)
    

class Pickle:

    NOTES = 'notes.pickle'
    CONTACTS = 'contacts.pickle'

    @staticmethod
    def save_to_file(file_name, data):
        """ Method for save pickled data in file
        :param file_name: name of file
        :type file_name: str
        :param data: any kind of data
        :type data: any
        """
        with open(file_name, "wb") as _file:
            pickle.dump(data, _file)

    @staticmethod
    def read_from_file(file_name):
        """ Method for read data from file
        :param file_name: name of file
        :type file_name: str
        :return: data
        :rtype: any
        """
        with open(file_name, "rb") as _file:
            content = pickle.load(_file)
        return content

    def save_notes(self, data):
        """ Method for save notes
        """
        self.save_to_file(self.NOTES, data)

    def read_notes(self):
        """ Method for read notes
        """
        try:
            return self.read_from_file(self.NOTES)
        except FileNotFoundError:
            return Notes()  # TODO: Class not exist, change name if it will be different name

    def save_contacts(self, data):
        """ Method for save contacts
        """
        self.save_to_file(self.CONTACTS, data)

    def read_contacts(self):
        """ Method for read notes
        """
        try:
            return self.read_from_file(self.CONTACTS)
        except FileNotFoundError:
            return AddressBook()


class CommandCompleter:

    def __init__(self, options):
        self.options = sorted(options)
        self.matches = []

    def complete(self, text, state):
        """ Method for autocomplete
        """
        response = None
        if state == 0:
            if text:
                self.matches = [_ for _ in self.options if _ and _.startswith(text)]
            else:
                self.matches = self.options[:]
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response


class Commands:
    ADD = 'add'
    CHANGE = 'change'
    PHONE = 'phone'
    ALL = 'all'
    ADD_BIRTHDAY = 'add-birthday'
    SHOW_BIRTHDAY = 'show-birthday'
    BIRTHDAYS = 'birthdays'
    ADD_ADDRESS = 'add-address'
    SHOW_ADDRESS = 'show-address'
    CHANGE_ADDRESS = 'change-address'
    ADD_EMAIL = 'add-email'
    SHOW_EMAIL = 'show-email'
    CHANGE_EMAIL = 'change-email'
    CLOSE = 'close'
    EXIT = 'exit'
    HELLO = 'hello'
    ADD_NOTE = "add-note"
    ADD_TAGS = "add-tags"
    FIND_NOTE = "find-note"
    DELETE_NOTE = "delete-note"
    EDIT_NOTE = "edit-note"
    FIND_NOTES_BY_TAGS = "find-by-tag"
    SORT_NOTES = "show-sorted-notes"

    @classmethod
    def all_keys(cls):
        """ Show list of all names of variables in Class
        :return: names
        :rtype: list
        """
        return [_ for _ in dir(Commands) if not _.startswith('_') and _.isupper()]

    @classmethod
    def all_values(cls):
        """ Show list of all values of variables in Class
        :return: values
        :rtype: list
        """
        return [getattr(cls, _) for _ in cls.all_keys()]
