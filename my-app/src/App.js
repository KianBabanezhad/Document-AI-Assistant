
import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');

  const handleSend = async () => {
    if (inputText.trim()) {
      const userMessage = { text: inputText, sender: 'user' };
      setMessages((prev) => [...prev, userMessage]);
      setInputText('');

      const botPlaceholder = { text: '', sender: 'bot', isThinking: false };
      setMessages((prev) => [...prev, botPlaceholder]);

      try {
        const response = await fetch("http://localhost:8000/chat/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question: inputText }),
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
        let fullResponse = "";

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          const chunk = decoder.decode(value, { stream: true });
          fullResponse += chunk;

          setMessages((prev) => {
            const updated = [...prev];
            updated[updated.length - 1] = { ...updated[updated.length - 1], text: fullResponse };
            return updated;
          });
        }
      } catch (error) {
        console.error('Error communicating with the backend:', error);
        updateBotMessage('Oops! Something went wrong.');
      }
    }
  };

  const updateBotMessage = (text) => {
    setMessages((prev) => {
      const lastMessage = prev[prev.length - 1];
      if (lastMessage.sender === 'bot') {
        return [...prev.slice(0, -1), { ...lastMessage, isThinking: false, text }];
      }
      return prev;
    });
  };

  useEffect(() => {
    const messageList = document.querySelector('.message-list');
    if (messageList) {
      messageList.scrollTop = messageList.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="chat-container">
      <div className="chat-title">Document AI Assistant</div>

      <div className="message-list">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            <div className="message-bubble">
              {msg.sender === 'bot' && msg.isThinking && (
                <span className="emoji-loader">🤖 AI is processing...</span>
              )}
              {msg.text}
            </div>
          </div>
        ))}
      </div>

      <div className="input-area">
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Type your message..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}

export default App;
