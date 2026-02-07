#-----------Imports-----------#
import random
import time
import urllib.parse
import os
import json

#-----------User Data----------#

def save_json(data, filename):
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4) # indent=4 makes it pretty to read
    except Exception as e:
        print(f"❌ Error saving {filename}: {e}")

def load_json(filename):
    if not os.path.exists(filename):
        return {}  # Return empty if file is missing
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except:
        return {}  # Return empty if file is corrupted

#------------Global Config------------#
YES = ["yes", "y", "yes.", "correct", "it is correct.", "ye"]
NO = ["no", "n", "no.", "nope", "nope."]

users_db = load_json("users.json")

question_count = 0
correct_count = 0

title = "--- FLASHCARD MACHINE ---"

def get_confirmation(prompt):
    while True:
        choice = input(prompt).lower().strip()
        if choice in YES: return "yes"
        if choice in NO: return "no"
        print(f"Invalid command. Try '{random.choice(YES)}' or '{random.choice(NO)}'.")
        time.sleep(1)
        print('\033[F\033[K', end='') # Clear the invalid line

def refresh_screen(title_text):
    print("\033[H\033[2J", end="") # Clears screen
    print("=" * 50)
    print(title_text.center(50))
    print("=" * 50 + "\n")

#---------Core Functions---------#

def create_flashcard_html(flashcards, filename="study_guide.html"):
    cards_html = ""
    for q, a in flashcards.items():
        # Using a Template Literal style for the cards
        cards_html += f"""
        <div class="card">
            <div class="question"><b>QUESTION:</b><br>{q}</div>
            <div class="divider"></div>
            <div class="answer"><b>ANSWER:</b><br>{a}</div>
        </div>
        """

    html_full_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flashcard Machine Output</title>
        <style>
            body {{ 
                font-family: 'Segoe UI', sans-serif; 
                background-color: #1a1a2e; 
                color: white; 
                display: flex; 
                flex-wrap: wrap; 
                justify-content: center; 
                padding: 40px;
            }}
            .card {{ 
                background: white; 
                color: #333; 
                width: 280px; 
                margin: 15px; 
                padding: 20px; 
                border-radius: 12px; 
                box-shadow: 0 8px 16px rgba(0,0,0,0.3);
                border-top: 8px solid #4CAF50;
                text-align: center;
            }}
            .question {{ font-size: 1.1em; color: #2c3e50; min-height: 50px; }}
            .divider {{ height: 2px; background: #eee; margin: 15px 0; }}
            .answer {{ font-size: 1.2em; color: #27ae60; font-weight: bold; }}
        </style>
    </head>
    <body>
        {cards_html}
    </body>
    </html>
    """
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_full_body)

def sign_up():
    print("\n--- FLASHCARD SYSTEM SIGN-UP ---")
    while True:
        new_user = input("Create a username: ").strip()
        if new_user in users_db:
            print("❌ Error: That username is already taken.")
        elif new_user == "":
            print("❌ Error: Username cannot be blank.")
        else:
            new_pass = input(f"Create a password for {new_user}: ")
            users_db[new_user] = new_pass
            save_json(users_db, "users.json")
            time.sleep(3)
            refresh_screen(f"Account for '{new_user}' created successfully!")
            break 

def password_system():
    account_fail = 0
    while True:
        ac = input("Do you already have an account? (yes/no): ").lower().strip()
        
        if ac in NO:
            sign_up()
            continue # Go back to ask if they have an account (to log in)
            
        elif ac in YES:
            if not users_db:
                print("❌ No accounts exist. Please sign up first.")
                time.sleep(1.5)
                print("\033[F\033[K" * 2, end="") # Clear message and prompt
                continue

            u = input("Username: ").strip()
            p = input("Password: ")
        
            if u in users_db and users_db[u] == p:
                print(f"\nAccess Granted! Welcome back, {u}.\n")
                return True
            else:
                account_fail += 1
                print(f"❌ Invalid. {4 - account_fail} attempts left.")
                time.sleep(1.5)
                # Clear Username, Password, and Error lines to keep it tidy
                print("\033[F\033[K" * 3, end="") 
                
                if account_fail >= 4:
                    print("SYSTEM LOCKED. Too many failed attempts.")
                    exit()
        else:
            print("❌ Invalid answer. Please type yes or no.")
            time.sleep(1)
            print("\033[F\033[K" * 2, end="")

def run_flashcard_system():
    flashcards = {}
    adding_questions = True
    
    while adding_questions:
        global question_count
        q = input("\nEnter the question: ")
        a = input("Enter the answer: ")
        
        query = urllib.parse.quote(q)
        print(f"Verify: https://www.google.com/search?q={query}")

        if get_confirmation("Is this correct? ") == "yes":
            flashcards[q] = a
            print("Question saved!")
            question_count += 1
        else:
            print("Restarting question...")
            time.sleep(2)
            continue

        if get_confirmation("Add another question? ") == "no":
            adding_questions = False

    if not flashcards:
        return

    create_flashcard_html(flashcards)
    print("\n--- Study Guide Generated! ---")

    try:
        cycles = int(input("\nRepeat how many times? "))
        question_count = question_count * cycles
    except ValueError:
        cycles = 1

    for cycle_num in range(1, cycles + 1):
        refresh_screen(f"ROUND {cycle_num} OF {cycles}")
        q_list = list(flashcards.keys())
        random.shuffle(q_list)
        
        for current_q in q_list:
            global correct_count
            print(f"\nQUESTION: {current_q}")
            user_ans = input("Your Answer: ").strip().lower()
            if user_ans == flashcards[current_q].lower().strip():
                print("✨ Correct!")
                correct_count += 1
            else:
                print(f"❌ Wrong. The answer was: {flashcards[current_q]}")
        time.sleep(2)
    # --- CALCULATE FINAL SCORE ---
    if question_count > 0:
        percent = (correct_count / question_count) * 100
    else:
        percent = 0

    # Determine Ranking
    if percent >= 90:
        ranking = "S-Tier ⭐"
    elif 80 <= percent < 90:
        ranking = "A-Tier 👌"
    elif 70 <= percent < 80:
        ranking = "E-Tier 👍"
    elif 60 <= percent < 70:
        ranking = "B-Tier 👏"
    elif 50 <= percent < 60:
        ranking = "C-Tier 🤔"
    elif 40 <= percent < 50:
        ranking = "D-Tier 😬"
    else:
        ranking = "F-Tier 😟, try again next time..."

    # --- RESULTS & RANKING LOOP ---
    showing_results = True
    while showing_results:
        refresh_screen("RESULTS")
        time.sleep(1.5)
        print(f"\n" + "-"*20)
        print(f"Final Score: {correct_count}/{question_count}")
        time.sleep(3)
        print(f"Grade: {percent:.2f}%")
        print("-" * 20)
        
        time.sleep(1.5)
        
        leadersee = input("\nDo you want to see your ranking detail? (yes/no): ").lower().strip()
        
        if leadersee in YES:
            refresh_screen("RANKING SYSTEM")
            print("1. S-Tier: 90-100%")
            time.sleep(2)
            print("2. A-Tier: 80-89.99%")
            time.sleep(2)
            print("3. E-Tier: 70-79.99%")
            time.sleep(2)
            print("4. B-Tier: 60-69.99%")
            time.sleep(2)
            print("5. C-Tier: 50-59.99%")
            time.sleep(2)
            print("6. D-Tier: 40-49.99%")
            time.sleep(2)
            print("7. F-Tier: 0-39.99%")
            time.sleep(5)
            print("\n" + "="*20)
            print(f"YOUR RANK: {ranking}")
            print("="*20)
            time.sleep(5)
            
            rank_back = input("\nGo back to results summary? (yes/no): ").lower().strip()
            if rank_back in NO:
                showing_results = False
        else:
            showing_results = False

    print("\nThank you for using Flashcard Machine! Goodbye.")

#-------------Run Code------------#
refresh_screen(title)
if password_system():
    run_flashcard_system()
