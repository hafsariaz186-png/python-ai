"""Task 2.8: First Agent for Sweet Crumbs.

An assistant that reads prices, checks orders and places orders (with owner approval).
"""

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from pydantic import ValidationError

PRICES = {"cupcake": 250, "brownie": 300, "chocolate cake": 1500}
ORDERS = {"A101": "delivered", "A102": "out for delivery", "A103": "being baked"}


# Why a docstring with Args: the AI reads it to learn what the tool does and what to pass in
@tool(parse_docstring=True)
def get_price(item: str) -> str:
    """Get the price of one menu item.

    Args:
        item: Name of the menu item, for example brownie.
    """
    item = item.lower().strip()
    if item in PRICES:
        return f"{item} costs {PRICES[item]} PKR"
    return f"{item} is not on the menu"


@tool(parse_docstring=True)
def order_status(order_id: str) -> str:
    """Check the status of an existing order.

    Args:
        order_id: The order number, for example A102.
    """
    order_id = order_id.upper().strip()
    if order_id in ORDERS:
        return f"Order {order_id} is {ORDERS[order_id]}"
    return f"Order {order_id} was not found"


@tool(parse_docstring=True)
def place_order(item: str, quantity: int, customer: str) -> str:
    """Place a new order for a customer. Asks the owner for approval first.

    Args:
        item: Name of the menu item, for example brownie.
        quantity: How many pieces the customer wants.
        customer: The customer's name.
    """
    item = item.lower().strip()
    if item not in PRICES:
        return f"Cannot place order: {item} is not on the menu"

    total = PRICES[item] * quantity

    # Why input(): the agent must never spend money without the owner saying yes
    answer = input(f"  [approve] {quantity} x {item} for {customer} = {total} PKR. Place it? (yes/no) ")
    if answer.strip().lower() != "yes":
        return "The owner did not approve. The order was NOT placed."

    order_id = f"A{101 + len(ORDERS)}"
    ORDERS[order_id] = "being baked"
    return f"Order {order_id} placed: {quantity} x {item}, total {total} PKR"



# Why a dictionary: the AI gives us a tool name as text, and we look the real function up here
TOOLS = {
    "get_price": get_price,
    "order_status": order_status,
    "place_order": place_order,
}

# Why MAX_STEPS: stops the agent from looping forever if the AI keeps calling tools
MAX_STEPS = 5

# Why temperature 0: choosing a tool should be reliable, not creative
model = ChatOllama(model="llama3.2", temperature=0)

# Why bind_tools: this tells the AI which tools exist, so it can ask to use them
agent_model = model.bind_tools(list(TOOLS.values()))

system_message = SystemMessage(
    content="You are the assistant of Sweet Crumbs bakery. "
            "Use the tools to get prices, check orders and place orders. "
            "Never guess prices or order status. Answer in 2 short lines."
)

print("Sweet Crumbs Agent: ask about prices, orders, or place an order. Type 'bye' to exit.")

# Why a list: this is the agent's memory, it keeps every message across questions
messages = [system_message]

while True:
    user_text = input("You: ").strip()
    if user_text.lower() == "bye":
        break
    if user_text == "":
        continue

    messages.append(HumanMessage(content=user_text))

    # Why for ... else: the loop is limited to MAX_STEPS, and else runs only if it never finished
    for step in range(MAX_STEPS):
        ai_message = agent_model.invoke(messages)
        messages.append(ai_message)

        # No tool requested: this is the final answer
        if not ai_message.tool_calls:
            print("Agent:", ai_message.content)
            break

        for call in ai_message.tool_calls:
            name = call["name"]
            args = call["args"]

            if name not in TOOLS:
                result = f"Unknown tool: {name}"
            else:
                try:
                    result = TOOLS[name].invoke(args)
                except ValidationError:
                    result = "Wrong arguments for this tool."

            print(f"  [tool] {name}({args}) -> {result}")

            # Why tool_call_id: it tells the AI which request this result belongs to
            messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
    else:
        print("Agent: Sorry, I could not finish that. Please ask again.")