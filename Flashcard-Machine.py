#-----------Imports-----------#
import random
import time
import urllib.parse
import os
import json
import csv

#-----------User Data----------#
DATA_DIR = "user_data"  # Folder for user.json
HTML_DIR = "study_guides" # Folder for HTML exports

# Folder for your generated study guides
HTML_EXPORT_DIR = "study_guides"

# Ensure the folder exists
if not os.path.exists(HTML_EXPORT_DIR):
    os.makedirs(HTML_EXPORT_DIR)

GUIDES_DIR = "saved_guides" 
os.makedirs(GUIDES_DIR, exist_ok=True)

# Create the folders if they don't exist
if not os.path.exists("user_data"):
    os.makedirs("user_data")
if not os.path.exists("study_guides"):
    os.makedirs("study_guides")

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(HTML_DIR, exist_ok=True)

USER_DB_PATH = os.path.join(DATA_DIR, "users.json")

def save_json(data, filename):
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"❌ Error saving {filename}: {e}")

def load_json(filename):
    if not os.path.exists(filename):
        return {}
    try:
        with open(filename, "r") as f:
            content = f.read().strip()
            return json.loads(content) if content else {}
    except:
        return {}

users_db = load_json(USER_DB_PATH)

#------------Global Config------------#
YES = ["yes", "y", "correct", "ye"]
NO = ["no", "n", "nope"]

def get_confirmation(prompt):
    while True:
        choice = input(prompt).lower().strip()
        if choice in YES: return "yes"
        if choice in NO: return "no"
        print(f"Invalid command. Try 'yes' or 'no'.")

def refresh_screen(title_text):
    print("\033[H\033[2J", end="") 
    print("=" * 50)
    print(title_text.center(50))
    print("=" * 50 + "\n")

def make_clickable(url, text):
    # Standard terminal hyperlink escape sequence
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"

#---------Core Functions---------#

def export_to_csv(flashcards, topic):
    filename = os.path.join(HTML_DIR, f"{topic}_export.csv")
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Question", "Answer"])
        for q, a in flashcards.items():
            writer.writerow([q, a])
    print(f"📊 Data exported to {filename}")
    
def exit_main():
    # Exit logic
    if get_confirmation("\nExit to main menu? ") == "yes":
        showing_results = False
    elif get_confirmation == "no":    
        time.sleep(1)
        print("\nThank you for using Flashcard Machine! Goodbye!")
        time.sleep(3)
        pass

def create_flashcard_html(flashcards, topic):
    # Create the full path: study_guides/Topic_Name.html
    filename = f"{topic.replace(' ', '_')}_study_guide.html"
    filepath = os.path.join(HTML_EXPORT_DIR, filename)

    cards_html = ""
    for q, a in flashcards.items():
        cards_html += f"""
        <div class="card">
            <div class="question"><b>Q:</b> {q}</div>
            <div class="divider"></div>
            <div class="answer"><b>A:</b> {a}</div>
        </div>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{topic} Flashcards</title>
        <style>
            body {{ font-family: sans-serif; background: #1a1a2e; color: white; display: flex; flex-wrap: wrap; justify-content: center; padding: 20px; }}
            .card {{ background: white; color: #333; width: 250px; margin: 10px; padding: 20px; border-radius: 10px; border-top: 5px solid #4CAF50; }}
            .question {{ font-weight: bold; min-height: 40px; }}
            .divider {{ height: 1px; background: #ddd; margin: 10px 0; }}
            .answer {{ color: #27ae60; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1 style="width: 100%; text-align: center;">Topic: {topic}</h1>
        {cards_html}
    </body>
    </html>
    """

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"🌐 Study Guide created at: {filepath}")

def sign_up():
    print("\n--- FLASHCARD SYSTEM SIGN-UP ---")
    while True:
        # Added a 'back' option
        new_user = input("Create a username (or type 'back' to exit): ").strip()
        
        if new_user.lower() == 'back':
            return None # Signal to go back to the main menu
            
        if new_user in users_db:
            print("❌ Error: That username is already taken.")
        elif new_user == "":
            print("❌ Error: Username cannot be blank.")
        else:
            new_pass = input(f"Create a password for {new_user} (have at least 3 characters): ")
            if len(new_pass) < 3:
                print("Not enough characters. Please try logging in again.")
                time.sleep(2)
                sign_up()
            else:
                users_db[new_user] = new_pass
                save_json(users_db, "users.json")
                print(f"\n✅ Account for '{new_user}' created! Logging you in...")
                time.sleep(2)
            return new_user 

def password_system():
    while True:
        ac = input("Do you already have an account? (yes/no): ").lower().strip()
        
        if ac in NO:
            user = sign_up()
            if user: return user
            continue # If they typed 'back', loop back to the start
            
        elif ac in YES:
            if not users_db:
                print("❌ No accounts exist. Sending you to Sign-up...")
                time.sleep(1.5)
                user = sign_up()
                if user: return user
                continue

            attempts = 4
            while attempts > 0:
                # Added the 'noaccount' check here
                u = input("Username (type 'noaccount' to sign up): ").strip()
                
                if u.lower() == "noaccount":
                    user = sign_up()
                    if user: return user
                    break # Break the attempt loop to go back to the 'yes/no' prompt
                
                p = input("Password: ")
        
                if u in users_db and users_db[u] == p:
                    print(f"\nAccess Granted! Welcome back, {u}.\n")
                    return u
                else:
                    attempts -= 1
                    print(f"❌ Invalid. {attempts} attempts left.")
                    time.sleep(1)
            
            if attempts == 0:
                exit("SYSTEM LOCKED. Too many failed attempts.")
        else:
            print("❌ Invalid answer. Please type yes or no.")

def run_flashcard_system(username):
    flashcards = {}
    wrong_answers = []
    refresh_screen(f"Welcome, {username}!")
    
    print("1. Load & Study existing set")
    print("2. Create New set")
    print("3. Edit an existing set")
    mode = input("\nSelect an option: ")

    # Handle Loading and Editing (Both need to pick a file first)
    if mode in ["1", "3"]:
        files = [f for f in os.listdir(GUIDES_DIR) if f.endswith(".json")]
        
        if not files:
            print("❌ No saved sets found. Sending you to 'Create New'...")
            time.sleep(2)
            mode = "2" # Fallback to creation
        else:
            print("\n--- SAVED SETS ---")
            for i, f in enumerate(files, 1):
                print(f"{i}. {f}")
            
            try:
                choice = int(input("\nSelect a number: "))
                filename = files[choice - 1]
                # Load the json from your separate folder
                flashcards = load_json(os.path.join(GUIDES_DIR, filename))
                topic = filename.replace(".json", "")
            except (ValueError, IndexError):
                print("Invalid selection. Restarting...")
                return run_flashcard_system(username)

    # Logic for EDITING
    if mode == "3":
        flashcards = edit_set_logic(flashcards) # The function we built earlier
        save_json(flashcards, os.path.join(GUIDES_DIR, filename))
        print(f"💾 {filename} updated successfully!")
        # Ask if they want to study it now or quit
        if get_confirmation("Study this set now? ") == "no":
            return
    
    elif mode == "2":
        topic = input("Enter study topic (e.g., Physics, History): ").strip() or "General"
    
        while True:
            global question_count
            q = input("\nEnter the question: ")
            a = input("Enter the answer: ")
        
            query = urllib.parse.quote(f"{q}")
            link = make_clickable(f"https://www.google.com/search?q={query}", "[CLICK HERE TO VERIFY]")
            print(f"Check source: {link}")

            if get_confirmation("Save this card? ") == "yes":
                flashcards[q] = a
        
            if get_confirmation("Add another? ") == "no":
                break

            if not flashcards: return

            safe_topic = "".join(x for x in topic if x.isalnum())
            filename = f"{safe_topic} study guide"
            create_flashcard_html(flashcards, topic, filename)
            #--- After adding questions ---
            if get_confirmation("Would you like to save this set for future use? ") == "yes":
                guide_name = input("Enter a filename to save as (e.g., biology_ch1): ").strip()
            # Add .json extension if not there
            if not guide_name.endswith(".json"):
                guide_name += ".json"
    
            save_path = os.path.join(GUIDES_DIR, guide_name)
            save_json(flashcards, save_path)
            print(f"💾 Set saved to {save_path}!")
            print(f"\n✅ {filename} generated!")
            time.sleep(1)
            print(f"\n{guide_name} loading...")
            time.sleep(3)

        try:
            cycles = int(input("\nHow many study rounds? "))
        except:
            cycles = 1

        correct_total = 0
        total_q_asked = len(flashcards) * cycles

        # --- STUDY LOOP ---
        # Initialize these at the start of the function!
        local_correct = 0
        local_total = 0

        for r in range(1, cycles + 1):
            refresh_screen(f"{topic.upper()} - ROUND {r}")
            qs = list(flashcards.keys())
            random.shuffle(qs)
        
            for q in qs:
                local_total += 1
                ans = input(f"\nQUESTION: {q}\nYour Answer: ").strip().lower()
            
                if ans == flashcards[q].lower().strip():
                    print("✨ Correct!")
                    local_correct += 1
                else:
                    print(f"❌ Wrong. Answer: {flashcards[q]}")
                    # We store the mistake as a dictionary
                    wrong_answers.append({
                        "q": q, 
                        "correct": flashcards[q], 
                        "user_said": ans
                    })
            time.sleep(1)

        # --- CALCULATE FINAL SCORE ---
        percent = (local_correct / local_total) * 100 if local_total > 0 else 0

        # --- RESULTS & RANKING LOOP ---
        showing_results = True
        while showing_results:
            refresh_screen("RESULTS")
            time.sleep(1.0)
            print("-" * 25)
            print(f"Final Score: {local_correct}/{local_total}")
            print(f"Grade: {percent:.2f}%")
            print("-" * 25)
        
            if wrong_answers:
                print(f"\n⚠️ You missed {len(wrong_answers)} questions.")
                see_mistakes = input("View your mistake log? (yes/no): ").lower().strip()
                if see_mistakes in YES:
                    refresh_screen("MISTAKE LOG")
                    for item in wrong_answers:
                        q_query = urllib.parse.quote(item['q'])
                        search_link = make_clickable(f"https://google.com/search?q={q_query}", "[Search for Answer]")
                    
                        print(f"Q: {item['q']}")
                        print(f"   ❌ Your Answer: {item['user_said']}")
                        print(f"   ✅ Correct Answer: {item['correct']}")
                        print(f"   🔗 {search_link}")
                        print("-" * 20)
                    input("\nPress Enter to return to Summary...")
                    continue # Go back to the Results screen
            else:
                print("Great job! You didn't miss anything!")

            leadersee = input("\nDo you want to see your ranking detail? (yes/no): ").lower().strip()
            if leadersee in YES:
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
        
        exit_main()

#-------------Run Code------------#
current_user = password_system()
if current_user:
    run_flashcard_system(current_user)
