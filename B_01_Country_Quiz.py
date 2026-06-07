import csv
import random
from tkinter import *
from functools import partial  # To prevent unwanted windows
from PIL import Image, ImageTk


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

        # Strings for labels
        intro_string = (
            "In each round you will have to guess the flag of a country (or capital if a harder difficulty is chosen). "
            "\n\nYour goal is to correctly guess the country and win the round with your knowledge!"
            "\n\nTo begin, please enter how many questions you'd like and then choose your difficulty.")

        choose_string = "How many questions do you want?"

        # list of labels to be made (text | font | fg | relief)
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

        self.num_questions_entry = Entry(self.start_frame, font=("Arial", 20, "bold"),
                                         width=15)
        self.num_questions_entry.grid(row=3, column=0, padx=10)

        # infinite button
        self.infinite_button = Button(self.start_frame, text="Infinite", font=("Arial", 15, "bold"),
                                      width=18, bg="#DAE8FC", height=1, command=self.inf_questions)
        self.infinite_button.grid(row=4, column=0)

        # initialise infinite questions
        self.infinite_questions = "no"
        self.num_questions_entry.config(state='normal')

        # difficulty buttons
        self.difficulty_heading = Label(self.start_frame, text="Choose your difficulty",
                                        font=("Arial", 17, "bold"))
        self.difficulty_heading.grid(row=5, column=0)

        # make button frame so can be placed on same row
        self.diff_button_frame = Frame(self.start_frame)
        self.diff_button_frame.grid(row=6)

        # button list (frame | text | bg | command | column)
        difficulty_button_list = [
            [self.diff_button_frame, "Normal", "#d5e8d4", lambda: self.check_questions("normal"), 0],
            [self.diff_button_frame, "Medium", "#fff2cc", lambda: self.check_questions("medium"), 1],
        ]

        for item in difficulty_button_list:
            difficulty_button = Button(item[0], text=item[1], bg=item[2],
                                       font=("Arial", 18, "bold"), fg="#000000", command=item[3])
            difficulty_button.grid(row=0, column=item[4], padx=10, pady=10)

        # extract choice label to config into error message if needed
        self.choose_label = start_label_ref[2]

    def check_questions(self, difficulty="normal"):
        """
        Checks users have entered 1 or more questions
        """

        # Retrieve questions and difficulty for Play class
        questions_wanted = self.num_questions_entry.get()

        if self.infinite_questions == "yes":
            questions_wanted = float('inf')

        # Reset label and entry box (for when users come back to home screen)
        self.choose_label.config(fg="#009900", font=("Arial", 12, "bold"))
        self.num_questions_entry.config(bg="#FFFFFF")

        error = "Oops - Please choose a whole number more than zero."
        has_errors = "no"

        # checks that amount to be converted is a number above absolute zero
        try:
            if self.infinite_questions == "no":
                questions_wanted = int(questions_wanted)
            if questions_wanted > 0:
                Play(questions_wanted, difficulty)
                root.withdraw()
            else:
                has_errors = "yes"
        except ValueError:
            has_errors = "yes"

        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000", font=("Arial", 12, "bold"))
            self.num_questions_entry.config(bg="#F4CCCC")
            self.num_questions_entry.delete(0, END)

    def inf_questions(self):
        """
        Enables infinite questions when 'infinite' button is pressed
        """
        if self.infinite_questions == "no":
            self.infinite_questions = "yes"
            self.num_questions_entry.config(state='disabled', bg="#FFFFFF")
            self.choose_label.config(text="You've chosen infinite questions!", fg="#009900")

        else:
            self.infinite_questions = "no"
            self.num_questions_entry.config(state='normal', bg="#FFFFFF")
            self.choose_label.config(text="How many questions do you want to answer?", fg="#009900")


class Play:
    """
    Initial Play interface
    (checks how many questions)
    """

    def __init__(self, how_many, difficulty="normal"):
        # Integers / String Variables
        self.points_penalised = 0
        self.reroll_counter = 0
        self.hints_counter = 0
        self.country_streak = 0
        self.capital_streak = 0
        self.target_country = ""
        self.target_capital = ""
        self.country_flag = ""
        self.country_code = ""

        # Lists for stats
        self.all_stats_list = []
        self.country_details = []

        # set up how many questions...
        self.questions_answered = IntVar()
        self.questions_answered.set(0)

        if how_many == float('inf'):
            self.questions_wanted = "Infinite"
        else:
            self.questions_wanted = IntVar()
            self.questions_wanted.set(how_many)

        self.correct_guesses = IntVar()

        # set up the difficulty
        self.difficulty_playing = difficulty

        # setup Play frame
        self.play_box = Toplevel()

        self.play_frame = Frame(self.play_box)
        self.play_frame.grid(padx=10, pady=10)

        # if 'x' at window is pressed, end all processes
        self.play_box.protocol('WM_DELETE_WINDOW',
                               root.destroy)

        # list for Play labels / buttons
        self.question_country_list = []
        self.question_type = "country"

        # font used for most labels / buttons
        default_font = ("Arial", 12)

        # round labels list (text | bg | row | font | relief | width)
        play_labels_list = [
            ["Question: X / X", None, 0, ("Arial", 20, "bold"), None],
            ["What Country Is This?", "#F5F5F5", 2, default_font, 25],
            ["Correct! It is [answer]..", "#D5E8D4", 6, default_font, None]
        ]

        play_label_ref = []
        for item in play_labels_list:
            self.play_label = Label(self.play_frame, text=item[0], bg=item[1],
                                    font=item[3], bd=2, width=item[4])
            self.play_label.grid(row=item[2], pady=3, padx=5)

            play_label_ref.append(self.play_label)

        # retrieve labels to configured later
        self.heading_label = play_label_ref[0]
        self.question_label = play_label_ref[1]
        self.result_label = play_label_ref[2]

        # create frame for answer buttons
        self.country_button_frame = Frame(self.play_frame)
        self.country_button_frame.grid(row=3)

        self.country_button_ref = []

        # creating country buttons
        for item in range(0, 4):
            self.country_button = Button(self.country_button_frame, text="Country",
                                         bg="#DAE8FC", font=("Arial", 15, "bold"),
                                         command=partial(self.question_outcome, item), width=12, height=2,
                                         wraplength=150, justify="center")
            self.country_button.grid(row=item // 2,
                                     column=item % 2,
                                     pady=2, padx=2)
            self.country_button_ref.append(self.country_button)

        # setup main control button frame
        self.control_button_frame = Frame(self.play_frame)
        self.control_button_frame.grid(row=8, padx=10, pady=10)

        # control button list (frame, text, bg, row, column, font, command, width)
        control_button_list = [
            [self.play_frame, "Next Question", "#FFF2CC", 7, 0, ("Arial", 16, "bold"), self.new_question, 20],
            [self.control_button_frame, "Help", "#ADD8E6", 0, 0, ("Arial", 13, "bold"), self.to_hints, 12],
            [self.control_button_frame, "Stats", "#F5F5F5", 0, 1, ("Arial", 13, "bold"), self.to_stats, 12],
            [self.play_frame, "End Quiz", "#F8CECC", 9, 0, ("Arial", 16, "bold"), self.close_quiz, 20]
        ]

        control_button_ref = []
        for item in control_button_list:
            self.control_button = Button(item[0], text=item[1], bg=item[2], font=item[5], command=item[6],
                                         width=item[7])
            self.control_button.grid(row=item[3], column=item[4], padx=5, pady=2)
            control_button_ref.append(self.control_button)

        # extract buttons to configure later
        self.next_question = control_button_ref[0]
        self.hints_button = control_button_ref[1]
        self.stats_button = control_button_ref[2]
        self.end_game_button = control_button_ref[3]

        # add the capital & reroll buttons when
        # medium difficulty is selected
        if difficulty == "medium":
            self.capital_reroll_frame = Frame(self.play_frame)
            self.capital_reroll_frame.grid(row=5)

            self.capital_button = Button(self.country_button_frame, text="Capital",
                                         command=self.capital, width=16, height=2,
                                         font=default_font, bg="#E1D5E7")
            self.capital_button.grid(row=5, column=0, padx=10, pady=10)

            self.reroll_button = Button(self.country_button_frame, text="Reroll",
                                        command=self.reroll,
                                        font=default_font, width=16, height=2, bg="#FFFFFF")
            self.reroll_button.grid(row=5, column=1, padx=10, pady=10)

        # start new round after GUI has been set up
        self.new_question()

    def new_question(self):

        """
        Start a new question for the Play GUI
        (configure Play buttons and labels)
        """

        # retrieve number of questions answered and add one to the heading
        questions_answered = self.questions_answered.get()
        self.questions_answered.set(questions_answered)

        # check for infinite rounds
        if "Infinite" == self.questions_wanted:
            questions_wanted = "Infinite"
        else:
            questions_wanted = self.questions_wanted.get()

        # extract country info for round variables
        self.question_country_list = get_country()

        # testing and shuffling for the questions
        shuffle = random.randint(0, 3)

        # set up target country / capital
        self.target_country = self.question_country_list[shuffle][0]
        self.target_capital = self.question_country_list[shuffle][1]
        self.country_code = self.question_country_list[shuffle][2]
        self.country_flag = self.question_country_list[shuffle][3]

        # Gather this question's country details for help and for stats
        self.country_details = [self.target_country, self.target_capital, self.country_code, self.country_flag]

        # create flag image for the question
        photo_path = (f"/users/afematam2360/OneDrive - Massey High School/"
                      f"Programming level 2 & 3/Flags/flag_images/{self.country_flag}")
        image = Image.open(f"{photo_path}")
        resized_image = image.resize((250, 150))
        img = ImageTk.PhotoImage(resized_image)

        image_label = Label(self.play_frame, image=img)

        # create reference so image isn't deleted
        image_label.image = img
        image_label.grid(row=1)

        # enable stats when user has completed a round
        if questions_answered >= 1:
            self.stats_button.config(state="normal")
        else:
            self.stats_button.config(state="disabled")

        # change question type back to capital to get country names for next question
        if self.difficulty_playing == "medium":
            self.question_type = "capital"
            self.capital()

            self.capital_button.config(state="normal")

        # Configuration area for control / country buttons
        self.heading_label.config(text=f"Question: {questions_answered} / "
                                       f"{questions_wanted}")
        self.result_label.config(text=f"{'=' * 20}", bg="#F0F0F0")
        self.next_question.config(state="disabled")

        for count, item in enumerate(self.country_button_ref):
            item.config(text=self.question_country_list[count][0], bg="#DAE8FC",
                        state="normal")

    def question_outcome(self, user_choice):
        """
        Checks the users answers and updates stats
        based on their results, checks for streak
        """

        # gets what the user picked, used to compare later
        answer = self.country_button_ref[user_choice].cget('text')

        # disable main question buttons / other control buttons
        # enable next rounds for user to continue
        for item in self.country_button_ref:
            item.config(state="disabled")
            self.next_question.config(state="normal", text="Next Question")

            if self.difficulty_playing == "medium":
                self.capital_button.config(state="disabled")

        # Compare the user choice (answer) with target country or capital for the question
        if answer == self.target_country:
            self.result_label.config(text=f"Correct! The {self.question_type} is {self.target_country}.", bg="#D5E8D4")
            self.country_button_ref[user_choice].config(bg="#D5E8D4")
            self.country_streak += 1
        elif answer == self.target_capital:
            self.result_label.config(text=f"Correct! The {self.question_type} is {self.target_capital}.", bg="#D5E8D4")
            self.country_button_ref[user_choice].config(bg="#D5E8D4")
            self.capital_streak += 1

        elif self.question_type == "capital" and answer != self.target_capital:
            self.result_label.config(text=f"Incorrect, the {self.question_type} is {self.target_capital}.",
                                     bg="#E8D4D4")
            self.country_button_ref[user_choice].config(bg="#E8D4D4")
            self.capital_streak = 0
        else:
            self.result_label.config(text=f"Incorrect, the {self.question_type} is {self.target_country}.",
                                     bg="#E8D4D4")
            self.country_button_ref[user_choice].config(bg="#E8D4D4")
            self.country_streak = 0

        # Add 1 to the number of questions answered
        questions_answered = self.questions_answered.get()
        questions_answered += 1
        self.questions_answered.set(questions_answered)

        if self.questions_wanted == "Infinite":
            pass
        else:
            questions_wanted = self.questions_wanted.get()

            if questions_answered == questions_wanted:
                self.heading_label.config(text=f"Question: {questions_answered} / {questions_wanted}")
                self.next_question.config(state='disabled', text="Quiz finished!")

        # update country details with new info
        # Country | Capital | Difficulty | Hints | No. of questions | Country Streak | Capital Streak
        self.all_stats_list = [self.country_details, self.difficulty_playing,
                               self.hints_counter, questions_answered, self.country_streak, self.capital_streak]

    def close_quiz(self):
        """Closes the Play GUI"""

        # destroy play GUI and go back to StartGame GUI
        root.deiconify()
        self.play_box.destroy()

    def capital(self):
        """
        Converts country buttons on the question
        to their capitals
        """

        if self.question_type == "capital":
            self.question_type = "country"
            self.question_label.config(text="What Country Is This?")
            self.capital_button.config(text="Capital", bg="#E1D5E7")

            for count, item in enumerate(self.country_button_ref):
                item.config(text=self.question_country_list[count][0], bg="#DAE8FC")
        else:
            # for testing, question_type serves to help for reroll
            self.question_type = "capital"
            self.question_label.config(text="What's the capital of this country?")
            self.capital_button.config(text="Country", bg="#DAE8FC")
            self.next_question.config(text="Answer this first!", state="disabled")

            for count, item in enumerate(self.country_button_ref):
                item.config(text=self.question_country_list[count][1], bg="#E1D5E7")

    def reroll(self):
        """
        Rerolls the country question for the user
        """
        # update the reroll button and start a new question
        self.reroll_counter += 1
        print(self.reroll_counter, "<< reroll times")
        self.points_penalised -= 1
        print(self.points_penalised, "<< points penalised")

        self.new_question()

        self.result_label.config(text=f"You have rerolled x{self.reroll_counter} times.."
                                      f"\nPoints penalised: {self.points_penalised}.")

        # penalise points for rerolling
        # PLACEHOLDER

    def to_hints(self):
        # Displays Help GUI and retrieves difficulty
        self.hints_counter += 1
        questions_answered = self.questions_answered.get()

        # Country | Capital | Difficulty | Hints | No. of questions | Country Streak | Capital Streak

        Help(self, self.target_capital, self.country_flag,
             self.country_code, self.difficulty_playing, self.hints_counter, questions_answered)

    def to_stats(self):
        # Displays Stats (with stats list for the question)

        Stats(self, self.all_stats_list)


class Stats:
    """
    Initial Stats GUI
    (Shows user the country and capital if needed)
    """

    def __init__(self, partner, all_stats):

        # set up help window and background
        background = '#FFFFFF'
        self.stats_box = Toplevel()

        # if 'x' at window is pressed, end all processes
        self.stats_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_stats, partner))

        # disable buttons
        partner.hints_button.config(state="disabled")
        partner.end_game_button.config(state="disabled")
        partner.stats_button.config(state="disabled")

        self.stats_frame = Frame(self.stats_box, width=500, height=200)
        self.stats_frame.grid()

        self.stats_frame.config(bg=background)

        # retrieve necessary stats for the strings and labels
        target_country = all_stats[0]
        target_capital = all_stats[1]
        difficulty_playing = all_stats[4]
        hint_count = all_stats[5]
        questions_answered = all_stats[6]
        country_streak = all_stats[7]
        capital_streak = all_stats[8]

        # Fonts for strings
        heading_font = ("Arial", 25, "bold")
        answer_font = ("Arial", 25)
        body_font = ("Arial", 15)
        round_font = ("Arial", 20, "bold")

        # Strings for the stats labels...

        question_stats_string = (f"\nDifficulty: {difficulty_playing}"
                              f"\nQuestions Answered: {questions_answered}"
                              f"\nHints Used: {hint_count}")
        country_streak_string = f"Countries: {country_streak}\n"
        capital_streak_string = ("Capitals: N/A\nPlay on higher difficulties to have a go at\n"
                                 "guessing the capitals!")

        # check if difficulty is medium, update capitals to be enabled..
        if difficulty_playing == "medium":
            capital_streak_string = f"Capitals: {capital_streak}\n"

        # update strings when there's a streak
        if country_streak > 2:
            country_streak_string = f"You're on a guessing roll! {country_streak} in a row.."

        if capital_streak > 2:
            capital_streak_string = f"You're on a guessing roll here too! {capital_streak} in a row.."


        # stats labels list (text | row | font | sticky)
        stats_labels_list = [
            ["Statistics", heading_font, "W"],
            [question_stats_string, body_font, "W"],
            [f"\nThis question's country was..",  round_font, "W"],
            [target_country, answer_font, "nsew"],
            [f"This Capital of this country is..",  round_font, "W"],
            [target_capital, answer_font, "nsew"],
            [country_streak_string, body_font, "W"],
            [capital_streak_string, body_font, "W"]

        ]

        recolour_list = []

        for count, item in enumerate(stats_labels_list):
            hint_label = Label(self.stats_frame, text=item[0], font=item[1], justify="left")
            hint_label.grid(row=count, column=0, sticky=item[2], padx=10)
            recolour_list.append(hint_label)


        for item in recolour_list:
            item.config(bg=background, fg="#333333")

        # close button
        self.close_button = Button(self.stats_frame,
                                   font=("Arial", 16, "bold"),
                                   text="Close", bg="#333333",
                                   fg="#FFFFFF", width=20,
                                   command=partial(self.close_stats, partner))
        self.close_button.grid(row=10, padx=10, pady=20)







    def close_stats(self, partner):
        """Closes the Stats GUI"""
        # put hint button state to normal
        partner.hints_button.config(state="normal")
        partner.end_game_button.config(state="normal")
        partner.stats_button.config(state="normal")

        # destroy play GUI and go back to StartGame GUI
        self.stats_box.destroy()



class Help:
    """
    Initial Help GUI
    (Gives users a hint to the country by providing
    flag codes. Capital is given on lower difficulties )
    """

    def __init__(self, partner, capital, image, code, difficulty, hint_count, questions_answered):

        # Get variables to be used for later
        self.questions_answered = questions_answered

        # set up help window and background
        background = '#ADD8E6'
        self.help_box = Toplevel()

        # if 'x' at window is pressed, end all processes
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_hints, partner))

        # disable buttons
        partner.hints_button.config(state="disabled")
        partner.end_game_button.config(state="disabled")
        partner.stats_button.config(state="disabled")


        # set up help frame
        help_frame = Frame(self.help_box, width=500, height=200)
        help_frame.grid()

        help_frame.config(bg=background)

        # Image area
        photo_path = (f"/users/afematam2360/OneDrive - Massey High School/"
                      f"Programming level 2 & 3/Flags/flag_images/{image}")
        image = Image.open(f"{photo_path}")
        resized_image = image.resize((250, 150))
        img = ImageTk.PhotoImage(resized_image)

        image_label = Label(help_frame, image=img, bg=background)

        # create reference so image isn't deleted
        image_label.image = img
        image_label.grid(row=3)

        # Help Labels list (text | row | font | sticky)
        help_labels_list = [
            ["Hints", 0, ("Arial", 20), "w"],
            [f"You have used {hint_count} Hint/s...", 2, ("Arial", 15), "W"],
            [f"\nFlag code of this country:\n{code}", 4, ("Arial", 15, "bold"), None],
            [f"\nCapital of this country:\n{capital}", 6, ("Arial", 15, "bold"), None],
        ]

        if difficulty == "medium":
            help_labels_list.pop(3)

        recolour_list = []

        for item in help_labels_list:
            hint_label = Label(help_frame, text=item[0], font=item[2], wraplength=350)
            hint_label.grid(row=item[1], column=0, sticky=item[3], padx=10, pady=10)
            recolour_list.append(hint_label)

        for item in recolour_list:
            item.config(bg=background)

    #close_button = Button(help_frame, font=("Arial", 16, "bold"), text="Close", bg="#333333", fg="#FFFFFF", width=20, command=partial(self.close_hints, partner))
    #close_button.grid(row=10, padx=10, pady=20)

    def close_hints(self, partner):
        """Closes the Help GUI"""
        # put hint button state to normal
        partner.hints_button.config(state="normal")
        partner.end_game_button.config(state="normal")

        if self.questions_answered > 1:
            partner.stats_button.config(state="normal")

        # destroy play GUI and go back to StartGame GUI
        self.help_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Country Flags")
    StartGame()
    root.mainloop()