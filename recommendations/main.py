"""
Creates a screenshot of Yahoo Finance's Recommendation Trends of each
S&P 500 company and saves it as file with the company's name.
"""

import keyboard
import pyautogui
import time
import webbrowser
import os
from datetime import date


def get_symbols(file_name="s&p500.txt"):
    symbols_file = open(file_name, "r")
    lines = symbols_file.readlines()
    symbols_file.close()

    symbols = []
    for line in lines:
        no_newline = line.rstrip('\n')
        symbols.append(no_newline)

    return symbols


def take_screenshot(symbol):
    chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/" \
                  "chrome.exe %s"
    url = "https://finance.yahoo.com/quote/" + symbol

    webbrowser.get(chrome_path).open(url)
    time.sleep(2)

    keyboard.press_and_release("page down")
    time.sleep(1.5)
    keyboard.press_and_release("page up")
    time.sleep(0.5)
    keyboard.press_and_release("space")
    time.sleep(0.5)
    keyboard.press_and_release("space")

    today = date.today().strftime("%d-%m-%Y")
    folder = "screenshots/" + today
    if not os.path.exists(folder):
        os.mkdir(folder)

    time.sleep(0.5)

    pyautogui.screenshot().save(folder + "/" + symbol + ".png")

    time.sleep(1)
    keyboard.press_and_release("ctrl+w")


def main():
    symbols = get_symbols("vbr.txt")
    # for i in range(len(symbols)):
    for i in range(800, 810):
        symbol = symbols[i]
        take_screenshot(symbol)


main()
