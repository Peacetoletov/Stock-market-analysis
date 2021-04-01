import keyboard
import pyautogui
import time

time.sleep(3)
print("test")


"""
# keyboard.press_and_release('shift+s, space, shift+a')
keyboard.press_and_release("page down")
time.sleep(1)
keyboard.press_and_release("page down")
time.sleep(1)
keyboard.press_and_release("page up")
"""

myScreenshot = pyautogui.screenshot()
myScreenshot.save(r'C:\Users\lukas\PycharmProjects\yfinance_test'
                  r'\recommendations'
                  r'\screen.png')
