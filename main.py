from kahoot import client
from time import sleep
from random import randint
from threading import Thread
from requests import get
from datetime import datetime
from urllib.request import getproxies


def create_bot(game_id: int, name: str, leave_after_time: int, current_bot: int, use_random_numbers: bool):
    bot = client()
    username = name
    if use_random_numbers:
        username += str(randint(0, 99999))
    else:
        username += str(current_bot)
    bot.join(game_id, username)
    if leave_after_time:
        sleep(leave_after_time)
        try:
            bot.leave()
        except Exception:
            pass

def prepare_bots():
    translate_characters = {'a': '𝘢', 'b': '𝘣', 'c': '𝘤', 'd': '𝘥', 'e': '𝘦', 'f': '𝘧', 'g': '𝘨', 'h': '𝘩', 'i': '𝘪', 'j': '𝘫', 'k': '𝘬', 'l': '𝘭', 'm': '𝘮', 'n': '𝘯', 'o': '𝘰', 'p': '𝘱', 'q': '𝘲', 'r': '𝘳', 's': '𝘴', 't': '𝘵', 'u': '𝘶', 'v': '𝘷', 'w': '𝘸', 'x': '𝘹', 'y':'𝘺', 'z': '𝘻'}
    bypassed_cuss_words = {'fuck': 'ᠻꪊᥴᛕ', 'ass': 'ꪖᦓᦓ', 'cunt': 'ᥴꪊꪀꪻ', 'bitch': '᥇꠸ꪻᥴꫝ', 'dick': 'ᦔ꠸ᥴᛕ', 'pussy': 'ρꪊᦓᦓꪗ', 'shit': 'ᦓꫝ꠸ꪻ', 'retard': '᥅ꫀꪻꪖ᥅ᦔ', 'fucking': 'ᠻꪊᥴᛕ꠸ꪀᧁ', 'retarded': '᥅ꫀꪻꪖ᥅ᦔꫀᦔ', 'fucked': 'ᠻꪊᥴᛕꫀᦔ'}
    times_to_sleep = {1: 0.5, 500: 0.75, 1000: 1}
    time_to_sleep = 0

    enabled = ['yes', 'y', 'yeah', 'yup', 'true', 'enabled', 'enable']

    name = input('Enter usename >> ')

    try:
        game_id = int(input('Enter the game id >> '))

    except ValueError:
        print('Invalid game id.')
        return

    try:
        amount = int(input('Enter the amount of bots >> '))

    except ValueError:
        amount = randint(25, 500)
        print(f"Unknown number; defaulting to {amount}.")

    try:
        time_to_leave = int(input('Time to leave >> '))

    except ValueError:
        time_to_leave = False
    
    bypass_cuss_words = input('Enable cuss words bypassing >> ')
    if bypass_cuss_words in enabled:
        bypass_cuss_words = True
        for word in name.split():
            if word in bypassed_cuss_words:
                name = name.replace(word, bypassed_cuss_words[word])
    else:
        bypass_cuss_words = False
    
    different_font = input('Enable different font >> ')

    if different_font.lower() in enabled:
        new_name = ""

        for old_character in list(name.lower()):
            if old_character in translate_characters and old_character not in bypassed_cuss_words:
                new_name += translate_characters[old_character]
            
            else:
                new_name += old_character

        name = new_name
    
    long_name = input("Enable long name >> ")
    if long_name.lower() in enabled:
        name *= 50

    default_kahoot_names = input('Enable kahoot names >> ')

    if default_kahoot_names.lower() in enabled:
        name = "Fuck this is a random name"

    anti_bot_bypassing = input('Enable anti bot bypassing >> ')
    if anti_bot_bypassing in enabled:
        for key, value in times_to_sleep.items():
            if amount >= key:
                time_to_sleep = value
                
        anti_bot_bypassing = True
    else:
        amount *= 2
        anti_bot_bypassing = False

    use_random_numbers = input('Enable random numbers >> ')
    if use_random_numbers in enabled:
        use_random_numbers = True
    else:
        use_random_numbers = False
            
    for i in range(amount):
        new_bot = Thread(target=create_bot, args=(game_id, name, time_to_leave, i, use_random_numbers))

        try:
            new_bot.start()

        except Exception:
            pass
        
        if i % 10 == 0:
            sleep(time_to_sleep)

    print(f'{amount} bots with the name of \"{name}\" joined the game with the pin of {game_id}.')

class Pins:
    def __init__(self):
        self.valid_pins = self.get()
        self.save()
    
    def save(self):
        with open('pins.txt', 'w') as my_file:
            for pin in self.valid_pins:
                my_file.write(pin)
    
    def get(self):
        with open('pins.txt', 'r') as my_file:
            return my_file.readlines()
    
    def add(self, pin: int):
        self.valid_pins.append(f"{datetime.now().strftime('%I:%M')}, Pin found: {pin}\n")
        self.save()


def check_valid_pin(url):
    if url.status_code == 200:
        return True
    return False

def bruteforce_counted_pins(use_proxies: bool, starting_number: int):
    for pin in range(starting_number, 9999999):
        if use_proxies:
            url = get(f"https://kahoot.it/reserve/session/{pin}", proxies=getproxies())
        else:
            url = get(f"https://kahoot.it/reserve/session/{pin}")

        if check_valid_pin(url):
            Pins().add(pin)

def bruteforce_random_pins(use_proxies: bool):
    while True:
        pin = randint(100000, 9999999)
        if use_proxies:
            url = get(f"https://kahoot.it/reserve/session/{pin}", proxies=getproxies())
        else:
            url = get(f"https://kahoot.it/reserve/session/{pin}")

        if check_valid_pin(url):
            Pins().add(pin)
            

def prepare_bruteforce_pins():
    enabled = ['yes', 'y', 'yeah', 'yup', 'true', 'enabled', 'enable']
    try:
        amount = int(input("Thread amount >> "))
    except ValueError:
        amount = 50
        print("Invalid number; defaulting to 50")

    use_proxies = input("Enable proxies >> ")
    if use_proxies in enabled:
        use_proxies = True
    else:
        use_proxies = False

    for i in range(8):
        counted_pins = Thread(target=bruteforce_counted_pins, args=(use_proxies, 100000*i))
        try:
            counted_pins.start()
        except Exception:
            pass

    for i in range(amount):
        random_pins = Thread(target=bruteforce_random_pins, args=(use_proxies, ))
        try:
            random_pins.start()
        except Exception:
            pass

def help():

    print("""       HELP
    pins:
        returns valid kahoot game pins
        -options:
            Thread amount: amount of threads to find pins
            Enable proxies: to enable proxies for less ratelimiting, may take a little longer
    bots:
        floods a game with bots
        -options:
            username: the name for the bots
            game id: the kahoot game id to flood
            amount of bots: the amount of bots to flood
            time to leave: time in seconds before the bots leave, leave blank for no leaving
            cuss words bypassing: bypasses kahoots cussword filter
            different front: to use a different front, leave blank for the regular font
            long name: makes the name extremely long
            kahoot names: uses kahoots random names, overrides the username option, leave blank for the inputted username
            anti bot bypassing: bypasses kahoots anti bot feature
            random numbers: uses random numbers at the end of the names
""")

def main():
    options = {'pins': prepare_bruteforce_pins, 'bots': prepare_bots, 'help': help, 'quit': quit}
    selected_option = input('Enter the option[pins, bots, help, quit] >> ')

    if selected_option not in options:
        return print('Not a valid option!')
    
    return options[selected_option]()



if __name__ == "__main__":
    while True: 
        main()
