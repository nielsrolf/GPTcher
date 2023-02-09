import React from 'react';
import { useRouter } from 'next/router';

const ExerciseSession: React.FC = () => {
  const router = useRouter();
  const { exercise_id } = router.query;

  return (
    <div>
      <h1>Exercise Session</h1>
      <p>Exercise ID: {exercise_id}</p>
    </div>
  );
};

export default ExerciseSession;
