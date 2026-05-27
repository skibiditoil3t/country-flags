import csv
import random
from random import randint
from tkinter import *
from functools import partial  # To prevent unwanted windows


def get_all_flags():
    # Retrieve colours from csv file and put them in a list
    file = open("country_flags.csv", "r")
    all_flags = list(csv.reader(file, delimiter=","))
    file.close()

    # remove the first row
    all_flags.pop(0)

    return all_flags


def get_country():
    all_flags = get_all_flags()

    round_countries = []

    # loop until we have four countries with different names

    while len(round_countries) < 4:
        potential_country = random.choice(all_flags)

        if potential_country[0] not in round_countries:

            # append country with details
            round_countries.append(potential_country)

    return round_countries


class StartGame:
    """ Initial Game interface (asks users how many questions they
    would like to play) """

    def __init__(self):
        """ Gets number of questions from user """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        self.start_button = Button(self.start_frame, text="Start", command=partial(Play),
                                   font=("Arial", 20, "bold"))
        self.start_button.grid(row=0)

class Play:
    """
    Initial Play interface
    (checks how many questions the user put and
    sets up the GUI for the country quiz)
    """

    def __init__(self, difficulty="normal"):

        # set up the difficulty
        self.difficulty_playing = difficulty

        # setup Play frame
        self.play_box = Toplevel()

        self.play_frame = Frame(self.play_box)
        self.play_frame.grid(padx=10, pady=10)

        self.help_button = Button(self.play_frame, text="Help", font=("Arial", 20, "bold"),
                                  bg="lightblue", command=self.to_hints)
        self.help_button.grid(row=0, column=0)

    def to_hints(self):
        # Displays hints and retrieves difficulty


        difficulty = self.difficulty_playing
        Help(difficulty)


class Help:
    """
    Initial Help GUI
    (Shows user the country and capital if needed)
    """
    def __init__(self, difficulty):
        difficulty_hint = difficulty

        self.help_box = Toplevel()

        self.help_frame = Frame(self.help_box, width=300, height=400)
        self.help_frame.grid()

        self.help_frame.config(bg='lightblue')

        # (text | row | font | justify)
        # ADD STICKY TO THESE LABELS SO THEY GO LEFT "STICKY="W""
        hint_labels_list = [
            ["Hints", 0, ("Arial", 20, "bold"), "left"],
            ["You have used 1/3 Hints...", 1, ("Arial", 15), "left"],
            ["Flag", 2, None, None],
            ["\nFlag code of this country:", 3, ("Arial", 15, "bold"), None],
            ["IL", 4, ("Arial", 20, "bold"), None],
            ["\nCapital of this country:", 5, ("Arial", 15, "bold"), None],
            ["Tel Aviv", 6, ("Arial", 20, "bold"), None]
        ]

        recolour_list = []
        for item in hint_labels_list:
            hint_label = Label(self.help_frame, text=item[0], font=item[2], anchor="w",
                               justify="right")
            hint_label.grid(row=item[1], column=0)

            recolour_list.append(hint_label)

        for item in recolour_list:
            item.config(bg='lightblue')




# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Country Flags")
    StartGame()
    root.mainloop()