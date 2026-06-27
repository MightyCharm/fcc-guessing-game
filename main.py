import random

def reset_variables():
    game_won = False
    guess_count = 1
    user_score = 100
    secret_number = get_random_number(MIN_NUMBER, MAX_NUMBER)
    return game_won, guess_count, user_score, secret_number

def get_user_name():
    while True:
        name = input("Please enter your name\n=> ").strip()
        if len(name) > 15:
            print("Name was too long. Please stay under 15 characters.\n")
        elif len(name) <= 0:
            print("No input.\n")
        else:
            return name

def get_user_guess():
    while True:
        try:
            guess = int(input("Please guess the secret number\n=> "))
            break
        except KeyboardInterrupt:
            print("\nGame stopped by user.")
            exit()
        except ValueError:
            print("Invalid input!\n")
    return guess

def ask_to_play_again():
    while True:
        user_input = input("Play a new game ? (y/n)\n=> ").lower().strip()
        if user_input == "y" or user_input == "yes":
            return True
        elif user_input == "n" or user_input == "no":
            return False
        else:
            print("Invalid input!")

def get_random_number(min, max):
    return random.randint(min, max)

def save_score(user_name, user_score):
    with open("scores.txt", "a") as file:
        file.write(f'{user_name},{user_score}\n')

def load_scores():
    try:
        with open("scores.txt", "r") as file:
            scores = file.readlines()
    except (FileNotFoundError, PermissionError):
        scores = []   
    if len(scores) <= 0:
        return [] 
    
    cleanedScores = []
    for player in scores:
        line = player.strip("\n")
        parts = line.split(",")
        if len(parts) != 2: continue
        if len(parts[0].strip()) <= 0: continue
        try: 
            name = parts[0]
            score = int(parts[1])
            cleanedScores.append((name, score))
        except ValueError:
            pass

    sortedScores = sorted(cleanedScores, key=lambda x: x[1], reverse=True)
    highscores = sortedScores[:10]
    return highscores

def output_highscores(highscores):
    max_width = 0
    for line in highscores:
        length_name = len(line[0])
        if length_name > max_width:
            max_width = length_name    
    print("\n=== 🏆 HIGHSCORES 🏆 ===")
    print(f"{'Place':<5} {'Name':<{max_width}} {'Score':>5}")
    if not highscores:
        print("NO HIGHSCORES HERE. BE THE FIRST!")
        return
    for index, player in enumerate(highscores, 1):
        print(f"{index:<5} {player[0]:<{max_width}} {player[1]:>5}")
    print() 

def display_highscores():
    highscores = load_scores()
    output_highscores(highscores)

def update_game_stats(user_score, guess_count):
    user_score -= 10
    guess_count += 1
    return user_score, guess_count

def display_win(user_name, guess_count, secret_number, user_score):
    print(f"\n🏁 {user_name} you guessed the secret number {secret_number}. 🏁")
    print(f"🏁 {guess_count} guesses in total. Your final score is {user_score}. 🏁")

def display_game_over(name, secret_number):
    print(f"\n{name} there are no guesses left. You lose!")
    print(f"The secret number was {secret_number}.")

def display_farewell(name):
    print(f'Thanks for playing {name}. Have a nice day. Till soon. 🦍🦍🦍')

def get_feedback(user_guess, secret_number):
    if user_guess > secret_number:
        print("📉 Your guess was too high.")
    else:
        print("📈 Your guess was too low.")  

# range of random number
MIN_NUMBER = 1
MAX_NUMBER = 100
# random number
secret_number = get_random_number(MIN_NUMBER, MAX_NUMBER);
# game variables
game_won = False
guess_count = 1

display_highscores()

user_score = 100
user_name = get_user_name()

while True:
    while user_score > 0 and not game_won:
        print(f'\n🎲 Round {guess_count} starts.')
        #print("[Only for testing] Score", user_score, " Secret number", secret_number);
        user_guess = get_user_guess()
        if user_guess == secret_number:
            game_won = True
            break
        get_feedback(user_guess, secret_number)
      
        user_score, guess_count = update_game_stats(user_score, guess_count)  
               
    if game_won:
        save_score(user_name, user_score)
        display_win(user_name, guess_count, secret_number, user_score)
    else:
        display_game_over(user_name, secret_number)
    restart = ask_to_play_again()
    
    if restart:
        game_won, guess_count, user_score, secret_number = reset_variables()
    else:
        break

display_highscores()
display_farewell(user_name)
