# Name: 5-os_listdir.py
# Author: emily h. (nemo) 
# Date: 16.06.24
# Description: A recursive function that receives a path to a folder and returns a list with all the files in it..

# os ייבוא מודל
import os
 
 # הגדרת משתנה לתיקייה הנוכחית שאני נמצאת בה
current_directory = os.getcwd()

# הגדרת פונקציה שבודקת בנתיב שהיא קיבלה האם זהו קובץ או תיקייה ואם זו תיקיה הוא מוציא את הקבצים ממנה
def rec(target_directory):

    for item in os.listdir(target_directory):
        item_path = os.path.join(target_directory, item)
        if os.path.isfile(item_path):
            print(f"File: {item_path}")
        elif os.path.isdir(item_path):
            rec(item_path)

# קריאה לפונקציה 
rec(current_directory)
