"""Glow Beauty Salon Front Desk: answers common questions, gives price quotes
and prepares AI-ready prompts for everything else."""

# constants in UPPER_CASE because these values never change while the program runs
BOT_NAME = "Glow Desk"
HOME_SERVICE_FEE = 500
FREE_SERVICE_LIMIT = 5000
CLOUD_PRICE_PER_1K = 0.2

print("=" * 50)
print(f"   {BOT_NAME}: rules, quotes and AI-ready prompts")
print("=" * 50)
print("Ask anything, type /quote for a price, or bye to exit.")

# ask the name once, before the loop, so we do not ask it again in every message
customer_name = input(f"{BOT_NAME}: What is your name? ").strip().title()

# counters to build the session report at the end
message_count = 0
rule_count = 0
unanswered_count = 0
quote_count = 0
quoted_value = 0
total_ai_cost = 0

# while True keeps the chat going until the customer types bye
while True:
    # strip() and lower() so " BYE " and "bye" are treated the same
    message = input(f"{customer_name}: ").strip().lower()

    # empty input asks again, and it is not counted as a message
    if message == "":
        print(f"{BOT_NAME}: Please type something.")
        continue

    message_count += 1

    # complaint rule is first so an unhappy customer always reaches a human
    if "refund" in message or "complaint" in message or "late" in message:
        rule_count += 1
        print(f"{BOT_NAME}: Sorry about that. A manager will call you within 1 hour.")
    elif message == "bye":
        print(f"{BOT_NAME}: Goodbye, {customer_name}!")
        break
    elif message == "/quote":
        item = input(f"{BOT_NAME}: Which item? ").strip().lower()
        quantity = int(input(f"{BOT_NAME}: How many? "))

        # price 0 means the item is not on our menu
        if item == "haircut":
            price = 800
        elif item == "facial":
            price = 2000
        elif item == "bridal makeup":
            price = 15000
        else:
            price = 0

        if price == 0:
            print(f"{BOT_NAME}: Sorry, {item} is not on our menu.")
        else:
            subtotal = price * quantity

            # discount first, because the free-service limit is checked on the discounted amount
            if quantity >= 5:
                discount = subtotal // 10
            else:
                discount = 0
            after_discount = subtotal - discount

            if after_discount >= FREE_SERVICE_LIMIT:
                service_fee = 0
            else:
                service_fee = HOME_SERVICE_FEE

            total = after_discount + service_fee
            quote_count += 1
            quoted_value += total
            rule_count += 1

            print(f"{BOT_NAME}: {quantity} x {item} = {subtotal:,} PKR")
            print(f"     Discount: -{discount:,} PKR | Home service: {service_fee:,} PKR")
            print(f"     Total: {total:,} PKR")
    elif message == "hi" or message.startswith("hello"):
        # == and startswith() because "hi" hides inside words like "which"
        rule_count += 1
        print(f"{BOT_NAME}: Hello! How can I help?")
    elif "timing" in message or "hours" in message or "open" in message or "close" in message:
        rule_count += 1
        print(f"{BOT_NAME}: We are open 11 am to 8 pm, every day.")
    elif "where" in message or "location" in message:
        rule_count += 1
        print(f"{BOT_NAME}: We are in Gulberg, Lahore.")
    elif "appointment" in message or "book" in message:
        rule_count += 1
        print(f"{BOT_NAME}: Call 0300-1234567 to book your appointment.")
    else:
        # smart fallback: no rule matched, so prepare a clean, cost-checked AI prompt
        unanswered_count += 1

        # [:150] keeps the prompt short so the AI cost stays small
        question = message.capitalize()[:150]
        tokens = round(len(question) / 4)

        # private details must stay on the local model, which is free and keeps data on this computer
        if "phone" in message or "cnic" in message or "my address" in message:
            model = "llama3.2 (local, private)"
            cost = 0
        else:
            model = "small cloud model (cheap)"
            cost = (tokens / 1000) * CLOUD_PRICE_PER_1K

        total_ai_cost += cost

        prompt = f"""You are the assistant of Glow Beauty Salon.
Answer {customer_name} in 2 short lines. Question: {question}"""

        print(f"{BOT_NAME}: Good question! Routed to: {model} (~{tokens} tokens)")
        print(f"     Prompt: {prompt}")

# session report is after the loop so it always prints when the chat ends
print("=" * 50)
print("Session report")
print(f"Messages: {message_count} | Answered by rules: {rule_count} | Unanswered: {unanswered_count}")
print(f"Quotes: {quote_count} | Quoted value: {quoted_value:,} PKR")
print(f"Estimated AI cost for unanswered questions: {total_ai_cost:.4f} PKR")
print("=" * 50)