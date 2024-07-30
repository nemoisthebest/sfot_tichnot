# Name: 6-webcrawler.py
# Author: emily h. (nemo) 
# Date: 19.06.24
# Description: webcralwer that receives a file with common file names on websites and tries to access them all.

# ייבוא מודל
import requests

#הגדרת משתנים
def main():
    website = input ("Enter the website you want to do a web crawler on: ")
    urls_file_path = input ("Enter the file path: ")
    urls_file = open(urls_file_path, "r")
    current_url = urls_file.readline()[:-1]

#הגדרת לולאה שבה הפונקציה תרוץ עד שיגמרו המחרוזות בקובץ
    while len(current_url) != 0:
 
 # מעבר על שורות הקובץ לאחר שהבקשה הפכה לדף דפדפן והדפסת הכתובות שנמצאות באתר  
        response = requests.get(website + current_url)
        if response.status_code in range(200, 299):
            print(response.url)
        current_url = urls_file.readline()[:-1]

# סגירת קריאת הקובץ
    urls_file.close()

# קריאה לפונקציה
if __name__ == "__main__":
    main()
