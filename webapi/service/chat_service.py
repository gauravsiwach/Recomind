import os, json
from openai import OpenAI
from mem0 import Memory
from dotenv import load_dotenv


load_dotenv()
# print('QDRANT_URL:', os.getenv('QDRANT_URL'))
# print('QDRANT_API_KEY:', os.getenv('QDRANT_API_KEY'))

# print('Config vector_store:', config['vector_store'])

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

config = {
    "version": "1.0",
    "embedder": {
        "type": "openai",
        "config": {
            "model": "text-embedding-3-small",
            "api_key": OPENAI_API_KEY
        }
    },
    "llm": {
        "provider": "openai",
        "config":{
            "model": "gpt-4o-mini",
            "api_key": OPENAI_API_KEY
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "url": os.getenv("QDRANT_URL"),
            "api_key": os.getenv("QDRANT_API_KEY")
        }
    },
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": os.getenv("NEO4J_URL"),
            "username": os.getenv("NEO4J_USERNAME"),
            "password": os.getenv("NEO4J_PASSWORD")
        }
    }
}
# print('Config vector_store:', config['vector_store'])

mem_client = Memory.from_config(config)
client = OpenAI()
conversation_history = []

def chat_service(user_input: str, user_id: str) -> str:
    # 1️⃣ Search memory from Mem0
    relevent_memory = mem_client.search(query=user_input, user_id=user_id)
    memories = [
        f"ID: {mem.get('id')}, Memory: {mem.get('memory')}"
        for mem in relevent_memory.get("results", [])
    ]

    # 2️⃣ Keep only last 5 messages for context
    recent_context = conversation_history[-5:]

    # 3️⃣ System Prompt
    SYSTEM_PROMPT = f"""
        You are a memory aware assistant which responds to user with context.
        You are given relevant memories from the past interactions about the user.
        Memory of user:
    {json.dumps(memories)}
    """

    # 4️⃣ Build final messages for LLM
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(recent_context)
    messages.append({"role": "user", "content": user_input})

    # 5️⃣ Get LLM response
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )
    reply = response.choices[0].message.content

    # 6️⃣ Save to conversation history
    conversation_history.append({"role": "user", "content": user_input})
    conversation_history.append({"role": "assistant", "content": reply})

    # 7️⃣ Update long-term memory
    mem_client.add([
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": reply}
    ], user_id=user_id)

    return reply
