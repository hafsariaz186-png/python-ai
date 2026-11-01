"""Batch product writer: asks the AI for a one-sentence description of every
product, skips items with no price, and reports the total tokens and seconds."""

from langchain.chat_models import init_chat_model

# Why: one dictionary holds every product and its price, so adding a new
# item later means adding one line here and nothing else.
products = {
    "Chocolate Cake": 1500,
    "Cupcake": 250,
    "Brownie": 300,
    "Donut": 200,
    "Old stock": 0,
}

# Why: the model is created once, before the loop, because building it
# again for every product would waste time.
llm = init_chat_model("llama3.2", model_provider="ollama", temperature=0.2)

# Why: accumulators must start at 0 before the loop, otherwise the totals
# would reset on every product.
results = []
total_tokens = 0
total_seconds = 0

for name, price in products.items():
    # Why: a price of 0 means the item is not for sale, so we skip it with
    # continue and spend no AI call and no tokens on it.
    if price == 0:
        print(f"Skipping {name.lower()} (no price)")
        continue

    response = llm.invoke([
        {
            "role": "system",
            "content": "You are a bakery menu writer. Reply with exactly one "
            "short, appetising sentence and nothing else.",
        },
        {"role": "user", "content": f"Write a description for: {name}"},
    ])

    total_tokens += response.usage_metadata["total_tokens"]
    total_seconds += response.response_metadata["total_duration"] / 1_000_000_000
    results.append({"item": name, "price": price, "text": response.text.strip()})

print("=" * 50)
for number, entry in enumerate(results, start=1):
    print(f"{number}. {entry['item']} ({entry['price']} PKR)")
    print(f"   {entry['text']}")
print("=" * 50)
print(f"{len(results)} descriptions, {total_tokens} tokens, {total_seconds:.1f} seconds")