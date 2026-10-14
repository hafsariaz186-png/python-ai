"""Business Prompt Builder: asks the user for business details
and creates a ready-to-use AI prompt."""

name = input("Your name: ")
business = input("Business type: ")
problem = input("Biggest problem: ")

# input() always returns text, so int() is needed to turn the budget into a number
budget = int(input("Monthly budget in PKR: "))

print(f"\nWelcome, {name}!")
print("--- Your AI Prompt ---")

# An f-string puts the user's answers directly inside the sentence, so no manual joining is needed
print(f"Suggest 3 AI solutions for a {business} that struggles with {problem}. Budget: {budget} PKR per month.")