# Name: 1-socket.py
# Author: emily h. (nemo) 
# Date: 20.06.24
# Description: A program that connects via socket to a remote connection, receives CMD commands and returns output, and on the other side connects with netcat.

# ייבוא מודלים
import socket 
import sys 
import subprocess

# הגדרת חיבור סוקט ווידוא הצלחתו
try: 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    print ("Socket successfully created")
except socket.error as err: 
    print ("socket creation failed with error %s" %(err))

# הגדרת פורט עליו תיוווצר ההתחברות
port = 80

# הגדרת כתובת המקור
host_ip = "127.0.0.1"  

# הגדרת העמדה כמקשיב למחשב השני שרוצה להתחבר אליו
s.bind((host_ip, port))
s.listen(5)

# הקמת התקשורת בין העמדות
c, addr = s.accept()     
print ('Got connection from', addr)

# יצירת פונקציה והגדרת לולאה שתמשיך לרוץ כל עוד אין שגיאה
def main():
    while True: 
        # קבלת פקודה, הרצתה והחזרת הפלט לעמדה שאליה התחברנו
        command = c.recv(1024).decode()
        output = subprocess.run([command], shell=True, capture_output=True, text=True)
        output = output.stdout.encode()
        c.send(output)
        
if __name__ == "__main__":
    main()



# במחשב השני ממנו נתחבר נכתוב את השורה הבאה
# ncat 127.0.0.1 80
