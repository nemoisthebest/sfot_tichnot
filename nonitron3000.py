#Impotrs
from os import listdir
from os.path import exists, join
from json import loads, dumps
from translate import Translator
from bidi.algorithm import get_display


# Constants
WELCOME_MASSAGE = "Welcome to noni's brain!!"
MENU_MASSAGE_SIMPLE_USER = """
MENU:

1. Find a memory by name.
2. List all memories in noni's brain.
3. Borrow memories.
4. Return a memory.
5. Check account status.
6. Translate sentences from Russian to Hebrew.
"""
MENU_MASSAGE_ADMIN_USER = """
MENU:

1. Find a memory by name.
2. List all the memories in noni's brain.
3. Borrow memories.
4. Return a memory.
5. Check account status.
6. Translate sentences from Russian to Hebrew.

                                                                                                    
                         @@@@@@@@@@@@@@@@@                                                          
                     @@@@@@@@@@@@@@@@@@@@@@@@@                                                      
                  @@@@@@@@@@@%#######%%@@@@@@@@@@                                                   
               @@@@@@@@@%##**************#%@@@@@@@@                                                 
             @@@@@@@@@@%#*******************#%@@@@@@@                                               
            @@@@@@@@@%*************************#@@@@@@@                                             
            @@@@@@@%*****************************%@@@@@@                                            
           @@@@@@@#********************************%@@@@@@                                          
          @@@@@@@#**********************************#@@@@@@@                                        
          @@@@@@%#*******************##%@@@@@%%##*****#@@@@@@@                                      
          @@@@@@@#*****************#%@@@@@@@@@@@@@@%##**#@@@@@@@                                    
         @@@@@@@@#****************#%@@@@@@@@@.=#@@@@@@@@%##@@@@@@@                                  
         @@@@@@@%#**************#@@@@@@@@@@@@#..+#+=*%@@@@@@@@@@@@@@@                               
         @@@@@@@@#*************#@@%%%@@@@@@@@@@@*+*#@@@@@@@@@@@@@@@@@@@@                            
          @@@@@@@#*********************#%%@@@@@@@@@@@@@@@@##*=*@@@@@@@@@@                           
          @@@@@@@%**************************#%%@@@@@@@@@**+=-::-%@@@@@                              
           @@@@@@@#*************************#%@@@@@@@%**=-::::::-=%@@@@@@                           
            @@@@@@@##%#*******************#%@@@@@*+-::::::::::::::-=#@@@@@@@@                       
             @@@@@@@%%@#****************#%@@@@@#+==----::::::::::::::-=*@@@@@@@@@@@@        @@@@@@@ 
              @@@@@@@@@@#**************#@@@@@@@@@@@@@@@@@%%##+=--::::::::-=+%@@@@@@@@@@@@@@@@@@@@@  
               @@@@@@@@@@@#***********%@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%#=---::::-===+*%@@@@@@@@@@@@   
                 @@@@@@@@@@%****************###%@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%%%%@@@@@@@@@@@     
                  @@@@@@@@@@@#*******************##@@@@@@@@     @@@@@@@@@@@@@@@@@@@@@@@@@@@@        
                    @@@@@@@@@@%**********************@@@@@@@                                        
                      @@@@@@@@@@#***************#******@@@@@@@                                      
                           @@@@@@%*************#@@@@@#**#@@@@@@                                     
                            @@@@@@@#***********#%@@@@@@#*#@@@@@                                     
                              @@@@@@#**********#%@@@@@@@@#%@@@@@                                    
                              @@@@@@@#*********#@@@@@@@@@@%%@@@@@                                   
                               @@@@@@@*********#@@@@@@@@@@@@@@@@@@                                  
                                @@@@@@%********@@@@@@@@@@@@@@@@@@@                                  
                                @@@@@@@*******%@@@@@@@@@@@@@@@@@@@                                  
                                 @@@@@@#*****%@@@@@@@@@@@@@@@%%@@@@                                 
                                 @@@@@@%****%@@@@@@@@@@@@@@@#::@@@@                                 
                                 @@@@@@%**%@@@@@@@@@@@@@@@%=. .@@@@                                 
                                @@@@@@@%%@@@@@@@@@@@@@@@%-..   %@@@                                 
                                @@@@@@@@@@@@@@@@@@@@@@=:.      %@@@                                 
                                @@@@@@@@@@@@@@@@@@*-...        %@@@                                 
                               @@@@@@@@@@@@@%+-:..            .@@@@                                 
                               @@@@@@*=-:...                 :%@@@@                                 
                              @@@@@@%                      .+@@@@@                                  
                             @@@@@@@.                    .=@@@@@@                                   
                             @@@@@@=                  ..#@@@@@@                                     
                            @@@@@@+.              ..:#@@@@@@@@                                      
                           @@@@@@+.           .:-*@@@@@@@@@                                         
                         @@@@@@%-.    ...::=*%@@@@@@@@@@                                            
                        @@@@@@@@@%%%%@@@@@@@@@@@@@@@@                                               
                      @@@@@@@@@@@@@@@@@@@@@@@@@@@                                                   
                      @@@@@@@@@@@@@@@@@@@@                                                          

admin action's:
7. Block simple user.
8. Report a loss of memory.
9. Add a new memories.
10. Add a new user to the database.
"""

MEMORY_ROOTDIR_PATH = 'C:\\Users\\Administrator\\Documents\\emily\\python\\nonitron\\memories'
DATABASE_USERS_PATH = 'C:\\Users\\Administrator\\Documents\\emily\\python\\nonitron\\database\\users.json'
MAX_AUTHENTICATION_LOOP_ATTEMPTS = 4
YES = "yes"
TXT_EXTENSION = ".txt"
AUTHENTICATION_SUCCESSFUL = 1
A = "A"
B = "B"

# Classes
class User:
    def __init__(self, username, password, bad_points_amount, full_name, user_type, memories_num):
        self.username = username
        self.password = password
        self.full_name = full_name
        self.usertype = user_type
        self.bad_points = bad_points_amount
        self.memories_num = memories_num

    # Copies the entered values ​​from the file to the class according to the categories
    @classmethod
    def fromJsonObject(cls, jsonData):
        return cls(jsonData["username"],
                   jsonData["password"],
                   jsonData["bad_points_amount"],
                   jsonData["full_name"],
                   jsonData["user_type"],
                   jsonData["current_memories_owned_amount"])

    # Arranges the entered values ​​in an orderly manner
    def __str__(self) -> str:
        return "User [{username}]\n\tFull Name: {fullname}\n\tBad Points: {badpoints}\n\tType: {type}\n\tAmount of Current Owned Memories: {memamount}".format(username=self.username,
                                                                                                                                                               fullname=self.full_name,
                                                                                                                                                               badpoints=self.bad_points,
                                                                                                                                                               type=self.usertype,
                                                                                                                                                               memamount=self.memories_num)


class UsersManager:
     currentUsers = []
     currentLoggedOnUser = None

     def __init__(self):
        #open file that inclouds info about users, in read mood.
        users_file = open(DATABASE_USERS_PATH, "r")
        #try to read the lines in the file and parse the info, in this line we convert from python to json.
        try:
            users_file_json_data = loads(users_file.read())
            # create a user and add it to the current user list.
            for userData in users_file_json_data:
                self.currentUsers.append(User.fromJsonObject(userData))
        #if the function cant go throw the lines it sends a massage to the user and exit.
        except:
            print("[-] Couldn't read users information:((((((")
            exit()
            # close the file
        users_file.close()
    
     def authenticate(self):
        # Setting a range of attempts in which the function will continue to run
        for logon_attempts_made in range(MAX_AUTHENTICATION_LOOP_ATTEMPTS):
            #inputs from the user
            username = input("Enter your username:")
            password = input("Enter your password:")
            # loop that check's if the authentication that been recive from the user Corresponds to what is saved in the database.
            for currentuser in self.currentUsers:
                if (currentuser.username == username and currentuser.password == password):
                    print ("Logon successfully to noonie's brain!")
                    # add to the current user list the name of the currrent user.
                    self.currentLoggedOnUser = currentuser
                    return AUTHENTICATION_SUCCESSFUL, currentuser.usertype
                # if the logon havent finished successfully, the user will recive a massage and another try to logon(if he hasn't reached to the max attamps.)
            print(f"Loser you have {MAX_AUTHENTICATION_LOOP_ATTEMPTS - logon_attempts_made - 1} more tries to login.")
        # If all attempts failed.
        exit()


class memory:
    def __init__(self, memory, memory_id, memory_path):
        self.memory = memory
        self.memoryid = memory_id
        self.memory_path = memory_path


# Function
def locating_memory():
    memory = input("enter the memory you want to locate:")
    #Adding a txt suffix to the name of the memory and checking whether the memory is in the path of the memories.
    if TXT_EXTENSION not in memory:
        memory = memory + TXT_EXTENSION
    this_memory_path = join(MEMORY_ROOTDIR_PATH, memory)

    if exists(this_memory_path):
        print(f"the memory {memory} exists!!")
    else:
        print(f"the memory {memory} doesnt exist..")
    # Receiving input regarding additional memory search, if the answer is positive repeat the function from before.
    while True:
        user_wants_another_memory = input(
            "do you want to locate another memory?:")
        if user_wants_another_memory == YES:
            locating_memory()
        else:
            break


def list_memories():
    # Print output of all the memories that are in the memory path in Noni's brain
    print(f"""here is the list of all the memories in noni's brain:
{listdir(MEMORY_ROOTDIR_PATH)}\n""")

def translator_from_Russian_to_Hebrew():
    # Receiving input in Russian and translating it into Hebrew
    translator= Translator(from_lang="russian",to_lang="hebrew")
    translation = translator.translate(input("please enter sentence in Russian:"))
    #Printing the translation correctly from right to left
    print (get_display(translation))

def translator_from_Hebrew_to_Russian():
    # Receiving input in Hebrew and translating it into Russian
    translator= Translator(from_lang="hebrew",to_lang="russian")
    translation = translator.translate(input("please enter sentence in Hebrew:"))
    #Printing the translation
    print (translation)

def add_user_to_database():
    

def main():

    UserManager = UsersManager()
    print(WELCOME_MASSAGE)
    UserManager.authenticate()

    print(MENU_MASSAGE_ADMIN_USER)
    print(MENU_MASSAGE_SIMPLE_USER)
    user_menu_input_choice = int(input("Enter the index of the action you want to preform: "))

    match user_menu_input_choice:
        case 1:
            locating_memory()
        case 2:
            list_memories()
        case 3:
            return 0
        case 4:
            return 0
        case 5:
            return 0
        case 6:
            translate_lang = input("""would you like to translate from:
                  A. Russian to Hebrew
                  B. Hebrew to Russian """)
            if translate_lang == A:
                translator_from_Russian_to_Hebrew()
            if translate_lang == B:
                translator_from_Hebrew_to_Russian()
        case 7:
            return 0
        case 8:
            return 0
        case 9:
            return 0
        case 10:
            return 0
        case _:
            print("Error")


if __name__ == "__main__":
    main()
