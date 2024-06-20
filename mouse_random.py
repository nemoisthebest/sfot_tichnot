# Name: mouse_random.py
# Author: emily h. (nemo) 
# Date: 17.06.24
# Description: A Python program generates random locations on the screen and moves the mouse to the location every 10 seconds.


# ייבוא מודלים הנחוצים לתוכנית
import win32api
import time
import random

# הגדרת זמן ריצה
runtime = 60

# הגדרת פונקציה 
def main():
   
# הגדרת זמן לריצת התוכנית וזמן לעצירתה
   start_time = time.time()

   while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time > runtime:
            break

# הלולאה שבה העכבר זז כל עשר שניות למקום רנדומלי שהתוכנית גינרטה ומדפיסה את המיקום של העכבר במסך
        for i in range(0,1):
            screen_width = win32api.GetSystemMetrics(0)
            screen_height = win32api.GetSystemMetrics(1)

            x = random.randint(0,screen_width)
            y = random.randint(0,screen_height)

            win32api.SetCursorPos((x,y))

            print(f"mouse moved to: ({x},{y})")

            time.sleep(10)

# קריאה לפונקציה
if __name__ == "__main__":
    main()

