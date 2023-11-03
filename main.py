# -*- coding: utf-8 -*-
"""
Console Bot helper.
For works with Address book
"""
import re
import calendar
import readline
from datetime import datetime, timedelta
from utils import input_error
from utils import Birthday
from utils import Record
from utils import Pickle
from utils import CommandCompleter
from utils import Commands
from utils import AddressBook
from utils import Notes

TELEPHONE_NUMBER_LEN = 10
EMAIL_MAX_LEN = 50
FINDER_INPUT_LEN = 3

pickle = Pickle()


@input_error
def find_contact(contacts: AddressBook, user_input: str):
    """ User search
    :param contacts: contacts object
    :type contacts: str
    :param user_input: input which user enters to look for a contact
    :type user_input: str
    :return: str with search result
    :rtype: str
    """
    list_of_users = []

    if len(user_input) >= FINDER_INPUT_LEN:
        for user_name, record in contacts.items():
            user_info = f"Contact name: {user_name}"
            user_info += f", {record.birthday.value}" if hasattr(
                record, 'birthday') and record.birthday is not None else ""
            user_info += f", phone: {record.phone.value}" if hasattr(
                record, 'phone') and record.phone is not None else ""
            user_info += f", address: {record.address.value}" if hasattr(
                record, 'address') and record.address is not None else ""
            if user_input.lower() in user_info.lower():
                list_of_users.append(user_info)
            else:
                continue
    else:
        return f"Enter {str(FINDER_INPUT_LEN)} and more characters."

    if list_of_users:
        final_list = '\n'.join(list_of_users)
        return final_list
    else:
        return "Match not found"


@input_error
def delete(contacts: AddressBook, name: str):
    """ Method for delete Record
    :param contacts: contacts object
    :param name: name of user
    :type name:str
    :return: Record
    :rtype: object
    """
    deleted_contact = contacts.pop(name)
    pickle.save_contacts(contacts)
    return f"{deleted_contact} deleted."


def _get_phone_number(phone: str):
    """ Static method for get phone number if it have 10 digits, or none if not
    :param phone: phone number
    :type phone: str
    :return: phone number or None
    :rtype: str or None
    """
    _phone = re.findall(r"[\+\(]?\d", phone)
    _len = len(_phone)
    if _len == TELEPHONE_NUMBER_LEN:
        return ''.join(_phone)
    else:
        return None
    

def _get_valid_email(email: str):
    _email = re.findall(r"[A-Za-z0-9!#$%&'r;+-.=?^^_`{}½~]+@[A-Za-z0-9]+(\.[A-Za-z]{2,})+", email)
    _len = len(email)
    if _len <= EMAIL_MAX_LEN:
        return ''.join(_email)
    else:
        return None


@input_error
def add_phone(contacts: AddressBook, name: str, phone: str):
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
        pickle.save_contacts(contacts)
        return f"Contact: {name} : {phone} added"
    else:
        return f"Phone: {phone} is not correct it should contain {str(TELEPHONE_NUMBER_LEN)} digits"


@input_error
def change_phone(contacts: AddressBook, name: str, phone: str):
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
        pickle.save_contacts(contacts)
        return f"Contact: {name} : {phone} changed"
    else:
        return f"Phone: {phone} is not correct it should contain 10 digits"


@input_error
def get_phone(contacts: AddressBook, name: str):
    """ Method get phone from contact
    :param contacts: contacts object
    :param name: name of contact
    :type name: str
    :return: phone number
    :rtype: str
    """
    return contacts.data[name].phone


def get_all(contacts: AddressBook):
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
def add_address(contacts: AddressBook, name: str, *args):
    """ Method for add Address
    :param contacts: Record
    :type contacts: class
    :param name: record name
    :type name: str
    :return: Representation string of add
    :rtype: str
    """
    address = ' '.join(args)
    contacts.data[name].add_address(address)
    pickle.save_contacts(contacts)
    return f"Address for {name} : {address} added"


@input_error
def get_address(contacts: AddressBook, name: str):
    """ Method for get address
    :param contacts: Record
    :type contacts: class
    :param name: record name
    :type name: str
    :return: Contact address
    :rtype: str
    """
    return contacts[name].get_address()


@input_error
def change_address(contacts: AddressBook, name: str, *args):
    """ Method for Change address
    :param contacts: Record
    :type contacts: class
    :param name: record name
    :type name: str
    :return: Representation string for change
    :rtype: str
    """
    address = ' '.join(args)
    contacts.data[name].add_address(address)
    pickle.save_contacts(contacts)
    return f"Address for {name} : {address} changed"


@input_error
def add_email(contacts: AddressBook, name: str, email: str):
    """ Method for add Email
    :param contacts: Record
    :type contacts: class
    :param name: record name
    :type name: str
    :param email: email of contact
    :type email: str
    :return: Representation string for add email
    :rtype: str
    """
    _email = _get_valid_email(email)
    if _email:
        contacts.data[name].add_email(email)
        pickle.save_contacts(contacts)
        return f"Email for: {name} : {email} added"
    else:
        return f"Email: {email} is not correct"


@input_error
def change_email(contacts: AddressBook, name: str, email: str):
    """ Method for change Email
    :param contacts: Record
    :type contacts: class
    :param name: record name
    :type name: str
    :param email: email of contact
    :type email: str
    :return: Representation string for change email
    :rtype: str
    """
    _email = _get_valid_email(email)
    if _email:
        contacts.data[name].edit_email(email)
        pickle.save_contacts(contacts)
        return f"Email for: {name} : {email} changed"
    else:
        return f"Email: {email} is not correct"


@input_error
def get_email(contacts: AddressBook, name: str):
    """ Method for get Email from contact
    :param contacts: Record
    :type contacts: class
    :param name: record name
    :type name: str
    :return: Representation string of contact email
    :rtype: str
    """
    return contacts[name].get_email()


@input_error
def add_birthday(contacts: AddressBook, name: str, birthday_date: str):
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
        pickle.save_contacts(contacts)
        return f"Birthday for {name} : {birthday_date} added"
    else:
        return f"Please use correct date format {Birthday.date_format}, instead of {birthday_date}"


@input_error
def show_birthday(contacts: AddressBook, name: str):
    """ Method for show birthday of contact
    :param contacts: contacts object
    :param name: name of contact
    :type name: str
    :return: birthday of contact
    :rtype: str
    """
    return contacts.data[name].get_birthday()


@input_error
def birthdays(contacts: AddressBook):
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
                birthday_this_year = birthday_this_year.replace(
                    year=today.year + 1)
            else:
                birthday_this_year = birthday_this_year.replace(
                    year=today.year)
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
def edit_record(contacts: AddressBook, name: str):
    """ Method for edit record
    :param contacts: AddressBook
    :type contacts: dict of contacts
    :param name: name of contact
    :type name: str
    :return: str representation of cmd
    :rtype: str
    """
    if contacts.data.get(name):
        user_input = input(f"""What do you want to edit for {name}:
            ° phone <new phone>
            ° birthday <new birthday>
            ° address <new address>
            ° email <new email>
            ° back
            >>>""")
        command, *args = parse_input(user_input)
        args = [name, *args]
        if command == "phone":
            return change_phone(contacts, *args)
        elif command == "birthday":
            return add_birthday(contacts, *args)
        elif command == "address":
            return change_address(contacts, *args)
        elif command == "email":
            return change_email(contacts, *args)
        elif command == "back":
            return "Returned to the main"
        else:
            return "Invalid command."
    else:
        return "Name is not present in address book"


@input_error
def add_note(notes: Notes, name: str, *args):
    """ Method for add Note
    :param notes: notes object
    :type notes: Notes
    :param name: Name of note
    :type name: str
    :return: Note added
    :rtype: str
    """
    text = ' '.join(args)
    notes.add_note(name, text)
    pickle.save_notes(notes)
    return f'Note {name} added'


@input_error
def add_tags(notes: Notes, note_name: str, *args):
    """
    :param notes: notes object
    :type notes: Notes
    :param note_name:  Name of note
    :type note_name: str
    :return: Tags added
    :rtype: str
    """
    tags = ' '.join(args)
    notes.add_tags(note_name, tags)
    pickle.save_notes(notes)
    return f'Tags for note {note_name} added'


@input_error
def find_note(notes: Notes, name: str):
    """ Method for find note
    :param notes: notes object
    :type notes: Notes
    :param name: Name of note
    :type name: str
    :return: notes str representation
    :rtype: str
    """
    return notes.find_note(name)


@input_error
def delete_note(notes: Notes, name: str):
    """ Method for delete note
    :param notes: notes object
    :type notes: Notes
    :param name: Name of note
    :type name: str
    :return:
    :rtype:
    """
    notes.delete_note(name)
    pickle.save_notes(notes)
    return f'Note {name} deleted'


@input_error
def edit_note(notes: Notes, name: str,  *args):
    """ Method for edit note
    :param notes: notes object
    :type notes: Notes
    :param name: Name of note
    :type name: str
    """
    new_text = ' '.join(args)
    notes.edit_note(name, new_text)
    pickle.save_notes(notes)
    return f'Note {name} edited'


@input_error
def find_notes_by_tag(notes: Notes, tag_name: str):
    """ Method for find note
    :param notes: notes object
    :type notes: Notes
    :param tag_name: Name of tag
    :type tag_name: str
    :return: sorted notes by tag
    :rtype: notes str representation
    """
    if len(notes.find_notes_by_tag(tag_name)) == 0:
        print('Teg not found')
    else:
        for name, data in notes.find_notes_by_tag(tag_name).items():
            print(f"Note's name: {name}")
            print(f"Tags: {', '.join(data['tags'])}")
            print(f"Text: {data['text']}\n")
    

@input_error
def sort_notes(notes: Notes):
    """ Method for sort notes
    :param notes: notes object
    :type notes: Notes
    :return: sorted notes
    :rtype: notes str representation
    """
    for name, data in notes.sort_notes().items():
        print(f"Note's name: {name}")
        print(f"Tags: {', '.join(data['tags'])}")
        print(f"Text: {data['text']}\n")


def upcoming_birthday(contacts: AddressBook, n_of_days: str):
    """ Method to show all birthdays in n days if exist
    :return: names of users who has birthday in n days
    :rtype: str
    """

    today = datetime.today().date()
    days = timedelta(days=int(n_of_days))
    upcoming_birthdays = today + days
    if contacts.data:
        birthdays_on_that_day = []
        for user in contacts.data.values():
            birthday = user.birthday.date_object
            birthday_this_year = birthday.replace(year=today.year)
            if upcoming_birthdays == birthday_this_year:
                birthdays_on_that_day.append(str(user.name))

        if birthdays_on_that_day:
            formatted_date = upcoming_birthdays.strftime("%d.%m.%Y")
            return f"{', '.join(birthdays_on_that_day)} have birthday on {formatted_date}"
        else:
            formatted_date = upcoming_birthdays.strftime("%d.%m.%Y")
            return f"No birthdays on {formatted_date}"
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
    contacts = pickle.read_contacts()
    notes = pickle.read_notes()
    print("""Welcome to the assistant bot!
    Available commands:
        ° hello
        ° add <name> <phone number>
        ° phone <name>
        ° all
        ° find <name/phone/birthday/address/email> (at least 3 char)
        ° add-birthday <name> <birthday(in format DD.MM.YYYY)>
        ° show-birthday <name>        
        ° birthdays
        ° upcoming-birthday <number_of_days>
        ° add-address <name> <address>
        ° show-address <name>
        ° add-email <name> <email>
        ° show-email <name>
        ° edit <name>
        ° delete-profile <name>
        ° add-note <name of the note> <text>
        ° add-tags <name of the note> <tags>
        ° find-note <name of the note>
        ° delete-note <name of the note>
        ° edit-note <name of the note> <new text>
        ° find-by-tag <tag>
        ° show-sorted-notes
        ° close/exit""")
    while True:
        readline.set_completer(CommandCompleter(Commands.all_values()).complete)
        readline.set_completer_delims(' ')
        readline.parse_and_bind('tab: complete')
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in [Commands.CLOSE, Commands.EXIT]:
            print("Good bye!")
            break
        elif command == Commands.HELLO:
            print("How can I help you?")
        elif command == Commands.ADD:
            print(add_phone(contacts, *args))
        elif command == Commands.PHONE:
            print(get_phone(contacts, *args))
        elif command == Commands.ALL:
            print(get_all(contacts))
        elif command == Commands.FIND:
            print(find_contact(contacts, *args))
        elif command == Commands.DELETE:
            print(delete(contacts, *args))
        elif command == Commands.ADD_BIRTHDAY:
            print(add_birthday(contacts, *args))
        elif command == Commands.SHOW_BIRTHDAY:
            print(show_birthday(contacts, *args))
        elif command == Commands.BIRTHDAYS:
            print(birthdays(contacts))
        elif command == Commands.UPCOMING_BIRTHDAY:
            print(upcoming_birthday(contacts, *args))
        elif command == Commands.ADD_ADDRESS:
            print(add_address(contacts, *args))
        elif command == Commands.SHOW_ADDRESS:
            print(get_address(contacts, *args))
        elif command == Commands.ADD_EMAIL:
            print(add_email(contacts, *args))
        elif command == Commands.SHOW_EMAIL:
            print(get_email(contacts, *args))
        elif command == Commands.ADD_NOTE:
            print(add_note(notes, *args))
        elif command == Commands.ADD_TAGS:
            print(add_tags(notes, *args))
        elif command == Commands.EDIT_NOTE:
            print(edit_note(notes, *args))
        elif command == Commands.FIND_NOTE:
            print(find_note(notes, *args))
        elif command == Commands.DELETE_NOTE:
            print(delete_note(notes, *args))
        elif command == Commands.FIND_NOTES_BY_TAGS:
            find_notes_by_tag(notes, *args)
        elif command == Commands.SORT_NOTES:
            sort_notes(notes)
        elif command == Commands.EDIT:
            print(edit_record(contacts, *args))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
