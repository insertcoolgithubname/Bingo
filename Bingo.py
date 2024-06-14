#import click
import cmd, sys

MainDict = dict()

class BingoCmd(cmd.Cmd):
    intro = "Welcome to Bingo lol"
    prompt = "Bingo "

    def do_test(self, arg):
        "Test"
        MainDict[arg] = True
    def do_complete(self, arg):
        "Completes the element of the specified index: complete 1"
    def do_refresh(self, arg):
        print(MainDict)
    def do_exit(self, arg):
        "Exits the app"
        exit()

if __name__ == "__main__":
    BingoCmd().cmdloop()


#MainDict["Test"] = True

#@click.command()



