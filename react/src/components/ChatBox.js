import React from 'react';
import LoadingDots from './LoadingDots';

const parseText = (text) => {
  const urlRegex = /(https?:\/\/[^\s]+)/g;
  return text.split('\n').map((line, i) => (
    <React.Fragment key={i}>
      {line.split(urlRegex).map((part, index) =>
        urlRegex.test(part) ? (
          <a key={index} href={part} target="_blank" rel="noopener noreferrer">
            {part}
          </a>
        ) : (
          part
        )
      )}
      <br />
    </React.Fragment>
  ));
};

function ChatBox({ messages, loading, chatBoxRef }) {
  const introMessage = {
    from: 'bot',
    text: 'Welcome to the ITSD Chat Bot. This chat bot can search all ITSD resources to find an answer to your question. Feel free to talk in a conversational manner! If you wish to switch from ITS to TLS mode just ask to switch or type TLS MODE.'
  };

  const allMessages = [introMessage, ...messages];

  return (
    <div className="chat-box" ref={chatBoxRef}>
      {allMessages.map((msg, index) => (
        <div key={index} className={`message ${msg.from === 'you' ? 'user' : 'bot'}`}>
          <p>{parseText(msg.text)}</p>
        </div>
      ))}
      {loading && <LoadingDots />}
    </div>
  );
}

export default ChatBox;










