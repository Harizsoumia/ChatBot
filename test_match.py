import json
import re

intents = json.load(open('intents.json'))

def match(clean):
    words = set(re.findall(r"\b\w+\b", clean.lower()))
    best_intent=None
    best_key=""
    for intent_name,data in intents.items():
        for k in data['keywords']:
            key=k.lower()
            matched=False
            if ' ' in key:
                matched = key in clean.lower()
            else:
                if key in words:
                    matched = True
                else:
                    for w in words:
                        if w.endswith('s') and w[:-1]==key:
                            matched = True
                            break
            if matched and len(key)>len(best_key):
                best_key=key
                best_intent=intent_name
    return best_intent

cases = [
    'show me the topics',
    'show me topics',
    'show me the articles',
    'tell me about articles',
    'article',
    'what are verb tenses',
    'help'
]

for c in cases:
    print(f"input: {c!r} -> matched intent: {match(c)!r}")
