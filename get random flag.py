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

    # loop until we have four countries with different names
    while len(round_countries) < 4:
        potential_country = random.choice(all_flags)

        if potential_country[0] not in round_countries:
            round_countries.append(potential_country[0])
            round_capitals.append(potential_country[1])

    return round_countries, round_capitals


class StartGame:
    """ Initial Game interface (asks users how many rounds they
    would like to play) """

    def __init__(self):
        """ Gets number of rounds from user """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Strings for labels
        intro_string = ("In each round you will have to guess the flag of a country (or capital if a harder difficulty is chosen). "
                        "\n\nYour goal is to correctly guess the country and win the round with your knowledge!"
                        "\n\nTo begin, please enter how many rounds you'd like to play and then choose your difficulty.")

        choose_string = "How many rounds do you want to play?"

        # list of labels to be made (text | font | fg)
        start_labels_list = [
            ["Country Flags", ("Arial", 16, "bold"), None],
            [intro_string, ("Arial", 12), None],
            [choose_string, ("Arial", 12, "bold"), "#009900"],
        ]

        # Create labels and add them to the reference list...
        start_label_ref = []

        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1],
                               fg=item[2],
                               wraplength=450, justify="left", pady=10, padx=20)
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        self.num_rounds_entry = Entry(self.start_frame, font=("Arial", 20, "bold"),
                                      width=15)
        self.num_rounds_entry.grid(row=3, column=0, padx=10)

        # infinite button
        self.infinite_button = Button(self.start_frame, text="Infinite",font=("Arial", 15, "bold"),
                                      width=18, bg="#DAE8FC", height=1, command=self.inf_rounds)
        self.infinite_button.grid(row=4, column=0)

        # difficulty buttons
        self.difficulty_heading = Label(self.start_frame, text="Choose your difficulty",
                                        font=("Arial", 17, "bold"))
        self.difficulty_heading.grid(row=5, column=0)

        # make button frame so can be placed on same row
        self.diff_button_frame = Frame(self.start_frame)
        self.diff_button_frame.grid(row=6)

        # button list (frame | text | bg | command | column)
        difficulty_button_list = [
            [self.diff_button_frame, "Normal", "#d5e8d4", lambda: self.check_rounds("normal"), 0],
            [self.diff_button_frame, "Medium", "#fff2cc", lambda: self.check_rounds("medium"), 1],
        ]

        for item in difficulty_button_list:
            difficulty_button = Button(item[0], text=item[1], bg=item[2],
                                       font=("Arial", 18, "bold"), fg="#000000", command=item[3])
            difficulty_button.grid(row=0, column=item[4], padx=10, pady=10)

        # extract choice label to config into error message if needed
        self.choose_label = start_label_ref[2]

    def check_rounds(self, difficulty="normal"):
        """
        Checks users have entered 1 or more rounds
        """

        # Retrieve rounds and difficulty for Play class
        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users come back to home screen)
        self.choose_label.config(fg="#009900", font=("Arial", 12, "bold"))
        self.num_rounds_entry.config(bg="#FFFFFF")

        error = "Oops - Please choose a whole number more than zero."
        has_errors = "no"

        # checks that amount to be converted is a number above absolute zero
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                pass
                # temporary success message, replace with cell to PlayGame class
                Play(rounds_wanted, difficulty)
                root.withdraw()
            else:
                has_errors = "yes"
        except ValueError:
            has_errors = "yes"

        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000", font=("Arial", 12, "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)

    def inf_rounds(self):
        # temporary success message, replace with cell to play game class
        self.choose_label.config(text="You have chosen to play Infinite Rounds!",fg="#009900",
                                 font=("Arial", 12, "bold"))
        Play(float('inf'))
        # reset entry box (for when users come back to home screen)
        self.num_rounds_entry.config(bg="#FFFFFF")
        self.num_rounds_entry.delete(0, END)

class Play:

    def __init__(self, how_many, difficulty="normal"):

        # set up rounds for game
        self.rounds_wanted = IntVar()
        self.rounds_wanted = how_many

        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        # set up the difficulty
        self.difficulty_playing = difficulty

        # setup Play frame
        self.play_box = Toplevel()

        self.play_frame = Frame(self.play_box)
        self.play_frame.grid(padx=10, pady=10)

        # if 'x' at window is pressed, end all processes
        self.play_box.protocol('WM_DELETE_WINDOW',
                               root.destroy)

        # lists for Play labels / buttons
        all_answers = []
        control_button_ref = []
        play_label_ref = []


        # round labels list (text | bg | row | font)
        play_labels_list = [
            ["Question: X / X", None, 0, ("Arial", 20, "bold")],
            ["What Country Is This?", "#F5F5F5", 2, ("Arial", 12)],
            ["Correct! It is [answer]..", "#D5E8D4", 5, ("Arial", 12)]
        ]

        for item in play_labels_list:
            self.play_label = Label(self.play_frame, text=item[0], bg=item[1],
                                    font=item[3])
            self.play_label.grid(row=item[2])

            play_label_ref.append(self.play_label)

        # create frame for answer buttons
        self.answer_button_frame = Frame(self.play_frame)
        self.answer_button_frame.grid(row=3)

        # creating answer buttons
        for item in range(0, 6):
            self.answer_button = Button(self.answer_button_frame, text="Country",
                                       bg="#DAE8FC", font=("Arial", 15, "bold"),
                                        command=self.close_play, width=12, height=2)
            self.answer_button.grid(row=item // 2,
                                    column= item % 2,
                                    pady=2, padx=2)
            all_answers.append(self.answer_button)

        # play button list (frame, text, bg)
        play_button_list = [
            ["Next Round"]
        ]

        # create image
        round_img = "AA-Flag.gif"
        photo_path = (f"/users/afematam2360/OneDrive - Massey High School/"
                           f"Programming level 2 & 3/Flags/flag_images/{round_img}")
        image = PhotoImage(file=photo_path)

        self.image_label = Label(self.play_frame, image=image)
        self.image_label.image = image
        self.image_label.grid(row=1, padx=10, pady=10)

        # self.round_heading_label = Label(self.play_frame, text=f"Rounds: {self.rounds_played.get()}"
        #                                                        f" / {self.rounds_wanted}",
        #                                  font=("Arial", 20, "bold"))
        # if how_many == float('inf'):
        #     self.round_heading_label.config(text="Rounds: INFINITE!!!!")
        #
        # self.round_heading_label.grid(row=0, column=0)

        # setup main question button frame
        self.round_button_frame = Frame(self.play_frame)
        self.round_button_frame.grid(row=4, padx=10, pady=10)

        # for item in range(0, 4):
        #     self.round_button = Button(self.round_button_frame, text=self.country)

        # self.end_game_button = Button(self.play_frame, text="End", font=("Arial", 20, "bold"),
        #                               command=self.close_play)
        # self.end_game_button.grid(row=4, column=0)

        if difficulty == "medium":
            self.capital_button = Button(self.round_button_frame, text="im capital", command=self.capital)
            self.capital_button.grid(row=2, column=0)

    def close_play(self):
        root.deiconify()
        self.play_box.destroy()

    def capital(self):
        print("im the capital button")

# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Country Flags")
    StartGame()
    root.mainloop()