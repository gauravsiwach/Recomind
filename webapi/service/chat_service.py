import os, json
from openai import OpenAI
from mem0 import Memory
from dotenv import load_dotenv


load_dotenv() 

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
client = OpenAI()

CACHE_SIZE = 10
# In-memory per-user chat history (kept while program runs)
# Structure: { user_id: [ {role: 'user'|'assistant', 'content': '...'}, ... ] }
in_memory_history = {}
HISTORY_MAX_LENGTH = 50  # max messages to keep per user
PAST_TURNS = 6  # number of past turns to include in the prompt

def append_in_memory(user_id, role, content):
    if user_id not in in_memory_history:
        in_memory_history[user_id] = []
    in_memory_history[user_id].append({"role": role, "content": content})
    # trim
    if len(in_memory_history[user_id]) > HISTORY_MAX_LENGTH:
        in_memory_history[user_id] = in_memory_history[user_id][-HISTORY_MAX_LENGTH:]


def chat_service(user_input: str, user_id: str) -> str:
    try:
        # 1️⃣ Retrieve relevant memories from mem0/vector DB for context
        search_results = mem_client.search(query=user_input, user_id=user_id)
        search_memories = [mem.get('memory', '') for mem in search_results.get("results", [])]
        # Keep only up to CACHE_SIZE most relevant memories
        memories_text = "\n".join(search_memories[:CACHE_SIZE])
 
        SystemPrompt = """You are Recomind, an AI memory assistant you have to act as friendly and try to now user personlity vai asking basic question.
           and user should not feel that you are trying to find out his personality. start with basic questions like how was your day, what are your name, hobbies etc. 
           what he do for living etc. how its working style how much he like to socialize etc.
           what he are his favorite movies, books, music etc.
           what he do for fun and relaxation.
           what his favorite food and drink.
    
           Example:
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
              Keep the conversation going naturally.

           
           You have access to the user's memories and conversation history.
        
        """

        content = f"""{SystemPrompt} \n
         User memories:\n{memories_text} \n
        """


        
        # 2️⃣ Create context-aware prompt
        # Include in-memory recent conversation history (if any) before the current user message
        past_messages = []
        try:
            hist = in_memory_history.get(user_id, [])
            # hist is a list of {role, content}; include only the last PAST_TURNS*2 entries
            if hist:
                past_messages = hist[-(PAST_TURNS * 2):] 
        except Exception:
            past_messages = []

        messages = [{"role": "system", "content": content}] + past_messages + [{"role": "user", "content": user_input}]
        # debug logs removed

        # 3️⃣ Get LLM response
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        
        reply = response.choices[0].message.content
        # Append to in-memory history (user + assistant)
        try:
            append_in_memory(user_id, 'user', user_input)
            append_in_memory(user_id, 'assistant', reply)
        except Exception:
            pass
        
        # 4️⃣ Store the conversation in memory
        conversation_text = f"User: {user_input}\nAssistant: {reply}"
        mem_client.add(conversation_text, user_id=user_id)
        
        
        return reply
    
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"