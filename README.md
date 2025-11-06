# Recomind

An AI-powered memory-based chatbot that learns user hobbies, likes, and dislikes to provide personalized recommendations.

## Features

- Interactive chat interface with modern React UI
- Memory persistence using Qdrant vector store and Neo4j graph database
- Personalized recommendations based on user preferences
- FastAPI backend for scalable API endpoints
- OpenAI integration for intelligent responses

## Tech Stack

### Frontend
- React (Vite)
- Styled Components
- Modern responsive design

### Backend
- FastAPI
- OpenAI API
- Mem0 for memory management
- Qdrant for vector storage
- Neo4j for graph database

## Setup

### Prerequisites
- Node.js (for frontend)
- Python 3.8+ (for backend)
- OpenAI API key
- Qdrant instance
- Neo4j instance

### Frontend Setup

1. Navigate to the webapp directory:
   ```bash
   cd webapp
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`

### Backend Setup

1. Navigate to the webapi directory:
   ```bash
   cd webapi
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the `webapi` directory with:
   ```
   OPENAI_API_KEY=your_openai_api_key
   QDRANT_API_KEY=your_qdrant_api_key
   NEO4J_URI=your_neo4j_uri
   NEO4J_USER=your_neo4j_username
   NEO4J_PASSWORD=your_neo4j_password
   ```

5. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

The backend API will be available at `http://localhost:8000`

## API Endpoints

- `POST /chat` - Send a chat message and receive AI response with memory context

## Usage

1. Start both frontend and backend servers
2. Open the frontend in your browser
3. Start chatting! The AI will learn from your conversations and provide personalized recommendations

## Project Structure

```
Recomind/
├── webapp/          # React frontend
├── webapi/          # FastAPI backend
│   ├── service/     # Business logic
│   └── main.py      # API endpoints
├── .gitignore
└── README.md
```</content>
<parameter name="filePath">c:\Gaurav\Learning\Python\AI_Learning\Code\Recomind\README.md