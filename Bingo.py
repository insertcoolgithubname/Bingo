import cmd
import random
import pickle
import csv
from colorama import init, Fore, Style, Back
from xdg_base_dirs import xdg_data_home
from pathlib import Path

init(autoreset=True)

main_dict = dict()
bingo_dict = dict()
bingo_array = list()
grid_size: int = 0


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
        self.main_dict = {}
        self.bingo_dict = {}
        for i in range(50):
            self.main_dict[f"test{i}"] = BingoElement()
        # self.main_dict = {"test1": BingoElement(), "test2": BingoElement()}
        # self.bingo_dict = {"test2": BingoElement(), "test1": BingoElement()}
        self.grid_size: int = 0
        self.bingo_array = []

    def set_option_completion(self, dict: dict, index, arg_bool: bool):
        # Completes the option of the given index from the given dict
        try:
            int(index)
        except ValueError:
            print(f"{Fore.RED}Invalid argument{Fore.RESET}")
        else:
            index = int(index)
            if index <= len(dict) and index >= 0:
                if dict[dict_key(arg_dict=dict, index=index)].complete != arg_bool:
                    self.main_dict[dict_key(arg_dict=dict, index=index)].complete = arg_bool
                    self.refresh()
                    print(f"{Fore.GREEN}Sucess{Fore.RESET}")
                else:
                    if arg_bool:
                        print(f"{Fore.RED}Index {index} already completed{Fore.RESET}")
                    else:
                        print(f"{Fore.RED}Index {index} already uncompleted{Fore.RESET}")
            else:
                print(f"{Fore.RED}Index out of bounds{Fore.RESET}")

    def list_dict(self, dict: dict):
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
        for i in self.bingo_dict:
            self.bingo_dict[i] = self.main_dict[i]

    def print_bingo(self):
        # Outputs the bingo_arry, indexes are referencing bingo_dict"
        grid_size = len(self.bingo_array[0])
        print("")
        for x in range(grid_size):
            row = str()
            for y in range(grid_size):
                # if bingo_dict[list(bingo_dict.keys())[(self.bingo_array[x][y])]]:
                if self.bingo_dict[dict_key(arg_dict=self.bingo_dict, index=self.bingo_array[x][y])].complete:
                    row = f"{row}  {Fore.GREEN}{(self.bingo_array[x][y]):02d}{Style.RESET_ALL}"
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
                if (len(self.main_dict) >= grid_size * grid_size) and grid_size > 0:
                    # create bingo array
                    self.bingo_array = [["empty"]*grid_size for i in range(grid_size)]
                    # create bingo_dict by choosing random indexes from main dict
                    random_main_dict_list = random.sample(range(0, len(self.main_dict)), grid_size*grid_size)
                    for x in range(grid_size*grid_size):
                        self.bingo_dict[dict_key(arg_dict=self.main_dict, index=random_main_dict_list[x])] = (
                            self.main_dict[dict_key(arg_dict=self.main_dict, index=random_main_dict_list[x])]
                        )
                    # fill bingo_array with randomized bingo_dict
                    random_bingo_dict_list = random.sample(range(0, len(self.bingo_dict)), len(self.bingo_dict))
                    index = 0
                    for x in range(grid_size):
                        for y in range(grid_size):
                            self.bingo_array[x][y] = random_bingo_dict_list[index]
                            index = index + 1
                    print(f"{Fore.GREEN}Sucess{Fore.RESET}")
                else:
                    print(f"{Fore.RED}Bingo grid too large{Fore.RESET}")

    def fill_main_dict(self, path):
        # Rewrites the full list of options that can end up in your bingo grid with a file named 'input.csv', argument must specify file path: input_file C:/Users/username/path/to/your/file"
        if confirm():
            try:
                with open(path+"/input.csv", "r", encoding="utf-8-sig", newline="") as f:
                    self.main_dict = {}
                    csvFile = csv.reader(f)
                    for line in csvFile:
                        self.main_dict[line[0]] = BingoElement()
                self.refresh()
                print(f"{Fore.GREEN}Sucess{Fore.RESET}")
            except FileNotFoundError:
                print(f'{Fore.RED}File not found, make sure the path to your file is correct{Fore.RESET}')


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


class BingoCmd(cmd.Cmd):
    intro = "Welcome to Bingo"
    prompt = "Bingo "

    def do_complete(self, arg):
        "Completes the element of the specified index: complete 1"
        try:
            if int(arg) <= len(bingo_dict) and int(arg) >= 0:
                if not bingo_dict[list(bingo_dict.keys())[int(arg)]]:
                    bingo_dict[list(bingo_dict.keys())[int(arg)]] = True
                    main_dict[list(bingo_dict.keys())[int(arg)]] = True
                    print(f"{Fore.GREEN}Sucess{Fore.RESET}")
                else:
                    print(f"{Fore.RED}Index {arg} already completed{Fore.RESET}")
            else:
                print(f"{Fore.RED}Index out of bounds{Fore.RESET}")
        except ValueError:
            print(f"{Fore.RED}Invalid argument{Fore.RESET}")

    def do_uncomplete(self, arg):
        "Uncompletes the element of the specified index, index is taken from list: uncomplete 1"
        try:
            if int(arg) <= len(bingo_dict) and int(arg) >= 0:
                if bingo_dict[list(bingo_dict.keys())[int(arg)]]:
                    bingo_dict[list(bingo_dict.keys())[int(arg)]] = False
                    main_dict[list(bingo_dict.keys())[int(arg)]] = False
                    print(f"{Fore.GREEN}Sucess{Fore.RESET}")
                else:
                    print(f"{Fore.RED}Index {arg} already completed{Fore.RESET}")
            else:
                print(f"{Fore.RED}Index out of bounds{Fore.RESET}")
        except ValueError:
            print(f"{Fore.RED}Invalid argument{Fore.RESET}")

    def do_complete_fl(self, arg):
        "Completes the element of the specified index, index is taken from list_full: complete_fl 1"
        try:
            if int(arg) <= len(main_dict) and int(arg) >= 0:
                if not main_dict[list(main_dict.keys())[int(arg)]]:
                    main_dict[list(main_dict.keys())[int(arg)]] = True
                    refresh()
                    print(f"{Fore.GREEN}Sucess{Fore.RESET}")
                else:
                    print(f"{Fore.RED}Index {arg} already completed{Fore.RESET}")
            else:
                print(f"{Fore.RED}Index out of bounds{Fore.RESET}")
        except ValueError:
            print(f"{Fore.RED}Invalid argument{Fore.RESET}")

    def do_uncomplete_fl(self, arg):
        "Uncompletes the element of the specified index, index is taken from list_full: uncomplete_fl 1"
        try:
            if int(arg) <= len(main_dict) and int(arg) >= 0:
                if main_dict[list(main_dict.keys())[int(arg)]]:
                    main_dict[list(main_dict.keys())[int(arg)]] = False
                    refresh()
                    print(f"{Fore.GREEN}Sucess{Fore.RESET}")
                else:
                    print(f"{Fore.RED}Index {arg} already completed{Fore.RESET}")
            else:
                print(f"{Fore.RED}Index out of bounds{Fore.RESET}")
        except ValueError:
            print(f"{Fore.RED}Invalid argument{Fore.RESET}")

    def do_complete_all(self, arg):
        "Completes all options, even those not present in your grid"
        if confirm():
            for x in main_dict:
                main_dict[x] = True
            refresh()
            print(f"{Fore.GREEN}Sucess{Fore.RESET}")

    def do_uncomplete_all(self, arg):
        "Uncompletes all options, even those not present in your grid"
        if confirm():
            for x in main_dict:
                main_dict[x] = False
            refresh()
            print(f"{Fore.GREEN}Sucess{Fore.RESET}")

    def do_complete_grid(self, arg):
        "Completes all options in your grid"
        if confirm():
            for x in bingo_dict:
                main_dict[x] = True
            refresh()
            print(f"{Fore.GREEN}Sucess{Fore.RESET}")

    def do_uncomplete_grid(self, arg):
        "Uncompletes all options in your grid"
        if confirm():
            for x in bingo_dict:
                main_dict[x] = False
            refresh()
            print(f"{Fore.GREEN}Sucess{Fore.RESET}")

    def do_list(self, arg):
        "Outputs a list of all options that are present in your bingo grid"
        index = 0
        completed_options = 0
        print()
        for x in bingo_dict:
            print(f"{index:02d} {x} {color(bingo_dict[x])}{bingo_dict[x]}{Style.RESET_ALL}")
            index = index + 1
            if bingo_dict[x]:
                completed_options += 1
        print()
        print(f"{completed_options} out of {len(bingo_dict)} completed")

    def do_full_list(self, arg):
        "Outputs the full list of all options, even those not present in your bingo grid"
        index = 0
        completed_options = 0
        print()
        for x in main_dict:
            print(f"{index:02d} {x} {color(main_dict[x])}{main_dict[x]}{Style.RESET_ALL}")
            index = index + 1
            if main_dict[x]:
                completed_options += 1
        print()
        print(f"{completed_options} out of {len(main_dict)} completed")

    def do_bingo(self, arg):
        "Outputs your bingo grid, indexes are referencing list"
        print()
        for x in range(grid_size):
            row = str()
            for y in range(grid_size):
                if bingo_dict[list(bingo_dict.keys())[(bingo_array[x][y])]]:
                    row = f"{row}  {Fore.GREEN}{(bingo_array[x][y]):02d}{Style.RESET_ALL}"
                else:
                    row = f"{row}  {Fore.RED}??{Style.RESET_ALL}"
            print(row)
        print()

    def do_input_file(self, arg):
        "Rewrites the full list of options that can end up in your bingo grid with a file named 'input.csv', argument must specify file path: input_file C:/Users/username/path/to/your/file"
        global main_dict
        if confirm():
            try:
                with open(arg+"/input.csv", "r", encoding="utf-8-sig", newline="") as f:
                    main_dict = dict()
                    csvFile = csv.reader(f)
                    for line in csvFile:
                        main_dict[line[0]] = False
                refresh()
                print(f"{Fore.GREEN}Sucess{Fore.RESET}")
            except FileNotFoundError:
                print(f'{Fore.RED}File not found, make sure the path to your file is correct{Fore.RESET}')

    def do_create_grid(self, arg):
        "Creates a bingo grid of the specified size, argument must be a number: create_grid 5"
        if confirm():
            try:
                global grid_size
                global bingo_dict
                global bingo_array
                global main_dict
                int(arg)
                if (len(main_dict) >= grid_size * grid_size) and int(arg) > 0:
                    grid_size = int(arg)
                    bingo_dict = dict()
                    # create bingo array
                    bingo_array = [["empty"]*grid_size for i in range(grid_size)]
                    # create bingo_dict by choosing random indexes from main dict
                    random_main_dict_list = random.sample(range(0, len(main_dict)), grid_size*grid_size)
                    for x in range(grid_size*grid_size):
                        bingo_dict[list(main_dict.keys())[random_main_dict_list[x]]] = main_dict[list(main_dict.keys())[x]]
                    # fill bingo_array with randomized bingo_dict
                    random_bingo_dict_list = random.sample(range(0, len(bingo_dict)), len(bingo_dict))
                    index = 0
                    for x in range(grid_size):
                        for y in range(grid_size):
                            bingo_array[x][y] = random_bingo_dict_list[index]
                            index = index + 1
                    print(f"{Fore.GREEN}Sucess{Fore.RESET}")
                else:
                    print(f"{Fore.RED}Bingo grid too large{Fore.RESET}")
            except ValueError:
                print(f"{Fore.RED}Invalid argument{Fore.RESET}")

    def do_save(self, arg):
        "Saves all data to a file"
        save()
        print(f"{Fore.GREEN}Sucess{Fore.RESET}")

    def do_load(self, arg):
        "Loads all data from a previously saved file"
        load()
        print(f"{Fore.GREEN}Sucess{Fore.RESET}")

    def do_settings(self, arg):
        SettingsCmd().cmdloop()

    def do_exit(self, arg):
        "Exits the app"
        save()
        exit()


my_settings = Settings()
my_bingo = Bingo()


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
    save_object = (main_dict, bingo_dict, bingo_array, grid_size)
    file_path = str(xdg_data_home())
    Path(file_path+"/bingo").mkdir(parents=True, exist_ok=True)
    with open(xdg_data_home()/"bingo"/"objs.pk1", "wb") as f:
        pickle.dump(save_object, f)


def load():
    global main_dict
    global bingo_dict
    global bingo_array
    global grid_size
    try:
        with open(xdg_data_home()/"bingo"/"objs.pk1", "rb") as f:
            main_dict, bingo_dict, bingo_array, grid_size = pickle.load(f)
    except FileNotFoundError:
        save()


def refresh():
    # Refresh bingo dict with values in main_dict
    for x in bingo_dict:
        bingo_dict[x] = main_dict[x]


def main():
    load()
    BingoCmd().cmdloop()


if __name__ == "__main__":
    # main()
    pass
