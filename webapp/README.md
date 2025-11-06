# Recomind 🧠

An AI-powered memory-based chatbot that learns user hobbies, likes, and dislikes to provide personalized recommendations.

## Features

- **Smart Memory**: Remembers user preferences across conversations
- **Personalized Recommendations**: AI-driven suggestions based on user data
- **Modern UI**: Glassmorphism design with 8K-inspired gradients
- **Responsive Layout**: Optimized for desktop and mobile
- **Real-time Chat**: Smooth chat interface with typing indicators

## Tech Stack

- **Frontend**: React 18 + Vite
- **Styling**: styled-components
- **Icons**: react-icons
- **Fonts**: Poppins (Google Fonts)

## Getting Started

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Start development server**:
   ```bash
   npm run dev
   ```

3. **Open** [http://localhost:5173](http://localhost:5173) in your browser

## Project Structure

```
webapp/
├── src/
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── LeftPanel.jsx
│   │   └── ChatPanel.jsx
│   ├── hooks/
│   │   └── useRecomindApi.js
│   ├── App.jsx
│   ├── index.css
│   └── main.jsx
├── public/
└── package.json
```

## Components

- **Header**: Displays user info, preferences summary, and recommendations
- **LeftPanel**: Shows hobbies, likes, dislikes, and memory summary in glassmorphic cards
- **ChatPanel**: Full chat interface with message bubbles and input
- **useRecomindApi**: Mock API hook for user memories and chat responses

## Design

- 8K color palette: Deep navy → Neon purple → Pink → Cyan gradients
- Glassmorphism effects with backdrop blur
- Smooth animations and hover effects
- Responsive flex layout (30% sidebar, 70% chat)

## Future Enhancements

- Real API integration
- User authentication
- Persistent memory storage
- Advanced AI recommendations
- Voice chat support
