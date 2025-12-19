import os, json, time, threading
from openai import OpenAI
from mem0 import Memory
from dotenv import load_dotenv
import redis

load_dotenv() 

# --- CONFIGURATION ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

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
           "api_key": os.getenv("QDRANT_API_KEY"),
            "collection_name": "user_memories"
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

mem_client = Memory.from_config(config)

# --- REDIS SETUP ---
REDIS_URL = os.getenv("REDIS_URL")
try:
    # Set decode_responses=True to handle strings instead of bytes
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()
except:
    redis_client = None

# --- BACKGROUND TASK (NON-BLOCKING) ---
def background_persistence(user_id, user_input, reply):
    """Saves to Redis and Mem0 in a separate thread to keep chat fast."""
    try:
        # 1. Update Redis History
        if redis_client:
            key = f"history:{user_id}"
            u_entry = json.dumps({"role": "user", "content": user_input})
            a_entry = json.dumps({"role": "assistant", "content": reply})
            redis_client.rpush(key, u_entry, a_entry)
            redis_client.ltrim(key, -20, -1) # Keep last 10 turns

        # 2. Update Mem0 (Extracts facts into Vector + Neo4j)
        conversation_text = f"User: {user_input}\nAssistant: {reply}"
        mem_client.add(conversation_text, user_id=user_id)
    except Exception as e:
        print(f"Logging Error: {e}")

# --- INTENT ROUTER ---
def check_if_memory_needed(user_input):

    """Determines if the LLM needs to fetch long-term memories."""
    check_prompt = f"Does the user message require knowing their past history, preferences, or personal details to answer? Answer ONLY 'YES' or 'NO'.\nUser: {user_input}"
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": check_prompt}],
        max_tokens=5
    )
    print("memory check for:", user_input, res.choices[0].message.content)
    return "YES" in res.choices[0].message.content.upper()

# --- MAIN CHAT SERVICE ---
def chat_service(user_input: str, user_id: str) -> str:
    try:
        # 1. Gated Memory Fetch
        memories_text = ""
        if check_if_memory_needed(user_input):
            search_results = mem_client.search(query=user_input, user_id=user_id)
            search_memories = [mem.get('memory', '') for mem in search_results.get("results", [])]
            memories_text = "\n".join(search_memories[:10])
            print(f"Fetched memories for user {user_id}: {memories_text}")

        # 2. Retrieve Short-term History from Redis
        past_messages = []
        if redis_client:
            raw = redis_client.lrange(f"history:{user_id}", -12, -1) # Get last 6 turns
            past_messages = [json.loads(r) for r in raw]

        # 3. Enhanced System Prompt
        SystemPrompt = f"""You are Recomind, an AI memory assistant. You are friendly and aim to understand the user's personality naturally.
        DO NOT make the user feel like you are interviewing them. Start with basic topics: how was their day, name, hobbies, work, and social style.
        
        GOALS:
        - Help with work-life balance.
        - Remember their favorite movies, books, and food.
        - Give personalized recommendations based on the 'User Memories' provided below.
        
        USER MEMORIES (Use these to personalize your response):
        {memories_text if memories_text else "No specific memories found yet. Continue getting to know the user."}
        
        Example Flow:
        User: Hi
        Assistant: Hello! How was your day today?
        User: It was good.
        Assistant: That's great to hear! By the way, what's your name?
        User: My name is John.
            Assistant: Nice to meet you, John! tell me about you, i am here to help you for wokr life balance and make your life more easy and relax.
            User: Sure, I work as a software developer.
            Assistant: That sounds interesting! so hows your work life balance? do you get time for your hobbies and fun activities?
            User: sometimes yes, sometimes no.
            Assistant: I understand, maintaining a good work-life balance can be challenging. so do you follow the 20-20-20 rule for eye care during work?
            User: No, I have do not remember that.
            Assistant: No worries, I can help you with tips on that later. So what do you like to do in your free time?
            User: I like to watch movies on internet.
            Assistant: Awesome! what is your latest movie that you watched and enjoyed?
            User: I watched Inception recently.
            Assistant: good to hear that!
            ....
            ........
            ........
            ...
                Keep the conversation flowing naturally.
             You have access to the user's memories and conversation history.
            """

        # 4. Generate Response
        messages = [{"role": "system", "content": SystemPrompt}] + past_messages + [{"role": "user", "content": user_input}]
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        reply = response.choices[0].message.content

        # 5. Async Persistence (Non-blocking)
        threading.Thread(target=background_persistence, args=(user_id, user_input, reply)).start()
        return reply
    
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"