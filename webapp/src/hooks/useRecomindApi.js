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

// Simulate API delay
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

export const useRecomindApi = () => {
  const [isLoading, setIsLoading] = useState(false);

  const getUserMemories = async () => {
    setIsLoading(true);
    await delay(500); // Simulate API call
    setIsLoading(false);
    return mockMemories;
  };

  const sendMessage = async (message) => {
    setIsLoading(true);
    await delay(1000); // Simulate thinking time
    setIsLoading(false);
    // Simple mock response based on message
    if (message.toLowerCase().includes('hobby')) {
      return "Based on your hobbies, I recommend exploring more sci-fi literature or learning advanced guitar techniques!";
    } else if (message.toLowerCase().includes('food')) {
      return "Since you like Italian cuisine but dislike spicy food, how about trying a creamy carbonara pasta?";
    } else {
      return "That's interesting! I'll remember that for future recommendations. What else would you like to chat about?";
    }
  };

  const getRecommendations = async () => {
    setIsLoading(true);
    await delay(800);
    setIsLoading(false);
    return mockRecommendations;
  };

  return {
    getUserMemories,
    sendMessage,
    getRecommendations,
    isLoading
  };
};