import React, { useState, useEffect} from 'react';
import ExerciseSession from '../../components/ExerciseSession';
import { useSession, useSupabaseClient } from '@supabase/auth-helpers-react'
import Menu from '../../components/Menu'
import Starfield from '../../components/Starfield'
import { Auth, ThemeSupa } from '@supabase/auth-ui-react'



const ExercisePage: React.FC = () => {
    const session = useSession()
    const supabase = useSupabaseClient()

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
            <ExerciseSession access_token={session.access_token} />
          )}
        </div>
      </div>
    )
  }

export default ExercisePage;
