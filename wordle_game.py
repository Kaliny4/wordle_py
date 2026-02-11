from colorama import Fore, Back, Style, init 
init()
import random

def correct_place(letter):
    return Back.GREEN + letter + Back.RESET

def correct_letter(letter):
    return Back.YELLOW + letter + Back.RESET

def incorrect_letter(letter):
    return Style.DIM + letter + Back.RESET

def compare(input_from_user, word):
    output = [""] * len(input_from_user)
    remaining_letters = list(word)

    for i, letter in enumerate(input_from_user):
        if letter == remaining_letters[i]:
            output[i] = correct_place(letter)
            remaining_letters[i] = None 

    for i, letter in enumerate(input_from_user):
        if output[i]:
            continue
        if letter in remaining_letters:
            output[i] = correct_letter(letter)
            remaining_letters[remaining_letters.index(letter)] = None
        else:
            output[i] = incorrect_letter(letter)
            
    return ''.join(output)

with open('wordle_ord.txt', 'r') as f:
    wordlist = [line.strip() for line in f]


while True:
    print(Back.WHITE + Fore.BLACK + "Start the game? (yes/no))" + Style.RESET_ALL)
    input_from_user = input()
    if input_from_user == "no":
        break
    elif input_from_user == "yes":
        attempts = 0
        word = random.choice(wordlist)
        print("Enter your word: ")

        while attempts < 6:
            temp_user_word = input().lower()
            if temp_user_word == "no":
                break
            if len(temp_user_word) != 5 or not temp_user_word.isalpha() or temp_user_word not in wordlist:
                print("Please enter a 5 letter valid word")
                continue
            
            user_word = temp_user_word

            result = compare(user_word, word)
            print(result)
            if word == user_word:
                print("Congrats")
                attempts = 6
                break
            attempts += 1
            
        print("The word was: ", word)

    else:
        print("Please enter yes or no")

   
print("Thanks for playing!")
    