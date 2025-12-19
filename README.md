# Recomind 🧠

**Recomind** is an advanced AI-powered memory assistant designed to build a deep, long-term understanding of a user's personality, preferences, and lifestyle. By combining real-time conversation tracking with semantic memory extraction, Recomind provides proactive recommendations for work-life balance, hobbies, and personal growth.



---

## 🚀 Key Architectural Features

- **Smart Intent Routing**: A "Gated" logic layer determines if a user's query requires long-term memory retrieval, significantly reducing latency and token costs for general conversation.
- **Hybrid Memory Layer**:
    - **Short-Term (Redis)**: Ultra-fast session persistence for immediate context (last 10-20 messages).
    - **Long-Term (Mem0 + Qdrant)**: Semantic storage of extracted facts and preferences.
    - **Relationship Mapping (Neo4j)**: Graph-based connections between user entities (e.g., connecting "Inception" to a "Preference for Mind-bending movies").
- **Asynchronous Persistence**: Leveraging FastAPI's `BackgroundTasks`, the system ensures the user receives a response in milliseconds. Memory extraction and database writes happen in the background after the reply is sent.
- **Proactive Personality Extraction**: Naturally identifies and saves details like favorite books, work habits, and social energy levels during fluid conversation.

---

## 🏗️ Technical Architecture

| Component | Responsibility | Technology |
| :--- | :--- | :--- |
| **API Layer** | Routing & Background Task Orchestration | FastAPI |
| **Brain** | Intent Classification & Dialogue Generation | OpenAI GPT-4o-mini |
| **Memory Engine** | Fact Extraction & Entity Linking | Mem0 |
| **Session Cache** | Fast retrieval of recent chat turns | Redis |
| **Vector Store** | Semantic search for long-term facts | Qdrant |
| **Graph Store** | Complex relationship & preference mapping | Neo4j |

---

## 📂 Project Structure

```text
Recomind/
├── webapp/                # React + Vite Frontend
│   └── src/               # UI Components & Chat UI
├── webapi/                # FastAPI Backend
│   ├── main.py            # API Entry Point & Background Tasks
│   ├── .env               # Secrets & Configuration
│   └── service/           # Business Logic Layer
│       ├── chat_service.py           # Router & LLM Logic
│       ├── memory_service.py         # Fact Retrieval Logic
│       └── recommendation_service.py # Graph-based Insights
├── Dockerfile             # Containerization for Azure Deployment
└── README.md              # Project Documentation
```

---

## ⚙️ Setup & Installation

### 1. Prerequisites
- **Python 3.10+**
- **Node.js 18+**
- **Redis** (Official Docker image or Managed Instance)
- **OpenAI API Key**

### 2. Backend Configuration
Navigate to the `webapi` directory and create a `.env` file:
```env
OPENAI_API_KEY=your_openai_key
REDIS_URL=redis://default:password@your-redis-ip:6379

QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_key

NEO4J_URL=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
```

### 3. Execution

**Run Backend:**
```bash
cd webapi
pip install -r requirements.txt
uvicorn main:app --reload
```

**Run Frontend:**
```bash
cd webapp
npm install
npm run dev
```

---

## 🌐 API Endpoints

- **`POST /api/chat`**: Processes input through the Intent Router, fetches context from Redis, and returns an AI response while asynchronously updating memory stores via background tasks.
- **`GET /api/memories`**: Retrieves a categorized summary of facts the AI has learned about the specific user from the vector store.
- **`GET /api/recommendations`**: Generates personalized suggestions by querying the Neo4j Knowledge Graph for related user interests.

---

## 🛡️ Security & Deployment
This project is optimized for seamless deployment via **Azure Container Instances (ACI)** or **Azure Container Apps**.
* **Secrets Management**: Use Azure Environment Variables or Key Vault to manage sensitive API keys.
* **Database**: Uses official Redis and Qdrant Docker images for local or cloud-native instances.