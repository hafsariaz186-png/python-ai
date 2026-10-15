"""AI Prompt Kit for a Local Business.

Asks a small business owner a few questions and prints 3 ready-to-use
AI prompts (marketing, customer service, growth) they can paste into
any AI tool. Made for shop owners who don't know what to type.
"""

business_name = input("Business name: ")
business_type = input("Business type: ")
city = input("City: ")
customers = input("Main customers: ")

# input() always returns text, so int() is needed to use the budget as a number
budget = int(input("Monthly budget (PKR): "))

# A header with separators makes the output easy to scan and look professional
print()
print("=========================================")
print(f"   AI Prompt Kit for {business_name}")
print("=========================================")

# Each prompt names a role, task, audience and tone, because specific prompts get better AI answers
print()
print("[1] Marketing")
print(f"Write a short Instagram post for {business_name}, a {business_type} in {city}.")
print(f"Target {customers}. Friendly tone, 1 call to action.")

print()
print("[2] Customer Service")
print(f"You are the manager of {business_name}. Write a polite reply to a customer")
print("whose order arrived late. Apologise and offer a small discount.")

# The budget is inserted into the prompt so the AI suggests ideas the owner can actually afford
print()
print("[3] Growth")
print(f"Suggest 3 low-cost AI tools a {business_type} in {city} can use")
print(f"to attract {customers} with a budget of {budget} PKR per month.")