import colorama
import pytest
from wordle_terminal import compare, correct_place, correct_letter, incorrect_letter
from colorama import Fore, Back, Style, init    
init()

def correct_place(letter):
    return Back.GREEN + letter + Back.RESET


def correct_letter(letter):
    return Back.YELLOW + letter + Back.RESET


def incorrect_letter(letter):
    return Style.DIM + letter + Back.RESET 

def test_compare() -> None:
    # Test case 1: All letters correct and in the correct position
    assert compare("tango", "tango") == correct_place("t") + correct_place("a") + correct_place("n") + correct_place("g") + correct_place("o")
    
    # Test case 2: All letters correct but in the wrong position
    assert compare("notag", "tango") == correct_letter("n") + correct_letter("o") + correct_letter("t") + correct_letter("a") + correct_letter("g")
    
      
    # Test case 3: All letters incorrect    
    assert compare("qwerk", "tango") == incorrect_letter("q") + incorrect_letter("w") + incorrect_letter("e") + incorrect_letter("r") + incorrect_letter("k")
    
    # Test case 4: Mixed case with some correct and some incorrect letters
    assert compare("mango", "tango") ==  incorrect_letter("m") + correct_place("a") + correct_place("n") + correct_place("g") + correct_place("o")
    
    