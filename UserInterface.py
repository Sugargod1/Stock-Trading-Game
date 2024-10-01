######################################################################
# Authors: Sugarragchaa Tumur-Ochir
# Username: Sugargod1
#
# P1: Final project
#
# Purpose: Testing the stock.py file fruitful functions
# ######################################################################
# Acknowledgements:
#
#
# licensed under a Creative Commons
# Attribution-Noncommercial-Share Alike 3.0 United States License.
####################################################################################

import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import stock_display as stock


class UserInterface:
    """
        Class for creating the user interface.
    """

    def __init__(self, master, stock_option):
        """
            Initialize the UserInterface class.

        Args:
            master (tk.Tk): The root window.
            stock_option (str): The stock option to display which has many things such as current price of tock.
        """
        # Initialize attributes
        self.master = master
        self.stock_display = stock.StockDisplay(master, stock_option)
        self.display = self.stock_display.display
        self.running = True
        self.initial = 1000  # the money they start with balance variable
        self.current = 0    # current money variable
        self.retire = False
        self.array1 = []    # for storing stonks current price
        self.array2 = []    # for storing money spend each time buying stocks
        self.array3 = []    # for the retire button in order to store how much money they made
        self.styles = []    # for storing all those colors for buttons
        self.buttons = []   # for storing all the buttons
        self.separators = []   # for storing separators
        self.image1 = ImageTk.PhotoImage(Image.open("image/canvas.jpg"))    # storing the image for retirement canvas
        self.canvas = tk.Canvas(self.master)    # first canvas for stocks
        self.canvas2 = tk.Canvas(self.master, width=400, height=400, bg="white")    # second canvas for retirement
        self.label1 = tk.Label()
        self.label2 = tk.Label()
        # Set up the root window
        master.title('Stonks')  # Title of the window
        master.geometry('800x500+500+250')  # Defining it's size

        # Define a grid of 30x20
        for i in range(30):
            master.columnconfigure(i, weight=1)
        for i in range(20):
            master.rowconfigure(i, weight=1)

        # Calling function to Create Widgets
        self.create_widgets(master)

        # Calling function to placing the widgets
        self.place_widgets()

    def create_widgets(self, master):
        """Create all the widgets for the user interface.

        Args:
            master (tk.Tk): The root window.
        """
        # Define button colors and commands
        colors = ['#FF5733', '#33FF57', '#3357FF', '#FFFF33', '#FF33FF']  # Example vibrant colors
        # the commands which we are going to assign it into each button
        commands = [self.buy_action, self.sell_action, self.retire_action, self.pause_action, self.resume_action]

        # Create button styles
        for color in range(len(commands)):
            style = ttk.Style()
            style.configure(f'Button{len(self.styles) + 1}.TButton', background=colors[color], foreground='black',
                            font=("Helvetica", 12))
            self.styles.append(style)

        # Create buttons
        for i, text in enumerate(['Buy', 'Sell', 'Retire', 'Pause', 'Resume']):
            button = ttk.Button(master, text=text, style=f'Button{i + 1}.TButton', command=commands[i])
            self.buttons.append(button)

        # Create separators
        for i in range(4):
            sep = ttk.Separator(master, orient='horizontal')
            self.separators.append(sep)
        sep6 = ttk.Separator(master, orient='vertical')
        self.separators.append(sep6)

        # Create labels
        self.label1 = tk.Label(text="Initial value", fg="darkblue", bg="lightblue", font=("Helvetica", 12, "bold"))
        self.label2 = tk.Label(text="Current value", fg="darkblue", bg="lightblue", font=("Helvetica", 12, "bold"))

        # First Canvas
        self.canvas = self.display

        # Second Canvas
        self.canvas2 = tk.Canvas(master, width=400, height=400, bg="white")
        self.canvas2.pack_forget()  # Initially hide the second canvas
        self.canvas2.create_image(400, 200, image=self.image1)
        sum2_text = "Wow you made" + str(1) + " dollars. If you want to play again, exit and run again"
        self.canvas2.create_text(10, 100, anchor="w", text=sum2_text, font=("Helvetica", 12, "bold"), fill="white")

    def place_widgets(self):
        """
            Place all the widgets on the grid.
        """
        # SEPARATORS
        for i, sep in enumerate(self.separators[:4]):
            sep.grid(row=i * 2 + 3, column=0, columnspan=4, sticky='ew')
        self.separators[3].grid(row=18, column=0, columnspan=30, sticky='ew')
        self.separators[4].grid(row=0, column=4, rowspan=13, sticky='ns')

        # BUTTONS
        self.buttons[0].grid(row=2, column=0, rowspan=1, columnspan=1, sticky="nsew")
        self.buttons[1].grid(row=4, column=0, rowspan=1, columnspan=1, sticky="nsew")
        self.buttons[2].grid(row=6, column=0, rowspan=1, columnspan=1, sticky="nsew")
        self.buttons[3].grid(row=19, column=9, rowspan=1, columnspan=1, sticky="nsew")
        self.buttons[4].grid(row=19, column=10, rowspan=1, columnspan=1, sticky="nsew")

        # Canvas with Image
        self.canvas.grid(column=5, columnspan=25, row=0, rowspan=18, sticky='nsew')

        # LABELS
        self.label1.grid(row=8, column=0, columnspan=3, sticky="nsew")
        self.label2.grid(row=10, column=0, columnspan=3, sticky="nsew")

    def buy_action(self):
        """
            Action for the Buy button.
        """
        # Each time button pressed we add money to array
        if self.initial >= self.stock_display.current_value:
            if self.initial >= 30:
                self.initial -= self.stock_display.current_value
                self.array2.append(self.stock_display.current_value)
                self.array1.append(round(self.stock_display.current_value, 4))
            else:
                self.array2.append(self.initial)
                self.initial = 0
                self.array1.append(round(self.stock_display.current_value, 4))

    def sell_action(self):
        """
            Action for the Sell button.
        """
        # Adds money to balance and clears everything stored
        self.initial += self.current
        self.array1 = []
        self.array2 = []
        self.current = 0

    def retire_action(self):
        """
            Action for the Retire button.
        """
        self.canvas.grid_forget()  # Hide the first canvas
        self.array3.append(round(self.current + self.initial - 1000, 5))

        # Create a new Canvas 2
        self.canvas2.create_image(400, 200, image=self.image1)
        self.array1 = []
        self.array2 = []
        self.initial = 0
        self.current = 0
        self.running = False
        self.retire = True
        # Update the text on Canvas 2
        sum2_text = f"Wow you made {self.array3[0]} dollars. If you want to play again, exit and run again"
        self.canvas2.create_text(10, 100, anchor="w", text=sum2_text, font=("Helvetica", 12, "bold"), fill="white")

        # Show the new Canvas 2
        self.canvas2.grid(row=0, column=5, columnspan=25, rowspan=18, sticky='nsew')

    def pause_action(self):
        """Action for the Pause button."""
        self.running = False

    def update_labels(self, initial_value, current_value):
        """
        Update the labels with new values.

        Args:
            initial_value : The initial value.
            current_value : The current value.
        """
        self.label1.config(text=f"Balance: {round(initial_value, 2)}$")
        self.label2.config(text=f"Stock portfolio: {round(current_value, 2)}$")
        sumofarray2 = 0
        for i in self.array2:
            sumofarray2 += i
        # Change label color based on condition
        if initial_value > 0:
            self.label1.config(fg="green")
        else:
            self.label1.config(fg="red")

        if current_value > sumofarray2:
            self.label2.config(fg="green")
        else:
            self.label2.config(fg="red")

    def resume_action(self):
        """
            Action for the Resume button.
        """
        self.running = True


def main():
    """
        Main function to run the application.
    """
    root = tk.Tk()
    ui = UserInterface(root, "AMZN")
    sum1 = 0
    while True:
        for i in range(len(ui.array1)):
            sum1 += ui.array2[i] / ui.array1[i] * round(ui.stock_display.current_value, 4)
        ui.current = sum1
        sum1 = 0
        if ui.running:
            ui.stock_display.movement()     # updates stock display
            ui.stock_display.update_display()   # updates stock display
        # After pressing retire button terminating to play again
        if ui.retire:
            ui.label1.config(text="Hey you should never think")
            ui.label2.config(text="about trading again")
        else:
            ui.update_labels(ui.initial, round(ui.current, 5))
        root.update()  # Update the Tkinter event loop
        time.sleep(0.1)  # Add a small delay to avoid consuming too much CPU and control how fast stock going


if __name__ == "__main__":
    main()
