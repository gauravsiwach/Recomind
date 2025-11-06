import styled from 'styled-components';
import { useState, useRef, useEffect } from 'react';
import { FaPaperPlane } from 'react-icons/fa';

const ChatContainer = styled.div`
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(15px);
  border-radius: 20px;
  padding: 10px;
  margin: 10px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  flex-direction: column;
  height: calc(100vh - 185px);
  font-family: 'Poppins', sans-serif;
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  margin-bottom: 20px;
  border-radius: 10px;
  background: rgba(0, 0, 0, 0.1);
  min-height: 0;
`;

const MessageBubble = styled.div`
  max-width: 70%;
  padding: 12px 16px;
  margin-bottom: 10px;
  border-radius: 18px;
  font-size: 0.9rem;
  line-height: 1.4;
  word-wrap: break-word;
  align-self: ${props => props.isUser ? 'flex-end' : 'flex-start'};
  background: ${props => props.isUser
    ? 'linear-gradient(135deg, #533483, #e94560)'
    : 'linear-gradient(135deg, #00d4ff, #16213e)'};
  color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
`;

const MessagesWrapper = styled.div`
  display: flex;
  flex-direction: column;
`;

const TypingIndicator = styled.div`
  display: flex;
  align-items: center;
  padding: 12px 16px;
  margin-bottom: 10px;
  align-self: flex-start;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 18px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.8rem;
`;

const Dots = styled.div`
  display: flex;
  margin-left: 8px;
`;

const Dot = styled.div`
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #00d4ff;
  margin: 0 2px;
  animation: bounce 1.4s infinite ease-in-out both;

  &:nth-child(1) { animation-delay: -0.32s; }
  &:nth-child(2) { animation-delay: -0.16s; }

  @keyframes bounce {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1); }
  }
`;

const InputContainer = styled.div`
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 25px;
  padding: 5px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
`;

const Input = styled.input`
  flex: 1;
  border: none;
  background: transparent;
  padding: 12px 20px;
  font-size: 1rem;
  color: white;
  outline: none;
  font-family: 'Poppins', sans-serif;

  &::placeholder {
    color: rgba(255, 255, 255, 0.6);
  }
`;

const SendButton = styled.button`
  background: linear-gradient(135deg, #00d4ff, #e94560);
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.2s ease;
  color: white;

  &:hover {
    transform: scale(1.1);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

const ChatPanel = ({ sendMessage, isLoading }) => {
  const [messages, setMessages] = useState([
    { text: "Hello! I'm Recomind, your AI memory assistant. I remember your preferences and can give personalized recommendations. What would you like to chat about?", isUser: false }
  ]);
  const [input, setInput] = useState('');
  const [hasUserMessaged, setHasUserMessaged] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (hasUserMessaged) {
      scrollToBottom();
    }
  }, [messages, isLoading, hasUserMessaged]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { text: input, isUser: true };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setHasUserMessaged(true);

    const response = await sendMessage(input);
    const botMessage = { text: response, isUser: false };
    setMessages(prev => [...prev, botMessage]);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  return (
    <ChatContainer>
      <MessagesContainer>
        <MessagesWrapper>
          {messages.map((msg, index) => (
            <MessageBubble key={index} isUser={msg.isUser}>
              {msg.text}
            </MessageBubble>
          ))}
          {isLoading && (
            <TypingIndicator>
              Recomind is typing
              <Dots>
                <Dot />
                <Dot />
                <Dot />
              </Dots>
            </TypingIndicator>
          )}
          <div ref={messagesEndRef} />
        </MessagesWrapper>
      </MessagesContainer>
      <InputContainer>
        <Input
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={isLoading}
        />
        <SendButton onClick={handleSend} disabled={isLoading || !input.trim()}>
          <FaPaperPlane />
        </SendButton>
      </InputContainer>
    </ChatContainer>
  );
};

export default ChatPanel;