"""Chat tutor with memory: remembers the conversation, supports /reset and
/count, and keeps only the last 8 messages so the cost does not grow forever."""

from langchain.chat_models import init_chat_model

# Why: the system message sets the tutor's role and answer length once,
# and it stays at messages[0] for the whole conversation.
SYSTEM_MESSAGE = {
    "role": "system",
    "content": "You are a friendly tutor. Answer in at most 3 short sentences.",
}

llm = init_chat_model("llama3.2", model_provider="ollama", temperature=0.2)

messages = [SYSTEM_MESSAGE]
print("Tutor: Ask me anything. Commands: /reset, /count, bye")

while True:
    user_text = input("You: ").strip()

    if user_text == "bye":
        print("Tutor: Goodbye!")
        break

    if user_text == "/reset":
        # Why: we rebuild the list with only the system message, so the tutor
        # forgets the chat but keeps its role.
        messages = [SYSTEM_MESSAGE]
        print("Tutor: Memory cleared.")
        continue

    if user_text == "/count":
        print(f"Tutor: {len(messages)} messages in memory.")
        continue

    messages.append({"role": "user", "content": user_text})
    response = llm.invoke(messages)
    messages.append({"role": "assistant", "content": response.text})

    # Why: we keep the system message plus only the last 8 messages, so the
    # tokens sent (and the cost) stop growing as the chat gets longer.
    messages = [messages[0]] + messages[1:][-8:]

    print(f"Tutor: {response.text}")
    print(f"       (tokens sent: {response.usage_metadata['input_tokens']})")
    