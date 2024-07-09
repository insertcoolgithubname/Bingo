import cmd
import random
import pickle
import csv
from colorama import init, Fore, Style, Back
from xdg_base_dirs import xdg_data_home
from pathlib import Path
from os.path import exists
from os import remove

init(autoreset=True)


def color(bool):
    if bool:
        return Fore.GREEN
    else:
        return Fore.RED


def confirm():
    if (input("Are you sure: y/n: ")) == "y":
        return True
    else:
        print("aborting")
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


class Settings():
    def __init__(self) -> None:
        self.show_completed = True
        self.show_format = True
        self.show_order = True
        self.show_comment = True
        self.show_date = True

    def print_settings(self):
        print(f"\n1: Show completed tasks: {color(self.show_completed)}{self.show_completed}")
        print(f"2: Show task format changes: {color(self.show_format)}{self.show_format}")
        print(f"3: Show task order of completion: {color(self.show_order)}{self.show_order}")
        print(f"4: Show task comments: {color(self.show_comment)}{self.show_comment}")
        print(f"5: Show task date of completion: {color(self.show_date)}{self.show_date}\n")

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
        else:
            print(f"{Fore.RED}Wrong setting index")


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
        else:
            index = int(index)
            if index <= len(dict) and index >= 0:
                if dict[dict_key(arg_dict=dict, index=index)].complete != arg_bool:
                    self._main_dict[dict_key(arg_dict=dict, index=index)].complete = arg_bool
                    self.refresh()
                    print(f"{Fore.GREEN}Sucess{Fore.RESET}")
                else:
                    if arg_bool:
                        print(f"{Fore.RED}Index {index} already completed{Fore.RESET}")
                    else:
                        print(f"{Fore.RED}Index {index} already uncompleted{Fore.RESET}")
            else:
                print(f"{Fore.RED}Index out of bounds{Fore.RESET}")

    def _list_dict(self, dict: dict):
        # Outputs a list of all options that are present in the grid
        index = 0
        completed_options = 0
        print("")
        for x in dict:
            print(f"{index:02d} {x} {color((dict[x]).complete)}"
                  f"{(dict[x]).complete}{Style.RESET_ALL}")
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
                # if bingo_dict[list(bingo_dict.keys())[(self.bingo_array[x][y])]]:
                if self._bingo_dict[dict_key(arg_dict=self._bingo_dict, index=self._bingo_array[x][y])].complete:
                    row = f"{row}  {Fore.GREEN}{(self._bingo_array[x][y]):02d}{Style.RESET_ALL}"
                else:
                    row = f"{row}  {Fore.RED}??{Style.RESET_ALL}"
            print(row)
        print("")

    def create_bingo_array(self, arg_size):
        "Creates a bingo grid of the specified size, argument must be a number: create_grid 5"
        if confirm():
            try:
                grid_size = int(arg_size)
            except ValueError:
                print(f"{Fore.RED}Invalid argument{Fore.RESET}")
            else:
                if (len(self._main_dict) >= grid_size * grid_size) and grid_size > 0:
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
                    print(f"{Fore.GREEN}Sucess{Fore.RESET}")
                else:
                    print(f"{Fore.RED}Bingo grid too large{Fore.RESET}")

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
                print(f"{Fore.GREEN}Sucess{Fore.RESET}")
            except FileNotFoundError:
                print(f'{Fore.RED}File not found, make sure the path to your file is correct{Fore.RESET}')

    def _set_dict_completion(self, arg_dict: dict, arg_bool):
        if confirm():
            for x in arg_dict:
                arg_dict[x].complete = arg_bool
            self.refresh()
            print(f"{Fore.GREEN}Sucess{Fore.RESET}")

    def complete(self, index):
        self._set_option_completion(dict=my_bingo._bingo_dict, index=index, arg_bool=True)

    def uncomplete(self, index):
        self._set_option_completion(dict=my_bingo._bingo_dict, index=index, arg_bool=False)

    def complete_fl(self, index):
        self._set_option_completion(dict=my_bingo._main_dict, index=index, arg_bool=True)

    def uncomplete_fl(self, index):
        self._set_option_completion(dict=my_bingo._main_dict, index=index, arg_bool=False)

    def complete_all(self):
        my_bingo._set_dict_completion(arg_dict=my_bingo._main_dict, arg_bool=True)

    def uncomplete_all(self):
        my_bingo._set_dict_completion(arg_dict=my_bingo._main_dict, arg_bool=False)

    def complete_grid(self):
        my_bingo._set_dict_completion(arg_dict=my_bingo._bingo_dict, arg_bool=True)

    def uncomplete_grid(self):
        my_bingo._set_dict_completion(arg_dict=my_bingo._bingo_dict, arg_bool=False)

    def list(self):
        my_bingo._list_dict(dict=my_bingo._bingo_dict)

    def full_list(self):
        my_bingo._list_dict(dict=my_bingo._main_dict)


class BingoElement():
    def __init__(self) -> None:
        self.complete = False
        self.text_format = TextFormat()
        self.completion_order = -1
        self.comment: str = ""
        self.completion_date: str = ""


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
        my_bingo.complete(arg)

    def do_uncomplete(self, arg):
        "Uncompletes the element of the specified index, index is taken from list: uncomplete 1"
        my_bingo.uncomplete(arg)

    def do_complete_fl(self, arg):
        "Completes the element of the specified index, index is taken from list_full: complete_fl 1"
        my_bingo.complete_fl(arg)

    def do_uncomplete_fl(self, arg):
        "Uncompletes the element of the specified index, index  is taken from list_full: uncomplete_fl 1"
        my_bingo.uncomplete_fl(arg)

    def do_complete_all(self, arg):
        "Completes all options, even those not present in your grid"
        my_bingo.complete_all()

    def do_uncomplete_all(self, arg):
        "Uncompletes all options, even those not present in your grid"
        my_bingo.uncomplete_all()

    def do_complete_grid(self, arg):
        "Completes all options in your grid"
        my_bingo.complete_grid()

    def do_uncomplete_grid(self, arg):
        "Uncompletes all options in your grid"
        my_bingo.uncomplete_grid()

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
        my_bingo.input_file(arg)

    def do_create_grid(self, arg):
        "Creates a bingo grid of the specified size, argument must be a number: create_grid 5"
        my_bingo.create_bingo_array(arg_size=arg)

    def do_save(self, arg):
        "Saves all data to a file"
        save()
        print(f"{Fore.GREEN}Sucess{Fore.RESET}")

    def do_load(self, arg):
        "Loads all data from a previously saved file"
        load()
        print(f"{Fore.GREEN}Sucess{Fore.RESET}")

    def do_settings(self, arg):
        "Opens the settings allowing you to change them"
        SettingsCmd().cmdloop()

    def do_exit(self, arg):
        "Exits the app"
        save()
        exit()


class SettingsCmd(cmd.Cmd):
    prompt = "Settings "

    def preloop(self):
        my_settings.print_settings()

    def do_exit(self, arg):
        "Exits settings and returns to bingo"
        BingoCmd().cmdloop()

    def do_list(self, arg):
        "Lists all settings"
        my_settings.print_settings()

    def do_flip(self, arg):
        "Changes True to False and False to True on the given setting. Also calls list, flip 1"
        my_settings.flip_setting(arg)
        my_settings.print_settings()


def save():
    global my_bingo
    file_path = str(xdg_data_home())
    Path(file_path+"/bingo").mkdir(parents=True, exist_ok=True)
    with open(xdg_data_home()/"bingo"/"bingodataV1,1.pk1", "wb") as f:
        pickle.dump(my_bingo, f)


def load():
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
            save()
        remove(xdg_data_home()/"bingo"/"objs.pk1")
    elif exists(xdg_data_home()/"bingo"/"bingodataV1,1.pk1"):
        with open(xdg_data_home()/"bingo"/"bingodataV1,1.pk1", "rb") as f:
            my_bingo = pickle.load(f)
    else:
        save()


def main():
    load()
    BingoCmd().cmdloop()


if __name__ == "__main__":
    main()
