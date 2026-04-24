import tkinter as tk
from tkinter import PhotoImage

# Create the main window
parent = tk.Tk()
parent.title("Image in Tkinter")

# Load the image
photo_path = "/users/afematam2360/OneDrive - Massey High School/Programming level 2 & 3/Flags/flag_images/AA-Flag.gif"
image = PhotoImage(file=photo_path)


# Create a label to display the image
image_label = tk.Label(parent, image=image)
image_label.pack()

# Start the Tkinter event loop
parent.mainloop()