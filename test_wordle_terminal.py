import colorama
import pytest
from wordle_terminal import compare
from colorama import Fore, Back, Style, init    
init()

def test_compare() -> None:
    # Test case 1: All letters correct and in the correct position
    assert compare("tango", "tango") == Back.GREEN + "tango" + Back.RESET
    
    # Test case 2: All letters correct but in the wrong position
    assert compare("notag", "tango") == Back.YELLOW + "notag" + Back.RESET
    
    # Test case 3: Some letters correct and in the correct position, some correct but in the wrong position, and some incorrect
    #assert compare("mango", "tango") == Style.DIM + "m" + Back.GREEN + "ango" + Back.RESET
    
    # Test case 4: All letters incorrect    
    assert compare("qwerk", "tango") == Style.DIM + "qwerk" + Back.RESET
    
    