from service.chat_service import mem_client, client
import json
import re

def get_user_memories(user_id: str):
    """
    Retrieve and categorize user memories from mem0 using LLM for better categorization
    Returns structured data with hobbies, likes, dislikes, and summary
    """
    try:
        # Get all memories for the user (broad search)
        all_memories_search = mem_client.search(query="*", user_id=user_id)  # Use wildcard to get all memories
        all_memories = [mem.get('memory', '') for mem in all_memories_search.get("results", [])]

        if not all_memories:
            return {
                "hobbies": [],
                "likes": [],
                "dislikes": [],
                "summary": "No memories found."
            }

        # Use LLM to categorize memories
        memories_text = "\n".join(all_memories)

        prompt = f"""
        Categorize the following user memories into three categories: hobbies, likes, dislikes, summary.
        Provide the response as a JSON object with keys: "hobbies", "likes", "dislikes" "summary". Each key should have a list of relevant memories.
        Only include memories that clearly fit each category. If a memory doesn't fit well, omit it.

        Memories:
        {memories_text}

        Response format:
        {{
            "hobbies": ["memory1", "memory2"],
            "likes": ["memory3", "memory4"],
            "dislikes": ["memory5"]
            "summary": "A brief summary of the user's memories."
        }}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=1000,
            temperature=0.3
        )

        content = response.choices[0].message.content

        # Extract JSON from markdown code block if present
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # If no code block, assume the whole content is JSON
            json_str = content.strip()

        categorized = json.loads(json_str)

        # Extract categorized lists
        hobbies = categorized.get("hobbies", [])
        likes = categorized.get("likes", [])
        dislikes = categorized.get("dislikes", [])
        summary = categorized.get("summary", "")

        # Create summary
        # total_memories = len(hobbies) + len(likes) + len(dislikes)
        # summary = f"Total categorized memories: {total_memories}. Hobbies: {len(hobbies)}, Likes: {len(likes)}, Dislikes: {len(dislikes)}."

        return {
            "hobbies": hobbies, 
            "likes": likes,
            "dislikes": dislikes,
            "summary": summary
        }

    except Exception as e:
        return {
            "hobbies": [],
            "likes": [],
            "dislikes": [],
            "summary": f"Error retrieving memories: {str(e)}"
        }