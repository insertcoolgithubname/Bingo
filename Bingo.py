import cmd
import random
import pickle
import csv
from colorama import init, Fore, Style, Back
from xdg_base_dirs import xdg_data_home
from pathlib import Path
from os.path import exists
from os import remove
import sys
import datetime
from calendar import monthrange

init(autoreset=True)


def color_fun(bool):
    if bool:
        return Fore.GREEN
    else:
        return Fore.RED


def confirm():
    if (input("Are you sure: y/n: ")) == "y":
        return True
    else:
        print(f"{Fore.RED}aborting")
        return False


def dict_index(arg_dict, key):
    if key in dict(arg_dict).keys():
        index = list(dict(arg_dict).keys()).index(key)
        return index
    else:
        # not found
        return (-1)


def dict_key(arg_dict, index):
    # returns key of index in bingo_dict
    if index <= (len(dict(arg_dict)) - 1):
        key = list(dict(arg_dict).keys())[index]
        return key
    else:
        # not found
        return (-1)


def check_input(arg_list, arg_index: str):
    # Checks if the input is a valid digit, and is present in the list or dict
    if arg_index.isdigit():
        arg_index = int(arg_index)
        if arg_index <= len(arg_list):
            return True
        else:
            print(f"{Fore.RED}Index out of bounds{Fore.RESET}")
            return False
    else:
        print(f"{Fore.RED}Invalid argument{Fore.RESET}")
        return False


def get_time():
    current_time = datetime.datetime.now()
    formated_time = (f"{current_time.hour}:{current_time.minute} "
                     f"{current_time.day}.{current_time.month} {current_time.year}")
    return formated_time


def to_int(arg_string: str):
    if arg_string.isdigit():
        arg_string = int(arg_string)
        return True, arg_string
    else:
        return False, arg_string


class Settings():
    def __init__(self) -> None:
        self.show_completed = True
        self.show_format = True
        self.show_order = True
        self.show_comment = True
        self.show_date = True
        self.show_index_in_grid = True

    def print_settings(self):
        print(f"\n1: Show completed tasks: {color_fun(self.show_completed)}{self.show_completed}")
        print(f"2: Show task format changes: {color_fun(self.show_format)}{self.show_format}")
        print(f"3: Show task order of completion: {color_fun(self.show_order)}{self.show_order}")
        print(f"4: Show task comments: {color_fun(self.show_comment)}{self.show_comment}")
        print(f"5: Show task date of completion: {color_fun(self.show_date)}{self.show_date}")
        print(f"6: Show completed numbers in grid: {color_fun(self.show_index_in_grid)}{self.show_index_in_grid}\n")

    def flip_setting(self, setting_index):
        if setting_index == "1":
            self.show_completed = not self.show_completed
        elif setting_index == "2":
            self.show_format = not self.show_format
        elif setting_index == "3":
            self.show_order = not self.show_order
        elif setting_index == "4":
            self.show_comment = not self.show_comment
        elif setting_index == "5":
            self.show_date = not self.show_date
        elif setting_index == "6":
            self.show_index_in_grid = not self.show_index_in_grid
        else:
            print(f"{Fore.RED}Wrong setting index")

    def get_format(self, arg_key: int, arg_dict: dict):
        if self.show_format:
            ref = arg_dict[arg_key].text_format
            return ref.text_style + ref.text_color + ref.back_color
        else:
            return ""

    def get_comment(self, arg_key: int, arg_dict: dict):
        if self.show_comment:
            ref = arg_dict[arg_key]
            return ref.comment
        else:
            return ""

    def get_date(self, arg_key: int, arg_dict: dict):
        if self.show_date:
            ref = arg_dict[arg_key]
            if arg_dict[arg_key].complete:
                return ref.completion_date.get_text()
            else:
                return ""
        else:
            return ""

    def get_completion_order(self, arg_key: int, arg_dict: dict, sorted_list: list):
        if self.show_order:
            if arg_dict[arg_key].complete and arg_dict[arg_key].completion_date.current_time is not None:
                return (sorted_list.index(arg_dict[arg_key].completion_date.current_time) + 1)
            else:
                return ""
        else:
            return ""


class Bingo():
    def __init__(self) -> None:
        self._main_dict = {}
        self._bingo_dict = {}
        self._bingo_array = []

    def _set_option_completion(self, dict: dict, index, arg_bool: bool):
        # Completes the option of the given index from the given dict
        try:
            int(index)
        except ValueError:
            print(f"{Fore.RED}Invalid argument{Fore.RESET}")
            return False
        else:
            index = int(index)
            if index <= len(dict) and index >= 0:
                if dict[dict_key(arg_dict=dict, index=index)].complete != arg_bool:
                    self._main_dict[dict_key(arg_dict=dict, index=index)].complete = arg_bool
                    if arg_bool:
                        self._main_dict[dict_key(arg_dict=dict, index=index)].completion_date.fill_date_and_time()
                    else:
                        self._main_dict[dict_key(arg_dict=dict, index=index)].completion_date = TimeAndDate()
                    self.refresh()
                    print(f"{Fore.GREEN}Success{Fore.RESET}")
                    return True
                else:
                    if arg_bool:
                        print(f"{Fore.RED}Index {index} already completed{Fore.RESET}")
                        return False
                    else:
                        print(f"{Fore.RED}Index {index} already uncompleted{Fore.RESET}")
                        return False
            else:
                print(f"{Fore.RED}Index out of bounds{Fore.RESET}")
                return False

    def _list_dict(self, dict: dict):
        # Outputs a list of all options that are present in the grid
        index = 0
        completed_options = 0
        sorted_list = my_bingo.sort_date_list(arg_dict=dict)
        print("")
        for x in dict:
            if not my_settings.show_completed and dict[x].complete:
                # dont show completed if settings dictate it
                pass
            else:
                print(f"{index:02d} {my_settings.get_format(arg_dict=dict, arg_key=x)}"
                      f"{x}{Style.RESET_ALL} {color_fun((dict[x]).complete)}"
                      f"{(dict[x]).complete}{Style.RESET_ALL} "
                      f"{Fore.LIGHTCYAN_EX}{my_settings.get_comment(arg_dict=dict, arg_key=x)}"
                      f"{Fore.RESET} {Fore.LIGHTMAGENTA_EX}{my_settings.get_date(arg_dict=dict, arg_key=x)} "
                      f"{Fore.LIGHTGREEN_EX}"
                      f"{my_settings.get_completion_order(arg_dict=dict, arg_key=x, sorted_list=sorted_list)}"
                      )
            index = index + 1
            if dict[x].complete:
                completed_options += 1
        print("")
        print(f"{completed_options} out of {len(dict)} completed")

    def refresh(self):
        # Refreshes values in bingo_dict with main_dict
        for i in self._bingo_dict:
            self._bingo_dict[i] = self._main_dict[i]

    def print_bingo(self):
        # Outputs the bingo_arry, indexes are referencing bingo_dict"
        grid_size = len(self._bingo_array[0])
        print("")
        for x in range(grid_size):
            row = str()
            for y in range(grid_size):
                if self._bingo_dict[dict_key(arg_dict=self._bingo_dict, index=self._bingo_array[x][y])].complete:
                    if my_settings.show_index_in_grid:
                        row = f"{row}   {Fore.GREEN}{(self._bingo_array[x][y]):02d}{Style.RESET_ALL}"
                    else:
                        row = f"{row}   {Fore.GREEN}[]{Style.RESET_ALL}"
                else:
                    row = f"{row}   {Fore.RED}??{Style.RESET_ALL}"
            print(f"{row}\n")
        print("")
        if self.check_for_victory():
            print(f"{Fore.GREEN}Bingo!\n")

    def create_bingo_array(self, arg_size):
        "Creates a bingo grid of the specified size, argument must be a number: create_grid 5"
        if confirm():
            try:
                grid_size = int(arg_size)
            except ValueError:
                print(f"{Fore.RED}Invalid argument{Fore.RESET}")
                return False
            else:
                if (len(self._main_dict) >= grid_size * grid_size) and grid_size > 0:
                    self._bingo_dict = {}
                    # create bingo array
                    self._bingo_array = [["empty"]*grid_size for i in range(grid_size)]
                    # create bingo_dict by choosing random indexes from main dict
                    random_main_dict_list = random.sample(range(0, len(self._main_dict)), grid_size*grid_size)
                    for x in range(grid_size*grid_size):
                        self._bingo_dict[dict_key(arg_dict=self._main_dict, index=random_main_dict_list[x])] = (
                            self._main_dict[dict_key(arg_dict=self._main_dict, index=random_main_dict_list[x])]
                        )
                    # fill bingo_array with randomized bingo_dict
                    random_bingo_dict_list = random.sample(range(0, len(self._bingo_dict)), len(self._bingo_dict))
                    index = 0
                    for x in range(grid_size):
                        for y in range(grid_size):
                            self._bingo_array[x][y] = random_bingo_dict_list[index]
                            index = index + 1
                    print(f"{Fore.GREEN}Success{Fore.RESET}")
                    return True
                else:
                    print(f"{Fore.RED}Bingo grid too large{Fore.RESET}")
                    return False

    def input_file(self, path):
        # Rewrites the full list of options that can end up in your bingo grid with a file named 'input.csv'
        # argument must specify file path in str: input_file C:/Users/username/path/to/your/file"
        if confirm():
            try:
                with open(path+"/input.csv", "r", encoding="utf-8-sig", newline="") as f:
                    self._main_dict = {}
                    csvFile = csv.reader(f)
                    for line in csvFile:
                        self._main_dict[line[0]] = BingoElement()
                self.refresh()
                print(f"{Fore.GREEN}Success{Fore.RESET}")
                return True
            except FileNotFoundError:
                print(f'{Fore.RED}File not found, make sure the path to your file is correct{Fore.RESET}')
                return False

    def _set_dict_completion(self, arg_dict: dict, arg_bool):
        if confirm():
            for x in arg_dict:
                arg_dict[x].complete = arg_bool
                if arg_bool:
                    arg_dict[x].completion_date.fill_date_and_time()
                else:
                    arg_dict[x].completion_date = TimeAndDate()
            self.refresh()
            print(f"{Fore.GREEN}Success{Fore.RESET}")
            return True
        else:
            return False

    def complete(self, index):
        return self._set_option_completion(dict=self._bingo_dict, index=index, arg_bool=True)

    def uncomplete(self, index):
        return self._set_option_completion(dict=self._bingo_dict, index=index, arg_bool=False)

    def complete_fl(self, index):
        return self._set_option_completion(dict=self._main_dict, index=index, arg_bool=True)

    def uncomplete_fl(self, index):
        return self._set_option_completion(dict=self._main_dict, index=index, arg_bool=False)

    def complete_all(self):
        return self._set_dict_completion(arg_dict=self._main_dict, arg_bool=True)

    def uncomplete_all(self):
        return self._set_dict_completion(arg_dict=self._main_dict, arg_bool=False)

    def complete_grid(self):
        return self._set_dict_completion(arg_dict=self._bingo_dict, arg_bool=True)

    def uncomplete_grid(self):
        return self._set_dict_completion(arg_dict=self._bingo_dict, arg_bool=False)

    def list(self):
        self._list_dict(dict=self._bingo_dict)

    def full_list(self):
        self._list_dict(dict=self._main_dict)

    def _change_option_color(self, arg_color: str, arg_dict: dict):
        index: str = input("Index which should be colored: ")
        if check_input(arg_list=arg_dict, arg_index=index):
            index = int(index)
            success = True
            if arg_color.casefold() == "red":
                color = Fore.RED
            elif arg_color.casefold() == "blue":
                color = Fore.BLUE
            elif arg_color.casefold() == "cyan":
                color = Fore.CYAN
            elif arg_color.casefold() == "green":
                color = Fore.GREEN
            elif arg_color.casefold() == "magenta":
                color = Fore.MAGENTA
            elif arg_color.casefold() == "yellow":
                color = Fore.YELLOW
            elif arg_color.casefold() == "normal":
                color = Fore.RESET
            else:
                success = False
            if success:
                self._main_dict[dict_key(arg_dict=arg_dict, index=index)].text_format.text_color = color
                self.refresh()
                return True
            else:
                print(f"{Fore.RED} Invalid input")
                return False
        else:
            return False

    def color_bingo_dict(self, arg_color):
        return self._change_option_color(arg_color=arg_color, arg_dict=self._bingo_dict)

    def color_main_dict(self, arg_color):
        return self._change_option_color(arg_color=arg_color, arg_dict=self._main_dict)

    def _change_option_style(self, arg_style: str, arg_dict: dict):
        index: str = input("Index which should be colored: ")
        if check_input(arg_list=arg_dict, arg_index=index):
            index = int(index)
            success = True
            if arg_style.casefold() == "bright":
                style = Style.BRIGHT
            elif arg_style.casefold() == "dim":
                style = Style.DIM
            elif arg_style.casefold() == "normal":
                style = Style.NORMAL
            else:
                success = False
            if success:
                self._main_dict[dict_key(arg_dict=arg_dict, index=index)].text_format.text_style = style
                self.refresh()
                return True
            else:
                print(f"{Fore.RED} Invalid input")
                return False
        else:
            return False

    def style_bingo_dict(self, arg_style):
        return self._change_option_style(arg_dict=self._bingo_dict, arg_style=arg_style)

    def style_main_dict(self, arg_style):
        return self._change_option_style(arg_dict=self._main_dict, arg_style=arg_style)

    def _change_background_color(self, arg_color: str, arg_dict: dict):
        index: str = input("Index which should be colored: ")
        if check_input(arg_list=arg_dict, arg_index=index):
            index = int(index)
            success = True
            if arg_color.casefold() == "red":
                color = Back.RED
            elif arg_color.casefold() == "blue":
                color = Back.BLUE
            elif arg_color.casefold() == "cyan":
                color = Back.CYAN
            elif arg_color.casefold() == "green":
                color = Back.GREEN
            elif arg_color.casefold() == "magenta":
                color = Back.MAGENTA
            elif arg_color.casefold() == "yellow":
                color = Back.YELLOW
            elif arg_color.casefold() == "normal":
                color = Back.RESET
            else:
                success = False
            if success:
                self._main_dict[dict_key(arg_dict=arg_dict, index=index)].text_format.back_color = color
                self.refresh()
                return True
            else:
                print(f"{Fore.RED} Invalid input")
                return False
        else:
            return False

    def color_back_bingo_dict(self, arg_color):
        return self._change_background_color(arg_color=arg_color, arg_dict=self._bingo_dict)

    def color_back_main_dict(self, arg_color):
        return self._change_background_color(arg_color=arg_color, arg_dict=self._main_dict)

    def _change_option_comment(self, arg_dict: dict, arg_index: str):
        comment: str = input("Enter comment: ")
        if check_input(arg_list=arg_dict, arg_index=arg_index):
            arg_index = int(arg_index)
            self._main_dict[dict_key(arg_dict=arg_dict, index=arg_index)].comment = comment
            self.refresh()
            return True
        else:
            return False

    def comment_bingo_dict(self, arg_index):
        return self._change_option_comment(arg_dict=self._bingo_dict, arg_index=arg_index)

    def comment_main_dict(self, arg_index):
        return self._change_option_comment(arg_dict=self._main_dict, arg_index=arg_index)

    def sort_date_list(self, arg_dict: dict):
        time_list = []
        for x in arg_dict.values():
            if x.completion_date.current_time is not None:
                time_list.append(x.completion_date.current_time)
            else:
                time_list.append(datetime.datetime(9999, 1, 1, 1, 1))
        time_list = sorted(time_list)
        return time_list

    def _set_completion_time(self, arg_dict: dict, arg_index: str):
        if check_input(arg_index=arg_index, arg_list=arg_dict):
            arg_index = int(arg_index)
            if arg_dict[dict_key(arg_dict=arg_dict, index=arg_index)].complete:
                current_time = datetime.datetime.now()
                year = input("Enter year: ")
                success, year = to_int(year)
                if not success or not year >= 1 or not year <= int(current_time.year):
                    print(f"{Fore.RED}Invalid input")
                    return False
                month = input("Enter month: ")
                success, month = to_int(month)
                if not success or not month >= 0 or not month <= 12:
                    print(f"{Fore.RED}Invalid input")
                    return False
                day = input("Enter day: ")
                success, day = to_int(day)
                if not success or not day >= 0 or not day <= monthrange(year, month)[1]:
                    print(f"{Fore.RED}Invalid input")
                    return False
                hour = input("Enter hour: ")
                success, hour = to_int(hour)
                if not success or not hour >= 0 or not hour <= 24:
                    print(f"{Fore.RED}Invalid input")
                    return False
                minute = input("Enter minute: ")
                success, minute = to_int(minute)
                if not success or not minute >= 0 or not minute <= 60:
                    print(f"{Fore.RED}Invalid input")
                    return False
                self._main_dict[dict_key(arg_dict=arg_dict, index=arg_index)].completion_date.current_time = (
                    datetime.datetime(year=year, hour=hour, minute=minute, day=day, month=month)
                    )
                self.refresh()
                print(f"{Fore.GREEN}Success")
                return True
            else:
                print(f"{Fore.RED}Index not completed")
                return False
        else:
            return False

    def set_bingo_dict_date(self, arg_index):
        return self._set_completion_time(arg_dict=self._bingo_dict, arg_index=arg_index)

    def set_main_dict_date(self, arg_index):
        return self._set_completion_time(arg_dict=self._main_dict, arg_index=arg_index)

    def check_for_victory(self):
        grid_size = len(self._bingo_array[0])
        success = True
        for x in range(grid_size):
            for y in range(grid_size):
                current_index = self._bingo_array[x][y]
                current_complete = self._bingo_dict[dict_key(arg_dict=self._bingo_dict, index=current_index)].complete
                if current_complete:
                    success = True
                else:
                    success = False
                    break
            if success:
                return True
        for x in range(grid_size):
            for y in range(grid_size):
                current_index = self._bingo_array[y][x]
                current_complete = self._bingo_dict[dict_key(arg_dict=self._bingo_dict, index=current_index)].complete
                if current_complete:
                    success = True
                else:
                    success = False
                    break
            if success:
                return True
        for i in range(grid_size):
            x = 0 + i
            y = 0 + i
            current_index = self._bingo_array[x][y]
            current_complete = self._bingo_dict[dict_key(arg_dict=self._bingo_dict, index=current_index)].complete
            if current_complete:
                success = True
            else:
                success = False
                break
        if success:
            return True
        for i in range(grid_size):
            x = 0 + i
            y = grid_size - i - 1
            current_index = self._bingo_array[x][y]
            current_complete = self._bingo_dict[dict_key(arg_dict=self._bingo_dict, index=current_index)].complete
            if current_complete:
                success = True
            else:
                success = False
                break
        if success:
            return True


class TimeAndDate():
    def __init__(self) -> None:
        self.current_time = None

    def fill_date_and_time(self):
        self.current_time = datetime.datetime.now()

    def get_text(self):
        if self.current_time is not None:
            return (f"{self.current_time.hour:02d}:{self.current_time.minute:02d} {self.current_time.day}."
                    f"{self.current_time.month} {self.current_time.year}")
        else:
            return ""


class BingoElement():
    def __init__(self) -> None:
        self.complete = False
        self.text_format = TextFormat()
        self.completion_order = -1
        self.comment: str = ""
        self.completion_date = TimeAndDate()


class TextFormat():
    def __init__(self) -> None:
        self.text_color = Fore.RESET
        self.text_style = Style.RESET_ALL
        self.back_color = Back.RESET


my_settings = Settings()
my_bingo = Bingo()


class BingoCmd(cmd.Cmd):
    intro = "Welcome to Bingo"
    prompt = "Bingo "

    def do_complete(self, arg):
        "Completes the element of the specified index: complete 1"
        if my_bingo.complete(arg):
            my_bingo.list()

    def do_uncomplete(self, arg):
        "Uncompletes the element of the specified index, index is taken from list: uncomplete 1"
        if my_bingo.uncomplete(arg):
            my_bingo.list()

    def do_complete_fl(self, arg):
        "Completes the element of the specified index, index is taken from list_full: complete_fl 1"
        if my_bingo.complete_fl(arg):
            my_bingo.full_list()

    def do_uncomplete_fl(self, arg):
        "Uncompletes the element of the specified index, index  is taken from list_full: uncomplete_fl 1"
        if my_bingo.uncomplete_fl(arg):
            my_bingo.full_list()

    def do_complete_all(self, arg):
        "Completes all options, even those not present in your grid"
        if my_bingo.complete_all():
            my_bingo.full_list()

    def do_uncomplete_all(self, arg):
        "Uncompletes all options, even those not present in your grid"
        if my_bingo.uncomplete_all():
            my_bingo.full_list()

    def do_complete_grid(self, arg):
        "Completes all options in your grid"
        if my_bingo.complete_grid():
            my_bingo.list()

    def do_uncomplete_grid(self, arg):
        "Uncompletes all options in your grid"
        if my_bingo.uncomplete_grid():
            my_bingo.list()

    def do_list(self, arg):
        "Outputs a list of all options that are present in your bingo grid"
        my_bingo.list()

    def do_full_list(self, arg):
        "Outputs the full list of all options, even those not present in your bingo grid"
        my_bingo.full_list()

    def do_bingo(self, arg):
        "Outputs your bingo grid, indexes are referencing list"
        my_bingo.print_bingo()

    def do_input_file(self, arg):
        """Rewrites the full list of options that can end up in your bingo grid with a file named 'input.csv'
        argument must specify file path: input_file C:/Users/username/path/to/your/file"""
        if my_bingo.input_file(arg):
            my_bingo.full_list()

    def do_create_grid(self, arg):
        "Creates a bingo grid of the specified size, argument must be a number: create_grid 5"
        if my_bingo.create_bingo_array(arg_size=arg):
            my_bingo.list()

    def do_save(self, arg):
        "Saves all data to a file"
        save()
        print(f"{Fore.GREEN}Success{Fore.RESET}")

    def do_load(self, arg):
        "Loads all data from a previously saved file"
        load()
        print(f"{Fore.GREEN}Success{Fore.RESET}")

    def do_settings(self, arg):
        "Opens the settings allowing you to change them"
        SettingsCmd().cmdloop()

    def do_color(self, arg):
        """Colors the index of list by the given color, argument is color, the index will be asked later: color red
        Available options: red, blue, cyan, green, magenta, yellow, normal"""
        if my_bingo.color_bingo_dict(arg_color=arg):
            my_bingo.list()

    def do_color_fl(self, arg):
        """Colors the index of full_list by the given color, argument is color, the index will be asked later: color red
        Available options: red, blue, cyan, green, magenta, yellow, normal"""
        if my_bingo.color_main_dict(arg_color=arg):
            my_bingo.full_list()

    def do_style(self, arg):
        """Sets the style of text on the index of list, argument is style, index will be asked later: style bright
        Available options: bright, dim, normal"""
        if my_bingo.style_bingo_dict(arg_style=arg):
            my_bingo.list()

    def do_style_fl(self, arg):
        """Sets the style of text on the index of list, argument is style, index will be asked later: style bright
        Available options: bright, dim, normal"""
        if my_bingo.style_main_dict(arg_style=arg):
            my_bingo.full_list()

    def do_color_back(self, arg):
        """Colors the index of full_list by the given background color, argument is color
        the index will be asked later: color red
        Available options: red, blue, cyan, green, magenta, yellow, normal"""
        if my_bingo.color_back_bingo_dict(arg_color=arg):
            my_bingo.list()

    def do_color_back_fl(self, arg):
        """Colors the index of full_list by the given background color, argument is color
        the index will be asked later: color red
        Available options: red, blue, cyan, green, magenta, yellow, normal"""
        if my_bingo.color_back_main_dict(arg_color=arg):
            my_bingo.full_list()

    def do_comment(self, arg):
        "Adds a custom comment to the option, argument is index from list: comment 1"
        if my_bingo.comment_bingo_dict(arg):
            my_bingo.list()

    def do_comment_fl(self, arg):
        "Adds a custom comment to the option, argument is index from full_list: comment 1"
        if my_bingo.comment_main_dict(arg):
            my_bingo.full_list()

    def do_change_date(self, arg):
        "Changes the completion date of index of list, date will be asked later: change_date 5"
        if my_bingo.set_bingo_dict_date(arg_index=arg):
            my_bingo.list()

    def do_change_date_fl(self, arg):
        "Changes the completion date of index of full_list, date will be asked later: change_date_fl 5"
        if my_bingo.set_main_dict_date(arg_index=arg):
            my_bingo.full_list()

    def do_exit(self, arg):
        "Exits the app"
        save()
        sys.exit()


class SettingsCmd(cmd.Cmd):
    prompt = "Settings "

    def preloop(self):
        my_settings.print_settings()

    def do_exit(self, arg):
        "Exits settings and returns to bingo"
        save_settings()
        BingoCmd().cmdloop()

    def do_list(self, arg):
        "Lists all settings"
        my_settings.print_settings()

    def do_flip(self, arg):
        "Changes True to False and False to True on the given setting. Also calls list, flip 1"
        my_settings.flip_setting(arg)
        my_settings.print_settings()


def save_settings():
    global my_settings
    file_path = str(xdg_data_home())
    Path(file_path+"/bingo").mkdir(parents=True, exist_ok=True)
    with open(xdg_data_home()/"bingo"/"bingosettingsV1,1.pk1", "wb") as f:
        pickle.dump(my_settings, f)


def save_data():
    global my_bingo
    file_path = str(xdg_data_home())
    Path(file_path+"/bingo").mkdir(parents=True, exist_ok=True)
    with open(xdg_data_home()/"bingo"/"bingodataV1,1.pk1", "wb") as f:
        pickle.dump(my_bingo, f)


def save():
    save_data()
    save_settings()


def load_settings():
    global my_settings
    if exists(xdg_data_home()/"bingo"/"bingosettingsV1,1.pk1"):
        with open(xdg_data_home()/"bingo"/"bingosettingsV1,1.pk1", "rb") as f:
            my_settings = pickle.load(f)
    else:
        save_settings()


def load_data():
    # check if old saving format exists (for backwards save compatibility)
    global my_bingo
    if exists(xdg_data_home()/"bingo"/"objs.pk1"):
        with open(xdg_data_home()/"bingo"/"objs.pk1", "rb") as f:
            main_dict, bingo_dict, bingo_array, grid_size = pickle.load(f)
            for i in main_dict:
                my_bingo._main_dict[i] = BingoElement()
                my_bingo._main_dict[i].complete = main_dict[i]
            for i in bingo_dict:
                my_bingo._bingo_dict[i] = BingoElement()
                my_bingo._bingo_dict[i].complete = bingo_dict[i]
            my_bingo._bingo_array = bingo_array
            save_data()
        remove(xdg_data_home()/"bingo"/"objs.pk1")
    elif exists(xdg_data_home()/"bingo"/"bingodataV1,1.pk1"):
        with open(xdg_data_home()/"bingo"/"bingodataV1,1.pk1", "rb") as f:
            my_bingo = pickle.load(f)
    else:
        save_data()


def load():
    load_data()
    load_settings()


def main():
    load()
    BingoCmd().cmdloop()


if __name__ == "__main__":
    main()
