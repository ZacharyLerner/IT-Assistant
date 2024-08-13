import React, { useState, useEffect, useRef } from 'react';
import ChatBox from './components/ChatBox';
import ChatInput from './components/ChatInput';
import './styles.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatBoxRef = useRef(null);

  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [messages, loading]);

  const handleSendMessage = async (message) => {
    setMessages([...messages, { from: "you", text: message }]);
    setLoading(true);
    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
      });
      const data = await response.json();
      setMessages((prevMessages) => [...prevMessages, {text: data.response }]);
    } catch (error) {
      console.error("Error fetching response:", error);
      setMessages((prevMessages) => [...prevMessages, {text: "Error fetching response." }]);
    }
    setLoading(false);
  };

  return (
    <div className="app-wrapper">
      <div className="app-container">
        <ChatBox messages={messages} loading={loading} chatBoxRef={chatBoxRef} />
        <ChatInput onSendMessage={handleSendMessage} />
      </div>
      <footer className="footer">
        Created by Zachary Lerner
      </footer>
    </div>
  );
}

export default App;






