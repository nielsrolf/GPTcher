import React, { useEffect, useState } from 'react'
import { useSession, useSupabaseClient } from '@supabase/auth-helpers-react'
import Menu from '../components/Menu'
import Starfield from '../components/Starfield'
import { useRouter } from 'next/router'
import config from '../config';
import { Auth, ThemeSupa } from '@supabase/auth-ui-react'



interface ExerciseData {
  id: string;
  language: string;
  topic: string;
  content_description: string;
  grammar?: string;
  exercise_number: number;
  task_description: string;
  user_id?: string;
}


const Exercise: React.FC<ExerciseData> = ({
  id,
  topic,
  grammar,
  exercise_number,
  language,
  content_description,
  task_description,
}) => {
  const router = useRouter();

  const handleClick = () => {
    router.push(`/exercises/${id}`);
  };

  return (
    <button style={{ width: "100%" }} onClick={handleClick}>
      {topic} {grammar ? `- ${grammar}` : ""} ({exercise_number})
    </button>
  );
};


interface ExercisesProps {
  access_token: string;
}


const Exercises: React.FC<ExercisesProps> = ({ access_token }) => {
  const [doneExercises, setDoneExerciseDatas] = useState<ExerciseData[]>([]);
  const [continueExercises, setContinueExerciseDatas] = useState<ExerciseData[]>([]);
  const [nextExercises, setNextExerciseDatas] = useState<ExerciseData[]>([]);
  const [error, setError] = useState<boolean | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const headers = new Headers({
          Authorization: `Bearer ${access_token}`,
          'Content-Type': 'application/json'
      });
        
        const [
          doneResponse,
          // continueResponse,
          nextResponse,
        ] = await Promise.all([
          fetch(`${config.backendUrl}/exercises/done`, {
            headers: {
                'Authorization': `Bearer ${access_token}`,
                'Content-Type': 'application/json'
            }}),
          // fetch(`${config.backendUrl}/exercises/continue`, {
          //   headers: {
          //       'Authorization': `Bearer ${access_token}`,
          //       'Content-Type': 'application/json'
          //   }}),
          fetch(`${config.backendUrl}/exercises/new`, {
            headers: {
                'Authorization': `Bearer ${access_token}`,
                'Content-Type': 'application/json'
            }}),
        ]);
    
        if (!doneResponse.ok) {
          throw new Error(
            `Could not fetch done exercises, received status code: ${doneResponse.status}`
          );
        }

        // if (!continueResponse.ok) {
        //   throw new Error(
        //     `Could not fetch continue exercises, received status code: ${continueResponse.status}`
        //   );
        // }

        if (!nextResponse.ok) {
          throw new Error(
            `Could not fetch next exercises, received status code: ${nextResponse.status}`
          );
        }

        // const [doneData, continueData, nextData] = await Promise.all([
          const [doneData, nextData] = await Promise.all([
          doneResponse.json(),
          // continueResponse.json(),
          nextResponse.json(),
        ]);

        setDoneExerciseDatas(doneData);
        // setContinueExerciseDatas(continueData);
        setNextExerciseDatas(nextData);
      } catch (error) {
        setError(true);
      }
    };

    fetchData();
  }, []);

  // if screen is > 500px, set width to 500px, else to 100%
  const [isMobile, setIsMobile] = useState(false);
    const checkMobile = () => {
        if (window.innerWidth < 600) {
            setIsMobile(true);
        } else {
            setIsMobile(false);
        }
    };

    useEffect(() => {
        checkMobile();
        window.addEventListener('resize', checkMobile);
        return () => window.removeEventListener('resize', checkMobile);
    }, []);

    return (
      <div>
          <h1>Exercises</h1>
          {error && <div>Sorry, something went wrong :/</div>}
          <h2>Done</h2>
          {doneExercises.map((exercise) => (
              <Exercise key={exercise.id} {...exercise}/>
          ))}
          {/* <h2>Continue</h2>
          {continueExercises.map((exercise) => (
            <Exercise key={exercise.id} {...exercise}/>
          ))} */}
          <h2>Next</h2>
          {nextExercises.map((exercise) => (
            <Exercise key={exercise.id} {...exercise}/>
          ))}
      </div>
    );
};


const ExercisesPage = () => {
  const session = useSession()
  const supabase = useSupabaseClient()


  // if screen is > 500px, set width to 500px, else to 100%
  const [isMobile, setIsMobile] = useState(false);
    const checkMobile = () => {
        if (window.innerWidth < 600) {
            setIsMobile(true);
        } else {
            setIsMobile(false);
        }
    };

    useEffect(() => {
        checkMobile();
        window.addEventListener('resize', checkMobile);
        return () => window.removeEventListener('resize', checkMobile);
    }, []);

  return (
    <div>
      <Starfield />
      <div id="content">
      <Menu session={session} supabase={supabase} />
      {!session ? (
        <div style={{width: isMobile ? '100%' : '500px', margin: '0 auto', minHeight: '60vh', marginTop: '20vh'}}>
          <Auth supabaseClient={supabase} appearance={{ theme: ThemeSupa }} theme="dark" />
        </div>
      ) : (
        <Exercises access_token={session.access_token} />
      )}
    </div>
    </div>
    
  )
}


export default ExercisesPage;