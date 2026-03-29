import csv
import random
from tkinter import *
from functools import partial # To prevent unwanted windows

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
    round_capitals = []
    round_flag_codes = []
    flag_images = []

    # loop until we have four flags with different names
    while len(round_countries) < 4:
        potential_country = random.choice(all_flags)

        if potential_country[1] not in all_flags[1]:
            round_countries.append(potential_country[0])
            round_capitals.append(potential_country[1])
            round_flag_codes.append(potential_country[2])
            flag_images.append(potential_country[3])


class StartGame:
    """ Initial Game interface (asks users how many rounds they
    would like to play) """

    def __init__(self):
        """ Gets number of rounds from user """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        self.play_button = Button(self.start_frame, text="Play", font=("Arial", 15, "bold"),
                                  width=10, bg="#d5e8d4", command=self.check_rounds)
        self.play_button.grid(row=2, column=0, padx=10, pady=10)

        # button list (frame | text | bg | command | column)
        difficulty_button_list = [
            [self.start_frame, "Easy", "#d5e8d4", lambda: self.check_rounds("normal"), 0],
            [self.start_frame, "Medium", "#fff2cc", lambda: self.check_rounds("medium"), 1],
            [self.start_frame, "Hard", "#f8cecc", lambda: self.check_rounds("hard"), 2]
        ]

        for item in difficulty_button_list:
            difficulty_button = Button(item[0], text=item[1], bg=item[2],
                                       font=("Arial", 20, "bold"), fg="#000000", command=item[3])
            difficulty_button.grid(row=1, column=item[4], padx=10, pady=10)

        self.difficulty_heading = Label(self.start_frame, text="Choose your difficulty",
                                        font=("Arial", 20, "bold"))
        self.difficulty_heading.grid(row=0, column=0)

    def check_rounds(self, difficulty="normal"):

        Play(5, difficulty)
        root.withdraw()

class Play:

    def __init__(self, how_many, difficulty="normal"):

        # set up rounds for game
        self.rounds_wanted = IntVar()
        self.rounds_wanted = how_many

        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.difficulty_playing = difficulty
        print(self.difficulty_playing)

        self.rounds_won = 0

        self.play_box = Toplevel()

        self.Play_frame = Frame(self.play_box)
        self.Play_frame.grid(padx=10, pady=10)

        self.heading_label = Label(self.Play_frame, text="sup nerds",
                                   font=("Arial", 20, "bold"))
        self.heading_label.grid(row=0, column=0)







# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Country Flags")
    StartGame()
    root.mainloop()