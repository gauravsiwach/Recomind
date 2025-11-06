import styled from 'styled-components';
import { FaHeart, FaTimes, FaStar, FaBrain, FaSync } from 'react-icons/fa';

const PanelContainer = styled.div`
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(15px);
  border-radius: 20px;
  padding: 10px;
  margin: 10px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  font-family: 'Poppins', sans-serif;
  height: calc(100vh - 160px);
  overflow-y: auto;
`;

const PanelHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
`;

const RefreshButton = styled.button`
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 10px;
  padding: 8px 12px;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.8rem;
  transition: all 0.2s ease;

  &:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: scale(1.05);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

const Card = styled.div`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: transform 0.2s ease;

  &:hover {
    transform: translateY(-2px);
  }
`;

const CardHeader = styled.div`
  display: flex;
  align-items: center;
  margin-bottom: 10px;
`;

const Icon = styled.div`
  font-size: 1.5rem;
  margin-right: 10px;
  color: ${props => props.color};
`;

const CardTitle = styled.h3`
  font-size: 1.2rem;
  margin: 0;
  color: white;
`;

const ItemList = styled.ul`
  list-style: none;
  padding: 0;
  margin: 0;
`;

const Item = styled.li`
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 5px;
  padding-left: 25px;
  position: relative;

  &::before {
    content: '•';
    color: ${props => props.color};
    font-weight: bold;
    position: absolute;
    left: 0;
  }
`;

const MemorySummary = styled.div`
  background: linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(233, 69, 96, 0.2));
  border-radius: 15px;
  padding: 15px;
  margin-top: 20px;
  border: 1px solid rgba(255, 255, 255, 0.3);
`;

const SummaryTitle = styled.h3`
  font-size: 1.2rem;
  margin: 0 0 10px 0;
  color: white;
  display: flex;
  align-items: center;
`;

const SummaryText = styled.p`
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  line-height: 1.4;
`;

const LeftPanel = ({ userMemories, onRefresh, isLoading }) => {
  return (
    <PanelContainer>
      <PanelHeader>
        <h2 style={{ color: 'white', margin: 0, fontSize: '1.3rem' }}>User Memories</h2>
        <RefreshButton onClick={onRefresh} disabled={isLoading}>
          <FaSync style={{ fontSize: '0.8rem' }} />
          Refresh
        </RefreshButton>
      </PanelHeader>
      <Card>
        <CardHeader>
          <Icon color="#00d4ff"><FaStar /></Icon>
          <CardTitle>Hobbies</CardTitle>
        </CardHeader>
        <ItemList>
          {userMemories.hobbies.map((hobby, index) => (
            <Item key={index} color="#00d4ff">{hobby}</Item>
          ))}
        </ItemList>
      </Card>

      <Card>
        <CardHeader>
          <Icon color="#e94560"><FaHeart /></Icon>
          <CardTitle>Likes</CardTitle>
        </CardHeader>
        <ItemList>
          {userMemories.likes.map((like, index) => (
            <Item key={index} color="#e94560">{like}</Item>
          ))}
        </ItemList>
      </Card>

      <Card>
        <CardHeader>
          <Icon color="#533483"><FaTimes /></Icon>
          <CardTitle>Dislikes</CardTitle>
        </CardHeader>
        <ItemList>
          {userMemories.dislikes.map((dislike, index) => (
            <Item key={index} color="#533483">{dislike}</Item>
          ))}
        </ItemList>
      </Card>

      <MemorySummary>
        <SummaryTitle>
          <FaBrain style={{ marginRight: '10px' }} />
          Memory Summary
        </SummaryTitle>
        <SummaryText>
          {userMemories.summary || "No memory summary available yet. Start chatting to build your memory profile!"}
        </SummaryText>
      </MemorySummary>
    </PanelContainer>
  );
};

export default LeftPanel;