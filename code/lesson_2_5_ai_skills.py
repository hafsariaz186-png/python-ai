"""Task 2.5: AI Skills Toolkit for Sweet Crumbs bakery.

Reusable AI skills (summarize, translate, reply to review) built on one ask_ai() function.
"""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

# Why at the top: loading a model once is faster than rebuilding it on every call
precise_model = ChatOllama(model="llama3.2", temperature=0.1)   # same answer each time
creative_model = ChatOllama(model="llama3.2", temperature=0.9)  # more varied answers


def ask_ai(prompt: str, system: str = "You are a helpful assistant for Sweet Crumbs bakery.",
           creative_mode: bool = False) -> str:
    """Send a prompt to the AI and return its answer as text."""
    model = creative_model if creative_mode else precise_model
    response = model.invoke([SystemMessage(content=system), HumanMessage(content=prompt)])
    return response.text


def summarize(text: str) -> str:
    """Summarize a text in 2 short lines."""
    return ask_ai(f"Summarize this in 2 short lines:\n{text}")


def translate(text: str, language: str = "Urdu") -> str:
    """Translate a text into the given language (default Urdu)."""
    return ask_ai(f"Translate into {language}. Reply with only the translation:\n{text}")


def reply_to_review(review: str) -> str:
    """Write a polite reply to a customer review."""
    # Why creative mode: replies should sound warm and different, not copy-paste
    return ask_ai(f"Write a short, polite reply to this review:\n{review}",
                  system="You are the friendly owner of Sweet Crumbs bakery.",
                  creative_mode=True)


def estimate_tokens(text: str) -> int:
    """Estimate tokens (about 4 characters per token)."""
    return round(len(text) / 4)


# Why assert: if I break this function later, the program stops right away and tells me
assert estimate_tokens("") == 0
assert estimate_tokens("abcd" * 10) == 10

# Why a dictionary: one place to count how often each skill is used
usage = {"summarize": 0, "translate": 0, "reply": 0}

print("Sweet Crumbs AI Toolkit. Commands: /summarize, /translate, /reply, bye")

while True:
    command = input("Command: ").strip().lower()

    if command == "bye":
        break
    elif command == "/summarize":
        text = input("Text to summarize: ")
        print("AI:", summarize(text))
        usage["summarize"] += 1
    elif command == "/translate":
        text = input("Text to translate: ")
        language = input("Language (Enter for Urdu): ").strip()
        if language == "":
            print("AI:", translate(text))  # default parameter is used
        else:
            print("AI:", translate(text, language))
        usage["translate"] += 1
    elif command == "/reply":
        review = input("Customer review: ")
        print("AI:", reply_to_review(review))
        print(f"    (review was about {estimate_tokens(review)} tokens)")
        usage["reply"] += 1
    else:
        print("Unknown command. Try /summarize, /translate, /reply or bye.")

print("Skills used today:")
for skill, count in usage.items():
    print(f"  {skill}: {count}")