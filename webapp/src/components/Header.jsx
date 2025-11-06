import styled from 'styled-components';

const HeaderContainer = styled.header`
  background: linear-gradient(135deg, #0a0a2e 0%, #16213e 25%, #533483 50%, #e94560 75%, #00d4ff 100%);
  color: white;
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  font-family: 'Poppins', sans-serif;
`;

const LogoSection = styled.div`
  display: flex;
  flex-direction: column;
`;

const Logo = styled.h1`
  font-size: 2.5rem;
  margin: 0;
  background: linear-gradient(45deg, #00d4ff, #e94560);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
`;

const Tagline = styled.p`
  font-size: 1rem;
  margin: 5px 0 0 0;
  opacity: 0.9;
`;

const UserSection = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-end;
`;

const UserName = styled.h2`
  font-size: 1rem;
  margin: 0;
`;

const PreferencesSummary = styled.p`
  font-size: 0.7rem;
  margin: 3px 0;
  opacity: 0.8;
`;

const Recommendations = styled.div`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 10px;
  padding: 10px;
  margin-top: 0px;
  border: 1px solid rgba(255, 255, 255, 0.2);
`;

const RecTitle = styled.h3`
  font-size: 1rem;
  margin: 0 0 5px 0;
`;

const RecItem = styled.p`
  font-size: 0.8rem;
  margin: 3px 0;
  opacity: 0.9;
`;

const Header = ({ userMemories, recommendations }) => {
  const summary = `You enjoy ${userMemories.likes.join(', ')} and dislike ${userMemories.dislikes.join(', ')}.`;

  return (
    <HeaderContainer>
      <LogoSection>
        <Logo>Recomind 🧠</Logo>
        <Tagline>Your Smart Memory & Recommendation Assistant</Tagline>
      </LogoSection>
      <UserSection>
        <UserName>Welcome, Alex!</UserName>
        <PreferencesSummary>{summary}</PreferencesSummary>
        <Recommendations>
          <RecTitle>Recommended for you:</RecTitle>
          {recommendations.slice(0, 2).map((rec, index) => (
            <RecItem key={index}>• {rec}</RecItem>
          ))}
        </Recommendations>
      </UserSection>
    </HeaderContainer>
  );
};

export default Header;