import { useState } from 'react';

// Mock data
const mockMemories = {
  hobbies: ['Reading sci-fi novels', 'Playing guitar', 'Hiking in nature'],
  likes: ['Dark chocolate', 'Jazz music', 'Italian cuisine'],
  dislikes: ['Spicy food', 'Loud noises', 'Crowded places']
};

const mockRecommendations = [
  'Try the new sci-fi book "Project Hail Mary" - you might love the space adventure!',
  'Check out this jazz playlist featuring Miles Davis - perfect for your music taste.',
  'How about trying a new hiking trail in the nearby mountains this weekend?'
];

// API configuration
const API_BASE_URL = 'http://localhost:8000';

// Simulate API delay for mock functions
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

export const useRecomindApi = (userId) => {
  const [isLoading, setIsLoading] = useState(false);

  const getUserMemories = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/memories?user_id=${userId}`);

      if (!response.ok) {
        throw new Error(`API call failed: ${response.status}`);
      }

      const data = await response.json();
      return {
        hobbies: data.hobbies || [],
        likes: data.likes || [],
        dislikes: data.dislikes || []
      };
    } catch (error) {
      console.error('Error fetching memories:', error);
      // Fallback to mock data if API fails
      return mockMemories;
    } finally {
      setIsLoading(false);
    }
  };

  const sendMessage = async (message) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          user_id: userId
        }),
      });

      if (!response.ok) {
        throw new Error(`API call failed: ${response.status}`);
      }

      const data = await response.json();
      return data.reply;
    } catch (error) {
      console.error('Error sending message:', error);
      // Fallback to mock response if API fails
      return "Sorry, I'm having trouble connecting to the server right now. Please try again later.";
    } finally {
      setIsLoading(false);
    }
  };

  const getRecommendations = async () => {
    setIsLoading(true);
    await delay(800);
    setIsLoading(false);
    return mockRecommendations;
  };

  const refreshMemories = async () => {
    // This will trigger a re-fetch of memories
    return await getUserMemories();
  };

  return {
    getUserMemories,
    sendMessage,
    getRecommendations,
    refreshMemories,
    isLoading
  };
};