class options:
    FIND_GAME=1
    CHALLENGE_FRIEND=2
    PLAY_BOT=3
    MAX_VAL=3


class Menu:
    MENU_PROMPT = "Hi, Welcome to P2PChess!\nOptions:\n\t1: Find game\n\t2: Play friend\n\t3: Play bot\n"
    
    def __init__(self):
        self.choice = None

    def display_menu(self):
        self.choice=input(self.MENU_PROMPT)
        try:
            choice = int(input("Enter your choice: "))
            if choice < 1 or choice > 3:
                print("Invalid choice. Please select a valid option.")
            else:
                self.choice = choice
        except ValueError:
            print("Invalid input. Please enter a number.")
        

    def get_choice(self):
        while self.choice is None:
            try:
                choice = int(input("Enter your choice: "))
                if choice < 1 or choice > 3:
                    print("Invalid choice. Please select a valid option.")
                else:
                    self.choice = choice
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def execute_choice(self):
        if self.choice == 1:
            print("Finding a game...")
        elif self.choice == 2:
            print("Playing with a friend...")
        elif self.choice == 3:
            print("Playing against a bot...")

