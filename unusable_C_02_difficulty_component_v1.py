from tkinter import *
from functools import partial # To prevent unwanted windows

class StartGame:
    """ Initial Game interface (asks users how many rounds they
    would like to play) """

    def __init__(self):
        """ Gets number of rounds from user """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        self.difficulty_button = Button(self.start_frame, text="Difficulty", bg="#D5E8D4", fg="#000000",
                                        font=("Arial", 20, "bold"), command=self.to_diff)
        self.difficulty_button.grid(row=0, padx=10, pady=10)

    def to_diff(self):
        """
        Displays difficulty for questions before playing game
        :return:
        """
        DisplayDiff(self)

class DisplayDiff:

    def __init__(self, partner):

        # setup difficulty box
        self.difficulty_box = Toplevel()

        # disable difficulty button
        partner.difficulty_button.config(state=DISABLED)

        # if users press 'x' on window, closes difficulty and releases
        # difficulty button
        self.difficulty_box.protocol('WM_DELETE_WINDOW',
                                     partial(self.close_diff, partner))

        self.difficulty_frame = Frame(self.difficulty_box, width=300, height=200)
        self.difficulty_frame.grid()

        # make button frame so can be placed on same row
        self.diff_button_frame = Frame(self.difficulty_frame)
        self.diff_button_frame.grid(row=1)

        # button list (frame | text | bg | command | column)
        difficulty_button_list = [
            [self.diff_button_frame, "Easy", "#d5e8d4", self.close_diff, 0],
            [self.diff_button_frame, "Medium", "#fff2cc", self.close_diff, 1],
            [self.diff_button_frame, "Hard", "#f8cecc", self.close_diff, 2]
        ]

        for item in difficulty_button_list:
            difficulty_button = Button(item[0], text=item[1], bg=item[2],
                                       font=("Arial", 20, "bold"), fg="#000000", command=item[3])
            difficulty_button.grid(row=0, column=item[4], padx=10, pady=10)

        self.difficulty_heading = Label(self.difficulty_frame, text="Choose your difficulty",
                                        font=("Arial", 20, "bold"))
        self.difficulty_heading.grid(row=0, column=0)

    def close_diff(self, partner):
        """
        closes diff. box ( enables diff. button)
        """
        # put diff. button to normal
        partner.difficulty_button.config(state=NORMAL)
        self.difficulty_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Country Flags")
    StartGame()
    root.mainloop()