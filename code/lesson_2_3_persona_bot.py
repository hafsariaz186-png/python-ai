"""Persona bot: chats with memory, answers only from real business facts,
lets the owner switch personality, and answers prices without calling the AI."""

from langchain.chat_models import init_chat_model

# Why: all real business information lives in one dictionary, so the AI
# can only repeat facts we gave it and never invents prices.
facts = {
    "name": "Sweet Crumbs",
    "city": "Lahore",
    "opening_hours": "9am to 9pm, every day",
    "delivery": "free delivery above 2000 PKR",
    "phone": "0300-1234567",
    "prices": {
        "cupcake": 250,
        "brownie": 300,
        "chocolate cake": 1500,
    },
}

# Why: each persona is just a short style sentence, so switching personality
# means swapping one string instead of rewriting the whole prompt.
personas = {
    "friendly": "warm and cheerful, uses simple words",
    "formal": "polite and professional, uses full sentences",
    "sales": "excited, always suggests one extra item to buy",
}

# Why: settings live in one config dictionary, so changing the model,
# temperature or memory size means editing one place only.
config = {
    "model": "llama3.2",
    "temperature": 0.2,
    "memory_size": 8,
}


def build_system_message(style):
    """Build the system message from the facts and the chosen style."""
    prices = "\n".join(f"- {item}: {price} PKR" for item, price in facts["prices"].items())
    return (
        f"You are the shop assistant of {facts['name']}, a bakery in {facts['city']}.\n"
        f"Opening hours: {facts['opening_hours']}\n"
        f"Delivery: {facts['delivery']}\n"
        f"Phone: {facts['phone']}\n"
        f"Our menu and prices:\n{prices}\n\n"
        f"Rules:\n"
        f"1. Only use the facts above. Never invent prices.\n"
        f"2. Answer the customer's question directly in your first sentence.\n"
        f"3. If an item is not on the menu, say we do not sell it.\n"
        f"4. Style: {style}.\n"
        f"5. Answer in at most 3 short sentences."
    )


llm = init_chat_model(
    config["model"],
    model_provider="ollama",
    temperature=config["temperature"],
)

messages = [{"role": "system", "content": build_system_message(personas["friendly"])}]

print("Bot ready. Commands: /persona friendly|formal|sales, /price <item>, bye")

while True:
    user_text = input("You: ").strip()

    if user_text == "bye":
        print("Bot: Goodbye!")
        break

    if user_text.startswith("/persona"):
        name = user_text.replace("/persona", "").strip().lower()
        # Why: .get() with a default means a wrong persona name falls back to
        # friendly instead of crashing with a KeyError.
        style = personas.get(name, personas["friendly"])
        messages[0]["content"] = build_system_message(style)
        print(f"Bot: Style changed to: {style}")
        continue

    if user_text.startswith("/price"):
        # Why: prices come straight from the dictionary, so this command is
        # instant, free (no tokens) and can never be wrong.
        item = user_text.replace("/price", "").strip().lower()
        if item in facts["prices"]:
            print(f"Bot: {item.title()} costs {facts['prices'][item]} PKR.")
        else:
            print(f"Bot: Sorry, {item} is not on our menu.")
        continue

    messages.append({"role": "user", "content": user_text})
    response = llm.invoke(messages)
    answer = response.text.strip()
    # Why: small local models sometimes start with the word "assistant",
    # so we remove it to keep the answer clean.
    if answer.lower().startswith("assistant"):
        answer = answer[len("assistant"):].strip()
    messages.append({"role": "assistant", "content": answer})

    # Why: we keep the system message plus only the last N messages, where N
    # comes from config, so the cost stops growing in long chats.
    messages = [messages[0]] + messages[1:][-config["memory_size"]:]

    print(f"Bot: {answer}")