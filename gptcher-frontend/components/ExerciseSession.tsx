import React from 'react';
import { useRouter } from 'next/router';
import { useState, useEffect } from 'react';
import config from '../config';
import Chat from './Chat';

interface ChatProps {
  access_token: string;
}


const ExerciseSession: React.FC<ChatProps> = ({ access_token }) => {
  const router = useRouter();
  const { exercise_id } = router.query;
  const [sessionId, setSessionId] = useState<string>('');

  console.log("Exercise ID:", exercise_id)

  useEffect(() => {
    const setExercise = async () => {
      if(!exercise_id) return;
      try {
        const response = await fetch(`${config.backendUrl}/exercise/${exercise_id}`, {
          headers: {
            Authorization: `Bearer ${access_token}`,
            'Content-Type': 'application/json'
        }});
        const data = await response.json();
        console.log("Created this session:", data.session)
        setSessionId(data.session);
      } catch (error) {
        console.log(error);
      }
    }
    setExercise();
    }, [exercise_id]);
    
  return (
    <div>
        {sessionId !== '' ? <Chat access_token={access_token} sessionId={sessionId} /> : <div>Loading...</div>}
    </div>
  );
};

export default ExerciseSession;
