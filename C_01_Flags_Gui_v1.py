from tkinter import *
from functools import partial # To prevent unwanted windows

class StartGame:
    """ Initial Game interface (asks users how many rounds they
    would like to play) """

    def __init__(self):
        """ Gets number of rounds from user """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Strings for labels
        intro_string = ("In each round you will have to guess the flag of a country (or capital if a harder difficulty is chosen). \n\nYour goal is to correctly guess the capital of a country and win the round."
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

        # Frame button area to hold 'play' and 'difficulty' buttons
        self.play_area_frame = Frame(self.start_frame)
        self.play_area_frame.grid(row=5)

        self.difficulty_heading = Label(self.play_area_frame, text="Choose your diffculty",
                                        font=("Arial", 30, "bold"))
        self.difficulty_heading.grid(row=0, column=0)

        # start button list (frame | text | bg | width | row | column | command)
        start_button_list = [
            [self.start_frame, "Infinite", "#D2E2D3", 12, 4, 0, self.inf_rounds],
            [self.play_area_frame, "Easy", "#d5e8d4", 5, 1, 1, self.check_rounds("easy")],
            [self.play_area_frame, "Medium", "#fff2cc", 7, 1, 2, self.check_rounds("medium")],
            [self.play_area_frame, "Hard", "#f8cecc", 5, 1, 3, self.check_rounds("hard")]
        ]

        for item in start_button_list:
            start_button = Button(item[0], text=item[1], font=("Arial", 20, "bold"),
                                  bg=item[2], fg="#000000", width=item[3], command=item[6])
            start_button.grid(row=item[4], column=item[5], padx=5, pady=5)

        # extract choice label to config into error message if needed
        # extract diff. button to disable prevent multiple windows when pressed
        self.choose_label = start_label_ref[2]
        self.difficulty_button = start_button_list[2]

    def check_rounds(self, difficulty):
        """
        Checks users have entered 1 or more rounds
        """

        # Retrieve temperature to be converted
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
                # temporary success message, replace with cell to PlayGame class
                self.difficulty_chosen = print(difficulty)
                self.choose_label.config(text=f"You have chosen to play {rounds_wanted} round/s")
            else:
                has_errors = "yes"
        except ValueError:
            has_errors = "yes"

        if has_errors == "yes":

            self.choose_label.config(text=error, fg="#990000",
                                     font=("Arial", 12, "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)

    def inf_rounds(self):
        # temporary success message, replace with cell to play game class
        self.choose_label.config(text="You have chosen to play Infinite Rounds!",fg="#009900",
                                 font=("Arial", 12, "bold"))

        # reset entry box (for when users come back to home screen)
        self.num_rounds_entry.config(bg="#FFFFFF")
        self.num_rounds_entry.delete(0, END)
#
# class Play:
#
#     def __init__(self, how_many, difficulty):
#         pass
#


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Country Flags")
    StartGame()
    root.mainloop()