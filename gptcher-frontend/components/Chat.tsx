import React, { useState, useEffect } from 'react';
import config from '../config';
import parse from 'html-react-parser';




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
    const userMessage = {
        'text': text,
        'sender': 'Student',
        'id': Math.random()
    }
    setMessages([...messages, userMessage]);
    setText('')
    const response =await fetch(`${config.backendUrl}/chat`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${session.access_token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text }),
    });
    const data = await response.json();
    setMessages([...messages, userMessage, ...data]);
    setText('');
  };

  useEffect(() => {
    const handleNewMessage = (newMessage: any) => {
      setMessages([...messages, newMessage]);
    };
    // Add event listener for new messages here
  }, [messages]);

  return (
    <div className="chat-container">
      <div className="messages-container">
        {messages.map((message) => (
          <div key={message.id} className={`message-container ${message.sender === 'Teacher' ? 'teacher-message' : 'student-message'}`}>
            <div>
                {parse(message.text.replace('</b>', '</b><hr>'))}
            </div>
          </div>
        ))}
      </div>
      <div className="input-container">
        <textarea className="input-text-area" value={text} onChange={(e) => setText(e.target.value)} />
        <button onClick={handleSendMessage}>Send</button>
      </div>
    </div>
  );
};

export default Chat;
