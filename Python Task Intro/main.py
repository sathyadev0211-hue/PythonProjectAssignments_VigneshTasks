"""
Task - 3: Python Games using Variables, Conditions, Loops, and String Manipulation
Games Included:
    1. Guess the Number
    2. Word Scramble
"""

import random


# ============================================================
# GAME 1: GUESS THE NUMBER
# ============================================================

def play_guess_the_number():
    """
    Guess the Number Game:
    The computer randomly selects a number within a range (1-100),
    and the player has to guess it within a limited number of attempts.
    Uses: Variables, Conditions, While Loop
    """
    print("\n" + "=" * 50)
    print("       WELCOME TO GUESS THE NUMBER!")
    print("=" * 50)
    print("I have picked a number between 1 and 100.")
    print("You have 7 attempts to guess it. Good luck!\n")

    # Variable: Store the randomly selected secret number
    secret_number = random.randint(1, 100)

    # Variable: Track the number of attempts used
    max_attempts = 7
    attempts_used = 0

    # Variable: Control the game loop
    game_won = False

    # While loop: Keep asking for guesses until won or out of attempts
    while attempts_used < max_attempts:
        attempts_left = max_attempts - attempts_used

        # String manipulation: Dynamic feedback message
        print(f"Attempts left: {attempts_left}")

        # Get player's guess using input
        try:
            player_guess = int(input("Enter your guess: "))
        except ValueError:
            print("Please enter a valid integer.\n")
            continue

        # Increment attempt counter
        attempts_used += 1

        # Condition: Check if the guess is correct, too high, or too low
        if player_guess == secret_number:
            game_won = True
            break
        if player_guess < secret_number:
            print("Too LOW! Try a higher number.\n")
        else:
            print("Too HIGH! Try a lower number.\n")

    # Final result using conditions and string formatting
    if game_won:
        print(f"\nCongratulations! You guessed it right in {attempts_used} attempt(s)!")
        print(f"The number was: {secret_number}")
    else:
        print(f"\nOut of attempts! The secret number was: {secret_number}")
        print("Better luck next time!")

    print("=" * 50 + "\n")


# ============================================================
# GAME 2: WORD SCRAMBLE
# ============================================================

def scramble_word(word):
    """
    String Manipulation Helper:
    Converts the word to a list of characters, shuffles them,
    and joins back into a scrambled string.
    Ensures the scrambled word is always different from the original.
    """
    word_chars = list(word)          # String -> list of characters

    # Keep shuffling until the scrambled word differs from the original
    while True:
        random.shuffle(word_chars)   # Shuffle the list in-place
        scrambled = "".join(word_chars)  # Join characters back to string
        if scrambled != word:        # Condition: ensure it's actually scrambled
            break

    return scrambled


def play_word_scramble():
    """
    Word Scramble Game:
    A random word is picked from a predefined list, scrambled,
    and the player must unscramble it within limited attempts.
    Uses: Variables, Conditions, While Loop, String Manipulation
    """
    print("\n" + "=" * 50)
    print("        WELCOME TO WORD SCRAMBLE!")
    print("=" * 50)
    print("Unscramble the jumbled word.")
    print("You have 4 attempts per word. Type 'skip' to skip.\n")

    # Variable: Predefined word list (as specified in the task)
    words = ['python', 'javascript', 'java', 'automation', 'pytest', 'guvi', 'selenium']

    # Variable: Track overall score
    score = 0
    total_words = len(words)

    # Shuffle the word list so each game is in a different order
    random.shuffle(words)

    # For loop: Iterate over each word in the list
    for index, original_word in enumerate(words):
        print(f"Word {index + 1} of {total_words}")

        # String Manipulation: Scramble the selected word
        scrambled = scramble_word(original_word)

        # String Manipulation: Display scrambled word in uppercase for visibility
        print(f"Scrambled Word: {scrambled.upper()}")

        # Variable: Attempt counter for this word
        max_word_attempts = 4
        word_attempts = 0

        # While loop: Allow multiple attempts per word
        while word_attempts < max_word_attempts:
            word_attempts += 1
            attempts_left = max_word_attempts - word_attempts + 1

            # Get player's guess
            player_input = input(f"Attempt {word_attempts}: Your guess: ").strip().lower()

            # Condition: Player chooses to skip
            if player_input == "skip":
                print(f"Skipped! The word was: '{original_word}'\n")
                break

            # String Manipulation: Compare lowercase versions
            if player_input == original_word:
                score += 1
                print("Correct! Well done!\n")
                break

            # Condition: Give hints based on remaining attempts
            if attempts_left > 1:
                print(f"Wrong! {attempts_left - 1} attempt(s) left. Try again.")
            else:
                print(f"Out of attempts! The word was: '{original_word}'\n")

    # Final score summary using string formatting
    print("=" * 50)
    print("         GAME OVER - WORD SCRAMBLE")
    print("=" * 50)
    print(f"Your Final Score: {score} / {total_words}")

    # Condition: Personalised message based on performance
    if score == total_words:
        print("Perfect score! You're a word wizard!")
    elif score >= total_words // 2:
        print("Good job! Keep practising!")
    else:
        print("Don't give up! Practice makes perfect!")

    print("=" * 50 + "\n")


# ============================================================
# MAIN MENU
# ============================================================

def main():
    """
    Main function: Displays a menu and lets the player choose a game.
    Loops until the player decides to quit.
    """
    print("\n" + "*" * 50)
    print("*      PYTHON MINI GAMES - TASK 3            *")
    print("*" * 50)

    # While loop: Keep showing menu until player quits
    while True:
        print("\nMAIN MENU")
        print("-" * 30)
        print("1. Guess the Number")
        print("2. Word Scramble")
        print("3. Quit")
        print("-" * 30)

        # Get menu choice
        choice = input("Enter your choice (1/2/3): ").strip()

        # Condition: Route to the selected game
        if choice == "1":
            play_guess_the_number()
        elif choice == "2":
            play_word_scramble()
        elif choice == "3":
            print("\nThanks for playing! Goodbye!\n")
            break
        else:
            # String manipulation: Highlight invalid input
            print(f"'{choice}' is not a valid option. Please enter 1, 2, or 3.")


# Entry point
if __name__ == "__main__":
    main()
