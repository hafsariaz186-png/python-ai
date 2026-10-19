"""AI Model Profile Card: shows a model's details and estimates the cost of one chat."""

model_name = "llama3.2"        # str
context_window = 128000        # int
price_per_1k = 0.5             # float (PKR, example price)
runs_locally = True            # bool

print("--- AI Model Profile Card ---")
print(f"Model: {model_name} {type(model_name)}")
print(f"Context Window: {context_window} tokens {type(context_window)}")
print(f"Price per 1k tokens: {price_per_1k} PKR {type(price_per_1k)}")
print(f"Runs Locally: {runs_locally} {type(runs_locally)}")
# int() because input() always returns text, and we need a number for maths
tokens_per_chat = int(input("Tokens per chat: "))
# round to 2 decimals so the cost looks clean, like real money
estimated_cost = round((tokens_per_chat / 1000) * price_per_1k, 2)
print(f"Estimated cost: {estimated_cost} PKR")