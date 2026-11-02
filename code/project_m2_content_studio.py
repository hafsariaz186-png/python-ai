"""
AI Content Studio for Sweet Crumbs bakery (Lahore).
Writes menu descriptions and social posts, answers prices from data,
and chats with customers using only real facts.
"""
from langchain.chat_models import init_chat_model

config = {
    "model": "llama3.2",
    "max_messages": 6,
}

facts = {
    "name": "Sweet Crumbs",
    "city": "Lahore",
    "hours": "9 am to 10 pm",
    "delivery": "200 PKR, free for orders from 3,000 PKR",
    "specialty": "fresh baked every morning",
    "prices": {
        "chocolate cake": 1500,
        "cupcake": 250,
        "brownie": 300,
        "mango tart": 0,  # 0 means coming soon
    },
}

tones = {
    "fun": "playful and full of energy, short sentences",
    "premium": "elegant and calm, focused on quality",
    "urgent": "exciting, limited-time feeling, a clear call to action",
}

# Why: two models created once. Low temperature keeps chat answers accurate,
# high temperature gives varied marketing text.
precise = init_chat_model(config["model"], model_provider="ollama", temperature=0.2)
creative = init_chat_model(config["model"], model_provider="ollama", temperature=0.8)

system_text = f"""You are the assistant for {facts['name']} in {facts['city']}.
Only use these facts. If the answer is not in them, say you do not know.
Opening hours: {facts['hours']}
Delivery: {facts['delivery']}
Prices in PKR (0 means coming soon): {facts['prices']}"""

messages = [{"role": "system", "content": system_text}]

# Why: these count everything the AI does, for the session report at the end
total_tokens = 0
total_seconds = 0
chat_count = 0
menu_count = 0
post_count = 0
price_count = 0

print("=" * 50)
print(f"   {facts['name']} AI Content Studio")
print("=" * 50)
print("Commands: /menu, /post fun|premium|urgent, /price <item>, /reset, bye")

while True:
    user_input = input("You: ").strip()

    # Why: an empty line should just ask again, not call anything
    if user_input == "":
        continue

    # lower() so /PRICE, /Price and /price all work
    lowered = user_input.lower()

    if lowered == "bye":
        print("Studio: Goodbye!")
        break

    elif lowered == "/reset":
        # Why: keep the system message, drop only the conversation
        messages = [messages[0]]
        print("Studio: Chat cleared.")

    elif lowered == "/menu":
        menu_items = []
        for item_name, item_price in facts["prices"].items():
            # Why: skipping before the AI call means coming-soon items cost nothing
            if item_price == 0:
                print(f"Studio: Skipping {item_name} (coming soon)")
                continue

            menu_messages = [
                {"role": "system", "content": f"You write menu text for {facts['name']}, a bakery in {facts['city']} where everything is {facts['specialty']}. Write exactly ONE sentence of at most 15 words. Do not mention prices. Do not invent ingredients, toppings or decorations."},
                {"role": "user", "content": f"Describe this item: {item_name}"},
            ]
            response = creative.invoke(menu_messages)

            # accumulators: every call adds its tokens and seconds
            total_tokens += response.usage_metadata["total_tokens"]
            total_seconds += response.response_metadata["total_duration"] / 1_000_000_000
            menu_count += 1

            menu_items.append({
                "name": item_name,
                "price": item_price,
                "description": response.text.strip(),
            })

        print("-" * 50)
        for number, entry in enumerate(menu_items, start=1):
            print(f"{number}. {entry['name'].title()} ({entry['price']:,} PKR)")
            print(f"   {entry['description']}")
        print("-" * 50)

    elif lowered.startswith("/price"):
        item = lowered.replace("/price", "").strip()
        price = facts["prices"].get(item)
        if price is None:
            print("Studio: Sorry, that is not on our menu.")
        elif price == 0:
            print(f"Studio: {item.title()} is coming soon.")
        else:
            print(f"Studio: {item.title()} costs {price:,} PKR.")
        # Why: every /price answer counts, not only the ones with a real price
        price_count += 1

    elif lowered.startswith("/post"):
        tone_name = lowered.replace("/post", "").strip()
        # Why: .get() with a default means a wrong tone like "pirate" still works
        tone_text = tones.get(tone_name, "friendly and simple")

        post_messages = [
            {"role": "system", "content": f"You write short Instagram posts for {facts['name']} in {facts['city']}. Only use these facts: opening hours {facts['hours']}, specialty {facts['specialty']}, prices in PKR {facts['prices']}. Never invent prices or products. Keep the post under 4 lines."},
            {"role": "user", "content": f"Write one post in this tone: {tone_text}"},
        ]

        print(f"Studio ({tone_text}):")
        # Why: streaming prints each piece as it arrives, so the owner sees text immediately
        full_chunk = None
        for chunk in creative.stream(post_messages):
            print(chunk.text, end="", flush=True)
            # Why: adding chunks together also adds their usage numbers,
            # because the last chunk alone may have none
            if full_chunk is None:
                full_chunk = chunk
            else:
                full_chunk = full_chunk + chunk
        print()

        # .get() with a default so a missing number never crashes the studio
        usage = full_chunk.usage_metadata or {}
        meta = full_chunk.response_metadata or {}
        total_tokens += usage.get("total_tokens", 0)
        total_seconds += meta.get("total_duration", 0) / 1_000_000_000
        post_count += 1

    else:
        # Why: the user message is added first so the AI sees the whole conversation
        messages.append({"role": "user", "content": user_input})

        # Why: keep the system message (position 0) plus only the last few messages,
        # so memory stays small and the system rules are never lost
        messages = [messages[0]] + messages[1:][-config["max_messages"]:]

        response = precise.invoke(messages)
        messages.append({"role": "assistant", "content": response.text})

        tokens = response.usage_metadata["total_tokens"]
        seconds = response.response_metadata["total_duration"] / 1_000_000_000
        total_tokens += tokens
        total_seconds += seconds
        chat_count += 1

        print(f"Studio: {response.text}")
        print(f"        (memory: {len(messages)} messages, {response.usage_metadata['input_tokens']} tokens sent)")

print("=" * 50)
print("Session report")
print(f"Chat answers: {chat_count} | Menu descriptions: {menu_count} | Posts: {post_count} | Price answers: {price_count}")
print(f"AI usage: {total_tokens:,} tokens in {total_seconds:.1f} seconds")
print("=" * 50)