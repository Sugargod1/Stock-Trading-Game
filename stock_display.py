######################################################################
# Authors: Steven Lintelman-Nader
# Username: CollegeSteven
#
# T12: Events and GUIs
#
# Purpose: Show interactive DNA strand copying using the turtle library.
#  This program also uses both mouse click and keypress event handling.
#  The mouse click causes the complementary nucleotides to appear under
#  the base that the user clicks on in the DNA strand.
# ######################################################################
# Acknowledgements:
#
# Original code written by Dr. Mario Nakazawa
# Previously modified by Scott Heggen and Brian Schack
#
# https://www.geeksforgeeks.org/creating-a-labelframe-inside-a-tkinter-canvas/ - How I updated the display for UI elements
# https://docs.python.org/3.3/library/functions.html#zip - found a way to loop over two different lists at once
#
#
# licensed under a Creative Commons
# Attribution-Noncommercial-Share Alike 3.0 United States License.
####################################################################################
import time
from turtle import RawTurtle
import tkinter as tk
import yfinance as yahooFinance


class DisplayCoordinates:
    def __init__(self, stock_option):
        self.stock_option = stock_option
        self.stock_ticker = yahooFinance.Ticker(stock_option)
        self.stock_values = self.get_stock_value()

    def get_stock_value(self):
        """
        Grabs a list of the stock valuations of the stock_option for the object
        :return:
        """
        day_info = self.stock_ticker.history(period="30d", interval="5m")
        stock_high = day_info['High']
        return stock_high.to_list()

    def stock_values_to_positional(self, display_height, display_width):
        """
        translates the instance's list of stock values into (x,y) coordinates
        :param display_height: the tk window height
        :param display_width: the tk window width
        :return:
        """
        lowest = min(self.stock_values)
        highest = max(self.stock_values)

        x_list = self.make_x_coordinate_list(len(self.stock_values), display_width)

        new_values = []

        for x, stock_value in zip(x_list, self.stock_values):
            y = self.short_from_minmax_bounds(lowest, highest, stock_value) * display_height - display_height / 2
            new_values.append((x, y))

        return new_values

    def make_x_coordinate_list(self, list_size, win_width):
        """
        partitions x coordinates for each place on a given x axis
        :param list_size: size of a list of values
        :param win_width: display window width
        :return:
        """
        each_day = list_size / 30
        each_length = win_width / each_day
        x_list = []
        for i in range((win_width // int(each_length)) + 1):
            x_list.append(-win_width / 2 + (i * int(each_length)))
        return x_list * 30

    def short_from_minmax_bounds(self, min_value, max_value, num):
        """
        takes in a minimum, maximum, and number value and divides the surplus value from the minimum by the delta of the
        min and max values
        :param min_value:
        :param max_value:
        :param num:
        :return:
        """
        return (num - min_value) / (max_value - min_value)


class StockDisplay:
    def __init__(self, root, stock_option, display_size=(540, 360)):

        # Initial state variables
        self.running = True
        self.root = root
        self.current_value = None
        self.step = 0

        # initialize display variables
        self.display_width = display_size[0]
        self.display_height = display_size[1]
        self.display = tk.Canvas(self.root, height=self.display_height, width=self.display_width, bg="white")
        # self.display.pack()

        # StockCoordinate setup
        self.stock_info = DisplayCoordinates(stock_option)
        self.stock_info.get_stock_value()
        self.position_list = self.stock_info.stock_values_to_positional(self.display_height, self.display_width)

        # initialized turtle variables
        self.ticker_line = RawTurtle(self.display)
        self.initial_ticker_default()

        # Initial display variables
        self.day = 0
        self.labelvar = None
        self.setup_display("Arial")

    def initial_ticker_default(self):
        """
        Sets the initial state of the ticker turtle
        :return:
        """
        self.ticker_line.speed(0)
        self.ticker_line.hideturtle()
        self.ticker_line.teleport(-self.display_width / 2, 0)
        self.ticker_line.color("red")

    def update_display(self):
        """
        Sets the values of the current_value, day, and stock_option
        :return:
        """
        self.labelvar.set("Current Value: " + str(round(self.current_value, 3)) + "   " + "Day: " + str(
            self.day) + "  " + self.stock_info.stock_option)

    def setup_display(self, font_option):
        """
        Sole purpose of creating a tkinter label within the stock display
        :return:
        """
        # Initial text value
        self.labelvar = tk.StringVar(value="Starting Up...")

        # Creating and displaying a LabelFrame
        label = tk.Label(self.display, textvariable=self.labelvar, font=(font_option, 14), bg="White")
        label.pack()

        # Displaying and resizing of LabelFrame inside Canvas
        self.display.create_window(-250, -(self.display_height / 2) + 40, window=label, anchor='w')

        self.display.config(bg="white")

    def movement(self):
        """
        This simulates exactly one interation of the stock movement
        :return:
        """
        if not self.running:
            return None
        if self.step >= len(self.stock_info.stock_values):
            self.step = 0
        self.current_value = self.stock_info.stock_values[self.step]
        if self.position_list[self.step][0] == -(self.display_width / 2):
            self.ticker_line.clear()
            self.ticker_line.teleport(self.position_list[self.step][0], self.position_list[self.step][1])
            self.day += 1
        else:
            self.ticker_line.goto(self.position_list[self.step])
        self.step += 1
        self.update_display()
        if self.day == 30:
            self.end_game("That's all folks! \n" + "There's no more stocks here!")
            self.running = False
            self.ticker_line.penup()

    def end_game(self, message):
        self.display.delete("all")
        labelvar = tk.StringVar(value=message)
        label = tk.Label(self.display, textvariable=labelvar, font=("Ariel", 14), bg="White")
        label.pack()


def main():
    root = tk.Tk()
    stock = StockDisplay(root, "META")
    stock.display.pack()
    stock.day = 25
    while stock.day < 31:
        stock.movement()
        print(stock.running)

    root.mainloop()


if __name__ == "__main__":
    main()
