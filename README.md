# Wordle Game in Python 
Six attempts to guess a 5-letter word. Guidance is by using color-coded feedback. 

🟢 Green means correct letter in the correct position  
🟡 Yellow means correct letter in the wrong position  
🔵 Gray means incorrect letter
Good luck!

### Proccess
- Researched existing implementations for inspiration
- Designed and implemented a terminal version
- Developed a Tkinter GUI version
- Implemented automated testing for the terminal version using pytest
- Expanded testing

### Project Structure
- wordle_terminal.py - Terminal version of the game
- wordle_tkinter.py - Tkinter GUI version
- wordle_ord.txt - Word list
- test_wordle_terminal.py - Pytest-based testing using unittest.mock for terminal version
- test_wordle_terminal_compare.py - Early test file for comparison logic for terminal version

### Usage 
git clone https://github.com/Kaliny4/wordle_py.git

cd wordle_py

##### For terminal version

pip install colorama

python wordle_terminal.py

<img width="1475" height="750" alt="image" src="https://github.com/user-attachments/assets/1d0f5412-1555-4012-9bc4-9e9df9a8bc0f" />


##### For test 

pip install pytest

pytest -vv 

##### For GUI version 

pip install tkinter

python wordle_tkinter.py

<img width="1134" height="995" alt="image" src="https://github.com/user-attachments/assets/7e256d77-b415-4722-a259-86c03056e7e7" />

### Reflection
- Writing tests is significantly harder when all logic is placed in one file
- The project would benefit from refactoring into smaller modules

### In Progress
- containerization with Docker
- wordle in C++
- infromation theory and wordle, how to estimate the word  

