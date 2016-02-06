from __future__ import print_function
from os import system

class ConsoleMenu(object):
    def __init__(self, choices):
        self.lines_per_screen = 35
        self.choices = choices
    def show(self):
        self.page_start = 0
        self._show_page()
        return self._prompt()
    def _show_page(self):
        system("clear")
        if len(self.choices) < self.page_start + self.lines_per_screen:
            top = len(self.choices) - self.page_start
        else:
            top = self.lines_per_screen
            
        for ln in range(top):
            index = ln + self.page_start
            print("%s: %s" % (ln + 1,
                              self.choices[index][0].ljust(72)))
    def _prompt(self):
        if len(self.choices) > self.page_start + self.lines_per_screen:
            print("(Enter for more...)")

        resp = input("Choice: ")

        if resp == "":
            self.page_start += self.lines_per_screen
            self._show_page()
            return self._prompt()
        else:
            index = int(resp) + self.page_start - 1
            return self.choices[index][1]

if __name__ == "__main__":
    choices = [["Test %s" % i, "Value %s" % i]
               for i in range(100)]
    
    menu = ConsoleMenu(choices)
    print(menu.show())
