import React, { useState, useEffect, useRef } from 'react';
import config from '../config';
import StudentMessage from '../components/StudentMessage';
import TeacherMessage from '../components/TeacherMessage';
import Button from '@mui/material/Button';
import DeleteIcon from '@mui/icons-material/Delete';
import SendIcon from '@mui/icons-material/Send';
import Stack from '@mui/material/Stack';


interface ChatProps {
  access_token: string;
  // optional sessionId
  sessionId?: string;
}


const Chat: React.FC<ChatProps> = ({ access_token, sessionId }) => {
  const [messages, setMessages] = useState<{ id: string, text: string, sender: string, text_en: string, text_translated: string, voice: string, created_at: string, session: string, evaluation: any, user_id: string }[]>([]);
  const [text, setText] = useState('');
  const lastMessageRef = useRef<HTMLDivElement | null>(null);
  const endpoint = sessionId ? `/session/${sessionId}` : '/chat';
  console.log(endpoint)

  useEffect(() => {
    try {
      if (lastMessageRef.current) {
        lastMessageRef.current.scrollIntoView({ behavior: 'smooth' });
      }
    } catch (error) {
      console.log(error);
    }
  }, [messages]);
  
  useEffect(() => {
    async function fetchChatHistory() {
      const response = await fetch(`${config.backendUrl}${endpoint}`, {
        headers: {
            Authorization: `Bearer ${access_token}`,
            'Content-Type': 'application/json'
        }});
      const data = await response.json();
      setMessages(data);
      try {
        if (lastMessageRef.current) {
          lastMessageRef.current.scrollIntoView({ behavior: 'smooth' });
        }
      } catch (error) {
        console.log(error);
      }
    }
    fetchChatHistory();
  }, []);

  const handleSendMessage = async () => {
    const userMessage = {
        'text': text,
        'sender': 'Student',
        'id': String(Math.random()),
        'text_en': '',
        'text_translated': '',
        'voice': '',
        'created_at': '',
        'session': '',
        'evaluation': '',
        'user_id': ''
    }
    setMessages([...messages, userMessage]);
    if(lastMessageRef.current){
      lastMessageRef.current.scrollIntoView({ behavior: 'smooth' });
    }
    setText('')
    const response =await fetch(`${config.backendUrl}${endpoint}`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${access_token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text }),
    });
    const data = await response.json();
    setMessages([...messages, ...data]);
    setText('');
  };

  /* Key listener: on enter send message */
  useEffect(() => {
    const handleKeyDown = (event: any) => {
      if (event.key === 'Enter') {
        handleSendMessage();
      }
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [text]);


  const clearChat = async () => {
    setMessages([]);
    const response = await fetch(`${config.backendUrl}/clearchat`, {
      headers: {
        Authorization: `Bearer ${access_token}`,
        'Content-Type': 'application/json'
    }});
    const data = await response.json();
    setMessages(data);
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
      {messages.map((message, index) => (
          message.sender === 'Student'
            ? <StudentMessage key={index} message={message} isExercise={sessionId!==undefined}/>
            : <TeacherMessage key={index} message={message} ref={index === messages.length - 1 ? lastMessageRef : null} />
      ))}
      </div>

      <div className="input-container">
        {sessionId === undefined && (
          <button  style={{borderRadius: '5px', marginRight: '5px'}} onClick={clearChat}>
            <DeleteIcon />
          </button>
        )}
        <textarea className="input-text-area" value={text} onChange={(e) => setText(e.target.value)} />
        {/* <button onClick={handleSendMessage}>Send</button>
        <DeleteForeverIcon onClick={clearChat} /> */}
        <button style={{borderRadius: '5px', marginLeft: '5px'}} onClick={handleSendMessage}>
          <SendIcon />
        </button>
      </div>
    </div>
  );
};

export default Chat;
