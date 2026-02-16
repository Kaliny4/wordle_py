"""
Test for Wordle Terminal Game

python -m pytest test_wordle_terminal.py -v

Tests cover color marking, word comparison logic, game flow, and user input validation.

Test Classes:
    - TestColorFunctions: Tests color formatting
    - TestCompare: Tests word comparison algorithm
    - TestCheckWord: Tests main game loop
    - TestMain: Tests game menu and flow control


Requirements:
    - pytest
    - colorama
    - unittest.mock
"""

import pytest
import colorama
from unittest.mock import patch, mock_open, MagicMock
from colorama import Fore, Back, Style, init    
init()


# Mock the reading of wordlist to avoid file I/O in tests
mock_wordlist = "tango\nmango\nbread\ncrane\ndrake\nflame\ngrape\nhouse\n"

with patch('builtins.open', mock_open(read_data=mock_wordlist)):
    from wordle_terminal import (
        correct_place,
        correct_letter,
        incorrect_letter,
        compare,
        check_word,
        main
    )


class TestColorFunctions:
    """
        These functions with the help of colorama libary apply  color  to letters based on their correctness:
        - Green background: Correct letter in correct position
        - Yellow background: Correct letter in wrong position
        - Dim style: Incorrect letter
    """
    
    def test_correct_place(self):
        """
        Test correct_place() returns green background formatting.
        
        Expected behavior:
        - Letter 'a' wrapped in green background 
        - Contains Back.GREEN, the letter, and Back.RESET
        """
        result = correct_place('a')
        assert result == Back.GREEN + 'a' + Back.RESET
    
    def test_correct_letter(self):
        """
        Test correct_letter() returns yellow background formatting.
        
        Expected behavior:
        - Letter 'b' wrapped in yellow background 
        - Contains Back.YELLOW, the letter, and Back.RESET
        """
        result = correct_letter('b')
        assert result == Back.YELLOW + 'b' + Back.RESET
    
    def test_incorrect_letter(self):
        """
        Test incorrect_letter() returns dim formatting.
        
        Expected behavior:
        - Letter 'z' wrapped in dim 
        - Contains Style.DIM, the letter, and Back.RESET
        """
        
        result = incorrect_letter('z')
        assert result == Style.DIM + 'z' + Back.RESET
       
class TestCompare:
    """
    Test for the compare() function.
    
    The compare function is the core game logic that determines which letters
    are correct, which are in the wrong position, and which are incorrect.
    
    Algorithm:
    1. First pass: Mark exact matches (green)
    2. Second pass: Mark letters that exist but are in wrong position (yellow)
    3. Remaining letters are marked as incorrect (dim)
    """
    def test_all_correct(self):
        """
        Test when all letters are correct and in correct positions.
        
        Input: "tango" vs Target: "tango"
        Expected: All 5 letters should be green
        
        This represents a winning guess.
        """
        # Test case 1: All letters correct and in the correct position
        result = compare("tango", "tango")
        assert result == correct_place("t") + correct_place("a") + correct_place("n") + correct_place("g") + correct_place("o")
    
    
    def test_correct_letter_wrong_position(self):
        """ Test when all letters are correct but in the wrong positions.
        Input: "notag" vs Target: "tango"
        Expected: All 5 letters should be yellow
        
        This tests the second pass of the algorithm where letters are correct but misplaced.
        """
        # Test case 2: Letters exist but all in wrong positions
        result = compare("notag", "tango")
        # All should be yellow (correct letter, wrong position)
        assert result == correct_letter("n") + correct_letter("o") + correct_letter("t") + correct_letter("a") + correct_letter("g")
    
    def test_correct_position(self):
        """
        Test a mix of correct letters in correct and wrong positions.
        
        Input: "mango" vs Target: "tango"
        Expected: 'm' is incorrect (dim), 'a', 'n', 'g', 'o' are correct and in correct positions (green)
        
        This tests the algorithm's ability to handle a mix of correct and incorrect letters.
        """
         # Test case 3: Mixed case with some correct and some incorrect letters
        result = compare("mango", "tango")
        assert result == incorrect_letter("m") + correct_place("a") + correct_place("n") + correct_place("g") + correct_place("o")
      
    def test_all_wrong(self):
        """
        Test when all letters are incorrect.
        
        Input: "qwerk" vs Target: "tango"
        Expected: All 5 letters should be dim (incorrect)
        
        This tests the algorithm's ability to mark all letters as incorrect.
        """
        # Test case 4: All letters incorrect    
        result = compare("qwerk", "tango")
        assert result == incorrect_letter("q") + incorrect_letter("w") + incorrect_letter("e") + incorrect_letter("r") + incorrect_letter("k")       
    
    
class TestCheckWord:
    """
    Test for the check_word() function.
    
    This is the main game loop that:
    1. Selects a random word
    2. Gets user input
    3. Validates input
    4. Compares input to target word
    5. Tracks attempts
    6. Handles win/loss conditions
    
    Mocking Strategy:
    - random.choice: Control which word is selected (predictable tests)
    - builtins.input: Simulate user keyboard input
    - builtins.print: Capture output for verification
    - builtins.exit: Raise SystemExit instead of terminating (allows test to catch)
    
    Note: All tests use pytest.raises(SystemExit) because check_word() calls exit()
    when the game ends. The mock makes exit() raise SystemExit which breaks the
    while loop and allows the test to continue.
    """
    
    @patch('wordle_terminal.random.choice', return_value='tango')
    @patch('builtins.input', return_value='tango')
    @patch('builtins.print')
    @patch('builtins.exit', side_effect=SystemExit)
    
    def test_win(self, mock_exit, mock_print, mock_input, mock_choice):
        """
        Test winning.
        
        Scenario: User guesses "tango", target word is "tango"
        
        Expected behavior:
        1. User inputs "tango"
        2. Matches target word
        3. Check that print congratulations message
        4. Call exit() once
        
        """
        
        wordlist = ["tango", "mango"]
        
        with pytest.raises(SystemExit):
            check_word(wordlist)
        
        mock_exit.assert_called_once()
        # Check that success message was printed
        assert any('Congrats' in str(call) for call in mock_print.call_args_list)
    
    @patch('wordle_terminal.random.choice', return_value='tango')
    @patch('builtins.input', return_value='no')
    @patch('builtins.print')
    @patch('builtins.exit', side_effect=SystemExit)
    
    def test_exit_on_no(self, mock_exit, mock_print, mock_input, mock_choice):
        """
        Test exiting on user input 'no'.
        
        Scenario: User inputs 'no' at the start of a game
        
        Expected behavior:
        1. User inputs 'no'
        2. Game exits without playing
        3. Print exit message
        4. Call exit() once
        2. Check that exit message was printed
        
        """
    
        wordlist = ["tango", "mango"]
        
        with pytest.raises(SystemExit):
            check_word(wordlist)
        
        mock_exit.assert_called_once()
    
    @patch('wordle_terminal.random.choice', return_value='tango')
    @patch('builtins.input')
    @patch('builtins.print')
    @patch('builtins.exit', side_effect=SystemExit)
    
    def test_invalid(self, mock_exit, mock_print, mock_input, mock_choice):
        """
        Test invalid inputs.
        
        Scenario: User inputs invalid words, then a valid word
        
        Expected behavior:
        1. User inputs "tan" (too short)
        2. User inputs "kalak" (not in wordlist)
        3. User inputs "123" (numbers)
        4. User inputs "tango" (valid word)
        5. Game continues with valid word
        6. Print error messages for invalid words
        7. Invalid inputs don't count as attempts
    
        """
        wordlist = ["tango", "mango"]
        mock_input.side_effect = ["tan", "kalak", "123", "tango"]
        
        with pytest.raises(SystemExit):
            check_word(wordlist)
        
        calls = [str(call) for call in mock_print.call_args_list]
        assert any('5 letter valid word' in call for call in calls)
  
    @patch('wordle_terminal.random.choice', return_value='tango')
    @patch('builtins.input')
    @patch('builtins.print')
    @patch('builtins.exit', side_effect=SystemExit)
    
    def test_max_attempts(self, mock_exit, mock_print, mock_input, mock_choice):
        """ 
        Test reaching max attempts without guessing the word
        This tests the loss condition.
        
        Scenario: User inputs 6 incorrect guesses, then game ends
        
        Expected behavior:
        1. User inputs 6 incorrect words    
        2. Game ends after 6 attempts
        3. Print max attempts message
        4. Call exit() once
        
        """
        
        wordlist = ['tango', 'bread', 'crane', 'drake', 'flame', 'grape', 'house']
        mock_input.side_effect = ['bread', 'crane', 'drake', 'flame', 'grape', 'house']
        
        with pytest.raises(SystemExit):
            check_word(wordlist)
        
        calls = [str(call) for call in mock_print.call_args_list]
        assert any('max attempts' in call.lower() for call in calls)
    
   


class TestMain:
    """
    Test for the main() function.
    
    The main() function handles:
    1. Game menu display
    2. User menu choice validation
    3. Starting new games
    4. Game loop continuation
    5. Exit handling
    
    Mocking Strategy:
    - builtins.input: Simulate user menu input
    - builtins.print: Capture output for verification
    - wordle_terminal.check_word: Mock to avoid running full game loop
    - builtins.exit: Raise SystemExit instead of terminating (allows test to catch)
    
    """
    
    @patch('builtins.input', return_value='no')
    @patch('builtins.print')
    
    def test_exit_immediately(self, mock_print, mock_input):
        """
        Test exiting immediately without playing.
        
        Scenario: User selects 'no' at the start menu
        
        Expected behavior:
        1. Display "Start the game?" prompt
        2. User inputs "no"
        3. Exit loop
        4. Print "Thanks for playing!"
        
        This tests the exit path without starting a game.
        """
        
        main()
        
        calls = [str(call) for call in mock_print.call_args_list]
        assert any('Thanks for playing' in call for call in calls)
    
    @patch('wordle_terminal.check_word')  
    @patch('builtins.input')
    @patch('builtins.print')
    
    def test_play_then_exit(self, mock_print, mock_input, mock_check_word):
        """
        Test playing once then exiting.
        
        Scenario: User selects 'yes' to start game, then 'no' to exit
        
        Expected behavior:
        1. Display "Start the game?" prompt
        2. User inputs "yes" to start game
        3. User inputs "no" to exit game
        4. Exit loop
        5. Print "Thanks for playing!"
        
        """
        
        mock_input.side_effect = ['yes', 'no']
        
        main()
        
        # Verify check_word was called once
        mock_check_word.assert_called_once()
        calls = [str(call) for call in mock_print.call_args_list]
        assert any('Thanks for playing' in call for call in calls)
        
    @patch('builtins.input')
    @patch('builtins.print')    
    def test_invalid_start_input(self, mock_print, mock_input):
        """
        Test handling of invalid input at game start.
        
        Scenario: User inputs invalid response at start menu, then exits
        
        Expected behavior:
        1. Display "Start the game?" prompt
        2. User inputs "maybe" (invalid)
        3. Print "Please enter yes or no"
        4. User inputs "no"
        5. Exit loop
        6. Print "Thanks for playing!"
        
        """
        # Test handling of invalid input at game start
        mock_input.side_effect = ['maybe', 'no']
        
        main()
        
        calls = [str(call) for call in mock_print.call_args_list]
        assert any('Please enter yes or no' in call for call in calls)


# Parametrized tests for invalid inputs
@pytest.mark.parametrize("invalid_input", [
    'cat',      # too short
    'taaangooo',  # too long  
    '12345',    # numbers
    'tan go',    # space
    'tan!go',    # special char
])
@patch('wordle_terminal.random.choice', return_value='tango')
@patch('builtins.input')
@patch('builtins.print')
@patch('builtins.exit', side_effect=SystemExit)

def test_invalid_inputs(mock_exit, mock_print, mock_input, mock_choice, invalid_input):
    """
    Parametrized test for various invalid input types.
    
    This single test function runs 5 times with different invalid inputs
    
    Scenario for each:
    1. User inputs invalid word
    2. System rejects with error message
    3. User inputs "tango" (valid, wins)
    
    Expected behavior:
    - Invalid input rejected
    - Error message "5 letter valid word" displayed
    - Game continues (doesn't count as attempt)
    - Valid input accepted

    """
    
    wordlist = ['tango', 'mango']
    mock_input.side_effect = [invalid_input, 'tango']
    
    with pytest.raises(SystemExit):
        check_word(wordlist)
    
    calls = [str(call) for call in mock_print.call_args_list]
    assert any('5 letter valid word' in call for call in calls)

"""
PS C:\Users\SPAC-O-6\Desktop\wordle_py> python -m pytest test_wordle_terminal.py -vv
=========================================================== test session starts ===========================================================
platform win32 -- Python 3.13.11, pytest-9.0.2, pluggy-1.6.0 -- C:\Program Files\Python313\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\SPAC-O-6\Desktop\wordle_py
collected 19 items                                                                                                                         

test_wordle_terminal.py::TestColorFunctions::test_correct_place PASSED                                                               [  5%] 
test_wordle_terminal.py::TestColorFunctions::test_correct_letter PASSED                                                              [ 10%] 
test_wordle_terminal.py::TestColorFunctions::test_incorrect_letter PASSED                                                            [ 15%] 
test_wordle_terminal.py::TestCompare::test_all_correct PASSED                                                                        [ 21%] 
test_wordle_terminal.py::TestCompare::test_correct_letter_wrong_position PASSED                                                      [ 26%] 
test_wordle_terminal.py::TestCompare::test_correct_position PASSED                                                                   [ 31%] 
test_wordle_terminal.py::TestCompare::test_all_wrong PASSED                                                                          [ 36%]
test_wordle_terminal.py::TestCheckWord::test_win PASSED                                                                              [ 42%] 
test_wordle_terminal.py::TestCheckWord::test_exit_on_no PASSED                                                                       [ 47%] 
test_wordle_terminal.py::TestCheckWord::test_invalid_length PASSED                                                                   [ 52%] 
test_wordle_terminal.py::TestCheckWord::test_max_attempts PASSED                                                                     [ 57%] 
test_wordle_terminal.py::TestMain::test_exit_immediately PASSED                                                                      [ 63%] 
test_wordle_terminal.py::TestMain::test_play_then_exit PASSED                                                                        [ 68%]
test_wordle_terminal.py::TestMain::test_invalid_start_input PASSED                                                                   [ 73%] 
test_wordle_terminal.py::test_invalid_inputs[cat] PASSED                                                                             [ 78%] 
test_wordle_terminal.py::test_invalid_inputs[taaangooo] PASSED                                                                       [ 84%]
test_wordle_terminal.py::test_invalid_inputs[12345] PASSED                                                                           [ 89%] 
test_wordle_terminal.py::test_invalid_inputs[tan go] PASSED                                                                          [ 94%] 
test_wordle_terminal.py::test_invalid_inputs[tan!go] PASSED                                                                          [100%] 

=========================================================== 19 passed in 0.17s ============================================================ 
"""