import React from 'react';

function Message({ from, text }) {
  return (
    <div className={`message ${from}`}>
      <p>{text}</p>
    </div>
  );
}

export default Message;
