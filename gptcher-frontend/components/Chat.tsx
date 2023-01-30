import React, { useState, useEffect } from 'react';
import config from '../config';


const Chat: React.FC = ({ session, supabase }: any) => {
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState('');
  
  useEffect(() => {
    async function fetchChatHistory() {
        console.log(session.access_token)
      const response = await fetch(`${config.backendUrl}/chat`, {
        headers: {
            Authorization: `Bearer ${session.access_token}`,
            'Content-Type': 'application/json'
        }});
      const data = await response.json();
      setMessages(data);
    }
    fetchChatHistory();
  }, []);

  const handleSendMessage = async () => {
    const response =await fetch(`${config.backendUrl}/chat`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${session.access_token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text }),
    });
    const data = await response.json();
    setMessages(data);
    setText('');
  };

  useEffect(() => {
    const handleNewMessage = (newMessage: any) => {
      setMessages([...messages, newMessage]);
    };
    // Add event listener for new messages here
  }, [messages]);

  return (
    <div>
      {messages.map((message) => (
        <p key={message.id}>{message.text}</p>
      ))}
      <input value={text} onChange={(e) => setText(e.target.value)} />
      <button onClick={handleSendMessage}>Send</button>
    </div>
  );
};

export default Chat;
