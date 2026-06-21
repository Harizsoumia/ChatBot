import json
import random
import os
import re

try:
    import colorama
    colorama.init(autoreset=True)
except ImportError:
    colorama = None

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"
WHITE = "\033[97m"
RED = "\033[91m"

# Emojis have been removed for broader terminal compatibility.


def color(text, color_code):
    return f"{color_code}{text}{RESET}"


def bot_print(message, end="\n"):
    print(f"{color('Bot:', GREEN)} {message}", end=end)


def load_intents():
    """Loads the external JSON knowledge base safely."""
    if not os.path.exists("intents_clean.json"):
        print(color("Error: intents_clean.json file missing! Creating a temporary one...", RED))
        return {}
    with open("intents_clean.json", "r") as file:
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


def _match_keyword(keyword, clean_input, words):
    """Match keyword robustly: whole-word for single words, substring for phrases."""
    key = keyword.lower()
    if " " in key:  # phrase
        return key in clean_input
    # single-word: check whole-word match
    if key in words:
        return True
    # simple plural handling: match 'articles' -> 'article'
    for w in words:
        if w.endswith('s') and w[:-1] == key:
            return True
    return False


def english_tutor_chatbot():
    """Advanced English learning chatbot with progress tracking."""
    print(color("=" * 55, CYAN))
    print(color("   ENGLISH LEARNING ASSISTANT", MAGENTA))
    print(color("   Master English Basics with Confidence!", BLUE))
    print(color("   (Type 'exit', 'bye', or 'quit' to close)", BLUE))
    print(color("   (Type 'topics' to see all lessons)", BLUE))
    print(color("   (Type 'progress' to check your learning)", BLUE))
    print(color("=" * 55, CYAN) + "\n")
    
    # Load external knowledge base
    intents = load_intents()
    
    # State Memory Tracking
    user_name = None
    topics_learned = set()  # Track which topics user has learned
    
    bot_print(color(f"Welcome! What's your name? I'll personalize your learning experience.", WHITE))
    
    while True:
        # Step 1: Input & Sanitization
        raw_input = input(color("You: ", YELLOW)).strip()
        clean_input = raw_input.lower().strip()
        
        # Empty input handling
        if not clean_input:
            if user_name:
                bot_print(color("Please ask me a question about English learning!", WHITE))
            continue
        
        # Step 2: Handle First-Time State Check (Name Assignment)
        if user_name is None:
            user_name = raw_input.strip()
            bot_print(color(f"Great to meet you, {user_name}! I'm here to help you master English basics.", WHITE))
            continue
        
        # Step 3: Hardcoded Global Exit Guardrail
        if any(exit_word in clean_input for exit_word in ["exit", "bye", "quit", "shutdown"]):
            if topics_learned:
                bot_print(color(f"Amazing work today, {user_name}! You explored {len(topics_learned)} topics:", WHITE))
                print(color(f"   {', '.join(sorted(topics_learned))}", CYAN))
            bot_print(color(f"Keep practicing, and your English will shine! Goodbye, {user_name}!", WHITE))
            break
        
        # Step 4: Handle special commands (accept variations)
        if "topic" in clean_input or clean_input == "topics":
            bot_print(color("Here are all the English lessons I can teach:", WHITE))
            for i, (topic, data) in enumerate(intents.items(), 1):
                if topic not in ["greetings", "purpose", "help"]:
                    status = color("✓ Learned", GREEN) if topic in topics_learned else color("○ Not yet", YELLOW)
                    print(color(f"   {i}. {topic.replace('_', ' ').title()} ", BLUE) + status)
            bot_print(color("Ask me about any of these topics, {name}!".format(name=user_name), WHITE))
            continue
        
        if "progress" in clean_input or clean_input == "progress":
            if not topics_learned:
                next_topic = get_learning_suggestions(topics_learned)
                bot_print(color(f"You haven't started yet! I suggest starting with: {next_topic.replace('_', ' ').title()}", WHITE))
            else:
                bot_print(color(f"Great progress, {user_name}! You've learned {len(topics_learned)} topics:", WHITE))
                print(color(f"   {', '.join(sorted(topics_learned)).title()}", CYAN))
                next_topic = get_learning_suggestions(topics_learned)
                if next_topic:
                    bot_print(color(f"Next, I recommend learning about: {next_topic.replace('_', ' ').title()}", WHITE))
                else:
                    bot_print(color(f"Wow! You've completed all topics. Keep practicing!", WHITE))
            continue
        
        # Step 5: Dynamic JSON Intent Processing Loop
        matched_intent = False
        
        # Precompute whole-word tokens to avoid false substring matches
        words = set(re.findall(r"\b\w+\b", clean_input))

        # Pick the best matching intent (prefer longest/more specific keyword)
        best_intent = None
        best_keyword = ""
        for intent_name, data in intents.items():
            for keyword in data["keywords"]:
                if _match_keyword(keyword, clean_input, words):
                    # prefer longer keyword (more specific)
                    if len(keyword) > len(best_keyword):
                        best_keyword = keyword
                        best_intent = intent_name

        if best_intent:
            chosen_response = random.choice(intents[best_intent]["responses"])
            formatted_response = chosen_response.format(name=user_name)
            bot_print(color(formatted_response, WHITE))
            if best_intent not in ["greetings", "purpose", "help"]:
                topics_learned.add(best_intent)
            matched_intent = True
        
        # Step 6: Fallback Mechanism with helpful suggestions
        if not matched_intent:
            bot_print(color(f"I didn't quite understand that, {user_name}.", WHITE))
            bot_print(color("Try asking about:", WHITE))
            print(color("   • 'parts of speech' - Learn nouns, verbs, adjectives, etc.", BLUE))
            print(color("   • 'verb tenses' - Master past, present, future tenses", BLUE))
            print(color("   • 'sentence structure' - Build correct sentences", BLUE))
            print(color("   • 'punctuation' - Use commas, periods, apostrophes correctly", BLUE))
            print(color("   • 'common mistakes' - Avoid their/there/they're confusion", BLUE))
            print(color("   • 'vocabulary' - Build your word list", BLUE))
            print(color("   • 'writing tips' - Improve your essays", BLUE))
            print(color("   • Type 'topics' to see all available lessons\n", BLUE))

if __name__ == "__main__":
    english_tutor_chatbot()