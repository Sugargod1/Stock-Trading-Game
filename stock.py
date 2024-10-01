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
#
# licensed under a Creative Commons
# Attribution-Noncommercial-Share Alike 3.0 United States License.
####################################################################################
from turtle import RawTurtle
import tkinter as tk
import copy
import time
import yfinance as yahooFinance
import pandas as pd
import turtle


class Stock:
    def __init__(self, root, stock_option):
        self.stock_option = stock_option
        self.root = root
        self.stock_values = None
        self.running = True
        self.step = 0
        self.day = 0
        self.labelvar = tk.StringVar(value="Starting Up...")
        self.current_value = None

        # initialize display variables
        self.display_width = 600
        self.display_height = 480
        self.display = tk.Canvas(self.root, height=self.display_height, width=self.display_width, bg="blue")
        self.display.pack()

        # initialized turtle variables
        self.ticker_line = RawTurtle(self.display)
        self.position = (self.ticker_line.xcor(), self.ticker_line.ycor())
        self.speed = self.ticker_line.speed(0)
        self.ticker_line.hideturtle()
        self.ticker_line.teleport(-self.display_width / 2, 0)
        self.stock_ticker = yahooFinance.Ticker(stock_option)
        self.ticker_line.color("white")
        self.display.config(bg="dark blue")

    def get_stock_value(self):
        """
        Grabs a list of the stock valuations of the stock_option for the object
        :return:
        """
        day_info = self.stock_ticker.history(period="1mo", interval="5m")
        stock_high = day_info['High']
        self.stock_values = stock_high.to_list()

    def stock_values_to_positional(self):
        lowest = min(self.stock_values)
        highest = max(self.stock_values)

        x_list = make_x_coordinate_list(len(self.stock_values), self.display_width)

        new_values = []

        for x, stock_value in zip(x_list, self.stock_values):
            y = alpha(lowest, highest, stock_value) * self.display_height - self.display_height / 2
            new_values.append((x, y))

        return new_values

    def update_display(self):
        self.labelvar.set("Current Value: " + str(round(self.current_value, 3)) + "   " + "Day: " + str(
            self.day) + "  " + self.stock_option)

    def setup_display(self):
        # Creating and displaying a LabelFrame
        label = tk.Label(self.display, textvariable=self.labelvar, font=("Arial", 14), bg="dark blue")
        label.pack()

        # Displaying and resizing of LabelFrame inside Canvas
        self.display.create_window(-250, -self.display_height / 2 + 40, window=label, anchor='w')

    def movement(self):
        self.current_value = self.stock_values[self.step]
        position_list = self.stock_values_to_positional()
        if position_list[self.step][0] == -(self.display_width / 2):
            self.ticker_line.clear()
            self.ticker_line.teleport(position_list[self.step][0], position_list[self.step][1])
            self.day += 1
        else:
            self.ticker_line.goto(position_list[self.step])
        self.step += 1
        if self.step == 2333:
            self.running = False

    def configure_default(self):
        self.get_stock_value()
        self.stock_values_to_positional()
        self.setup_display()


def make_x_coordinate_list(list_size, win_size):
    each_day = list_size / 30
    each_length = win_size / each_day
    x_list = []
    for i in range((win_size // int(each_length)) + 1):
        x_list.append(-win_size / 2 + (i * int(each_length)))
    return x_list * 30


def get_average_int_value(number_list):
    total = 0
    for i in number_list:
        total = total + i
    return int(total / len(number_list))


def alpha(min_value, max_value, num):
    return (num - min_value) / (max_value - min_value)


def main():
    root = tk.Tk()

    mystock = Stock(root, "INTC")
    mystock.configure_default()
    print(mystock.stock_values_to_positional())
    while mystock.running:
        mystock.movement()
        mystock.update_display()
    root.mainloop()


if __name__ == "__main__":
    main()
