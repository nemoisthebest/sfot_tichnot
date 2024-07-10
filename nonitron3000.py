#Impotrs
from os import listdir
from os.path import exists, join
from json import loads, dumps, load, dump
from translate import Translator
from bidi.algorithm import get_display




#Constants
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
NO = "no"
TXT_EXTENSION = ".txt"
AUTHENTICATION_SUCCESSFUL = 1
A = "A"
B = "B"

#Classes
class User:
    def __init__(self, username, password, bad_points_amount, full_name, user_type, memories_num):
        self.username = username
        self.password = password
        self.full_name = full_name
        self.usertype = user_type
        self.bad_points = bad_points_amount
        self.memories_num = memories_num

    #Copies the entered values ​​from the file to the class according to the categories.
    @classmethod
    def fromJsonObject(cls, jsonData):
        return cls(jsonData["username"],
                   jsonData["password"],
                   jsonData["bad_points_amount"],
                   jsonData["full_name"],
                   jsonData["user_type"],
                   jsonData["current_memories_owned_amount"])

    #Arranges the entered values ​​in an orderly manner.
    def __str__(self) -> str:
        return "User [{username}]\n\tFull Name: {fullname}\n\tBad Points: {badpoints}\n\tType: {type}\n\tAmount of Current Owned Memories: {memamount}".format(username=self.username,
                                                                                                                                                               fullname=self.full_name,
                                                                                                                                                               badpoints=self.bad_points,
                                                                                                                                                               type=self.usertype,
                                                                                                                                                               memamount=self.memories_num)


class UsersManager:
     currentUsers: list[User] = []
     currentLoggedOnUser = None

     def __init__(self):
        #Open file that inclouds info about users,  in read mood.
        users_file = open(DATABASE_USERS_PATH, "r")
        #Try to read the lines in the file and parse the info, in this line we convert from json to python.
        try:
            users_file_json_data = load(users_file)
            #Create a user and add it to the current user list.
            for userData in users_file_json_data:
                self.currentUsers.append(User.fromJsonObject(userData))
        #If the function cant go throw the lines it sends a massage to the user and exit.
        except:
            print("[-] Couldn't read users information :((((((")
            exit()
            #Close the file.
        users_file.close()
    
     def authenticate(self):
        # Setting a range of attempts in which the function will continue to run.
        for logon_attempts_made in range(MAX_AUTHENTICATION_LOOP_ATTEMPTS):
            #Inputs from the user
            username = input("Enter your username:")
            password = input("Enter your password:")
            #Loop that check's if the authentication that been recive from the user Corresponds to what is saved in the database.
            for currentuser in self.currentUsers:
                if (currentuser.username == username and currentuser.password == password):
                    print ("Logon successfully to noonie's brain!")
                    #Add to the current user list the name of the currrent user.
                    self.currentLoggedOnUser = currentuser
                    return AUTHENTICATION_SUCCESSFUL
                #If the logon havent finished successfully, the user will recive a massage and another try to logon(if he hasn't reached to the max attamps).
            print(f"Loser you have {MAX_AUTHENTICATION_LOOP_ATTEMPTS - logon_attempts_made - 1} more tries to login.")
        #If all attempts failed.
        exit()


class memory:
    def __init__(self, memory_name, memory_serial_number, memory_date_written):
        self.memory_name = memory_name
        self.memory_id = memory_serial_number
        self.memory_date_written = memory_date_written


# Function
def locating_memory():
    memory = input("Enter the memory you want to locate:")
    #Adding a txt suffix to the name of the memory and checking whether the memory is in the path of the memories.
    if TXT_EXTENSION not in memory:
        memory = memory + TXT_EXTENSION
    this_memory_path = join(MEMORY_ROOTDIR_PATH, memory)

    if exists(this_memory_path):
        print(f"The memory {memory} exists!!")
    else:
        print(f"The memory {memory} doesnt exist..")
    #Receiving input regarding additional memory search, if the answer is positive repeat the function from before.
    while True:
        user_wants_another_memory = input(
            "Would you like to locate another memory?:")
        if user_wants_another_memory == YES:
            locating_memory()
        else:
            break


def list_memories():
    #Print output of all the memories that are in the memory path in Noni's brain.
    print(f"""Here is the list of all the memories in noni's brain:
{listdir(MEMORY_ROOTDIR_PATH)}\n""")

def translator_from_Russian_to_Hebrew():
    #Receiving input in Russian and translating it into Hebrew.
    translator= Translator(from_lang="russian",to_lang="hebrew")
    translation = translator.translate(input("Enter sentence in Russian:"))
    #Printing the translation correctly from right to left.
    print (get_display(translation))

def translator_from_Hebrew_to_Russian():
    #Receiving input in Hebrew and translating it into Russian.
    translator= Translator(from_lang="hebrew",to_lang="russian")
    translation = translator.translate(input("Enter sentence in Hebrew:"))
    #Printing the translation
    print (translation)


def add_user_to_database(new_user: User):
    #Open file with read Permissions.
    json_data_base_file = open(DATABASE_USERS_PATH, "r+")
    #Convert file content from json to python dict.
    parsed_json_data : list[User] = load(json_data_base_file)
    #Close file.
    json_data_base_file.close()
    #Add the new user data into the file content without run over the original text.
    parsed_json_data.append(new_user)
    #Ofen file with write Permissions.
    json_data_base_file = open(DATABASE_USERS_PATH, "w")
    #Convert the file content with the new user back to json file
    dump(parsed_json_data, json_data_base_file)
    #Close file.
    json_data_base_file.close()

def block_simple_users(username_to_block: User):
    #Open file with read Permissions.
    json_data_base_file = open(DATABASE_USERS_PATH, "r+")
    #Convert file content from json to python dict.
    parsed_json_data : list[User] = load(json_data_base_file)
    #Close file.
    json_data_base_file.close()
    #Add the new user data into the file content without run over the original text.
    wanted_user_to_block = None
    for user_object in parsed_json_data:
        if user_object["username"] == username_to_block:
            wanted_user_to_block = user_object
            break
    parsed_json_data.remove(wanted_user_to_block)
    #Ofen file with write Permissions.
    json_data_base_file = open(DATABASE_USERS_PATH, "w")
    #Convert the file content with the new user back to json file
    dump(parsed_json_data, json_data_base_file)
    #Close file.
    json_data_base_file.close()

def add_new_memory():
    return 0

def borrow_memory():
    memory_to_borrow = input("Enter the full name(wirh .txt suffix) of the memory you would like to borrow: ")
    return 0

def return_memory():
    memory_to_return = input("Enter the full name(wirh .txt suffix) of the memory you would like to return: ")
    return 0

def check_account_status():
    return 0

def main():

    UserManager = UsersManager()
    print(WELCOME_MASSAGE)
    UserManager.authenticate()

    if UserManager.currentLoggedOnUser.usertype == "admin":
        print(MENU_MASSAGE_ADMIN_USER)
    else:
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
            translate_lang = input("""Would you like to translate from:
                A. Russian to Hebrew
                B. Hebrew to Russian """)
            if translate_lang == A:
                translator_from_Russian_to_Hebrew()
            if translate_lang == B:
                translator_from_Hebrew_to_Russian()
        case 7:
            block_username= input("Enter the username you would like to block: ")
            block_simple_users(block_username)
            print(f"User {block_username} has been successfully blocked.")
        case 8:
            return 0
        case 9:
            return 0
        case 10:
            username_input = input("Enter username:" )
            password_input = input("Enter password:" )
            full_name_input = input("Enter full_name:" )
            user_type_input = input("Enter user_type:" )
            new_user_object = {
                "username": username_input,
                "password": password_input,
                "bad_points_amount": 0,
                "current_memories_owned_amount": 0,
                "full_name": full_name_input,
                "user_type": user_type_input
            }

            add_user_to_database(new_user_object)
        case _:
            print("Error")

if __name__ == "__main__":
    main()
