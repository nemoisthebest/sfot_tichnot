import pyautogui
import time
import random

# קביעת מיקום המסך
screen_width, screen_height = pyautogui.size()

while True:
    # יצירת מיקום רנדומלי
    random_x = random.randint(0, screen_width)
    random_y = random.randint(0, screen_height)

    # הזזת העכבר למיקום הרנדומלי
    pyautogui.moveTo(random_x, random_y, duration=0.25)

    # המתנה 10 שניות
    time.sleep(10)
