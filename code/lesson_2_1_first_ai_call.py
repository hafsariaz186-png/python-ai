""" AI Tutor : asks for a topic and a level, explains it with a local  AI model, and reports how many tokens and second the answer cost."""
from langchain.chat_models import init_chat_model
topic = input("Topic: ").strip()
level = input("Level (beginner or expert): ").strip()
# Why: the system message sets the role and length once, so every answer
# stays short and matched to the student's level.
system_message = (
    f"You are a friendly tutor at a tuition centre. "
    f"Explain at a {level} level. "
    f"Answer in at most 3 short sentences."
)
# Why: temperature 0.2 keeps answers focused and consistent, which suits teaching.
llm = init_chat_model("llama3.2", model_provider="ollama", temperature=0.2)

response = llm.invoke([
    {"role": "system", "content": system_message},
    {"role": "user", "content": topic},
])
tokens = response.usage_metadata["total_tokens"]
seconds = response.response_metadata["total_duration"] / 1_000_000_000

print("=" * 40)
print(response.text)
print("=" * 40)
print(f"{tokens} tokens in {seconds:.1f} seconds")
