# Wordle_Helper
Coded a little helper app to suggest words to try in [Wordle](https://www.powerlanguage.co.uk/wordle/) puzzles.

## Coding Concepts
- Reading in a word list in text file format. Update: Turns out the list of possible puzzle words is embedded in the page source, provided an updated wordle.txt file of the 2000+ possible words.
- Various string manipulation to check for word length and whether necessary letters are at particular indexes.
- Use of pyautogui and pytesseract for the OCR version which obviates the need to manually input the nope, green and yellow letters in code.

## Notes
Word suggestions are based on letter frequencies. The code scans through all words that are still possible given the current set of constraints (i.e. letters not in the secret word, letters in correct positions, letters in wrong positions), and identifies the as-yet-untried letters that occur most frequently and suggests them for testing.
