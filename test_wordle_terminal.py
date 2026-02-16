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
    
    def test_correct_place(self):
        result = correct_place('a')
        assert result == Back.GREEN + 'a' + Back.RESET
    
    def test_correct_letter(self):
        result = correct_letter('b')
        assert result == Back.YELLOW + 'b' + Back.RESET
    
    def test_incorrect_letter(self):
        result = incorrect_letter('z')
        assert result == Style.DIM + 'z' + Back.RESET
       
class TestCompare:
    
    def test_all_correct(self):
        # Test case 1: All letters correct and in the correct position
        result = compare("tango", "tango")
        assert result == correct_place("t") + correct_place("a") + correct_place("n") + correct_place("g") + correct_place("o")
    
    
    def test_correct_letter_wrong_position(self):
        # Test case 2: Letters exist but all in wrong positions
        result = compare("notag", "tango")
        # All should be yellow (correct letter, wrong position)
        assert result == correct_letter("n") + correct_letter("o") + correct_letter("t") + correct_letter("a") + correct_letter("g")
    
    def test_correct_position(self):
         # Test case 3: Mixed case with some correct and some incorrect letters
        result = compare("mango", "tango")
        assert result == incorrect_letter("m") + correct_place("a") + correct_place("n") + correct_place("g") + correct_place("o")
      
    def test_all_wrong(self):
        # Test case 4: All letters incorrect    
        result = compare("qwerk", "tango")
        assert result == incorrect_letter("q") + incorrect_letter("w") + incorrect_letter("e") + incorrect_letter("r") + incorrect_letter("k")       
    
    
class TestCheckWord:
    
    @patch('wordle_terminal.random.choice', return_value='tango')
    @patch('builtins.input', return_value='tango')
    @patch('builtins.print')
    @patch('builtins.exit', side_effect=SystemExit)
    def test_win(self, mock_exit, mock_print, mock_input, mock_choice):
        # Test winning by guessing the correct word
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
        # Test exiting immediately with 'no'
        wordlist = ["tango", "mango"]
        
        with pytest.raises(SystemExit):
            check_word(wordlist)
        
        mock_exit.assert_called_once()
    
    @patch('wordle_terminal.random.choice', return_value='tango')
    @patch('builtins.input')
    @patch('builtins.print')
    @patch('builtins.exit', side_effect=SystemExit)
    def test_invalid_length(self, mock_exit, mock_print, mock_input, mock_choice):
        # Test rejection of invalid words
        wordlist = ["tango", "mango"]
        mock_input.side_effect = ["tan", "kalak", "123", "tango"]
        
        with pytest.raises(SystemExit):
            check_word(wordlist)
        
        # Verify error message
        calls = [str(call) for call in mock_print.call_args_list]
        assert any('5 letter valid word' in call for call in calls)
  
    @patch('wordle_terminal.random.choice', return_value='tango')
    @patch('builtins.input')
    @patch('builtins.print')
    @patch('builtins.exit', side_effect=SystemExit)
    def test_max_attempts(self, mock_exit, mock_print, mock_input, mock_choice):
        # Test reaching max attempts without guessing the word
        wordlist = ['tango', 'bread', 'crane', 'drake', 'flame', 'grape', 'house']
        mock_input.side_effect = ['bread', 'crane', 'drake', 'flame', 'grape', 'house']
        
        with pytest.raises(SystemExit):
            check_word(wordlist)
        
        calls = [str(call) for call in mock_print.call_args_list]
        assert any('max attempts' in call.lower() for call in calls)
    
   


class TestMain:
    
    @patch('builtins.input', return_value='no')
    @patch('builtins.print')
    def test_exit_immediately(self, mock_print, mock_input):
        # Test exiting immediately at game start
        main()
        
        calls = [str(call) for call in mock_print.call_args_list]
        assert any('Thanks for playing' in call for call in calls)
    
    @patch('wordle_terminal.check_word')  
    @patch('builtins.input')
    @patch('builtins.print')
    def test_play_then_exit(self, mock_print, mock_input, mock_check_word):
        # Test playing once then exiting
        mock_input.side_effect = ['yes', 'no']
        
        main()
        
        # Verify check_word was called once
        mock_check_word.assert_called_once()
        calls = [str(call) for call in mock_print.call_args_list]
        assert any('Thanks for playing' in call for call in calls)
        
    @patch('builtins.input')
    @patch('builtins.print')    
    def test_invalid_start_input(self, mock_print, mock_input):
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
    
    wordlist = ['tango', 'mango']
    mock_input.side_effect = [invalid_input, 'tango']
    
    with pytest.raises(SystemExit):
        check_word(wordlist)
    
    calls = [str(call) for call in mock_print.call_args_list]
    assert any('5 letter valid word' in call for call in calls)