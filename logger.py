import colorama
import datetime

from colorama import Fore, Back
colorama.init(autoreset=True)

def logOutput(user):
     try:
          date = datetime.datetime.now().strftime("%d.%m.%y %H:%M")
          user_name = user.first_name
          user_username = "None"
          try:
               if user.last_name:
                    user_name = f"{user.first_name} {user.last_name}"
               user_username = user.username
          except:
               pass
          print(f"{Fore.CYAN}[{date}]{Fore.YELLOW} VOICE {Fore.WHITE}от {user_name} [{Fore.YELLOW}@{user_username}{Fore.WHITE}]")
     except Exception as gh:
        print(Fore.RED + "Ошибка логгирования. " + Back.WHITE + Fore.WHITE + str(gh))
     return

def logException(rf):
     print(Fore.RED + "Ошибка обработки сообщения. " + Back.WHITE + Fore.WHITE + str(rf))

def logBDSuccesfull(msg):
     date = datetime.datetime.now().strftime("%d.%m.%y %H:%M")
     print(f"{Fore.CYAN}[{date}]{Fore.GREEN} Database operation sucessfull: {Fore.WHITE}{msg}")

def logExecuteCommand(msg):
     date = datetime.datetime.now().strftime("%d.%m.%y %H:%M")
     print(f"{Fore.CYAN}[{date}]{Fore.GREEN} Command executed sucessfull: {Fore.WHITE}{msg}")