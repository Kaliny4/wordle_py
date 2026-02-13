from colorama import Fore, Back, Style, init

init()
import random

with open("wordle_ord.txt", "r") as f:
    wordlist = [line.strip() for line in f]


def correct_place(letter):
    return Back.GREEN + letter + Back.RESET


def correct_letter(letter):
    return Back.YELLOW + letter + Back.RESET


def incorrect_letter(letter):
    return Style.DIM + letter + Back.RESET


def compare(input_from_user, word):
    output = [""] * len(input_from_user)
    remaining_letters = list(word)

    # Mark correct letter and position - Green
    for i, letter in enumerate(input_from_user):
        if letter == remaining_letters[i]:
            output[i] = correct_place(letter)
            remaining_letters[i] = None

    # Mark correct letter anbut not position - Yellow
    for i, letter in enumerate(input_from_user):
        if output[i]:
            continue
        if letter in remaining_letters:
            output[i] = correct_letter(letter)
            remaining_letters[remaining_letters.index(letter)] = None
        else:
            output[i] = incorrect_letter(letter)
    return "".join(output)


def check_word(wordlist):
    word = random.choice(wordlist)
    attempts = 0
    max_attempts = 6
    while attempts < max_attempts:
        user_word = input().lower()
        if user_word == "no":
            exit()
        if len(user_word) != 5 or not user_word.isalpha() or user_word not in wordlist:
            print("Please enter a 5 letter valid word")
            continue
        elif user_word == word:
            print(Back.WHITE + Fore.RED + "Congrats! the word was:" + word)
            exit()
            
        else:
            attempts += 1
            print(compare(user_word, word))
            print("Try again. Attempts left: ", max_attempts - attempts)
        
    print("You reached max attempts. The word was:", word)
    exit()


def main():
    while True:
        print(Back.WHITE + Fore.BLACK + "Start the game? (yes/no))" + Style.RESET_ALL)
        input_from_user = input()
        if input_from_user == "no":
            break
        elif input_from_user == "yes":
            print("Enter your word: ")
            check_word(wordlist)
        else:
            print("Please enter yes or no")
    print("Thanks for playing!")


if __name__ == "__main__":
    main()
