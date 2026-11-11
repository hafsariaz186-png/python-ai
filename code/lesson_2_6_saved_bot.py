"""Task 2.6: Saved Bot for Sweet Crumbs.

Answers from faq.json, remembers old chats, and never shows a red error to the customer.
"""

import json
from datetime import datetime

import httpx
import ollama

MODEL = "llama3.2"
FAQ_FILE = "faq.json"
HISTORY_FILE = "chat_history.json"
ERROR_LOG = "errors.log"

# Why a function: the same logging code is used in more than one place
def log_error(error: Exception) -> None:
    """Append an error with the time to errors.log."""
    with open(ERROR_LOG, "a", encoding="utf-8") as file:
        file.write(f"{datetime.now()} | {type(error).__name__}: {error}\n")


def save_history(history: list) -> None:
    """Save the chat history to a readable JSON file."""
    # Why ensure_ascii=False: so Urdu text stays readable and is not turned into \u codes
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=2, ensure_ascii=False)

    # --- Load the business facts ---
# Why try/except: a missing file should give a clear message, not a scary traceback
try:
    with open(FAQ_FILE, encoding="utf-8") as file:
        faq = json.load(file)
except FileNotFoundError:
    print(f"Cannot find {FAQ_FILE}. Run the bot from the code folder.")
    raise SystemExit

# Why build from the file: changing faq.json changes the bot's answers, no code change needed
facts = json.dumps(faq, indent=2, ensure_ascii=False)
system_message = {
    "role": "system",
    "content": f"You are the friendly assistant of {faq['business_name']}. "
               f"Answer in 2 short lines using ONLY these facts:\n{facts}",
}

# --- Load old chat history ---
history = []
try:
    with open(HISTORY_FILE, encoding="utf-8") as file:
        history = json.load(file)
    print(f"Loaded {len(history)} old messages.")
except FileNotFoundError:
    pass  # first run, no history yet, that is normal
except json.JSONDecodeError:
    # Why: a damaged file must not crash the bot, we just start fresh
    print("History file was damaged. Starting a fresh chat.")
    history = []

    print(f"{faq['business_name']} Bot: Ask me anything. Commands: /reset, bye")

while True:
    user_text = input("You: ").strip()

    if user_text.lower() == "bye":
        save_history(history)
        print("Bot: Goodbye! Your chat is saved.")
        break
    if user_text.lower() == "/reset":
        history = []
        save_history(history)
        print("Bot: Chat cleared.")
        continue
    if user_text == "":
        continue

    history.append({"role": "user", "content": user_text})

    try:
        response = ollama.chat(model=MODEL, messages=[system_message] + history)
        answer = response["message"]["content"]
        history.append({"role": "assistant", "content": answer})
        print("Bot:", answer)
    except (httpx.ConnectError, ConnectionError) as error:
        # Why remove the question: otherwise history has a question with no answer
        history.pop()
        log_error(error)
        print("Bot: I am offline right now. Please open the Ollama app and try again.")
    except ollama.ResponseError as error:
        history.pop()
        log_error(error)
        print("Bot: Something went wrong with the AI model. Please try again.")

    save_history(history)  # save after every turn