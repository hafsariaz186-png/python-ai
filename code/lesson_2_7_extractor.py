"""Task 2.7: Order Extractor for Sweet Crumbs.

Turns messy WhatsApp orders into checked data with correct totals.
"""

import json

import ollama

MODEL = "llama3.2"

# Why a dictionary: prices live in Python, so totals never depend on the AI's maths
PRICES = {"cupcake": 250, "brownie": 300, "chocolate cake": 1500}

MESSAGES = [
    "Hi, I want 3 cupcakes. Sara, DHA Phase 5",
    "Salam! 2 cupcakes aur 1 chocolate cake chahiye. Ali, house 12 Gulberg",
    "1 pizza and 2 brownies, Bilal, Model Town",
    "hi do you deliver to Johar Town?",
    "bhai 4 brownies bhej do, Usman, Johar Town",
]

# Why a schema: it forces the AI to reply in exactly this JSON shape
SCHEMA = {
    "type": "object",
    "properties": {
        "is_order": {"type": "boolean"},
        "customer": {"type": "string"},
        "address": {"type": "string"},
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "quantity": {"type": "integer"},
                },
                "required": ["name", "quantity"],
            },
        },
    },
    "required": ["is_order", "customer", "address", "items"],
}
def extract_order(message: str) -> dict:
    """Ask the AI to turn one message into order data. Returns a dictionary."""
    # Why format=SCHEMA and temperature 0: same strict shape and the least guessing
    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Extract order details from the customer message. "
                           "If it is not an order, set is_order to false and leave the rest empty. "
                           "Use only what is written in the message.",
            },
            {"role": "user", "content": message},
        ],
        format=SCHEMA,
        options={"temperature": 0},
    )
    # Why try/except: even with a schema, the reply can occasionally be broken JSON
    try:
        return json.loads(response["message"]["content"])
    except json.JSONDecodeError:
        return {}

def check_order(message: str, data: dict) -> tuple:
    """Check the AI's data against the menu and the message. Returns (lines, total, checks)."""
    lines = []   # each item with its price
    total = 0
    checks = []  # warnings

    # Why .get(): a missing key gives a default instead of crashing the program
    customer = data.get("customer", "")
    items = data.get("items", [])

    # Why check the name: the AI sometimes invents a name that is not in the message
    if customer and customer.lower() not in message.lower():
        checks.append(f"customer name '{customer}' is not in the message")

    for item in items:
        name = item.get("name", "").lower().strip()
        quantity = item.get("quantity", 0)

        # Why strip a trailing 's': "cupcakes" should match "cupcake" on the menu
        if name not in PRICES and name.endswith("s"):
            name = name[:-1]

        # Why never price off-menu items: we cannot sell what is not on the menu
        if name not in PRICES:
            checks.append(f"'{name}' is not on the menu")
            continue

        line_total = quantity * PRICES[name]
        lines.append((name, quantity, line_total))
        total += line_total

    return lines, total, checks

orders = []        # valid orders to save
total_value = 0
total_checks = 0

for message in MESSAGES:
    print(f"\nMessage: {message}")
    data = extract_order(message)

    # Why .get(): the AI reply may be empty or missing keys
    if not data.get("is_order", False):
        print("  Not an order: needs a human reply.")
        continue

    lines, total, checks = check_order(message, data)

    for name, quantity, line_total in lines:
        print(f"  {quantity} x {name} = {line_total} PKR")
    print(f"  Customer: {data.get('customer', '')}, Address: {data.get('address', '')}")
    print(f"  Total: {total} PKR")

    for warning in checks:
        print(f"  CHECK: {warning}")

    total_checks += len(checks)

    # Why skip empty orders: if nothing on the menu was found, there is nothing to save
    if lines:
        orders.append({
            "customer": data.get("customer", ""),
            "address": data.get("address", ""),
            "items": [{"name": n, "quantity": q, "line_total": t} for n, q, t in lines],
            "total": total,
        })
        total_value += total

# Why ensure_ascii=False and indent=2: readable file, Urdu names stay readable
with open("orders.json", "w", encoding="utf-8") as file:
    json.dump(orders, file, indent=2, ensure_ascii=False)

print("\n" + "=" * 50)
print(f"Orders found: {len(orders)} | Total value: {total_value:,} PKR | Checks: {total_checks}")
print(f"Saved {len(orders)} orders to orders.json")