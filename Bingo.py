import cmd
import random
import pickle
import csv
from colorama import init, Fore, Style

init()

main_dict = dict()
bingo_dict = dict()
bingo_array = list()
grid_size: int = 0


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
                else:
                    print(f"Index {arg} already completed")
            else:
                print("Index out of bounds")
        except ValueError:
            print("Invalid argument")

    def do_uncomplete(self, arg):
        "Uncompletes the element of the specified index, index is taken from list: uncomplete 1"
        try:
            if int(arg) <= len(bingo_dict) and int(arg) >= 0:
                if bingo_dict[list(bingo_dict.keys())[int(arg)]]:
                    bingo_dict[list(bingo_dict.keys())[int(arg)]] = False
                    main_dict[list(bingo_dict.keys())[int(arg)]] = False
                else:
                    print(f"Index {arg} already uncompleted")
            else:
                print("Index out of bounds")
        except ValueError:
            print("Invalid argument")

    def do_complete_fl(self, arg):
        "Completes the element of the specified index, index is taken from list_full: complete_fl 1"
        try:
            if int(arg) <= len(main_dict) and int(arg) >= 0:
                if not main_dict[list(main_dict.keys())[int(arg)]]:
                    main_dict[list(main_dict.keys())[int(arg)]] = True
                    refresh()
                else:
                    print(f"Index {arg} already completed")
            else:
                print("Index out of bounds")
        except ValueError:
            print("Invalid argument")

    def do_uncomplete_fl(self, arg):
        "Uncompletes the element of the specified index, index is taken from list_full: uncomplete_fl 1"
        try:
            if int(arg) <= len(main_dict) and int(arg) >= 0:
                if main_dict[list(main_dict.keys())[int(arg)]]:
                    main_dict[list(main_dict.keys())[int(arg)]] = False
                    refresh()
                else:
                    print(f"Index {arg} already uncompleted")
            else:
                print("Index out of bounds")
        except ValueError:
            print("Invalid argument")

    def do_complete_all(self, arg):
        "Completes all options, even those not present in your grid"
        if confirm():
            for x in main_dict:
                main_dict[x] = True
            refresh()

    def do_uncomplete_all(self, arg):
        "Uncompletes all options, even those not present in your grid"
        if confirm():
            for x in main_dict:
                main_dict[x] = False
            refresh()

    def do_complete_grid(self, arg):
        "Completes all options in your grid"
        if confirm():
            for x in bingo_dict:
                main_dict[x] = True
            refresh()

    def do_uncomplete_grid(self, arg):
        "Uncompletes all options in your grid"
        if confirm():
            for x in bingo_dict:
                main_dict[x] = False
            refresh()

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
        "Rewrites the full list of options that can end up in your bingo grid with a file named 'input.csv' in your folder: input_file"
        global main_dict
        if confirm():
            main_dict = dict()
            with open("input.csv", "r", encoding="utf-8-sig", newline="") as f:
                csvFile = csv.reader(f)
                for line in csvFile:
                    main_dict[line[0]] = False
            refresh()

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

                else:
                    print("Bingo grid too large")
            except ValueError:
                print("Invalid argument")

    def do_save(self, arg):
        "Saves all data to a file"
        save()

    def do_load(self, arg):
        "Loads all data from a previously created file"
        load()

    def do_exit(self, arg):
        "Exits the app"
        save()
        exit()


def save():
    save_object = (main_dict, bingo_dict, bingo_array, grid_size)
    with open("objs.pk1", "wb") as f:
        pickle.dump(save_object, f)


def load():
    global main_dict
    global bingo_dict
    global bingo_array
    global grid_size
    try:
        with open("objs.pk1", "rb") as f:
            main_dict, bingo_dict, bingo_array, grid_size = pickle.load(f)
    except FileNotFoundError:
        save()


def refresh():
    # Refresh bingo dict with values in main_dict
    for x in bingo_dict:
        bingo_dict[x] = main_dict[x]


def color(bool):
    if bool:
        return Fore.GREEN
    else:
        return Fore.RED


def confirm():
    if (input("Are you sure: y/n: ")) == "y":
        return True
    else:
        return False


def main():
    load()
    BingoCmd().cmdloop()


if __name__ == "__main__":
    main()
