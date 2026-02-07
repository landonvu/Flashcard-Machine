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

def refresh_screen(title_text):
    print("\033[H\033[2J", end="") # Clears screen
    print("=" * 50)
    print(title_text.center(50))
    print("=" * 50 + "\n")

#---------Core Functions---------#

def create_flashcard_html(flashcards, filename="study_guide.html"):
    # Updated to handle MULTIPLE cards in one file
    cards_html = ""
    for q, a in flashcards.items():
        cards_html += f"""
        <div class="card">
            <div class="question">Q: {q}</div>
            <hr>
            <div class="answer">A: {a}</div>
        </div>
        """

    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: sans-serif; background-color: #2c3e50; padding: 50px; display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; }}
            .card {{ background: white; width: 300px; padding: 20px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); text-align: center; }}
            .question {{ color: #e67e22; font-size: 1.1em; font-weight: bold; }}
            .answer {{ color: #27ae60; font-size: 1.3em; margin-top: 10px; }}
        </style>
    </head>
    <body>
        {cards_html}
    </body>
    </html>
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_template)

def run_flashcard_system():
    flashcards = {}
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
        else:
            print("Restarting question...")
            continue

        more = get_confirmation("Add another question? ")
        if more == "no":
            adding_questions = False

    if not flashcards:
        print("No questions saved. Exiting.")
        return

    # Generate the HTML file once all questions are in
    create_flashcard_html(flashcards)
    print("\n--- HTML Study Guide Generated! ---")

    try:
        cycles = int(input("\nHow many times do you want to repeat the set? "))
    except ValueError:
        cycles = 1

    # Simple countdown
    for i in range(3, 0, -1):
        print(f"\rReady? Starting in... {i}", end="")
        time.sleep(1)

    # Quizzing Loop
    for cycle_num in range(1, cycles + 1):
        refresh_screen(f"ROUND {cycle_num} OF {cycles}")
        q_list = list(flashcards.keys())
        random.shuffle(q_list)
        score = 0

        for current_q in q_list:
            print(f"\nQUESTION: {current_q}")
            user_ans = input("Your Answer: ").strip().lower()
            if user_ans == flashcards[current_q].lower().strip():
                print("✨ Correct!")
                score += 1
            else:
                print(f"❌ Wrong. The answer was: {flashcards[current_q]}")
        
        print(f"\nRound Complete! Score: {score}/{len(q_list)}")
        time.sleep(2)

def password_system():
    users_db = {}
    print("--- FLASHCARD SYSTEM SIGN-UP ---")
    new_user = input("Create a username: ")
    new_pass = input("Create a password: ")
    users_db[new_user] = new_pass
    print("Account created!\n")

    while True:
        print("--- LOG IN ---")
        u = input("Username: ")
        p = input("Password: ")
        if u in users_db and users_db[u] == p:
            print("\nAccess Granted!\n")
            break
        print("Invalid credentials. Try again.")

#-------------Run Code------------#
password_system()
run_flashcard_system()
