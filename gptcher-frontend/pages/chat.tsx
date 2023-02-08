import { Auth, ThemeSupa } from '@supabase/auth-ui-react'
import { useSession, useSupabaseClient } from '@supabase/auth-helpers-react'
import Chat from '../components/Chat'
import Menu from '../components/Menu'
import Starfield from '../components/Starfield'
import { useEffect, useState } from 'react'

const Home = () => {
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
        <Chat access_token={session.access_token} />
      )}
    </div>
    </div>
    
  )
}

export default Home
