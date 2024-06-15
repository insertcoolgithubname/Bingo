# import click
import cmd
# import sys
import random

main_dict = dict()
bingo_dict = dict()
bingo_array = list()

for x in range(50):
    main_dict["pes" + str(x)] = True


class BingoCmd(cmd.Cmd):
    intro = "Welcome to Bingo lol"
    prompt = "Bingo "

    def do_complete(self, arg):
        "Completes the element of the specified index: complete 1"
        try:
            bingo_dict[list(bingo_dict.keys())[int(arg)]] = True
        except ValueError:
            print("Invalid argument")

    def do_uncomplete(self, arg):
        "Uncompletes the element of the specified index: uncomplete 1"
        try:
            bingo_dict[list(bingo_dict.keys())[int(arg)]] = False
        except ValueError:
            print("Invalid argument")

    def do_list(self, arg):
        "Outputs a list of all options that are present in your bingo grid"
        index = 0
        for x in bingo_dict:
            print(f"{index:02d} {x} {bingo_dict[x]}")
            index = index + 1

    def do_bingo(self, arg):
        "Outputs your bingo grid"
        pass

    def do_create_grid(self, arg):
        "Creates a bingo grid of the specified size, argument must be a number: create_grid 5"
        try:
            grid_size = int(arg)
            if len(main_dict) >= grid_size * grid_size:
                # create bingo array
                bingo_array = [["empty"]*grid_size for i in range(grid_size)]
                # create bingo_dict by choosing random indexes from main dict
                random_main_dict_list = random.sample(range(0, len(main_dict)), grid_size*grid_size)
                for x in range(grid_size*grid_size):
                    bingo_dict[list(main_dict.keys())[random_main_dict_list[x]]] = False
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

    def do_exit(self, arg):
        "Exits the app"
        exit()


if __name__ == "__main__":
    BingoCmd().cmdloop()
