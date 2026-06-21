import json
import random
import os
from collections import defaultdict

def load_intents():
    """Loads the external JSON knowledge base safely."""
    if not os.path.exists("intents.json"):
        print("Error: intents.json file missing! Creating a temporary one...")
        return {}
    with open("intents.json", "r") as file:
        return json.load(file)

def get_learning_suggestions(topics_learned):
    """Provides learning path suggestions based on progress."""
    suggested_order = [
        "parts_of_speech",
        "sentence_structure", 
        "verb_tenses",
        "punctuation",
        "article_usage",
        "prepositions",
        "common_mistakes",
        "vocabulary",
        "writing_tips",
        "phonetics"
    ]
    
    for topic in suggested_order:
        if topic not in topics_learned:
            return topic
    return None

def english_tutor_chatbot():
    """Advanced English learning chatbot with progress tracking."""
    print("=" * 55)
    print("   🌟 ENGLISH LEARNING ASSISTANT 🌟")
    print("   Master English Basics with Confidence!")
    print("   (Type 'exit', 'bye', or 'quit' to close)")
    print("   (Type 'topics' to see all lessons)")
    print("   (Type 'progress' to check your learning)")
    print("=" * 55 + "\n")
    
    # Load external knowledge base
    intents = load_intents()
    
    # State Memory Tracking
    user_name = None
    topics_learned = set()  # Track which topics user has learned
    
    print("Bot: Welcome! What's your name? I'll personalize your learning experience.\n")
    
    while True:
        # Step 1: Input & Sanitization
        raw_input = input("You: ").strip()
        clean_input = raw_input.lower().strip()
        
        # Empty input handling
        if not clean_input:
            if user_name:
                print("Bot: Please ask me a question about English learning!\n")
            continue
        
        # Step 2: Handle First-Time State Check (Name Assignment)
        if user_name is None:
            user_name = raw_input.strip()
            print(f"Bot: Great to meet you, {user_name}! I'm here to help you master English basics. 📚\n")
            continue
        
        # Step 3: Hardcoded Global Exit Guardrail
        if any(exit_word in clean_input for exit_word in ["exit", "bye", "quit", "shutdown"]):
            if topics_learned:
                print(f"\nBot: Amazing work today, {user_name}! 🎉 You explored {len(topics_learned)} topics:")
                print(f"   {', '.join(sorted(topics_learned))}")
            print(f"Bot: Keep practicing, and your English will shine! Goodbye, {user_name}!\n")
            break
        
        # Step 4: Handle special commands
        if clean_input == "topics":
            print("Bot: Here are all the English lessons I can teach:\n")
            for i, (topic, data) in enumerate(intents.items(), 1):
                if topic not in ["greetings", "purpose", "help"]:
                    status = "✓ Learned" if topic in topics_learned else "○ Not yet"
                    print(f"   {i}. {topic.replace('_', ' ').title()} [{status}]")
            print("\nBot: Ask me about any of these topics, {name}!\n".format(name=user_name))
            continue
        
        if clean_input == "progress":
            if not topics_learned:
                next_topic = get_learning_suggestions(topics_learned)
                print(f"Bot: You haven't started yet! 📖 I suggest starting with: {next_topic.replace('_', ' ').title()}\n")
            else:
                print(f"Bot: Great progress, {user_name}! 🌟 You've learned {len(topics_learned)} topics:")
                print(f"   {', '.join(sorted(topics_learned)).title()}\n")
                next_topic = get_learning_suggestions(topics_learned)
                if next_topic:
                    print(f"Bot: Next, I recommend learning about: {next_topic.replace('_', ' ').title()}\n")
                else:
                    print(f"Bot: Wow! You've completed all topics. Keep practicing! 🏆\n")
            continue
        
        # Step 5: Dynamic JSON Intent Processing Loop
        matched_intent = False
        
        for intent_name, data in intents.items():
            # Check if ANY keyword inside this specific JSON intent matches the input
            if any(keyword in clean_input for keyword in data["keywords"]):
                # Select a random response variety from the array
                chosen_response = random.choice(data["responses"])
                
                # Format the response dynamically with the saved memory state
                formatted_response = chosen_response.format(name=user_name)
                print(f"Bot: {formatted_response}\n")
                
                # Track learning progress for educational topics
                if intent_name not in ["greetings", "purpose", "help"]:
                    topics_learned.add(intent_name)
                
                matched_intent = True
                break  # Exit the loop early since we found a match
        
        # Step 6: Fallback Mechanism with helpful suggestions
        if not matched_intent:
            print(f"Bot: I didn't quite understand that, {user_name}. 🤔\n")
            print("Bot: Try asking about:")
            print("   • 'parts of speech' - Learn nouns, verbs, adjectives, etc.")
            print("   • 'verb tenses' - Master past, present, future tenses")
            print("   • 'sentence structure' - Build correct sentences")
            print("   • 'punctuation' - Use commas, periods, apostrophes correctly")
            print("   • 'common mistakes' - Avoid their/there/they're confusion")
            print("   • 'vocabulary' - Build your word list")
            print("   • 'writing tips' - Improve your essays")
            print("   • Type 'topics' to see all available lessons\n")

if __name__ == "__main__":
    english_tutor_chatbot()