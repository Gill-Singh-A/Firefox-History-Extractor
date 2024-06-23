#! /usr/bin/env python3

import os, sqlite3
from pathlib import Path
from datetime import date
from optparse import OptionParser
from colorama import Fore, Back, Style
from time import strftime, localtime

status_color = {
    '+': Fore.GREEN,
    '-': Fore.RED,
    '*': Fore.YELLOW,
    ':': Fore.CYAN,
    ' ': Fore.WHITE
}

query = "SELECT datetime(moz_historyvisits.visit_date/1000000,'unixepoch'), moz_places.url, moz_places.title FROM moz_places, moz_historyvisits;"
history_file_name = "places.sqlite"
folder_name = ".mozilla"
default_path = Path.home() / folder_name

def display(status, data, start='', end='\n'):
    print(f"{start}{status_color[status]}[{status}] {Fore.BLUE}[{date.today()} {strftime('%H:%M:%S', localtime())}] {status_color[status]}{Style.BRIGHT}{data}{Fore.RESET}{Style.RESET_ALL}", end=end)

def get_arguments(*args):
    parser = OptionParser()
    for arg in args:
        parser.add_option(arg[0], arg[1], dest=arg[2], help=arg[3])
    return parser.parse_args()[0]

def extractFirefoxHistory(history_db):
    '''
    Return Data Format
    [
        (date time, url, title),
    ]
    '''
    try:
        db = sqlite3.connect(history_db)
        cursor = db.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    except:
        return False

if __name__ == "__main__":
    arguments = get_arguments(('-p', "--path", "path", f"Path to Firefox Cache Folder (Default={default_path})"),
                              ('-w', "--write", "write", "Write to File (Default=Current Date and Time)"))
    if not arguments.path:
        arguments.path = default_path
    if not os.path.isdir(arguments.path):
        display('-', f"No Directory as {Back.YELLOW}{arguments.path}{Back.RESET}")
        exit(0)
    if not arguments.write:
        arguments.write = f"{date.today()} {strftime('%H_%M_%S', localtime())}"
    for path, folders, files in os.walk(arguments.path):
        if history_file_name in files:
            history_file_path = f"{path}/{history_file_name}"