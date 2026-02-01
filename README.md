# Flashcard-Machine
A basic flashcard generator

#-----------Imports-----------#

import random
import time
import urllib.parse
import os

#------------Global Config------------#
YES = ["yes", "y", "yes.", "correct", "it is correct."]
NO = ["no", "n", "no.", "nope", "nope."]

title = "--- FLASHCARD MACHINE ---"

def get_confirmation(prompt):
    while True:
        choice = input(prompt).lower().strip()
        if choice in YES: return "yes"
        if choice in NO: return "no"

        print(f"Invalid command. Try '{random.choice(YES)}' or '{random.choice(NO)}'.")
        time.sleep(1)
        print('\033[1A\033[K', end='')

def refresh_screen(title):
    # This clears the entire terminal window
    print("\033[H\033[2J", end="")

    # Now the title is automatically reprinted
    print("=" * 50)
    print(title.center(50))
    print("=" * 50 + "\n")

#---------Core Functions---------#

def run_flashcard_system():
    flashcards = {}

    # --- PHASE 1: ENTERING QUESTIONS ---
    adding_questions = True
    while adding_questions:
        q = input("\nEnter the question: ")
        a = input("Enter the answer: ")

        query = urllib.parse.quote(q)
        print(f"Verify here if needed: https://www.google.com/search?q={query}")

        confirm = get_confirmation("Is this correct? ")
        if confirm == "yes":
            flashcards[q] = a
            print("Question saved!")
            time.sleep(1)
            k = True
        if confirm == "no":
            print("Restarting question!")
            time.sleep(1.5)
            print('\033[1A\033[K')
            print("Restarting question!")
            time.sleep(1.5)
            print('\033[1A\033[K')
            print("Restarting question!")
            time.sleep(1.5)
            print('\033[1A\033[K')
            run_flashcard_system()

        more = get_confirmation("Add another question? ")
        if more == "no":
            adding_questions = False

    if not flashcards:
        print("No questions saved. Exiting.")
        return

    # --- PHASE 2: SETUP CYCLES ---
    try:
        cycles = int(input("\nHow many times do you want to repeat the question set? "))
    except ValueError:
        print("Invalid number. Setting cycles to 1.")
        cycles = 1

    cycle_time = 5
    while cycle_time > 0:
        print(f"\r\t\tReady? We will begin in... {cycle_time}", end="")
        time.sleep(1)
        cycle_time -= 1

    print("\r\t\t[ GO! ]" + " " * 20) # Clears the line and starts

    refresh_screen("--- FLASHCARD MACHINE ---")


    # --- PHASE 3: QUIZZING ---
    for cycle_num in range(1, cycles + 1):
        print(f"\n--- ROUND {cycle_num} OF {cycles} ---".center(40))
        time.sleep(1)

        q_list = list(flashcards.keys())
        random.shuffle(q_list) # Mix them up each round

        round_score = 0

        for current_q in q_list:
            print(f"\nQUESTION: {current_q}")
            user_ans = input("Your Answer: ").strip().lower()

            if user_ans == flashcards[current_q].lower().strip():
                print("✨ Correct!")
                round_score += 1
            else:
                print(f"❌ Wrong. The answer was: {flashcards[current_q]}")

        print(f"\nRound {cycle_num} Complete! Score: {round_score}/{len(q_list)}")
        time.sleep(2)

    print("\n" + "="*40)
    print("ALL CYCLES FINISHED!".center(40))
    print("="*40)

#-------------Run Code------------#
print("=" * 50)
print(title.center(50))
print("=" * 50 + "\n")
run_flashcard_system()
more = "no"
[Flashcards.py](https://github.com/user-attachments/files/24993915/Flashcards.py)
