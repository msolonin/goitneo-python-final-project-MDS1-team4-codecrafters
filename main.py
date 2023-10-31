# -*- coding: utf-8 -*-
"""
Console Bot helper.
For works with Address book
"""
import re
import calendar
from datetime import datetime
from utils import input_error
from utils import Birthday
from utils import AddressBook
from utils import Record

TELEPHONE_NUMBER_LEN = 10


@input_error
def find(contacts, name: str):
    """ getter for get object Record from dict by name
    :param contacts: contacts object
    :param name: name of user
    :type name: str
    :return: Record object
    :rtype: object
    """
    return contacts.get(name)


@input_error
def delete(contacts, name: str):
    """ Method for delete Record
    :param contacts: contacts object
    :param name: name of user
    :type name:str
    :return: Record
    :rtype: object
    """
    return contacts.pop(name)


def _get_phone_number(phone: str):
    """ Static method for get phone number if it have 10 digits, or none if not
    :param phone: phone number
    :type phone: str
    :return: phone number or None
    :rtype: str or None
    """
    _phone = re.findall(r"[\+\(]?[1-9]", phone)
    _len = len(_phone)
    if _len == TELEPHONE_NUMBER_LEN:
        return ''.join(_phone)
    else:
        return None


@input_error
def add_phone(contacts, name: str, phone: str):
    """ Method for add new contact in address book
    :param contacts: contacts object
    :param name: name of contact
    :type name: str
    :param phone: phone number
    :type phone: str
    :return: String for print in cmd
    :rtype: str
    """
    _phone = _get_phone_number(phone)
    if _phone:
        phone = ''.join(_phone)
        record = Record(name)
        record.add_phone(phone)
        contacts.update(**{record.name.value: record})
        return f"Contact: {name} : {phone} added"
    else:
        return f"Phone: {phone} is not correct it should contain 10 digits"


@input_error
def change_phone(contacts, name: str, phone: str):
    """ Method for change phone number
    :param contacts: contacts object
    :param name: Contact name
    :type name: str
    :param phone: new phone number
    :type phone: str
    :return: String for print in cmd
    :rtype: str
    """
    _phone = _get_phone_number(phone)
    if _phone:
        contacts.data[name].edit_phone(phone)
        return f"Contact: {name} : {phone} changed"
    else:
        return f"Phone: {phone} is not correct it should contain 10 digits"


@input_error
def get_phone(contacts, name: str):
    """ Method get phone from contact
    :param contacts: contacts object
    :param name: name of contact
    :type name: str
    :return: phone number
    :rtype: str
    """
    return contacts.data[name].phone


def get_all(contacts):
    """ Method for get all contacts with all info
    :param contacts: contacts object
    :return: All contacts info
    :rtype: str
    """
    if contacts.data:
        return '\n'.join([f"{v}" for k, v in contacts.data.items()])
    else:
        return "Data is empty, nothing to show"


@input_error
def add_birthday(contacts, name: str, birthday_date: str):
    """ Method for add birthday in address book
    :param contacts: contacts object
    :param name: name of contact
    :type name: str
    :param birthday_date: birthdate of contact in %d.%m.%Y format
    :type birthday_date: str
    :return: Answer in cmd
    :rtype: str
    """
    result = Birthday.convert_date(birthday_date)
    if result:
        contacts.data[name].add_birthday(birthday_date)
        return f"Birthday for {name} : {birthday_date} added"
    else:
        return f"Please use correct date format {Birthday.date_format}, instead of {birthday_date}"


@input_error
def show_birthday(contacts, name: str):
    """ Method for show birthday of contact
    :param contacts: contacts object
    :param name: name of contact
    :type name: str
    :return: birthday of contact
    :rtype: str
    """
    return contacts.data[name].get_birthday()


@input_error
def birthdays(contacts):
    """ Method for show all birthdays in nearest 7 days if exist
    :return: list of birthdays by days for cmd representation
    :rtype: str
    """
    days_in_week = 7
    result = {}
    today = datetime.today().date()
    if contacts.data:
        for user in contacts.data.values():
            name = user.name
            birthday = user.birthday.date_object
            birthday_this_year = birthday.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)
            else:
                birthday_this_year = birthday_this_year.replace(year=today.year)
            delta_days = (birthday_this_year - today).days
            if delta_days < days_in_week:
                weekday = birthday_this_year.weekday()
                day_name = calendar.day_name[weekday]
                if weekday in [5, 6]:
                    day_name = calendar.day_name[0]
                if day_name in result:
                    result[day_name] = result[day_name] + ', ' + name
                else:
                    result[day_name] = name
        week_days = [calendar.day_name[_] for _ in range(days_in_week)]
        print_result = []
        for weekday in week_days:
            if weekday in result:
                print_result.append("{}: {}".format(weekday, result[weekday]))
        if print_result:
            return "\n".join(print_result)
        else:
            return "No birthdays on next week"
    else:
        return "Empty birthday list"


@input_error
def parse_input(user_input):
    """ Method for parse cmd input
    :param user_input:
    :type user_input:
    :return: cmd command for execution, *args for continue usage in methods,
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def main():
    """ Main method for execution, start point
    """
    contacts = AddressBook()
    print("""Welcome to the assistant bot!
    Available commands:
        ° hello
        ° add <name> <phone number>
        ° change <name> <new phone number>
        ° phone <name>
        ° all
        ° add-birthday <name> <birthday(in format DD.MM.YYYY)>
        ° show-birthday <name>        
        ° birthdays
        ° close/exit""")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_phone(contacts, *args))
        elif command == "change":
            print(change_phone(contacts, *args))
        elif command == "phone":
            print(get_phone(contacts, *args))
        elif command == "all":
            print(get_all(contacts))
        elif command == "add-birthday":
            print(add_birthday(contacts, *args))
        elif command == "show-birthday":
            print(show_birthday(contacts, *args))
        elif command == "birthdays":
            print(birthdays(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
