import json
import random
import os

def load_intents():
    """Loads the external JSON knowledge base safely."""
    if not os.path.exists("intents.json"):
        print("Error: intents.json file missing! Creating a temporary one...")
        return {}
    with open("intents.json", "r") as file:
        return json.load(file)

def ultimate_chatbot():
    print("=========================================")
    print("  DecodeLabs Advanced Guardrail Engine   ")
    print("  Memory + JSON Data Inflow Activated     ")
    print("  (Type 'exit' or 'bye' to quit)         ")
    print("=========================================\n")
    
    # Load external knowledge base
    intents = load_intents()
    
    # State Memory Tracking
    user_name = None
    
    print("Bot: Initialization complete. Before we loop, what is your name?")
    
    while True:
        # Step 1: Input & Sanitization
        raw_input = input("You: ")
        clean_input = raw_input.lower().strip()
        
        # Step 2: Handle First-Time State Check (Name Assignment)
        if user_name is None:
            if clean_input == "":
                print("Bot: Name cannot be blank. Please enter your name:")
                continue
            user_name = raw_input.strip() # Preserve original capitalization for names
            print(f"Bot: Profile established. Welcome, Engineer {user_name}! System is ready for input.\n")
            continue
            
        # Step 3: Hardcoded Global Exit Guardrail
        if any(exit_word in clean_input for exit_word in ["exit", "bye", "quit", "shutdown"]):
            print(f"Bot: Terminating session. Have a productive day, {user_name}!\n")
            break
            
        # Step 4: Dynamic JSON Intent Processing Loop
        matched_intent = False
        
        for intent_name, data in intents.items():
            # Check if ANY keyword inside this specific JSON intent matches the input
            if any(keyword in clean_input for keyword in data["keywords"]):
                # Select a random response variety from the array
                chosen_response = random.choice(data["responses"])
                
                # Format the response dynamically with the saved memory state (the user's name)
                print(f"Bot: {chosen_response.format(name=user_name)}\n")
                matched_intent = True
                break # Exit the loop early since we found a match
                
        # Step 5: Fallback Mechanism
        if not matched_intent:
            print(f"Bot: Input unrecognised by the intent framework, {user_name}. Try asking about my purpose or type 'help'.\n")

if __name__ == "__main__":
    ultimate_chatbot()