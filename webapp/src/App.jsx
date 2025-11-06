import { useState, useEffect } from 'react';
import styled from 'styled-components';
import Header from './components/Header';
import LeftPanel from './components/LeftPanel';
import ChatPanel from './components/ChatPanel';
import { useRecomindApi } from './hooks/useRecomindApi';
import './App.css';

const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0a2e 0%, #16213e 50%, #533483 100%);
  font-family: 'Poppins', sans-serif;
`;

const MainContent = styled.div`
  display: flex;
  height: calc(100vh - 120px); /* Adjust based on header height */
`;

const LeftSection = styled.div`
  flex: 0 0 30%;
  padding: 0;
`;

const RightSection = styled.div`
  flex: 0 0 70%;
  padding: 0;
`;

function App() {
  const [userId, setUserId] = useState('gaurav'); // Make user ID configurable
  const { getUserMemories, sendMessage, getRecommendations, refreshMemories, isLoading } = useRecomindApi(userId);
  const [userMemories, setUserMemories] = useState({ hobbies: [], likes: [], dislikes: [] });
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    const loadData = async () => {
      const memories = await getUserMemories();
      setUserMemories(memories);
      const recs = await getRecommendations();
      setRecommendations(recs);
    };
    loadData();
  }, [userId]); // Reload data when userId changes

  const handleRefreshMemories = async () => {
    const memories = await refreshMemories();
    setUserMemories(memories);
  };

  return (
    <AppContainer>
      <Header 
        userMemories={userMemories} 
        recommendations={recommendations}
        userId={userId}
        onUserIdChange={setUserId}
      />
      <MainContent>
        <LeftSection>
          <LeftPanel userMemories={userMemories} onRefresh={handleRefreshMemories} isLoading={isLoading} />
        </LeftSection>
        <RightSection>
          <ChatPanel sendMessage={sendMessage} isLoading={isLoading} />
        </RightSection>
      </MainContent>
    </AppContainer>
  );
}

export default App;
