from neo4j import GraphDatabase
from service.chat_service import client
import os, json, re

NEO4J_URL = os.getenv('NEO4J_URL')
NEO4J_USER = os.getenv('NEO4J_USERNAME')
NEO4J_PWD = os.getenv('NEO4J_PASSWORD')

drv = None
if NEO4J_URL and NEO4J_USER and NEO4J_PWD:
    drv = GraphDatabase.driver(NEO4J_URL, auth=(NEO4J_USER, NEO4J_PWD))


def fetch_candidates_from_neo4j(user_id, limit=20):
    try:
        # debug logs removed
        if not drv:
            return []

        with drv.session() as s:
            q = """
            MATCH (u:__User__)-[r:thinks|finds|has_time_for]->(c:concept)
            RETURN
              c {
                .name,
                .type,
                dbid: id(c)
              } AS item,
              type(r) AS reason
            LIMIT $limit
            """
            recs = s.run(q, limit=limit).data()
            return recs

    except Exception:
        return []


def generate_recommendations_with_llm(user_id, candidates):
    if not candidates:
        return []

    candidates_text = "\n".join(
        f"- {c['item'].get('name','(no name)')} — reason: {c.get('reason','')}"
        for c in candidates
    )

    prompt = f"""
You are an assistant that converts user interests into friendly recommendations.

User id: {user_id}

User likes:
{candidates_text}

Return a JSON array.
Each item must have: title, reason, explain (short sentence).
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=500
    )

    text = response.choices[0].message.content

    try:
        start = text.find('[')
        end = text.rfind(']')
        return json.loads(text[start:end+1])
    except Exception:
        return [
            {
                "title": c['item'].get('name'),
                "reason": c.get('reason'),
                "explain": f"You seem interested in {c['item'].get('name')}."
            }
            for c in candidates
        ]


def get_recommendations(user_id, limit=6):
    candidates = fetch_candidates_from_neo4j(user_id, limit=limit * 2)
    if not candidates:
        return {"recommendations": []}

    recs = generate_recommendations_with_llm(user_id, candidates[:limit])
    return {"recommendations": recs}
